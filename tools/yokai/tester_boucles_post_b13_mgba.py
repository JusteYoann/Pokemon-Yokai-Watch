#!/usr/bin/env python3
"""Five actual native wraps of each newly approved sample, captured audio privately.

Real intro then isolated music calls; route/event triggers verified separately.
Shares strict reference/audio-seam assertions with established native harness.
"""
import hashlib,json,os
from pathlib import Path
from mgba_rpc import ROOT
from mgba_new_game import new_game
import tester_musiques_integrees_mgba as audio
P=ROOT/'QA_RECETTE_FINALE/POST_B13/audio/boucles-nouvelles';P.mkdir(parents=True,exist_ok=True);(P/'preuves').mkdir(exist_ok=True)
audio.P=P
r=new_game();base=r.snapshot();passed=False;error='Interrupted'
try:
 for n in [27,28,29,30,31]:
  print('START',n,flush=True);r.restore(base);r.call('m4aMPlayAllStop');r.call('m4aSongNumStart',346+n)
  audio.run_song(r,n,'Native m4aSongNumStart after real controller intro; isolated playback fixture, not actual event trigger')
  print('PASS',n,flush=True)
 passed=True;error=None
except BaseException as e:error=str(e);raise
finally:
 r.close();report={'passed':passed,'error':error,'rom_sha256':hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),'scope':'Real new-game initialization, native isolated music calls, five loop boundaries per track measured in actual mixer audio before/after SFX and cry, Flash save; no perceptual listening or full adventure claim','results':audio.results};(P/'TEST_MGBA.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
