#!/usr/bin/env python3
"""Vérifie les données réellement liées dans la ROM compilée, sans simuler mGBA."""
import os
import csv
import hashlib
import json
import re
import struct
import subprocess
import zipfile
from pathlib import Path

R = Path(__file__).resolve().parents[2]
rom_path = Path(os.environ.get('YOKAI_VERIFY_ROM',str(R/'pokefirered.gba')))
elf_path = rom_path.with_suffix('.elf')
rom = rom_path.read_bytes()
symbols = {}
for line in subprocess.check_output(['arm-none-eabi-nm','-S','--defined-only',str(elf_path)],cwd=R,text=True).splitlines():
    fields = line.split()
    if len(fields) == 4:
        symbols[fields[3]] = (int(fields[0],16), int(fields[1],16))


def data(symbol):
    address, length = symbols[symbol]
    assert 0x08000000 <= address < 0x0A000000, symbol
    return rom[address-0x08000000:address-0x08000000+length]


def unlz(raw):
    assert raw[0] == 0x10
    length, cursor, result = int.from_bytes(raw[1:4],'little'), 4, bytearray()
    while len(result) < length:
        flags=raw[cursor];cursor+=1
        for bit in range(7,-1,-1):
            if len(result) >= length: break
            if flags & (1<<bit):
                a,b=raw[cursor:cursor+2];cursor+=2
                for _ in range((a>>4)+3):
                    result.append(result[-(((a&15)<<8|b)+1)])
                    if len(result)==length: break
            else: result.append(raw[cursor]);cursor+=1
    return bytes(result)


source=R/'RECUPERATION_PROJET/sources_validees'
stats=list(csv.DictReader((source/'02_STATS_TYPES_TALENTS.csv').open(encoding='utf-8-sig'),delimiter=';'))
names=json.loads((R/'data/yokai/noms_affiches.json').read_text())
count=len(data('gSpeciesNames'))//11
stride=len(data('gSpeciesInfo'))//count
constants={}
for p in ['species','abilities','pokemon','items']:
    for key,value in re.findall(r'^#define\s+(\w+)\s+(\d+)\s*(?:$|//)',(R/f'include/constants/{p}.h').read_text(),re.M):constants[key]=int(value)
glyphs={m[1]:int(m[2],16) for m in re.finditer(r"^'(.*?)'\s*= ([0-9A-F]{2})$",(R/'charmap.txt').read_text(),re.M)}
glyphs["'"]=glyphs['’']
for row,name in zip(stats,names):
    number=int(row['numero_yokai']);entry=data('gSpeciesInfo')[number*stride:(number+1)*stride]
    assert list(entry[:6])==[int(row[k]) for k in ['pv','attaque','defense','vitesse','attaque_speciale','defense_speciale']],number
    assert entry[22:24]==bytes([constants[row['ability_1']],constants.get(row['ability_2'],0)]),number
    expected=bytes(glyphs[c] for c in name['nom_affiche_gba'])+b'\xff'
    assert data('gSpeciesNames')[number*11:number*11+len(expected)]==expected,(number,name)
presentation={row['source']:row['target'] for row in json.loads((R/'data/yokai/sprite_presentation.json').read_text())['profiles']} if (R/'data/yokai/sprite_presentation.json').exists() else {}
checks=0
with zipfile.ZipFile(R/'docs/yokai-gallery/sources/gba-graphics.zip') as archive:
    for entry in json.loads(archive.read('manifest.json'))['species']:
        n=entry['index'];constant=entry['constant']
        for kind,asset in entry['resources'].items():
            binary=data(asset['symbol'])
            raw=unlz(binary) if kind in ['front','back','normal','shiny'] else binary
            path=R/f'graphics/yokai/{n:03}'/ {'front':'front.4bpp','back':'back.4bpp','normal':'normal.gbapal','shiny':'shiny.gbapal','icon':'icon.4bpp','footprint':'footprint.1bpp'}[kind]
            displayed=R/presentation.get(str(path.relative_to(R)),str(path.relative_to(R)))
            assert raw==displayed.read_bytes(),(n,kind,'linked file mismatch')
            if n not in {17,22,41,71,84,86,100,112,114,117,124,128,133,149} or kind in ['icon','footprint']:
                assert path.read_bytes()==archive.read(asset['snapshot']),(n,kind,'source snapshot roundtrip mismatch')
            if kind in ['front','back']:
                table=data('gMonFrontPicTable' if kind=='front' else 'gMonBackPicTable')
                pointer=struct.unpack_from('<I',table,n*8)[0]
                assert pointer==symbols[asset['symbol']][0],(n,kind,'inactive sprite')
            checks+=1
