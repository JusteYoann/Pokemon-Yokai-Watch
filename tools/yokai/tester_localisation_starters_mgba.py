#!/usr/bin/env python3
"""Original starter-ball event scripts: French prompts and actual chosen species."""
import hashlib,json
from PIL import Image,ImageDraw
from mgba_rpc import ROOT
from mgba_new_game import new_game
P=ROOT/'QA_RECETTE_FINALE/LOCALISATION_FR/starters';P.mkdir(parents=True,exist_ok=True)
r=new_game();rows=[];passed=False;error='Interrupted'
try:
 groups=json.loads((ROOT/'data/maps/map_groups.json').read_text());g,n=next((i,j) for i,k in enumerate(groups['group_order']) for j,v in enumerate(groups[k]) if v=='PalletTown_ProfessorOaksLab')
 r.call('VarSet',0x4055,2);r.call('SetWarpDestination',g,n,255,5,5);r.call('WarpIntoMap');r.call('SetMainCallback2',r.symbols['CB2_LoadMap']|1);r.run(600);base=r.snapshot()
 for event,expected,name in [('Bulbasaur',5,'Komasan'),('Squirtle',29,'Padrezo'),('Charmander',87,'Kappacap')]:
  r.restore(base);r.call('ScriptContext_SetupScript',r.symbols['PalletTown_ProfessorOaksLab_EventScript_'+event+'Ball']);r.run(300)
  assert r.call('VarGet',0x4002)==expected,(name,'Wrong starter species in original script')
  r.frame.save(P/(name+'-1.png'));r.keys={8};r.run(4);r.keys=set();r.run(600);r.frame.save(P/(name+'-2.png'))
  rows.append(dict(name=name,species_id=expected,original_ball_event=True,choice_confirmed=False,captured=True))
 passed=True;error=None
except BaseException as e:error=str(e);r.frame.save(P/'diagnostic.png');raise
finally:
 r.close();(P/'TEST_MGBA.json').write_text(json.dumps(dict(passed=passed,error=error,rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),scope='New-game then laboratory/scene fixtures; original three ball scripts to preview and confirmation text; no party acceptance or rival battle claimed.',results=rows),ensure_ascii=False,indent=2)+'\n')
if passed:
 sheet=Image.new('RGB',(720,344),(224,224,224));d=ImageDraw.Draw(sheet)
 for i,row in enumerate(rows):
  d.text((i*240+2,2),row['name'],fill='black')
  for j in range(2):sheet.paste(Image.open(P/(row['name']+'-'+str(j+1)+'.png')),(i*240,j*162+20))
 sheet.save(P/'PLANCHE.png');print('STARTERS FR PASS',len(rows))
