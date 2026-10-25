#!/usr/bin/env python3
"""Assemble trois captures continues et un extrait de vraie victoire, sans accélérer."""
import concurrent.futures,hashlib,json,subprocess,tempfile
from pathlib import Path
from mgba_rpc import ROOT
P=ROOT/'docs/terre-heure-regard-oni-20261025';P.mkdir(exist_ok=True)
work=Path(tempfile.mkdtemp(prefix='trois-oni-montage-'))
specs=[('GARGAROS','Gargaros - Mont Sélénite','gargaros'),('OGRALOS','Ogralos - Grotte Sombre','ogralos'),('ORQANOS','Orqanos - Îles Écume','orqanos'),('VICTOIRE','Bonus - Fondu après une victoire','victoire')]
rom_sha=hashlib.sha256((ROOT/'pokefirered_audio.gba').read_bytes()).hexdigest()
def duration(path):return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(path)],text=True))
def encode(spec):
 key,label,name=spec;source=Path('/tmp/terre-livree-'+name);meta=json.loads((source/'ENREGISTREMENT_SORTIE.json').read_text());assert meta['rom_sha256']==rom_sha
 args=['ffmpeg','-v','error','-y']
 if name=='victoire':args+=['-ss',str(meta['evenements_secondes']['victoire_oni']-3)]
 else:
  assert meta['objectif_fuite_sans_combat'] and 'combat_oni' not in meta['evenements_secondes']
  assert meta['evenements_secondes']['interaction_porte']-meta['evenements_secondes']['exploration']<360
 args+=['-i',str(source/meta['video'])]
 if name=='victoire':args+=['-t','15']
 target=work/(key+'.mp4');args+=['-vf',f"pad=iw:ih+32:0:32:color=black,drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:text='{label}':x=12:y=7:fontsize=18:fontcolor=white",'-c:v','libx264','-preset','fast','-crf','22','-threads','2','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-ar','48000',str(target)]
 subprocess.run(args,check=True)
 (P/(key+'.json')).write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n')
 return target,duration(target),label
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:segments=list(pool.map(encode,specs))
listing=work/'concat.txt';listing.write_text(''.join("file '"+str(path)+"'\n" for path,_,_ in segments))
chapters=[';FFMETADATA1'];cursor=0;timeline=[]
for path,seconds,label in segments:
 end=cursor+seconds;chapters+=['[CHAPTER]','TIMEBASE=1/1000',f'START={round(cursor*1000)}',f'END={round(end*1000)}','title='+label];timeline.append({'titre':label,'debut_secondes':cursor,'duree_secondes':seconds});cursor=end
chapter_file=work/'chapters.txt';chapter_file.write_text('\n'.join(chapters)+'\n')
output=P/'trois-oni-trois-grottes-mgba.mp4'
subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',str(listing),'-i',str(chapter_file),'-map_metadata','1','-map_chapters','1','-c','copy','-movflags','+faststart',str(output)],check=True)
assert output.stat().st_size<100*1024**2
(P/'VIDEO.json').write_text(json.dumps({'rom_sha256':rom_sha,'video':output.name,'video_sha256':hashlib.sha256(output.read_bytes()).hexdigest(),'taille_octets':output.stat().st_size,'duree_secondes':duration(output),'chapitres':timeline,'montage':'Trois prises continues, séparées par un changement de scénario; aucune coupe interne et aucune accélération. Bonus: extrait de 15 secondes autour d’une victoire réelle. Bandeau ajouté au-dessus de l’image du jeu, sans cacher le chrono.','preparation':'Situations, stades Oni, équipe et visite favorable préparés avant chaque capture. Aucun changement RAM, warp ou résultat de combat injecté ensuite. Les déplacements sont pilotés à la manette par un algorithme qui connaît les cartes et la destination de la porte.'},ensure_ascii=False,indent=2)+'\n')
print(output,output.stat().st_size,duration(output))
