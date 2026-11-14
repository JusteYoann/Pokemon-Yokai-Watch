"""Préflight : aucun téléchargement ni build avec des fichiers incorrects."""
from pathlib import Path
import hashlib
import importlib.util
import tempfile
import unittest
from unittest.mock import patch
P=Path(__file__).resolve().parents[1]/'SCRIPTS/emerald_inputs.py'
spec=importlib.util.spec_from_file_location('emerald_inputs',P)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class EmeraldInputsTests(unittest.TestCase):
    def test_missing_file(self):
        with tempfile.TemporaryDirectory() as t:
            with self.assertRaisesRegex(ValueError,'manquant'):
                m.verify_file(Path(t)/'absent.gba','0'*40,'Hack')

    def test_real_digest_not_extension(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)/'fixture.gba';p.write_bytes(b'not a game')
            digest=hashlib.sha1(p.read_bytes()).hexdigest()
            self.assertEqual(m.verify_file(p,digest,'Fixture'),digest)
            with self.assertRaisesRegex(ValueError,'SHA-1'):
                m.verify_file(p,'0'*40,'Fixture')

    def test_invalid_inputs_do_not_create_work_directory(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)/'bad.gba';p.write_bytes(b'wrong');work=Path(t)/'work'
            with self.assertRaises(ValueError):m.validate(p,p,'us',work)
            self.assertFalse(work.exists())

    def test_language_cannot_select_english_generator_as_us(self):
        with tempfile.TemporaryDirectory() as t:
            with self.assertRaisesRegex(ValueError,'Langue'):
                m.validate(Path(t)/'hack',Path(t)/'base','en',Path(t)/'work')

    def test_mismatching_resume_is_rejected(self):
        with tempfile.TemporaryDirectory() as t:
            work=Path(t)/'work';work.mkdir();(work/'.yokai_build_inputs.json').write_text('{}')
            with patch.object(m,'verify_file',return_value='checked'):
                with self.assertRaisesRegex(ValueError,'autre version'):
                    m.validate(Path(t)/'hack',Path(t)/'base','us',work)

if __name__=='__main__':unittest.main()
