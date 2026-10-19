#!/usr/bin/env python3
"""Preservation checks and native shiny/blocked-shiny battle rendering fixtures."""
import hashlib,json,re,subprocess
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from mgba_rpc import ROOT
from mgba_new_game import new_game
Q=ROOT/'QA_RECETTE_FINALE/CADRAGE_COMBATS_151'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 before=json.loads((Q/'sources/ETAT_AVANT.json').read_text());after=json.loads((Q/'sources/ETAT_APRES.json').read_text());checks=[]
 policy=json.loads((ROOT/'data/yokai/shiny_artwork_policy.json').read_text());assert not policy['dedicated_bitmaps_enabled'];retired={r['number']:r for r in policy['species']}
 for a,b in zip(before['species'],after['species']):
  assert a['number']==b['number']
  for side in ['front','back']:assert a[side]['source_sha256']==sha(ROOT/a[side]['original_png'])==b[side]['source_sha256']
  for pal in ['normal_palette','shiny_palette']:
   if pal=='shiny_palette' and a['number'] in retired:
    row=retired[a['number']];assert a[pal]['sha256']==row['retired_palette_sha256'];assert sha(ROOT/a[pal]['source'])==b[pal]['sha256']
    expected=[row['retired_palette'][i] for i in row['normal_index_to_retired_palette_index']];actual=[list(map(int,l.split())) for l in (ROOT/a[pal]['source']).read_text().splitlines()[3:]];assert actual==expected
   else:assert a[pal]['sha256']==sha(ROOT/a[pal]['source'])==b[pal]['sha256']
 checks.append('All302 original normal PNG and151 normal palettes unchanged;146 shiny palettes unchanged;5 palettes remapped to normal artwork indices using existing colors')
 # Original independent shiny drawings and overworld assets are also immutable.
 baseline=before['reference_commit'];allowed=['data/yokai/sprite_presentation.json','src/data/graphics/pokemon.h','src/data/pokemon_graphics/front_pic_coordinates.h','src/data/pokemon_graphics/back_pic_coordinates.h','src/decompress.c','data/yokai/shiny_artwork_policy.json']+[f'graphics/yokai/{n:03}/shiny.pal' for n in retired]
 changed=subprocess.check_output(['git','diff',baseline,'--name-only'],cwd=ROOT,text=True).splitlines()
 assert all(p in allowed or p.startswith(('QA_RECETTE_FINALE/CADRAGE_COMBATS_151/','tools/yokai/')) for p in changed),changed
 for folder in ['graphics/yokai_shiny','graphics/yokai_characters','sound','data/maps','data/scripts','src/data/pokemon','src/data/trainers.h','src/battle_script_commands.c']:
  assert not subprocess.check_output(['git','diff',baseline,'--',folder],cwd=ROOT,text=True),folder
 # Normal decompression prefix unchanged; retired hook cannot overwrite artwork.
 current=(ROOT/'src/decompress.c').read_text();old=subprocess.check_output(['git','show',baseline+':src/decompress.c'],cwd=ROOT,text=True)
 assert current.split('// Dedicated shiny drawings retired')[0]==old.split('// Palette selection already contains')[0]
 assert not re.search(r'INCBIN.*graphics/yokai_shiny/',current)
 hook=current.split('bool8 TryLoadYokaiShinyPicWithPalette',1)[1];assert re.search(r'\{\s*return FALSE;\s*\}\s*$',hook)
 assert not any('/shiny-' in p['id'] for p in json.loads((ROOT/'data/yokai/sprite_presentation.json').read_text())['profiles'])
 symbols=subprocess.check_output(['arm-none-eabi-nm','--defined-only',str(ROOT/'pokefirered_audio.elf')],text=True);assert 'sYokaiShiny019Front' not in symbols
 checks.append('Gameplay, overworld and audio unchanged;5 dedicated bitmaps no longer linked;normal decompression unchanged')
 allowed_species=set(re.findall(r'\[(SPECIES_\w+)\] = TRUE',(ROOT/'src/data/pokemon/yokai_shiny.h').read_text()));assert len(allowed_species)==84
 out=Q/'shiny';out.mkdir(exist_ok=True);r=new_game();base=r.snapshot();rows=[];passed=False;error=None
 callbacks={int(f[0],16)|1 for line in subprocess.check_output(['arm-none-eabi-nm','--defined-only',str(r.elf_path)],text=True).splitlines() if len(f:=line.split())==3 and f[2]=='HandleInputChooseAction'}
 try:
  for mon in after['species']:
   n=mon['number'];r.restore(base);expected=mon['species'] in allowed_species
   for party in ['gPlayerParty','gEnemyParty']:
    r.call('CreateMon',r.symbols[party],n,30,31,1,0,1,0);assert bool(r.call('IsMonShiny',r.symbols[party]))==expected
   for count in ['gPlayerPartyCount','gEnemyPartyCount']:r.write(r.symbols[count],b'\x01')
   r.call('StartScriptedWildBattle')
   for frame in range(6000):
    r.keys={0} if frame%16<2 else set();r.run()
    if r.u32(r.symbols['gMain']+4)==r.symbols['BattleMainCB2']|1 and r.u32(r.symbols['gBattlerControllerFuncs']) in callbacks:break
   else:raise AssertionError(('battle action menu not reached',n))
   r.keys=set();r.run(12)
   palette=ROOT/mon['shiny_palette' if expected else 'normal_palette']['active']
   for side,label in [(0,'back'),(1,'front')]:
    ptr=r.u32(r.u32(r.symbols['gMonSpritesGfxPtr'])+4+4*side);path=ROOT/mon[label]['active_4bpp']
    assert r.read(ptr,2048)==path.read_bytes(),(n,label,'indexed artwork mismatch')
    sp=r.symbols['gSprites']+68*r.read(r.symbols['gBattlerSpriteIds']+side,1)[0];bank=(int.from_bytes(r.read(sp+4,2),'little')>>12)&15
    assert r.read(r.symbols['gPlttBufferUnfaded']+512+32*bank,32)==palette.read_bytes(),(n,label,'palette mismatch')
   r.frame.save(out/f'{n:03}.png');rows.append(dict(number=n,shiny_requested=True,actual_shiny=expected,both_native_sprites_verified=True,both_palettes_verified=True))
   if n%15==0:print('SHINY/BLOCKED NATIVE CAPTURE',n,flush=True)
  passed=True
 except BaseException as e:error=str(e);r.frame.save(out/'diagnostic.png');raise
 finally:
  r.close();(out/'TEST_MGBA.json').write_text(json.dumps(dict(passed=passed,error=error,rom_sha256=sha(r.elf_path.with_suffix('.gba')),preservation_checks=checks,scope='Real mGBA battle action menu using explicit party fixtures. PID0 requests shiny;84 allowed,67 blocked. Both sides native tile bytes and palette banks checked. Not all attack animations or full adventure.',results=rows),ensure_ascii=False,indent=2)+'\n')
 if passed:
  font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',13)
  for page in range(19):
   batch=rows[page*8:page*8+8];im=Image.new('RGB',(496,len(batch)*184),'#ddd');d=ImageDraw.Draw(im)
   for i,row in enumerate(batch):
    n=row['number'];y=i*184;d.text((4,y),f"{n:03} Normal / "+('Shiny' if row['actual_shiny'] else 'Statut shiny interdit'),fill='black',font=font)
    im.paste(Image.open(Q/f'apres/{n:03}.png'),(4,y+20));im.paste(Image.open(out/f'{n:03}.png'),(252,y+20))
   im.save(out/f'comparatif-shiny-{page+1:02}.png')
  print('SHINY/BLOCKED MGBA PASS',len(rows),flush=True)
if __name__=='__main__':main()
