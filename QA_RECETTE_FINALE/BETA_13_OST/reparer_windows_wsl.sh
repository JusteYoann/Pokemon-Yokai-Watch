#!/usr/bin/env bash
# Repair the existing diagnosed B13 build. No full game/audio rebuild.
set -euo pipefail
if (( $# > 2 )); then
  echo "Usage: bash $0 [dossier-de-compilation [dossier-de-sortie]]" >&2; exit 2
fi
if (( $# == 0 )); then
  # Select only when exactly one known B13 build is found. Never guess between builds.
  work=$(python3 - <<'PYAUTO'
import hashlib
from pathlib import Path
import sys
known = {'505eabc4470f967aa2d6c6441f923dfa0ea530a16008de8b41a1bcfda1287b79', '36bbf1f1c759f0e355be122caf68d7d110f86c83c1862bda1e85c72ea37abfc5'}
found = [p.parent.parent for p in Path.home().glob('yokai-beta-b13.*/sources/pokefirered_audio.gba') if hashlib.sha256(p.read_bytes()).hexdigest() in known]
if len(found) != 1:
    print('Indiquer explicitement le dossier conserve. Candidats :', *map(str,found), sep='\n', file=sys.stderr)
    raise SystemExit(2)
print(found[0])
PYAUTO
)
else
  work=$(realpath -e "$1")
fi
output=${2:-/mnt/c/YokaiBeta}
test -f "$work/sources/pokefirered_audio.gba"
mkdir -p "$work/repair-tools" "$output"
python3 - "$work/repair-tools" <<'PY'
from pathlib import Path
import sys, urllib.request
root = 'https://raw.githubusercontent.com/JusteYoann/Pokemon-Yokai-Watch/dev/reconstruction-finalisation/'
files = ['tools/yokai/diagnostiquer_beta_b13.py', 'tools/yokai/normaliser_bibliotheques_b13.py',
         'tools/yokai/reparer_beta_b13.py', 'QA_RECETTE_FINALE/BETA_13_OST/REFERENCE_B13_DIAGNOSTIC.json',
         'QA_RECETTE_FINALE/BETA_13_OST/BIBLIOTHEQUES_B13_LOCK.json']
for relative in files:
    with urllib.request.urlopen(root + relative, timeout=60) as response:
        Path(sys.argv[1], relative.rsplit('/', 1)[1]).write_bytes(response.read())
PY
source "$work/outils/env.sh"
source "$work/venv/bin/activate"
python "$work/repair-tools/reparer_beta_b13.py" --work "$work" --output-dir "$output" --reference "$work/repair-tools/REFERENCE_B13_DIAGNOSTIC.json" --lock "$work/repair-tools/BIBLIOTHEQUES_B13_LOCK.json"
printf '\nOuvrir dans mGBA : %s/pokemon-yokai-BETA-B13-20261018.gba\n' "$output"
