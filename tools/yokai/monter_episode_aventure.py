#!/usr/bin/env python3
"""Montage ×5/×1 d’un épisode natif, avec chapitres et son à hauteur préservée.
Tous les instants importants et leurs marges de deux secondes restent à ×1.
"""
import json,math,subprocess,sys,wave
from pathlib import Path
part=Path(sys.argv[1]);dest=Path(sys.argv[2]);dest.parent.mkdir(parents=True,exist_ok=True)
m=json.loads((part/'ENREGISTREMENT.json').read_text());fps=m['fps'];total=m['frames'];events=m['speed_events'];normal=[]
for i,e in enumerate(events):
 end=events[i+1]['frame'] if i+1<len(events) else total
 if e['speed']==1:normal.append((max(0,e['frame']-round(2*fps)),min(total,end+round(2*fps))))
merged=[]
for a,b in normal:
 if merged and a<=merged[-1][1]+round(.5*fps):merged[-1]=(merged[-1][0],max(b,merged[-1][1]))
 else:merged.append((a,b))
segments=[];cursor=0
for a,b in merged:
 if a>cursor:segments.append((cursor,a,5))
 segments.append((a,b,1));cursor=b
if cursor<total:segments.append((cursor,total,5))
work=part/'montage';work.mkdir(exist_ok=True);out_frames=0;results=[];pcm=wave.open(str(work/'audio-final.wav'),'wb');pcm.setparams((2,2,48000,0,'NONE','not compressed'))
for index,(a,b,speed) in enumerate(segments):
 nframes=max(1,round((b-a)/speed));duration=nframes/fps;stem=work/f'{index:03}';log=stem.with_suffix('.log').open('wb')
 af='anull' if speed==1 else 'atempo=2,atempo=2,atempo=1.25'
 # Accurate decode after seeking; encode each interval separately to avoid a large split-filter buffer.
 subprocess.run(['ffmpeg','-y','-ss',str(a/fps),'-t',str((b-a)/fps),'-i',str(part/'video-native.mp4'),'-an','-vf',f'setpts=(PTS-STARTPTS)/{speed},fps={fps},scale=720:480:flags=neighbor','-frames:v',str(nframes),'-c:v','libx264','-preset','fast','-crf','21','-pix_fmt','yuv420p',str(stem.with_suffix('.mp4'))],stdout=subprocess.DEVNULL,stderr=log,check=True)
 samples=round(duration*48000)
 subprocess.run(['ffmpeg','-y','-ss',str(a/fps),'-t',str((b-a)/fps),'-i',str(part/'audio-natif.wav'),'-vn','-af',af+f',aresample=48000,apad,atrim=end_sample={samples}','-c:a','pcm_s16le',str(stem.with_suffix('.wav'))],stdout=subprocess.DEVNULL,stderr=log,check=True);log.close()
 with wave.open(str(stem.with_suffix('.wav')),'rb') as wav:pcm.writeframes(wav.readframes(wav.getnframes()))
 results.append({'source_start':a,'source_end':b,'speed':speed,'output_start_frame':out_frames,'output_frames':nframes});out_frames+=nframes;print('SEGMENT',index,a,b,speed,flush=True)
pcm.close();listing=work/'concat.txt';listing.write_text(''.join("file '"+str((work/f'{i:03}.mp4').resolve())+"'\n" for i in range(len(segments))))
subprocess.run(['ffmpeg','-y','-f','concat','-safe','0','-i',str(listing),'-i',str(work/'audio-final.wav'),'-c:v','copy','-c:a','aac','-b:a','160k','-ar','48000','-movflags','+faststart',str(dest)],stdout=subprocess.DEVNULL,stderr=(work/'mux.log').open('wb'),check=True)
def output_time(frame):
 for s in results:
  if frame<=s['source_end']:return (s['output_start_frame']+(max(frame,s['source_start'])-s['source_start'])/s['speed'])/fps
 return out_frames/fps
chapters=[{'seconds':output_time(e['frame']),'title':e['title']} for e in m['chapters']]
report={'rom_sha256':m['rom_sha256'],'rom_commit':m['rom_commit'],'source_frames':total,'source_seconds':total/fps,'output_seconds':out_frames/fps,'only_speed_changes_no_story_cuts':True,'ordinary_speed':5,'important_speed':1,'normal_speed_margin_seconds':2,'pitch_preserved_in_accelerated_sections':True,'intervals':results,'chapters':chapters,'file':dest.name}
dest.with_suffix('.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
text=['# '+m['title'],'','Mode Normal, nouvelle partie native mGBA. ×5 pendant les passages ordinaires ; moments importants à vitesse normale. Aucun Pokémon, objet, drapeau ou résultat de combat injecté.','']
for c in chapters:
 seconds=round(c['seconds']);text.append(f"- {seconds//60:02}:{seconds%60:02} — {c['title']}")
dest.with_suffix('.md').write_text('\n'.join(text)+'\n');print('PASS montage',dest,dest.stat().st_size,flush=True)
