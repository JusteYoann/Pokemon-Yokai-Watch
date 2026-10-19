#!/usr/bin/env python3
"""Linked French menu labels, native widths and actual Start/party/bag/Medallium."""
import hashlib,json,re,struct
from mgba_rpc import Emulator,ROOT
P=ROOT/'QA_RECETTE_FINALE/LOCALISATION_FR/interfaces';P.mkdir(parents=True,exist_ok=True);(P/'preuves').mkdir(exist_ok=True);checks=[];r=Emulator()
glyphs={m[1]:int(m[2],16) for m in re.finditer(r"^'(.*?)'\s*= ([0-9A-F]{2})$",(ROOT/'charmap.txt').read_text(),re.M)}
glyphs["'"]=glyphs['’']
def pulse(key,frames=120):
 r.keys={key};r.run(1);r.keys=set();r.run(frames)
def fixture():
 r.call('SetSaveBlocksPointers');r.call('Sav2_ClearSetDefault');r.call('CB2_NewGame');r.run(180)
 r.write(r.u32(r.symbols['gSaveBlock2Ptr']),bytes(glyphs[c] for c in 'Test')+b'\xff');r.call('CreateMon',r.symbols['gPlayerParty'],1,10,31,1,100,1,0);r.write(r.symbols['gPlayerPartyCount'],b'\x01')
 r.call('FlagSet',0x828);r.call('FlagSet',0x829);r.call('GetSetPokedexFlag',1,2);r.call('GetSetPokedexFlag',1,3);r.call('SetWarpDestination',3,0,255,10,10);r.call('WarpIntoMap');r.call('SetMainCallback2',r.symbols['CB2_LoadMap']|1);r.run(600)
passed=False;error='Interrupted'
try:
 # Check actual linked labels, including accent encoding; not just their source.
 manual={'gText_MenuPokedex':'Médallium','gText_MenuPokemon':'Yo-kai','gText_MenuBag':'SAC','gText_MenuSave':'SAUVER','gText_TextSpeed':'VITESSE TEXTE','gText_BattleScene':'ANIMATIONS','gText_YourName':'TON PRÉNOM?','gText_WithdrawPokemon':'RETIRER YO-KAI','gText_DepositPokemon':'DÉPOSER YO-KAI','gText_PokeSum_PageName_KnownMoves':'CAPACITÉS'}
 for name,text in manual.items():
  if '{' in text or chr(92) in text:continue
  expected=bytes(glyphs[ch] for ch in text)+b'\xff';assert r.read(r.symbols[name],len(expected))==expected,(name,'Linked text mismatch')
  width=r.call('GetStringWidth',2,r.symbols[name],0)
  if name.startswith('gText_Menu'):assert width<=56,(name,width,'8tiles minus8px cursor')
  checks.append(dict(test='Exact linked label/native normal font',symbol=name,text=text,width_pixels=width,passed=True))
 fixture();base=r.snapshot()
 for order,label in [(0,'medallium'),(1,'equipe'),(2,'sac')]:
  r.restore(base);pulse(3,180)
  assert r.read(r.symbols['sNumStartMenuItems'],1)[0]==7
  wid=r.call('GetStartMenuWindowId');assert r.read(r.symbols['gWindows']+12*wid+3,1)[0]==8
  r.frame.save(P/'preuves'/'menu-francais.png')
  for _ in range(order):pulse(5,20)
  assert r.read(r.symbols['sStartMenuCursorPos'],1)[0]==order
  pulse(8,600);r.frame.save(P/'preuves'/f'interface-{label}.png')
  assert r.u32(r.symbols['gMain']+4)!=r.symbols['CB2_Overworld']|1,(label,'Did not open chosen interface')
  checks.append(dict(test='Actual START/DPAD/A opens '+label,passed=True))
  if label=='medallium':
   # Explicit fixture adds all151 flags plus one out-of-range legacy/import flag.
   r.call('EnableNationalPokedex')
   for number in list(range(1,152))+[386]:
    r.call('GetSetPokedexFlag',number,2);r.call('GetSetPokedexFlag',number,3)
   assert r.call('DexScreen_GetDexCount',0,1)==151
   assert r.call('DexScreen_GetDexCount',1,1)==151
   for order in range(6):assert r.call('DexScreen_CountMonsInOrderedList',order)==151,(order,'Médallium should contain151 entries')
   checks.append(dict(test='National postgame unlock preserves151-entry Medallium in six sorts and seen/caught counts; outside151 imported flag ignored by UI',passed=True,actual_capture_of151_tested=False))

 passed=True;error=None
except Exception as e:error=str(e);raise
finally:
 if not passed:r.frame.save(P/'preuves'/'interface-diagnostic.png')
 r.close();(P/'INTERFACE_FR_MGBA.json').write_text(json.dumps(dict(passed=passed,error=error,rom_sha256=hashlib.sha256(r.elf_path.with_suffix('.gba').read_bytes()).hexdigest(),scope='Native linked labels, font widths and controller-opened interfaces; does not validate every text/window in game',results=checks),ensure_ascii=False,indent=2)+'\n');print(dict(passed=passed,error=error,checks=len(checks)))
