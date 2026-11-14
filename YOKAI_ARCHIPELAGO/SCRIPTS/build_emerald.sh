#!/usr/bin/env bash
# Construit « Pokémon Yo-kai Emerald » compatible Archipelago, puis l'APWorld, à partir de VOS fichiers.
# Linux ou WSL2 (Ubuntu 24.04) sous Windows. Usage :
#   SCRIPTS/build_emerald.sh <rom_du_hack.gba> <rom_emeraude_de_base.gba> us|fr <dossier_de_travail>
#   - rom_du_hack : « Pokémon Yo-kai Emerald » de SnappleRainKirby (SHA-1 ff71db05…)
#   - rom de base : Émeraude US (SHA-1 f3ae0881…) pour « us », Émeraude France (SHA-1 ca666651…) pour « fr »
# Résultat : <travail>/apworld/pokemon_yokai_emerald.apworld (à copier dans Archipelago/custom_worlds).
# Dépendances : build-essential git libpng-dev binutils-arm-none-eabi gcc-arm-none-eabi nodejs python3-pip ;
#               pip install pillow bsdiff4
set -euo pipefail
HACK=$(realpath "$1"); BASE=$(realpath "$2"); LANG_=$3; WORK=$(realpath -m "$4")
HERE=$(cd "$(dirname "$0")/.." && pwd)
FLIT_BASEPATCH=https://github.com/FlitPix/pokeemerald      # branche combo, commit validé fd64301
FLIT_APWORLD=https://github.com/FlitPix/ap-pokeemerald     # commit validé c62beb1
QIGAST_FR=https://github.com/qigast/pokeemeraude           # commit validé 2ec3c4d9
mkdir -p "$WORK" && cd "$WORK"
[ -d agbcc ] || { git clone -q https://github.com/pret/agbcc && (cd agbcc && ./build.sh); }
[ -d ap-pokeemerald ] || { git clone -q "$FLIT_APWORLD" ap-pokeemerald && git -C ap-pokeemerald checkout -q c62beb1; }
if [ ! -d build ]; then
  git clone -q -b combo "$FLIT_BASEPATCH" build && git -C build checkout -q fd64301
  if [ "$LANG_" = fr ]; then
    # Base française : fusion du code AP de Flit dans la décompilation française (étape à valider sur votre PC)
    git -C build remote add fr "$QIGAST_FR" && git -C build fetch -q fr && git -C build merge --no-edit fr/master \
      || { echo "Conflits de fusion AP × français : voir DOCUMENTATION/chantiers/E_pokemon_yokai_emerald.md"; exit 2; }
  fi
  (cd agbcc && ./install.sh ../build)
  python3 "$HERE/PATCHES/pokemon_yokai_emerald/yokai_source_patch.py" build "$HACK" --lang "$LANG_" --extract-dir yokai_extract
fi
cp "$BASE" build/pokeemerald.gba          # base du différentiel (bsdiff) : votre ROM d'origine
(cd build && make tools -j"$(nproc)" && make -j"$(nproc)" && make extract)
python3 "$HERE/TESTS/verify_emerald_build.py" build/pokeemerald_ap_flit.gba build/pokeemerald_ap_flit.map --hack "$HACK"
python3 "$HERE/APWORLDS/pokemon_yokai_emerald/make_apworld.py" ap-pokeemerald build --base "$LANG_" --out apworld
echo "OK : $WORK/apworld/pokemon_yokai_emerald.apworld"
