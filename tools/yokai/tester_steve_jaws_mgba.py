#!/usr/bin/env python3
"""Parties isolées : graphisme Ciléo, scènes Sevii, équipe native et Arène postgame.
Prérequis et équipe niveau100 préparés ; progression et combat par commandes natives.
"""
import hashlib,json,re,struct
from pathlib import Path
from postgame_qa_common import QA
from mgba_rpc import ROOT
D=ROOT/'docs/steve-jaws-sevii-jadielle-20261025';D.mkdir(exist_ok=True)
checks=[]
q=QA('TEMP.json');r=q.r
try:
 q.mon()
 # Native font widths with worst-case player/placeholder lengths.
 maximum=0
 for file in ['data/maps/OneIsland_PokemonCenter_1F/text.inc','data/maps/OneIsland/text.inc','data/maps/CinnabarIsland/text.inc','data/maps/ViridianCity_Gym/scripts.inc']:
  text=(ROOT/file).read_text()
  for label in re.findall(r'^(\w+)::',text,re.M):
   if label not in r.symbols or ('Text_' not in label and 'SteveJaws_Text' not in label):continue
   raw=r.read(r.symbols[label],4096).split(b'\xff',1)[0]
   for line in re.split(b'[\xfa\xfb\xfe]',raw):
    if not line:continue
    line=line.replace(b'\xfd\x01',b'\xd1'*7)
    if len(line)>110:continue
    r.write(r.PARAMS+128,line+b'\xff');width=r.call('GetStringWidth',2,r.PARAMS+128,0);maximum=max(maximum,width)
    assert width<=208,(label,width,line.hex())
 checks.append(dict(test='native_font_widths',maximum=maximum))
 # Before the League, Don remains the story Gym leader and Steve is absent.
 q.warp('ViridianCity_Gym',2,3);r.run(240)
 objects=json.loads((ROOT/'data/maps/ViridianCity_Gym/map.json').read_text())['object_events'];steve=len(objects)
 assert q.local('LOCALID_VIRIDIAN_GIOVANNI') in q.actors() and steve not in q.actors()
 checks.append(dict(test='pre_League_Don_unchanged',passed=True))
 # Introduction on Sevii and its actor walking to the network machine.
 q.warp('OneIsland_PokemonCenter_1F',9,9);q.drain(40000)
 celio=q.local('LOCALID_CELIO');actor=q.actors()[celio]
 assert r.call('GetObjectEventGraphicsInfo',r.read(actor+5,1)[0])==r.symbols['gObjectEventGraphicsInfo_RequinLunettes']
 def colors():
  a=q.actors()[celio];sp=r.symbols['gSprites']+68*r.read(a+4,1)[0];bank=r.read(sp+5,1)[0]>>4
  assert r.read(r.symbols['gPlttBufferUnfaded']+512+32*bank,32)==r.read(r.symbols['gObjectEventPal_RequinLunettes'],32)
 colors();r.frame.save(D/'steve-sevii.png');checks.append(dict(test='Sevii_introduction_actor_and_palette',passed=True))
 # The two original native item exchanges still complete with Steve.
 q.f(0x82c);q.f(0x2dd);r.call('AddBagItem',349,1);r.call('VarSet',0x4076,4)
 q.warp('OneIsland_PokemonCenter_1F',15,7);q.script('OneIsland_PokemonCenter_1F_EventScript_Celio');q.drain(40000)
 assert r.call('VarGet',0x4076)==5;colors();checks.append(dict(test='Ruby_exchange',passed=True))
 q.f(0x2dc);r.call('AddBagItem',350,1);q.script('OneIsland_PokemonCenter_1F_EventScript_Celio');q.drain(40000)
 assert r.call('VarGet',0x4076)==6;colors();checks.append(dict(test='Sapphire_exchange',passed=True))
 # The actual postgame leader is present; talk through the normal A input.
 for i,sp in enumerate((150,149,65,123,25,87)):
  mon=q.mon(i,sp,100)
  for j,m in enumerate((53,94,58,85)):r.call('SetMonMoveSlot',mon,m,j)
 for flag in range(0x820,0x828):q.f(flag)
 q.warp('ViridianCity_Gym',2,3);r.run(240);assert q.local('LOCALID_VIRIDIAN_GIOVANNI') not in q.actors() and steve in q.actors()
 r.frame.save(D/'steve-jadielle.png');q.pulse(4,24);q.pulse(8,24)
 q.wait(lambda:q.callback()=='BattleMainCB2',30000)
 assert r.u32(r.symbols['gTrainerBattleOpponent_A'])&65535==755
 expected=[(18,75),(44,76),(105,77),(145,78),(97,79),(19,80)];actual=[]
 for i,pair in enumerate(expected):
  mon=r.symbols['gEnemyParty']+100*i;item=(r.call('GetMonData',mon,11,0),r.call('GetMonData',mon,56,0));actual.append(item);assert item==pair,(i,item,pair)
 # Capture the trainer portrait once its entry slide is complete.
 found=False
 for frame in range(2000):
  r.keys=set();r.run()
  sprite_id=r.read(r.symbols['gBattlerSpriteIds']+1,1)[0]
  if sprite_id<64:
   sp=r.symbols['gSprites']+68*sprite_id
   if int.from_bytes(r.read(sp+6,2),'little')==171 and struct.unpack('<h',r.read(sp+36,2))[0]==0:
    r.frame.save(D/'portrait-en-combat.png');found=True;break
 assert found,'Portrait Steve non observé'
 q.drain(120000);print('OUTCOME',r.read(r.symbols['gBattleOutcome'],1).hex(),'ACTORS',list(q.actors()),'STEVE',steve,flush=True);r.frame.save(D/'diagnostic-retour.png');assert r.read(r.symbols['gBattleOutcome'],1)==b'\1' and steve in q.actors()
 r.frame.save(D/'apres-victoire.png');checks.append(dict(test='native_postgame_Gym_victory',party=actual,portrait=171,leader_remains=True))
 q.pulse(4,24);q.pulse(8,24);q.wait(lambda:q.callback()=='BattleMainCB2',30000)
 assert r.u32(r.symbols['gTrainerBattleOpponent_A'])&65535==755;checks.append(dict(test='rematch_available',passed=True))
 (D/'TESTS_MGBA.json').write_text(json.dumps(dict(passed=True,rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),scope=__doc__,checks=checks),ensure_ascii=False,indent=2)+'\n');print('PASS',checks,flush=True)
finally:r.close()
