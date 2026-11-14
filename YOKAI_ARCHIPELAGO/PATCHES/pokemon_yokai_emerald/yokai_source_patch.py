#!/usr/bin/env python3
"""Ajoute « Pokémon Yo-kai Emerald » (six Yo-kai équilibrés, Nathan/Katie, crédits) à une décompilation Émeraude.

    python3 yokai_source_patch.py <decomp> <rom_du_hack.gba> --lang fr|en [--extract-dir DIR]

<decomp> : pret/pokeemerald (anglais) ou qigast/pokeemeraude (français), ou un fork de l'un d'eux (patch AP).
<rom_du_hack.gba> : VOTRE copie du hack de SnappleRainKirby (SHA-1 ff71db05…) : graphismes et données du créateur
y sont lus au moment de la génération ; rien du créateur n'est stocké dans ce dépôt.

Sources de vérité :
- research/yokai-emerald/balance/yokai_balance.json + .resolved.json  (fiches validées : stats, types, talents,
  attaques, CT/CS, rencontres, starter) ;
- la ROM du hack (sprites, palettes, icônes, coordonnées, catégorie et descriptions Pokédex, valeurs non
  couvertes par les fiches : taux de capture, objets tenus, sexe, groupes d'œufs…).

Décisions appliquées (voir YOKAI_ARCHIPELAGO/DOCUMENTATION/chantiers/E_pokemon_yokai_emerald.md) :
- « Regard Touchant » (6e génération, absente) -> Rugissement (même effet : Attaque -1), validé par l'utilisateur ;
- « Protection » = Reflect et « Lance-Boue » = Mud Sport (noms français de 2005, lecture littérale) ;
- Whisper niv. 38 : doublon d'Onde Folie conservé (alternative Feinte en attente) ;
- espèces n° 412-417 et Pokédex national 387-392 / Hoenn 203-208, comme dans le hack ;
- Pokédex de Komajiro et Whisper corrigés (bug du hack), cris empruntés à des espèces existantes.
L'outil s'arrête si la décompilation contient déjà SPECIES_JIBANYAN (idempotence).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import struct
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
BAL = os.path.join(REPO, "research", "yokai-emerald", "balance")
EXTRACTOR = os.path.join(REPO, "research", "yokai-emerald", "tools", "yokai_extract.py")
HACK_SHA1 = "ff71db053a6d4d0f31368d95b39c6b7d6038da13"

ORDER = ["JIBANYAN", "KOMASAN", "KOMAJIRO", "BLIZZARIA", "GARGAROS", "WHISPER"]      # n° 412..417 (hack)
CAMEL = {n: n.capitalize() for n in ORDER}
CRY_FROM = {"JIBANYAN": "MEOWTH", "KOMASAN": "GROWLITHE", "KOMAJIRO": "PIKACHU", "BLIZZARIA": "JYNX",
            "GARGAROS": "MACHAMP", "WHISPER": "GASTLY"}
BACK_ANIM = "BACK_ANIM_CONVEX_DOUBLE_ARC"
FRONT_ANIM = "ANIM_V_SQUISH_AND_BOUNCE"
TYPES = ["NORMAL", "FIGHTING", "FLYING", "POISON", "GROUND", "ROCK", "BUG", "GHOST", "STEEL", "MYSTERY", "FIRE",
         "WATER", "GRASS", "ELECTRIC", "PSYCHIC", "ICE", "DRAGON", "DARK"]
GROWTH = ["GROWTH_MEDIUM_FAST", "GROWTH_ERRATIC", "GROWTH_FLUCTUATING", "GROWTH_MEDIUM_SLOW", "GROWTH_FAST", "GROWTH_SLOW"]
COLORS = ["RED", "BLUE", "YELLOW", "GREEN", "BLACK", "BROWN", "PURPLE", "GRAY", "WHITE", "PINK"]
EXTRA_MOVES = {"BLIZZARIA": {1: "MOVE_GROWL"}}           # « Regard Touchant » -> Rugissement (validé)

DEX_FR = {
    "JIBANYAN": "Renversé par un camion, il hante un\ncarrefour et cherche à se venger\ndes camions qui passent.",
    "KOMASAN": "Ce chien-lion gardien s'est lassé\nde garder son sanctuaire.\nIl en cherche un nouveau.",
    "KOMAJIRO": "Le petit frère de Komasan. Il cherche\nson grand frère fugueur, mais ne\nle trouve nulle part, le pauvre.",
    "BLIZZARIA": "Elle maîtrise enfin son pouvoir glacial.\nElle fait neiger en plein été\net gèle les volcans.",
    "GARGAROS": "Un ogre rouge géant qui hante les\ncauchemars des enfants. On dit que\nle vaincre aide à grandir.",
    "WHISPER": "Il se dit majordome Yo-kai et semble\ntout savoir, mais il lit simplement\nles infos de son Yo-kai Pad.",
}
CATEGORY = {"fr": "YO-KAI", "en": "YOKAI"}
NURSE = {
    "fr": ['Par exemple, ton JIBANYAN est\\n', 'de type FEU et COMBAT.\\p',
           'Il est fort contre les types PLANTE,\\n', 'GLACE, INSECTE, ACIER et NORMAL.\\p',
           'Mais il craint les attaques EAU,\\n', 'SOL, VOL et PSY.$'],
    "en": ['For example, your JIBANYAN\\n', 'is a FIRE and FIGHTING type.\\p',
           "It's strong against GRASS, ICE,\\n", 'BUG, STEEL and NORMAL types.\\p',
           "But, it's weak against WATER,\\n", 'GROUND, FLYING and PSYCHIC moves.$'],
}
CREDITS = {
    "fr": ["Pokémon Yo-kai Emerald, un fangame\\n", "de SnappleRainKirby (KirbyLemonRain sur X).\\p",
           "Jibanyan d'après un sprite de :\\n", "Ludo.\\p", "Autres sprites :\\n", "SonGoku et Nicowico.$"],
    "en": ["Pokémon Yo-kai Emerald, a fangame\\n", "by SnappleRainKirby (KirbyLemonRain on X).\\p",
           "Jibanyan based on sprite of:\\n", "Ludo.\\p", "the other sprites by:\\n", "SonGoku and Nicowico.$"],
}


class Src:
    """Éditions de fichiers par ANCRES : chaque ancre doit exister exactement une fois, sinon arrêt."""

    def __init__(self, root):
        self.root, self.cache, self.log = root, {}, []

    def get(self, rel):
        if rel not in self.cache:
            self.cache[rel] = open(os.path.join(self.root, rel), encoding="utf-8").read()
        return self.cache[rel]

    def set(self, rel, text, what):
        self.cache[rel] = text
        self.log.append(f"{rel}: {what}")

    def replace_once(self, rel, old, new, what):
        t = self.get(rel)
        if t.count(old) != 1:
            raise SystemExit(f"[{rel}] ancre introuvable ou multiple ({t.count(old)}) : {old[:60]!r}")
        self.set(rel, t.replace(old, new, 1), what)

    def after_line(self, rel, pattern, new, what):
        """insère `new` après la ligne (unique) qui correspond à `pattern` (regex)."""
        t = self.get(rel)
        ms = list(re.finditer(pattern, t, re.M))
        if len(ms) != 1:
            raise SystemExit(f"[{rel}] motif {pattern!r} trouvé {len(ms)} fois")
        end = t.index("\n", ms[0].end()) + 1
        self.set(rel, t[:end] + new + t[end:], what)

    def after_block(self, rel, pattern, new, what):
        """insère après le bloc { … } qui suit le motif (entrée de tableau désignée sur plusieurs lignes)."""
        t = self.get(rel)
        ms = list(re.finditer(pattern, t, re.M))
        if len(ms) != 1:
            raise SystemExit(f"[{rel}] motif {pattern!r} trouvé {len(ms)} fois")
        i = t.index("{", ms[0].end())
        depth = 0
        while True:
            depth += {"{": 1, "}": -1}.get(t[i], 0)
            i += 1
            if depth == 0:
                break
        if t[i] == ";":                                   # définition de tableau complète : on insère après « }; »
            i += 1
            insert = "\n" + new.rstrip("\n")
        elif t[i] == ",":
            i += 1
            insert = "\n" + new.rstrip("\n")
        else:
            insert = ",\n" + new.rstrip("\n").rstrip(",")
        self.set(rel, t[:i] + insert + t[i:], what)

    def write_all(self):
        for rel, text in self.cache.items():
            open(os.path.join(self.root, rel), "w", encoding="utf-8").write(text)


def write_indexed_png(raw4bpp, wtiles, htiles, pal, path, mw=None, mh=None):
    """4bpp brut -> PNG indexé 4 bits. Avec -mwidth/-mheight, les frames (mw×mh tuiles) se suivent dans les données."""
    from PIL import Image
    img = Image.new("P", (wtiles * 8, htiles * 8))
    img.putpalette([v for c in pal for v in c] + [0] * (768 - 3 * len(pal)))
    px = img.load()
    ntiles = len(raw4bpp) // 32
    for t in range(ntiles):
        if mw:
            per_row = wtiles // mw
            frame, k = divmod(t, mw * mh)
            fx, fy = frame % per_row, frame // per_row
            tx, ty = fx * mw + k % mw, fy * mh + k // mw
        else:
            tx, ty = t % wtiles, t // wtiles
        for y in range(8):
            for x in range(8):
                b = raw4bpp[t * 32 + y * 4 + x // 2]
                px[tx * 8 + x, ty * 8 + y] = (b >> 4) if x & 1 else (b & 15)
    img.save(path, bits=4)


def read_png_palette(path):
    from PIL import Image
    im = Image.open(path)
    p = im.getpalette()[:48]
    return [tuple(p[i:i + 3]) for i in range(0, 48, 3)], im.size


def lz10(d, o):
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


def gba_pal(raw, n=16):
    return [((c & 31) * 255 // 31, ((c >> 5) & 31) * 255 // 31, ((c >> 10) & 31) * 255 // 31)
            for c in struct.unpack_from(f"<{n}H", raw)]


def find_table(rom, sig, stride, index_of_sig):
    hits = [m.start() for m in re.finditer(re.escape(sig), rom)]
    hits = [h - stride * index_of_sig for h in hits]
    if len(hits) != 1:
        raise SystemExit(f"table du hack introuvable (signature {sig.hex()}, {len(hits)} résultats)")
    return hits[0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("decomp"); ap.add_argument("hack_rom")
    ap.add_argument("--lang", choices=["fr", "en"], required=True)
    ap.add_argument("--extract-dir", default=None)
    a = ap.parse_args()
    rom = open(a.hack_rom, "rb").read()
    if hashlib.sha1(rom).hexdigest() != HACK_SHA1:
        raise SystemExit("ROM du hack inattendue (SHA-1 attendu ff71db05…).")
    src = Src(a.decomp)
    if "SPECIES_JIBANYAN" in src.get("include/constants/species.h"):
        raise SystemExit("Déjà appliqué (SPECIES_JIBANYAN présent).")
    ex = a.extract_dir or os.path.join(a.decomp, "..", "yokai_extract_out")
    if not os.path.exists(os.path.join(ex, "species.json")):
        subprocess.run([sys.executable, EXTRACTOR, a.hack_rom, ex], check=True, stdout=subprocess.DEVNULL)
    creator = {s["name"]: s for s in json.load(open(os.path.join(ex, "species.json"), encoding="utf-8"))}
    spec = json.load(open(os.path.join(BAL, "yokai_balance.json"), encoding="utf-8"))
    res = json.load(open(os.path.join(BAL, "yokai_balance.resolved.json"), encoding="utf-8"))["resolved"]
    tms = re.findall(r"F\((\w+)\)", src.get("include/constants/tms_hms.h"))
    gf = lambda off: struct.unpack_from("<I", rom, off)[0] - 0x08000000

    # ---- 1. constantes -------------------------------------------------------------------------------------
    src.replace_once("include/constants/species.h", "#define SPECIES_EGG 412",
                     "".join(f"#define SPECIES_{n} {412 + i}\n" for i, n in enumerate(ORDER)) + "#define SPECIES_EGG 418",
                     "6 espèces 412-417, SPECIES_EGG = 418")
    src.after_line("include/constants/pokedex.h", r"^    NATIONAL_DEX_DEOXYS,$",
                   "".join(f"    NATIONAL_DEX_{n},\n" for n in ORDER), "Pokédex national 387-392")
    src.replace_once("include/constants/pokedex.h", "#define NATIONAL_DEX_COUNT  NATIONAL_DEX_DEOXYS",
                     "#define NATIONAL_DEX_COUNT  NATIONAL_DEX_WHISPER", "NATIONAL_DEX_COUNT = 392")
    src.after_line("include/constants/pokedex.h", r"^    HOENN_DEX_DEOXYS,$",
                   "".join(f"    HOENN_DEX_{n},\n" for n in ORDER), "Pokédex de Hoenn 203-208")
    src.replace_once("include/constants/pokedex.h", "#define HOENN_DEX_COUNT HOENN_DEX_DEOXYS",
                     "#define HOENN_DEX_COUNT HOENN_DEX_WHISPER", "HOENN_DEX_COUNT = 208")

    # ---- 2. données d'espèce -------------------------------------------------------------------------------
    src.after_line("src/data/text/species_names.h", r"^\s*\[SPECIES_CHIMECHO\] = _\(",
                   "".join(f'    [SPECIES_{n}] = _("{n}"),\n' for n in ORDER), "noms")
    info, learn, ptrs, tmhm = [], [], [], []
    for n in ORDER:
        sp, r, c = spec["species"][n], res[n], creator[n]
        s = sp["stats"]
        t = [x[5:] for x in r["types"]] * (2 if len(r["types"]) == 1 else 1)
        ab = r["ability"]["const"]
        ev = c["ev_yield_raw"]
        evs = [(ev >> (2 * k)) & 3 for k in range(6)]          # PV, Atq, Déf, Vit, AtqSpé, DéfSpé
        col = c["body_color_raw"]
        info.append(f"""    [SPECIES_{n}] =
    {{
        .baseHP        = {s['hp']},
        .baseAttack    = {s['atk']},
        .baseDefense   = {s['def']},
        .baseSpeed     = {s['spe']},
        .baseSpAttack  = {s['spa']},
        .baseSpDefense = {s['spd']},
        .types = {{ TYPE_{t[0]}, TYPE_{t[1]} }},
        .catchRate = {c['catch_rate']},
        .expYield = {c['exp_yield']},
        .evYield_HP        = {evs[0]},
        .evYield_Attack    = {evs[1]},
        .evYield_Defense   = {evs[2]},
        .evYield_Speed     = {evs[3]},
        .evYield_SpAttack  = {evs[4]},
        .evYield_SpDefense = {evs[5]},
        .itemCommon = {c['items'][0]},
        .itemRare   = {c['items'][1]},
        .genderRatio = {c['gender_ratio']},
        .eggCycles = {c['egg_cycles']},
        .friendship = {c['friendship']},
        .growthRate = {c['growth_rate'] if str(c['growth_rate']).startswith('GROWTH') else 'GROWTH_' + str(c['growth_rate'])},
        .eggGroups = {{ {c['egg_groups'][0]}, {c['egg_groups'][1]} }},
        .abilities = {{{ab}, {ab}}},
        .safariZoneFleeRate = {c['safari_flee']},
        .bodyColor = BODY_COLOR_{COLORS[col & 0x7F]},
        .noFlip = {'TRUE' if col & 0x80 else 'FALSE'},
    }},
