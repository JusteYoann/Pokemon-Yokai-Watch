"""Applique un .apyokaiemerald comme le fait Archipelago (procédure du monde), à partir d'une ROM de base donnée.

    cd <Archipelago> && python <ce fichier> <fichier.apyokaiemerald> <rom_de_base.gba> <sortie.gba>

La ROM de base doit être celle attendue par le monde (Émeraude US, ou France selon --base de make_apworld.py) :
le MD5 est contrôlé comme le ferait le réglage rom_file d'Archipelago.
"""
import hashlib
import os
import sys

sys.path.insert(0, os.getcwd())
os.environ.setdefault("SKIP_REQUIREMENTS_UPDATE", "1")
import worlds  # noqa: F401  (charge custom_worlds)
from worlds.pokemon_yokai_emerald.rom import PokemonEmeraldFlitProcedurePatch as P
from worlds.pokemon_yokai_emerald.constants import ROM_HASH

patch_file, base, out = sys.argv[1:4]
data = open(base, "rb").read()
md5 = hashlib.md5(data).hexdigest()
print("MD5 de la base :", md5, "| attendu :", ROM_HASH, "->", "OK" if md5 == ROM_HASH else "REFUS")
if md5 != ROM_HASH:
    sys.exit(1)
P.get_source_data = classmethod(lambda cls: data)
P.source_data = data
p = P(path=patch_file)
p.read()
p.patch(out)
r = open(out, "rb").read()
print("ROM écrite :", out, "| nom :", r[0x108:0x128].rstrip(b"\0").decode())
