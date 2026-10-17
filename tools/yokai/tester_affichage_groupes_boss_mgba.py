#!/usr/bin/env python3
"""Native four-facing boss groups, simultaneous palette and safe map-floor checks."""
import hashlib,json
from PIL import Image
from tester_cameos_boss_mgba import fixture,ROOT,P
spec=json.loads((ROOT/'data/yokai/cameos_boss.json').read_text());actors={a['name']:a for a in spec['actors']};results=[]
for name,num,boss,palette in [('domniscian',57,'Domniscian','domniscian'),('morleone',114,'DonMorleone','don_morleone')]:
 group={'map':num,'boss':actors[boss]};expected={a['object_gfx'] for a in spec['graphics'] if a['palette_group']==('DOMNISCIAN' if name=='domniscian' else 'MORLEONE')}
 for post in [False,True]:
  r=fixture(group,post)
  try:
   r.frame.save(P/('cameo-'+name+('-groupe-postgame.png' if post else '-avant-ligue.png')))
   objects=[]
   for i in range(16):
    obj=r.symbols['gObjectEvents']+i*36
    if r.read(obj,1)[0]&1 and r.read(obj+5,1)[0] in expected:objects.append(obj)
   assert len(objects)==(len(expected) if post else 0)
   if not post:continue
   native_palette=r.read(r.symbols['gPlttBufferUnfaded']+512+10*32,32)
   assert native_palette==(ROOT/'graphics/yokai_characters'/palette/'normal.gbapal').read_bytes(),(name,'simultaneous NPC palette mismatch')
   contact=Image.new('RGB',(960,160))
   for i,direction in enumerate([1,2,3,4]):
    for obj in objects:r.call('ObjectEventTurn',obj,direction)
    r.run(24);contact.paste(r.frame,(240*i,0))
   contact.save(P/('cameo-'+name+'-groupe-directions.png'))
   checked=[]
   for actor in [a for a in spec['actors'] if a['map']==group['boss']['map']]:
    for dy in [0,1]:
     x,y=actor['x']+7,actor['y']+7+dy;collision=r.call('MapGridGetCollisionAt',x,y);behavior=r.call('MapGridGetMetatileBehaviorAt',x,y)
     assert collision==0 and behavior not in list(range(0x40,0x48))+list(range(0x54,0x58))+list(range(0x62,0x66)),(actor['name'],'blocked/conveyor/spin/warp tile',dy,collision,behavior)
     checked.append({'person':actor['name'],'tile':[x-7,y-7],'behavior':behavior})
   results.append({'group':name,'postgame_objects':len(objects),'four_native_facings':'south/north/west/east columns','simultaneous_OBJ_palette10_matches_group_source':True,'floor_and_interaction_tiles':checked,'passed':True})
  finally:r.close()
report={'engine':'mGBA libretro','rom_sha256':hashlib.sha256((ROOT/'pokefirered.gba').read_bytes()).hexdigest(),'scope':'Fixtures teleport to real maps; actual four facings and shared palette readback. Wait300frames after CB2_Overworld for map-preview fade before PNG captures. No change to game sprites or map transitions for preview correction. Does not prove maze access during a playthrough.','results':results}
(ROOT/'QA_RECETTE_FINALE/RECONSTRUCTION/TEST_AFFICHAGE_GROUPES_BOSS_MGBA.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False,indent=2))
