#!/usr/bin/env python3
"""Vérifie les archives musicales privées d'origine sans les copier dans Git."""
import argparse
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('asset_dir', type=Path)
args = parser.parse_args()
directory = args.asset_dir.resolve()
if directory.is_relative_to(root):
    parser.error('Conserver les enregistrements hors du checkout public.')
manifest = json.loads((root/'RECUPERATION_PROJET/REFERENCES_AUDIO_EXTERNES.json').read_text())
failures = []
for record in manifest['archives']:
    path = directory/record['archive']
    if (not path.is_file() or path.stat().st_size != record['size']
            or hashlib.sha256(path.read_bytes()).hexdigest() != record['sha256']):
        failures.append(record['archive'])
if failures:
    raise SystemExit('Archives absentes ou differentes : ' + ', '.join(failures))
print(f"{len(manifest['archives'])} archives privees verifiees ; aucune integration musicale executee.")
