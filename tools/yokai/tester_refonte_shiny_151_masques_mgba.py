#!/usr/bin/env python3
"""Eight color-mask renderers: generic UI, battle BG copy and five real turns.
Fixed test parties/moves and Badge8 are fixtures (obedience; enemy uses Splash);
no ROM, HP or battle result edits.
Five historically eligible species play a real damaging move via controller.
The three blocked species receive explicit palette/texture fixtures for BG tests.
"""
import hashlib,json,os,struct,subprocess
from PIL import Image
from mgba_rpc import ROOT
from mgba_new_game import new_game
from masques_shiny_151 import MASKED
from mafiamille_qa import C
from pilote_combat_mgba import battle_keys
mode='prive' if '_audio' in os.environ.get('YOKAI_QA_ROM','') else 'public';Q=ROOT/'docs/shiny-151-20261024/revision-2/mgba'/mode/'masques';Q.mkdir(parents=True,exist_ok=True)
r=new_game();r.call('FlagSet',0x827);base=r.snapshot();results=[];passed=False;error=None
rows={m['number']:m for m in json.loads((ROOT/'data/yokai/shiny-151-20261024/palettes.json').read_text())['species']}
callbacks={int(f[0],16)|1 for line in subprocess.check_output(['arm-none-eabi-nm','--defined-only',str(r.elf_path)],text=True).splitlines() if len(f:=line.split())==3 and f[2]=='HandleInputChooseAction'}
def check_battlers(n):
 for b,side in [(0,'back'),(1,'front')]:
  ptr=r.u32(r.u32(r.symbols['gMonSpritesGfxPtr'])+4+4*b);expected=(ROOT/f'graphics/yokai_shiny_revised/{n:03}/{side}-battle.4bpp').read_bytes();assert r.read(ptr,2048)==expected,(n,b,'shiny texture lost')
  sid=r.read(r.symbols['gBattlerSpriteIds']+b,1)[0];sp=r.symbols['gSprites']+68*sid;attr=int.from_bytes(r.read(sp+4,2),'little');bank=attr>>12
  assert r.read(0x06010000+32*(attr&1023),2048)==expected,(n,b,'native VRAM texture lost')
  assert r.read(r.symbols['gPlttBufferUnfaded']+512+32*bank,32)==(ROOT/f'graphics/yokai/{n:03}/shiny.gbapal').read_bytes(),(n,b,'shiny palette lost')
