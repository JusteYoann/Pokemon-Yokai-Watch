#!/usr/bin/env python3
"""Inventory current committed artwork and capture the BEFORE state in mGBA.
No image, palette, coordinate, species or presentation profile is edited.
Final art choices require the user's BATTLE_SPRITE reference archive.
"""
import argparse,csv,hashlib,json,re,struct,subprocess
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from mgba_rpc import ROOT
from mgba_new_game import new_game
Q=ROOT/'QA_RECETTE_FINALE/CADRAGE_COMBATS_151';Q.mkdir(exist_ok=True)
NAMES=json.loads((ROOT/'data/yokai/noms_affiches.json').read_text())

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def coord(header,species):
 text=(ROOT/header).read_text();b=re.search(r'\['+species+r'\]\s*=\s*\{(.*?)\}',text,re.S)[1]
 return dict(size=[int(v) for v in re.search(r'MON_COORDS_SIZE\((\d+),\s*(\d+)\)',b).groups()],y_offset=int(re.search(r'\.y_offset\s*=\s*(\d+)',b)[1]))
def inventory(stage):
 assert stage!='avant' or not (Q/f'sources/ETAT_{stage.upper()}.json').exists(), "Refusing to overwrite frozen snapshot"
 header=(ROOT/'src/data/graphics/pokemon.h').read_text();rows=[]
 for mon in NAMES:
  n=int(mon['numero_yokai']);species=mon['species_constant'];row=dict(number=n,name=mon['nom_yokai'],species=species,reference_status='reference recovered and numbered',artwork_revision=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip())
  for side in ['front','back']:
   path=ROOT/f'graphics/yokai/{n:03d}/{side}.png';im=Image.open(path)
   assert im.mode=='P' and im.size==(64,64),(path,im.mode,im.size)
   values=list(im.get_flattened_data());assert max(values)<=15 and any(values),(path,'invalid/empty pixel indices')
   mask=Image.new('L',im.size);mask.putdata([255 if v else 0 for v in values]);box=mask.getbbox()
   active=re.findall(r'INCBIN_U32\("(graphics/yokai/'+f'{n:03d}/'+side+r'(?:-display)?\.4bpp\.lz)"\)',header);assert len(active)==1,(n,side,active)
   raw=ROOT/active[0].removesuffix('.lz');assert raw.stat().st_size==2048
   row[side]=dict(original_png=str(path.relative_to(ROOT)),source_sha256=sha(path),active_4bpp=str(raw.relative_to(ROOT)),active_sha256=sha(raw),source_visible_bbox=list(box),source_visible_size=[box[2]-box[0],box[3]-box[1]],source_opaque_pixels=sum(v!=0 for v in values),used_indices=sorted(set(values)),png_index_depth=path.read_bytes()[24],transparent_index=0,coords=coord(f'src/data/pokemon_graphics/{side}_pic_coordinates.h',species))
  for name in ['normal','shiny']:
   path=ROOT/f'graphics/yokai/{n:03d}/{name}.pal';native=path.with_suffix('.gbapal');assert native.stat().st_size==32
   row[name+'_palette']=dict(source=str(path.relative_to(ROOT)),sha256=sha(path),active=str(native.relative_to(ROOT)),active_sha256=sha(native))
  rows.append(row)
 profiles=ROOT/'data/yokai/sprite_presentation.json'
 snapshot=dict(reference_commit=rows[0]['artwork_revision'],reference_archives=['BATTLE_SPRITE1.rar','BATTLE_SPRITE2.rar'],reference_available=True,presentation_profiles_sha256=sha(profiles),species=rows,scope='Current committed latest artwork, not the older drawings appearing in mockups. No correction or approval inferred without inspecting those mockups.')
 (Q/f'sources/ETAT_{stage.upper()}.json').write_text(json.dumps(snapshot,ensure_ascii=False,indent=2)+'\n')
 for path in ['data/yokai/sprite_presentation.json','src/data/pokemon_graphics/front_pic_coordinates.h','src/data/pokemon_graphics/back_pic_coordinates.h']:
  (Q/'sources'/(('apres-' if stage=='apres' else '')+Path(path).name)).write_bytes((ROOT/path).read_bytes())
 with (Q/'INVENTAIRE_151.csv').open('w',newline='') as f:
  w=csv.writer(f,lineterminator='\n');w.writerow(['numero','nom','species','face_source','dos_source','face_active_4bpp','dos_actif_4bpp','face_y','dos_y','reference','etat'])
  for row in rows:w.writerow([row['number'],row['name'],row['species'],row['front']['original_png'],row['back']['original_png'],row['front']['active_4bpp'],row['back']['active_4bpp'],row['front']['coords']['y_offset'],row['back']['coords']['y_offset'],f'references/{row["number"]:03}.png',stage])
 return snapshot

