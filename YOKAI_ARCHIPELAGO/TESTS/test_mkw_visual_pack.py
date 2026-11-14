"""Test d'assemblage XML avec archives synthétiques, sans jeu ni mod réel."""
from pathlib import Path
import importlib.util,json,tempfile,unittest
import xml.etree.ElementTree as ET
P=Path(__file__).resolve().parents[1]/'PATCHES/mario_kart_wii/build_visual_pack.py'
s=importlib.util.spec_from_file_location('mkw_pack',P);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)

class MKWVisualPackTests(unittest.TestCase):
    def setUp(self):
        self.t=tempfile.TemporaryDirectory();self.p=Path(self.t.name);(self.p/'driver.szs').write_bytes(b'Yaz0'+b'fixture')
        self.data={'game_id':'RMCP01','files':[{'source':'driver.szs','disc':'/Race/Driver/lg.szs'}]}
        self.manifest=self.p/'manifest.json'
    def tearDown(self):self.t.cleanup()
    def build(self):
        self.manifest.write_text(json.dumps(self.data));return m.build(self.manifest,self.p/'out')
    def test_same_pal_game_file_replacement_only(self):
        result=self.build();xml=ET.parse(self.p/'out/riivolution/yokai-mkw.xml')
        self.assertEqual(xml.find('id').attrib,{'game':'RMCP','developer':'01'})
        self.assertIsNone(xml.find('.//memory'));self.assertIsNone(xml.find('.//savegame'))
        self.assertEqual(len(xml.findall('.//file')),1);self.assertFalse(result['emulation_tested'])
        self.assertTrue(result['same_dolphin_instance_required'])
    def test_tracks_and_common_physics_rejected(self):
        for path in ['/Race/Course/luigi_circuit.szs','/Race/Common.szs','/Race/Kart/../../Course/track.szs']:
            self.data['files'][0]['disc']=path
            with self.subTest(path=path),self.assertRaises(ValueError):self.build()
    def test_wrong_region_rejected(self):
        self.data['game_id']='RMCE01'
        with self.assertRaises(ValueError):self.build()
    def test_wrong_archive_rejected(self):
        (self.p/'driver.szs').write_bytes(b'not an szs')
        with self.assertRaises(ValueError):self.build()
    def test_existing_pack_not_silently_overwritten(self):
        self.build()
        with self.assertRaises(ValueError):self.build()

if __name__=='__main__':unittest.main()
