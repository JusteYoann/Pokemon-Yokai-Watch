#!/usr/bin/env python3
"""Enquête Ariane: carte et prérequis préparés, vraie scène, vrai combat duo et fuite des sbires."""
import json,hashlib
from postgame_qa_common import QA
from mafiamille_qa import strong_party
from observer_collisions_cinematiques import Observer
q=QA('TEMP_ENQUETE.json');r=q.r;monitor=None
try:
 strong_party(r);r.call('VarSet',0x40f4,1)
 monitor=Observer(r,'enquete');q.warp('VermilionCity_PhilosovniWarehouse',6,9)
 q.drain(12000);q.script('Philosovni_Overhear');q.wait(lambda:q.callback()=='BattleMainCB2',30000);q.drain(90000)
 assert r.call('VarGet',0x40f4)==3
 result=monitor.finish();monitor=None;assert not result['suspects'],result['suspects']
 result.update(passed=True,rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),scope=__doc__)
 (q.P.parent/'cinematiques-collisions-20261025/ENQUETE_MGBA.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print('PASS scène Ariane, combat duo et départ des sbires',flush=True)
finally:
 if monitor:monitor.finish()
 r.close()
