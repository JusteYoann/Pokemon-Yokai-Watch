#!/usr/bin/env python3
"""Extrait le contenu Yo-kai de VOTRE copie de « Pokémon Yo-kai Emerald » vers des fichiers prêts pour une
décompilation (pret/pokeemerald ou qigast/pokeemeraude). Rien n'est copié dans le dépôt : la sortie va dans le
dossier que vous indiquez (gardez-le hors de git, voir .gitignore de ce dossier).

    python3 yokai_extract.py <rom_yokai.gba> <dossier_sortie>

Dépendance : Pillow (images). Analyse décrite dans ../ROM_ANALYSIS.md.

Sortie :
  species.json            statistiques, types, talents, objets, attaques, CT/CS, évolutions (brutes + effectives),
                          Pokédex (catégorie, taille, poids, description), n° national/Hoenn, rencontres sauvages
  graphics/<NOM>/front.png, back.png (PNG indexés 16 couleurs, palette normale), shiny.pal, normal.pal (JASC),
               icon.png (+ id de palette d'icône dans species.json)
  trainers/BRENDAN_front.png, MAY_front.png  (illustrations de dresseur remplacées : Nathan / Katie)
  texts.json              textes ajoutés (noms, descriptions, crédits du panneau de Bourg-en-Vol)
  report.txt              anomalies détectées (évolutions copiées, type invalide, niveaux 1-100...)
"""
from __future__ import annotations

import json
import os
import re
import struct
import sys

try:
    from PIL import Image
except ImportError:  # pragma: no cover
    sys.exit("Pillow est requis : pip install pillow")

ROM_BASE = 0x08000000
VANILLA_SPECIES = 412          # SPECIES_NONE..SPECIES_CHIMECHO
TYPES = "NORMAL FIGHTING FLYING POISON GROUND ROCK BUG GHOST STEEL MYSTERY FIRE WATER GRASS ELECTRIC PSYCHIC ICE DRAGON DARK".split()
GROWTH = "MEDIUM_FAST ERRATIC FLUCTUATING MEDIUM_SLOW FAST SLOW".split()
VALID_EVO_METHODS = range(1, 16)

# --- table de caractères Gen 3 (anglais) : suffisante pour les textes de ce hack ---------------------------------
DEC = {0x00: " ", 0xAB: "!", 0xAC: "?", 0xAD: ".", 0xAE: "-", 0xB0: "…", 0xB1: "“", 0xB2: "”", 0xB3: "‘", 0xB4: "'",
       0xB5: "♂", 0xB6: "♀", 0xB8: ",", 0xBA: "/", 0xF0: ":", 0x1B: "é", 0xFE: "\\n", 0xFA: "\\l", 0xFB: "\\p"}
