#!/usr/bin/env python3
"""Native Gym victories driven by controller input. Warps, script entry and a
boosted one-member player team are fixtures; no enemy HP, outcomes, badges,
rewards, graphics or palettes are injected. This is not a balance playthrough.
"""
import json,hashlib,os,re,struct,subprocess
from pathlib import Path
from PIL import Image
from mgba_rpc import ROOT
from mgba_new_game import new_game
from mafiamille_qa import C,MAPS,warp,strong_party
rom=Path(os.environ.get('YOKAI_QA_ROM',ROOT/'pokefirered.gba'));mode='prive' if '_audio' in rom.name else 'public'
P=ROOT/'docs/champions-yokai-watch/validation'/mode;P.mkdir(parents=True,exist_ok=True)
rows=[];passed=False;failure=None;r=None
# Native game IDs and original Gym script labels retain their save semantics.
cases=[('wyatt','PewterCity','Brock',1,'TM39','TRAINER_LEADER_BROCK','WYATT','YokaiWyatt'),('katie','CeruleanCity','Misty',2,'TM03','TRAINER_LEADER_MISTY','KATIE','YokaiKatie'),('ariane','VermilionCity','LtSurge',3,'TM34','TRAINER_LEADER_LT_SURGE','ARIANE','Ariane'),('alyzon','PokemonTower_7F','MrFuji',4,'TM19','TRAINER_LEADER_ERIKA','ALYZON BIE','YokaiAlyzon'),('koga','FuchsiaCity','Koga',5,'TM06','TRAINER_LEADER_KOGA','KOGA','Koga'),('berenice','SaffronCity','Sabrina',6,'TM04','TRAINER_LEADER_SABRINA','BÉRÉNICE','YokaiBerenice'),('nathaniel','CinnabarIsland','Blaine',7,'TM38','TRAINER_LEADER_BLAINE','NATHANIEL','YokaiNathaniel'),('don','ViridianCity','Giovanni',8,'TM26','TRAINER_LEADER_GIOVANNI','DON MORLÉONE','YokaiDonMorleone')]
glyphs={m[1]:int(m[2],16) for m in re.finditer(r"^'(.*?)'\s*= ([0-9A-F]{2})$",(ROOT/'charmap.txt').read_text(),re.M)}
def encoded(s):return bytes(glyphs[c] for c in s)+b'\xff'
def field():return r.u32(r.symbols['gMain']+4)==r.symbols['CB2_Overworld']|1
def free():return field() and r.read(r.symbols['sGlobalScriptContextStatus'],1)==b'\x02'
def tick(f,key=8):r.keys={key} if f%16<4 else set();r.run()
def shot(name):r.frame.save(P/(name+'.png'));r.frame.resize((720,480),Image.Resampling.NEAREST).save(P/(name+'-x3.png'))
def report(name,**kw):rows.append(dict(test=name,passed=True,**kw));print(name,kw,flush=True)
def finish(limit=12000):
 for f in range(limit):
  tick(f)
  if f>40 and free():r.keys=set();r.run(8);return
 raise AssertionError(('field script stuck',hex(r.u32(r.symbols['gMain']+4))))
def script(label):r.keys=set();r.call('ScriptContext_SetupScript',r.symbols[label])
def value(mon,field):return r.call('GetMonData',mon,C[field],0)
def expect_party(trainer):
 data=(ROOT/'src/data/trainer_parties.h').read_text();ts=(ROOT/'src/data/trainers.h').read_text();body=re.search(r'\['+trainer+r'\] = \{(.*?)\n    \}',ts,re.S)[1];symbol=re.search(r'ITEM_CUSTOM_MOVES\((\w+)\)',body)[1]
 pb=re.search(r'static const struct TrainerMonItemCustomMoves '+symbol+r'\[\] = \{(.*?)\n\};',data,re.S)[1]
 return [(C[sp],int(lv)) for lv,sp in re.findall(r'\.lvl = (\d+), .species = (SPECIES_\w+)',pb)]
def actors():
 return [(i,r.read(r.symbols['gObjectEvents']+36*i,36)) for i in range(16) if r.read(r.symbols['gObjectEvents']+36*i,1)[0]&1]