assert checks==906
evolutions=list(csv.DictReader((source/'03_EVOLUTIONS.csv').open(encoding='utf-8-sig'),delimiter=';'))
evo_stride=len(data('gEvolutionTable'))//count//5
for row in evolutions:
    start=int(row['no_depart']);end=int(row['no_arrivee'])
    method={'NIVEAU':4,'PIERRE':7,'BONHEUR_ET_OBJET':16}[row['methode']]
    param=int(row['niveau']) if method==4 else constants[row['item_evolution'] if method==7 else row['item_tenu']]
    entries=[struct.unpack_from('<HHH',data('gEvolutionTable'),(start*5+i)*evo_stride) for i in range(5)]
    assert (method,param,end) in entries,row
# Check actual learned-move arrays and French labels, independent of C compilation success.
constants.update({k:int(v) for k,v in re.findall(r'^#define\s+(MOVE_\w+)\s+(\d+)\s*$',(R/'include/constants/moves.h').read_text(),re.M)})
move_rows=list(csv.DictReader((R/'data/yokai/attaques_validees.csv').open(),delimiter=';'))
for number in range(1,152):
    expected=[];delayed=[]
    for row in move_rows:
        if int(row['numero_yokai'])!=number:continue
        if row['apprentissage']=='EVOLUTION_PLUS_2':delayed.append((101<<9)|constants[row['move_id']])
        else:expected.append((int(row['niveau'])<<9)|constants[row['move_id']])
    expected+=delayed+[0xFFFF]
    assert data(f'sYokai{number:03}LevelUpLearnset')==struct.pack('<'+'H'*len(expected),*expected),(number,'linked learnset')
for label in json.loads((R/'data/yokai/libelles_attaques_talents.json').read_text()):
    index=int(label['id']);symbol='gMoveNames' if label['constant'].startswith('MOVE_') else 'gAbilityNames'
    expected=bytes(glyphs[c] for c in label['display'])+b'\xff'
    assert data(symbol)[index*13:index*13+len(expected)]==expected,(symbol,index,label)
# Matt uses per-frame 16x32 tile ordering; a whole-image conversion corrupts sprites.
matt=R/'graphics/yokai_characters/matt'
if matt.exists():
    from PIL import Image
    def encode4(im):
        output=bytearray()
        for ty in range(0,im.height,8):
            for tx in range(0,im.width,8):
                for y in range(8):
                    for x in range(0,8,2):output.append(im.getpixel((tx+x,ty+y))|(im.getpixel((tx+x+1,ty+y))<<4))
        return bytes(output)
    im=Image.open(matt/'overworld.png')
    assert im.size==(144,32) and im.mode=='P'
    assert data('gObjectEventPic_Blue')==b''.join(encode4(im.crop((i*16,0,i*16+16,32))) for i in range(9))
    for role,suffix in [('early','RivalEarly'),('late','RivalLate'),('champion','ChampionRival')]:
        im=Image.open(matt/f'battle_{role}.png');assert im.size==(64,64)
        assert unlz(data('gTrainerFrontPic_'+suffix))==encode4(im)
        assert unlz(data('gTrainerPalette_'+suffix))==(matt/'normal.gbapal').read_bytes()
    assert data('gObjectEventPal_Matt')==(matt/'normal.gbapal').read_bytes()
ariane=R/'graphics/yokai_characters/ariane'
if ariane.exists():
    im=Image.open(ariane/'battle.png');assert im.size==(64,64)
    assert unlz(data('gTrainerFrontPic_Ariane'))==encode4(im)
    assert unlz(data('gTrainerPalette_Ariane'))==(ariane/'normal.gbapal').read_bytes()
    im=Image.open(ariane/'overworld.png');assert im.size==(48,32)
    assert data('gObjectEventPic_Ariane')==b''.join(encode4(im.crop((i*16,0,i*16+16,32))) for i in range(3))
    im=Image.open(ariane/'usapion_overworld.png');assert im.size==(32,32)
    assert data('gObjectEventPic_UsapionCameo')==(R/presentation['graphics/yokai_characters/ariane/usapion_overworld.4bpp']).read_bytes() if 'graphics/yokai_characters/ariane/usapion_overworld.4bpp' in presentation else data('gObjectEventPic_UsapionCameo')==encode4(im)
    assert data('gObjectEventPal_Ariane')==(ariane/'normal.gbapal').read_bytes()
