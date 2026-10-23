from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,struct,hashlib
R=Path(__file__).resolve().parents[4];D=R/'graphics/alyzon_bie/reprise-red';Q=R/'docs/lavanville-zombie-night/phase-1/prototypes/alyzon-reprise-red';D.mkdir(parents=True,exist_ok=True);Q.mkdir(parents=True,exist_ok=True)
pal={'.':(0,0,0),'K':(32,24,32),'O':(112,88,40),'H':(184,144,48),'Y':(224,192,80),'L':(248,224,128),'S':(240,192,152),'s':(192,136,104),'E':(32,152,168),'W':(248,248,232),'w':(184,184,192),'P':(120,64,144),'p':(80,32,96),'B':(40,64,88),'b':(24,40,56),'M':(128,144,152)}
face=[
'....OOOOOO....',
'...OHLLLLHO...',
'..OHLLLLYYHO..',
'.OHLLHLYYYYHO.',
'.OLLLLLHYYYHO.',
'OHLHLLLLHYYYHO',
'OHLLLLHHLYYYHO',
'.OHLLHHSHYYHO.',
'.OHLLHSSKHYHO.',
'.OHYHSSSEHYHO.',
'OHYOKSSSSKOYHO',
'OYKwWPPWwWKYO.',
'.KSWwPPwWSsK..',
'.KSwWBBWWsSK..',
'..KwWMMWWwK...',
'..KwWBBWWwK...',
'..KWWKKWWWK...',
'...KK....KK...',
'...KK....KK...']
back=[
'....OOOOOO....',
'...OHLLLLHO...',
'..OHLLLLYYHO..',
'.OHLLLLYYYYHO.',
'.OLLLHLYYYYHO.',
'OHLHLLLLHYYYHO',
'OHLLHLLYHYYYHO',
'.OHLYHLYHYYHO.',
'.OHLYHYYHYYHO.',
'.OHYHHYYHHYHO.',
'OHYOHHYYHHOYHO',
'OYKwWWWWwWKYO.',
'.KSWwWWwWSsK..',
'.KSwWWWWWsSK..',
'..KwWWwWWwK...',
'..KwWWwWWwK...',
'..KWWKKWWWK...',
'...KK....KK...',
'...KK....KK...']
left=[
'....OOOOO.....',
'...OHLLLHO....',
'..OHLLLLYHO...',
'.OHLLLLYYHO...',
'.OHLLHLYYYHO..',
'.OHLLHLYYYHO..',
'..OHLLHYYYHO..',
'...OHLHYYYHO..',
'...OHHHYYYHO..',
'...OHSHYYHYO..',
'..OKSSKOYHYHO.',
'...KwPWWKYYHO.',
'...KWSSWWKO...',
'...KwSsWWK....',
'...KwBBWWK....',
'...KwBBWWK....',
'...KWWKWWK....',
'...KK...KK....',
'...KK...KK....']
right=[list(r[::-1]) for r in left]
for y,changes in {7:{8:'S',9:'K',10:'S'},8:{8:'S',9:'E',10:'S'},9:{8:'S',9:'S',10:'S'}}.items():
 for x,c in changes.items():right[y][x]=c
right=[''.join(r) for r in right]
base={'face':face,'dos':back,'gauche':left,'droite':right};keys=list(pal);flat=sum((list(v) for v in pal.values()),[])+[0]*(768-48);frames={};records=[]
for d,rows in base.items():
 assert len(rows)==19
 assert all(len(row)==14 for row in rows),(d,[(i,len(row),row) for i,row in enumerate(rows) if len(row)!=14])
 frames[d]=[]
 for phase in range(3):
  mat=[list(row) for row in rows]
  if phase:
   # Same head clusters; Red's native walk bob is applied by the frame origin.
   if d in ['face','dos']:
    for y in [17,18]:mat[y]=list('.'*14)
    for y in [17,18]:
     for x in ([2,3] if phase==1 else [4,5]):mat[y-(1 if phase==1 else 0)][x]='K'
     for x in ([8,9] if phase==1 else [10,11]):mat[y-(1 if phase==2 else 0)][x]='K'
    # A small alternating cuff shadow accompanies the step.
    mat[12][2]='s' if phase==1 else 'S';mat[12][10]='S' if phase==1 else 's'
   else:
    for y in [17,18]:mat[y]=list('.'*14)
    foots=[(2,3),(8,9)] if d=='gauche' else [(4,5),(10,11)]
    for leg,positions in enumerate(foots):
     for y in [17,18]:
      for x in positions:mat[y-(1 if (leg==0)==(phase==1) else 0)][x]='K'
  f=Image.new('P',(16,32));f.putpalette(flat);f.info['transparency']=0;oy=12 if phase==0 else 13
  for y,row in enumerate(mat):
   for x,c in enumerate(row):f.putpixel((1+x,oy+y),keys.index(c))
  frames[d].append(f);pose=['repos','pas-1','pas-2'][phase];f.save(D/f'{d}-{pose}.png',transparency=0);bbox=f.convert('RGBA').getbbox();records.append(dict(direction=d,pose=pose,bbox=bbox,height=bbox[3]-bbox[1],width=bbox[2]-bbox[0],origin_y=oy))
  assert f.crop((1,oy,15,oy+11)).tobytes()==bytes(keys.index(c) for row in rows[:11] for c in row)
