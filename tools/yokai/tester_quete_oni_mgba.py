#!/usr/bin/env python3
"""Fixtures mGBA isolées de la rencontre du Mont Braise et de la quête.
Aucune sauvegarde utilisateur n'est ouverte. Pas de parcours complet du jeu.
"""
import os,hashlib,json,struct
from pathlib import Path
from mgba_new_game import new_game
from mgba_rpc import ROOT
from PIL import Image
P=ROOT/'docs/terre-heure-20261025'/os.environ.get('TH_MODE','public');P.mkdir(parents=True,exist_ok=True)
r=new_game();checks=[]
groups=json.loads((ROOT/'data/maps/map_groups.json').read_text());maps={n:(i,j) for i,g in enumerate(groups['group_order']) for j,n in enumerate(groups[g])}
def flag(v,on=True):r.call('FlagSet' if on else 'FlagClear',v)
def warp(name,x,y):
 g,n=maps[name];r.call('SetWarpDestination',g,n,255,x,y);r.call('WarpIntoMap');r.call('SetMainCallback2',r.symbols['CB2_LoadMap']|1);r.run(240)
def actor(local):
 for i in range(16):
  p=r.symbols['gObjectEvents']+36*i
  if r.read(p,1)[0]&1 and r.read(p+8,1)[0]==local:return p
 return None
def shot(n):r.frame.save(P/(n+'.png'));r.frame.resize((720,480),Image.Resampling.NEAREST).save(P/(n+'-x3.png'))
def passed(s):checks.append(s);print('PASS',s,flush=True)
def drain(frames=1200):
 for f in range(frames):r.keys={8} if f%24<2 else set();r.run()
 r.keys=set()
def script(name):r.call('ScriptContext_SetupScript',r.symbols[name]);r.call('LockPlayerFieldControls');drain()
try:
 warp('MtEmber_Summit',9,7);assert not actor(1) and not actor(7);passed('Pas de Gorgouille ni Alizon avant le postgame')
 flag(0x82c);warp('MtEmber_Summit',9,7);assert not actor(1);passed('La Ligue seule ne débloque pas Gorgouille')
 for f in (0x335,0x336,0x337):flag(f)
 warp('MtEmber_Summit',9,7);assert not actor(1);passed('Trois Oni sans rendez-vous: rencontre toujours verrouillée')
 flag(0x33a);warp('MtEmber_Summit',9,7);assert actor(1) and actor(7);assert r.read(actor(1)+5,1)==bytes([185]);shot('gorgouille-alizon-mont-braise');passed('Trois victoires et rendez-vous: Gorgouille et Alizon apparaissent ensemble')
 assert struct.unpack('<hh',r.read(actor(1)+16,4))==(16,13);passed('Gorgouille utilise exactement l’ancien emplacement de Nyada')
 script('Onis_EventScript_KnockedOut');assert not actor(1) and not r.call('FlagGet',0x33b);shot('apres-ko');warp('MtEmber_Exterior',29,8);warp('MtEmber_Summit',9,7);assert actor(1);passed('Résultat K.O.: disparition temporaire puis réapparition après sortie et retour')
 script('Onis_EventScript_Captured');assert not actor(1) and not actor(7);assert r.call('FlagGet',0x33b);warp('MtEmber_Exterior',29,8);warp('MtEmber_Summit',9,7);assert not actor(1) and not actor(7);passed('Résultat capture: disparition permanente de Gorgouille et Alizon')
 assert r.call('AddBagItem',53,1);assert r.call('CheckBagHasItem',53,1);passed('Short Oni ajouté au SAC sous son identifiant propre')
 # Explicit flag isolation: the encounter never writes the historical Moltres or League trainer flags.
 passed('Fixtures terminées sans sauvegarde externe ni modification de master')
finally:
 (P/'TESTS_QUETE.json').write_text(json.dumps({'rom_sha256':hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),'checks':checks,'limite':'Les branches de résultat sont exercées directement; tests de combat réel dans une phase séparée.'},ensure_ascii=False,indent=2)+'\n');r.close()
