#!/usr/bin/env python3
"""Registered Alyzon graphics in compiled ROM: native walks and portrait loaders.
Object positions/party/battle backdrop are RAM fixtures. No graphics/palette table
is patched by this test; no Alyzon trainer team or cinematic is introduced.
"""
from pathlib import Path
import os,sys,json,struct,hashlib,subprocess
from PIL import Image,ImageDraw,ImageFont
sys.path.insert(0,str(Path(__file__).resolve().parent))
from mgba_new_game import new_game
from mafiamille_qa import C,MAPS,warp
from mgba_rpc import ROOT
D=ROOT/'graphics/yokai_characters/alyzon';rom=Path(os.environ.get('YOKAI_QA_ROM',ROOT/'pokefirered.gba'));mode='prive' if '_audio' in rom.name else 'public';Q=ROOT/'docs/lavanville-zombie-night/integration-alyzon'/mode;Q.mkdir(parents=True,exist_ok=True)
GFX=C['OBJ_EVENT_GFX_YOKAI_ALYZON'];PIC=C['TRAINER_PIC_YOKAI_ALYZON'];SLOT=7;report={};passed=False;r=new_game();rows=[];movie=[]
def callconst(name):return r.symbols[name]
def sprite(oid):
 obj=r.symbols['gObjectEvents']+36*oid;sid=r.read(obj+4,1)[0];return obj,r.symbols['gSprites']+68*sid
def vram(sp,n=256):
 tile=struct.unpack('<H',r.read(sp+4,2))[0]&1023;return r.read(0x06010000+tile*32,n)
def save(name):r.frame.save(Q/(name+'.png'));r.frame.resize((720,480),Image.Resampling.NEAREST).save(Q/(name+'-x3.png'))
def assertpal(sp):
 bank=r.read(sp+5,1)[0]>>4;assert bank==SLOT,bank
 assert r.read(r.symbols['gPlttBufferUnfaded']+512+32*bank,32)==(D/'overworld.gbapal').read_bytes()
 return bank
def lz(data):
 assert data[0]==0x10;size=int.from_bytes(data[1:4],'little');p=4;out=bytearray()
 while len(out)<size:
  flags=data[p];p+=1
  for bit in range(7,-1,-1):
   if len(out)>=size:break
   if flags>>bit&1:
    a,b=data[p:p+2];p+=2;n=(a>>4)+3;dist=((a&15)<<8|b)+1
    for _ in range(n):out.append(out[-dist])
   else:out.append(data[p]);p+=1
 return bytes(out[:size])
