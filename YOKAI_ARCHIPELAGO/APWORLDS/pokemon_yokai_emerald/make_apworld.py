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
import hashlib
import json
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
    if os.path.realpath(work) in (os.path.realpath(a.flit), os.path.realpath(a.build)):
        raise SystemExit("La sortie ne doit pas remplacer les sources ou la compilation.")
    for required in ("base_patch.bsdiff4", "extracted_data.json"):
        if not os.path.isfile(os.path.join(a.build, required)):
            raise SystemExit(f"Compilation incomplète : {required} manquant.")
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
    # The client is registered independently from the procedure patch. Both must
    # use our extension, and Steven's goal must reference the defined flag.
    edit("client.py", [('patch_suffix = ".apemeraldflit"', 'patch_suffix = ".apyokaiemerald"'),
                       ('FLAG_IS_CHAMPION = data.constants["TRAINER_FLAGS_START"] + data.constants["FLAG_IS_CHAMPION"]',
                        'FLAG_IS_CHAMPION = data.constants["FLAG_IS_CHAMPION"]'),
                       ('self.goal_flags.add(FLAG_DEFEATED_WALLACE)', 'self.goal_flags.add(FLAG_DEFEATED_STEVEN)'),
                       ('if not ctx.finished_game and self.goal_flags == self.checked_goal_flags:',
                        'if self.goal_flags and not ctx.finished_game and self.goal_flags == self.checked_goal_flags:')])
    # Do not write a gift after the save block moved or the player left the
    # overworld between the preceding read and the actual write. Publish the
    # full flag last, after the payload and item classification are complete.
    edit("client.py", [('''            await bizhawk.write(ctx.bizhawk_ctx, [
                (received_item_address + 0, (next_item.item).to_bytes(2, "little"), "System Bus"),
                (received_item_address + 2, (num_received_items + 1).to_bytes(2, "little"), "System Bus"),
                (received_item_address + 4, [1], "System Bus"),
                (received_item_address + 5, [classification], "System Bus"),
            ])''', '''            await bizhawk.guarded_write(ctx.bizhawk_ctx, [
                (received_item_address + 0, (next_item.item).to_bytes(2, "little"), "System Bus"),
                (received_item_address + 2, (num_received_items + 1).to_bytes(2, "little"), "System Bus"),
                (received_item_address + 5, [classification], "System Bus"),
                (received_item_address + 4, [1], "System Bus"),
            ], [guards["IN OVERWORLD"], guards["SAVE BLOCK 1"],
                (sb1_address + 0x3700, read_result[0], "System Bus"),
                (received_item_address + 4, [0], "System Bus")])''')])
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
    manifest_path = os.path.join(work, "archipelago.json")
    with open(manifest_path, encoding="utf-8") as stream:
        manifest = json.load(stream)
    manifest.update(compatible_version=7, version=7)
    with open(manifest_path, "w", encoding="utf-8") as stream:
        json.dump(manifest, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
    with open(os.path.join(work, "yokai_build.json"), "w", encoding="utf-8") as stream:
        json.dump({"base": a.base, "rom_md5": MD5[a.base], "game": "Pokemon Yo-kai Emerald",
                   "inputs": {f: hashlib.sha256(open(os.path.join(a.build, f), "rb").read()).hexdigest()
                              for f in ("base_patch.bsdiff4", "extracted_data.json")}}, stream, indent=2)
        stream.write("\n")
    out = os.path.join(a.out, PKG + ".apworld")
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for root, dirs, files in os.walk(work):
            dirs.sort()
            for f in sorted(files):
                full = os.path.join(root, f)
                z.write(full, os.path.relpath(full, a.out))
    print("APWorld :", out)


if __name__ == "__main__":
    main()
