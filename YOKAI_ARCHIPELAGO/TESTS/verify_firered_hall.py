#!/usr/bin/env python3
"""Test ciblé de la vraie séquence Panthéon, avec équipe et position préparées.

Ne constitue pas un parcours de Ligue : le dernier adversaire n'est pas combattu
ici. Aucun flag de victoire ni compteur Panthéon n'est injecté.
"""
import argparse
import ctypes as C
import hashlib
import json
import os
from pathlib import Path
import sys
import traceback

def main():
    p=argparse.ArgumentParser(description=__doc__)
    for name in ('build','libretro','out'):p.add_argument('--'+name,type=Path,required=True)
    a=p.parse_args()
    os.environ.update(YOKAI_QA_ROM=str(a.build/'pokefirered_audio.gba'),YOKAI_QA_ELF=str(a.build/'pokefirered_audio.elf'),MGBA_LIBRETRO_PATH=str(a.libretro))
    sys.path.insert(0,str(a.build/'tools/yokai'))
    from mgba_new_game import new_game
    from mgba_rpc import Emulator
    from postgame_qa_common import QA
    report={'passed':False,'kind':'native_hall_of_fame_script_fixture','final_boss_fought':False,
            'victory_flag_injected':False,'rom_sha256':hashlib.sha256((a.build/'pokefirered_audio.gba').read_bytes()).hexdigest(),'checks':[]}
    r=None
    def ok(name,condition):
        if not condition:raise AssertionError(name)
        report['checks'].append(name);print('PASS',name,flush=True)
    try:
        r=new_game();q=QA.__new__(QA);q.r=r
        q.reverse={address|1:name for name,address in r.symbols.items()}
        groups=json.loads((a.build/'data/maps/map_groups.json').read_text())
        q.maps={name:(i,j) for i,key in enumerate(groups['group_order']) for j,name in enumerate(groups[key])}
        q.mon(0,65,50)
        ok('New game has no Hall of Fame record',r.call('GetGameStat',10)==0)
        q.warp('PokemonLeague_HallOfFame',5,12)
        q.wait(lambda:r.call('GetGameStat',10)>0,limit=24000)
        ok('Native Hall of Fame scene created a record',r.call('GetGameStat',10)==1)
        # Let the native Flash save finish; no new manual save overwrites it.
        r.keys=set();r.run(180)
        r.lib.retro_get_memory_data.argtypes=[C.c_uint];r.lib.retro_get_memory_data.restype=C.c_void_p
        r.lib.retro_get_memory_size.argtypes=[C.c_uint];r.lib.retro_get_memory_size.restype=C.c_size_t
        battery=C.string_at(r.lib.retro_get_memory_data(0),r.lib.retro_get_memory_size(0))
        r.close();r=Emulator()
        r.lib.retro_get_memory_data.argtypes=[C.c_uint];r.lib.retro_get_memory_data.restype=C.c_void_p
        C.memmove(r.lib.retro_get_memory_data(0),battery,len(battery));r.lib.retro_reset();r.run(600)
        r.keys={3};r.run(2);r.keys=set();r.run(180)
        q.r=r;q.wait(lambda:q.callback()=='CB2_Overworld' and q.unlocked(),limit=16000)
        r.run(60)
        ok('Native Hall save survives cold Continue',r.call('GetGameStat',10)==1)
        ok('AP Goal reported after native Hall record and cold Continue',r.read(r.symbols['gYokaiAPMailbox']+42,1)==b'\1')
        report['passed']=True
    except Exception as e:report['error']=str(e);traceback.print_exc()
    finally:
        if r:r.close()
        a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(report,indent=2)+'\n')
    return 0 if report['passed'] else 1

if __name__=='__main__':raise SystemExit(main())
