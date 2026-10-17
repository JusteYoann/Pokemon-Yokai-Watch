#!/usr/bin/env python3
"""Install Ariane's approved teams, optional script and original native assets.

Reuses two verified-unused RS trainer entries; species IDs/save structure stay fixed.
"""
import csv,json,re
from pathlib import Path
R=Path(__file__).resolve().parents[2]
if 'TRAINER_PIC_ARIANE' in (R/'include/constants/trainers.h').read_text():
    raise SystemExit('Ariane already integrated; modify active sources rather than rerun this one-time installer.')
def edit(path,fn):
 p=R/path;s=p.read_text();p.write_text(fn(s))
def append_array(text,name,addition):
 m=re.search(r'('+name+r'\[[^]]*\][^=]*=\s*\{)(.*?)(\n\};)',text,re.S);assert m,name
 if addition.strip() in m[2]:return text
 return text[:m.end(2)]+ '\n'+addition+text[m.end(2):]
# Reuse native unused trainer slots, not flags beyond MAX_TRAINERS_COUNT.
edit('include/constants/opponents.h',lambda s:s.replace('#define TRAINER_NONE                               0','#define TRAINER_NONE                               0\n#define TRAINER_YOKAI_ARIANE                       TRAINER_AQUA_LEADER\n#define TRAINER_YOKAI_ARIANE_POST                  TRAINER_AQUA_GRUNT_M'))
edit('include/constants/trainers.h',lambda s:s.replace('#define TRAINER_PIC_PAINTER               147','#define TRAINER_PIC_PAINTER               147\n#define TRAINER_PIC_ARIANE                148'))
edit('include/constants/event_objects.h',lambda s:s.replace('#define NUM_OBJ_EVENT_GFX     152','#define OBJ_EVENT_GFX_ARIANE 152\n#define OBJ_EVENT_GFX_USAPION_CAMEO 153\n#define NUM_OBJ_EVENT_GFX     154'))
edit('include/constants/flags.h',lambda s:s.replace('#define FLAG_0x300               0x300','#define FLAG_0x300               0x300\n#define FLAG_YOKAI_ARIANE_WON         FLAG_0x300\n#define FLAG_YOKAI_ARIANE_REWARD      FLAG_0x301\n#define FLAG_YOKAI_ARIANE_POST_WON    FLAG_0x302'))
# Battle graphics: extend every corresponding table together.
edit('include/graphics.h',lambda s:s.replace('extern const u32 gTrainerFrontPic_RivalEarly[];','extern const u32 gTrainerFrontPic_Ariane[];\nextern const u32 gTrainerPalette_Ariane[];\nextern const u32 gTrainerFrontPic_RivalEarly[];'))
edit('src/data/graphics/trainers.h',lambda s:s+'\nconst u32 gTrainerFrontPic_Ariane[] = INCBIN_U32("graphics/yokai_characters/ariane/battle.4bpp.lz");\nconst u32 gTrainerPalette_Ariane[] = INCBIN_U32("graphics/yokai_characters/ariane/normal.gbapal.lz");\n')
def front(s):
 for name,row in [('gTrainerFrontPicCoords','    [TRAINER_PIC_ARIANE] = {.size = 8, .y_offset = 1},'),('gTrainerFrontPicTable','    TRAINER_SPRITE(ARIANE, gTrainerFrontPic_Ariane, 0x800),'),('gTrainerFrontPicPaletteTable','    TRAINER_PAL(ARIANE, gTrainerPalette_Ariane),')]:s=append_array(s,name,row)
 return s