def check_overworld(data,obj,key):
 local=data['object_events'].index(obj)+1
 matches=[(i,b) for i,b in actors() if b[8]==local]
 assert len(matches)==1,(key,'leader object missing',local)
 _,b=matches[0];sid=b[4];sp=r.symbols['gSprites']+68*sid
 assert not r.read(sp+62,1)[0]&4,(key,'leader sprite invisible')
 if key not in ['koga','don']:
  folder={'katie':'katie','nathan':'nathan','ariane':'ariane','wyatt':'wyatt','nathaniel':'nathaniel','michael':'michael','berenice':'berenice','alyzon':'alyzon'}[key]
  file='normal.png' if key in ['katie','nathan'] else 'overworld.png'
  im=Image.open(ROOT/'graphics/yokai_characters'/folder/file)
  expected=bytearray()
  for ty in range(4):
   for tx in range(2):
    for y in range(8):
     for x in range(0,8,2):expected.append(im.getpixel((tx*8+x,ty*8+y))|im.getpixel((tx*8+x+1,ty*8+y))<<4)
  attr=struct.unpack('<H',r.read(sp+4,2))[0];tile=attr&1023
  assert r.read(0x06010000+32*tile,256)==bytes(expected),(key,'OW VRAM differs from approved PNG face')
  pal_folder='nathan' if key in ['katie','nathan'] else folder
  palette=(ROOT/'graphics/yokai_characters'/pal_folder/'overworld.gbapal').read_bytes()
  bank=attr>>12
  assert r.read(r.symbols['gPlttBufferUnfaded']+0x200+32*bank,32)==palette[:32],(key,'OW palette')

def continue_save():
 assert r.call('TrySavingData',0,max_frames=1200)==1
 assert r.call('LoadGameSave',0,max_frames=1200)==1
 r.call('SetMainCallback2',r.symbols['CB2_ContinueSavedGame']|1)
 for f in range(2000):
  tick(f)
  if f>160 and free():r.keys=set();return
 raise AssertionError('Flash Continue did not return to field')
