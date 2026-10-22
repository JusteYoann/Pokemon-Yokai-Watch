#!/usr/bin/env python3
"""Register available scenario artwork without replacing any existing sprite ID."""
import json,re
from pathlib import Path
R=Path(__file__).resolve().parents[2]
P=R/'graphics/yokai_characters/scenario_2026'
spec=json.loads((P/'manifest.json').read_text())
actors=[x['id'] for x in spec['characters'] if (R/'graphics/yokai_characters'/x['id']/'overworld.png').exists()]
def camel(a):return ''.join(s.title() for s in a.split('_'))
def patch(path,name,body,anchor=None):
 p=R/path;s=p.read_text();start='// BEGIN SCENARIO '+name;end='// END SCENARIO '+name
 block=start+'\n'+body+'\n'+end+'\n'
 if start in s:s=re.sub(re.escape(start)+r'.*?'+re.escape(end)+r'\n?',lambda _:block,s,flags=re.S)
 elif anchor:
  assert anchor in s,(path,anchor);s=s.replace(anchor,block+anchor,1)
 else:s+='\n'+block
 p.write_text(s)
const='\n'.join(f'#define OBJ_EVENT_GFX_SCENARIO_{a.upper()} {173+i}' for i,a in enumerate(actors))
patch('include/constants/event_objects.h','IDS',const,'#define NUM_OBJ_EVENT_GFX')
p=R/'include/constants/event_objects.h';s=p.read_text();s=re.sub(r'#define NUM_OBJ_EVENT_GFX\s+\d+',f'#define NUM_OBJ_EVENT_GFX     {173+len(actors)}',s);p.write_text(s)
gfx='const u16 gObjectEventPal_Scenario[] = INCBIN_U16("graphics/yokai_characters/berenice/overworld.gbapal");\n'
for a in actors:gfx+=f'const u16 gObjectEventPic_Scenario{camel(a)}[] = INCBIN_U16("graphics/yokai_characters/{a}/overworld.4bpp");\n'
patch('src/data/object_events/object_event_graphics.h','GRAPHICS',gfx)
pics=''
for a in actors:
 pics+=f'static const struct SpriteFrameImage sPicTable_Scenario{camel(a)}[] = {{\n'
 pics+=''.join(f'    overworld_frame(gObjectEventPic_Scenario{camel(a)}, 2, 4, {i}),\n' for i in range(9))+'};\n'
patch('src/data/object_events/object_event_pic_tables.h','FRAMES',pics)
info=''
for a in actors:
 info+=f'''const struct ObjectEventGraphicsInfo gObjectEventGraphicsInfo_Scenario{camel(a)} = {{
    .tileTag = TAG_NONE, .paletteTag = OBJ_EVENT_PAL_TAG_SCENARIO,
    .reflectionPaletteTag = OBJ_EVENT_PAL_TAG_NONE,
    .size = 256, .width = 16, .height = 32,
    .paletteSlot = PALSLOT_NPC_SPECIAL, .shadowSize = SHADOW_SIZE_M,
    .inanimate = FALSE, .disableReflectionPaletteLoad = FALSE, .tracks = TRACKS_FOOT,
    .oam = &gObjectEventBaseOam_16x32, .subspriteTables = gObjectEventSpriteOamTables_16x32,
    .anims = sAnimTable_Standard, .images = sPicTable_Scenario{camel(a)},
    .affineAnims = gDummySpriteAffineAnimTable,
}};
'''
patch('src/data/object_events/object_event_graphics_info.h','INFO',info)
patch('src/data/object_events/object_event_graphics_info_pointers.h','DECLARATIONS','\n'.join(f'const struct ObjectEventGraphicsInfo gObjectEventGraphicsInfo_Scenario{camel(a)};' for a in actors),'const struct ObjectEventGraphicsInfo gObjectEventGraphicsInfo_YokaiLeoJibanyan;')
patch('src/data/object_events/object_event_graphics_info_pointers.h','POINTERS','\n'.join(f'    [OBJ_EVENT_GFX_SCENARIO_{a.upper()}] = &gObjectEventGraphicsInfo_Scenario{camel(a)},' for a in actors),'    [OBJ_EVENT_GFX_YOKAI_MAFIAMILLE3]')
patch('src/event_object_movement.c','PALETTE_TAG','#define OBJ_EVENT_PAL_TAG_SCENARIO 0x1140','#define OBJ_EVENT_PAL_TAG_YOKAI_WYATT')
patch('src/event_object_movement.c','PALETTE_ENTRY','    {gObjectEventPal_Scenario, OBJ_EVENT_PAL_TAG_SCENARIO},','    {gObjectEventPal_YokaiWyatt, OBJ_EVENT_PAL_TAG_YOKAI_WYATT},')
patch('src/event_object_movement.c','REFLECTION_TAGS','static const u16 sScenarioReflectionPaletteTags[] = {OBJ_EVENT_PAL_TAG_SCENARIO, OBJ_EVENT_PAL_TAG_SCENARIO, OBJ_EVENT_PAL_TAG_SCENARIO, OBJ_EVENT_PAL_TAG_SCENARIO};','static const u16 sYokaiWyattReflectionPaletteTags[]')
patch('src/event_object_movement.c','REFLECTION_ENTRY','    {OBJ_EVENT_PAL_TAG_SCENARIO, sScenarioReflectionPaletteTags},','    {OBJ_EVENT_PAL_TAG_YOKAI_WYATT, sYokaiWyattReflectionPaletteTags},')
patch('include/constants/trainers.h','TRAINER_IDS','\n'.join(f'#define TRAINER_PIC_SCENARIO_{a.upper()} {160+i}' for i,a in enumerate(actors)),'// The player back pics')
train=''
for a in actors:
 train+=f'const u32 gTrainerFrontPic_Scenario{camel(a)}[] = INCBIN_U32("graphics/yokai_characters/{a}/battle.4bpp.lz");\nconst u32 gTrainerPalette_Scenario{camel(a)}[] = INCBIN_U32("graphics/yokai_characters/{a}/normal.gbapal.lz");\n'
patch('src/data/graphics/trainers.h','TRAINERS',train)
patch('include/graphics.h','TRAINER_EXTERNS','\n'.join(f'extern const u32 gTrainerFrontPic_Scenario{camel(a)}[];\nextern const u32 gTrainerPalette_Scenario{camel(a)}[];' for a in actors))
for section,anchor,content in [('COORDS','    [TRAINER_PIC_YOKAI_WYATT]', '\n'.join(f'    [TRAINER_PIC_SCENARIO_{a.upper()}] = {{.size = 8, .y_offset = 1}},' for a in actors)),('TRAINER_SPRITES','    TRAINER_SPRITE(YOKAI_WYATT', '\n'.join(f'    TRAINER_SPRITE(SCENARIO_{a.upper()}, gTrainerFrontPic_Scenario{camel(a)}, 0x800),' for a in actors)),('TRAINER_PALETTES','    TRAINER_PAL(YOKAI_WYATT', '\n'.join(f'    TRAINER_PAL(SCENARIO_{a.upper()}, gTrainerPalette_Scenario{camel(a)}),' for a in actors))]:
 patch('src/data/trainer_graphics/front_pic_tables.h',section,content,anchor)
for a in spec['characters']:
 if a['id'] in actors:
  i=actors.index(a['id']);a.update(status='registered_not_yet_engine_tested',graphics_id=173+i,trainer_pic_id=160+i)
(P/'manifest.json').write_text(json.dumps(spec,ensure_ascii=False,indent=2)+'\n')
print('Registered',len(actors),'map sheets and trainer portraits')
