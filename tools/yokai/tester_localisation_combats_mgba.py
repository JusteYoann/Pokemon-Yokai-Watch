#!/usr/bin/env python3
"""Native battle text expansion/rendering and the real300-byte buffer bound."""
import hashlib,json,re,subprocess
from PIL import Image,ImageDraw
from mgba_rpc import ROOT
from mgba_new_game import new_game
P=ROOT/'QA_RECETTE_FINALE/LOCALISATION_FR/combats';P.mkdir(parents=True,exist_ok=True)
glyph={m[1]:int(m[2],16) for m in re.finditer(r"^'(.*?)'\s*= ([0-9A-F]{2})$",(ROOT/'charmap.txt').read_text(),re.M)};glyph["'"]=glyph['’']
samples=['sText_AttackerUsedX','sText_AttackMissed','sText_AvoidedDamage','sText_PkmnProtectedItself','sText_PkmnWasPoisoned','sText_PkmnHurtByPoison','sText_PkmnWasParalyzed','sText_PkmnIsParalyzed','sText_PkmnIsConfused','sText_PkmnHealedConfusion','sText_PkmnRegainedHealth','sText_PkmnHPFull','sText_CriticalHit','sText_SuperEffective','sText_NotVeryEffective','sText_TrainerBlockedBall','sText_PkmnBrokeFree','sText_GiveNicknameCaptured','sText_PkmnPreventsUsage','sText_PkmnsXPreventsFlinching','sText_NoPPLeft','sText_PkmnFellAsleep','sText_PkmnWokeUp','sText_ItDoesntAffect','gText_ForPetesSake','gText_HowDissapointing']
r=new_game();rows=[];passed=False;error='Interrupted'
try:
 r.call('CreateMon',r.symbols['gPlayerParty'],1,15,31,1,100,0,0);r.write(r.symbols['gPlayerPartyCount'],b'\x01');r.call('CreateMon',r.symbols['gEnemyParty'],16,10,31,1,101,0,0);r.write(r.symbols['gEnemyPartyCount'],b'\x01');r.call('StartWildBattle')
 callbacks={int(v[0],16)|1 for line in subprocess.check_output(['arm-none-eabi-nm','--defined-only',str(r.elf_path)],text=True).splitlines() if len(v:=line.split())==3 and v[2] in ['HandleInputChooseAction','HandleInputChooseMove']}
 assert callbacks
 for f in range(6000):
  r.keys={8} if f%16<3 else set();r.run()
  if r.u32(r.symbols['gMain']+4)==r.symbols['BattleMainCB2']|1 and r.u32(r.symbols['gBattlerControllerFuncs']) in callbacks:break
 else:raise AssertionError('Wild battle did not reach command menu')
 r.keys=set();r.run(120)
 # Suspend only the battle controller for this text-rendering fixture. The
 # normal BattleMainCB2 still draws sprites, tasks and native text printers.
 r.write(r.symbols['gMain'],(r.symbols['BattleControllerDummy']|1).to_bytes(4,'little'))
 original_bottom=r.frame.crop((4,116,236,156)).tobytes()
 dest=r.call('AllocZeroed',1024);packet=r.call('AllocZeroed',64);assert dest and packet
 r.write(packet,(10).to_bytes(2,'little')*2);r.write(r.symbols['sBattleMsgDataPtr'],packet.to_bytes(4,'little'))
 base=r.snapshot()
 for key in samples:
  print('BATTLE',key,flush=True)
  r.restore(base)
  # Direct rendering fixture must supply a valid move; command-menu controller
  # buffers no longer hold a BattleMsgData move packet after the intro.
  r.write(r.symbols['sBattleMsgDataPtr'],packet.to_bytes(4,'little'))
  for symbol,value in [('gBattleTextBuff1','Jibanyan'),('gBattleTextBuff2','Griffe'),('gBattleTextBuff3','10')]:r.write(r.symbols[symbol],bytes(glyph[c] for c in value)+b'\xff')
  r.write(dest,b'\xa5'*1024)
  size=r.call('BattleStringExpandPlaceholders',r.symbols[key],dest)
  assert size<300,(key,size,'Native displayed-string capacity exceeded')
  assert r.read(dest+300,8)==b'\xa5'*8,(key,'Overflow into guard region')
  # GetStringWidth only resets on NEWLINE; the dialogue renderer also
  # resets at prompt-clear/scroll, so measure each expanded visible line.
  raw=r.read(dest,size).rstrip(b'\xff');line_widths=[]
  for line in re.split(b'[\xfa\xfb\xfe]',raw):
   r.write(dest+512,line+b'\xff');line_widths.append(r.call('GetStringWidth',2,dest+512,0))
  width=max(line_widths,default=0)
  assert width<=208,(key,width,'Expanded line too wide')
  # Match PlayerHandlePrintString: command menus use BG0 Y=160.
  r.write(r.symbols['gBattle_BG0_X'],b'\0\0');r.write(r.symbols['gBattle_BG0_Y'],b'\0\0')
  r.call('BattlePutTextOnWindow',dest,0);r.run(400)
  assert r.frame.crop((4,116,236,156)).tobytes()!=original_bottom,(key,'Battle menu overwrote the preview')
  r.frame.save(P/(key+'.png'))
  rows.append(dict(symbol=key,expanded_bytes=size,native_max_line_pixels=width,rendered_in_native_battle_window=True,buffer_limit_passed=True))
 passed=True;error=None
except BaseException as e:error=str(e);r.frame.save(P/'diagnostic.png');raise
finally:
 r.close();(P/'TEST_MGBA.json').write_text(json.dumps(dict(passed=passed,error=error,rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),scope='Real new-game, party/enemy fixtures and native wild battle;26 linked French strings expanded and rendered with actual battle state plus declared text buffers. Not26 triggered combat outcomes or all moves/items.',results=rows),ensure_ascii=False,indent=2)+'\n')
if passed:
 sheet=Image.new('RGB',(960,((len(rows)+3)//4)*184),(224,224,224));d=ImageDraw.Draw(sheet)
 for i,row in enumerate(rows):
  x=i%4*240;y=i//4*184;d.text((x+2,y+2),row['symbol'][:34],fill='black');sheet.paste(Image.open(P/(row['symbol']+'.png')),(x,y+22))
 sheet.save(P/'PLANCHE.png');print('BATTLE FR PASS',len(rows))
