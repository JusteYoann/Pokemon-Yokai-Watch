#!/usr/bin/env python3
"""Static musical call-site audit with linked song/header verification."""
from pathlib import Path
import csv,json,re,subprocess,struct,collections
R=Path(__file__).resolve().parents[3];D=R/'docs/musique-audit'
def table(name,rows):
 with (D/name).open('w',encoding='utf-8-sig',newline='') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter=';',lineterminator='\n');w.writeheader();w.writerows(rows)
constants={m[1]:int(m[2]) for m in re.finditer(r'^#define\s+(MUS_\w+)\s+(\d+)\b',(R/'include/constants/songs.h').read_text(),re.M)}
sym={}
for line in subprocess.check_output(['arm-none-eabi-nm','-S','--defined-only',str(R/'pokefirered.elf')],text=True).splitlines():
 a=line.split()
 if len(a)==4:sym[a[3]]=(int(a[0],16),int(a[1],16))
 elif len(a)==3:sym[a[2]]=(int(a[0],16),0)
rom=(R/'pokefirered.gba').read_bytes();songs=re.findall(r'^\s*song\s+(\w+),\s*(\d+),\s*(\d+)',(R/'sound/song_table.inc').read_text(),re.M);assert len(songs)==347
refs=collections.defaultdict(list);maps=[]
for p in sorted((R/'data/maps').glob('*/map.json')):
 obj=json.loads(p.read_text());maps.append({'map':obj['name'],'id':obj['id'],'music':obj['music'],'linked_header':obj['name'] in sym,'file':str(p.relative_to(R))});refs[obj['music']].append(f"{p.relative_to(R)}:music")
triggers=[]
for root in [R/'src',R/'data']:
 for p in sorted(root.rglob('*')):
  if not p.is_file() or p.suffix not in ['.c','.h','.inc','.s']:continue
  label=''
  for n,line in enumerate(p.read_text(errors='replace').splitlines(),1):
   m=re.match(r'^(\w+)::',line)
   if m:label=m[1]
   code=line.split('//',1)[0].split('@',1)[0]
   for name in set(re.findall(r'\bMUS_\w+\b',code)):
    if name in constants:
     ref=f'{p.relative_to(R)}:{n}';refs[name].append(ref);triggers.append({'music':name,'file':str(p.relative_to(R)),'line':n,'label':label,'code':line.strip()})
rows=[]
for name,value in sorted(constants.items(),key=lambda x:x[1]):
 if name=='MUS_DUMMY':continue
 song,player,spare=songs[value];pointer=struct.unpack_from('<I',rom,sym['gSongTable'][0]-0x08000000+value*8)[0];assert pointer==sym[song][0],name
 offset=pointer-0x08000000;tracks,blocks,priority,reverb=rom[offset:offset+4];bank=struct.unpack_from('<I',rom,offset+4)[0];banks=[n for n,(addr,_) in sym.items() if addr==bank and n.startswith('voicegroup')];path=R/'sound/songs/midi'/(song+'.s')
 if not path.exists():path=R/'sound/songs'/(song+'.s')
 content=path.read_text() if path.exists() else '';tempo=re.findall(r'TEMPO\s*,\s*([^\n]+)',content)
 rows.append({'music_id':value,'constante':name,'morceau_pokemon_original':song,'maps_utilisatrices':' | '.join(m['map'] for m in maps if m['music']==name),'sources_declencheurs':' | '.join(sorted(set(refs[name]))),'role':'jingle/transition, conserver durée et reprise' if value<=271 or name in ['MUS_OBTAIN_KEY_ITEM','MUS_CAUGHT','MUS_CAUGHT_INTRO','MUS_DEX_RATING','MUS_PHOTO','MUS_POKE_FLUTE'] else 'combat' if '_VS_' in name else 'rencontre brève' if 'ENCOUNTER' in name or name=='MUS_RIVAL_EXIT' else 'exploration/interface/événement','contrainte':f'Lecteur {player}; {tracks} pistes séquencées; priorité {priority}; banque '+','.join(banks),'boucle_source':'GOTO présent, borne musicale à contrôler' if re.search(r'\bGOTO\b',content) else 'Pas de GOTO détecté dans la source consultée','tempo_source':' | '.join(dict.fromkeys(tempo)),'source_sequence':str(path.relative_to(R)) if path.exists() else 'non trouvée','preuve_liaison_rom':'gSongTable pointe vers '+song,'utilisation_statut':'Référence source trouvée' if refs[name] else 'Défini et lié, pas de référence MUS explicite retrouvée'})
table('EMPLACEMENTS_MUSICAUX_KANTO.csv',rows);table('DECLENCHEURS_AUDIO.csv',triggers);table('MUSIQUES_PAR_CARTE.csv',maps)
# Specific existing hack contexts inherit native routing, not custom audio.
trainers=(R/'src/data/trainers.h').read_text();parties=[]
actors=[]
for p in sorted((R/'data/maps').glob('*/map.json')):
 obj=json.loads(p.read_text())
 for event in obj.get('object_events',[]):
  script=event.get('script','')
  if script.startswith('Cameo_'):actors.append({'actor':script[6:].replace('_','').upper(),'map':obj['name'],'map_music':obj['music'],'object_script':script})
for m in re.finditer(r'\[(TRAINER_CAMEO_\w+)\]\s*=\s*\{(.*?)\n\s*\},',trainers,re.S):
 cls=re.search(r'\.trainerClass\s*=\s*(\w+)',m[2])[1];song='MUS_VS_CHAMPION' if cls=='TRAINER_CLASS_CHAMPION' else 'MUS_VS_GYM_LEADER' if cls in ['TRAINER_CLASS_LEADER','TRAINER_CLASS_ELITE_FOUR'] else 'MUS_VS_TRAINER';key=m[1].removeprefix('TRAINER_CAMEO_').removesuffix('_ADV').removesuffix('_POST').replace('_','');owner=[e for e in actors if e['actor']==key];assert owner,m[1]
 parties.append({'trainer':m[1],'class':cls,'current_music':song,'map':' | '.join(e['map'] for e in owner),'map_music':' | '.join(e['map_music'] for e in owner),'object_script':' | '.join(e['object_script'] for e in owner),'routing':'src/pokemon.c:GetBattleBGM','explicit_cameo_bgm':'Non : trainerbattle_no_intro, pas de playbgm dédié'})
table('CAMEOS_AUDIO.csv',parties)
(D/'preuves/INVENTAIRE_JEU.json').write_text(json.dumps({'music_definitions':len(rows),'map_headers':len(maps),'linked_map_headers':sum(m['linked_header'] for m in maps),'explicit_music_reference_lines':len(triggers),'cameo_parties':len(parties),'rom_sha256':__import__('hashlib').sha256(rom).hexdigest(),'scope':'Static source and linked ROM table audit, not an audio playback or all event execution. MUS_NONE sentinel excluded; sound effects remain separate.'},indent=2)+'\n');print('GAME INVENTORY',len(rows),'songs',len(maps),'map headers',len(triggers),'references',len(parties),'cameo parties')
