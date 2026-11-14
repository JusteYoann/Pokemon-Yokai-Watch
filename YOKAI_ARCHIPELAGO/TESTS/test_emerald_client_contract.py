"""Contrats du vrai client AP généré, avec mémoire simulée (aucun jeu testé).

YOKAI_TEST_AP=<Archipelago> YOKAI_TEST_FLIT=<ap-pokeemerald épinglé>
SKIP_REQUIREMENTS_UPDATE=1 python -m unittest discover -s YOKAI_ARCHIPELAGO/TESTS -p test_emerald_client_contract.py -v
"""
from __future__ import annotations
import asyncio
import importlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import AsyncMock, patch
import zipfile

ROOT = Path(__file__).resolve().parents[2]
AP = os.environ.get('YOKAI_TEST_AP')
FLIT = os.environ.get('YOKAI_TEST_FLIT')

@unittest.skipUnless(AP and FLIT, 'Définir YOKAI_TEST_AP et YOKAI_TEST_FLIT ; mémoire de test simulée.')
class EmeraldClientContract(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls):
        os.environ['SKIP_REQUIREMENTS_UPDATE'] = '1'
        os.environ['AP_TEST_WORLDS'] = 'apquest'
        sys.path.insert(0, AP)
        cls.temp = tempfile.TemporaryDirectory()
        cls.build = Path(cls.temp.name) / 'build'
        cls.build.mkdir()
        # The fixture uses the upstream extracted tables, not Yo-kai graphics.
        # No generated package or copyrighted bytes are committed by this test.
        for name in ('extracted_data.json', 'base_patch.bsdiff4'):
            shutil.copy(Path(FLIT) / 'data' / name, cls.build / name)
        cls.output = Path(cls.temp.name) / 'out'
        subprocess.run([sys.executable, str(ROOT / 'YOKAI_ARCHIPELAGO/APWORLDS/pokemon_yokai_emerald/make_apworld.py'),
                        FLIT, str(cls.build), '--base', 'us', '--out', str(cls.output)], check=True,
                       stdout=subprocess.PIPE, text=True)
        cls.archive = cls.output / 'pokemon_yokai_emerald.apworld'
        import worlds
        from worlds.Files import APWorldContainer
        container = APWorldContainer(str(cls.archive)); container.read()
        source = worlds.WorldSource(str(cls.archive), is_zip=True, relative=False)
        worlds.add_apworld_spec(source, container)
        if not source.load():
            raise AssertionError(worlds.failed_world_loads)
        cls.module = importlib.import_module('worlds.pokemon_yokai_emerald.client')

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def setUp(self):
        self.client = self.module.PokemonEmeraldFlitClient()
        self.client.initialize_client()
        self.sb = 0x02020000
        self.guards = {'IN OVERWORLD': (0x03000004, b'\x01\x02\x03\x08', 'System Bus'),
                       'SAVE BLOCK 1': (0x03000000, self.sb.to_bytes(4, 'little'), 'System Bus')}
        self.ctx = SimpleNamespace(bizhawk_ctx=object(), items_received=[SimpleNamespace(item=13, flags=1),
                                  SimpleNamespace(item=14, flags=2)])

    def test_valid_manifest_and_extension(self):
        from worlds.Files import APWorldContainer
        from worlds.AutoWorld import AutoWorldRegister
        world = AutoWorldRegister.world_types['Pokemon Yo-kai Emerald']
        self.assertEqual(self.client.game, 'Pokemon Yo-kai Emerald')
        self.assertEqual(self.client.patch_suffix, '.apyokaiemerald')
        self.assertEqual(world.settings_key, 'pokemon_yokai_emerald_settings')
        container = APWorldContainer(str(self.archive)); container.read()
        self.assertEqual(container.game, self.client.game)
        with zipfile.ZipFile(self.archive) as z:
            manifest = json.loads(z.read('pokemon_yokai_emerald/archipelago.json'))
            self.assertEqual(manifest['compatible_version'], 7)
            self.assertEqual(json.loads(z.read('pokemon_yokai_emerald/yokai_build.json'))['base'], 'us')

    async def test_first_item_guarded_payload_then_commit(self):
        with patch.object(self.module.bizhawk, 'guarded_read', AsyncMock(return_value=[b'\0\0', b'\0'])), \
             patch.object(self.module.bizhawk, 'guarded_write', AsyncMock(return_value=True)) as write:
            await self.client.handle_received_items(self.ctx, self.guards)
        writes, guards = write.call_args.args[1:]
        addr = self.module.data.ram_addresses['gArchipelagoReceivedItem']
        self.assertEqual(writes[0], (addr, b'\x0d\0', 'System Bus'))
        self.assertEqual(writes[1], (addr + 2, b'\x01\0', 'System Bus'))
        self.assertEqual(writes[2], (addr + 5, [2], 'System Bus'))
        self.assertEqual(writes[-1], (addr + 4, [1], 'System Bus'))
        self.assertIn(self.guards['IN OVERWORLD'], guards)
        self.assertIn(self.guards['SAVE BLOCK 1'], guards)
        self.assertIn((self.sb + 0x3700, b'\0\0', 'System Bus'), guards)
        self.assertIn((addr + 4, [0], 'System Bus'), guards)

    async def test_resume_uses_persistent_counter_for_next_item(self):
        with patch.object(self.module.bizhawk, 'guarded_read', AsyncMock(return_value=[b'\x01\0', b'\0'])), \
             patch.object(self.module.bizhawk, 'guarded_write', AsyncMock(return_value=True)) as write:
            await self.client.handle_received_items(self.ctx, self.guards)
        writes = write.call_args.args[1]
        self.assertEqual(writes[0][1], b'\x0e\0')
        self.assertEqual(writes[1][1], b'\x02\0')

    async def test_no_duplicate_or_overwrite_when_busy_or_applied(self):
        for state in ([b'\x02\0', b'\0'], [b'\0\0', b'\1'], None):
            with self.subTest(state=state), \
                 patch.object(self.module.bizhawk, 'guarded_read', AsyncMock(return_value=state)), \
                 patch.object(self.module.bizhawk, 'guarded_write', AsyncMock()) as write:
                await self.client.handle_received_items(self.ctx, self.guards)
                write.assert_not_called()

    async def goal(self, names, active):
        ctx = SimpleNamespace(server=SimpleNamespace(socket=SimpleNamespace(closed=False)),
                              slot_data={'goals': names}, bizhawk_ctx=object(), items_received=[],
                              server_locations=set(), finished_game=False,
                              send_msgs=AsyncMock(), check_locations=AsyncMock())
        flags = bytearray(300)
        for flag in active:
            self.assertLess(flag, len(flags) * 8)
            flags[flag // 8] |= 1 << (flag % 8)
        with patch.object(self.module.bizhawk, 'read', AsyncMock(return_value=[self.sb.to_bytes(4,'little')])), \
             patch.object(self.module.bizhawk, 'guarded_read', AsyncMock(side_effect=[
                 [b'\0\0', b'\0'], [flags[:150]], [flags[150:]]])):
            await self.client.game_watcher(ctx)
        return ctx

    async def test_hall_of_fame_uses_system_flag_without_trainer_offset(self):
        flag = self.module.data.constants['FLAG_IS_CHAMPION']
        self.assertEqual(self.module.FLAG_IS_CHAMPION, flag)
        ctx = await self.goal(['Hall of Fame'], [flag])
        self.assertTrue(ctx.finished_game)
        ctx.send_msgs.assert_awaited_once()

    async def test_steven_goal_uses_defined_trainer_flag(self):
        ctx = await self.goal(['Steven'], [self.module.FLAG_DEFEATED_STEVEN])
        self.assertTrue(ctx.finished_game)

    async def test_both_goals_require_both_flags(self):
        ctx = await self.goal(['Hall of Fame', 'Steven'], [self.module.FLAG_IS_CHAMPION])
        self.assertFalse(ctx.finished_game)
        ctx.send_msgs.assert_not_called()

    async def test_missing_goal_does_not_grant_victory(self):
        ctx = await self.goal([], [])
        self.assertFalse(ctx.finished_game)
        ctx.send_msgs.assert_not_called()

if __name__ == '__main__':
    unittest.main()