try:
 for n in sorted(MASKED):
  r.restore(base);buf=r.call('AllocZeroed',4096);assert buf
  for side,label in [(0,'back'),(1,'front')]:
   table=r.symbols['gMonFrontPicTable' if side else 'gMonBackPicTable']+8*n
   r.call('LoadSpecialPokePic_DontHandleDeoxys',table,buf,n,0,side)
   original=r.read(buf,2048);normal=r.u32(r.symbols['gMonPaletteTable']+8*n);shiny=r.u32(r.symbols['gMonShinyPaletteTable']+8*n)
   assert r.call('TryLoadYokaiShinyPicWithPalette',buf,n,normal,side)==0 and r.read(buf,2048)==original
   assert r.call('TryLoadYokaiShinyPicWithPalette',buf,n,shiny,side)==1
   assert r.read(buf,2048)==(ROOT/f'graphics/yokai_shiny_revised/{n:03}/{label}-display.4bpp').read_bytes(),(n,label,'generic display')
  results.append(dict(species=n,generic_front_back=True,normal_loader_unchanged=True))
  r.restore(base)
  for p in ['gPlayerParty','gEnemyParty']:r.call('CreateMon',r.symbols[p],n,70,31,1,0,1,0)
  for p in ['gPlayerPartyCount','gEnemyPartyCount']:r.write(r.symbols[p],b'\1')
  r.call('SetMonMoveSlot',r.symbols['gPlayerParty'],C['MOVE_AERIAL_ACE'],0)
  for slot in range(4):r.call('SetMonMoveSlot',r.symbols['gEnemyParty'],C['MOVE_SPLASH'],slot)
  r.call('StartScriptedWildBattle')
  for frame in range(6000):
   r.keys={0} if frame%16<2 else set();r.run()
   if r.u32(r.symbols['gMain']+4)==r.symbols['BattleMainCB2']|1 and r.u32(r.symbols['gBattlerControllerFuncs']) in callbacks:break
  else:raise AssertionError((n,'no action menu'))
  r.keys=set();r.run(12)
  moves=[struct.unpack('<4H',r.read(r.symbols['gBattleMons']+88*b+12,8)) for b in [0,1]]
  assert moves[0][0]==C['MOVE_AERIAL_ACE'] and moves[1]==(C['MOVE_SPLASH'],)*4,(n,'moves reset',moves)
  if not rows[n]['natural_shiny_enabled']:
   for b,side in [(0,'back'),(1,'front')]:
    ptr=r.u32(r.u32(r.symbols['gMonSpritesGfxPtr'])+4+4*b);pal=r.u32(r.symbols['gMonShinyPaletteTable']+8*n)
    assert r.call('TryLoadYokaiShinyPicWithPalette',ptr,n,pal,b)==1
    sp=r.symbols['gSprites']+68*r.read(r.symbols['gBattlerSpriteIds']+b,1)[0];attr=int.from_bytes(r.read(sp+4,2),'little');r.call('LoadCompressedPalette',pal,256+16*(attr>>12),32);r.call('CpuSet',ptr,0x06010000+32*(attr&1023),1024)
  check_battlers(n);state=r.snapshot()
  for b in [0,1]:
   r.restore(state);g=struct.unpack('<hhbbbbBB',r.read(r.call('GetYokaiBattleGeometry',b),10));tiles=r.call('AllocZeroed',4096);tilemap=r.call('AllocZeroed',2048);assert tiles and tilemap
   assert r.call('CopyYokaiBattlerToBg',1,b,2,tiles,tilemap,0)==1
   cols=(g[6]+7)//8;src=r.read(r.u32(r.u32(r.symbols['gMonSpritesGfxPtr'])+4+4*b),2048);expected=bytearray(4096)
   for y in range(g[7]):
    sy=((y+g[5])*g[1]>>8)+32
    for x in range(g[6]):
     sx=((x+g[4])*g[0]>>8)+32
     if 0<=sx<64 and 0<=sy<64:
      v=(src[(sy//8*8+sx//8)*32+(sy%8)*4+(sx%8)//2]>>((sx&1)*4))&15;idx=(y//8*cols+x//8)*32+(y%8)*4+(x%8)//2;expected[idx]|=v<<((x&1)*4)
   assert r.read(tiles,4096)==expected,(n,b,'animation BG mask')
  r.restore(state);results[-1]['battle_animation_BG_both_sides']=True
  if rows[n]['natural_shiny_enabled']:
   before=int.from_bytes(r.read(r.symbols['gBattleMons']+88+0x28,2),'little');frames=[]
   for frame in range(2400):
    r.keys=battle_keys(r,frame);r.run()
    if frame%12==0:frames.append(r.frame.copy().resize((480,320),Image.Resampling.NEAREST))
    hp=int.from_bytes(r.read(r.symbols['gBattleMons']+88+0x28,2),'little')
    if frame>60 and 0<hp<before and r.u32(r.symbols['gBattlerControllerFuncs']) in callbacks:break
   else:raise AssertionError((n,'real damaging turn did not finish'))
   r.keys=set();r.run(12);check_battlers(n);frames[0].save(Q/f'{n:03}-attaque.gif',save_all=True,append_images=frames[1:],duration=160,loop=0);r.frame.save(Q/f'{n:03}-apres-attaque.png');results[-1].update(real_turn=True,enemy_hp_before=before,enemy_hp_after=hp,shiny_retained=True,native_VRAM_retained=True)
  print('MASK QA',mode,n,flush=True)
 passed=True
 if (Q/'diagnostic.png').exists():(Q/'diagnostic.png').unlink()
except BaseException as e:
 error=str(e);r.frame.save(Q/'diagnostic.png');raise
finally:
 sha=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest();r.close();(Q/'TEST_MGBA.json').write_text(json.dumps(dict(passed=passed,scope=__doc__,rom_sha256=sha,error=error,results=results),ensure_ascii=False,indent=2)+'\n')
