#!/usr/bin/env python3
"""Valide les fichiers personnels et l'état de reprise avant toute création de build."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path

HACK_SHA1='ff71db053a6d4d0f31368d95b39c6b7d6038da13'
BASE_SHA1={'us':'f3ae088181bf583e55daf962a92bb46f4f1d07b7',
           'fr':'ca666651374d89ca439007bed54d839eb7bd14d0'}
ROOT=Path(__file__).resolve().parents[2]


def verify_file(path,expected,label):
    if not path.is_file():raise ValueError(f'{label} manquant : {path}')
    actual=hashlib.sha1(path.read_bytes()).hexdigest()
    if actual!=expected:raise ValueError(f'{label}: SHA-1 {actual}, attendu {expected}')
    return actual


def validate(hack,base,language,work):
    if language not in BASE_SHA1:raise ValueError('Langue : us ou fr')
    state={'language':language,'hack_sha1':verify_file(hack,HACK_SHA1,'Hack Yo-kai Emerald'),
           'base_sha1':verify_file(base,BASE_SHA1[language],'Émeraude de base'),
           'source_patch_sha256':hashlib.sha256((ROOT/'YOKAI_ARCHIPELAGO/PATCHES/pokemon_yokai_emerald/yokai_source_patch.py').read_bytes()).hexdigest(),
           'build_version':2}
    work=work.resolve()
    if work==ROOT or ROOT.is_relative_to(work) or work in (hack.resolve(),base.resolve()):
        raise ValueError('Choisir un dossier de travail séparé des sources et des fichiers personnels')
    marker=work/'.yokai_build_inputs.json'
    if marker.exists() and json.loads(marker.read_text())!=state:
        raise ValueError('Ce dossier contient une autre version/langue/ROM : choisir un nouveau dossier de travail')
    if (work/'build').exists() and not (work/'build/.yokai_source_ready').is_file():
        raise ValueError('Build incomplète sans marqueur source : conserver son diagnostic et choisir un nouveau dossier')
    return state


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('hack',type=Path);p.add_argument('base',type=Path)
    p.add_argument('language',choices=['us','fr']);p.add_argument('work',type=Path)
    a=p.parse_args(argv)
    try:state=validate(a.hack,a.base,a.language,a.work)
    except (ValueError,OSError) as e:p.exit(2,str(e)+'\n')
    print(json.dumps(state,indent=2))

if __name__=='__main__':main()
