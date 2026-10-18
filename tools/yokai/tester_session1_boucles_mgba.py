#!/usr/bin/env python3
"""Five actual native wraps per active sample; private audio evidence only."""
import argparse,hashlib,json
from mgba_rpc import ROOT
from mgba_new_game import new_game
import tester_musiques_integrees_mgba as audio
parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--numbers');parser.add_argument('--output-subdir',default='boucles');a=parser.parse_args()
numbers=list(map(int,a.numbers.split(','))) if a.numbers else json.loads((ROOT/'data/yokai/audio_loops.json').read_text())['active_tracks']
P=ROOT/'QA_RECETTE_FINALE/SESSION_1_AUDIO'/a.output_subdir;P.mkdir(parents=True,exist_ok=True);(P/'preuves').mkdir(exist_ok=True);audio.P=P
r=new_game();base=r.snapshot();passed=False;error='Interrupted'
try:
    for n in numbers:
        r.restore(base);r.call('m4aMPlayAllStop');r.call('m4aSongNumStart',346+n)
        audio.run_song(r,n,'Isolated native playback after real controller new-game; five loops with SFX, cry and Flash save; event routes tested separately')
        print('LOOPS PASS',n,flush=True)
    passed=True;error=None
except BaseException as e:error=str(e);raise
finally:
    r.close();(P/'TEST_MGBA.json').write_text(json.dumps(dict(passed=passed,error=error,
        rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),results=audio.results,
        scope='Native mixer and waveform-reference checks; not subjective listening, hardware or full-adventure playthrough.'),ensure_ascii=False,indent=2)+'\n')
