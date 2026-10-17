#!/usr/bin/env python3
"""Add repeatable catchable events in maps without native wild encounter terrain.

Item-ball graphics are explicit provisional containers, not completed Yo-kai OW art.
"""
import json,re,struct
from pathlib import Path
R=Path(__file__).resolve().parents[2]
species={int(v):k for k,v in re.findall(r'^#define\s+(SPECIES_\w+)\s+(\d+)\s*$',(R/'include/constants/species.h').read_text(),re.M)}
layout={x['id']:x for x in json.loads((R/'data/layouts/layouts.json').read_text())['layouts'] if 'id' in x}
events=[
 (51,'SilphCo_3F',7,5,28), (61,'SilphCo_5F',13,5,27), (108,'SilphCo_9F',19,9,30),
 (55,'UndergroundPath_EastWestTunnel',12,3,20), (93,'UndergroundPath_NorthSouthTunnel',3,20,18),
 (96,'SSAnne_1F_Corridor',8,9,20),
 (110,'RocketHideout_B1F',14,4,24), (121,'RocketHideout_B2F',27,4,25),
 (122,'RocketHideout_B3F',5,3,26), (142,'RocketHideout_B4F',6,6,27),
 (133,'Route17',4,5,38), (148,'SevenIsland_SevaultCanyon',10,5,60),
]
report=[]
for n,mapname,x,y,level in events:
 path=R/'data/maps'/mapname/'map.json';m=json.loads(path.read_text());l=layout[m['layout']]
 tiles=struct.unpack('<'+'H'*(l['width']*l['height']),(R/l['blockdata_filepath']).read_bytes())
 tile=tiles[y*l['width']+x];assert tile&0xC00==0 and tile>>12==3,(mapname,x,y,hex(tile))
 for kind in ['object_events','warp_events','coord_events','bg_events']:
  for o in m.get(kind,[]):
   if o.get('script')==f'{mapname}_EventScript_Yokai{n:03}':continue
   assert (o['x'],o['y'])!=(x,y),(mapname,kind,x,y)
 label=f'{mapname}_EventScript_Yokai{n:03}'
 m['object_events']=[o for o in m['object_events'] if o.get('script')!=label]
 m['object_events'].append({'type':'object','graphics_id':'OBJ_EVENT_GFX_ITEM_BALL','x':x,'y':y,
  'elevation':3,'movement_type':'MOVEMENT_TYPE_FACE_DOWN','movement_range_x':0,'movement_range_y':0,
  'trainer_type':'TRAINER_TYPE_NONE','trainer_sight_or_berry_tree_id':'0','script':label,'flag':'0'})
 assert len(m['object_events'])<=64
 path.write_text(json.dumps(m,indent=2)+'\n')
 script=path.with_name('scripts.inc');s=script.read_text()
 if label+'::' in s:s=s[:s.index('\n'+label+'::')]
 gate='\tgoto_if_unset FLAG_SYS_GAME_CLEAR, EventScript_ReleaseEnd\n' if n==148 else ''
 s+=f'''
{label}::
	lock
	faceplayer
{gate}	bufferspeciesname STR_VAR_1, {species[n]}
	msgbox {label}_Text, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EventScript_ReleaseEnd
	setwildbattle {species[n]}, {level}
	dowildbattle
	release
	end
{label}_Text::
	.string "Un {{STR_VAR_1}} se cache ici.\\n"
	.string "Veux-tu le rencontrer?$"
'''
 script.write_text(s)
 report.append({'number':n,'map':mapname,'coordinates':[x,y],'level':level,'script':label,'repeatable':True,'catchable':True,'post_league_only':n==148,'graphics':'provisional item-ball container','collision_tile_checked':True,'actual_walkthrough_tested':False})
(R/'data/yokai/rencontres_script.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(len(report),'scripted catchable events added; map walkthrough and artwork still pending')
