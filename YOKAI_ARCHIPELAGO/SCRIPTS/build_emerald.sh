#!/usr/bin/env bash
# Sources et assets personnels uniquement locaux. Voir DOCUMENTATION/INSTALLATION_PC_FR.md.
set -euo pipefail
if [[ ${1:-} == --help ]]; then
  echo 'Usage: build_emerald.sh <hack.gba> <base.gba> us|fr <dossier_de_travail>'
  exit 0
fi
if [[ $# != 4 ]]; then
  echo 'Usage: build_emerald.sh <hack.gba> <base.gba> us|fr <dossier_de_travail>' >&2
  exit 2
fi
HACK=$(realpath "$1"); BASE=$(realpath "$2"); LANG_=$3; WORK=$(realpath -m "$4")
HERE=$(cd "$(dirname "$0")/.." && pwd)
# No build directory, checkout, copy, or download before validating both inputs.
INPUT_STATE=$(python3 "$HERE/SCRIPTS/emerald_inputs.py" "$HACK" "$BASE" "$LANG_" "$WORK")
case "$LANG_" in us) SOURCE_LANG=en;; fr) SOURCE_LANG=fr;; *) exit 2;; esac
lock_value() {
  python3 - "$HERE/CONFIG/dependencies.lock.json" "$1" "$2" <<'PY'
import json,sys
entries=json.load(open(sys.argv[1]))['dependencies']
print(next(e[sys.argv[3]] for e in entries if e['id']==sys.argv[2]))
PY
}
ensure_repo() {
  local path=$1 key=$2 url commit
  url=$(lock_value "$key" url); commit=$(lock_value "$key" commit)
  if [[ ! -e "$path" ]]; then git clone --filter=blob:none "$url" "$path"; fi
  [[ -d "$path/.git" ]] || { echo "Dossier non Git existant : $path" >&2; exit 2; }
  [[ -z $(git -C "$path" status --porcelain --untracked-files=no) ]] || {
    echo "Sources modifiées, arrêt pour les préserver : $path" >&2; exit 2; }
  git -C "$path" cat-file -e "$commit^{commit}" 2>/dev/null || git -C "$path" fetch origin "$commit"
  git -C "$path" checkout --detach "$commit"
}
mkdir -p "$WORK"
printf '%s\n' "$INPUT_STATE" > "$WORK/.yokai_build_inputs.json"
ensure_repo "$WORK/agbcc" agbcc
if [[ ! -x "$WORK/agbcc/agbcc" || ! -f "$WORK/agbcc/libc.a" ]]; then (cd "$WORK/agbcc" && bash ./build.sh); fi
ensure_repo "$WORK/ap-pokeemerald" emerald_apworld
if [[ ! -d "$WORK/build" ]]; then
  if [[ "$LANG_" == fr ]]; then
    ensure_repo "$WORK/ap-source" emerald_ap_code
    ensure_repo "$WORK/fr-source" emerald_fr
    python3 "$HERE/PATCHES/pokemon_yokai_emerald/merge_french_base.py" \
      --ap-source "$WORK/ap-source" --fr-source "$WORK/fr-source" --output "$WORK/build"
  else
    ensure_repo "$WORK/build" emerald_ap_code
  fi
  (cd "$WORK/agbcc" && bash ./install.sh "$WORK/build")
  python3 "$HERE/PATCHES/pokemon_yokai_emerald/yokai_source_patch.py" "$WORK/build" "$HACK" \
    --lang "$SOURCE_LANG" --extract-dir "$WORK/yokai_extract"
  touch "$WORK/build/.yokai_source_ready"
fi
cp "$BASE" "$WORK/build/pokeemerald.gba"
JOBS=${YOKAI_BUILD_JOBS:-4}
(cd "$WORK/build" && make tools -j"$JOBS" && make -j"$JOBS" && make extract)
python3 "$HERE/TESTS/verify_emerald_build.py" "$WORK/build/pokeemerald_ap_flit.gba" "$WORK/build/pokeemerald_ap_flit.map" --hack "$HACK"
python3 "$HERE/APWORLDS/pokemon_yokai_emerald/make_apworld.py" "$WORK/ap-pokeemerald" "$WORK/build" \
  --base "$LANG_" --out "$WORK/apworld"
echo "OK : $WORK/apworld/pokemon_yokai_emerald.apworld (fichier personnel, ne pas committer)"