edit('src/data/trainer_graphics/front_pic_tables.h',front)
edit('src/data/trainer_graphics/front_pic_anims.h',lambda s:append_array(s,'gTrainerFrontAnimsPtrTable','    [TRAINER_PIC_ARIANE] = sAnims_AquaLeaderArchie,'))
edit('src/data/object_events/object_event_graphics.h',lambda s:s+'\nconst u16 gObjectEventPal_Ariane[] = INCBIN_U16("graphics/yokai_characters/ariane/normal.gbapal");\nconst u16 gObjectEventPic_Ariane[] = INCBIN_U16("graphics/yokai_characters/ariane/overworld.4bpp");\nconst u16 gObjectEventPic_UsapionCameo[] = INCBIN_U16("graphics/yokai_characters/ariane/usapion_overworld.4bpp");\n')
def pointers(s):
 declarations='const struct ObjectEventGraphicsInfo gObjectEventGraphicsInfo_Ariane;\nconst struct ObjectEventGraphicsInfo gObjectEventGraphicsInfo_UsapionCameo;\n'
 s=declarations+s
 name=re.search(r'const struct ObjectEventGraphicsInfo \*const (\w+)\[',s)[1]
 return append_array(s,name,'    [OBJ_EVENT_GFX_ARIANE] = &gObjectEventGraphicsInfo_Ariane,\n    [OBJ_EVENT_GFX_USAPION_CAMEO] = &gObjectEventGraphicsInfo_UsapionCameo,')
edit('src/data/object_events/object_event_graphics_info_pointers.h',pointers)
edit('src/data/object_events/object_event_pic_tables.h',lambda s:s+'''\nstatic const struct SpriteFrameImage sPicTable_Ariane[] = {
    overworld_frame(gObjectEventPic_Ariane, 2, 4, 0),
    overworld_frame(gObjectEventPic_Ariane, 2, 4, 1),
    overworld_frame(gObjectEventPic_Ariane, 2, 4, 2),
};
static const struct SpriteFrameImage sPicTable_UsapionCameo[] = {
    overworld_frame(gObjectEventPic_UsapionCameo, 4, 4, 0),
};
''')
# Stationary cameo: only facing animations are necessary. Fallback movement entries
# reference the same facing frame instead of nonexistent walking frame indices.
def anims(s):
 a=s.index('static const union AnimCmd *const sAnimTable_Standard[] = {');b=s.index('\n};',a)+3
 t=s[a:b].replace('sAnimTable_Standard','sAnimTable_Ariane')
 t=re.sub(r'= sAnim_Go\w*?(South|North|West|East),',lambda m:'= sAnim_Face'+m[1]+',',t)
 t=t.replace('sAnim_RaiseHand','sAnim_FaceSouth')
 return s+'\n'+t+'\n'
edit('src/data/object_events/object_event_anims.h',anims)
def info(s):
 a=s.index('const struct ObjectEventGraphicsInfo gObjectEventGraphicsInfo_Woman1 = {');b=s.index('\n};',a)+3
 human=s[a:b].replace('gObjectEventGraphicsInfo_Woman1','gObjectEventGraphicsInfo_Ariane').replace('OBJ_EVENT_PAL_TAG_NPC_GREEN','OBJ_EVENT_PAL_TAG_ARIANE').replace('PALSLOT_NPC_3','PALSLOT_NPC_SPECIAL').replace('sPicTable_Woman1','sPicTable_Ariane').replace('sAnimTable_Standard','sAnimTable_Ariane')
 assert 'PALSLOT_NPC_SPECIAL' in human and 'sPicTable_Ariane' in human
 monster='''const struct ObjectEventGraphicsInfo gObjectEventGraphicsInfo_UsapionCameo = {
    .tileTag = TAG_NONE, .paletteTag = OBJ_EVENT_PAL_TAG_ARIANE,
    .reflectionPaletteTag = OBJ_EVENT_PAL_TAG_NONE,
    .size = 512, .width = 32, .height = 32,
    .paletteSlot = PALSLOT_NPC_SPECIAL, .shadowSize = SHADOW_SIZE_M,
    .inanimate = TRUE, .disableReflectionPaletteLoad = FALSE, .tracks = TRACKS_NONE,
    .oam = &gObjectEventBaseOam_32x32, .subspriteTables = gObjectEventSpriteOamTables_32x32,
    .anims = sAnimTable_Inanimate, .images = sPicTable_UsapionCameo,
    .affineAnims = gDummySpriteAffineAnimTable,
};'''
 return s+'\n'+human+'\n'+monster+'\n'
