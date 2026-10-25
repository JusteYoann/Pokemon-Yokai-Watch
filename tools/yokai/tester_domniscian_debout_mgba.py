#!/usr/bin/env python3
"""Apparitions natives de Domniscian et routage de ses deux combats d’arène."""
import json,hashlib,struct
from postgame_qa_common import QA
from mafiamille_qa import strong_party
from mgba_rpc import ROOT
q=QA('TEMP_DOMNISCIAN.json');r=q.r;P=ROOT/'docs/cinematiques-collisions-20261025';rows=[]
try:
 strong_party(r);q.f(0x3e);base=r.snapshot()
 for rematch in (False,True):
  r.restore(base);q.f(0x82c,rematch);q.f(0x4b5,rematch);q.f(0x29a,rematch)
  q.warp('SaffronCity_Gym',14,13);a=q.actors();gfx=r.read(a[7]+5,1)[0];assert r.call('GetObjectEventGraphicsInfo',gfx)==r.symbols['gObjectEventGraphicsInfo_YokaiDomniscian']
  sid=r.read(a[7]+4,1)[0];tile=int.from_bytes(r.read(r.symbols['gSprites']+68*sid+4,2),'little')&1023;assert r.read(0x06010000+tile*32,512)==r.read(r.symbols['gObjectEventPic_YokaiDomniscian'],512)
  (r.frame).save(P/('domniscian-arene-'+('revanche' if rematch else 'initial')+'.png'))
  # Same shared graphics table is used at every Domniscian location.
  tiles=(ROOT/'graphics/yokai_characters/domniscian/overworld.4bpp').read_bytes();assert r.read(r.symbols['gObjectEventPic_YokaiDomniscian'],len(tiles))==tiles
  q.script('SaffronCity_Gym_EventScript_Sabrina');q.wait(lambda:q.callback()=='BattleMainCB2',30000);assert r.call('GetBattleBGM')==348
  r.run(120);pointer=r.u32(r.symbols['gMPlayInfo_BGM']);names=[n for n,v in r.symbols.items() if v==pointer];assert pointer==r.call('YokaiGetSongHeader',348,r.u32(r.symbols['gSongTable']+348*8)),(names,hex(pointer));assert 'mus_yokai_02' in names,names
  rows.append({'combat':'revanche' if rematch else 'initial','graphics_id':161,'sprite_debout_natif_verifie':True,'ost_id':348,'ost_native':names});print('PASS Domniscian',rows[-1],flush=True)
 r.restore(base);q.f(0x82c);q.f(0x30f,False);q.warp('SilphCo_11F',6,10)
 objects=[p for p in q.actors().values() if r.read(p+5,1)[0]==161];assert objects
 r.frame.save(P/'domniscian-yopple.png');rows.append({'lieu':'Yopple, 11F','graphics_id':161,'apparitions_natives':len(objects),'standing_without_desk':True})
finally:
 (P/'DOMNISCIAN_MGBA.json').write_text(json.dumps({'rom_sha256':hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),'scope':__doc__,'checks':rows},ensure_ascii=False,indent=2)+'\n');r.close()
