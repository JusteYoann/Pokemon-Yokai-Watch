#!/usr/bin/env python3
"""Native NPC/coordinate events with controller victories and explicit isolated progression fixtures."""
import hashlib,json,re
from mgba_new_game import new_game
from mgba_rpc import ROOT
from mafiamille_qa import MAPS,C,warp,strong_party
from pilote_combat_mgba import battle_keys
from tester_cameos_boss_mgba import interact
P=ROOT/'QA_RECETTE_FINALE/MAFIAMILLE_KANTO/evenements';P.mkdir(parents=True,exist_ok=True)
C['FLAG_BADGE08_GET']=0x827
cases=[('MtMoon_B2F','MtMoon_B2F_EventScript_Grunt1','TRAINER_TEAM_ROCKET_GRUNT'),('CeruleanCity','CeruleanCity_EventScript_Grunt','TRAINER_TEAM_ROCKET_GRUNT_5'),('Route24','Route24_EventScript_Rocket','TRAINER_TEAM_ROCKET_GRUNT_6'),('CeladonCity_GameCorner','CeladonCity_GameCorner_EventScript_RocketGrunt','TRAINER_TEAM_ROCKET_GRUNT_7'),('RocketHideout_B4F','RocketHideout_B4F_EventScript_Grunt1','TRAINER_TEAM_ROCKET_GRUNT_18'),('RocketHideout_B4F','RocketHideout_B4F_EventScript_Giovanni','TRAINER_BOSS_GIOVANNI'),('PokemonTower_7F','PokemonTower_7F_EventScript_Grunt1','TRAINER_TEAM_ROCKET_GRUNT_19'),('PokemonTower_7F','PokemonTower_7F_EventScript_Grunt2','TRAINER_TEAM_ROCKET_GRUNT_20'),('PokemonTower_7F','PokemonTower_7F_EventScript_Grunt3','TRAINER_TEAM_ROCKET_GRUNT_21'),('ViridianCity_Gym','ViridianCity_Gym_EventScript_Giovanni','TRAINER_LEADER_GIOVANNI'),('MtEmber_Exterior','MtEmber_Exterior_EventScript_Grunt1','TRAINER_TEAM_ROCKET_GRUNT_43'),('FiveIsland_Meadow','FiveIsland_Meadow_EventScript_Rocket1','TRAINER_TEAM_ROCKET_GRUNT_49'),('SixIsland_OutcastIsland','SixIsland_OutcastIsland_EventScript_Rocket','TRAINER_TEAM_ROCKET_GRUNT_46'),('FiveIsland_RocketWarehouse','FiveIsland_RocketWarehouse_EventScript_Admin1','TRAINER_TEAM_ROCKET_ADMIN'),('FiveIsland_RocketWarehouse','FiveIsland_RocketWarehouse_EventScript_Admin2','TRAINER_TEAM_ROCKET_ADMIN_2'),('FiveIsland_RocketWarehouse','FiveIsland_RocketWarehouse_EventScript_Gideon','TRAINER_SCIENTIST_GIDEON')]
results=[];r=new_game();strong_party(r)
# Other trainers already defeated to prevent fixture warps from starting unrelated sight battles.
for name in re.findall(r'^    \[(TRAINER_\w+)\] =', (ROOT/'src/data/trainers.h').read_text(),re.M):
 if name in C:r.call('SetTrainerFlag',C[name])
r.call('FlagSet',C['FLAG_GOT_SS_TICKET']);base=r.snapshot();passed=False;error='Interrupted'
def idle():return r.u32(r.symbols['gMain']+4)==r.symbols['CB2_Overworld']|1 and r.read(r.symbols['sGlobalScriptContextStatus'],1)==b'\x02'
def drive(stem,trainer=None,frames=40000):
 started=False;first=None;stable=0
 for f in range(frames):
  r.keys=battle_keys(r,f) if r.u32(r.symbols['gMain']+4)==r.symbols['BattleMainCB2']|1 else ({8} if f%16<4 else set());r.run()
  if r.u32(r.symbols['gMain']+4)==r.symbols['BattleMainCB2']|1:
   if not started:
    first=f
    actual=int.from_bytes(r.read(r.symbols['gTrainerBattleOpponent_A'],2),'little')
    assert trainer is None or actual==trainer,(stem,'unrelated sight battle',actual,trainer)
   started=True
   if f-first in [45,160,360]:r.frame.save(P/(stem+f'-combat-{f-first}.png'))
  ready=idle() and (trainer is None or started and r.call('HasTrainerBeenFought',trainer))
  if ready:
   r.keys=set();r.run(90);assert idle();r.frame.save(P/(stem+'-apres.png'));return dict(native_battle=started,frames=f,controller_victory=trainer is None or r.read(r.symbols['gBattleOutcome'],1)==b'\x01')
 raise AssertionError((stem,'event timeout',started,hex(r.u32(r.symbols['gMain']+4)),r.read(r.symbols['sGlobalScriptContextStatus'],1).hex()))
