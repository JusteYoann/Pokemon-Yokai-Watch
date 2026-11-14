#!/usr/bin/env bash
# Build local uniquement : jamais de téléchargement de ROM/graphismes/musiques.
set -euo pipefail
if [[ $# -ne 3 ]]; then
    echo "Usage: bash $0 <sources_RC1_completes> <agbcc_compile> <nouveau_dossier_sortie>" >&2
    exit 2
fi
project_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
rc1_source="$(realpath "$1")"
compiler_source="$(realpath "$2")"
build_target="$(realpath -m "$3")"
for command_name in python3 make gcc arm-none-eabi-as arm-none-eabi-ld arm-none-eabi-nm; do
    command -v "$command_name" >/dev/null || { echo "Outil manquant : $command_name" >&2; exit 2; }
done
[[ -f "$compiler_source/install.sh" && -f "$compiler_source/agbcc" ]] || {
    echo "Compiler agbcc d'abord, puis fournir son dossier source." >&2; exit 2;
}
python3 "$project_root/PATCHES/pokemon_yokai_firered/prepare_source.py" --source "$rc1_source" --output "$build_target"
(cd "$compiler_source" && bash ./install.sh "$build_target")
make -C "$build_target" -j4
python3 "$project_root/PATCHES/pokemon_yokai_firered/export_profile.py" \
    "$build_target/pokefirered_audio.gba" "$build_target/pokefirered_audio.elf" --out "$build_target/build.json"
python3 "$project_root/APWORLDS/pokemon_yokai_firered/make_apworld.py" \
    --profile "$build_target/build.json" --out "$build_target/dist"
sha256sum "$build_target/pokefirered_audio.gba"
echo "ROM et package AP locaux dans $build_target ; ne pas publier la ROM."
