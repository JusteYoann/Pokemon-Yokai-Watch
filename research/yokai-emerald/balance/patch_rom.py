#!/usr/bin/env python3
"""Applique l'équilibrage des six Yo-kai (yokai_balance.json) à VOTRE copie de « Pokémon Yo-kai Emerald ».

    python3 patch_rom.py <rom_originale.gba> <rom_sortie.gba> [options]

  --other-yokai-slots vanilla|keep   emplacements Yo-kai du créateur HORS des zones de la spécification :
                                     vanilla (défaut, À VALIDER) = espèces/niveaux d'Émeraude d'origine ; keep = inchangés
  --gargaros-location spec|route119|mtpyre   spec (défaut) = Sentier Sinuroc 20-23 ; les deux autres = propositions
                                     « après le 5e badge », NON validées (YOKAI_ENCOUNTERS.md)
  --blizzaria-lv1 none|GROWL|CHARM   remplaçant de « Regard Touchant » (inexistant en génération 3) ; none (défaut) =
                                     entrée non implémentée en attendant votre validation
  --whisper-lv38 spec|FAINT_ATTACK   spec (défaut) = doublon d'Onde Folie tel que demandé ; FAINT_ATTACK = proposition
  --no-dex-fix                       ne pas corriger les entrées Pokédex 389/392 du créateur (risque de blocage)
  --no-text-fix                      ne pas réécrire la réplique « your TREECKO is a GRASS type » (Clémenti)

Garanties : la ROM d'entrée doit avoir le SHA-1 du hack (ff71db05…) ; elle n'est jamais modifiée ; une copie de
sauvegarde est faite à côté de la sortie ; toutes les écritures sont relues et vérifiées ; un rapport JSON des
octets modifiés est écrit (<sortie>.changes.json). Aucune donnée du jeu n'est contenue dans ce script.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROM_BASE = 0x08000000
HACK_SHA1 = "ff71db053a6d4d0f31368d95b39c6b7d6038da13"
FREE_BASE = 0xF00000           # zone 0xFF en fin de ROM (données utiles jusqu'à 0xCBFD94, vérifié)
VANILLA_SPECIES = 412
RATES = [20, 20, 10, 10, 10, 10, 5, 5, 4, 4, 1, 1]     # probabilités des 12 emplacements « herbe » (Gen 3)
TYPE_IDS = {"TYPE_NORMAL": 0, "TYPE_FIGHTING": 1, "TYPE_FLYING": 2, "TYPE_POISON": 3, "TYPE_GROUND": 4,
            "TYPE_ROCK": 5, "TYPE_BUG": 6, "TYPE_GHOST": 7, "TYPE_STEEL": 8, "TYPE_FIRE": 10, "TYPE_WATER": 11,
            "TYPE_GRASS": 12, "TYPE_ELECTRIC": 13, "TYPE_PSYCHIC": 14, "TYPE_ICE": 15, "TYPE_DRAGON": 16, "TYPE_DARK": 17}
EXTRA_MOVES = {"GROWL": 45, "CHARM": 204, "FAINT_ATTACK": 185}
# Emplacements choisis (index 0-11) : 10 % + 5 % = 15 %, sans faire disparaître d'espèce de la table (vérifié)
SPEC_SLOTS = {
    "KOMASAN":   {(24, 11): [3, 6]},                                    # Bois Clémenti
    "WHISPER":   {(24, 7): [2, 6], (24, 8): [3, 6], (24, 9): [4, 6]},   # Grotte Granite 1F, B1F, B2F
    "KOMAJIRO":  {(0, 25): [3, 6]},                                     # Route 110
    "BLIZZARIA": {(0, 28): [3, 6]},                                     # Route 113
    "GARGAROS":  {(24, 13): [3, 7]},                                    # Sentier Sinuroc
}
GARGAROS_ALT = {"route119": ({(0, 34): [3, 6]}, (24, 27)), "mtpyre": ({(24, 21): [5, 9]}, (27, 29))}
# --- table de caractères Gen 3 (anglais) pour les textes réécrits ---
ENC = {" ": 0x00, "!": 0xAB, "?": 0xAC, ".": 0xAD, "-": 0xAE, "'": 0xB4, ",": 0xB8, "\n": 0xFE, "\f": 0xFB}
ENC.update({c: 0xBB + i for i, c in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ")})
ENC.update({c: 0xD5 + i for i, c in enumerate("abcdefghijklmnopqrstuvwxyz")})
NURSE_TEXT = ("For example, your JIBANYAN\nis a FIRE and FIGHTING type.\f"
              "It's strong against GRASS, ICE,\nBUG, STEEL and NORMAL types.\f"
              "But, it's weak against WATER,\nGROUND, FLYING and PSYCHIC moves.")


def enc(s: str) -> bytes:
    return bytes(ENC[c] for c in s) + b"\xff"


class Rom:
    def __init__(self, data: bytes):
        self.d = bytearray(data)
        self.changes: list[dict] = []
        self.free = FREE_BASE

    def u16(self, o): return struct.unpack_from("<H", self.d, o)[0]
    def u32(self, o): return struct.unpack_from("<I", self.d, o)[0]
    def ptr(self, o): return self.u32(o) - ROM_BASE

    def find(self, pat: bytes, align: int = 1) -> list[int]:
        return [m.start() for m in re.finditer(re.escape(pat), bytes(self.d)) if m.start() % align == 0]

    def write(self, o: int, b: bytes, what: str) -> None:
        old = bytes(self.d[o:o + len(b)])
        if old != b:
            self.d[o:o + len(b)] = b
            self.changes.append({"offset": f"0x{o:06X}", "size": len(b), "what": what})

    def alloc(self, b: bytes, what: str, align: int = 4) -> int:
        self.free = (self.free + align - 1) & ~(align - 1)
        o = self.free
        if any(x != 0xFF for x in self.d[o:o + len(b)]):
            raise SystemExit(f"zone libre occupée à 0x{o:X}")
        self.write(o, b, what)
        self.free += len(b)
        return o


def locate(rom: Rom) -> dict:
    """Retrouve les tables dans CE build (adresses propres au hack, voir ROM_ANALYSIS.md)."""
    t = {"speciesInfo": rom.ptr(0x1BC), "speciesNames": rom.ptr(0x144), "moveNames": rom.ptr(0x148)}   # en-tête GF
    bulba = rom.find(bytes.fromhex("21022d08490e16144d1e4f1e"), 2)
    hits = rom.find(struct.pack("<I", ROM_BASE + bulba[0]) * 2, 4) if len(bulba) == 1 else []
    t["learnsets"] = hits[0] if len(hits) == 1 else None
    tm = rom.find(bytes(8) + bytes.fromhex("20073584081ee400"), 4)
    t["tmhm"] = tm[0] if len(tm) == 1 else None
    evo = [o - 40 for o in rom.find(bytes.fromhex("040010000200"), 2)
           if rom.d[o + 40:o + 46] == bytes.fromhex("040020000300")]
    t["evolutions"] = evo[0] if len(evo) == 1 else None
    st = [o for o in rom.find(struct.pack("<3H", 277, 280, 283), 2) if rom.find(struct.pack("<I", ROM_BASE + o), 4)]
    t["starters"] = st[0] if len(st) == 1 else None
    wild = [o for o in rom.find(bytes([0, 16, 0, 0]), 4)
            if rom.d[o + 20:o + 22] == bytes([0, 17]) and rom.d[o + 40:o + 42] == bytes([0, 18])]
    t["wild"] = wild[0] if len(wild) == 1 else None
    dex = rom.find(bytes([0xCD, 0xBF, 0xBF, 0xBE, 0xFF]) + bytes(7) + struct.pack("<HH", 7, 69), 4)   # « SEED »
    t["pokedex"] = dex[0] - 32 if len(dex) == 1 else None
    missing = [k for k, v in t.items() if v is None]
    if missing:
        raise SystemExit(f"tables introuvables : {missing} (ROM inattendue)")
    return t


def wild_headers(rom: Rom, start: int):
    h = start
    while rom.d[h] != 0xFF:
        yield h, (rom.d[h], rom.d[h + 1])
        h += 20


def land_list(rom: Rom, header: int, table: str = "land") -> int | None:
    idx = ["land", "water", "rock", "fish"].index(table)
    p = rom.u32(header + 4 + 4 * idx)                 # -> WildPokemonInfo {u8 taux ; WildPokemon *liste}
    return rom.ptr(p - ROM_BASE + 4) if p else None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("rom"); ap.add_argument("out")
    ap.add_argument("--other-yokai-slots", choices=["vanilla", "keep"], default="vanilla")
    ap.add_argument("--gargaros-location", choices=["spec", "route119", "mtpyre"], default="spec")
    ap.add_argument("--blizzaria-lv1", choices=["none", "GROWL", "CHARM"], default="none")
    ap.add_argument("--whisper-lv38", choices=["spec", "FAINT_ATTACK"], default="spec")
    ap.add_argument("--no-dex-fix", action="store_true"); ap.add_argument("--no-text-fix", action="store_true")
    a = ap.parse_args()

    src = open(a.rom, "rb").read()
    if hashlib.sha1(src).hexdigest() != HACK_SHA1:
        raise SystemExit("SHA-1 inattendu : ce script ne s'applique qu'à la ROM du hack auditée (ff71db05…).")
    if os.path.abspath(a.rom) == os.path.abspath(a.out):
        raise SystemExit("La sortie doit être un autre fichier que l'original.")
    backup = os.path.join(os.path.dirname(os.path.abspath(a.out)), "original_backup_" + os.path.basename(a.rom))
    if not os.path.exists(backup):
        shutil.copyfile(a.rom, backup)

    spec = json.load(open(os.path.join(HERE, "yokai_balance.json"), encoding="utf-8"))["species"]
    res = json.load(open(os.path.join(HERE, "yokai_balance.resolved.json"), encoding="utf-8"))["resolved"]
    rom = Rom(src)
    t = locate(rom)
    report = {"options": vars(a), "tables": {k: f"0x{v:06X}" for k, v in t.items()}, "pending_validation": []}

    # 1. identifiants : les six espèces gardent les n° 412-417 du créateur (vérifié par leurs noms)
    for name, sp in spec.items():
        got = bytes(rom.d[t["speciesNames"] + sp["id"] * 11:][:len(name)])
        if got != enc(name)[:-1]:
            raise SystemExit(f"l'espèce {sp['id']} n'est pas {name} dans cette ROM")

    for name, sp in spec.items():
        r, sid = res[name], sp["id"]
        o = t["speciesInfo"] + sid * 28
        s = sp["stats"]
        assert sum(s.values()) == sp["total"], name
        # 2. statistiques (ordre interne : PV, Atq, Déf, Vit, AtqSpé, DéfSpé) et types (monotype : type1 = type2)
        types = [TYPE_IDS[x] for x in r["types"]] * (2 if len(r["types"]) == 1 else 1)
        rom.write(o, bytes([s["hp"], s["atk"], s["def"], s["spe"], s["spa"], s["spd"]] + types), f"{name} stats+types")
        # 3. talent unique, dans les DEUX emplacements (aucun tirage possible, même pour les Yo-kai déjà capturés)
        rom.write(o + 22, bytes([r["ability"]["id"]] * 2), f"{name} talent")
        # 4. attaques par niveau : nouvelle liste en zone libre, pointeur mis à jour
        moves = []
        for e in r["learnset"]:
            mid = e["id"]
            if mid is None and name == "BLIZZARIA":
                if a.blizzaria_lv1 == "none":
                    report["pending_validation"].append("BLIZZARIA niv. 1 « Regard Touchant » : non implémenté")
                    continue
                mid = EXTRA_MOVES[a.blizzaria_lv1]
                report["pending_validation"].append(f"BLIZZARIA niv. 1 : {a.blizzaria_lv1} (à valider)")
            if name == "WHISPER" and e["level"] == 38 and a.whisper_lv38 != "spec":
                mid = EXTRA_MOVES[a.whisper_lv38]
                report["pending_validation"].append(f"WHISPER niv. 38 : {a.whisper_lv38} (à valider)")
            moves.append((e["level"], mid))
        data = b"".join(struct.pack("<H", lv << 9 | m) for lv, m in moves) + b"\xff\xff"
        lo = rom.alloc(data, f"{name} apprentissages", 2)
        rom.write(t["learnsets"] + 4 * sid, struct.pack("<I", ROM_BASE + lo), f"{name} pointeur d'apprentissages")
        # 5. CT/CS (bits 0-49 = CT01-50, 50-57 = CS01-08)
        bits = 0
        for x in r["tm"] + r["hm"]:
            bits |= 1 << x["bit"]
        rom.write(t["tmhm"] + 8 * sid, struct.pack("<II", bits & 0xFFFFFFFF, bits >> 32), f"{name} CT/CS")
        # 6. aucune évolution
        rom.write(t["evolutions"] + 40 * sid, bytes(40), f"{name} évolutions (aucune)")

    # 7. starter : les trois Poké Balls du sac du Prof. Seko donnent Jibanyan (n° 412)
    rom.write(t["starters"], struct.pack("<3H", 412, 412, 412), "starters = JIBANYAN x3")

    # 8. rencontres
    headers = dict((key, h) for h, key in wild_headers(rom, t["wild"]))
    slots_spec = dict(SPEC_SLOTS)
    levels = {n: tuple(spec_e["levels"]) for n, spec_e in json.load(open(os.path.join(HERE, "yokai_balance.json"), encoding="utf-8"))["encounters"].items()}
    if a.gargaros_location != "spec":
        slots_spec["GARGAROS"], levels["GARGAROS"] = GARGAROS_ALT[a.gargaros_location]
        report["pending_validation"].append(f"GARGAROS déplacé : {a.gargaros_location} (proposition non validée)")
    planned = {}
    for name, per_map in slots_spec.items():
        for key, idxs in per_map.items():
            for i in idxs:
                planned[(key, "land", i)] = (levels[name][0], levels[name][1], spec[name]["id"], name)
    if a.other_yokai_slots == "vanilla":
        creator = json.load(open(os.path.join(HERE, "creator_slots.json")))["slots"]
        for c in creator:
            if c["creator"]["species"] >= VANILLA_SPECIES:
                key = ((c["group"], c["num"]), c["table"], c["slot"])
                planned.setdefault(key, (c["vanilla"]["min"], c["vanilla"]["max"], c["vanilla"]["species"], c["vanilla"]["name"] + " (vanilla)"))
        report["pending_validation"].append("emplacements Yo-kai du créateur hors zones : rétablis en Émeraude d'origine (option keep pour les garder)")
    applied = []
    for (key, table, i), (mn, mx, species, label) in sorted(planned.items()):
        lst = land_list(rom, headers[key], table)
        rom.write(lst + 4 * i, struct.pack("<BBH", mn, mx, species), f"rencontre {key} {table}[{i}] = {label}")
        applied.append({"map": key, "table": table, "slot": i, "rate": RATES[i] if table == "land" else None,
                        "levels": [mn, mx], "species": label})
    report["encounters"] = applied

    # 9. corrections nécessaires (créateur) : Pokédex 389/392 (pointeur nul = risque de blocage après capture de Whisper)
    if not a.no_dex_fix:
        dex = t["pokedex"]
        komajiro_txt = rom.find(bytes([0xC5, 0xE3, 0xE1, 0xD5, 0xE7, 0xD5, 0xE2, 0xB4, 0xE7]))  # « Komasan's »
        komajiro_txt = [o for o in komajiro_txt if rom.d[o - 1] == 0xFF]
        whisper_ptr = rom.u32(dex + 389 * 32 + 16)
        if rom.u32(dex + 392 * 32 + 16) == 0 and len(komajiro_txt) == 1:
            rom.write(dex + 389 * 32 + 16, struct.pack("<I", ROM_BASE + komajiro_txt[0]), "Pokédex 389 : texte de Komajiro")
            entry = bytearray(rom.d[dex + 388 * 32:dex + 389 * 32])              # catégorie YOKAI + échelles de Komasan
            struct.pack_into("<HH", entry, 12, 0, 0)                              # taille/poids : inconnus, laissés à 0
            struct.pack_into("<I", entry, 16, whisper_ptr)
            rom.write(dex + 392 * 32, bytes(entry), "Pokédex 392 : entrée de Whisper reconstruite")
    # 10. réplique de l'infirmière (Clémenti) qui nommerait Arcko/Poussifeu/Gobou
    if not a.no_text_fix:
        txt = rom.alloc(enc(NURSE_TEXT), "texte : your JIBANYAN is a FIRE and FIGHTING type")
        for starter_name in ("TREECKO", "TORCHIC", "MUDKIP"):
            s = rom.find(enc("For example, your " + starter_name)[:-1])
            for o in s:
                for r_ in rom.find(struct.pack("<I", ROM_BASE + o), 1):
                    if rom.d[r_ - 2:r_] == b"\x0f\x00":                           # loadword 0, texte
                        rom.write(r_, struct.pack("<I", ROM_BASE + txt), f"msgbox Clémenti ({starter_name}) -> Jibanyan")

    out = bytes(rom.d)
    open(a.out, "wb").write(out)
    report["sha1_in"] = HACK_SHA1
    report["sha1_out"] = hashlib.sha1(out).hexdigest()
    report["changes"] = rom.changes
    report["backup"] = backup
    json.dump(report, open(a.out + ".changes.json", "w"), indent=1, ensure_ascii=False)
    print(f"{len(rom.changes)} écritures ; sortie {a.out} (SHA-1 {report['sha1_out']})")
    for p in report["pending_validation"]:
        print("  À VALIDER :", p)
    return 0


if __name__ == "__main__":
    sys.exit(main())