def battle(case):
 key,city,leader,badge,tm,trainer,name,gfx=case;mapname=city if city=='PokemonTower_7F' else city+'_Gym'
 data=json.loads((ROOT/'data/maps'/mapname/'map.json').read_text());obj=next(o for o in data['object_events'] if o['script'].endswith('_EventScript_'+leader))
 if mapname=='PokemonTower_7F':r.call('FlagSet',0x322);r.call('VarSet',0x40f3,1)
 warp(r,*MAPS[mapname],obj['x'],obj['y']+(1 if key=='alyzon' else 2));r.call('ZeroPlayerPartyMons');strong_party(r);shot(key+'-overworld')
 check_overworld(data,obj,key)
 original_id=C[obj['graphics_id']]
 assert r.call('GetObjectEventGraphicsInfo',original_id)==r.symbols['gObjectEventGraphicsInfo_'+gfx],(key,'map identity')
 ptr=r.call('YokaiChampionName',C[trainer]);actual=r.read(ptr,len(encoded(name)))
 # Don's pre-existing label may use native shortened spelling, verified by preservation audit.
 if key!='don':assert actual==encoded(name),(key,'name',actual,encoded(name))
 label=mapname+'_EventScript_'+leader;script(label);order=[];checked=False;portrait=False;art=False;intro_seen=False;movie=[]
 callbacks={int(line.split()[0],16)|1 for line in subprocess.check_output(['arm-none-eabi-nm','--defined-only',str(rom.with_suffix('.elf'))],text=True).splitlines() if len(line.split())==3 and line.split()[2]=='HandleInputChooseAction'}
 pic=r.call('YokaiChampionPortrait',C[trainer]);expected=expect_party(trainer);announcement_samples=[];captured=set();reply_frames=[]
 for f in range(26000):
  tick(f);cb=r.u32(r.symbols['gMain']+4)
  if not intro_seen and f%8==0:
   raw=r.read(r.symbols['gStringVar4'],12)
   if raw==r.read(r.symbols[mapname+'_Text_'+('NathanIntro' if key=='nathan' else 'MichaelIntro' if key=='michael' else leader+'Intro')],12) if key!='alyzon' else False:
    shot(key+'-dialogue');intro_seen=True
  if cb==r.symbols['BattleMainCB2']|1:
   if not checked:
    for i,(sp,lv) in enumerate(expected):
     mon=r.symbols['gEnemyParty']+100*i;assert (value(mon,'MON_DATA_SPECIES'),value(mon,'MON_DATA_LEVEL'))==(sp,lv),(key,i)
    if key=='alyzon':
     mon=r.symbols['gEnemyParty']+300
     assert [value(mon,'MON_DATA_'+fld) for fld in ['MAX_HP','ATK','DEF','SPEED','SPATK','SPDEF']]==[140,80,80,25,36,54]
    checked=True
   sid=r.read(r.symbols['gBattlerSpriteIds']+1,1)[0]
   if sid<64:
    a=r.symbols['gSprites']+68*sid
    if not portrait and r.read(a+62,1)[0]&1 and struct.unpack('<H',r.read(a+6,2))[0]==pic and struct.unpack('<h',r.read(a+36,2))[0]==0:
     shot(key+'-portrait');portrait=True
   if f%8==0 and checked:
    idx=struct.unpack('<H',r.read(r.symbols['gBattlerPartyIndexes']+2,2))[0]
    if idx<len(expected) and (not order or idx!=order[-1]):order.append(idx)
   if r.u32(r.symbols['gBattlerControllerFuncs']) in callbacks:
    idx=struct.unpack('<H',r.read(r.symbols['gBattlerPartyIndexes']+2,2))[0]
    if idx<len(expected):
     if idx not in captured:shot(key+'-adversaire-'+str(idx));captured.add(idx)
     if key=='alyzon' and idx==3 and not art:
      tile=struct.unpack('<H',r.read(a+4,2))[0]&1023
      assert r.read(0x06010000+32*tile,2048)==(ROOT/'graphics/yokai_zombies/colosse/battle-front.4bpp').read_bytes()
      assert r.u32(r.symbols['gBattleTypeFlags'])&8 and not r.u32(r.symbols['gBattleTypeFlags'])&(1<<20)
      assert r.call('YokaiChampionExpYield',1,60)==156
      assert r.read(r.symbols['sColossusAnnounced'],1)==b'\x01'
      assert not r.call('YokaiChampionAnnounceColossus',1)
      shot('alyzon-colosse');art=True
   if key=='alyzon' and f%8==0 and r.u32(r.symbols['gBattlescriptCurrInstr'])>=r.symbols['BattleScript_AlyzonColossus'] and r.u32(r.symbols['gBattlescriptCurrInstr'])<r.symbols['BattleScript_AlyzonColossus']+7:
    announcement_samples.append(f)
    reply_frames.append(r.frame.copy())
    if len(announcement_samples)==8:shot('alyzon-replique-colosse')
  if checked and field() and r.read(r.symbols['gBattleOutcome'],1)==b'\x01':finish();break
 else:raise AssertionError((key,'battle did not finish',order,hex(r.u32(r.symbols['gMain']+4))))
 assert checked and portrait,(key,'team/portrait',checked,portrait)
 assert r.call('FlagGet',0x820+badge-1),(key,'badge missing')
 assert r.call('CheckBagHasItem',C['ITEM_'+tm],1),(key,'TM missing')
 assert r.call('HasTrainerBeenFought',C[trainer]),(key,'victory missing')
 if key in ['katie','nathan','ariane','alyzon','nathaniel','michael']:assert order==list(range(len(expected))),(key,'order',order)
 if key=='alyzon':
  assert art and announcement_samples,'Colossus not presented'
  reply_frames[0].resize((720,480),Image.Resampling.NEAREST).save(P/'alyzon-replique-colosse.gif',save_all=True,append_images=[im.resize((720,480),Image.Resampling.NEAREST) for im in reply_frames[1:]],duration=134,loop=0)
  reply_frames[-1].resize((720,480),Image.Resampling.NEAREST).save(P/'alyzon-replique-fin-x3.png')
 shot(key+'-victoire');continue_save();shot(key+'-continuer')
 assert r.call('FlagGet',0x820+badge-1) and r.call('HasTrainerBeenFought',C[trainer])
 assert r.call('CheckBagHasItem',C['ITEM_'+tm],1)
 check_overworld(data,obj,key)
 assert r.call('GetObjectEventGraphicsInfo',original_id)==r.symbols['gObjectEventGraphicsInfo_'+gfx]
 # The same native leader interaction after Continue must not start a second battle.
 count=r.call('GetGameStat',9);script(label);finish();assert r.call('GetGameStat',9)==count
 report('Native Gym victory, reward, Flash Continue and no rematch',champion=key,gender=r.read(r.u32(r.symbols['gSaveBlock2Ptr'])+8,1)[0],party=expected,observed_order=order,portrait=pic,colossus_dialogue_observed=bool(announcement_samples))
try:
 r=new_game()
 for case in cases:battle(case)
 assert all(r.call('FlagGet',0x820+i) for i in range(8));report('All eight native badge flags earned by actual Gym victories')
 r.close();r=new_game(1)
 for i,key,name,gfx in [(1,'nathan','NATHAN','YokaiNathan'),(6,'michael','MICHAEL','YokaiMichael')]:
  case=list(cases[i]);case[0]=key;case[6]=name;case[7]=gfx;battle(case)
 passed=True
except BaseException as e:
 failure=repr(e);print('FAIL',failure,flush=True)
 if r:shot('ECHEC-champions')
 raise
finally:
 if r:r.close()
 (P/'TEST_CHAMPIONS_MGBA.json').write_text(json.dumps(dict(passed=passed,rom_sha256=hashlib.sha256(rom.read_bytes()).hexdigest(),scope=__doc__,results=rows,failure=failure),ensure_ascii=False,indent=2)+'\n')
print('CHAMPIONS PASS',len(rows))
