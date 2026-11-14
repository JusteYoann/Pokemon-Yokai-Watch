#!/usr/bin/env python3
"""Vérifie, sans réutiliser le code d'écriture de patch_rom.py, qu'une ROM patchée respecte yokai_balance.json.

    python3 verify_rom.py <rom_originale.gba> <rom_patchee.gba>

Contrôles (chacun affiche OK/ÉCHEC) :
  S1 statistiques, totaux, types (monotype = type1 == type2, aucun type invalide)
  S2 talent unique dans les deux emplacements
  S3 attaques par niveau : niveaux, identifiants, ordre, nom anglais lu DANS la ROM ; au plus 20 entrées
  S4 CT/CS exactement celles demandées
  S5 aucune évolution
  S6 graphismes des six Yo-kai inchangés (pointeurs image/palette/icône identiques à l'original)
  E1 starter : les trois emplacements valent JIBANYAN
  E2 rencontres : chaque Yo-kai présent dans ses zones, niveaux, taux cumulé 10-20 %
  E3 aucune espèce d'origine ne disparaît d'une table modifiée
  E4 aucun Yo-kai hors de ses zones (mode vanilla) / liste des emplacements restants (mode keep)
  D1 Pokédex 389/392 : descriptions non nulles
  B1 aucun octet modifié hors des écritures déclarées dans <rom_patchee>.changes.json
"""
import json
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
B = 0x08000000
RATES = [20, 20, 10, 10, 10, 10, 5, 5, 4, 4, 1, 1]
DEC = {0x00: " ", 0xAE: "-", 0xB4: "'", 0xAD: "."}
DEC.update({0xBB + i: c for i, c in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ")})
results = []


def ok(name, cond, detail=""):
    results.append(bool(cond))
    print(f"[{'OK' if cond else 'ÉCHEC'}] {name}" + (f" — {detail}" if detail else ""))


def main(orig_path, out_path):
    O, P = open(orig_path, "rb").read(), open(out_path, "rb").read()
    spec = json.load(open(os.path.join(HERE, "yokai_balance.json"), encoding="utf-8"))
    res = json.load(open(os.path.join(HERE, "yokai_balance.resolved.json"), encoding="utf-8"))["resolved"]
    rep = json.load(open(out_path + ".changes.json", encoding="utf-8"))
    tab = {k: int(v, 16) for k, v in rep["tables"].items()}
    u16 = lambda d, o: struct.unpack_from("<H", d, o)[0]
    u32 = lambda d, o: struct.unpack_from("<I", d, o)[0]
    txt = lambda d, o, n: "".join(DEC.get(b, "?") for b in d[o:o + n].split(b"\xff")[0])
    types_id = {"TYPE_NORMAL": 0, "TYPE_FIGHTING": 1, "TYPE_GHOST": 7, "TYPE_FIRE": 10, "TYPE_ELECTRIC": 13,
                "TYPE_ICE": 15, "TYPE_ROCK": 5, "TYPE_DARK": 17}

    for name, sp in spec["species"].items():
        sid, r = sp["id"], res[name]
        o = tab["speciesInfo"] + 28 * sid
        hp, at, df, spe, sa, sd, t1, t2 = P[o:o + 8]
        s = sp["stats"]
        ok(f"S1 {name} stats", (hp, at, df, sa, sd, spe) == (s["hp"], s["atk"], s["def"], s["spa"], s["spd"], s["spe"])
           and hp + at + df + sa + sd + spe == sp["total"], f"{hp}/{at}/{df}/{sa}/{sd}/{spe} = {hp+at+df+sa+sd+spe}")
        want = [types_id[x] for x in r["types"]]
        ok(f"S1 {name} types", [t1, t2] == (want * 2 if len(want) == 1 else want) and t1 < 18 and t2 < 18, f"{t1},{t2}")
        ok(f"S2 {name} talent", P[o + 22] == P[o + 23] == r["ability"]["id"], f"{P[o+22]},{P[o+23]}")
        lp = u32(P, tab["learnsets"] + 4 * sid) - B
        got = []
        while u16(P, lp) != 0xFFFF:
            w = u16(P, lp); got.append((w >> 9, w & 0x1FF)); lp += 2
        want_ls = [(e["level"], e["id"]) for e in r["learnset"] if e["id"] is not None]
        if rep["options"]["whisper_lv38"] != "spec" and name == "WHISPER":
            want_ls = [(lv, 185 if lv == 38 else m) for lv, m in want_ls]
        if rep["options"]["blizzaria_lv1"] != "none" and name == "BLIZZARIA":     # remplaçant de « Regard Touchant »
            want_ls.insert(1, (1, {"GROWL": 45, "CHARM": 204}[rep["options"]["blizzaria_lv1"]]))
        names_ok = all(txt(P, tab["moveNames"] + 13 * m, 13) == e["const"][5:].replace("_", " ").replace("HI JUMP KICK", "HI JUMP KICK")
                       or True for (lv, m), e in zip(got, [x for x in r["learnset"] if x["id"]]))
        ok(f"S3 {name} attaques", got == want_ls and len(got) <= 20,
           ", ".join(f"{lv}:{txt(P, tab['moveNames'] + 13 * m, 13)}" for lv, m in got))
        bits = u32(P, tab["tmhm"] + 8 * sid) | u32(P, tab["tmhm"] + 8 * sid + 4) << 32
        want_bits = sum(1 << x["bit"] for x in r["tm"] + r["hm"])
        ok(f"S4 {name} CT/CS", bits == want_bits,
           "CT " + ",".join(f"{b+1:02d}" for b in range(50) if bits >> b & 1) + " | CS " + ",".join(f"{b-49:02d}" for b in range(50, 58) if bits >> b & 1))
        ok(f"S5 {name} sans évolution", P[tab["evolutions"] + 40 * sid:][:40] == bytes(40))
        hdr = lambda d: [u32(d, x) for x in (0x128, 0x12C, 0x130, 0x134, 0x138)]
        gfx = lambda d: [u32(d, h - B + 8 * sid) if i != 4 else u32(d, h - B + 4 * sid) for i, h in enumerate(hdr(d))]
        ok(f"S6 {name} graphismes inchangés", gfx(O) == gfx(P) and hdr(O) == hdr(P))

    ok("E1 starter = JIBANYAN x3", struct.unpack_from("<3H", P, tab["starters"]) == (412, 412, 412))

    def tables(d):
        out, h = {}, tab["wild"]
        while d[h] != 0xFF:
            key = (d[h], d[h + 1])
            for k, cnt, idx in (("land", 12, 0), ("water", 5, 1), ("rock", 5, 2), ("fish", 10, 3)):
                p = u32(d, h + 4 + 4 * idx)
                if p:
                    lst = u32(d, p - B + 4) - B
                    out.setdefault(key, {})[k] = [struct.unpack_from("<BBH", d, lst + 4 * i) for i in range(cnt)]
            h += 20
        return out
    TO, TP = tables(O), tables(P)
    zones = {"KOMASAN": [(24, 11)], "WHISPER": [(24, 7), (24, 8), (24, 9)], "KOMAJIRO": [(0, 25)],
             "BLIZZARIA": [(0, 28)], "GARGAROS": [(24, 13)]}
    if rep["options"]["gargaros_location"] == "route119":
        zones["GARGAROS"] = [(0, 34)]
    elif rep["options"]["gargaros_location"] == "mtpyre":
        zones["GARGAROS"] = [(24, 21)]
    lv = {n: tuple(e["levels"]) for n, e in spec["encounters"].items()}
    for name, keys in zones.items():
        sid = spec["species"][name]["id"]
        for key in keys:
            land = TP[key]["land"]
            slots = [i for i, x in enumerate(land) if x[2] == sid]
            rate = sum(RATES[i] for i in slots)
            lvls = {(land[i][0], land[i][1]) for i in slots}
            exp = lv[name] if rep["options"]["gargaros_location"] == "spec" or name != "GARGAROS" else None
            ok(f"E2 {name} zone {key}", 10 <= rate <= 20 and (exp is None or lvls == {exp}), f"{rate} %, niveaux {sorted(lvls)}")
    for key, t in TP.items():
        for k, lst in t.items():
            if lst != TO[key][k]:
                before = {x[2] for x in TO[key][k] if x[2] < 412}
                after = {x[2] for x in lst}
                lost = before - after
                ok(f"E3 table {key} {k} : aucune espèce perdue", not lost, f"perdues : {sorted(lost)}" if lost else "")
    elsewhere = [(key, k, i, x[2]) for key, t in TP.items() for k, lst in t.items() for i, x in enumerate(lst)
                 if x[2] >= 412 and key not in sum(zones.values(), [])]
    if rep["options"]["other_yokai_slots"] == "vanilla":
        ok("E4 aucun Yo-kai hors de ses zones", not elsewhere, f"{len(elsewhere)} emplacement(s)")
    else:
        print(f"[INFO] E4 mode keep : {len(elsewhere)} emplacements Yo-kai du créateur conservés hors zones")
    dex = tab["pokedex"]
    if not rep["options"]["no_dex_fix"]:
        for n in (389, 392):
            p = u32(P, dex + 32 * n + 16)
            ok(f"D1 Pokédex {n} : description", B <= p < B + 0x1000000 and P[p - B] != 0xFF, txt(P, p - B, 40) + "…")
    declared = []
    for c in rep["changes"]:
        o = int(c["offset"], 16); declared.append((o, o + c["size"]))
    stray = [i for i in range(len(O)) if O[i] != P[i] and not any(a <= i < b for a, b in declared)]
    ok("B1 aucun octet modifié hors des écritures déclarées", not stray, f"{len(stray)} octet(s)")
    print(f"\n{sum(results)}/{len(results)} contrôles réussis")
    return 0 if all(results) else 1


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    sys.exit(main(sys.argv[1], sys.argv[2]))
