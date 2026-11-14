#!/usr/bin/env python3
"""Installe localement les mondes disponibles, sans ROM et sans génération prétendue à cinq slots."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import zipfile
ROOT=Path(__file__).resolve().parents[1]


def pinned(path, commit):
    actual=subprocess.check_output(['git','-C',str(path),'rev-parse','HEAD'],text=True).strip()
    if actual!=commit:raise ValueError(f'{path.name}: attendu {commit}, reçu {actual}')


def commit_file(src, dest, replace):
    if dest.exists() and hashlib.sha256(src.read_bytes()).digest()!=hashlib.sha256(dest.read_bytes()).digest() and not replace:
        raise ValueError(f'{dest.name} existe déjà avec un autre contenu ; sauvegarder puis utiliser --replace')
    dest.parent.mkdir(parents=True,exist_ok=True)
    if src.resolve()!=dest.resolve():shutil.copy2(src,dest)


def package_world(source, output, package):
    with zipfile.ZipFile(output,'w',zipfile.ZIP_DEFLATED) as z:
        for f in sorted(source.rglob('*')):
            if not f.is_file() or any(p in {'__pycache__','.git'} for p in f.parts):continue
            relative=Path(package)/f.relative_to(source)
            payload=f.read_bytes()
            if f==source/'archipelago.json':
                metadata=json.loads(payload);metadata.update(version=7,compatible_version=7)
                payload=(json.dumps(metadata,indent=2)+'\n').encode()
            info=zipfile.ZipInfo(relative.as_posix(),date_time=(2026,11,14,0,0,0))
            info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16
            z.writestr(info,payload)


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--dependencies',type=Path,required=True)
    p.add_argument('--archipelago',type=Path,required=True)
    p.add_argument('--emerald-apworld',type=Path)
    p.add_argument('--firered-apworld',type=Path)
    p.add_argument('--replace',action='store_true')
    a=p.parse_args(argv)
    if not (a.archipelago/'MultiServer.py').is_file():p.error('Dossier Archipelago invalide')
    deps={e['id']:e for e in json.loads((ROOT/'CONFIG/dependencies.lock.json').read_text())['dependencies']}
    for key in ['archipelago','yokai_watch_2','mario_kart_wii']:
        dep=deps[key];pinned(a.archipelago if key=='archipelago' else a.dependencies/dep['directory'],dep['commit'])
    custom=a.archipelago/'custom_worlds';custom.mkdir(exist_ok=True)
    commit_file(a.dependencies/deps['yokai_watch_2']['directory']/'yokaiwatch2.apworld',custom/'yokaiwatch2.apworld',a.replace)
    with tempfile.TemporaryDirectory() as temp:
        packed=Path(temp)/'mkwii.apworld'
        package_world(a.dependencies/deps['mario_kart_wii']['directory']/'worlds/mkwii',packed,'mkwii')
        commit_file(packed,custom/packed.name,a.replace)
    if a.emerald_apworld:
        with zipfile.ZipFile(a.emerald_apworld) as z:
            md=json.loads(z.read('pokemon_yokai_emerald/archipelago.json'))
            if md['game']!='Pokemon Yo-kai Emerald':raise ValueError('Mauvais monde Emerald')
        commit_file(a.emerald_apworld,custom/'pokemon_yokai_emerald.apworld',a.replace)
    if a.firered_apworld:
        with zipfile.ZipFile(a.firered_apworld) as z:
            md=json.loads(z.read('pokemon_yokai_firered/archipelago.json'))
            profile=json.loads(z.read('pokemon_yokai_firered/build.json'))
            if md['game']!='Pokemon Yo-kai FireRed' or profile['mode']!='surf_randomized':
                raise ValueError('Mauvais monde ou profil Rouge Feu')
        commit_file(a.firered_apworld,custom/'pokemon_yokai_firered.apworld',a.replace)
    lua=a.archipelago/'data/lua'
    for dep in ['base64.lua','json.lua']:
        if not (lua/dep).is_file():raise ValueError(f'Archipelago incomplet : data/lua/{dep}')
    commit_file(ROOT/'CONNECTORS/mgba/connector_bizhawkclient_yokai.lua',lua/'connector_bizhawkclient_yokai.lua',a.replace)
    print('Installés : Yo-kai Watch 2, Mario Kart Wii, connecteur Lua mGBA.')
    print('Emerald : '+('installé depuis votre build personnelle.' if a.emerald_apworld else 'en attente de votre APWorld local.'))
    print('Rouge Feu : '+('jalon Surf installé depuis votre build.' if a.firered_apworld else 'fournir --firered-apworld après compilation locale.'))
    print('Yo-kai Watch 1 : prototype non jouable, exclu de cette installation. Yo-kai Watch 3 abandonné.')
    return 0

if __name__=='__main__':raise SystemExit(main())
