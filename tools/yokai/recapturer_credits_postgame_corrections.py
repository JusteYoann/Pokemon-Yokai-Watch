#!/usr/bin/env python3
"""Photos du moteur mGBA, positions de test isolées et sol vérifié pour les deux joueurs."""
import json,subprocess,hashlib
from PIL import Image,ImageOps
from postgame_qa_common import QA
from mgba_rpc import ROOT
from mafiamille_qa import C
D=ROOT/'docs/postgame-corrections-terminyanator-20261025';D.mkdir(exist_ok=True)
board=json.loads((ROOT/'data/yokai/credits_storyboard.json').read_text());rep=json.loads((ROOT/'data/yokai/credits_replacements.json').read_text());rows=[]
for gender,label in enumerate(('garcon','fille')):
 q=QA('TEMP.json');r=q.r
 try:
  r.write(r.u32(r.symbols['gSaveBlock2Ptr'])+8,bytes([gender]));q.mon()
  r.call('VarSet',0x4020,10000)
  for index,mp,x,y in [(12,'PokemonTower_7F',11,5),(21,'CinnabarIsland',17,14),(7,'Route25_SeaCottage',7,6),(28,'CeruleanCave_1F',22,18)]:
   if index==7:
    q.f(C['FLAG_HIDE_BILL_CLEFAIRY']);q.f(C['FLAG_HIDE_BILL_HUMAN_SEA_COTTAGE'],False)
   if index==28:
    for f in (0x82c,0x32f,0x345,0x33b):q.f(f)
   if index==21:
    q.f(0x32c);r.call('VarSet',0x4071,4);r.call('VarSet',0x4072,2)
   if index==12:
    for opponent in (369,370,371):r.call('SetTrainerFlag',opponent)
   q.warp(mp,x,y);r.keys=set();r.run(240)
   if index==7:
    q.f(C['FLAG_HIDE_BILL_CLEFAIRY']);q.f(C['FLAG_HIDE_BILL_HUMAN_SEA_COTTAGE'],False)
    r.call('RemoveObjectEventByLocalIdAndMap',2,q.maps[mp][1],q.maps[mp][0])
    r.call('TrySpawnObjectEvent',1,q.maps[mp][1],q.maps[mp][0])
    r.call('MoveObjectEventToMapCoords',q.actors()[1],17,13)
    r.call('ObjectEventTurn',q.actors()[1],3)
    r.run(12)
   assert r.call('MapGridGetCollisionAt',x+7,y+7)==0,(mp,x,y)
   r.call('LockPlayerFieldControls');r.call('FreezeObjectEvents');r.call('ObjectEventTurn',q.actors()[255],2)
   r.run(8);native=D/f'{label}-credit-{index}-native.png';r.frame.save(native)
   row=dict(gender=label,index=index,map=mp,player=[x,y],floor=True,capture=str(native.relative_to(ROOT)));rows.append(row)
   s=board['slides'][index];photo=ImageOps.fit(r.frame.convert('RGB'),(s['width'],s['height']),method=Image.Resampling.NEAREST).quantize(colors=95 if index==28 else 223,dither=Image.Dither.NONE)
   out=Image.new('P',photo.size);out.putpalette([0,0,0]+photo.getpalette()[:669]+[0]*96);out.putdata([v+1 for v in photo.getdata()]);stem=f'postgame-{label}-28' if index==28 else f'{label}-{index:02}';out.save(ROOT/f'graphics/yokai_credits/{stem}.png')
   subprocess.run(['python3',str(ROOT/'tools/yokai/preparer_souvenirs_credits.py'),'--pack',stem],check=True,stdout=subprocess.DEVNULL)
   if index!=28:
    entry=rep.setdefault(str(index),dict(title=s['title'],captures={}))
    entry['captures'][label]=row['capture']
   r.call('UnlockPlayerFieldControls');print('PASS',row,flush=True)
 finally:r.close()
(ROOT/'data/yokai/credits_replacements.json').write_text(json.dumps(rep,ensure_ascii=False,indent=2)+'\n')
(D/'PHOTOS_CREDITS.json').write_text(json.dumps(dict(scope=__doc__,captures=rows,rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest()),ensure_ascii=False,indent=2)+'\n')
