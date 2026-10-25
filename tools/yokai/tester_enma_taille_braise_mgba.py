#!/usr/bin/env python3
"""Fixtures isolées mGBA : taille/palette Enma et retrait du caméo au Mont Braise."""
import json,struct,hashlib
from PIL import Image
from postgame_qa_common import QA
from mgba_rpc import ROOT
D=ROOT/'docs/enma-taille-braise-20261025';D.mkdir(exist_ok=True);checks=[]
q=QA('TEMP.json');r=q.r
try:
 q.mon();q.warp('MtEmber_Summit',9,7);r.run(240)
 assert 6 not in q.actors() and 1 not in q.actors()
 q.f(0x82c);q.warp('MtEmber_Summit',9,7);r.run(240);assert 6 not in q.actors()
 for flag in (0x335,0x336,0x337,0x33a):q.f(flag)
 q.warp('MtEmber_Summit',9,7);r.run(240)
 assert 6 not in q.actors() and 1 in q.actors() and 7 in q.actors()
 r.call('ObjectEventTurn',q.actors()[255],2);r.run(8);r.frame.save(D/'mont-braise-gorgouille-alizon.png')
 checks.append('Mont Braise avant/après Ligue : Enma absent ; après les prérequis Oni, Gorgouille et Alizon restent présents')
 # Emulate a legacy live object before the return-to-field callback.
 r.call('FlagClear',0x304);r.call('TrySpawnObjectEvent',6,q.maps['MtEmber_Summit'][1],q.maps['MtEmber_Summit'][0])
 assert 6 in q.actors();q.script('MtEmber_Summit_OnResume');r.run(30);assert 6 not in q.actors()
 checks.append('Un ancien objet Enma déjà chargé est également retiré au retour terrain, sans décaler les identifiants des autres PNJ')
 q.warp('CeruleanCave_B1F',7,13);r.run(300);assert 3 in q.actors()
 actor=q.actors()[3];sid=r.read(actor+4,1)[0];bank=r.read(r.symbols['gSprites']+68*sid+5,1)[0]>>4
 assert r.read(r.symbols['gPlttBufferUnfaded']+512+32*bank,32)==r.read(r.symbols['gObjectEventPal_YokaiEnma'],32)
 tiles=(ROOT/'graphics/yokai_characters/enma/overworld.4bpp').read_bytes();assert r.read(r.symbols['gObjectEventPic_YokaiEnma'],len(tiles))==tiles
 r.call('ObjectEventTurn',q.actors()[255],2);r.run(8);r.frame.save(D/'enma-grotte-azuree.png')
 im=Image.open(ROOT/'graphics/yokai_characters/enma/overworld.png').convert('RGBA');front=im.crop((0,0,16,32)).getchannel('A').getbbox()
 n=Image.open(ROOT/'graphics/yokai_characters/nathan/normal.png').convert('RGBA').crop((0,0,16,32)).getchannel('A').getbbox()
 assert front[2]-front[0]==n[2]-n[0]==12
 assert front[3]-front[1]>=n[3]-n[1]
 checks.append('Grotte Azurée : Enma royal présent, bons graphismes et bonne palette, largeur frontale 12 px comme Nathan, hauteur visible '+str(front[3]-front[1])+' px contre '+str(n[3]-n[1]))
 q.warp('PalletTown_PlayersHouse_1F',6,6);q.warp('PalletTown',6,7);r.run(60);r.frame.save(D/'enma-introduction-postgame.png')
 assert q.local('LOCALID_PG_ENMA_INTRO') in q.actors();checks.append('Le même grand sprite royal reste présent dans l’introduction du postgame')
finally:r.close()
(D/'TESTS_MGBA.json').write_text(json.dumps(dict(passed=True,scope=__doc__,rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),checks=checks),ensure_ascii=False,indent=2)+'\n');print('PASS Enma, Mont Braise, Gorgouille et introduction',flush=True)
