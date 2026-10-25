#!/usr/bin/env python3
"""Fixtures mGBA isolées : crédits postgame, retour blanc, cadeau et sauvegarde.
Ces vérifications ne font pas partie de l'aventure filmée par entrées manette.
"""
import hashlib,json,struct,os
from pathlib import Path
from postgame_qa_common import QA
from mgba_rpc import ROOT
D=ROOT/os.environ.get('YOKAI_CREDITS_POSTGAME_DIR','docs/credits-postgame-yoann-20261025');D.mkdir(exist_ok=True)
checks=[]
for gender,label in enumerate(('garcon','fille')):
 q=QA('TEMP_CREDITS.json');q.P=D;r=q.r
 try:
  r.write(r.u32(r.symbols['gSaveBlock2Ptr'])+8,bytes([gender]));q.mon();q.f(0x331)
  q.warp('PalletTown_PlayersHouse_2F',6,3)
  before=struct.unpack('<hh',r.read(r.u32(r.symbols['gSaveBlock1Ptr']),4))
  if gender==0:
   q.script('Yoann_EventScript_NPC')
   q.wait(lambda:q.callback()=='BattleMainCB2',18000)
  else:q.script('Yoann_EventScript_FirstVictory')
  q.wait(lambda:q.callback()=='CB2_RollYokaiCredits',60000)
  assert q.fg(0x332) and not q.fg(0x333)
  visited=set();photos=set();white=False
  for f in range(16000):
   if q.callback()!='CB2_RollYokaiCredits':break
   index=r.read(r.symbols['sYokaiCreditsSlide'],1)[0];tick=int.from_bytes(r.read(r.symbols['sYokaiCreditsTick'],2),'little')
   if index<32:visited.add(index)
   if index in (27,28,29,30,31) and 160<=tick<170 and index not in photos:
    stem=ROOT/'graphics/yokai_credits'/((f'postgame-{label}-{index}') if index<31 else f'{label}-31')
    tiles=stem.with_suffix('.8bpp').read_bytes();assert r.read(0x6000000,len(tiles))==tiles
    assert r.read(r.symbols['gPlttBufferUnfaded'],480)==stem.with_suffix('.gbapal').read_bytes()[:480]
    r.frame.save(D/f'{label}-credit-{index}.png');photos.add(index)
   if index==32 and tick>=178:
    white=r.read(r.symbols['gPlttBufferFaded'],512)==struct.pack('<H',0x7fff)*256
   r.keys=set();r.run()
  assert visited==set(range(32)) and photos=={27,28,29,30,31},(visited,photos)
  assert white
  q.drain(18000)
  assert q.fg(0x332) and q.fg(0x333) and r.call('CheckBagHasItem',52,1)
  assert not r.call('CheckBagHasItem',52,2)
  sb=r.u32(r.symbols['gSaveBlock1Ptr']);assert struct.unpack('<hh',r.read(sb,4))==before
  assert r.read(sb+4,2)==bytes(q.maps['PalletTown_PlayersHouse_2F'])
  assert not r.read(r.symbols['sPostgameCredits'],1)[0]
  assert r.read(r.symbols['gPlttBufferFaded'],1024)==r.read(r.symbols['gPlttBufferUnfaded'],1024)
  r.frame.save(D/f'{label}-retour-chambre.png')
  q.pulse(3,90)
  assert any('StartMenu' in q.reverse.get(r.u32(r.symbols['gTasks']+40*i),'') for i in range(16) if r.read(r.symbols['gTasks']+40*i+4,1)==b'\1')
  q.pulse(0,90);q.drain()
  q.saved(0x332,0x333);assert r.call('CheckBagHasItem',52,1)
  q.script('Yoann_EventScript_NPC');q.drain();assert not r.call('CheckBagHasItem',52,2)
  checks.append(dict(gender=label,native_six_mon_victory=gender==0,all_32_slides=True,postgame_photos_and_original_group=True,white_return=white,return_to_same_position=True,charm_after_credits=True,single_charm=True,native_save_continue=True,later_dialogue_no_replay=True))
  print('PASS postgame',label,checks[-1],flush=True)
 finally:r.close()
# First-ending regression: normal League credits still use the original photos
# and reset to the title. No postgame entry point is involved.
q=QA('TEMP_CREDITS.json');r=q.r
try:
 r.call('DoCredits');r.run(10);visited=set();original=False
 for f in range(16000):
  if q.callback()!='CB2_RollYokaiCredits':break
  idx=r.read(r.symbols['sYokaiCreditsSlide'],1)[0];tick=int.from_bytes(r.read(r.symbols['sYokaiCreditsTick'],2),'little')
  if idx<32:visited.add(idx)
  if idx==30 and tick==160:
   stem=ROOT/'graphics/yokai_credits/garcon-30';original=r.read(0x6000000,len(stem.with_suffix('.8bpp').read_bytes()))==stem.with_suffix('.8bpp').read_bytes()
  r.run()
 assert visited==set(range(32)) and original
 r.run(180);assert q.callback()!='CB2_Overworld'
 checks.append(dict(league_32_slides=True,league_original_images=True,league_reset=True))
 print('PASS Ligue',flush=True)
finally:r.close()
(D/'TESTS_MGBA.json').write_text(json.dumps(dict(passed=True,scope=__doc__,rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),checks=checks),ensure_ascii=False,indent=2)+'\n')
