#!/usr/bin/env python3
"""Reproduce the completed speech's obsolete tile trigger, or verify the fix.

Completed flag and starting position are explicit fixtures, not a played story.
The old ROM must freeze directions and START at y36 while L help still opens.
"""
import argparse,hashlib,json,struct
from pathlib import Path
from mgba_new_game import new_game
from mgba_rpc import ROOT
from mafiamille_qa import C,MAPS,warp
p=argparse.ArgumentParser();p.add_argument('--avant',action='store_true');p.add_argument('--rapport',type=Path,required=True);a=p.parse_args();a.rapport.mkdir(parents=True,exist_ok=True)
r=new_game();rows={};passed=False

def loc():
 sb=r.u32(r.symbols['gSaveBlock1Ptr']);return tuple(r.read(sb+4,2)),struct.unpack('<hh',r.read(sb,4))
def menu_active():return any(r.read(r.symbols['gTasks']+40*i+4,1)==b'\1' and r.u32(r.symbols['gTasks']+40*i)==r.symbols['Task_StartMenuHandleInput']|1 for i in range(16))
def press(k,n):r.keys={k};r.run(n);r.keys=set();r.run(60)
try:
 r.call('FlagSet',C['FLAG_ARGENTA_MORLEONE_DONE'])
 r.call('CreateMon',r.symbols['gPlayerParty'],1,100,31,1,100,0,0);r.write(r.symbols['gPlayerPartyCount'],b'\1');r.call('VarSet',C['VAR_REPEL_STEP_COUNT'],10000)
 warp(r,*MAPS['PewterCity'],23,34);rows['var_temp_f_after_reload']=r.call('VarGet',0x400F)
 press(5,100);rows['after_south']=loc();r.frame.save(a.rapport/'sortie.png')
 if a.avant:
  assert loc()==(MAPS['PewterCity'],(23,36));fixed=loc()
  for key in (4,5,6,7):press(key,32);assert loc()==fixed
  press(3,1);assert not menu_active();rows['directions_and_start_blocked']=True
  r.call('HelpSystem_Enable');rows['help_enabled_fixture']=True
  press(10,1);rows['help_opens']=bool(r.read(r.symbols['sInHelpSystem'],1)[0]);assert rows['help_opens'];r.frame.save(a.rapport/'aide-L.png')
 else:
  assert loc()[0]==MAPS['Route2'];press(3,1);assert menu_active();rows['start_works']=True
  r.frame.save(a.rapport/'menu.png')
 passed=True
finally:
 if not passed:r.frame.save(a.rapport/'echec.png')
 r.close();(a.rapport/'TEST_MGBA.json').write_text(json.dumps(dict(passed=passed,expected_old_bug=a.avant,rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),scope=__doc__,results=rows),ensure_ascii=False,indent=2)+'\n')