def prepare(mapname):
 c=json.loads((ROOT/'data/maps'/mapname/'map.json').read_text())
 for o in c.get('object_events',[]):
  if o.get('flag') not in [None,'0'] and o.get('flag') in C:r.call('FlagClear',C[o['flag']])
 return c
try:
 for index,(mapname,script,trainerkey) in enumerate(cases):
  r.restore(base);strong_party(r);c=prepare(mapname);o=next(o for o in c['object_events'] if o.get('script')==script);trainer=C[trainerkey];r.call('ClearTrainerFlag',trainer)
  if mapname=='MtEmber_Exterior':r.call('VarSet',C['VAR_MAP_SCENE_ONE_ISLAND_POKEMON_CENTER_1F'],4);r.call('VarSet',C['VAR_MAP_SCENE_MT_EMBER_EXTERIOR'],2)
  warp(r,*MAPS[mapname],o['x'],o['y']+1);stem=f'{index:02d}-{mapname}'
  if idle():interact(r)
  result=drive(stem,trainer);assert result['controller_victory']
  if mapname=='CeruleanCity':assert r.call('CheckBagHasItem',C['ITEM_TM28'],1) and r.call('FlagGet',C['FLAG_GOT_TM28_FROM_ROCKET'])
  if mapname=='Route24':assert r.call('CheckBagHasItem',C['ITEM_NUGGET'],1) and r.call('VarGet',C['VAR_MAP_SCENE_ROUTE24'])==1
  if trainerkey=='TRAINER_LEADER_GIOVANNI':assert r.call('FlagGet',C['FLAG_BADGE08_GET']) and r.call('CheckBagHasItem',C['ITEM_TM26'],1)
  if trainerkey=='TRAINER_BOSS_GIOVANNI':assert not r.call('FlagGet',C['FLAG_HIDE_SILPH_SCOPE'])
  if trainerkey=='TRAINER_TEAM_ROCKET_GRUNT_18':assert not r.call('FlagGet',C['FLAG_HIDE_LIFT_KEY'])
  if trainerkey=='TRAINER_TEAM_ROCKET_ADMIN_2':assert r.call('FlagGet',C['FLAG_DEFEATED_ROCKETS_IN_WAREHOUSE'])
  if trainerkey=='TRAINER_SCIENTIST_GIDEON':assert r.call('FlagGet',C['FLAG_RECOVERED_SAPPHIRE']) and r.call('CheckBagHasItem',C['ITEM_SAPPHIRE'],1)
  if trainerkey in ['TRAINER_BOSS_GIOVANNI','TRAINER_TEAM_ROCKET_GRUNT_18']:
   itemscript='RocketHideout_B4F_EventScript_'+('SilphScope' if trainerkey=='TRAINER_BOSS_GIOVANNI' else 'LiftKey');item=C['ITEM_SILPH_SCOPE' if trainerkey=='TRAINER_BOSS_GIOVANNI' else 'ITEM_LIFT_KEY'];ball=next(o for o in c['object_events'] if o.get('script')==itemscript)
   warp(r,*MAPS[mapname],ball['x'],ball['y']+1);interact(r);drive(stem+'-objet');assert r.call('CheckBagHasItem',item,1);result['native_reward_collected']=True
  results.append(dict(map=mapname,script=script,trainer=trainerkey,**result,passed=True));print('EVENT PASS',mapname,trainerkey,flush=True)
 # Two real coordinate triggers for the Silph boss; no replacement of the battle callback.
 for x in [5,6]:
  r.restore(base);prepare('SilphCo_11F');r.call('ClearTrainerFlag',C['TRAINER_BOSS_GIOVANNI_2']);r.call('FlagSet',C['FLAG_SILPH_11F_DOOR']);r.call('VarSet',C['VAR_MAP_SCENE_SILPH_CO_11F'],0)
  warp(r,*MAPS['SilphCo_11F'],x,16);r.keys={4};r.run(16);r.keys=set()
  result=drive('silph-approche-'+str(x),C['TRAINER_BOSS_GIOVANNI_2']);assert r.call('FlagGet',C['FLAG_HIDE_SAFFRON_ROCKETS']) and r.call('VarGet',C['VAR_MAP_SCENE_SILPH_CO_11F'])==1
  results.append(dict(map='SilphCo_11F',coordinate_trigger_x=x,liberation_flags=True,**result,passed=True));print('EVENT PASS Silph trigger',x,flush=True)
 # The complete Lorelei scene through the original coordinate trigger.
 r.restore(base);prepare('FourIsland_IcefallCave_Back');r.call('ClearTrainerFlag',C['TRAINER_TEAM_ROCKET_GRUNT_45'])
 warp(r,*MAPS['FourIsland_IcefallCave_Back'],12,19);r.keys={4};r.run(16);r.keys=set()
 result=drive('olga-grotte',C['TRAINER_TEAM_ROCKET_GRUNT_45']);assert r.call('VarGet',C['VAR_MAP_SCENE_ICEFALL_CAVE_BACK'])==1
 results.append(dict(map='FourIsland_IcefallCave_Back',original_Lorelei_scene=True,**result,passed=True));print('EVENT PASS Lorelei scene',flush=True)
 # Fuji rescue and the existing Poke Flute reward, with actual NPC interactions.
 r.restore(base);c=prepare('PokemonTower_7F');fuji=next(o for o in c['object_events'] if o.get('script')=='PokemonTower_7F_EventScript_MrFuji')
 warp(r,*MAPS['PokemonTower_7F'],fuji['x'],fuji['y']+1);interact(r);drive('fuji-liberation');assert r.call('FlagGet',C['FLAG_RESCUED_MR_FUJI'])
 c=prepare('LavenderTown_VolunteerPokemonHouse');fuji=next(o for o in c['object_events'] if o.get('script')=='LavenderTown_VolunteerPokemonHouse_EventScript_MrFuji')
 warp(r,*MAPS['LavenderTown_VolunteerPokemonHouse'],fuji['x'],fuji['y']+1);interact(r);drive('fuji-flute');assert r.call('CheckBagHasItem',C['ITEM_POKE_FLUTE'],1)
 interact(r);drive('fuji-flute-second-passage');assert not r.call('CheckBagHasItem',C['ITEM_POKE_FLUTE'],2)
 results.append(dict(event='Fuji rescued, native warp, Poke Flute unique on second interaction',passed=True));print('EVENT PASS Fuji rescue/flute',flush=True)
 # A full normal-item pocket prevents the bridge reward and fight, then permits retry.
 r.restore(base);c=prepare('Route24');target=next(o for o in c['object_events'] if o.get('script')=='Route24_EventScript_Rocket');r.call('ClearTrainerFlag',C['TRAINER_TEAM_ROCKET_GRUNT_6']);r.call('ClearBag');filled=[]
 for n in range(1,347):
  if n==C['ITEM_NUGGET'] or r.call('GetPocketByItemId',n)!=1:continue
  if r.call('AddBagItem',n,1):filled.append(n)
  if len(filled)==42:break
 assert len(filled)==42 and not r.call('CheckBagHasSpace',C['ITEM_NUGGET'],1)
 warp(r,*MAPS['Route24'],target['x'],target['y']+1);interact(r);drive('pont-sac-plein');assert not r.call('HasTrainerBeenFought',C['TRAINER_TEAM_ROCKET_GRUNT_6']) and not r.call('CheckBagHasItem',C['ITEM_NUGGET'],1)
 r.call('RemoveBagItem',filled[0],1);interact(r);drive('pont-sac-libere',C['TRAINER_TEAM_ROCKET_GRUNT_6']);assert r.call('CheckBagHasItem',C['ITEM_NUGGET'],1)
 assert r.call('TrySavingData',0,max_frames=1200)==1;r.call('VarSet',C['VAR_MAP_SCENE_ROUTE24'],0);assert r.call('LoadGameSave',0,max_frames=1200)==1;assert r.call('VarGet',C['VAR_MAP_SCENE_ROUTE24'])==1 and r.call('CheckBagHasItem',C['ITEM_NUGGET'],1)
 results.append(dict(event='Bridge full bag, no premature fight, retry, native Flash save/load',passed=True));print('EVENT PASS Bridge full bag/save',flush=True)
 passed=True;error=None
except BaseException as e:error=str(e);r.frame.save(P/'diagnostic.png');raise
finally:
 r.close();(P/'TEST_MGBA.json').write_text(json.dumps(dict(passed=passed,error=error,rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),scope=__doc__,fixtures='Real new-game then warps, explicit visibility/progression, level100 player with999 stats for wins; enemy teams and event programs unchanged. Independent cases, not a full adventure or balance validation.',results=results),ensure_ascii=False,indent=2)+'\n')
