#!/usr/bin/env python3
"""Real initialized mGBA: native boss-group palettes and Matt's four gait speeds."""
import hashlib,json,re,os
from PIL import Image
from mgba_rpc import ROOT
from mgba_new_game import new_game
P=ROOT/os.environ.get('YOKAI_CAST_GROUP_REPORT_DIR','QA_RECETTE_FINALE/POST_B13/SESSION_2_GRAPHISMES/CAST_GABARIT_FRLG/groupes');P.mkdir(parents=True,exist_ok=True)
C={}
for file in ['flags','event_objects','event_object_movement']:
 C.update({k:int(v,0) for k,v in re.findall(r'^#define\s+(\w+)\s+(0x[0-9A-Fa-f]+|\d+)\b',(ROOT/f'include/constants/{file}.h').read_text(),re.M)})
C['FLAG_SYS_GAME_CLEAR']=0x82C
spec=json.loads((ROOT/'data/yokai/cameos_boss.json').read_text());groups=json.loads((ROOT/'data/maps/map_groups.json').read_text());maps={name:(i,j) for i,k in enumerate(groups['group_order']) for j,name in enumerate(groups[k])};rows=[]
r=new_game();passed=False;error='Interrupted'
def warp(name,x,y):
 g,n=maps[name];r.keys=set();r.call('SetWarpDestination',g,n,255,x,y);r.call('WarpIntoMap');r.call('SetMainCallback2',r.symbols['CB2_LoadMap']|1);r.run(600)
 assert r.u32(r.symbols['gMain']+4)==r.symbols['CB2_Overworld']|1
try:
 r.call('CreateMon',r.symbols['gPlayerParty'],1,30,31,1,100,1,0);r.write(r.symbols['gPlayerPartyCount'],b'\x01')
 clean=r.snapshot()
 for family,name,pal in [('DOMNISCIAN','Domniscian','domniscian'),('MORLEONE','DonMorleone','don_morleone')]:
  boss=next(a for a in spec['actors'] if a['name']==name);expected={a['object_gfx'] for a in spec['graphics'] if a['palette_group']==family}
  for post in [False,True]:
   r.restore(clean)
   if post:
    for f in ['FLAG_SYS_GAME_CLEAR','FLAG_HIDE_SILPH_ROCKETS','FLAG_SILPH_11F_DOOR','FLAG_DEFEATED_ROCKETS_IN_WAREHOUSE','FLAG_HIDE_FIVE_ISLAND_ROCKETS']:r.call('FlagSet',C[f])
   warp(boss['map'],boss['x'],boss['y']+1)
   objects=[r.symbols['gObjectEvents']+36*i for i in range(16) if r.read(r.symbols['gObjectEvents']+36*i,1)[0]&1 and r.read(r.symbols['gObjectEvents']+36*i+5,1)[0] in expected]
   assert len(objects)==(len(expected) if post else 0),(name,post,len(objects))
   if not post:r.frame.save(P/f'{pal}-avant-ligue.png');continue
   source=(ROOT/f'graphics/yokai_characters/{pal}/normal.gbapal').read_bytes();assert r.read(r.symbols['gPlttBufferUnfaded']+512+10*32,32)==source
   contact=Image.new('RGB',(960,160));poses=[]
   for i,d in enumerate([1,2,3,4]):
    for obj in objects:r.call('ObjectEventTurn',obj,d)
    r.run(24)
    for obj in objects:
     sprite=r.symbols['gSprites']+68*r.read(obj+4,1)[0]
     assert not r.read(sprite+62,1)[0]&4
     assert r.read(sprite+5,1)[0]>>4==10
    contact.paste(r.frame,(240*i,0));poses.append(d)
   contact.save(P/f'{pal}-groupe-directions.png');rows.append(dict(group=name,simultaneous_actors=len(objects),palette_bank=10,palette_exact=True,facings=poses,pre_league_hidden=True,passed=True))
 r.restore(clean);r.call('VarSet',0x4050,3);r.call('VarSet',0x4055,9);warp('PalletTown',8,16)
 oid=r.call('SpawnSpecialObjectEventParameterized',C['OBJ_EVENT_GFX_BLUE'],C['MOVEMENT_TYPE_FACE_DOWN'],200,17,23,3);assert oid<16
 obj=r.symbols['gObjectEvents']+36*oid;sprite=r.symbols['gSprites']+68*r.read(obj+4,1)[0]
 header=(ROOT/'include/constants/event_object_movement.h').read_text();anims={k:int(v,0) for k,v in re.findall(r'^#define\s+(ANIM_STD_\w+)\s+(0x[0-9A-Fa-f]+|\d+)\b',header,re.M)}
 cycle=[]
 for speed in ['GO','GO_FAST','GO_FASTER','GO_FASTEST']:
  for d,label,flip in [(3,'WEST',False),(4,'EAST',True)]:
   r.call('ObjectEventTurn',obj,d);r.call('StartSpriteAnim',sprite,anims[f'ANIM_STD_{speed}_{label}']);samples=[];movie=[]
   for f in range(72):
    r.run();attribute=int.from_bytes(r.read(sprite+2,2),'little');assert bool(attribute&0x1000)==flip,(speed,label,f,hex(attribute));samples.append(bool(attribute&0x1000))
    if f%4==0:movie.append(r.frame.copy())
   movie[0].save(P/f'matt-{speed}-{label}.gif',save_all=True,append_images=movie[1:],duration=67,loop=0)
   contact=Image.new('RGB',(960,160))
   for i,f in enumerate([0,2,4,6]):contact.paste(movie[f],(240*i,0))
   contact.save(P/f'matt-{speed}-{label}.png');cycle.append(dict(speed=speed,direction=label,frames=72,constant_correct_hflip=True))
 rows.append(dict(person='Matt',native_gait_cycles=cycle,scope='Animation on a native temporary object, fixed tile; tests gait image directions at all four speeds, not a replay of story movement scripts',passed=True));passed=True;error=None
except BaseException as e:error=str(e);r.frame.save(P/'diagnostic.png');raise
finally:
 r.close();(P/'TEST_MGBA.json').write_text(json.dumps(dict(passed=passed,error=error,rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),scope='Real new-game initialization then RAM progression fixtures and map warps, no saved game changes; does not revalidate complete boss battles/rewards',results=rows),indent=2)+'\n')
print('PASS native simultaneous boss groups, pre/post-League visibility and Matt four-speed horizontal gait')