enma=R/'graphics/yokai_characters/enma'
if enma.exists():
    im=Image.open(enma/'battle.png');assert im.size==(64,64) and im.mode=='P'
    assert unlz(data('gTrainerFrontPic_YokaiEnma'))==encode4(im)
    assert unlz(data('gTrainerPalette_YokaiEnma'))==(enma/'normal.gbapal').read_bytes()
    im=Image.open(enma/'overworld.png');assert im.size==(48,32)
    assert data('gObjectEventPic_YokaiEnma')==b''.join(encode4(im.crop((i*16,0,i*16+16,32))) for i in range(3))
    im=Image.open(enma/'kyubi_overworld.png');assert im.size==(32,32)
    assert data('gObjectEventPic_YokaiKyubi')==encode4(im)
    assert data('gObjectEventPal_YokaiEnma')==(enma/'normal.gbapal').read_bytes()
enma_creature=R/'graphics/yokai_characters/enma_creature'
if enma_creature.exists():
    im=Image.open(enma_creature/'overworld.png');assert im.size==(32,32) and im.mode=='P' and im.info.get('transparency')==0
    assert data('gObjectEventPic_YokaiEnmaCreature')==encode4(im)
    assert data('gObjectEventPal_YokaiEnmaCreature')==(enma_creature/'normal.gbapal').read_bytes()
    assert '"OBJ_EVENT_GFX_YOKAI_ENMA_CREATURE"' in (R/'data/maps/CeruleanCave_B1F/map.json').read_text()
    assert '"OBJ_EVENT_GFX_YOKAI_ENMA"' in (R/'data/maps/MtEmber_Summit/map.json').read_text()
protagonists_active='graphics/yokai_characters/nathan/normal.4bpp' in (R/'src/data/object_events/object_event_graphics.h').read_text()
def encode8(im):
    return bytes(im.getpixel((tx+x,ty+y)) for ty in range(0,im.height,8) for tx in range(0,im.width,8) for y in range(8) for x in range(8))
if protagonists_active:
    for person,prefix,trainer,role in [('nathan','Red','Red','Male'),('katie','Green','Leaf','Female')]:
        root=R/'graphics/yokai_characters'/person
        for file,suffix,width in [('normal','Normal',16),('surf_run','SurfRun',16),('bike','Bike',32),('vs_seeker_bike','VSSeekerBike',32),('item','Item',32),('fish','Fish',32)]:
            im=Image.open(root/(file+'.png'));assert im.mode=='P' and im.height==32
            assert data('gObjectEventPic_'+prefix+suffix)==b''.join(encode4(im.crop((x,0,x+width,32))) for x in range(0,im.width,width)),(person,file,'frame tile order')
        assert unlz(data('gTrainerFrontPic_'+trainer))==encode4(Image.open(root/'front.png'))
        assert data('gTrainerBackPic_'+trainer)==encode4(Image.open(root/'back.png'))
        assert unlz(data('gTrainerPalette_'+trainer))==(root/'normal.gbapal').read_bytes()
        assert unlz(data('gTrainerPalette_'+trainer+'BackPic'))==(root/'normal.gbapal').read_bytes()
        assert unlz(data('sPlayerIcon_'+trainer))==encode4(Image.open(root/'region_icon.png'))
        assert data('sPlayerIcon_'+trainer+'Pal')==(root/'normal.gbapal').read_bytes()
        assert unlz(data('sOakSpeech_'+trainer+'_Tiles'))==encode8(Image.open(root/'intro.png'))
        assert data('sOakSpeech_'+trainer+'_Pal')==(root/'intro.gbapal').read_bytes()
        assert unlz(data('sPlayer'+role+'_Tiles'))==encode4(Image.open(root/'credits.png'))
        assert data('sPlayer'+role+'_Pal')==(root/'normal.gbapal').read_bytes()
    assert data('gObjectEventPal_Player')==(R/'graphics/yokai_characters/nathan/normal.gbapal').read_bytes()
    assert data('gObjectEventPal_PlayerReflection')==(R/'graphics/yokai_characters/nathan/reflection.gbapal').read_bytes()
    assert data('gObjectEventPal_YokaiPlayerBridge')==(R/'graphics/yokai_characters/nathan/bridge_reflection.gbapal').read_bytes()
    assert unlz(data('sOakSpeech_Rival_Tiles'))==encode8(Image.open(matt/'intro.png'))
    assert data('sOakSpeech_Rival_Pal')==(matt/'intro.gbapal').read_bytes()
    assert unlz(data('sRival_Tiles'))==encode4(Image.open(matt/'credits.png'))
