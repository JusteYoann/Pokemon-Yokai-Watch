#!/usr/bin/env python3
"""Native fanfare pause/resume preserves the sampled music cursor, not a restart."""
import hashlib,json,re,os
from mgba_rpc import ROOT
from mgba_new_game import new_game
C={k:int(v) for k,v in re.findall(r'^#define\s+(MUS_\w+)\s+(\d+)\b',(ROOT/'include/constants/songs.h').read_text(),re.M)}
fanfares=re.findall(r'\[FANFARE_\w+\]\s*=\s*\{\s*(MUS_\w+),\s*(\d+)',(ROOT/'src/sound.c').read_text())
active=json.loads((ROOT/'data/yokai/audio_loops.json').read_text())['active_tracks']
r=new_game();base=r.snapshot();rows=[];passed=False;error='Interrupted'
def channel(n):
    for i in range(5):
        p=r.symbols['gSoundInfo']+80+64*i
        if r.u32(p+36)==r.symbols[f'yokai_wave_{n:02d}'] and r.read(p,1)[0]&0x83:return p
    return None
try:
    cases=[(27,mus) for mus,_ in fanfares]+[(n,'MUS_OBTAIN_ITEM') for n in active]
    assert len(fanfares)==14 and len(cases)==14+len(active)
    for n,mus in cases:
        r.restore(base);r.call('m4aMPlayAllStop');r.call('m4aSongNumStart',346+n);r.run(750)
        before=r.u32(channel(n)+40);r.call('PlayFanfare',C[mus])
        assert r.u32(r.symbols['gMPlayInfo_BGM']+4)&0x80000000,(n,mus,'Did not pause')
        for frame in range(1400):
            r.run()
            if frame%8==0 and r.call('IsFanfareTaskInactive') and channel(n) and not r.u32(r.symbols['gMPlayInfo_BGM']+4)&0x80000000:break
        else:raise AssertionError((n,mus,'No resume'))
        after=r.u32(channel(n)+40)
        assert before<=after<before+224*25,(n,mus,'Sample reset/jumped',before,after)
        assert r.u32(r.symbols['gMPlayInfo_BGM'])==r.symbols[f'mus_yokai_{n:02d}']
        r.run(30);assert r.u32(channel(n)+40)>after,(n,mus,'Cursor not advancing')
        rows.append(dict(number=n,fanfare=mus,native_pause=True,native_resume=True,
                         sample_before=before,sample_after=after,no_reset=True,passed=True))
    passed=True;error=None
except BaseException as e:error=str(e);raise
finally:
    output=ROOT/os.environ.get('YOKAI_AUDIO_QA_REPORT_ROOT','QA_RECETTE_FINALE/SESSION_1_AUDIO');output.mkdir(parents=True,exist_ok=True)
    r.close();(output/'FANFARES_MGBA.json').write_text(json.dumps(dict(passed=passed,error=error,
        rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),results=rows,
        scope=f'{len(rows)} isolated native fanfare calls after real new-game init; actual sequencer pause, sampled-channel restoration and advancing cursor. Not every in-world item/evolution event.'),indent=2)+'\n')
    print('FANFARES',len(rows),passed,error,flush=True)
