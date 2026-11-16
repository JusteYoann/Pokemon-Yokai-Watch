"""Prevent an apparently valid four-game seed from silently replacing a game."""
import importlib.util,json,tempfile,unittest,zipfile
from pathlib import Path
PROJECT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('four',PROJECT/'SCRIPTS/generate_four_game_seed.py')
four=importlib.util.module_from_spec(spec);spec.loader.exec_module(four)

class FourGamePreflight(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name);self.players=PROJECT/'CONFIG/createurs/quatre_jeux'
        self.custom=self.root/'custom_worlds';self.custom.mkdir()
    def packages(self,wrong_emerald=False):
        for package,game in four.WORLDS.items():
            with zipfile.ZipFile(self.custom/f'{package}.apworld','w') as z:
                z.writestr(f'{package}/archipelago.json',json.dumps({'game':'Pokemon Emerald' if wrong_emerald and 'emerald' in package else game,'world_version':'0.2.1'}))
                if package=='pokemon_yokai_emerald':
                    z.writestr(f'{package}/constants.py','ROM_NAME = \"pokemon emerald / yokai ap fr2\"')
                if package=='pokemon_yokai_firered':
                    catalog=json.loads((PROJECT/'APWORLDS/pokemon_yokai_firered/checks.json').read_text())
                    z.writestr(f'{package}/build.json',json.dumps({'catalog_sha256':catalog['catalog_sha256']}))
    def test_missing_emerald_is_blocking(self):
        self.packages();(self.custom/'pokemon_yokai_emerald.apworld').unlink()
        with self.assertRaisesRegex(FileNotFoundError,'pokemon_yokai_emerald'):four.preflight(self.root,self.players)
    def test_vanilla_emerald_is_not_a_substitute(self):
        self.packages(wrong_emerald=True)
        with self.assertRaisesRegex(ValueError,'Mauvais monde'):four.preflight(self.root,self.players)
    def test_exact_four_slots_and_catalog(self):
        self.packages();self.assertEqual(set(four.preflight(self.root,self.players)),set(four.WORLDS))
        other=self.root/'players';other.mkdir()
        (other/'one.yaml').write_text('name: Someone\ngame: Yo-kai Watch 1\n')
        with self.assertRaises(ValueError):four.preflight(self.root,other)

if __name__=='__main__':unittest.main()
