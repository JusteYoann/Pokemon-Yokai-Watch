#!/usr/bin/env python3
"""Client AP officiel sans GUI, port mGBA explicite et traces de mémoire réelle.

Aucune mémoire simulée, aucune injection de check et aucune sauvegarde chargée
par ce script. Le joueur utilise le jeu et le Lua dans mGBA. Un événement de
journal n'est pas à lui seul un certificat de test bout-en-bout.
"""
from __future__ import annotations
import argparse
import asyncio
import datetime
import importlib
import json
import logging
import os
from pathlib import Path
import sys


def arguments(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--archipelago', type=Path, required=True)
    p.add_argument('--server', default='localhost:38281')
    p.add_argument('--slot', required=True)
    p.add_argument('--emulator-port', type=int, default=43055, choices=range(43055, 43060))
    p.add_argument('--password-env', default='YOKAI_AP_PASSWORD')
    p.add_argument('--record', type=Path, required=True, help='Journal JSONL local des événements observés')
    p.add_argument('--duration', type=float, default=None, help='Arrêt après N secondes, sans résultat PASS implicite')
    a = p.parse_args(argv)
    if not (a.archipelago / 'CommonClient.py').is_file():
        p.error('--archipelago doit pointer vers les sources Archipelago 0.6.9')
    if a.duration is not None and a.duration <= 0:
        p.error('--duration doit être positif')
    return a


async def run(a):
    os.environ['SKIP_REQUIREMENTS_UPDATE'] = '1'
    sys.path.insert(0, str(a.archipelago.resolve()))
    import worlds  # registers the installed APWorld and its actual client
    import worlds._bizhawk as bizhawk
    from CommonClient import server_loop
    from worlds._bizhawk.context import BizHawkClientContext, _game_watcher
    from worlds.AutoWorld import AutoWorldRegister
    if 'Pokemon Yo-kai Emerald' not in AutoWorldRegister.world_types:
        raise RuntimeError("Installer l'APWorld Yo-kai Emerald généré localement dans custom_worlds")
    game = importlib.import_module('worlds.pokemon_yokai_emerald.client')
    bizhawk.BIZHAWK_SOCKET_PORT_RANGE_START = a.emulator_port
    bizhawk.BIZHAWK_SOCKET_PORT_RANGE_SIZE = 1
    a.record.parent.mkdir(parents=True, exist_ok=True)

    def event(kind, **fields):
        row = dict(time=datetime.datetime.now(datetime.timezone.utc).isoformat(), event=kind, **fields)
        with a.record.open('a', encoding='utf-8') as f:
            f.write(json.dumps(row, ensure_ascii=False) + '\n')
        logging.info('%s: %s', kind, fields)

    class RecordedContext(BizHawkClientContext):
        def on_package(self, cmd, args):
            super().on_package(cmd, args)
            if cmd == 'Connected':
                event('server_connected', slot=args.get('slot'), checked=len(args['checked_locations']),
                      missing=len(args['missing_locations']))
            elif cmd == 'ReceivedItems':
                event('received_items', index=args['index'], items=[i.item for i in args['items']])
            elif cmd == 'RoomUpdate' and 'checked_locations' in args:
                event('server_checked_locations', locations=args['checked_locations'])
            elif cmd == 'ConnectionRefused':
                event('connection_refused', errors=args.get('errors'))

        async def send_msgs(self, msgs):
            await super().send_msgs(msgs)
            for msg in msgs:
                if msg.get('cmd') == 'LocationChecks':
                    event('location_checks_sent', locations=msg['locations'])
                elif msg.get('cmd') == 'StatusUpdate':
                    event('status_sent', status=int(msg['status']))

    ctx = RecordedContext(a.server, os.environ.get(a.password_env))
    ctx.auth = a.slot
    ctx.username = a.slot
    ctx.server_task = asyncio.create_task(server_loop(ctx), name='ArchipelagoServer')
    ctx.run_cli()

    async def observe():
        previous = None
        while not ctx.exit_event.is_set():
            if ctx.client_handler is not None:
                if ctx.client_handler.game != 'Pokemon Yo-kai Emerald':
                    raise RuntimeError('Le port mGBA sélectionné contient un autre jeu')
                try:
                    pointer = (await bizhawk.read(ctx.bizhawk_ctx, [
                        (game.data.ram_addresses['gSaveBlock1Ptr'], 4, 'System Bus')]))[0]
                    sb = int.from_bytes(pointer, 'little')
                    if 0x02000000 <= sb < 0x02040000:
                        data = await bizhawk.guarded_read(ctx.bizhawk_ctx, [
                            (sb + 0x3700, 2, 'System Bus'),
                            (game.data.ram_addresses['gArchipelagoReceivedItem'] + 4, 1, 'System Bus')], [
                            (game.data.ram_addresses['gSaveBlock1Ptr'], pointer, 'System Bus'),
                            (game.data.ram_addresses['gMain'] + 4,
                             (game.data.ram_addresses['CB2_Overworld'] + 1).to_bytes(4, 'little'), 'System Bus')])
                        if data is not None:
                            state = (int.from_bytes(data[0], 'little'), data[1][0], ctx.rom_hash,
                                     len(ctx.checked_locations), len(ctx.items_received))
                            if state != previous:
                                event('game_memory_observed', applied_item_count=state[0], mailbox_full=state[1],
                                      rom_crc=state[2], server_checks=state[3], server_items=state[4])
                                previous = state
                except (bizhawk.RequestFailedError, bizhawk.NotConnectedError):
                    pass
            await asyncio.sleep(0.25)

    event('session_start', slot=a.slot, game='Pokemon Yo-kai Emerald', emulator_port=a.emulator_port,
          test_kind='real_emulator_required', automatic_pass=False)
    tasks = [asyncio.create_task(_game_watcher(ctx), name='GameWatcher'),
             asyncio.create_task(observe(), name='MemoryObserver'),
             asyncio.create_task(ctx.exit_event.wait(), name='ExitWait')]
    if a.duration:
        tasks.append(asyncio.create_task(asyncio.sleep(a.duration), name='Duration'))
    try:
        done, _ = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
        for task in done:
            if not task.cancelled() and task.exception():
                raise task.exception()
    finally:
        ctx.exit_event.set()
        for task in tasks:
            task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)
        bizhawk.disconnect(ctx.bizhawk_ctx)
        await ctx.shutdown()
        event('session_end', automatic_pass=False)


def main(argv=None):
    a = arguments(argv)
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    try:
        asyncio.run(run(a))
    except KeyboardInterrupt:
        return 130
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
