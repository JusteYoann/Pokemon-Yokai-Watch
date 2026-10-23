#!/usr/bin/env python3
"""Native production-room loss/retry fixtures. Only player's strength and initial
position/respawn are prepared; no enemy HP, outcome or victory-flag injection.
"""
import os,json,struct,hashlib
from mgba_rpc import ROOT
from mgba_new_game import new_game
from mafiamille_qa import C,MAPS,warp,strong_party
from pilote_combat_mgba import battle_keys
Q=ROOT/os.environ.get('YOKAI_LOSS_REPORT_DIR','QA_RECETTE_FINALE/DON_SPIRATON/ETAPE_B/jalon4/defaites-public');Q.mkdir(parents=True,exist_ok=True)
r=new_game();base=r.snapshot();rows=[];passed=False
try:
 for target in [743,744]:
  r.restore(base);r.call('SetLastHealLocationWarp',20)
  if target==743:
   r.call('CreateMon',r.symbols['gPlayerParty'],1,1,0,1,0,0,0x1234);r.write(r.symbols['gPlayerPartyCount'],b'\1')
  else:strong_party(r)
  warp(r,*MAPS['PokemonLeague_ChampionsRoom'],6,18)
  weakened=False;observed=False
  for f in range(45000):
   cb=r.u32(r.symbols['gMain']+4);ib=cb==r.symbols['BattleMainCB2']|1
   trainer=int.from_bytes(r.read(r.symbols['gTrainerBattleOpponent_A'],2),'little')
   if ib and trainer==target:
    observed=True
    if target==744 and not weakened and r.read(r.symbols['sFirst'],1)==b'\1' and r.read(r.symbols['gBattleMons']+88+42,1)==b'8':
     # Player-only battle fixture, after normal Don victory and Matt heal.
     for offset in [2,4,6,8,10,40]:r.write(r.symbols['gBattleMons']+offset,struct.pack('<H',1))
     for field in ['MON_DATA_HP','MON_DATA_MAX_HP','MON_DATA_ATK','MON_DATA_SPATK','MON_DATA_DEF','MON_DATA_SPDEF']:
      r.w32(r.PARAMS+128,1);r.call('SetMonData',r.symbols['gPlayerParty'],C[field],r.PARAMS+128)
     r.call('SetMonMoveSlot',r.symbols['gPlayerParty'],C['MOVE_TACKLE'],0)
     r.write(r.symbols['gBattleMons']+12,struct.pack('<4H',C['MOVE_TACKLE'],0,0,0));r.write(r.symbols['gBattleMons']+36,b'\x23\0\0\0');weakened=True
   r.keys=battle_keys(r,f) if ib else ({8} if f%16<4 else set());r.run()
   pair=r.read(r.u32(r.symbols['gSaveBlock1Ptr'])+4,2)
   if observed and pair==bytes(MAPS['SixIsland_PokemonCenter_1F']) and cb==r.symbols['CB2_Overworld']|1:
    r.keys=set();r.run(360);break
  else:raise AssertionError(('Native loss did not reach Center',target,observed,weakened))
  assert r.call('FlagGet',0x82C)==0 and r.call('FlagGet',0x500+744)==0
  assert r.call('FlagGet',0x500+743)==(target==744)
  assert not r.call('SpiratonArtIsActive') and r.call('GetSpriteTileStartByTag',0x7D54)==65535
  r.frame.save(Q/f'defaite-{target}-centre.png')
  warp(r,*MAPS['PokemonLeague_ChampionsRoom'],6,18)
  for f in range(1600):
   r.keys={8} if f%16<4 else set();r.run()
   if r.u32(r.symbols['gMain']+4)==r.symbols['BattleMainCB2']|1 and int.from_bytes(r.read(r.symbols['gTrainerBattleOpponent_A'],2),'little')==743:break
  else:raise AssertionError(('Retry must start classical Don, not fusion',target))
  r.frame.save(Q/f'reprise-{target}-don-classique.png')
  rows.append(dict(test='Native whiteout then normal room retry starts Don743',lost_to=target,passed=True,spiraton_flag=False,game_clear=False,first_don_flag=target==744))
 passed=True
finally:
 if not passed:r.frame.save(Q/'diagnostic.png')
 (Q/'DEFAITES_MGBA.json').write_text(json.dumps(dict(passed=passed,scope=__doc__,rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),results=rows),indent=2)+'\n');r.close()
print('PASS: normal losses against both opponents, native whiteout, clean resources and full retry')