cameo_extra_frames=0
for person in ['Nathaniel','Michael','Wyatt']:
    root=R/'graphics/yokai_characters'/person.lower()
    if not root.exists() or 'gTrainerFrontPic_Yokai'+person not in symbols:continue
    im=Image.open(root/'battle.png');ow=Image.open(root/'overworld.png')
    assert im.mode==ow.mode=='P' and im.size==(64,64) and ow.size==(48,32)
    assert im.info.get('transparency')==ow.info.get('transparency')==0
    assert max(im.get_flattened_data())<=15 and max(ow.get_flattened_data())<=15
    assert unlz(data('gTrainerFrontPic_Yokai'+person))==encode4(im)
    assert unlz(data('gTrainerPalette_Yokai'+person))==(root/'normal.gbapal').read_bytes()
    assert data('gObjectEventPal_Yokai'+person)==(root/'normal.gbapal').read_bytes()
    assert data('gObjectEventPic_Yokai'+person)==b''.join(encode4(ow.crop((x,0,x+16,32))) for x in range(0,48,16))
    cameo_extra_frames+=4
boss_cameo_frames=0
boss_spec=R/'data/yokai/cameos_boss.json'
if boss_spec.exists():
    for entry in json.loads(boss_spec.read_text())['graphics']:
        root=R/'graphics/yokai_characters'/entry['folder'];person=entry['person'];width=entry['ow_width']
        im=Image.open(root/'battle.png');ow=Image.open(root/'overworld.png')
        assert im.mode==ow.mode=='P' and im.size==(64,64) and ow.size==(width*3,32)
        assert im.info.get('transparency')==ow.info.get('transparency')==0
        assert max(im.get_flattened_data())<=15 and max(ow.get_flattened_data())<=15
        assert unlz(data('gTrainerFrontPic_Yokai'+person))==encode4(im)
        assert unlz(data('gTrainerPalette_Yokai'+person))==(root/'normal.gbapal').read_bytes()
        group='Domniscian' if entry['palette_group']=='DOMNISCIAN' else 'DonMorleone'
        assert data('gObjectEventPal_Yokai'+group+'Group')==(root/'normal.gbapal').read_bytes()
        assert data('gObjectEventPic_Yokai'+person)==b''.join(encode4(ow.crop((x,0,x+width,32))) for x in range(0,width*3,width))
        boss_cameo_frames+=4
report={'rom_sha256':hashlib.sha256(rom).hexdigest(),'rom_size':len(rom),'species_stats_and_abilities_verified':151,'encoded_display_names_verified':151,'linked_graphic_resources_verified':checks,'canonical_battle_artwork_preserved_except_whitelist':True,'presentation_overrides_verified':len(presentation),'evolution_edges_verified':len(evolutions),'linked_learnsets_verified':151,'french_move_and_ability_labels_verified':len(json.loads((R/'data/yokai/libelles_attaques_talents.json').read_text())),'matt_native_frames_verified':12 if matt.exists() else 0,'ariane_and_usapion_native_frames_verified':5 if ariane.exists() else 0,'enma_and_kyubi_native_frames_verified':5 if enma.exists() else 0,'distinct_enma_creature_frame_verified':1 if enma_creature.exists() else 0,'protagonist_native_frame_slots_verified':146 if protagonists_active else 0,'matt_additional_intro_and_credit_frames_verified':7 if protagonists_active else 0,'additional_adventure_cameo_native_frames_verified':cameo_extra_frames,'postgame_boss_cameo_native_frames_verified':boss_cameo_frames,'emulator_tests':False,'final_shiny_artwork_validated':False,'verdict':'JALON DONNEES/GRAPHISMES LIE ; RECETTE COMPLETE NON TERMINEE'}
out=Path(os.environ['YOKAI_VERIFY_REPORT']) if os.environ.get('YOKAI_VERIFY_REPORT') else R/('QA_RECETTE_FINALE/INTEGRATION_MUSIQUES/CONTROLE_ROM_PRIVEE.json' if os.environ.get('YOKAI_VERIFY_ROM') else 'QA_RECETTE_FINALE/RECONSTRUCTION/CONTROLE_ROM.json');out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2))
