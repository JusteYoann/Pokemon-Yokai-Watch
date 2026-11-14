#!/usr/bin/env python3
"""Vrai mGBA/C, fixtures contrôlées ; pas un parcours complet ni une preuve réseau.

Construit une partie neuve avec les boutons. Les états de sac plein et le badge
sont ensuite injectés EXPLICITEMENT comme fixtures. Les dons sont consommés par
le C du jeu en frames normales. Aucun fichier de sauvegarde personnel n'est lu.
"""
from __future__ import annotations
import argparse
import ctypes as C
import hashlib
import json
import os
from pathlib import Path
import struct
import sys
import traceback


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--build',type=Path,required=True);p.add_argument('--libretro',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    os.environ['YOKAI_QA_ROM']=str(a.build/'pokefirered_audio.gba')
    os.environ['YOKAI_QA_ELF']=str(a.build/'pokefirered_audio.elf')
    os.environ['MGBA_LIBRETRO_PATH']=str(a.libretro)
    sys.path.insert(0,str(a.build/'tools/yokai'))
    from mgba_new_game import new_game
    from mgba_rpc import Emulator
    report={'passed':False,'type':'native_mgba_fixture','network_server_tested':False,
            'badge_source':'FlagSet fixture, no gym battle played',
            'rom_sha256':hashlib.sha256((a.build/'pokefirered_audio.gba').read_bytes()).hexdigest(),'checks':[]}
    r=None
    def ok(name,condition):
        if not condition:raise AssertionError(name)
        report['checks'].append(name);print('PASS',name,flush=True)
    def u16(address):return struct.unpack('<H',r.read(address,2))[0]
    seed=hashlib.sha256(b'native-fixture-session').digest()[:16]
    try:
        r=new_game();r.run(30);box=r.symbols['gYokaiAPMailbox']
        ok('Mailbox below native fixture trampoline',box+48<r.STUB)
        sb1=r.u32(r.symbols['gSaveBlock1Ptr']);sb2=r.u32(r.symbols['gSaveBlock2Ptr'])
        ok('Native mailbox initialised safely',r.u32(box)==0x31504B59 and r.read(box+38,1)==b'\1')
        protected={'vacuum_state':(sb1+0x3A94,64),'nuzlocke':(sb1+0x348C,400),
                   'before_gap':(sb2+0xB20+0x2F0,16),'after_gap':(sb2+0xB20+0x340,64)}
        snapshots={k:r.read(addr,n) for k,(addr,n) in protected.items()}
        held=bytes(range(80));r.write(sb2+0xB20+0x380,held)
        def bind(value=seed,slot=1):
            r.write(box+8,struct.pack('<H',slot));r.write(box+16,value)
            r.write(box+6,struct.pack('<H',1));r.run(4)
        def gift(item,index):
            r.write(box+10,struct.pack('<HI',item,index));r.write(box+6,struct.pack('<H',2));r.run(4)
        before=r.call('BagGetQuantityByItemId',13)
        bind();ok('Seed and slot bound in native save',r.read(box+39,1)==b'\1' and u16(box+36)==0)
        gift(13,1)
        ok('Real native AddBagItem consumes first request',r.call('BagGetQuantityByItemId',13)==before+1 and r.u32(box+32)==1)
        gift(13,1)
        ok('Replayed request does not give twice',r.call('BagGetQuantityByItemId',13)==before+1 and r.u32(box+32)==1)
        gift(13,3)
        ok('Out-of-order request rejected',u16(box+36)==2 and r.u32(box+32)==1)
        gift(289,2)
        ok('Progression item outside bonus whitelist rejected',u16(box+36)==4 and r.u32(box+32)==1)
        bind(b'wrong-session!!!')
        ok('Other seed refused without altering counter',u16(box+36)==1 and r.u32(box+32)==1)
        bind();bind(seed,2)
        ok('Other slot refused',u16(box+36)==1 and r.u32(box+32)==1)
        bind()
        bag=sb1+0x310;original=r.read(bag,0xA8)
        for i in range(42):
            r.write(bag+4*i,struct.pack('<H',13));r.call('SetBagItemQuantity',bag+4*i+2,999)
        gift(13,2)
        ok('Full native bag retains unacknowledged request',u16(box+36)==3 and u16(box+6)==2 and r.u32(box+32)==1)
        r.write(bag,original);r.run(6)
        ok('Freeing bag space retries same request exactly once',u16(box+6)==0 and r.u32(box+32)==2 and r.call('BagGetQuantityByItemId',13)==before+2)
        for key,(address,n) in protected.items():ok('Protected storage unchanged: '+key,r.read(address,n)==snapshots[key])
        r.call('BlastersBackupParty');r.call('BlastersRestoreParty',1);r.run(4)
        ok('AP ledger survives real Blasters backup/restore',r.u32(sb2+0xE20+24)==2)
        ok('Vacuum held-mon region preserved',r.read(sb2+0xB20+0x380,80)==held)
        r.call('FlagSet',0x820);r.run(5)
        ok('Badge flag fixture reflected in native check bits',u16(box+40)&1==1)
        r.call('SaveMapView');save_result=r.call('TrySavingData',0);r.run(10)
        ok('Native save routine succeeds',save_result==1)
        r.lib.retro_get_memory_data.argtypes=[C.c_uint];r.lib.retro_get_memory_data.restype=C.c_void_p
        r.lib.retro_get_memory_size.argtypes=[C.c_uint];r.lib.retro_get_memory_size.restype=C.c_size_t
        battery=C.string_at(r.lib.retro_get_memory_data(0),r.lib.retro_get_memory_size(0))
        report['battery_bytes']=len(battery);r.close();r=None
        r=Emulator();r.lib.retro_get_memory_data.argtypes=[C.c_uint];r.lib.retro_get_memory_data.restype=C.c_void_p
        C.memmove(r.lib.retro_get_memory_data(0),battery,len(battery));r.lib.retro_reset();r.run(600)
        r.keys={3};r.run(2);r.keys=set();r.run(180)
        for i in range(9000):
            r.keys={8} if i%16<3 else set();r.run()
            if r.u32(r.symbols['gMain']+4)==r.symbols['CB2_Overworld']|1 and r.read(r.symbols['sLockFieldControls'],1)==b'\0':break
        else:raise AssertionError('Native cold Continue did not reach player control')
        r.keys=set();r.run(60);box=r.symbols['gYokaiAPMailbox']
        ok('Native cold Continue reloads applied item count',r.u32(box+32)==2)
        ok('Native cold Continue reloads inventory',r.call('BagGetQuantityByItemId',13)==before+2)
        bind();gift(13,2)
        ok('Reconnect replay after cold restart still idempotent',r.call('BagGetQuantityByItemId',13)==before+2 and r.u32(box+32)==2)
        report['passed']=True
    except BaseException as e:
        report['error']=str(e);traceback.print_exc()
    finally:
        if r:r.close()
        a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(report,indent=2)+'\n')
    return 0 if report['passed'] else 1

if __name__=='__main__':raise SystemExit(main())
