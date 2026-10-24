#!/usr/bin/env python3
"""Regression: complete speech, nurse care, museum admission, south exit and return."""
import os
from mgba_rpc import ROOT
os.environ.setdefault('YOKAI_ARGENTA_REPORT_DIR','docs/argenta-retour-route2-20261024/apres/'+('fille' if os.environ.get('YOKAI_ARGENTA_GENDER')=='1' else 'garcon'))
p=ROOT/'tools/yokai/tester_argenta_mgba.py'
s=p.read_text()
check=r'''  def sb():return r.u32(r.symbols['gSaveBlock1Ptr'])
  def pos():return struct.unpack('<hh',r.read(sb(),4))
  def walk(key,frames):
   r.keys={key};r.run(frames);r.keys=set();r.run(24)
  def visit_exit(mapname,x,y,frames):
   warp(r,*MAPS[mapname],x,y)
   walk(5,frames);r.run(300)
   assert tuple(r.read(sb()+4,2))==MAPS['PewterCity'],('Building exit',mapname,pos())
   assert r.call('VarGet',0x400F)==1,('Entrance should be disabled after building visit',mapname)
  # Native nurse interaction, then actual door exit. Only pre-positioning is a fixture.
  r.call('CreateMon',r.symbols['gPlayerParty'],1,5,31,1,100,0,0)
  r.write(r.symbols['gPlayerPartyCount'],b'\x01')
  warp(r,*MAPS['PewterCity_PokemonCenter_1F'],7,4)
  walk(4,1)
  before_heals=r.call('GetGameStat',C['GAME_STAT_USED_POKECENTER'])
  began=False
  for f in range(4000):
   r.keys={8} if f%16<4 else set();r.run()
   status=r.read(r.symbols['sGlobalScriptContextStatus'],1)[0]
   if status!=2:began=True
   if began and status==2:break
  else:raise AssertionError('Nurse dialogue timeout')
  r.keys=set();r.run(60)
  assert r.call('GetGameStat',C['GAME_STAT_USED_POKECENTER'])==before_heals+1
  r.frame.save(P/f'{entry}-soins.png')
  walk(5,110);r.run(300)
  assert tuple(r.read(sb()+4,2))==MAPS['PewterCity'],'Centre door exit failed'
  assert r.call('VarGet',0x400F)==1,'Entrance rearmed after Centre'
  # Paid museum visit: enter the real ticket trigger and accept the dialogue.
  warp(r,*MAPS['PewterCity_Museum_1F'],14,6)
  walk(4,16)
  began=False
  for f in range(3000):
   r.keys={8} if f%16<4 else set();r.run()
   status=r.read(r.symbols['sGlobalScriptContextStatus'],1)[0]
   if status!=2:began=True
   if began and status==2:break
  else:raise AssertionError('Museum ticket timeout')
  r.keys=set();r.run(60)
  assert r.call('VarGet',C['VAR_MAP_SCENE_PEWTER_CITY_MUSEUM_1F'])==1,'Museum admission failed'
  r.frame.save(P/f'{entry}-musee.png')
  visit_exit('PewterCity_Museum_1F',14,8,32)
  # Suppress incidental wild encounters on grass columns of Route2.
  # This fixture isolates controls/scene reentry, not encounter behavior.
  r.call('CreateMon',r.symbols['gPlayerParty'],1,100,31,1,100,0,0)
  r.call('VarSet',C['VAR_REPEL_STEP_COUNT'],10000)
  # From south of the buildings, cross the formerly looping row, by input only.
  warp(r,*MAPS['PewterCity'],entry,34)
  walk(5,150)
  assert tuple(r.read(sb()+4,2))==MAPS['Route2'],('South exit blocked',pos())
  r.frame.save(P/f'{entry}-retour-route2.png')
  def menu():
   r.keys={3};r.run();r.keys=set();r.run(90)
   assert any(r.read(r.symbols['gTasks']+40*i+4,1)==b'\x01' and r.u32(r.symbols['gTasks']+40*i)==r.symbols['Task_StartMenuHandleInput']|1 for i in range(16)), 'START menu failed'
   r.frame.save(P/f'{entry}-menu-route2.png')
   r.keys={0};r.run();r.keys=set();r.run(90)
  menu()
  # Walk well past y36 on the way back, not merely across the map connection.
  walk(4,180)
  assert tuple(r.read(sb()+4,2))==MAPS['PewterCity'] and pos()[1]<35,('North return blocked',pos())
  r.frame.save(P/f'{entry}-retour-argenta.png')
  # Re-arm a stale, already-loaded coordinate trigger: its guard must consume it.
  for completed,pending in [(True,False),(False,False)]:
   warp(r,*MAPS['PewterCity'],entry,34)
   r.call('FlagSet' if completed else 'FlagClear',C['FLAG_ARGENTA_MORLEONE_DONE'])
   r.call('FlagClear',C['FLAG_ARGENTA_MORLEONE_PENDING'])
   r.call('VarSet',0x400F,0)
   walk(5,150)
   assert tuple(r.read(sb()+4,2))==MAPS['Route2'],('Obsolete guard loop',completed,pos())
   menu()
'''
s=s.replace('  rows.append(dict(entry=entry',check+'  rows.append(dict(centre_heal=True,museum_admission=True,return_route2=True,start_menu=True,north_past_trigger=True,stale_guards=True,entry=entry')
s=s.replace('scope=__doc__',"scope='Speech, Centre healing, museum ticket, Route2 exit, START and return beyond trigger row'")
exec(compile(s,str(p),'exec'))
