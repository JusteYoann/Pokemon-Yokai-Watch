#!/usr/bin/env python3
"""Actual private mixer routing for the three approved battle roles."""
import hashlib,json,struct
from mgba_rpc import ROOT
from mgba_new_game import new_game
from mafiamille_qa import strong_party
Q=ROOT/'QA_RECETTE_FINALE/DON_SPIRATON';rows=[];passed=False;live=False
try:
 for trainer,slot in [(743,3),(744,6),(739,15)]:
  r=new_game();live=True;strong_party(r)
  if trainer==744:r.call('SpiratonBattleArmPrototype')
  r.write(r.symbols['gTrainerBattleOpponent_A'],struct.pack('<H',trainer));r.call('StartTrainerBattle')
  for f in range(700):r.keys={0} if f%16<4 else set();r.run()
  header=r.u32(r.symbols['gMPlayInfo_BGM']);assert header==r.symbols[f'mus_yokai_{slot:02d}']
  wave=r.symbols[f'yokai_wave_{slot:02d}'];channels=[]
  for i in range(5):
   p=r.symbols['gSoundInfo']+80+64*i
   if r.u32(p+36)==wave and r.read(p,1)[0]&0x83:channels.append(i)
  assert channels,(trainer,slot)
  rows.append(dict(trainer=trainer,private_slot=slot,native_active_channels=channels,passed=True));r.close();live=False
 passed=True
finally:
 try:
  if live:r.close()
 except Exception:pass
 (Q/'MUSIQUES_MGBA.json').write_text(json.dumps(dict(passed=passed,scope=__doc__,rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),results=rows),indent=2)+'\n')
print('PASS private mixer: Ghoulfather, Zazelmare, Matt Decisive Battle')
