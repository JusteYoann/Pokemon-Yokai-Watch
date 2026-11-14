#!/usr/bin/env python3
"""Fabrique l'APWorld « Pokemon Yo-kai Emerald » à partir du monde de Flit (MIT) et de VOTRE build.

    python3 make_apworld.py <ap-pokeemerald (FlitPix, c62beb1)> <build_dir> --base us|fr --out <dossier>

<build_dir> : la décompilation AP compilée par build_emerald.sh (contient base_patch.bsdiff4 et extracted_data.json).
--base us : ROM de base attendue = Pokémon Émeraude US (MD5 605b89b6…) ; --base fr = Émeraude France (MD5 2c00e335…).
Sortie : <out>/pokemon_yokai_emerald.apworld (à copier dans Archipelago/custom_worlds). Le patch de base contient des
graphismes du créateur du hack : NE PAS publier ce fichier (usage personnel).

Modifications du monde de Flit (toutes listées dans le README de ce dossier) :
- nom de jeu « Pokemon Yo-kai Emerald », nom de ROM « pokemon emerald / yokai ap v0.1 », extension .apyokaiemerald,
  clé de réglages pokemon_yokai_emerald_settings (pour coexister avec le monde de Flit et le monde officiel) ;
- hash de la ROM de base selon --base ;
- 6 Yo-kai ajoutés à ALL_SPECIES (n° nationaux 387-392) ;
- données (base_patch.bsdiff4, extracted_data.json) remplacées par celles de votre build.
Le monde de Flit n'a pas d'option de randomisation des starters ni des rencontres : Jibanyan et les zones des Yo-kai
restent ceux du patch, quelle que soit la graine.
"""
import argparse
import os
import re
import shutil
import zipfile

MD5 = {"us": "605b89b67018abcea91e693a4dd25be3", "fr": "2c00e335288a96650e34785b5e2a7588"}
YOKAI = [("SPECIES_JIBANYAN", "Jibanyan", 387), ("SPECIES_KOMASAN", "Komasan", 388), ("SPECIES_KOMAJIRO", "Komajiro", 389),
         ("SPECIES_BLIZZARIA", "Blizzaria", 390), ("SPECIES_GARGAROS", "Gargaros", 391), ("SPECIES_WHISPER", "Whisper", 392)]
PKG = "pokemon_yokai_emerald"


def sub_once(text, old, new, path):
    if text.count(old) < 1:
        raise SystemExit(f"{path}: motif introuvable {old!r}")
    return text.replace(old, new)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("flit"); ap.add_argument("build")
    ap.add_argument("--base", choices=["us", "fr"], required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    work = os.path.join(a.out, PKG)
    shutil.rmtree(work, ignore_errors=True)
    shutil.copytree(a.flit, work, ignore=shutil.ignore_patterns(".git", ".github", "__pycache__", "test", "*.md"))
    for d in ("docs",):
        shutil.rmtree(os.path.join(work, d), ignore_errors=True)

    def edit(rel, pairs):
        p = os.path.join(work, rel); t = open(p, encoding="utf-8").read()
        for old, new in pairs:
            t = sub_once(t, old, new, rel)
        open(p, "w", encoding="utf-8").write(t)

    edit("constants.py", [('GAME_NAME = "Pokemon Emerald Version - Flit\'s ver."', 'GAME_NAME = "Pokemon Yo-kai Emerald"'),
                          ('ROM_NAME = "pokemon emerald / flit ap v0.1"', 'ROM_NAME = "pokemon emerald / yokai ap v0.1"'),
                          ('ROM_HASH = "605b89b67018abcea91e693a4dd25be3"', f'ROM_HASH = "{MD5[a.base]}"')])
    edit("archipelago.json", [("\"Pokemon Emerald Version - Flit's ver.\"", '"Pokemon Yo-kai Emerald"')])
    edit("rom.py", [('patch_file_ending = ".apemeraldflit"', 'patch_file_ending = ".apyokaiemerald"'),
                    ("pokemon_emerald_flit_settings", "pokemon_yokai_emerald_settings")])
    edit("world.py", [('settings_key = "pokemon_emerald_flit_settings"', 'settings_key = "pokemon_yokai_emerald_settings"')])
    p = os.path.join(work, "data.py"); t = open(p, encoding="utf-8").read()
    t = sub_once(t, '    ("SPECIES_CHIMECHO", "Chimecho", 358),\n]',
                 '    ("SPECIES_CHIMECHO", "Chimecho", 358),\n' + "".join(f'    ("{c}", "{n}", {k}),\n' for c, n, k in YOKAI) + "]", "data.py")
    open(p, "w", encoding="utf-8").write(t)
    # réglage de la ROM de base : message adapté
    p = os.path.join(work, "world.py"); t = open(p, encoding="utf-8").read()
    t = re.sub(r'description = "[^"]*"', f'description = "Pokemon Emerald ({"US" if a.base == "us" else "France"}) ROM File"', t, count=1)
    open(p, "w", encoding="utf-8").write(t)
    for f in ("base_patch.bsdiff4", "extracted_data.json"):
        shutil.copyfile(os.path.join(a.build, f), os.path.join(work, "data", f))
    out = os.path.join(a.out, PKG + ".apworld")
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for root, _, files in os.walk(work):
            for f in files:
                full = os.path.join(root, f)
                z.write(full, os.path.relpath(full, a.out))
    print("APWorld :", out)


if __name__ == "__main__":
    main()