""")
        moves = [(e["level"], e["const"] or EXTRA_MOVES.get(n, {}).get(e["level"])) for e in r["learnset"]]
        if any(m is None for _, m in moves):
            raise SystemExit(f"{n} : attaque non résolue")
        learn.append(f"static const u16 s{CAMEL[n]}LevelUpLearnset[] = {{\n"
                     + "".join(f"    LEVEL_UP_MOVE({lv:2d}, {m}),\n" for lv, m in moves) + "    LEVEL_UP_END\n};\n\n")
        ptrs.append(f"    [SPECIES_{n}] = s{CAMEL[n]}LevelUpLearnset,\n")
        fields = [tms[x["bit"]] for x in r["tm"] + r["hm"]]
        tmhm.append(f"    [SPECIES_{n}] = {{ .learnset = {{\n" + "".join(f"        .{f} = TRUE,\n" for f in fields) + "    } },\n")
    src.after_block("src/data/pokemon/species_info.h", r"^\s*\[SPECIES_CHIMECHO\] =", "".join(info), "6 fiches d'espèce")
    src.after_block("src/data/pokemon/level_up_learnsets.h", r"^static const u16 sChimechoLevelUpLearnset\[\] =",
                    "\n" + "".join(learn), "apprentissages")
    src.after_line("src/data/pokemon/level_up_learnset_pointers.h", r"^\s*\[SPECIES_CHIMECHO\] = ", "".join(ptrs), "pointeurs")
    src.after_block("src/data/pokemon/tmhm_learnsets.h", r"^\s*\[SPECIES_CHIMECHO\] = ", "".join(tmhm), "CT/CS")

    # ---- 3. Pokédex : n° nationaux et textes (descriptions anglaises du créateur, ou traduction française) -----
    for macro, enum in (("SPECIES_TO_HOENN", "CHIMECHO"), ("SPECIES_TO_NATIONAL", "CHIMECHO"), ("HOENN_TO_NATIONAL", "CHIMECHO")):
        src.after_line("src/pokemon.c", rf"^\s*{macro}\({enum}\),", "".join(f"    {macro}({n}),\n" for n in ORDER), macro)
    src.after_line("src/pokemon.c", r"^\s*\[SPECIES_CHIMECHO - 1\]\s*= ANIM_", "".join(f"    [SPECIES_{n} - 1] = {FRONT_ANIM},\n" for n in ORDER), "animations")
    dex_tab = None
    # entrées Pokédex du hack : catégorie/échelles (n° 387-391 ; Whisper 392 vide dans le hack -> échelles de Komasan)
    dex_sig = bytes([0xCD, 0xBF, 0xBF, 0xBE, 0xFF]) + bytes(7) + struct.pack("<HH", 7, 69)
    dex_tab = find_table(rom, dex_sig, 32, 1)
    entries, texts = [], []
    for i, n in enumerate(ORDER):
        k = 387 + i
        o = dex_tab + 32 * (k if n != "WHISPER" else 388)
        height, weight = struct.unpack_from("<HH", rom, dex_tab + 32 * k + 12)
        scales = struct.unpack_from("<4H", rom, o + 22)
        desc = DEX_FR[n] if a.lang == "fr" else creator[n]["pokedex"]["description"].replace("\\n", "\n")
        if a.lang == "en" and n in ("KOMAJIRO", "WHISPER"):        # textes croisés dans le hack (bug corrigé)
            desc = {"KOMAJIRO": "Komasan's younger twin. He looks\nfor his runaway bro.\nBut he can't find him anywhere,\npoor guy.",
                    "WHISPER": creator["KOMAJIRO"]["pokedex"]["description"].replace("\\n", "\n")}[n]
        lines = desc.split("\n")
        texts.append(f"const u8 g{CAMEL[n]}PokedexText[] = _(\n" + "\n".join(
            f'    "{l}\\n"' if j < len(lines) - 1 else f'    "{l}"' for j, l in enumerate(lines)) + ");\n\n")
        entries.append(f"""    [NATIONAL_DEX_{n}] =
    {{
        .categoryName = _("{CATEGORY[a.lang]}"),
        .height = {height},
        .weight = {weight},
        .description = g{CAMEL[n]}PokedexText,
        .pokemonScale = {scales[0]},
        .pokemonOffset = {scales[1]},
        .trainerScale = {scales[2]},
        .trainerOffset = {scales[3]},
    }},
