#!/usr/bin/env python3
"""One-time active-resource integration, guarded against incomplete artwork.

Run only after all generated sets have been reviewed. Builds use committed
sources directly, never this installer. Species/gameplay/trainer parties stay fixed.
"""
import json,re
from pathlib import Path
from PIL import Image
R=Path(__file__).resolve().parents[2]
required={'front.png':(64,64),'back.png':(64,320),'normal.png':(144,32),'surf_run.png':(224,32),'bike.png':(288,32),'vs_seeker_bike.png':(192,32),'fish.png':(384,32),'item.png':(288,32),'credits.png':(64,384),'region_icon.png':(16,16),'intro.png':(64,96)}
for person in ['nathan','katie']:
 for file,size in required.items():
  p=R/'graphics/yokai_characters'/person/file
  assert p.exists(),('Incomplete protagonist set; no active file changed',p)
  im=Image.open(p);assert im.size==size and im.mode=='P',(p,im.size,im.mode)
  assert set(im.get_flattened_data())-{0},('Blank asset',p)
 assert (R/f'graphics/yokai_characters/{person}/reflection.pal').exists()
 assert (R/f'graphics/yokai_characters/{person}/bridge_reflection.pal').exists()
for file,size in [('credits.png',(64,384)),('intro.png',(64,96))]:
 p=R/'graphics/yokai_characters/matt'/file;assert p.exists() and Image.open(p).size==size,('Complete rival appearances before activating protagonists',p)
old=(R/'src/data/object_events/object_event_graphics.h').read_text()
assert 'graphics/yokai_characters/nathan/normal.4bpp' not in old,'Already active: modify maintained sources rather than rerun installer'
def edit(path,fn):
 p=R/path;s=p.read_text();p.write_text(fn(s))
def remap(path,pairs):
 def run(s):
  for a,b in pairs:
   assert a in s,(path,a);s=s.replace(a,b)
  return s
 edit(path,run)
pairs=[]
for oldprefix,person in [('red','nathan'),('green','katie')]:
 for oldsuffix,new in [('normal','normal'),('surf_run','surf_run'),('bike','bike'),('vs_seeker_bike','vs_seeker_bike'),('fish','fish'),('item','item')]:
  pairs.append((f'graphics/object_events/pics/people/{oldprefix}_{oldsuffix}.4bpp',f'graphics/yokai_characters/{person}/{new}.4bpp'))
pairs += [('graphics/object_events/palettes/player.gbapal','graphics/yokai_characters/nathan/normal.gbapal'),('graphics/object_events/palettes/player_reflection.gbapal','graphics/yokai_characters/nathan/reflection.gbapal')]
remap('src/data/object_events/object_event_graphics.h',pairs)
edit('src/data/object_events/object_event_graphics.h',lambda s:s+'\nconst u16 gObjectEventPal_YokaiPlayerBridge[] = INCBIN_U16("graphics/yokai_characters/nathan/bridge_reflection.gbapal");\n')
pairs=[]
for old,person in [('red','nathan'),('leaf','katie')]:
 pairs += [(f'graphics/trainers/front_pics/{old}_front_pic.4bpp.lz',f'graphics/yokai_characters/{person}/front.4bpp.lz'),(f'graphics/trainers/back_pics/{old}_back_pic.4bpp',f'graphics/yokai_characters/{person}/back.4bpp'),(f'graphics/trainers/palettes/{old}.gbapal.lz',f'graphics/yokai_characters/{person}/normal.gbapal.lz'),(f'graphics/trainers/palettes/{old}_back_pic.gbapal.lz',f'graphics/yokai_characters/{person}/normal.gbapal.lz')]
remap('src/data/graphics/trainers.h',pairs)
remap('src/region_map.c',[(f'graphics/region_map/player_icon_{old}.{suffix}',f'graphics/yokai_characters/{person}/{new}.{suffix}') for old,person in [('red','nathan'),('leaf','katie')] for suffix,new in [('gbapal','normal'),('4bpp.lz','region_icon')]])
remap('src/oak_speech.c',[(f'graphics/oak_speech/{old}/{file}.{suffix}',f'graphics/yokai_characters/{person}/intro.{suffix}') for old,person in [('red','nathan'),('leaf','katie'),('rival','matt')] for file,suffix in [('pic','8bpp.lz'),('pal','gbapal')]])
remap('src/credits.c',[(f'graphics/credits/{old}.{suffix}',f'graphics/yokai_characters/{person}/{file}.{suffix}') for old,person in [('player_male','nathan'),('player_female','katie'),('rival','matt')] for suffix,file in [('gbapal','normal'),('4bpp.lz','credits')]])
# Item/field action frames grow to32x32 to keep actor scale with raised wrists.
def pics(s):
 for role in ['RedItem','GreenItem']:
  a=s.index('static const struct SpriteFrameImage sPicTable_'+role+'[] = {');b=s.index('\n};',a)+3
  s=s[:a]+s[a:b].replace(', 2, 4,',', 4, 4,')+s[b:]
 return s
