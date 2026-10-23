"""QA continuation into unmodified Hall of Fame, credits and Flash reload.

Caller has won the diagnostic boss. The pending artistic conclusion is bypassed
by an explicit QA warp, not by a production script or an invented dialogue.
"""
from mafiamille_qa import MAPS,C,warp

def check_hof(r,Q):
 r.call('FlagSet',C['FLAG_DEFEATED_CHAMP'])
 warp(r,*MAPS['PokemonLeague_HallOfFame'],5,12)
 seen_hof=False;seen_credits=False;states=set()
 for f in range(42000):
  r.keys={8} if f%16<4 else set();r.run();cb=r.u32(r.symbols['gMain']+4)
  if cb==r.symbols['CB2_HofIdle']|1:
   if not seen_hof:r.frame.save(Q/'pantheon-natif.png')
   seen_hof=True
  if cb==r.symbols['CB2_Credits']|1:
   seen_credits=True;mgr=r.u32(r.symbols['sCreditsMgr'])
   if mgr:
    state=r.read(mgr,1)[0]
    if state not in states and state in [0,17,18]:r.frame.save(Q/f'credits-{state}.png')
    states.add(state)
  if seen_credits and cb!=r.symbols['CB2_Credits']|1:break
 else:raise AssertionError(('Hall of Fame/credits timeout',seen_hof,seen_credits,states))
 assert seen_hof and seen_credits and {17,18}<=states
 r.keys=set();r.run(1200)
 for f in range(7000):
  r.keys={3} if f%120<2 else {8} if f%120 in [60,61] else set();r.run()
  if f>120 and r.u32(r.symbols['gMain']+4)==r.symbols['CB2_Overworld']|1 and r.read(r.symbols['gQuestLogState'],1)[0] not in [2,3]:break
 else:raise AssertionError('Continue after native Hall of Fame save failed')
 assert r.call('FlagGet',C['FLAG_SYS_GAME_CLEAR'])
 r.keys=set();r.run(180);r.frame.save(Q/'postgame-apres-continue.png')
 return dict(test='QA warp after diagnostic boss victory, native Hall of Fame/credits 17/18, Flash save and real Continue to postgame',passed=True,credits_states=sorted(states),production_conclusion_tested=False)
