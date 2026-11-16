"""Compatibility and progression contracts; native execution is tested separately."""
import json
from pathlib import Path
import unittest

DATA=json.loads((Path(__file__).resolve().parents[1]/'APWORLDS/pokemon_yokai_firered/checks.json').read_text())
ACTIVE=[c for c in DATA['checks'] if c['status']=='active']

class FireRedCatalog(unittest.TestCase):
    def test_original_fifteen_ids_remain(self):
        expected={0x594B2000+v for v in (0x156,0x157,0x158,0x1BE,1000,1001,0x239)}
        self.assertEqual(set(DATA['legacy_pickup_ids']),expected)
        self.assertTrue(expected.issubset(c['id'] for c in ACTIVE))
        self.assertEqual([c['id'] for c in DATA['badge_checks']],[0x594B1000+i for i in range(8)])

    def test_no_postgame_or_missable_ship_sources_activated(self):
        for c in ACTIVE:
            self.assertFalse(c['map'].startswith(('OneIsland','TwoIsland','ThreeIsland','FourIsland','FiveIsland','SixIsland','SevenIsland','CeruleanCave','SSAnne')))
            self.assertFalse(c.get('underfoot',False))
        self.assertEqual(len({c['id'] for c in ACTIVE}),len(ACTIVE))

    def test_aides_use_caught_thresholds_and_native_counter(self):
        self.assertEqual([c['caught_required'] for c in ACTIVE if c['kind']=='aide'],[10,20,30,40,50])
        cap=DATA['capture_capacity']
        self.assertGreaterEqual(cap['pre_flash_count'],10)
        self.assertGreaterEqual(cap['pre_surf_count_with_level30_evolutions'],50)
        self.assertNotIn(18,cap['pre_surf_species']) # retired, not an obtainable species
        self.assertIn('first151',cap['counter'])

    def test_all_seventy_four_ids_are_stable(self):
        old=json.loads((Path(__file__).parent/'fixtures/firered_74_ids.json').read_text())
        self.assertEqual(len(old),74)
        self.assertTrue(set(old).issubset({c['id'] for c in ACTIVE+DATA['badge_checks']}))

    def test_trainer_ledger_has_no_save_overlap_or_aliases(self):
        trainers=[c for c in ACTIVE if c['kind']=='trainer']
        self.assertEqual(sorted(c['persistent_index'] for c in trainers),list(range(len(trainers))))
        self.assertLessEqual(len(trainers),256)
        ids=[t for c in trainers for t in c['trainer_ids']]
        self.assertEqual(len(ids),len(set(ids)))
        for c in ACTIVE:
            if c['map']=='ViridianCity_Gym':self.assertEqual(c['access'],'surf')

    def test_all_reference_categories_have_evidence(self):
        ref=DATA['bulk_correspondence']
        self.assertEqual(ref['total'],1715)
        self.assertEqual(len(ref['by_category']),9)
        self.assertEqual(sum(ref['summary'].values()),1715)
        self.assertEqual(set(ref['summary']),{'compatible','a_adapter','absent_ou_incompatible'})
        self.assertTrue(all(any(r['category_evidence'] for r in ref['rows'] if r['category']==cat) for cat in ('SHOP_ITEM','TRAINER_REMATCH','FAME_ENTRY')))
        self.assertTrue(all(not r['integrated'] for r in ref['rows'] if r['category'] in ('SHOP_ITEM','TRAINER_REMATCH','FAME_ENTRY')))
        self.assertFalse(any(c.get('original_item')=='ITEM_NONE' for c in ACTIVE))

    def test_rng_is_explicitly_optional_and_never_a_required_gate(self):
        rng=[c for c in ACTIVE if c['access']=='optional_random']
        self.assertEqual([c['id'] for c in rng],[0x594B4002])
        self.assertFalse(rng[0]['mandatory'])
        self.assertNotIn('FLAG_ONI_QUEST_ACCEPTED',{c.get('flag') for c in ACTIVE})

if __name__=='__main__':unittest.main()
