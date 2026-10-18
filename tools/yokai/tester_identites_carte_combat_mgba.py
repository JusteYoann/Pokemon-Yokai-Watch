#!/usr/bin/env python3
"""Five original staff interactions: shared OW models, distinct native battle art."""
import hashlib,json,re,os
from PIL import Image,ImageDraw
from mgba_rpc import ROOT
from mgba_new_game import new_game
P=ROOT/os.environ.get('YOKAI_IDENTITIES_REPORT_DIR','QA_RECETTE_FINALE/POST_B13/SESSION_2_GRAPHISMES/RED_STRICT_V3/carte-combat');P.mkdir(parents=True,exist_ok=True)
spec=json.loads((ROOT/'data/yokai/cameos_boss.json').read_text());actors={x['name']:x for x in spec['actors']};gfx={x['person']:x for x in spec['graphics']}
groups=json.loads((ROOT/'data/maps/map_groups.json').read_text());maps={n:(i,j) for i,k in enumerate(groups['group_order']) for j,n in enumerate(groups[k])};flags={k:int(v,0) for k,v in re.findall(r'^#define\s+(FLAG_\w+)\s+(0x[0-9A-Fa-f]+|\d+)\b',(ROOT/'include/constants/flags.h').read_text(),re.M)}
r=new_game();rows=[];passed=False;error='Interrupted'
try:
 r.call('CreateMon',r.symbols['gPlayerParty'],87,100,31,1,100,0,0);r.write(r.symbols['gPlayerPartyCount'],b'\x01')
 for f in [0x82C,flags['FLAG_HIDE_SILPH_ROCKETS'],flags['FLAG_SILPH_11F_DOOR'],flags['FLAG_DEFEATED_ROCKETS_IN_WAREHOUSE'],flags['FLAG_HIDE_FIVE_ISLAND_ROCKETS']]:r.call('FlagSet',f)
 base=r.snapshot()
 for name in ['Mafiamille1','Mafiamille2','Mafiamille3','EmployeRouge','EmployeBleu']:
  r.restore(base);a=actors[name];g,n=maps[a['map']];r.call('SetWarpDestination',g,n,255,a['x'],a['y']+1);r.call('WarpIntoMap');r.call('SetMainCallback2',r.symbols['CB2_LoadMap']|1);r.run(600)
  r.frame.save(P/f'{name}-carte.png');r.keys={4};r.run(8);r.keys=set();r.run(16)
  for f in range(8000):
   r.keys={8} if f%16<4 else set();r.run()
   if r.u32(r.symbols['gMain']+4)==r.symbols['BattleMainCB2']|1:break
  else:raise AssertionError((name,'Original NPC interaction did not start battle'))
  r.keys=set();r.run(200);assert r.u32(r.symbols['gMPlayInfo_BGM'])==r.symbols['mus_yokai_20']
  r.frame.save(P/f'{name}-combat.png')
  # Native fixed-size trainer-art table entry must still select the actor's
  # original distinct portrait, never the common overworld bitmap.
  expected=gfx[name]['trainer_pic'];trainer=int.from_bytes(r.read(r.symbols['gTrainerBattleOpponent_A'],2),'little')
  assert r.read(r.symbols['gTrainers']+40*trainer+3,1)[0]==expected,(name,'Wrong trainer table portrait')
  sprite=r.symbols['gSprites']+68*r.read(r.symbols['gBattlerSpriteIds']+1,1)[0]
  assert int.from_bytes(r.read(sprite+6,2),'little')==expected,(name,'Native trainer sprite uses another portrait')
  rows.append(dict(actor=name,original_map=a['map'],actual_map_NPC_interaction=True,trainer_id=trainer,trainer_front_pic_id=expected,normal_map_gfx=gfx[name]['object_gfx'],battle_slot=20,native_battle_entry_captured=True,battle_won_or_replayed=False,passed=True));print('IDENTITY PASS',name,flush=True)
 passed=True;error=None
except BaseException as e:error=str(e);r.frame.save(P/'diagnostic.png');raise
finally:
 r.close();(P/'TEST_MGBA.json').write_text(json.dumps(dict(passed=passed,error=error,rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),scope='Real new-game; postgame/party/warp fixtures; five original NPC interactions and native trainer entries. Battle portraits captured, fights not completed. Source/ROM preservation checked separately.',results=rows),indent=2)+'\n')
if passed:
 sheet=Image.new('RGB',(496,len(rows)*184),(224,224,224));d=ImageDraw.Draw(sheet)
 for i,row in enumerate(rows):
  y=i*184;d.text((4,y+2),row['actor']+' : carte / portrait au combat',fill='black')
  sheet.paste(Image.open(P/f"{row['actor']}-carte.png"),(0,y+22));sheet.paste(Image.open(P/f"{row['actor']}-combat.png"),(256,y+22))
 sheet.save(P/'MEME_CARTE_COMBATS_DISTINCTS.png')
