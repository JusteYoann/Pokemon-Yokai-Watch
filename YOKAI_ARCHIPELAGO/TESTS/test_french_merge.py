"""Vérifie la conservation des contrats de variables lors de la traduction."""
from pathlib import Path
import importlib.util
import unittest
P=Path(__file__).resolve().parents[1]/'PATCHES/pokemon_yokai_emerald/merge_french_base.py'
spec=importlib.util.spec_from_file_location('french_merge',P)
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)

class FrenchMergeTests(unittest.TestCase):
    def test_same_placeholders_allow_localized_order(self):
        a='Text::\n\t.string "{PLAYER} receives {STR_VAR_1}!$"\n'
        b='Text::\n\t.string "{STR_VAR_1} remis à {PLAYER}!$"\n'
        result,n,skipped=module.localize(a,b,True)
        self.assertEqual(result,b);self.assertEqual(n,1);self.assertEqual(skipped,[])

    def test_changed_item_buffer_is_not_silently_translated(self):
        a='Text::\n\t.string "{STR_VAR_1}$"\n';b='Text::\n\t.string "{STR_VAR_2}$"\n'
        result,n,skipped=module.localize(a,b,True)
        self.assertEqual(result,a);self.assertEqual(n,0);self.assertEqual(skipped,['Text'])

    def test_ap_logic_and_new_label_are_preserved(self):
        a='Event::\n\tsetflag FLAG_AP\nText::\n\t.string "Hello$"\nNew::\n\t.string "AP$"\n'
        b='Event::\n\tend\nText::\n\t.string "Bonjour$"\n'
        result,n,_=module.localize(a,b,True)
        self.assertIn('setflag FLAG_AP',result);self.assertIn('"Bonjour$"',result)
        self.assertIn('New::',result);self.assertEqual(n,1)

    def test_c_string_semicolon_and_escaped_quote(self):
        a='static const u8 a[] = _("EN; \\\"quote\\\"");\nconst u8 b[] = _("KEEP {STR_VAR_1}");\n'
        b='const u8 a[] = _("FR; \\\"citation\\\"");\nconst u8 b[] = _("CHANGE {STR_VAR_2}");\n'
        result,n,skipped=module.localize(a,b,False)
        self.assertIn('static const u8 a[]',result);self.assertIn('FR;',result)
        self.assertIn('KEEP {STR_VAR_1}',result);self.assertEqual(n,1);self.assertEqual(skipped,['b'])

if __name__=='__main__':unittest.main()
