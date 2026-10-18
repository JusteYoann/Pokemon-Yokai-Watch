#!/usr/bin/env bash
# Diagnose an existing build only. No build, checkout change or ROM patch.
set -euo pipefail
if (( $# < 1 || $# > 2 )); then
  echo "Usage: bash $0 /home/yoann/yokai-beta-b13.XXXXXXXX [/mnt/c/YokaiBeta/diagnostic-b13.json]" >&2
  exit 2
fi
work=$(realpath -e "$1")
output=${2:-/mnt/c/YokaiBeta/diagnostic-b13.json}
test -f "$work/sources/pokefirered_audio.gba" || { echo 'ROM introuvable dans sources/ de ce dossier.' >&2; exit 1; }
mkdir -p "$(dirname "$output")" "$work/diagnostic-tools"
# Download only public diagnostic code/hash metadata over verified HTTPS.
python3 - "$work/diagnostic-tools" <<'PY'
from pathlib import Path
import sys, urllib.request
root = 'https://raw.githubusercontent.com/JusteYoann/Pokemon-Yokai-Watch/dev/reconstruction-finalisation/'
for relative in ['tools/yokai/diagnostiquer_beta_b13.py', 'QA_RECETTE_FINALE/BETA_13_OST/REFERENCE_B13_DIAGNOSTIC.json']:
    with urllib.request.urlopen(root + relative, timeout=60) as response:
        Path(sys.argv[1], relative.rsplit('/', 1)[1]).write_bytes(response.read())
PY
source "$work/outils/env.sh"
source "$work/venv/bin/activate"
python "$work/diagnostic-tools/diagnostiquer_beta_b13.py" --work "$work" --reference "$work/diagnostic-tools/REFERENCE_B13_DIAGNOSTIC.json" --output "$output"
printf '\nJoindre uniquement ce rapport JSON a la conversation : %s\n' "$output"