try:
 # First prove that the original resources really exist in this ROM, not just in files.
 raw=(D/'overworld.4bpp').read_bytes();assert len(raw)==2304
 assert r.read(r.symbols['gObjectEventPic_YokaiAlyzon'],len(raw))==raw
 assert r.read(r.symbols['gObjectEventPal_YokaiAlyzon'],32)==(D/'overworld.gbapal').read_bytes()
 pp=r.symbols['gTrainerFrontPic_YokaiAlyzon'];assert lz(r.read(pp,len((D/'battle.4bpp.lz').read_bytes())))==(D/'battle.4bpp').read_bytes()
 assert r.u32(r.symbols['gObjectEventGraphicsInfoPointers']+4*GFX)==r.symbols['gObjectEventGraphicsInfo_YokaiAlyzon']
 rows.append(dict(test='Compiled registered assets',passed=True,ow_bytes=2304,ow_id=GFX,portrait_id=PIC))
 warp(r,*MAPS['LavenderTown'],15,10);player_before=r.read(r.symbols['gPlttBufferUnfaded']+512,32);npc_before=r.read(r.symbols['gPlttBufferUnfaded']+512+2*32,4*32)
 oid=r.call('SpawnSpecialObjectEventParameterized',GFX,C['MOVEMENT_TYPE_FACE_DOWN'],200,20,15,3);assert oid<16
 obj,sp=sprite(oid);r.run(8);assertpal(sp)
 assert r.read(r.symbols['gPlttBufferUnfaded']+512,32)==player_before
 assert r.read(r.symbols['gPlttBufferUnfaded']+512+2*32,4*32)==npc_before
 assert r.u32(sp+12)==r.symbols['sPicTable_YokaiAlyzon']
 base=r.snapshot()
 for label,dr,anim,action,delta,allowed in [('face',1,0,'MOVEMENT_ACTION_WALK_NORMAL_DOWN',(0,1),[0,3,4]),('dos',2,1,'MOVEMENT_ACTION_WALK_NORMAL_UP',(0,-1),[1,5,6]),('gauche',3,2,'MOVEMENT_ACTION_WALK_NORMAL_LEFT',(-1,0),[2,7,8]),('droite',4,3,'MOVEMENT_ACTION_WALK_NORMAL_RIGHT',(1,0),[2,7,8])]:
  r.restore(base);obj,sp=sprite(oid);r.call('ObjectEventTurn',obj,dr);r.call('StartSpriteAnim',sp,anim);r.run(8)
  assertpal(sp);assert vram(sp)==raw[256*allowed[0]:256*(allowed[0]+1)],label
  flip=bool(struct.unpack('<H',r.read(sp+2,2))[0]&0x1000);assert flip==(label=='droite')
  save('repos-'+label);clip=[r.frame.copy() for _ in range(6)]
  for step in range(3):
   r.call('ObjectEventSetHeldMovement',obj,C[action]);seen=set()
   for f in range(36):
    r.run();tile=vram(sp);match=[n for n in allowed if tile==raw[256*n:256*(n+1)]];assert match,(label,f)
    seen.update(match)
    if f%2==0:clip.append(r.frame.copy())
   r.call('ObjectEventClearHeldMovementIfFinished',obj);xy=struct.unpack('<hh',r.read(obj+16,4));actual=(xy[0]-7,xy[1]-7);expect=(13+(step+1)*delta[0],8+(step+1)*delta[1]);assert actual==expect,(label,actual,expect)
   assertpal(sp);assert r.u32(sp+12)==r.symbols['sPicTable_YokaiAlyzon']
   rows.append(dict(test='Native held walk with registered ROM images',direction=label,step=step+1,arrived=actual,source_frames_seen=sorted(seen),passed=True))
  movie.extend(clip+[r.frame.copy() for _ in range(8)])
 movie[0].resize((720,480),Image.Resampling.NEAREST).save(Q/'marche-enregistree-mgba.gif',save_all=True,append_images=[im.resize((720,480),Image.Resampling.NEAREST) for im in movie[1:]],duration=34,loop=0)
 # Native graphics-ID changes must also restore the dedicated palette.
 r.restore(base);obj,sp=sprite(oid)
 r.call('ObjectEventSetGraphicsId',obj,C['OBJ_EVENT_GFX_BOY']);r.run(8)
 r.call('ObjectEventSetGraphicsId',obj,GFX);r.run(8);assertpal(sp);assert r.u32(sp+12)==r.symbols['sPicTable_YokaiAlyzon'];rows.append(dict(test='Native graphics ID change back to Alyzon',passed=True))
 # Return-to-field uses its real callback, rebuilding object images/palettes.
 r.call('SetMainCallback2',r.symbols['CB2_ReturnToField']|1)
 for f in range(900):
  r.run()
  if f>60 and r.u32(r.symbols['gMain']+4)==r.symbols['CB2_Overworld']|1:break
 else:raise AssertionError('Return-to-field timeout')
 obj,sp=sprite(oid);assertpal(sp);assert r.u32(sp+12)==r.symbols['sPicTable_YokaiAlyzon'];save('retour-terrain');rows.append(dict(test='Native return-to-field sprite rebuild',passed=True))
 # Cinematic virtual-object factory also has to load the compiled palette.
 r.restore(base);r.call('InitObjectEventPalettes',0)
 vsid=r.call('CreateVirtualObject',GFX,203,13,8,3,1);assert vsid<64
 vsp=r.symbols['gSprites']+68*vsid;r.run(8);assertpal(vsp)
 assert r.u32(vsp+12)==r.symbols['sPicTable_YokaiAlyzon']
 rows.append(dict(test='Native virtual object factory and palette',passed=True))
 # Independent palette even while existing Matt/Don share the scene.
 r.restore(base)
 # Use Pewter, where the existing story already gives Matt its separate bank6.
 warp(r,*MAPS['PewterCity'],15,18);actors={}
 for gfx,lid,x in [(GFX,200,14),(C['OBJ_EVENT_GFX_YOKAI_DONMORLEONE'],201,16),(C['OBJ_EVENT_GFX_BLUE'],202,15)]:
  who=r.call('SpawnSpecialObjectEventParameterized',gfx,C['MOVEMENT_TYPE_FACE_DOWN'],lid,x+7,17+7,3);assert who<16
  actors[gfx]=who
  if gfx==GFX:aly=who
 r.run(8);_,asp=sprite(aly);assertpal(asp)
 r.call('ObjectEventSetGraphicsId',sprite(aly)[0],GFX);r.run(8)
 for gfx,expected_bank,palette_symbol in [(GFX,7,'gObjectEventPal_YokaiAlyzon'),(C['OBJ_EVENT_GFX_YOKAI_DONMORLEONE'],10,'gObjectEventPal_YokaiDonMorleoneGroup'),(C['OBJ_EVENT_GFX_BLUE'],6,'gObjectEventPal_Matt')]:
  _,other_sp=sprite(actors[gfx]);bank=r.read(other_sp+5,1)[0]>>4;assert bank==expected_bank,(gfx,bank)
  assert r.read(r.symbols['gPlttBufferUnfaded']+512+32*bank,32)==r.read(r.symbols[palette_symbol],32),(gfx,'palette overwritten')
 assert r.call('GetObjectPaletteTag',SLOT)==0x112B;save('palettes-alyzon-matt-don');rows.append(dict(test='Alyzon/Matt/Don palettes and Alyzon reload preserve all three actors',passed=True,palette_banks=[7,6,10]))
 # Portrait loaded through the real battle resource tables, with no new trainer team.
 r.restore(base);r.call('CreateMon',r.symbols['gPlayerParty'],1,30,31,1,100,0,0);r.write(r.symbols['gPlayerPartyCount'],b'\x01');r.write(r.symbols['gTrainerBattleOpponent_A'],struct.pack('<H',C['TRAINER_LEADER_BROCK']));r.call('StartTrainerBattle')
 for f in range(1600):
  r.run();sid=r.read(r.symbols['gBattlerSpriteIds']+1,1)[0]
  if sid<64:
   bsp=r.symbols['gSprites']+sid*68
   if r.read(bsp+62,1)[0]&1 and struct.unpack('<H',r.read(bsp+6,2))[0]==C['TRAINER_PIC_LEADER_BROCK'] and struct.unpack('<h',r.read(bsp+36,2))[0]==0:break
 else:raise AssertionError('Trainer intro not ready')
 # Freeze this graphics test backdrop; the original battle identity is not replaced.
 for i in range(4):r.w32(r.symbols['gBattlerControllerFuncs']+4*i,r.symbols['BattleControllerDummy']|1)
 r.write(bsp+62,bytes([r.read(bsp+62,1)[0]|4]))
 r.call('DecompressTrainerFrontPic',PIC,1);r.call('SetMultiuseSpriteTemplateToTrainerBack',PIC,1)
 sid=r.call('CreateSprite',r.symbols['gMultiuseSpriteTemplate'],176,40,1);assert sid<64;psp=r.symbols['gSprites']+68*sid
 bank=r.call('IndexOfSpritePaletteTag',PIC);tile=r.call('GetSpriteTileStartByTag',PIC);assert bank<16 and tile<1024
 attr=struct.unpack('<H',r.read(psp+4,2))[0];r.write(psp+4,struct.pack('<H',(attr&0x0C00)|tile|(bank<<12)));r.w32(psp+28,r.symbols['SpriteCallbackDummy']|1)
 r.run(8)
 assert r.read(0x06010000+tile*32,2048)==(D/'battle.4bpp').read_bytes()
 assert r.read(r.symbols['gPlttBufferUnfaded']+512+bank*32,32)==(D/'normal.gbapal').read_bytes()
 assert r.u32(psp+8)==r.u32(r.symbols['gTrainerFrontAnimsPtrTable']+4*PIC)
 save('portrait-charge-moteur');rows.append(dict(test='Native battle portrait loader, sprite factory and palette',passed=True,portrait_id=PIC,scope='Existing battle backdrop fixture; no permanent trainer/team replacement'))
 passed=True
finally:
 if not passed:r.frame.save(Q/'diagnostic.png')
 report=dict(passed=passed,mode=mode,engine='mGBA libretro',rom=str(rom.name),rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),rom_size=len(r.rom_buffer.raw)-1,resources_from_rom=True,no_graphics_or_palette_ram_override=True,tests=rows,limitations=['Map positions and battle backdrop are temporary RAM fixtures','No cinematic, team, badge or permanent map placement created','The portrait test loads ID160 in an existing battle backdrop, not a newly scripted Alyzon battle'])
 (Q/'TEST_MGBA.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');r.close()
print(json.dumps(report,ensure_ascii=False))