DEC.update({0xBB + i: c for i, c in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ")})
DEC.update({0xD5 + i: c for i, c in enumerate("abcdefghijklmnopqrstuvwxyz")})
DEC.update({0xA1 + i: c for i, c in enumerate("0123456789")})
ENC = {v: k for k, v in DEC.items() if len(v) == 1}


def text(d: bytes, o: int, n: int = 400) -> str:
    out = []
    for b in d[o:o + n]:
        if b == 0xFF:
            break
        out.append(DEC.get(b, "{%02X}" % b))
    return "".join(out)


def enc(s: str) -> bytes:
    return bytes(ENC[c] for c in s)


class Rom:
    def __init__(self, path: str):
        self.d = open(path, "rb").read()
        if self.d[0xAC:0xB0] != b"BPEE":
            raise SystemExit("Ce n'est pas une ROM Émeraude US (code BPEE).")

    def u8(self, o): return self.d[o]
    def u16(self, o): return struct.unpack_from("<H", self.d, o)[0]
    def u32(self, o): return struct.unpack_from("<I", self.d, o)[0]
    def ptr(self, o): return self.u32(o) - ROM_BASE

    def find(self, pat: bytes, align: int = 1) -> list[int]:
        return [m.start() for m in re.finditer(re.escape(pat), self.d) if m.start() % align == 0]

    # en-tête GF (src/rom_header_gf.c) : pointeurs vers les grandes tables
    def gf(self) -> dict:
        names = ["monFrontPics", "monBackPics", "monNormalPalettes", "monShinyPalettes", "monIcons",
                 "monIconPaletteIds", "monIconPalettes", "monSpeciesNames", "moveNames", "decorations"]
        h = {n: self.ptr(0x128 + 4 * i) for i, n in enumerate(names)}
        h["pokedexCount"] = self.u32(0x170)
        h["speciesInfo"] = self.ptr(0x1BC)
        return h


def lz10(d: bytes, o: int) -> bytes:
    if d[o] != 0x10:
        raise ValueError("pas de compression LZ10 à 0x%X" % o)
    size = d[o + 1] | d[o + 2] << 8 | d[o + 3] << 16
    o += 4
    out = bytearray()
    while len(out) < size:
        flags = d[o]; o += 1
        for b in range(8):
            if len(out) >= size:
                break
            if flags & (0x80 >> b):
                x = d[o] << 8 | d[o + 1]; o += 2
                for _ in range((x >> 12) + 3):
                    out.append(out[-((x & 0xFFF) + 1)])
            else:
                out.append(d[o]); o += 1
    return bytes(out)


def palette(raw: bytes, n: int = 16) -> list[tuple[int, int, int]]:
    out = []
    for i in range(n):
        c = struct.unpack_from("<H", raw, 2 * i)[0]
        out.append(((c & 31) * 255 // 31, ((c >> 5) & 31) * 255 // 31, ((c >> 10) & 31) * 255 // 31))
    return out


def indexed_png(raw4bpp: bytes, wtiles: int, pal, path: str) -> None:
    ntiles = len(raw4bpp) // 32
    htiles = ntiles // wtiles
    img = Image.new("P", (wtiles * 8, htiles * 8))
    img.putpalette([v for c in pal for v in c] + [0] * (768 - 3 * len(pal)))
    px = img.load()
    for t in range(ntiles):
        tx, ty = t % wtiles, t // wtiles
        for y in range(8):
            for x in range(8):
                b = raw4bpp[t * 32 + y * 4 + x // 2]
                px[tx * 8 + x, ty * 8 + y] = (b >> 4) if x & 1 else (b & 15)
    img.save(path)


def jasc(pal, path: str) -> None:
    with open(path, "w", newline="\r\n") as f:
        f.write("JASC-PAL\n0100\n%d\n" % len(pal))
        for r, g, b in pal:
            f.write(f"{r} {g} {b}\n")


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    rom, out = Rom(sys.argv[1]), sys.argv[2]
    d, g = rom.d, rom.gf()
    n_species = VANILLA_SPECIES + (g["pokedexCount"] - 386)
    new = list(range(VANILLA_SPECIES, n_species))
    os.makedirs(out, exist_ok=True)
    name = lambda sp: text(d, g["monSpeciesNames"] + sp * 11, 11)
    move = lambda m: text(d, g["moveNames"] + m * 13, 13)
    report: list[str] = [f"espèces : {n_species} (vanilla 412) ; Pokédex national : {g['pokedexCount']} (vanilla 386)"]

    # --- tables trouvées par signature (données vanilla d'Émeraude, positions propres à chaque build) -------------
    # gEvolutionTable[espèce][5] : struct Evolution {u16 méthode, param, cible} = 6 octets, ARRONDIS à 8 par l'ABI
    # apcs-gnu des builds « modern » (-mstructure-size-boundary=32) -> 40 octets par espèce
    EVO_STRIDE, EVO_SIZE = 40, 8
    evo = [o - EVO_STRIDE for o in rom.find(bytes.fromhex("040010000200"), 2)
           if d[o + EVO_STRIDE:o + EVO_STRIDE + 6] == bytes.fromhex("040020000300")]   # Bulbizarre, Herbizarre
    evo = evo[0] if len(evo) == 1 else None
    tm = rom.find(bytes(8) + bytes.fromhex("20073584081ee400"), 4)              # CT de Bulbizarre
    tm = tm[0] if len(tm) == 1 else None
    bulba_learn = rom.find(bytes.fromhex("21022d08490e16144d1e4f1e"), 2)
    learn = None
    if len(bulba_learn) == 1:
        p = struct.pack("<I", ROM_BASE + bulba_learn[0]) * 2                   # [NONE] et [BULBIZARRE] -> même liste
        hits = rom.find(p, 4)
        learn = hits[0] if hits else None
    dex = rom.find(enc("SEED") + b"\xff" + bytes(7) + struct.pack("<HH", 7, 69), 4)
    dex = dex[0] - 32 if len(dex) == 1 else None
    report.append(f"tables : évolutions 0x{evo or 0:X}, CT/CS 0x{tm or 0:X}, apprentissages 0x{learn or 0:X}, Pokédex 0x{dex or 0:X}")

    species = []
    for sp in new:
        e = d[g["speciesInfo"] + sp * 28: g["speciesInfo"] + sp * 28 + 26]
        (hp, at, df, spe, sa, sd, t1, t2, catch, exp, ev, i1, i2, gender, eggc, fr, growth,
         eg1, eg2, ab1, ab2, safari, col) = struct.unpack("<6B2BBBHHH6B2BBB", e)
        s = {"species_id": sp, "name": name(sp),
             "base_stats": {"hp": hp, "atk": at, "def": df, "spe": spe, "spa": sa, "spd": sd,
                            "total": hp + at + df + spe + sa + sd},
             "types": [TYPES[t] if t < 18 else f"INVALID_{t}" for t in (t1, t2)],
             "catch_rate": catch, "exp_yield": exp, "ev_yield_raw": ev, "items": [i1, i2],
             "gender_ratio": gender, "egg_cycles": eggc, "friendship": fr,
             "growth_rate": GROWTH[growth] if growth < 6 else growth, "egg_groups": [eg1, eg2],
             "abilities": [ab1, ab2], "safari_flee": safari, "body_color_raw": col}
        if t2 >= 18 and t2 != t1:
            report.append(f"{name(sp)} : second type invalide ({t2})")
        if learn is not None:
            o = rom.ptr(learn + 4 * sp); ls = []
            while rom.u16(o) != 0xFFFF:
                w = rom.u16(o); ls.append({"level": w >> 9, "move_id": w & 0x1FF, "move": move(w & 0x1FF)}); o += 2
            s["level_up_learnset"] = ls
        if tm is not None:
            lo, hi = struct.unpack_from("<II", d, tm + 8 * sp)
            s["tmhm_bits"] = [k for k in range(64) if (lo | hi << 32) >> k & 1]
        if evo is not None:
            raw = [struct.unpack_from("<3H", d, evo + sp * EVO_STRIDE + EVO_SIZE * k) for k in range(5)]
            s["evolutions_raw"] = raw
            eff = [{"method": m, "param": p, "target": t, "target_name": name(t)} for m, p, t in raw
                   if m in VALID_EVO_METHODS]
            s["evolutions_effective"] = eff
            for x in eff:
                report.append(f"{name(sp)} : évolue en {x['target_name']} (méthode {x['method']}, param {x['param']}) "
                              "— probablement copié d'une espèce vanilla")
        species.append(s)

    # Pokédex : entrée indexée par n° national (387.. pour les espèces ajoutées, vérifié dans ROM_ANALYSIS.md)
    if dex is not None:
        for i, s in enumerate(species):
            k = 387 + i                                                          # vérifié sur ce hack (ROM_ANALYSIS.md)
            o = dex + k * 32
            s["pokedex"] = {"national": k, "category": text(d, o, 12), "height_dm": rom.u16(o + 12),
                            "weight_hg": rom.u16(o + 14), "description": text(d, rom.ptr(o + 16)),
                            "scales": struct.unpack_from("<4H", d, o + 22)}

    # graphismes
    gdir = os.path.join(out, "graphics")
    for s in species:
        sp = s["species_id"]; sd_ = os.path.join(gdir, s["name"]); os.makedirs(sd_, exist_ok=True)
        npal = palette(lz10(d, rom.ptr(g["monNormalPalettes"] + 8 * sp)))
        spal = palette(lz10(d, rom.ptr(g["monShinyPalettes"] + 8 * sp)))
        indexed_png(lz10(d, rom.ptr(g["monFrontPics"] + 8 * sp)), 8, npal, os.path.join(sd_, "front.png"))
        indexed_png(lz10(d, rom.ptr(g["monBackPics"] + 8 * sp)), 8, npal, os.path.join(sd_, "back.png"))
        jasc(npal, os.path.join(sd_, "normal.pal")); jasc(spal, os.path.join(sd_, "shiny.pal"))
        pid = d[g["monIconPaletteIds"] + sp]; s["icon_palette_id"] = pid
        ipal = palette(d[rom.ptr(g["monIconPalettes"] + 8 * pid):])
        indexed_png(d[rom.ptr(g["monIcons"] + 4 * sp):][:1024], 4, ipal, os.path.join(sd_, "icon.png"))

    # illustrations de dresseur 71 (BRENDAN) / 72 (MAY) : gTrainerFrontPicTable = {ptr, taille 0x800, tag = index},
    # suivie de gTrainerFrontPicPaletteTable (93 entrées plus loin, comme dans pokeemerald)
    tdir = os.path.join(out, "trainers"); os.makedirs(tdir, exist_ok=True)
    NUM_TRAINER_PICS = 93
    cand = [o - 4 for o in rom.find(struct.pack("<HH", 0x800, 0), 4)
            if d[o + 8:o + 12] == struct.pack("<HH", 0x800, 1) and d[o + 16:o + 20] == struct.pack("<HH", 0x800, 2)]
    if cand:
        ft = cand[0]; pt = ft + 8 * NUM_TRAINER_PICS
        for idx, who in ((71, "BRENDAN"), (72, "MAY")):
            pal = palette(lz10(d, rom.ptr(pt + 8 * idx)))
            indexed_png(lz10(d, rom.ptr(ft + 8 * idx)), 8, pal, os.path.join(tdir, f"{who}_front.png"))
            jasc(pal, os.path.join(tdir, f"{who}_front.pal"))
        report.append(f"illustrations de dresseur : images 0x{ft:X}, palettes 0x{pt:X}")

    # rencontres sauvages : en-têtes {groupe, carte, 2 octets, 4 pointeurs}, terminés par 0xFF 0xFF
    wild = []
    for o in rom.find(bytes([0, 16, 0, 0]), 4):
        if d[o + 20:o + 22] == bytes([0, 17]) and d[o + 40:o + 42] == bytes([0, 18]):
            counts = {"land": 12, "water": 5, "rock": 5, "fish": 10}; h = o
            while d[h] != 0xFF:
                for k, ptrv in zip(counts, struct.unpack_from("<4I", d, h + 4)):
                    if ptrv:
                        lst = rom.ptr(ptrv - ROM_BASE + 4)            # WildPokemonInfo {u8 taux; ptr liste}
                        for j in range(counts[k]):
                            mn, mx, spc = struct.unpack_from("<BBH", d, lst + 4 * j)
                            if spc >= VANILLA_SPECIES:
                                wild.append({"map_group": d[h], "map_num": d[h + 1], "table": k, "slot": j,
                                             "min_level": mn, "max_level": mx, "species": name(spc)})
                                if mx - mn > 30:
                                    report.append(f"{name(spc)} : niveaux {mn}-{mx} (groupe {d[h]} carte {d[h+1]})")
                h += 20
            break
    for s in species:
        s["wild_encounters"] = [w for w in wild if w["species"] == s["name"]]
    report.append(f"emplacements sauvages Yo-kai : {len(wild)}")

    # textes : crédits (panneau de Bourg-en-Vol)
    credit = rom.find(enc("Jibanyan based on sprite of"))
    texts = {"species_names": [s["name"] for s in species],
             "credits_sign": text(d, credit[0]) if credit else None}
    json.dump(species, open(os.path.join(out, "species.json"), "w"), indent=1, ensure_ascii=False)
    json.dump(texts, open(os.path.join(out, "texts.json"), "w"), indent=1, ensure_ascii=False)
    open(os.path.join(out, "report.txt"), "w").write("\n".join(report) + "\n")
    print("\n".join(report))
    return 0


if __name__ == "__main__":
    sys.exit(main())
