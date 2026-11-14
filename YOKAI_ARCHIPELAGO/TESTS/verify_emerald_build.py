#!/usr/bin/env python3
"""Vérifie une ROM « Pokémon Yo-kai Emerald » COMPILÉE (décompilation + yokai_source_patch.py) contre les fiches validées.

    python3 verify_emerald_build.py <rom.gba> <rom.map> [--hack <rom_du_hack.gba>]

Lit les tables via les symboles du .map (aucune adresse supposée). Contrôles : stats/types/talents, attaques,
CT/CS, absence d'évolution, noms, Pokédex (n° nationaux, description non vide), starter ×3, rencontres
(zones, niveaux, taux 10-20 %), et avec --hack : sprites de face/dos/palettes identiques au hack.
"""
import json
import os
import re
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BAL = os.path.join(HERE, "..", "..", "research", "yokai-emerald", "balance")
B = 0x08000000
RATES = [20, 20, 10, 10, 10, 10, 5, 5, 4, 4, 1, 1]
ORDER = ["JIBANYAN", "KOMASAN", "KOMAJIRO", "BLIZZARIA", "GARGAROS", "WHISPER"]
TID = {"NORMAL": 0, "FIGHTING": 1, "ROCK": 5, "GHOST": 7, "FIRE": 10, "ELECTRIC": 13, "ICE": 15, "DARK": 17}
DEC = {0x00: " ", 0xAE: "-", 0xB4: "'"}
DEC.update({0xBB + i: c for i, c in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ")})
res_ok = []


def ok(name, cond, detail=""):
    res_ok.append(bool(cond))
    print(f"[{'OK' if cond else 'ÉCHEC'}] {name}" + (f" — {detail}" if detail else ""))


def lz10(d, o):
    size = d[o + 1] | d[o + 2] << 8 | d[o + 3] << 16; o += 4; out = bytearray()
    while len(out) < size:
        fl = d[o]; o += 1
        for b in range(8):
            if len(out) >= size: break
            if fl & (0x80 >> b):
                x = d[o] << 8 | d[o + 1]; o += 2
                for _ in range((x >> 12) + 3): out.append(out[-((x & 0xFFF) + 1)])
            else:
                out.append(d[o]); o += 1
    return bytes(out)


def main(rom_path, map_path, hack=None):
    R = open(rom_path, "rb").read()
    sym = {}
    for line in open(map_path):
        m = re.match(r"\s+0x([0-9a-f]{8})\s+(\w+)\s*$", line)
        if m:
            sym.setdefault(m.group(2), int(m.group(1), 16) - B)
    spec = json.load(open(os.path.join(BAL, "yokai_balance.json"), encoding="utf-8"))
    res = json.load(open(os.path.join(BAL, "yokai_balance.resolved.json"), encoding="utf-8"))["resolved"]
    u16 = lambda o: struct.unpack_from("<H", R, o)[0]
    u32 = lambda o: struct.unpack_from("<I", R, o)[0]
    # taille d'une entrée d'évolution selon le compilateur (agbcc : 6 octets ; modern : 8) -> déduite de Bulbizarre
    ev = sym["gEvolutionTable"]
    evo_stride = 30 if R[ev + 30:ev + 36] == bytes.fromhex("040010000200") else 40
    for i, n in enumerate(ORDER):
        sid, sp, r = 412 + i, spec["species"][n], res[n]
        name = "".join(DEC.get(b, "?") for b in R[sym["gSpeciesNames"] + 11 * sid:][:11].split(b"\xff")[0])
        ok(f"{n} nom", name == n, name)
        o = sym["gSpeciesInfo"] + 28 * sid
        hp, at, df, spe, sa, sd, t1, t2 = R[o:o + 8]
        s = sp["stats"]
        ok(f"{n} stats", (hp, at, df, sa, sd, spe) == (s["hp"], s["atk"], s["def"], s["spa"], s["spd"], s["spe"]),
           f"{hp}/{at}/{df}/{sa}/{sd}/{spe} = {hp+at+df+sa+sd+spe}")
        want = [TID[x[5:]] for x in r["types"]]
        ok(f"{n} types", [t1, t2] == (want * 2 if len(want) == 1 else want), f"{t1},{t2}")
        ok(f"{n} talent unique", R[o + 22] == R[o + 23] == r["ability"]["id"], f"{R[o+22]},{R[o+23]}")
        lp = u32(sym["gLevelUpLearnsets"] + 4 * sid) - B
        got = []
        while u16(lp) != 0xFFFF:
            w = u16(lp); got.append((w >> 9, w & 0x1FF)); lp += 2
        want_ls = [(e["level"], e["id"] if e["id"] is not None else 45) for e in r["learnset"]]   # Regard Touchant -> Rugissement (45)
        ok(f"{n} attaques", got == want_ls, f"{len(got)} attaques")
        tm = sym.get("sTMHMLearnsets", sym.get("gTMHMLearnsets"))
        bits = u32(tm + 8 * sid) | u32(tm + 8 * sid + 4) << 32
        ok(f"{n} CT/CS", bits == sum(1 << x["bit"] for x in r["tm"] + r["hm"]))
        ok(f"{n} sans évolution", R[ev + evo_stride * sid:][:evo_stride] == bytes(evo_stride))
        dex = sym["gPokedexEntries"] + 32 * (387 + i)
        ok(f"{n} Pokédex {387+i}", u32(dex + 16) >= B and R[u32(dex + 16) - B] != 0xFF)
        if hack:
            H = open(hack, "rb").read()
            for label, off in (("face", 0x128), ("dos", 0x12C), ("palette", 0x130)):
                a = lz10(R, u32(u32(off) - B + 8 * sid) - B)
                b = lz10(H, struct.unpack_from("<I", H, struct.unpack_from("<I", H, off)[0] - B + 8 * sid)[0] - B)
                ok(f"{n} graphisme {label} identique au hack", a == b)
    # starter : sStarterMon est statique ; on lit le littéral de GetStarterPokemon
    f = sym["GetStarterPokemon"] & ~1
    lits = [u32(f + k) for k in range(0, 0x40, 4) if B <= u32(f + k) < B + 0x2000000]
    arr = lits[0] - B if lits else None
    ok("starter = JIBANYAN ×3", arr is not None and struct.unpack_from("<3H", R, arr) == (412, 412, 412))
    # rencontres
    h = sym["gWildMonHeaders"]; found = {}
    while R[h] != 0xFF:
        p = u32(h + 4)
        if p:
            lst = u32(p - B + 4) - B
            for k in range(12):
                mn, mx, s_ = struct.unpack_from("<BBH", R, lst + 4 * k)
                if s_ >= 412:
                    found.setdefault(ORDER[s_ - 412], {}).setdefault((R[h], R[h + 1]), []).append((k, mn, mx))
        h += 20
    for n, e in spec["encounters"].items():
        zones = found.get(n, {})
        lv = tuple(e["levels"])
        good = zones and all(10 <= sum(RATES[k] for k, _, _ in v) <= 20 and all((mn, mx) == lv for _, mn, mx in v) for v in zones.values())
        ok(f"rencontres {n}", good and len(zones) == len(e["maps"]),
           "; ".join(f"{z}: {sum(RATES[k] for k,_,_ in v)} %, niv. {v[0][1]}-{v[0][2]}" for z, v in zones.items()))
    ok("aucun Yo-kai hors de ses zones", "JIBANYAN" not in found)
    print(f"\n{sum(res_ok)}/{len(res_ok)} contrôles réussis")
    return 0 if all(res_ok) else 1


if __name__ == "__main__":
    args = sys.argv[1:]
    hack = None
    if "--hack" in args:
        i = args.index("--hack"); hack = args[i + 1]; del args[i:i + 2]
    if len(args) != 2:
        sys.exit(__doc__)
    sys.exit(main(args[0], args[1], hack))
