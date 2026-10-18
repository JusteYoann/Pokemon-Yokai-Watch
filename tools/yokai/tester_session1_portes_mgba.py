#!/usr/bin/env python3
"""Real controller door crossings for ordinary city/route facilities, explicit warps."""
import hashlib,json,os
from mgba_rpc import ROOT
from mgba_new_game import new_game
P=ROOT/os.environ.get('YOKAI_AUDIO_QA_REPORT_ROOT','QA_RECETTE_FINALE/SESSION_1_AUDIO')/'portes';P.mkdir(parents=True,exist_ok=True)
G=json.loads((ROOT/'data/maps/map_groups.json').read_text())
MAPS={n:(i,j) for i,k in enumerate(G['group_order']) for j,n in enumerate(G[k])}
maps={p.parent.name:json.loads(p.read_text()) for p in (ROOT/'data/maps').glob('*/map.json')}
names={d['id']:name for name,d in maps.items()}
selected_towns=set(filter(None,os.environ.get('YOKAI_AUDIO_DOOR_TOWNS','').split(',')))
r=new_game();checks=[];passed=False;error='Interrupted'
def location():return tuple(r.read(r.u32(r.symbols['gSaveBlock1Ptr'])+4,2))
def warp(name,x,y):
    r.keys=set();g,n=MAPS[name];r.call('SetWarpDestination',g,n,255,x,y)
    r.call('WarpIntoMap');r.call('SetMainCallback2',r.symbols['CB2_LoadMap']|1);r.run(600)
    assert location()==(g,n)
def cross(destination,key,label):
    expected=MAPS[destination];h=r.u32(r.symbols['gMPlayInfo_BGM']);last=r.u32(r.symbols['gMPlayInfo_BGM']+12);before=last
    for frame in range(750):
        r.keys={key} if frame<40 else set();r.run()
        assert r.u32(r.symbols['gMPlayInfo_BGM'])==h,(label,'Changed music')
        clock=r.u32(r.symbols['gMPlayInfo_BGM']+12);assert clock>=last,(label,'Restarted music')
        assert not r.u32(r.symbols['gMPlayInfo_BGM']+4)&0x80000000,(label,'Paused music')
        assert r.u32(r.symbols['gSoundInfo'])==0x68736D53,(label,'Stopped mixer')
        last=clock
        if frame>100 and location()==expected and r.u32(r.symbols['gMain']+4)==r.symbols['CB2_Overworld']|1:break
    else:raise AssertionError((label,'Door not crossed',location(),expected))
    r.keys=set();r.run(60);assert last>before
    r.frame.save(P/(label+'.png'))
    return dict(test=label,destination=destination,controller_frames=frame+1,same_header=True,
                clock_before=before,clock_after=last,no_restart=True,no_pause=True,passed=True)
try:
    r.call('CreateMon',r.symbols['gPlayerParty'],1,20,31,1,100,0,0);r.write(r.symbols['gPlayerPartyCount'],b'\x01')
    for flag in [0x828,0x829]:r.call('FlagSet',flag)
    r.call('VarSet',0x4050,3);r.call('VarSet',0x4055,9)
    # Postgame door fixture: the first-visit Matt scene otherwise locks movement.
    r.call('VarSet',0x4086,1);r.call('FlagSet',0x097)
    r.call('VarSet',0x4076,7);r.call('VarSet',0x4075,3)
    r.call('VarSet',0x4089,1)
    r.call('VarSet',0x4057,2)  # Parcel already delivered; no introductory clerk lock.
    base=r.snapshot()
    for town,d in sorted(maps.items()):
        if selected_towns and town not in selected_towns:continue
        if d['map_type'] not in ['MAP_TYPE_TOWN','MAP_TYPE_CITY','MAP_TYPE_ROUTE']:continue
        for w in d.get('warp_events',[]):
            dest=names.get(w['dest_map'],'')
            if not (dest.endswith('_PokemonCenter_1F') or dest.endswith('_Mart') or dest=='PalletTown_ProfessorOaksLab'):continue
            assert d['music']==maps[dest]['music'],(town,dest,'Source themes disagree')
            label=town+'--'+dest
            r.restore(base);warp(town,w['x'],w['y']+1)
            checks.append(cross(dest,4,label+'-entree'))
            checks.append(cross(town,5,label+'-sortie'))
            print('DOORS',town,dest,flush=True)
    assert len(checks)>=(2 if selected_towns else 40), 'Too few door tests executed'
    passed=True;error=None
except BaseException as e:
    error=str(e);r.frame.save(P/'diagnostic.png');raise
finally:
    r.keys=set();r.close();(P/'TEST_MGBA.json').write_text(json.dumps(dict(passed=passed,error=error,
        rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),results=checks,
        scope='Actual controller doors after real new-game initialization and explicit position/progression fixtures. Header, monotonic sequencer clock, no pause. Not all homes/routes or a whole-adventure playthrough.'),ensure_ascii=False,indent=2)+'\n')
    print('DOORS RESULT',len(checks),passed,error,flush=True)