""")
    src.after_block("src/data/pokemon/pokedex_entries.h", r"^\s*\[NATIONAL_DEX_DEOXYS\] =", "".join(entries), "entrées Pokédex")
    src.set("src/data/pokemon/pokedex_text.h", src.get("src/data/pokemon/pokedex_text.h") + "\n" + "".join(texts), "textes Pokédex")
    for label in ("gPokedexOrder_Alphabetical", "gPokedexOrder_Weight", "gPokedexOrder_Height"):
        t = src.get("src/data/pokemon/pokedex_orders.h")
        i = t.index(label); j = t.index("};", i)
        src.set("src/data/pokemon/pokedex_orders.h", t[:j] + "".join(f"    NATIONAL_DEX_{n},\n" for n in ORDER) + t[j:], f"{label} (ajout en fin)")

    # ---- 4. graphismes --------------------------------------------------------------------------------------
    hdr = {k: gf(o) for k, o in (("front", 0x128), ("back", 0x12C), ("pal", 0x130), ("shiny", 0x134),
                                    ("icons", 0x138), ("iconpal", 0x13C), ("iconpals", 0x140))}
    for i, n in enumerate(ORDER):
        sid = 412 + i
        d = os.path.join(a.decomp, "graphics", "pokemon", n.lower())
        os.makedirs(d, exist_ok=True)
        pal = gba_pal(lz10(rom, struct.unpack_from("<I", rom, hdr["pal"] + 8 * sid)[0] - 0x08000000))
        shiny = gba_pal(lz10(rom, struct.unpack_from("<I", rom, hdr["shiny"] + 8 * sid)[0] - 0x08000000))
        front = lz10(rom, struct.unpack_from("<I", rom, hdr["front"] + 8 * sid)[0] - 0x08000000)
        back = lz10(rom, struct.unpack_from("<I", rom, hdr["back"] + 8 * sid)[0] - 0x08000000)
        write_indexed_png(front, 8, len(front) // 256, pal, os.path.join(d, "anim_front.png"))
        write_indexed_png(front[:2048], 8, 8, pal, os.path.join(d, "front.png"))
        write_indexed_png(back, 8, 8, pal, os.path.join(d, "back.png"))
        for nm, p in (("normal.pal", pal), ("shiny.pal", shiny)):
            with open(os.path.join(d, nm), "w", newline="\r\n") as f:
                f.write("JASC-PAL\n0100\n16\n" + "".join(f"{r} {g} {b}\n" for r, g, b in p))
        pid = rom[hdr["iconpal"] + sid]
        ipal = gba_pal(rom[struct.unpack_from("<I", rom, hdr["iconpals"] + 8 * pid)[0] - 0x08000000:][:32])
        icon = rom[struct.unpack_from("<I", rom, hdr["icons"] + 4 * sid)[0] - 0x08000000:][:1024]
        write_indexed_png(icon, 4, 8, ipal, os.path.join(d, "icon.png"))
        from PIL import Image
        fp = Image.new("1", (16, 16), 0)          # empreinte vide (non extraite du hack)
        fp.save(os.path.join(d, "footprint.png"))
    decl = "".join(f"""const u32 gMonStillFrontPic_{CAMEL[n]}[] = INCGFX_U32("graphics/pokemon/{n.lower()}/front.png", ".4bpp.lz");
