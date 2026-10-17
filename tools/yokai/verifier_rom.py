#!/usr/bin/env python3
"""Vérifie les données réellement liées dans la ROM compilée, sans simuler mGBA."""
import csv
import hashlib
import json
import re
import struct
import subprocess
import zipfile
from pathlib import Path

R = Path(__file__).resolve().parents[2]
rom = (R/'pokefirered.gba').read_bytes()
symbols = {}
for line in subprocess.check_output(['arm-none-eabi-nm','-S','--defined-only','pokefirered.elf'],cwd=R,text=True).splitlines():
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
checks=0
with zipfile.ZipFile(R/'docs/yokai-gallery/sources/gba-graphics.zip') as archive:
    for entry in json.loads(archive.read('manifest.json'))['species']:
        n=entry['index'];constant=entry['constant']
        for kind,asset in entry['resources'].items():
            binary=data(asset['symbol'])
            raw=unlz(binary) if kind in ['front','back','normal','shiny'] else binary
            path=R/f'graphics/yokai/{n:03}'/ {'front':'front.4bpp','back':'back.4bpp','normal':'normal.gbapal','shiny':'shiny.gbapal','icon':'icon.4bpp','footprint':'footprint.1bpp'}[kind]
            assert raw==path.read_bytes(),(n,kind,'linked file mismatch')
            if n not in {17,22,41,71,84,86,100,112,114,117,124,128,133,149} or kind in ['icon','footprint']:
                assert raw==archive.read(asset['snapshot']),(n,kind,'snapshot roundtrip mismatch')
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
report={'rom_sha256':hashlib.sha256(rom).hexdigest(),'rom_size':len(rom),'species_stats_and_abilities_verified':151,'encoded_display_names_verified':151,'linked_graphic_resources_verified':checks,'historical_graphics_preserved_except_whitelist':True,'evolution_edges_verified':len(evolutions),'emulator_tests':False,'final_shiny_artwork_validated':False,'verdict':'JALON DONNEES/GRAPHISMES LIE ; RECETTE COMPLETE NON TERMINEE'}
out=R/'QA_RECETTE_FINALE/RECONSTRUCTION/CONTROLE_ROM.json';out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2))
