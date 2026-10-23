#!/usr/bin/env python3
"""151 native battles with front/back tiles and compiled palette-bank checks.
PID0 requests shiny naturally (84 allowed/67 blocked). After checking automatic selection, normal/shiny images are compared using
explicit native color-loading fixtures (required for the67 blocked species). No ROM,
PID rules, encounter probabilities or eligibility tables are modified.
This is not a full adventure or an all-attacks test.
"""
import hashlib,json,os,subprocess
from PIL import Image
from mgba_rpc import ROOT
from mgba_new_game import new_game
Q=ROOT/'docs/shiny-151-20261024/revision-2';mode='prive' if '_audio' in os.environ.get('YOKAI_QA_ROM','') else 'public';out=Q/'mgba'/mode;out.mkdir(parents=True,exist_ok=True)
rows=json.loads((ROOT/'data/yokai/shiny-151-20261024/palettes.json').read_text())['species']
if chosen:=os.environ.get('YOKAI_QA_SPECIES'):
 selected=set(map(int,chosen.split(',')));rows=[row for row in rows if row['number'] in selected];out=out/'retouche-appak';out.mkdir(exist_ok=True)
r=new_game();base=r.snapshot();results=[];passed=False;error=None
callbacks={int(f[0],16)|1 for line in subprocess.check_output(['arm-none-eabi-nm','--defined-only',str(r.elf_path)],text=True).splitlines() if len(f:=line.split())==3 and f[2]=='HandleInputChooseAction'}
try:
 for row in rows:
  n=row['number'];r.restore(base)
  for party in ['gPlayerParty','gEnemyParty']:
   r.call('CreateMon',r.symbols[party],n,30,31,1,0,1,0)
   assert bool(r.call('IsMonShiny',r.symbols[party]))==row['natural_shiny_enabled']
  for count in ['gPlayerPartyCount','gEnemyPartyCount']:r.write(r.symbols[count],b'\x01')
  r.call('StartScriptedWildBattle')
  for frame in range(6000):
   r.keys={0} if frame%16<2 else set();r.run()
   if r.u32(r.symbols['gMain']+4)==r.symbols['BattleMainCB2']|1 and r.u32(r.symbols['gBattlerControllerFuncs']) in callbacks:break
  else:raise AssertionError(('action menu missing',n))
  r.keys=set();r.run(12);banks=[]
  for side,label in [(0,'back'),(1,'front')]:
   ptr=r.u32(r.u32(r.symbols['gMonSpritesGfxPtr'])+4+4*side)
   folder='yokai_shiny_revised' if row.get('masked_texture') and row['natural_shiny_enabled'] else 'yokai'
   assert r.read(ptr,2048)==(ROOT/f'graphics/{folder}/{n:03}/{label}-battle.4bpp').read_bytes(),(n,label,'tiles')
   sp=r.symbols['gSprites']+68*r.read(r.symbols['gBattlerSpriteIds']+side,1)[0];bank=(int.from_bytes(r.read(sp+4,2),'little')>>12)&15;banks.append(bank)
   initial='shiny' if row['natural_shiny_enabled'] else 'normal'
   assert r.read(r.symbols['gPlttBufferUnfaded']+512+32*bank,32)==(ROOT/f'graphics/yokai/{n:03}/{initial}.gbapal').read_bytes(),(n,label,'automatic palette')
  for kind,table in [('normal','gMonPaletteTable'),('shiny','gMonShinyPaletteTable')]:
   ptr=r.u32(r.symbols[table]+8*n)
   for bank in banks:r.call('LoadCompressedPalette',ptr,256+16*bank,32)
   for side,label in [(0,'back'),(1,'front')]:
    ram=r.u32(r.u32(r.symbols['gMonSpritesGfxPtr'])+4+4*side)
    r.call('LoadSpecialPokePic_DontHandleDeoxys',r.symbols['gMonFrontPicTable' if side else 'gMonBackPicTable']+8*n,ram,n,0,side)
    applied=r.call('TryLoadYokaiShinyPicWithPalette',ram,n,ptr,side)
    assert bool(applied)==bool(kind=='shiny' and row.get('masked_texture'))
    folder='yokai_shiny_revised' if kind=='shiny' and row.get('masked_texture') else 'yokai'
    expected=(ROOT/f'graphics/{folder}/{n:03}/{label}-battle.4bpp').read_bytes();assert r.read(ram,2048)==expected
    sp=r.symbols['gSprites']+68*r.read(r.symbols['gBattlerSpriteIds']+side,1)[0];tile=int.from_bytes(r.read(sp+4,2),'little')&1023
    r.call('CpuSet',ram,0x06010000+tile*32,1024)
    assert r.read(0x06010000+tile*32,2048)==expected
   r.run(2)
   for bank in banks:assert r.read(r.symbols['gPlttBufferUnfaded']+512+32*bank,32)==(ROOT/f'graphics/yokai/{n:03}/{kind}.gbapal').read_bytes(),(n,kind,'loaded palette')
   r.frame.save(out/f'{n:03}-{kind}.png')
  a=Image.new('RGB',(480,180),'#ddd');a.paste(Image.open(out/f'{n:03}-normal.png'),(0,20));a.paste(Image.open(out/f'{n:03}-shiny.png'),(240,20))
  from PIL import ImageDraw
  ImageDraw.Draw(a).text((4,4),f"{n:03} {row['name']} / Normal - Shiny"+(' (palette fixture)' if not row['natural_shiny_enabled'] else ''),fill='black');a.resize((960,360),Image.Resampling.NEAREST).save(out/f'{n:03}-comparaison-x2.png')
  results.append(dict(number=n,natural_shiny=row['natural_shiny_enabled'],explicit_palette_fixture=not row['natural_shiny_enabled'],localized_texture=bool(row.get('masked_texture')),front_back_tiles=True,automatic_palette=True,compiled_normal_shiny_palettes=True))
  if n%10==0:print('MGBA',mode,n,'/151',flush=True)
 # Verify every compiled palette pointer in the current ROM, even on a targeted rerun.
 for n in range(1,152):
  for kind,table in [('normal','gMonPaletteTable'),('shiny','gMonShinyPaletteTable')]:
   r.call('LoadCompressedPalette',r.u32(r.symbols[table]+8*n),256,32)
   assert r.read(r.symbols['gPlttBufferUnfaded']+512,32)==(ROOT/f'graphics/yokai/{n:03}/{kind}.gbapal').read_bytes(),(n,kind,'current ROM palette table')
 passed=True
except BaseException as e:
 error=str(e);r.frame.save(out/'diagnostic.png');raise
finally:
 digest=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest();r.close();(out/'TEST_MGBA.json').write_text(json.dumps(dict(passed=passed,scope=__doc__,rom_sha256=digest,error=error,all_302_current_ROM_palette_pointers_verified=passed,results=results),ensure_ascii=False,indent=2)+'\n')
print('PASS MGBA',mode,len(results),flush=True)
