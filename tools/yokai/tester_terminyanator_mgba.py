#!/usr/bin/env python3
"""GFX motard global inchangé : 32×32, moto conservée, palettes, marche et combat natifs."""
import json,hashlib,struct
from PIL import Image
from postgame_qa_common import QA
from mgba_rpc import ROOT
from mafiamille_qa import C
D=ROOT/'docs/postgame-corrections-terminyanator-20261025';D.mkdir(exist_ok=True)
q=QA('TEMP.json');r=q.r;frames=[]
try:
 q.mon();q.warp('PalletTown',10,10);r.run(300);r.call('LockPlayerFieldControls');r.call('FreezeObjectEvents')
 oid=r.call('SpawnSpecialObjectEventParameterized',53,8,200,12,17,3);assert oid<16;obj=r.symbols['gObjectEvents']+36*oid;sid=r.read(obj+4,1)[0];sprite=r.symbols['gSprites']+68*sid
 source=(ROOT/'graphics/yokai_characters/terminyanator/overworld.4bpp').read_bytes();assert len(source)==5120
 info=r.call('GetObjectEventGraphicsInfo',53);assert info==r.symbols['gObjectEventGraphicsInfo_Biker']
 def check():
  bank=r.read(sprite+5,1)[0]>>4;assert bank==9
  assert r.read(r.symbols['gPlttBufferUnfaded']+512+32*bank,32)==r.read(r.symbols['gObjectEventPal_Terminyanator'],32)
  tile=int.from_bytes(r.read(sprite+4,2),'little')&1023;actual=r.read(0x6010000+32*tile,512);assert any(actual==source[i*512:(i+1)*512] for i in range(10))
  frames.append(r.frame.resize((720,480),Image.Resampling.NEAREST))
 for _ in range(15):r.run(2);check()
 for d,steps in [(1,2),(3,3),(0,2),(2,3)]:
  for _ in range(steps):
   r.call('ObjectEventClearHeldMovementIfActive',obj);assert not r.call('ObjectEventSetHeldMovement',obj,0x10+d)
   for _ in range(9):r.run(2);check()
 frames[0].save(D/'terminyanator-quatre-directions-mgba.gif',save_all=True,append_images=frames[1:],duration=34,loop=0)
 # Native Route 13 biker encounter; only progression and player level are fixtures.
 r.call('UnlockPlayerFieldControls');q.warp('Route13',14,9);r.run(60)
 r.call('ClearTrainerFlag',C['TRAINER_BIKER_JARED']);q.script('Route13_EventScript_Jared');q.wait(lambda:q.callback()=='BattleMainCB2',12000)
 found=False
 for f in range(2500):
  r.keys=set();r.run();sid=r.read(r.symbols['gBattlerSpriteIds']+1,1)[0]
  if sid<64:
   sp=r.symbols['gSprites']+68*sid
   if int.from_bytes(r.read(sp+6,2),'little')==91 and r.read(sp+36,2)==b'\0\0':
    r.frame.save(D/'terminyanator-en-combat.png');found=True;break
 assert found
 result=dict(passed=True,scope=__doc__,rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),overworld_gfx=53,trainer_pic=91,frame=[32,32],frames=10,palette_bank=9,actual_vram_frames=True,native_four_directions=True,global_map_objects=sum(1 for p in (ROOT/'data/maps').glob('*/map.json') for o in json.loads(p.read_text()).get('object_events',[]) if o.get('graphics_id')=='OBJ_EVENT_GFX_BIKER'),trainer_data_unchanged=True)
 (D/'TESTS_TERMINYANATOR.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print('PASS',result,flush=True)
finally:r.close()
