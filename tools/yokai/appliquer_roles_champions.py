#!/usr/bin/env python3
"""Reapply canonical identity overlays after trainer generation, never changing parties."""
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]

def apply_to_trainers(source):
    config=json.loads((ROOT/'data/yokai/scenario/roles_champions.json').read_text())
    for role in config['roles']:
        pattern=r'(    \['+re.escape(role['trainer'])+r'\] = \{)(.*?)(\n    \},)'
        def replace(m):
            body,n=re.subn(r'\.trainerName = _\("[^"]*"\)',lambda _:'.trainerName = _("'+role['trainer_name']+'")',m[2]);assert n==1
            body,n=re.subn(r'\.trainerPic = \w+',lambda _:'.trainerPic = '+role['trainer_pic'],body);assert n==1
            return m[1]+body+m[3]
        source,n=re.subn(pattern,replace,source,flags=re.S);assert n==1,role['trainer']
    return source

if __name__=='__main__':
    p=ROOT/'src/data/trainers.h';p.write_text(apply_to_trainers(p.read_text()))