# Native FRLG standard nine frames; right is separate because hair is asymmetric.
order=[('face',0),('dos',0),('gauche',0),('face',1),('face',2),('dos',1),('dos',2),('gauche',1),('gauche',2)]
sheet=Image.new('P',(144,32));sheet.putpalette(flat);sheet.info['transparency']=0;raw=bytearray()
for i,(d,p) in enumerate(order):
 f=frames[d][p];sheet.paste(f,(16*i,0))
 for ty in range(4):
  for tx in range(2):
   for y in range(8):
    for x in range(0,8,2):raw.append(f.getpixel((tx*8+x,ty*8+y))|f.getpixel((tx*8+x+1,ty*8+y))<<4)
sheet.save(D/'overworld.png',transparency=0);(D/'overworld.4bpp').write_bytes(raw);(D/'overworld.gbapal').write_bytes(b''.join(struct.pack('<H',(r//8)|((g//8)<<5)|((b//8)<<10)) for r,g,b in pal.values()))
allposes=Image.new('P',(48,128));allposes.putpalette(flat);allposes.info['transparency']=0
for j,d in enumerate(frames):
 for i,f in enumerate(frames[d]):allposes.paste(f,(16*i,32*j))
allposes.save(D/'douze-poses.png',transparency=0)
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',16);board=Image.new('RGB',(720,900),(232,232,240));dr=ImageDraw.Draw(board)
for i,t in enumerate(['REPOS','PAS 1','PAS 2']):dr.text((180+175*i,8),t,font=font,fill='black')
for j,(d,fs) in enumerate(frames.items()):
 dr.text((10,145+210*j),d.upper(),font=font,fill='black')
 for i,f in enumerate(fs):
  a=f.convert('RGBA').resize((160,320),Image.Resampling.NEAREST).crop((0,100,160,320));board.paste(a,(135+175*i,34+210*j),a)
board.save(Q/'douze-poses-x10.png')
red=Image.open(R/'graphics/object_events/pics/people/red_normal.png');compare=Image.new('RGB',(800,340),(232,232,240));dr=ImageDraw.Draw(compare)
for i,(label,im) in enumerate([('RED',red.crop((0,0,16,32)))]+[(d.upper(),frames[d][0]) for d in frames]):
 a=im.convert('RGBA').resize((128,256),Image.Resampling.NEAREST);compare.paste(a,(i*155+15,10),a);dr.text((i*155+38,280),label,font=font,fill='black')
compare.save(Q/'comparaison-red-x8.png')
movie=[]
for p in [0,1,0,2]:
 im=Image.new('RGBA',(64,32),(232,232,240,255))
 for i,d in enumerate(frames):im.alpha_composite(frames[d][p].convert('RGBA'),(16*i,0))
 movie.append(im.convert('RGB').resize((768,384),Image.Resampling.NEAREST))
movie[0].save(Q/'marche-quatre-directions.gif',save_all=True,append_images=movie[1:],duration=134,loop=0)
red_records=[]
for i in range(9):
 f=red.crop((16*i,0,16*(i+1),32)).convert('RGBA');b=f.getbbox();red_records.append(dict(frame=i,bbox=b,width=b[2]-b[0],height=b[3]-b[1]))
meta=dict(restart_from_scratch=True,native_canvas=[16,32],palette_rgb555=list(pal.values()),logical_rows=base,red_source='graphics/object_events/pics/people/red_normal.png',red_frames=red_records,records=records,front_cyan_eye_viewer_right=True,left_eye_covered=True,right_eye_visible=True,engine_frame_order=order,bytes_4bpp=len(raw))
(D/'CONSTRUCTION.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2));print('New native Red-based12poses built; standard sheet2304bytes.')
