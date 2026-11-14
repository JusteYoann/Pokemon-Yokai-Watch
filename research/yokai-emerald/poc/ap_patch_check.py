"""Test RÉEL : le patch Archipelago Pokémon Émeraude (.apemerald) accepte-t-il une ROM donnée ?

    cd <Archipelago> && python <ce fichier> <fichier.apemerald> <rom1.gba> [<rom2.gba> ...] [--out DIR]

Pour chaque ROM : (1) validation officielle d'Archipelago (MD5 attendu par le réglage rom_file du monde),
(2) application de la procédure du patch (bsdiff4 + jetons) même si (1) échoue, pour observer le résultat,
(3) contrôle du nom AP écrit en 0x108 et comparaison avec la ROM vanilla attendue.
Aucune ROM n'est produite hors du dossier --out (local, jamais versionné).
"""
import hashlib, sys, os, argparse
sys.path.insert(0, os.getcwd())
os.environ.setdefault("SKIP_REQUIREMENTS_UPDATE", "1")
import worlds  # noqa: F401  (enregistre les mondes)
from worlds.pokemon_emerald import PokemonEmeraldSettings
from worlds.pokemon_emerald.rom import PokemonEmeraldProcedurePatch

ap = argparse.ArgumentParser(); ap.add_argument("patch"); ap.add_argument("roms", nargs="+"); ap.add_argument("--out", default="patched")
a = ap.parse_args(); os.makedirs(a.out, exist_ok=True)
print("MD5 attendu par le monde :", PokemonEmeraldProcedurePatch.hash)
for rom in a.roms:
    data = open(rom, "rb").read(); md5 = hashlib.md5(data).hexdigest()
    print(f"\n== {os.path.basename(rom)}  md5={md5}")
    try:
        PokemonEmeraldSettings.PokemonEmeraldRomFile.validate(rom); print("  validation Archipelago : ACCEPTÉE")
    except Exception as e:
        print("  validation Archipelago : REFUSÉE ->", type(e).__name__, str(e)[:120])
    patch = PokemonEmeraldProcedurePatch(path=a.patch); patch.read()
    PokemonEmeraldProcedurePatch.get_source_data = classmethod(lambda cls, d=data: d)
    PokemonEmeraldProcedurePatch.source_data = data   # Files.py garde la 1re ROM en cache (get_source_data_with_cache)
    out = os.path.join(a.out, os.path.basename(rom) + ".ap.gba")
    try:
        patch.patch(out); res = open(out, "rb").read()
        print("  procédure appliquée ; nom en 0x108 :", res[0x108:0x128].rstrip(b"\0"), " taille", len(res))
    except Exception as e:
        print("  procédure ÉCHOUÉE ->", type(e).__name__, str(e)[:160])
