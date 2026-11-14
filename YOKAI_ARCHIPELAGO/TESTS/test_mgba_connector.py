"""Tests Lua exécutés avec lupa, transport/mémoire simulés, pas un jeu mGBA."""
from pathlib import Path
import unittest
try:
    from lupa import LuaRuntime
except ImportError:
    LuaRuntime = None
SOURCE = Path(__file__).resolve().parents[1] / 'CONNECTORS/mgba/connector_bizhawkclient_yokai.lua'
HARNESS = r'''
Q = {}; OUTPUT = {}; LOG = {}; BOUND = nil; WRITES = 0; CLOSED = false
console = {createBuffer=function() return {print=function() end} end,
           log=function(_, s) table.insert(LOG,s) end, error=function() end}
C = {PLATFORM={GB=1,GBA=2},CHECKSUM={CRC32=1}}
local mem = {readRange=function(_,address,n) return string.rep("\0",n) end,
             write8=function() WRITES=WRITES+1 end, size=function() return 4096 end}
emu = {platform=function() return 2 end, memory={bios=mem,cart0=mem,wram=mem,iwram=mem,vram=mem,oam=mem,io=mem},
       readRange=mem.readRange, write8=mem.write8, checksum=function() return "\0\0\0\0" end}
callbacks = {add=function() end}
CLIENT = {receive=function() if #Q > 0 then return table.remove(Q,1) end; return nil,99 end,
          send=function(_,s) table.insert(OUTPUT,s) end, add=function() end,
          close=function() CLOSED=true end, poll=function() end}
SERVER = {bind=function(_,host,port) BOUND=port; return true end, listen=function() return true end,
          add=function() end, close=function() end, accept=function() return CLIENT end}
socket={ERRORS={AGAIN=99},tcp=function() return SERVER end}
package.preload.base64=function() return {decode=function(s) local t={}; for i=1,#s do t[i]=s:byte(i) end; return t end,
                                        encode=function(s) return s end} end
package.preload.json=function() return {
 decode=function(s)
  if s=='[{"type":"PING"}]' then return {{type="PING"}} end
  if s=='guard-fail' then return {{type="GUARD",domain="EWRAM",address=0,expected_data="\1"},
                                {type="WRITE",domain="EWRAM",address=0,value="\5"}} end
  if s=='guard-pass' then return {{type="GUARD",domain="EWRAM",address=0,expected_data="\0"},
                                {type="WRITE",domain="EWRAM",address=0,value="\5"}} end
  assert(false,"bad json")
 end,
 encode=function(rows) local names={}; for _,r in ipairs(rows) do table.insert(names,r.type) end;
                      return table.concat(names,",") end
} end
'''

@unittest.skipUnless(LuaRuntime, 'Installer lupa pour les tests Lua simulés')
class MgbaConnectorTests(unittest.TestCase):
    def setUp(self):
        self.lua=LuaRuntime(unpack_returned_tuples=True)
        self.lua.execute(HARNESS)
        self.lua.execute(SOURCE.read_text())
        self.lua.execute('create_server(); accept(); tick()')

    def feed(self,s):
        self.lua.globals().Q[1]=s
        self.lua.globals().received()

    def outputs(self):
        g=self.lua.globals()
        return [g.OUTPUT[i] for i in range(1,len(g.OUTPUT)+1)]

    def test_fragmented_version_is_retained(self):
        self.feed('VER');self.assertEqual(self.outputs(),[])
        self.feed('SION\n');self.assertEqual(self.outputs(),['1\n'])

    def test_partial_tail_and_multiple_lines(self):
        self.feed('VERSION\nVER');self.assertEqual(self.outputs(),['1\n'])
        self.feed('SION\nVERSION\n');self.assertEqual(self.outputs(),['1\n']*3)

    def test_fragmented_json(self):
        self.feed('[{"type":');self.assertEqual(self.outputs(),[])
        self.feed('"PING"}]\n');self.assertEqual(self.outputs(),['PONG\n'])

    def test_failed_guard_prevents_all_following_writes(self):
        self.feed('guard-fail\n')
        self.assertEqual(self.lua.globals().WRITES,0)
        self.assertEqual(self.outputs(),['GUARD_RESPONSE,GUARD_RESPONSE\n'])

    def test_successful_guard_allows_write(self):
        self.feed('guard-pass\n')
        self.assertEqual(self.lua.globals().WRITES,1)
        self.assertEqual(self.outputs(),['GUARD_RESPONSE,WRITE_RESPONSE\n'])

    def test_invalid_json_disconnects_without_crashing(self):
        self.feed('not json\n')
        self.assertTrue(self.lua.globals().CLOSED)
        self.lua.execute('create_server(); accept()')
        self.feed('VERSION\n');self.assertEqual(self.outputs(),['1\n'])

    def test_separate_emulator_ports(self):
        self.assertEqual(self.lua.globals().BOUND,43055)
        second=LuaRuntime(unpack_returned_tuples=True);second.execute(HARNESS)
        second.globals().YOKAI_CONNECTOR_PORT=43056
        second.execute(SOURCE.read_text());second.execute('create_server()')
        self.assertEqual(second.globals().BOUND,43056)

if __name__=='__main__':unittest.main()
