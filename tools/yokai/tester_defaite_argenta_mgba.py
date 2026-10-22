#!/usr/bin/env python3
"""Native trainer-defeat expansion via GetTrainerALoseText; no battle traversal."""
import argparse, hashlib, json, os
from pathlib import Path
from mgba_new_game import new_game
from mgba_rpc import ROOT

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output',required=True)
parser.add_argument('--expect-overflow',action='store_true')
args=parser.parse_args()
r=new_game()
try:
    # Exactly the normal defeat-message route: battle placeholder -> field expansion
    # in GetTrainerALoseText -> copy into gDisplayedStringBattle.
    r.w32(r.symbols['sTrainerADefeatSpeech'],r.symbols['PewterCity_Gym_Text_BrockDefeat'])
    source=r.PARAMS+128
    r.write(source,b'\xfd\x24\xff')
    adjacent=r.symbols['gBattleTextBuff1']
    canary=bytes([0xAB])*48
    r.write(adjacent,canary)
    size=r.call('BattleStringExpandPlaceholdersToDisplayedString',source)
    changed=r.read(adjacent,48)!=canary
    result=dict(rom_sha256=hashlib.sha256(Path(os.environ['YOKAI_QA_ROM']).read_bytes()).hexdigest(),
        scope=__doc__,pipeline='B_TRAINER1_LOSE_TEXT -> GetTrainerALoseText/StringExpandPlaceholders -> gDisplayedStringBattle',
        battle_buffer_capacity=300,expanded_bytes_including_eos=size,
        adjacent_buffer_changed=changed,bug_reproduced=changed)
    Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
    assert changed==args.expect_overflow,result
    assert args.expect_overflow or size<=300,result
    print(json.dumps(result),flush=True)
finally:r.close()
