#!/usr/bin/env python3
"""Actual native scripts with prepared positions/interaction/caught-bit fixtures.
No full playthrough, real catches, GUI Lua or random Terr'heure trigger claimed.
"""
import argparse,ctypes as C,hashlib,json,os,struct,sys,traceback
from pathlib import Path

def main():
    p=argparse.ArgumentParser(description=__doc__)
    for n in ('build','libretro','out'):p.add_argument('--'+n,type=Path,required=True)
    a=p.parse_args();os.environ.update(YOKAI_QA_ROM=str(a.build/'pokefirered_audio.gba'),YOKAI_QA_ELF=str(a.build/'pokefirered_audio.elf'),MGBA_LIBRETRO_PATH=str(a.libretro))
    sys.path.insert(0,str(a.build/'tools/yokai'))
    from mgba_new_game import new_game
    from mgba_rpc import Emulator
    from postgame_qa_common import QA
    data=json.loads((Path(__file__).resolve().parents[1]/'APWORLDS/pokemon_yokai_firered/checks.json').read_text())
    active=[c for c in data['checks'] if c['status']=='active']
    report={'passed':False,'type':'native_script_and_caught_counter_fixtures','rom_sha256':hashlib.sha256((a.build/'pokefirered_audio.gba').read_bytes()).hexdigest(),
            'physical_paths_tested':False,'wild_captures_played':False,'random_terreur_trigger_tested':False,'checks':[],'validated_ids':[]}
    r=None
    def ok(name,value):
        if not value:raise AssertionError(name)
        report['checks'].append(name);print('PASS',name,flush=True)
    def u16(addr):return int.from_bytes(r.read(addr,2),'little')
    def validate(c):
        r.run(6);idx=active.index(c)
        if not (r.read(r.symbols['gYokaiAPChecks']+idx//8,1)[0]&(1<<(idx%8))):
            report['diagnostic']={'id':c['id'],'flag':r.call('FlagGet',c['flag_value']) if 'flag_value' in c else None,
                'mailbox':r.read(r.symbols['gYokaiAPMailbox'],48).hex(),'callback':q.callback(),
                'terreur':r.call('TerreHeureActive'),'blasters':r.call('BlastersCityActive'),'yopple':r.call('YoppleInDungeon')}
        ok('Native bitmap '+str(c['id']),bool(r.read(r.symbols['gYokaiAPChecks']+idx//8,1)[0]&(1<<(idx%8))))
        report['validated_ids'].append(c['id'])
    try:
        r=new_game();q=QA.__new__(QA);q.r=r;q.reverse={v|1:k for k,v in r.symbols.items()}
        groups=json.loads((a.build/'data/maps/map_groups.json').read_text());q.maps={n:(i,j) for i,k in enumerate(groups['group_order']) for j,n in enumerate(groups[k])}
        q.mon(0,65,100);box=r.symbols['gYokaiAPMailbox']
        ok('Expanded bitmap outside native test trampoline',r.symbols['gYokaiAPChecks']+64<r.STUB)
        r.write(box+8,struct.pack('<H',1));r.write(box+16,hashlib.sha256(b'expanded-native').digest()[:16]);r.write(box+6,struct.pack('<H',1));r.run(6)
        ok('Transport2 keeps native save schema1',u16(box+4)==2 and u16(box+46)==1)
        for c in active:
            if c['kind'] not in ('ball','hidden','gift'):continue
            q.warp(c['map'],1,1)
            before=r.call('BagGetQuantityByItemId',c['native_item_id'])
            if c['kind']=='ball':
                objects=json.loads((a.build/f"data/maps/{c['map']}/map.json").read_text())['object_events']
                local=next(i for i,e in enumerate(objects,1) if e.get('script')==c['script'])
                r.write(r.symbols['gSpecialVar_LastTalked'],struct.pack('<H',local));q.script(c['script'])
            elif c['kind']=='hidden':
                for name,value in [('gSpecialVar_0x8004',c['flag_value']),('gSpecialVar_0x8005',c['native_item_id']),('gSpecialVar_0x8006',1)]:r.write(r.symbols[name],struct.pack('<H',value))
                q.script('EventScript_HiddenItemScript')
            else:q.script(c['script'])
            q.drain();validate(c)
            ok('Original reward suppressed '+str(c['id']),r.call('BagGetQuantityByItemId',c['native_item_id'])==before)
        ok('Fixture party did not fabricate caught entries',r.call('GetKantoPokedexCount',1)==0)
        for n in range(1,152):r.call('GetSetPokedexFlag',n,2) # all seen, zero caught
        caught=0
        possible=data['capture_capacity']['pre_surf_species']
        for c in [x for x in active if x['kind']=='aide']:
            n=c['caught_required']
            while caught<n-1:
                r.call('GetSetPokedexFlag',possible[caught],3);caught+=1
            q.warp(c['map'],1,1);q.script(c['script']);q.drain()
            ok(f'Aide {n} refuses {n-1} caught despite151 seen',r.call('FlagGet',c['flag_value'])==0)
            r.call('GetSetPokedexFlag',possible[caught],3);caught+=1
            before=r.call('BagGetQuantityByItemId',c['native_item_id'])
            q.script(c['script']);q.drain();validate(c)
            ok('Aide native original reward suppressed '+str(n),r.call('BagGetQuantityByItemId',c['native_item_id'])==before)
            q.script(c['script']);q.drain()
            ok('Aide repeat remains single check '+str(n),r.call('BagGetQuantityByItemId',c['native_item_id'])==before)
        q.warp('ViridianForest',1,1)
        r.call('BingoWelcomeGift');r.run(8)
        validate(next(c for c in active if c['id']==0x594B4000))
        r.call('JibanyanGiveFriend');r.run(8)
        validate(next(c for c in active if c['id']==0x594B4001))
        q.warp('PalletTown_PlayersHouse_2F',6,6)
        r.call('SaveMapView');ok('Native save after all checks',r.call('TrySavingData',0)==1);r.run(15)
        r.lib.retro_get_memory_data.argtypes=[C.c_uint];r.lib.retro_get_memory_data.restype=C.c_void_p
        r.lib.retro_get_memory_size.argtypes=[C.c_uint];r.lib.retro_get_memory_size.restype=C.c_size_t
        battery=C.string_at(r.lib.retro_get_memory_data(0),r.lib.retro_get_memory_size(0));r.close();r=Emulator();q.r=r
        r.lib.retro_get_memory_data.argtypes=[C.c_uint];r.lib.retro_get_memory_data.restype=C.c_void_p
        C.memmove(r.lib.retro_get_memory_data(0),battery,len(battery));r.lib.retro_reset();r.run(600)
        q.pulse(3,180)
        replay=r.read(r.symbols['gQuestLogState'],1)[0] in (2,3)
        report['questlog_replay_observed']=replay
        if replay:
            ok('AP distribution paused during actual journal replay',r.read(r.symbols['gYokaiAPMailbox']+38,1)==b'\0')
        q.wait(lambda:q.callback()=='CB2_Overworld' and q.unlocked()
            and r.read(r.symbols['gQuestLogState'],1)[0] not in (2,3),24000);r.run(30)
        for c in active:
            if c['id'] in report['validated_ids']:
                idx=active.index(c)
                ok('Cold Continue check persists '+str(c['id']),bool(r.read(r.symbols['gYokaiAPChecks']+idx//8,1)[0]&(1<<(idx%8))))
        ok('Native captured count survives cold restart',r.call('GetKantoPokedexCount',1)==50)
        report['passed']=True
    except Exception as e:report['error']=str(e);traceback.print_exc()
    finally:
        if r:r.close()
        a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(report,indent=2)+'\n')
    return 0 if report['passed'] else 1

if __name__=='__main__':raise SystemExit(main())
