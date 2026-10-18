#!/usr/bin/env python3
"""Actual native header resolution for every alias, every SFX and every fanfare."""
import hashlib,json,re
from mgba_rpc import ROOT
from mgba_new_game import new_game
P=ROOT/'QA_RECETTE_FINALE/SESSION_1_AUDIO';P.mkdir(exist_ok=True)
C={k:int(v) for k,v in re.findall(r'^#define\s+((?:MUS|SE|TRAINER)_\w+)\s+(\d+)\b',
   '\n'.join((ROOT/f'include/constants/{n}.h').read_text() for n in ['songs','opponents']),re.M)}
for key,target in re.findall(r'^#define\s+(TRAINER_\w+)\s+(TRAINER_\w+)\b',(ROOT/'include/constants/opponents.h').read_text(),re.M):
    C[key]=C[target]
entries=re.findall(r'^\s*song\s+(\w+),\s*(\d+),\s*(\d+)',(ROOT/'sound/song_table.inc').read_text(),re.M)
active=set(json.loads((ROOT/'data/yokai/audio_loops.json').read_text())['active_tracks'])
r=new_game();rows=[];passed=False;error='Interrupted'
def header(n):return r.u32(r.symbols['gSongTable']+8*n)
try:
    for a in json.loads((ROOT/'data/yokai/audio_session1_aliases.json').read_text())['aliases']:
        n=C[a['source']];target=C[a['target']];slot=target-346
        expected=r.symbols[f'mus_yokai_{slot:02d}'] if slot in active else header(target)
        actual=r.call('YokaiGetSongHeader',n,header(n));assert actual==expected,(a,actual,expected)
        r.call('m4aSongNumStart',n);r.run(6)
        assert r.u32(r.symbols['gMPlayInfo_BGM'])==expected,(a,'Not actually started')
        before=r.u32(r.symbols['gMPlayInfo_BGM']+12)
        r.call('m4aSongNumStartOrChange',target);r.run(6)
        assert r.u32(r.symbols['gMPlayInfo_BGM'])==expected
        assert r.u32(r.symbols['gMPlayInfo_BGM']+12)>before,(a,'Alias/explicit track restarted')
        rows.append(dict(source=a['source'],target=a['target'],private_sample_active=slot in active,
                         native_playback_header_correct=True,alias_to_explicit_without_restart=True))
    unchanged=[]
    for n in range(1,len(entries)):
        if n>255 and entries[n][1]=='0':continue
        assert r.call('YokaiGetSongHeader',n,header(n))==header(n),(n,'SFX/fanfare replaced')
        unchanged.append(n)
    battles=[]
    for name,theme in [('TRAINER_YOKAI_DOMNISCIAN','MUS_YOKAI_HINOZALL'),
                       ('TRAINER_YOKAI_DONMORLEONE','MUS_YOKAI_GHOULFATHER'),
                       ('TRAINER_YOKAI_ENMA','MUS_YOKAI_ZAZELMARE'),
                       ('TRAINER_ELITE_FOUR_LORELEI','MUS_YOKAI_DECISIVE_BATTLE'),
                       ('TRAINER_LEADER_BROCK','MUS_YOKAI_BOSS_YOKAI')]:
        r.w32(r.symbols['gBattleTypeFlags'],8)
        r.write(r.symbols['gTrainerBattleOpponent_A'],C[name].to_bytes(2,'little'))
        assert r.call('GetBattleBGM')==C[theme],name
        battles.append(dict(trainer=name,music=theme,passed=True))
    passed=True;error=None
except BaseException as e:error=str(e);raise
finally:
    r.close();(P/'ROUTAGE_MGBA.json').write_text(json.dumps(dict(passed=passed,error=error,
        rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),aliases=rows,
        unchanged_native_sfx_and_fanfare_ids=locals().get('unchanged',[]),special_bosses=locals().get('battles',[]),
        scope='Real new-game initialization, native resolver and short playback fixtures. Not every scripted event or whole-track listening.'),ensure_ascii=False,indent=2)+'\n')
    print('ROUTAGE',len(rows),passed,error,flush=True)
