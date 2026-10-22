#!/usr/bin/env python3
"""Source PNG -> linked frame bytes -> native object VRAM, and portrait registry."""
import hashlib,json,re,struct,subprocess
from PIL import Image
from mgba_rpc import ROOT
from mgba_new_game import new_game
from tester_argenta_scenario_mgba import warp
out=ROOT/'QA_RECETTE_FINALE/CARMIN_SCENARIO_2026';out.mkdir(exist_ok=True)
actors=[('berenice','Berenice',173),('giraud','Giraud',174),('alyzon','Alyzon',175),('enma_humain','EnmaHumain',176),('laure','Laure',177),('marge','Marge',178),('lady_perpetua','LadyPerpetua',179),('mckraken','Mckraken',180),('agent_x','AgentX',181),('zazel','Zazel',182),('enma_ancien','EnmaAncien',183),('nathaniel_age','NathanielAge',184),('zombie','Zombie',185),('soranaki_phase1','SoranakiPhase1',186),('soranaki_phase2','SoranakiPhase2',187),('bingo_kai','BingoKai',188),('capsule_souhait','CapsuleSouhait',189),('triptic_tac','TripticTac',190)]
def encode(im,x,w,h):
 b=bytearray()
 for ty in range(h//8):
  for tx in range(w//8):
   for y in range(8):
    for px in range(0,8,2):
     lo=im.getpixel((x+tx*8+px,ty*8+y));hi=im.getpixel((x+tx*8+px+1,ty*8+y));assert max(lo,hi)<16
     b.append(lo|hi<<4)
 return bytes(b)
r=new_game();rows=[];atlas=Image.new('RGB',(240*4,160*5))
try:
 for i,(name,symbol,gfx) in enumerate(actors):
  im=Image.open(ROOT/f'graphics/yokai_characters/{name}/overworld.png');w=32 if name in ['bingo_kai','triptic_tac'] else 16;h=16 if name=='capsule_souhait' else 32
  frames=[encode(im,x,w,h) for x in range(0,im.width,w)]
  assert all(any(f) for f in frames),(name,'blank source frame')
  linked=r.read(r.symbols['gObjectEventPic_Scenario'+symbol],len(frames)*len(frames[0]))
  assert linked==b''.join(frames),(name,'wrong linked frame tiling')
  warp(r,9,9,7,12)
  obj=r.call('SpawnSpecialObjectEventParameterized',gfx,8,200,14,17,3);assert obj<16
  r.run(120);spriteId=r.read(r.symbols['gObjectEvents']+36*obj+4,1)[0];sp=r.symbols['gSprites']+68*spriteId
  tile=int.from_bytes(r.read(sp+4,2),'little')&1023;vram=r.read(0x06010000+tile*32,len(frames[0]))
  assert vram in frames and any(vram),(name,'native VRAM frame not one of the source frames')
  assert r.read(r.symbols['gPlttBufferUnfaded']+512+10*32,32)==r.read(r.symbols['gObjectEventPal_Scenario'],32),(name,'palette')
  r.frame.save(out/'sprite-temp.png');atlas.paste(r.frame,(i%4*240,i//4*160))
  rows.append({'actor':name,'frames':len(frames),'frame_size':[w,h],'linked_source_bytes_match':True,'native_vram_frame_matches':True,'palette_matches':True})
 # Verify every newly registered front portrait has a real in-bounds animation table.
 syms=subprocess.check_output(['arm-none-eabi-nm','-S','--defined-only',str(ROOT/'pokefirered.elf')],text=True)
 size=int(next(l.split()[1] for l in syms.splitlines() if l.endswith(' gTrainerFrontAnimsPtrTable')),16)
 ids=[(n,int(v)) for n,v in re.findall(r'^#define (TRAINER_PIC_SCENARIO_\w+) (\d+)',(ROOT/'include/constants/trainers.h').read_text(),re.M)]
 for name,pic in ids:
  assert (pic+1)*4<=size,(name,'animation pointer index out of bounds')
  ptr=r.u32(r.symbols['gTrainerFrontAnimsPtrTable']+4*pic);assert 0x08000000<=ptr<0x09000000
  anim=r.u32(ptr);assert 0x08000000<=anim<0x09000000
  assert int.from_bytes(r.read(anim,2),'little')==0,(name,'single-frame portrait expected')
finally:r.close()
(out/'sprite-temp.png').unlink(missing_ok=True);atlas.save(out/'SPRITES_SCENARIO_NATIFS.png')
(out/'TEST_SPRITES_LIES_MGBA.json').write_text(json.dumps({'passed':True,'rom_sha256':hashlib.sha256((ROOT/'pokefirered.gba').read_bytes()).hexdigest(),'scope':'18 native spawned object graphics checked against independent source PNG encoding and actual VRAM;15 front portrait animation registry contracts. Actual Berenice intro/battle covered separately; does not play every future boss battle.','results':rows,'portrait_animation_entries_checked':len(ids)},ensure_ascii=False,indent=2)+'\n');print('PASS',len(rows),'native object renderings;',len(ids),'portrait animation entries')