edit('src/data/object_events/object_event_graphics_info.h',info)
def event(s):
 s=s.replace('#define OBJ_EVENT_PAL_TAG_MATT                        0x111C','#define OBJ_EVENT_PAL_TAG_ARIANE                      0x111D\n#define OBJ_EVENT_PAL_TAG_MATT                        0x111C')
 s=s.replace('    {gObjectEventPal_Matt, OBJ_EVENT_PAL_TAG_MATT},','    {gObjectEventPal_Matt, OBJ_EVENT_PAL_TAG_MATT},\n    {gObjectEventPal_Ariane, OBJ_EVENT_PAL_TAG_ARIANE},')
 s=s.replace('static const u16 sMattReflectionPaletteTags[] =','static const u16 sArianeReflectionPaletteTags[] = {OBJ_EVENT_PAL_TAG_ARIANE, OBJ_EVENT_PAL_TAG_ARIANE, OBJ_EVENT_PAL_TAG_ARIANE, OBJ_EVENT_PAL_TAG_ARIANE};\n\nstatic const u16 sMattReflectionPaletteTags[] =')
 s=s.replace('    {OBJ_EVENT_PAL_TAG_MATT,                sMattReflectionPaletteTags},','    {OBJ_EVENT_PAL_TAG_MATT,                sMattReflectionPaletteTags},\n    {OBJ_EVENT_PAL_TAG_ARIANE,              sArianeReflectionPaletteTags},')
 return s
edit('src/event_object_movement.c',event)
# Original approved species/order/levels; only unspecified moves and IVs are selected.
lookup={int(v):k for k,v in re.findall(r'^#define\s+(SPECIES_\w+)\s+(\d+)\s*$',(R/'include/constants/species.h').read_text(),re.M)}
learns=list(csv.DictReader((R/'data/yokai/attaques_validees.csv').open(),delimiter=';'))
configs=[('TRAINER_AQUA_LEADER','sParty_YokaiAriane',[(100,17),(28,18),(145,20)],150),('TRAINER_AQUA_GRUNT_M','sParty_YokaiArianePost',[(101,56),(28,57),(110,58),(30,59),(145,60)],200)]
metadata=[]
for old,symbol,members,iv in configs:
 part='static const struct TrainerMonItemCustomMoves '+symbol+'[] = {\n';data=[]
 for n,level in members:
  moves=[]
  for row in learns:
   if int(row['numero_yokai'])==n and row['apprentissage']!='EVOLUTION_PLUS_2' and int(row['niveau'])<=level and row['move_id'] not in moves:moves=(moves+[row['move_id']])[-4:]
  moves+=['MOVE_NONE']*(4-len(moves))
  part+='    {.iv = '+str(iv)+', .lvl = '+str(level)+', .species = '+lookup[n]+', .heldItem = ITEM_NONE, .moves = {'+', '.join(moves)+'}},\n'
  data.append({'number':n,'species':lookup[n],'level':level,'moves':moves,'held_item':'ITEM_NONE'})
 part+='};\n';edit('src/data/trainer_parties.h',lambda s:s+'\n'+part)
 body='''    ['''+old+'''] = {
        .trainerClass = TRAINER_CLASS_COOLTRAINER,
        .encounterMusic_gender = TRAINER_ENCOUNTER_MUSIC_FEMALE | F_TRAINER_FEMALE,
        .trainerPic = TRAINER_PIC_ARIANE,
        .trainerName = _("Ariane"),
        .items = {}, .doubleBattle = FALSE,
        .aiFlags = AI_SCRIPT_CHECK_BAD_MOVE | AI_SCRIPT_TRY_TO_FAINT | AI_SCRIPT_CHECK_VIABILITY,
        .party = ITEM_CUSTOM_MOVES('''+symbol+'''),
    },'''
 edit('src/data/trainers.h',lambda s:re.sub(r'    \['+old+r'\] = \{.*?\n    \},',lambda m:body,s,count=1,flags=re.S))
 metadata.append({'trainer_entry':old,'members':data})
(R/'data/yokai/cameo_ariane.json').write_text(json.dumps({'specification':'CAMEOS_YOKAI_WATCH_CODEX.md + last mandate: Usapion visibly next to Ariane','teams':metadata,'reward':'ITEM_MOON_STONE','reward_once_flag':'FLAG_YOKAI_ARIANE_REWARD','location':'Route25','artwork':'original battle portrait, three overworld facings, Usapion static companion','not_complete':'Other cameos remain to integrate'},ensure_ascii=False,indent=2)+'\n')
