#!/usr/bin/env python3
"""Native battle opening captures for original adventure cameo trainer portraits."""
import hashlib,json,re
from mgba_rpc import Emulator,ROOT
P=ROOT/'QA_RECETTE_FINALE/RECONSTRUCTION/preuves';results=[]
glyphs={m[1]:int(m[2],16) for m in re.finditer(r"^'(.*?)'\s*= ([0-9A-F]{2})$",(ROOT/'charmap.txt').read_text(),re.M)}
for person,trainer,gender in [('nathaniel',8,0),('michael',10,1),('wyatt',12,0),('domniscian',14,0),('employe_rouge',15,0),('employe_bleu',16,0),('don_morleone',17,0),('mafiamille_1',18,0),('mafiamille_2',19,0),('mafiamille_3',20,0)]:
 r=Emulator()
 try:
  r.call('SetSaveBlocksPointers');r.call('Sav2_ClearSetDefault');r.call('CB2_NewGame');r.run(180)
  r.write(r.u32(r.symbols['gSaveBlock2Ptr']),bytes(glyphs[c] for c in 'Test')+b'\xff');r.write(r.u32(r.symbols['gSaveBlock2Ptr'])+8,bytes([gender]))
  r.call('CreateMon',r.symbols['gPlayerParty'],1,30,31,1,100,0,0);r.write(r.symbols['gPlayerPartyCount'],b'\x01')
  r.w32(r.symbols['gTrainerBattleOpponent_A'],trainer);r.call('StartTrainerBattle');r.run(401)
  r.frame.save(P/('cameo-'+person+'-portrait-combat.png'))
  results.append({'person':person,'trainer_id':trainer,'test':'Real battle opening captured at401frames; battle completions are in TEST_CAMEOS_AVENTURE_MGBA.json / TEST_CAMEOS_BOSS_MGBA.json','capture':'cameo-'+person+'-portrait-combat.png','passed':True})
 finally:r.close()
report={'engine':'mGBA libretro','rom_sha256':hashlib.sha256((ROOT/'pokefirered.gba').read_bytes()).hexdigest(),'scope':'Direct battle-entry fixtures for visual inspection of trainer portrait and player back; these three specific battles are not completed here','results':results}
(ROOT/'QA_RECETTE_FINALE/RECONSTRUCTION/TEST_PORTRAITS_CAMEOS_MGBA.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False,indent=2))
