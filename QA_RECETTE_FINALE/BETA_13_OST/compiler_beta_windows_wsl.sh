#!/usr/bin/env bash
# Run in Debian 13 amd64 under WSL. No protected resource is downloaded.
set -euo pipefail
if (( $# != 2 )); then
  echo "Usage: bash $0 /mnt/c/YokaiBeta/archives /mnt/c/YokaiBeta" >&2
  exit 2
fi
archives_dir=$(realpath -e "$1")
mkdir -p "$2"
output_dir=$(realpath -e "$2")
source /etc/os-release
[[ "$ID" == debian && "$VERSION_ID" == 13 && "$(dpkg --print-architecture)" == amd64 ]] || {
  echo 'Utiliser Debian 13 amd64 (WSL2), pour la chaine reproductible validee.' >&2; exit 1;
}
shopt -s nullglob
archives=("$archives_dir"/*.rar "$archives_dir"/*.RAR)
(( ${#archives[@]} > 0 )) || { echo 'Aucune archive RAR dans le dossier fourni.' >&2; exit 1; }
# Do not reuse or overwrite another checkout or an earlier attempt.
work=$(mktemp -d "$HOME/yokai-beta-b13.XXXXXXXX")
printf 'Dossier de travail conserve : %s\n' "$work"
on_error() {
  status=$?
  printf 'En cas dechec, conserver ce dossier pour diagnostic : %s\n' "$work" >&2
  if [[ -f "$work/diagnostic-tools/diagnostiquer_beta_b13.py" && -f "$work/sources/pokefirered_audio.gba" && -f "$work/sources/pokefirered_audio.elf" ]]; then
    python "$work/diagnostic-tools/diagnostiquer_beta_b13.py" --work "$work" --reference "$work/diagnostic-tools/REFERENCE_B13_DIAGNOSTIC.json" --output "$output_dir/diagnostic-b13.json" || printf 'Le diagnostic automatique a aussi echoue ; conserver le dossier complet.\n' >&2
  fi
  exit "$status"
}
trap on_error ERR
sudo apt-get update
sudo apt-get install -y git build-essential zlib1g-dev python3 python3-venv libarchive13t64 'ffmpeg=7:7.1.5-0+deb13u1'
git clone --branch dev/reconstruction-finalisation https://github.com/JusteYoann/Pokemon-Yokai-Watch.git "$work/sources"
cd "$work/sources"
# Latest tested B13 checkpoint; subsequent delivery docs do not alter the ROM.
git checkout --detach ff1cb36b2ecbe7b8ce167e375a6bff378df31347
# Delivery diagnostics come from the fetched branch, outside the pinned checkout.
mkdir -p "$work/diagnostic-tools"
git show origin/dev/reconstruction-finalisation:tools/yokai/diagnostiquer_beta_b13.py > "$work/diagnostic-tools/diagnostiquer_beta_b13.py"
git show origin/dev/reconstruction-finalisation:QA_RECETTE_FINALE/BETA_13_OST/REFERENCE_B13_DIAGNOSTIC.json > "$work/diagnostic-tools/REFERENCE_B13_DIAGNOSTIC.json"
git show origin/dev/reconstruction-finalisation:tools/yokai/normaliser_bibliotheques_b13.py > "$work/diagnostic-tools/normaliser_bibliotheques_b13.py"
git show origin/dev/reconstruction-finalisation:QA_RECETTE_FINALE/BETA_13_OST/BIBLIOTHEQUES_B13_LOCK.json > "$work/diagnostic-tools/BIBLIOTHEQUES_B13_LOCK.json"
export YOKAI_SETUP_DIR="$work/outils"
bash RECUPERATION_PROJET/scripts/configurer_outils_debian.sh
source "$YOKAI_SETUP_DIR/env.sh"
# The pinned ff1 checkout predates the installer fix: normalize both its cached
# runtime and installed archives without changing any source or member bytes.
python3 "$work/diagnostic-tools/normaliser_bibliotheques_b13.py" --lib-dir "$YOKAI_SETUP_DIR/agbcc" --lock "$work/diagnostic-tools/BIBLIOTHEQUES_B13_LOCK.json"
python3 "$work/diagnostic-tools/normaliser_bibliotheques_b13.py" --lib-dir "$work/sources/tools/agbcc/lib" --lock "$work/diagnostic-tools/BIBLIOTHEQUES_B13_LOCK.json"

python3 -m venv "$work/venv"
source "$work/venv/bin/activate"
python -m pip install -r tools/yokai/requirements-audio.txt
python tools/yokai/extraire_audio_prive.py --output "$work/audio-prive/extracted" "${archives[@]}"
python tools/yokai/preparer_ost_dpcm.py --extracted-manifest "$work/audio-prive/extracted/manifest-private.json" --private-output "$work/audio-prive/sources" --jobs 4
python tools/yokai/generer_audio_prive.py --full-source-dir "$work/audio-prive/sources" --output "$work/audio-prive/integration" --jobs 4
make -j4 YOKAI_AUDIO_DIR="$work/audio-prive/integration"
python - "$output_dir" <<'PY'
import hashlib, json, pathlib, shutil, sys
rom = pathlib.Path('pokefirered_audio.gba')
expected = '36bbf1f1c759f0e355be122caf68d7d110f86c83c1862bda1e85c72ea37abfc5'
actual = hashlib.sha256(rom.read_bytes()).hexdigest()
if actual != expected or rom.stat().st_size != 24400776:
    raise SystemExit(f'ARRET : ROM differente ({actual}, {rom.stat().st_size} octets). Ne pas ignorer ce controle.')
out = pathlib.Path(sys.argv[1])/'pokemon-yokai-BETA-B13-20261018.gba'
# Preserve any existing ROM; a byte-identical output is already complete.
if out.exists():
    if hashlib.sha256(out.read_bytes()).hexdigest() != expected:
        raise SystemExit(f'ARRET : fichier de sortie existant different, non ecrase : {out}')
else:
    shutil.copyfile(rom, out)
metadata = {'version':'BETA-B13-20261018','checkpoint':'ff1cb36b2ecbe7b8ce167e375a6bff378df31347','bytes':24400776,'sha256':actual,'active_ost':13,'final_release':False}
out.with_suffix('.manifest.json').write_text(json.dumps(metadata,indent=2)+'\n')
print(f'PRET A OUVRIR DANS mGBA : {out}\nSHA-256 : {actual}')
PY
