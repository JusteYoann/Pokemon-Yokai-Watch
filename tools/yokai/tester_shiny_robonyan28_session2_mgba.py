#!/usr/bin/env python3
"""Five formerly dedicated species: normal/shiny renderer regression in PC, summary and generic front/back.

Explicit party/box/UI fixtures after real new-game init; not trading gameplay.
"""
import hashlib,json,os
from PIL import Image,ImageDraw
from mgba_rpc import ROOT
from mgba_new_game import new_game
P=ROOT/os.environ.get('YOKAI_SHINY_REPORT_DIR','QA_RECETTE_FINALE/POST_B13/SESSION_2_GRAPHISMES/shiny-interfaces');P.mkdir(parents=True,exist_ok=True)
r=new_game();base=r.snapshot();rows=[];frames=[];passed=False;error='Interrupted'
try:
 for species,shiny in [(n,b) for n in [19,99,100,101,126] for b in [False,True]]:
  r.restore(base);pid=0 if shiny else 100
  r.call('CreateMon',r.symbols['gPlayerParty'],species,30,31,1,pid,1,0);r.write(r.symbols['gPlayerPartyCount'],b'\x01')
  assert bool(r.call('IsMonShiny',r.symbols['gPlayerParty']))==shiny
  state=r.snapshot()
  r.call('SetCurrentBox',0);ptr=r.call('GetBoxedMonPtr',0,0);r.call('CreateBoxMon',ptr,species,30,31,1,pid,1,0)
  r.call('EnterPokeStorage',2);r.run(1500);assert r.u32(r.symbols['gMain']+4)==r.symbols['CB2_PokeStorage']|1
  label=f'{species:03}-'+('shiny' if shiny else 'normal');r.frame.save(P/f'pc-{label}.png');frames.append((f'PC {label}',r.frame.copy()))
  r.restore(state);r.call('ShowPokemonSummaryScreen',r.symbols['gPlayerParty'],0,0,r.symbols['CB2_ReturnToField']|1,0);r.run(1200)
  r.frame.save(P/f'resume-{label}.png');frames.append((f'Resume {label}',r.frame.copy()))
  # Decompress generic picture sprites used by summary/evolution/etc. Their
  # image pointers expose exactly the native rendered indexed 2048-byte data.
  for front in [True,False]:
   r.restore(state)
   sprite=r.call('CreateMonPicSprite_HandleDeoxys',species,0,pid,int(front),120,80,12,65535)
   assert sprite<64
   images=r.u32(r.symbols['gSprites']+68*sprite+12);tiles=r.u32(images)
   policy=ROOT/'data/yokai/shiny_artwork_policy.json';dedicated=not policy.exists() or json.loads(policy.read_text())['dedicated_bitmaps_enabled']
   directory=f'graphics/yokai_shiny/{species:03}' if shiny and dedicated else f'graphics/yokai/{species:03}';stem='front' if front else 'back'
   file=ROOT/f'{directory}/{stem}-display.4bpp'
   if not file.exists():file=ROOT/f'{directory}/{stem}.4bpp'
   assert r.read(tiles,2048)==file.read_bytes(),(label,stem,'Generic native tiles differ')
   rows.append(dict(test='Generic mon picture exact indexed native tiles',species=species,shiny=shiny,front=front,passed=True))
  rows.append(dict(test='Actual PC and summary screens rendered; visual comparison screenshots',species=species,shiny=shiny,passed=True))
 passed=True;error=None
except BaseException as e:error=str(e);r.frame.save(P/'diagnostic.png');raise
finally:
 r.close();(P/'TEST_MGBA.json').write_text(json.dumps(dict(passed=passed,error=error,rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),scope=__doc__,results=rows),ensure_ascii=False,indent=2)+'\n')
if passed:
 sheet=Image.new('RGB',(960,900),(224,224,224));d=ImageDraw.Draw(sheet)
 for i,(label,img) in enumerate(frames):d.text((240*(i%4)+4,180*(i//4)+2),label,fill='black');sheet.paste(img,(240*(i%4),180*(i//4)+20))
 sheet.save(P/'pc-et-resume.png')