def capture(snapshot,stage):
 out=Q/stage;out.mkdir(exist_ok=True);r=new_game();rows=[];passed=False;error='Interrupted'
 callbacks={int(f[0],16)|1 for line in subprocess.check_output(['arm-none-eabi-nm','--defined-only',str(r.elf_path)],text=True).splitlines() if len(f:=line.split())==3 and f[2]=='HandleInputChooseAction'};assert callbacks
 base=r.snapshot()
 try:
  for mon in snapshot['species']:
   n=mon['number'];r.restore(base)
   for party in ['gPlayerParty','gEnemyParty']:
    r.call('CreateMon',r.symbols[party],n,30,31,1,100,1,0);assert not r.call('IsMonShiny',r.symbols[party])
   for count in ['gPlayerPartyCount','gEnemyPartyCount']:r.write(r.symbols[count],b'\x01')
   r.call('StartScriptedWildBattle')
   for frame in range(6000):
    r.keys={0} if frame%16<2 else set();r.run()
    if r.u32(r.symbols['gMain']+4)==r.symbols['BattleMainCB2']|1 and r.u32(r.symbols['gBattlerControllerFuncs']) in callbacks:break
   else:raise AssertionError(('Battle did not reach native action menu',n))
   r.keys=set();r.run(12);positions={}
   for side,label in [(0,'back'),(1,'front')]:
    ptr=r.u32(r.u32(r.symbols['gMonSpritesGfxPtr'])+4+4*side)
    assert r.read(ptr,2048)==(ROOT/mon[label]['active_4bpp']).read_bytes(),(n,label,'Native loaded art differs from active current source')
    sp=r.symbols['gSprites']+68*r.read(r.symbols['gBattlerSpriteIds']+side,1)[0]
    positions[label]=list(struct.unpack('<hhhh',r.read(sp+32,8)))
    bank=(int.from_bytes(r.read(sp+4,2),'little')>>12)&15
    assert r.read(r.symbols['gPlttBufferUnfaded']+512+32*bank,32)==(ROOT/mon['normal_palette']['active']).read_bytes(),(n,label,'Native palette differs')
   r.frame.save(out/f'{n:03d}.png');rows.append(dict(number=n,name=mon['name'],path=str((out/f'{n:03d}.png').relative_to(ROOT)),native_battle_capture=True,front_and_back_native_art_verified=True,normal_palettes_verified=True,positions_x_y_x2_y2=positions))
   if n%15==0:print(stage.upper(),'NATIVE CAPTURE',n,flush=True)
  passed=True;error=None
 except BaseException as e:error=str(e);r.frame.save(out/'diagnostic.png');raise
 finally:
  r.close();(out/'TEST_MGBA.json').write_text(json.dumps(dict(stage=stage,passed=passed,error=error,rom_sha256=sha(r.elf_path.with_suffix('.gba')),rom_bytes=r.elf_path.with_suffix('.gba').stat().st_size,source_commit=snapshot['reference_commit'],scope='151 original native scripted wild battle fixtures, same species on both sides, normal form. Actual battle action menu reached, linked artwork and palette verified for both sides. See stage field; these are actual engine captures, not mockups. Does not test all animation frames or shiny forms.',results=rows),ensure_ascii=False,indent=2)+'\n')
 if passed:
  font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',13)
  for page in range((len(rows)+15)//16):
   batch=rows[page*16:(page+1)*16];sheet=Image.new('RGB',(1008,776),(232,232,232));d=ImageDraw.Draw(sheet)
   for i,row in enumerate(batch):
    x=i%4*252;y=i//4*194;d.text((x+4,y+3),f"{row['number']:03d} {row['name']}",font=font,fill='black');sheet.paste(Image.open(ROOT/row['path']),(x+6,y+26))
   sheet.save(out/f'planche-{stage}-{page+1:02d}.png')
  print(stage.upper(),'MGBA PASS',len(rows))

def main():
 p=argparse.ArgumentParser();p.add_argument('--capture',action='store_true');p.add_argument('--stage',choices=['avant','apres'],default='avant');a=p.parse_args();snapshot=inventory(a.stage);print('INVENTORY PASS',len(snapshot['species']),flush=True)
 if a.capture:capture(snapshot,a.stage)
if __name__=='__main__':main()