const u32 gMonPalette_{CAMEL[n]}[] = INCGFX_U32("graphics/pokemon/{n.lower()}/normal.pal", ".gbapal.lz");
const u32 gMonBackPic_{CAMEL[n]}[] = INCGFX_U32("graphics/pokemon/{n.lower()}/back.png", ".4bpp.lz");
const u32 gMonShinyPalette_{CAMEL[n]}[] = INCGFX_U32("graphics/pokemon/{n.lower()}/shiny.pal", ".gbapal.lz");
const u8 gMonIcon_{CAMEL[n]}[] = INCGFX_U8("graphics/pokemon/{n.lower()}/icon.png", ".4bpp");
const u8 gMonFootprint_{CAMEL[n]}[] = INCGFX_U8("graphics/pokemon/{n.lower()}/footprint.png", ".1bpp");
""" for n in ORDER)
    src.after_line("src/data/graphics/pokemon.h", r"^const u8 gMonFootprint_Chimecho\[\]", decl, "déclarations graphiques")
    src.after_line("src/anim_mon_front_pics.c", r"^const u32 gMonFrontPic_Chimecho\[\]",
                   "".join(f'const u32 gMonFrontPic_{CAMEL[n]}[] = INCGFX_U32("graphics/pokemon/{n.lower()}/anim_front.png", ".4bpp.lz");\n' for n in ORDER), "images animées")
    src.after_line("include/graphics.h", r"^extern const u8 gMonFootprint_Chimecho\[\];",
                   "".join(f"extern const u32 gMonFrontPic_{c}[];\nextern const u32 gMonPalette_{c}[];\nextern const u32 gMonBackPic_{c}[];\n"
                           f"extern const u32 gMonShinyPalette_{c}[];\nextern const u32 gMonStillFrontPic_{c}[];\nextern const u8 gMonIcon_{c}[];\n"
                           f"extern const u8 gMonFootprint_{c}[];\n" for c in (CAMEL[n] for n in ORDER)), "extern")
    G = "src/data/pokemon_graphics/"
    simple = [
        (G + "front_pic_table.h", r"^\s*SPECIES_SPRITE\(CHIMECHO,", lambda n: f"    SPECIES_SPRITE({n}, gMonFrontPic_{CAMEL[n]}),\n"),
        (G + "back_pic_table.h", r"^\s*SPECIES_SPRITE\(CHIMECHO,", lambda n: f"    SPECIES_SPRITE({n}, gMonBackPic_{CAMEL[n]}),\n"),
        (G + "still_front_pic_table.h", r"^\s*SPECIES_SPRITE\(CHIMECHO,", lambda n: f"    SPECIES_SPRITE({n}, gMonStillFrontPic_{CAMEL[n]}),\n"),
        (G + "palette_table.h", r"^\s*SPECIES_PAL\(CHIMECHO,", lambda n: f"    SPECIES_PAL({n}, gMonPalette_{CAMEL[n]}),\n"),
        (G + "shiny_palette_table.h", r"^\s*SPECIES_SHINY_PAL\(CHIMECHO,", lambda n: f"    SPECIES_SHINY_PAL({n}, gMonShinyPalette_{CAMEL[n]}),\n"),
        (G + "footprint_table.h", r"^\s*\[SPECIES_CHIMECHO\] = gMonFootprint", lambda n: f"    [SPECIES_{n}] = gMonFootprint_{CAMEL[n]},\n"),
        (G + "front_pic_anims.h", r"^\s*\[SPECIES_CHIMECHO\]\s*= sAnims_Chimecho", lambda n: f"    [SPECIES_{n}] = sAnims_Chimecho,\n"),
        (G + "unknown_table.h", r"^\s*\[SPECIES_CHIMECHO\]\s*= 0x", lambda n: f"    [SPECIES_{n}] = 0x88,\n"),
        ("src/pokemon_icon.c", r"^\s*\[SPECIES_CHIMECHO\] = gMonIcon_Chimecho", lambda n: f"    [SPECIES_{n}] = gMonIcon_{CAMEL[n]},\n"),
        ("src/pokemon_icon.c", r"^\s*\[SPECIES_CHIMECHO\] = \d", lambda n: f"    [SPECIES_{n}] = {rom[hdr['iconpal'] + 412 + ORDER.index(n)]},\n"),
        ("src/pokemon_animation.c", r"^\s*\[SPECIES_CHIMECHO\]\s*= BACK_ANIM", lambda n: f"    [SPECIES_{n}] = {BACK_ANIM},\n"),
        ("src/data/pokemon/cry_ids.h", r"^\s*\[SPECIES_CHIMECHO - 277\]", lambda n: f"    [SPECIES_{n} - 277] = SPECIES_{CRY_FROM[n]} - 1,\n"),
    ]
    for rel, pat, fn in simple:
        src.after_line(rel, pat, "".join(fn(n) for n in ORDER), os.path.basename(rel))
    # coordonnées / élévation : valeurs du créateur (tables du hack retrouvées par la signature de Bulbizarre)
    fc = src.get(G + "front_pic_coordinates.h")
    def coords_sig(text, k):
        m = re.search(rf"\[SPECIES_{k}\]\s*= {{ \.size = MON_COORDS_SIZE\((\d+), (\d+)\), \.y_offset = +(\d+) }}", text)
        w, h, y = map(int, m.groups())
        return bytes([((w + 7) // 8) << 4 | ((h + 7) // 8), y, 0, 0])
    for fname in ("front_pic_coordinates.h", "back_pic_coordinates.h"):
        t = src.get(G + fname)
        sig = coords_sig(t, "BULBASAUR") + coords_sig(t, "IVYSAUR") + coords_sig(t, "VENUSAUR")
        base = find_table(rom, sig, 4, 1)
        lines = []
        for i, n in enumerate(ORDER):
            size, yoff = rom[base + 4 * (412 + i)], rom[base + 4 * (412 + i) + 1]
            lines.append(f"    [SPECIES_{n}] = {{ .size = MON_COORDS_SIZE({(size >> 4) * 8}, {(size & 15) * 8}), .y_offset = {yoff:2d} }},\n")
        src.after_line(G + fname, r"^\s*\[SPECIES_CHIMECHO\]\s*= { \.size", "".join(lines), f"{fname} (valeurs du créateur)")
    # élévation (u8 par espèce) : signature = valeurs des espèces 1..80 lues dans la décompilation
    t = src.get(G + "enemy_mon_elevation.h")
    elev = {k: int(v) for k, v in re.findall(r"\[SPECIES_(\w+)\] = (\d+),", t)}
    ids = {k: int(v) for k, v in re.findall(r"#define SPECIES_(\w+) (\d+)\n", src.get("include/constants/species.h"))}
    sig = bytes(elev.get(next((k for k, v in ids.items() if v == i), ""), 0) for i in range(1, 81))
    base = find_table(rom, sig, 1, 1)
    src.after_line(G + "enemy_mon_elevation.h", r"^\s*\[SPECIES_CHIMECHO\] = \d+", "".join(
        f"    [SPECIES_{n}] = {rom[base + 412 + i]},\n" for i, n in enumerate(ORDER)), "élévation (valeurs du créateur)")

    # ---- 5. starter, rencontres, réplique de l'infirmière, panneau de crédits ---------------------------------
    t = src.get("src/starter_choose.c")
    t2 = re.sub(r"(static const u16 sStarterMon\[STARTER_MON_COUNT\] =\s*\{)[^}]*\}",
                r"\1\n    SPECIES_JIBANYAN,\n    SPECIES_JIBANYAN,\n    SPECIES_JIBANYAN,\n}", t, count=1)
    if t2 == t:
        raise SystemExit("sStarterMon introuvable")
    src.set("src/starter_choose.c", t2, "starter = JIBANYAN ×3")
    wild = json.loads(src.get("src/data/wild_encounters.json"))
    slots = {"KOMASAN": {"MAP_PETALBURG_WOODS": [3, 6]},
             "WHISPER": {"MAP_GRANITE_CAVE_1F": [2, 6], "MAP_GRANITE_CAVE_B1F": [3, 6], "MAP_GRANITE_CAVE_B2F": [4, 6]},
             "KOMAJIRO": {"MAP_ROUTE110": [3, 6]}, "BLIZZARIA": {"MAP_ROUTE113": [3, 6]},
             "GARGAROS": {"MAP_JAGGED_PASS": [3, 7]}}
    done = 0
    for grp in wild["wild_encounter_groups"]:
        for enc in grp.get("encounters", []):
            for n, maps in slots.items():
                if enc.get("map") in maps and "land_mons" in enc:
                    lo, hi = spec["encounters"][n]["levels"]
                    for k in maps[enc["map"]]:
                        enc["land_mons"]["mons"][k] = {"min_level": lo, "max_level": hi, "species": f"SPECIES_{n}"}
                        done += 1
    if done != 14:
        raise SystemExit(f"rencontres : {done} emplacements modifiés au lieu de 14")
    src.set("src/data/wild_encounters.json", json.dumps(wild, indent=2, ensure_ascii=False) + "\n", "14 emplacements Yo-kai")
    sc = "data/maps/PetalburgCity_PokemonCenter_1F/scripts.inc"
    t = src.get(sc)
    t2 = re.sub(r"\tcall_if_eq VAR_STARTER_MON, 0, \w+\n\tcall_if_eq VAR_STARTER_MON, 1, \w+\n\tcall_if_eq VAR_STARTER_MON, 2, \w+\n",
                "\tmsgbox PetalburgCity_PokemonCenter_1F_Text_JibanyanType, MSGBOX_DEFAULT\n", t, count=1)
    if t2 == t:
        raise SystemExit("script de l'infirmière introuvable")
    src.set(sc, t2 + "\nPetalburgCity_PokemonCenter_1F_Text_JibanyanType:\n" + "".join(f'\t.string "{l}"\n' for l in NURSE[a.lang]),
            "réplique de l'infirmière (Jibanyan)")
    mj = "data/maps/LittlerootTown/map.json"
    m = json.loads(src.get(mj))
    m["bg_events"].append({"type": "sign", "x": 7, "y": 5, "elevation": 0, "player_facing_dir": "BG_EVENT_PLAYER_FACING_ANY",
                           "script": "LittlerootTown_EventScript_YokaiCreditsSign"})
    src.set(mj, json.dumps(m, indent=2, ensure_ascii=False) + "\n", "panneau de crédits (x=7, y=5)")
    ls = "data/maps/LittlerootTown/scripts.inc"
    src.set(ls, src.get(ls) + "\nLittlerootTown_EventScript_YokaiCreditsSign::\n\tmsgbox LittlerootTown_Text_YokaiCredits, MSGBOX_SIGN\n\tend\n\n"
            "LittlerootTown_Text_YokaiCredits:\n" + "".join(f'\t.string "{l}"\n' for l in CREDITS[a.lang]), "texte des crédits")

    # ---- 6. Nathan et Katie : sprites de terrain et illustrations de dresseur du hack -------------------------
    offs = json.load(open(os.path.join(HERE, "player_gfx_offsets.json")))
    for sym, o in offs.items():
        path = os.path.join(a.decomp, o["file"])
        pal, (w, h) = read_png_palette(path)
        mw = mh = None
        mm = re.match(r"-mwidth (\d+) -mheight (\d+)", o["args"] or "")
        if mm:
            mw, mh = int(mm.group(1)), int(mm.group(2))
        raw = rom[o["hack_offset"]:o["hack_offset"] + o["size"]]
        write_indexed_png(raw, w // 8, h // 8, pal, path, mw, mh)
    # illustrations de face (et palette commune face/dos) des dresseurs Brendan/May
    from PIL import Image
    for who, fn in (("BRENDAN", "brendan"), ("MAY", "may")):
        im = Image.open(os.path.join(ex, "trainers", f"{who}_front.png"))
        im.save(os.path.join(a.decomp, "graphics", "trainers", "front_pics", f"{fn}.png"), bits=4)
        palf = os.path.join(ex, "trainers", f"{who}_front.pal")
        open(os.path.join(a.decomp, "graphics", "trainers", "palettes", f"{fn}.pal"), "w", newline="\r\n").write(
            open(palf).read().replace("\r\n", "\n"))
        # le dos utilise la même palette : on ré-indexe l'image du dos avec la palette du hack
        back = os.path.join(a.decomp, "graphics", "trainers", "back_pics", f"{fn}.png")
        b = Image.open(back)
        b.putpalette(im.getpalette())
        b.save(back, bits=4)

    # ---- 7. patch Archipelago (fork de Flit) : nom de ROM distinct, vérifié par le client du monde « Pokemon Yo-kai Emerald »
    hdr_c = "src/rom_header_gf.c"
    if "flit ap" in src.get(hdr_c):
        t = src.get(hdr_c)
        t2 = re.sub(r'\.gameName = "pokemon emerald / flit ap [^"]*"', '.gameName = "pokemon emerald / yokai ap v0.1"', t)
        src.set(hdr_c, t2, "nom de ROM « pokemon emerald / yokai ap v0.1 »")

    src.write_all()
    open(os.path.join(a.decomp, "YOKAI_PATCH_LOG.txt"), "w", encoding="utf-8").write("\n".join(src.log) + "\n")
    print(f"{len(src.log)} modifications de sources ; graphismes écrits pour {len(ORDER)} Yo-kai et Nathan/Katie.")


if __name__ == "__main__":
    main()