edit('src/data/object_events/object_event_pic_tables.h',pics)
# Hardware mirroring corrects individual source orientations without redrawing art.
def animations(s):
 original=s
 for table,flips,label in [('sAnimTable_RedGreenNormal',{17},'KatieNormal'),('sAnimTable_Standard',{2,7},'KatieBike'),('sAnimTable_RedGreenFish',{0,1,2,3},'KatieFish')]:
  m=re.search(r'static const union AnimCmd \*const '+table+r'\[\] = \{.*?\n\};',original,re.S);assert m,table
  body=m[0];changed={}
  for symbol in set(re.findall(r'= (sAnim_\w+),',body)):
   pattern=r'static const union AnimCmd '+symbol+r'\[\] = \{.*?\n\};';a=re.search(pattern,original,re.S);assert a,symbol
   touched=[]
   def command(c):
    if int(c[1]) not in flips:return c[0]
    touched.append(int(c[1]));rest=c[2]
    if '.hFlip = TRUE' in rest:rest=rest.replace('.hFlip = TRUE','.hFlip = FALSE')
    elif '.hFlip = FALSE' in rest:rest=rest.replace('.hFlip = FALSE','.hFlip = TRUE')
    else:rest+=', .hFlip = TRUE'
    return 'ANIMCMD_FRAME('+c[1]+','+rest+')'
   value=re.sub(r'ANIMCMD_FRAME\((\d+),([^)]*)\)',command,a[0])
   if touched:
    new=symbol+'_'+label;changed[symbol]=new;s+='\n'+value.replace(symbol,new)+'\n'
  for a,b in changed.items():body=re.sub(r'\b'+a+r'\b',b,body)
  s+='\n'+body.replace(table,'sAnimTable_'+label)+'\n'
 return s
edit('src/data/object_events/object_event_anims.h',animations)
def info(s):
 def block(m):
  text=m[0];name=m[1]
  if not name.startswith(('Red','Green')):return text
  text=text.replace('OBJ_EVENT_PAL_TAG_BRIDGE_REFLECTION','OBJ_EVENT_PAL_TAG_YOKAI_PLAYER_BRIDGE')
  if re.search(r'\.images = sPicTable_(Red|Green)Item,',text):
   text=text.replace('.size = 256,','.size = 512,').replace('.width = 16,','.width = 32,').replace('gObjectEventBaseOam_16x32','gObjectEventBaseOam_32x32').replace('gObjectEventSpriteOamTables_16x32','gObjectEventSpriteOamTables_32x32')
  for role,table in [('GreenNormal','KatieNormal'),('GreenBike','KatieBike'),('GreenFish','KatieFish')]:
   if name==role:text=re.sub(r'\.anims = \w+,','.anims = sAnimTable_'+table+',',text)
  return text
 return re.sub(r'const struct ObjectEventGraphicsInfo gObjectEventGraphicsInfo_(\w+) = \{.*?\n\};',block,s,flags=re.S)
edit('src/data/object_events/object_event_graphics_info.h',info)
edit('src/event_object_movement.c',lambda s:s.replace('#define OBJ_EVENT_PAL_TAG_YOKAI_ENMA','#define OBJ_EVENT_PAL_TAG_YOKAI_PLAYER_BRIDGE          0x111F\n#define OBJ_EVENT_PAL_TAG_YOKAI_ENMA',1).replace('    {gObjectEventPal_YokaiEnma, OBJ_EVENT_PAL_TAG_YOKAI_ENMA},','    {gObjectEventPal_YokaiEnma, OBJ_EVENT_PAL_TAG_YOKAI_ENMA},\n    {gObjectEventPal_YokaiPlayerBridge, OBJ_EVENT_PAL_TAG_YOKAI_PLAYER_BRIDGE},'))
rules='\n# Original Yo-kai protagonists: preserve native per-frame tile order.\n'
for person in ['nathan','katie']:
 for file,width in [('normal',2),('surf_run',2),('bike',4),('vs_seeker_bike',4),('fish',4),('item',4),('back',8),('credits',8)]:
  rules+=f'graphics/yokai_characters/{person}/{file}.4bpp: %.4bpp: %.png\n\t$(GFX) $< $@ -mwidth {width} -mheight '+('8' if file in ['back','credits'] else '4')+'\n\n'
rules+='graphics/yokai_characters/matt/credits.4bpp: %.4bpp: %.png\n\t$(GFX) $< $@ -mwidth 8 -mheight 8\n'
edit('spritesheet_rules.mk',lambda s:s+rules)
p=R/'data/yokai/registre_identifiants.json';d=json.loads(p.read_text());d['palette_tags']['PROTAGONIST_BRIDGE_REFLECTION']='0x111F';p.write_text(json.dumps(d,indent=2)+'\n')
for person in ['nathan','katie']:
 p=R/f'graphics/yokai_characters/{person}/production.json';d=json.loads(p.read_text());d['integration_state']='ACTIVE — requires compile/native graphical validation';p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
print('Active protagonist resources updated. Compile and run native graphical tests before claiming completion.')
