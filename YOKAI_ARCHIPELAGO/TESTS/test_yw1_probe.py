from pathlib import Path
from types import SimpleNamespace
import importlib.util,unittest
from unittest.mock import Mock
P=Path(__file__).resolve().parents[1]/'CONNECTORS/3ds/probe_yokai_watch_1.py'
s=importlib.util.spec_from_file_location('yw1_probe',P);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)

class YW1ProbeTests(unittest.TestCase):
    def rpc(self,title=None):
        rpc=Mock();rpc.processes.return_value=[SimpleNamespace(title_id=m.TITLE_ID if title is None else title,pid=42)]
        rpc.current_process.return_value=42;rpc.read.return_value=b'abcd';return rpc
    def test_identity_without_memory_read(self):
        rpc=self.rpc();result=m.collect(rpc,[])
        self.assertEqual(result['title_id'],'0004000000167800');rpc.read.assert_not_called();rpc.write.assert_not_called()
    def test_other_game_is_rejected_before_any_read(self):
        rpc=self.rpc(0x00040000001B2900)
        with self.assertRaises(ValueError):m.collect(rpc,[(0x100000,4)])
        rpc.read.assert_not_called();rpc.write.assert_not_called()
    def test_other_process_is_rejected(self):
        rpc=self.rpc();rpc.current_process.return_value=7
        with self.assertRaises(ValueError):m.collect(rpc,[(0x100000,4)])
        rpc.read.assert_not_called()
    def test_explicit_range_only(self):
        rpc=self.rpc();report=m.collect(rpc,[(0x100000,4)])
        rpc.read.assert_called_once_with(0x100000,4);rpc.write.assert_not_called()
        self.assertFalse(report['game_memory_written']);self.assertEqual(report['reads'][0]['hex'],'61626364')

if __name__=='__main__':unittest.main()
