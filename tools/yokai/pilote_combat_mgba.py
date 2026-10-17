#!/usr/bin/env python3
"""Controller-only move selection for native fixtures, including exhausted/blocked PP.

RAM is read to observe the UI. No enemy team, PP, cursor or battle outcome is
written by this driver. Native CheckMoveLimitations supplies the legal choices.
"""
import json,subprocess
from mgba_rpc import ROOT

def battle_keys(r,frame):
 if not hasattr(r,'qa_move_callbacks'):
  r.qa_move_callbacks=set()
  for line in subprocess.check_output(['arm-none-eabi-nm','--defined-only','pokefirered.elf'],cwd=ROOT,text=True).splitlines():
   f=line.split()
   if len(f)==3 and f[2]=='HandleInputChooseMove':r.qa_move_callbacks.add(int(f[0],16)|1)
  assert r.qa_move_callbacks
  r.qa_fallbacks=[];r.qa_next_keys={8}
 if frame%16==0:
  r.qa_next_keys={8}
  if r.u32(r.symbols['gBattlerControllerFuncs']) in r.qa_move_callbacks:
   r.keys=set();mask=r.call('CheckMoveLimitations',0,0,255)&15
   choices=[i for i in range(4) if not(mask&(1<<i))]
   if choices:
    target=choices[0];current=r.read(r.symbols['gMoveSelectionCursor'],1)[0]
    if target!=current:
     r.qa_next_keys={7 if target&1 else 6} if (target&1)!=(current&1) else {5 if target&2 else 4}
     item={'loop_iteration':frame,'from_slot':current,'to_slot':target,'unusable_mask':mask,'pp':list(r.read(r.symbols['gBattleMons']+0x24,4))}
     if mask&1:r.qa_fallbacks.append(item)
 return r.qa_next_keys if frame%16<4 else set()

def capture_failure(r,stem):
 p=ROOT/'QA_RECETTE_FINALE/RECONSTRUCTION/preuves';r.frame.save(p/(stem+'-echec-pilote.png'))
 state={'callback2':hex(r.u32(r.symbols['gMain']+4)),'battle_controller':hex(r.u32(r.symbols['gBattlerControllerFuncs'])),'outcome':r.read(r.symbols['gBattleOutcome'],1)[0],'move_cursor':r.read(r.symbols['gMoveSelectionCursor'],1)[0],
        'battle_mons':[{'species':int.from_bytes(r.read(r.symbols['gBattleMons']+88*i,2),'little'),'hp':int.from_bytes(r.read(r.symbols['gBattleMons']+88*i+0x28,2),'little'),'pp':list(r.read(r.symbols['gBattleMons']+88*i+0x24,4)),'moves':[int.from_bytes(r.read(r.symbols['gBattleMons']+88*i+0xC+j*2,2),'little') for j in range(4)]} for i in [0,1]],'fallbacks':getattr(r,'qa_fallbacks',[])}
 (p/(stem+'-echec-pilote.json')).write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n')
 return state
