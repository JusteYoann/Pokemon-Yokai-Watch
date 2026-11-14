#!/usr/bin/env python3
"""Résout les noms français de yokai_balance.json en identifiants internes de Pokémon Émeraude.

    python3 resolve_names.py <qigast/pokeemeraude> <pret/pokeemerald> [--json resolved.json]

Sources de vérité : la décompilation FRANÇAISE (noms officiels : src/data/text/move_names.h, abilities.h) et
la décompilation anglaise (identifiants : include/constants/*.h ; données : src/data/battle_moves.h).
Tout nom introuvable est signalé : AUCUN remplacement automatique.
"""
import json
import os
import re
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
TYPES_FR = {"NORMAL": "TYPE_NORMAL", "COMBAT": "TYPE_FIGHTING", "VOL": "TYPE_FLYING", "POISON": "TYPE_POISON",
            "SOL": "TYPE_GROUND", "ROCHE": "TYPE_ROCK", "INSECTE": "TYPE_BUG", "SPECTRE": "TYPE_GHOST",
            "ACIER": "TYPE_STEEL", "FEU": "TYPE_FIRE", "EAU": "TYPE_WATER", "PLANTE": "TYPE_GRASS",
            "ELECTRIK": "TYPE_ELECTRIC", "PSY": "TYPE_PSYCHIC", "GLACE": "TYPE_ICE", "DRAGON": "TYPE_DRAGON",
            "TENEBRES": "TYPE_DARK"}
# Orthographes modernes -> orthographe du jeu de 2005 : MÊME attaque, pas un remplacement (documenté dans YOKAI_MOVESETS.md)
SPELLING_ALIASES = {"POING FEU": "POING DE FEU", "LANCE-FLAMMES": "LANCE-FLAMME"}
# génération 3 : la catégorie dépend du TYPE (include/battle.h, IS_TYPE_PHYSICAL : type < TYPE_MYSTERY)
SPECIAL_TYPES = {"TYPE_FIRE", "TYPE_WATER", "TYPE_GRASS", "TYPE_ELECTRIC", "TYPE_PSYCHIC", "TYPE_ICE",
                 "TYPE_DRAGON", "TYPE_DARK"}


def norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", s.upper()).encode("ascii", "ignore").decode()
    return re.sub(r"\s+", " ", s.replace("’", "'")).strip()


def enum_values(path, prefix):
    """#define PREFIX_X N"""
    out = {}
    for m in re.finditer(r"#define\s+(" + prefix + r"\w+)\s+(\d+)\b", open(path).read()):
        out[m.group(1)] = int(m.group(2))
    return out


def text_table(path, prefix):
    return {m.group(1): m.group(2) for m in re.finditer(r"\[(" + prefix + r"\w+)\]\s*=\s*_\(\"([^\"]*)\"\)", open(path, encoding="utf-8").read())}


def battle_moves(path):
    src = open(path).read()
    out = {}
    for m in re.finditer(r"\[(MOVE_\w+)\]\s*=\s*\{(.*?)\n\s*\}", src, re.S):
        body = m.group(2)
        get = lambda k: (re.search(r"\." + k + r"\s*=\s*([^,\n]+)", body) or [None, None])[1]
        out[m.group(1)] = {"type": get("type"), "power": int(get("power") or 0),
                           "accuracy": int(get("accuracy") or 0), "pp": int(get("pp") or 0), "effect": get("effect")}
    return out


def main():
    fr, en = sys.argv[1], sys.argv[2]
    out_json = sys.argv[sys.argv.index("--json") + 1] if "--json" in sys.argv else None
    spec = json.load(open(os.path.join(HERE, "yokai_balance.json"), encoding="utf-8"))
    move_ids = enum_values(os.path.join(en, "include/constants/moves.h"), "MOVE_")
    ab_ids = enum_values(os.path.join(en, "include/constants/abilities.h"), "ABILITY_")
    fr_moves = {norm(v): k for k, v in text_table(os.path.join(fr, "src/data/text/move_names.h"), "MOVE_").items()}
    fr_abil = {norm(v): k for k, v in text_table(os.path.join(fr, "src/data/text/abilities.h"), "ABILITY_").items()}
    data = battle_moves(os.path.join(en, "src/data/battle_moves.h"))
    tms = re.findall(r"F\((\w+)\)", open(os.path.join(en, "include/constants/tms_hms.h")).read())
    problems, resolved = [], {}
    for name, sp in spec["species"].items():
        r = {"types": [], "ability": None, "learnset": [], "tm": [], "hm": []}
        for t in sp["types"]:
            r["types"].append(TYPES_FR.get(norm(t)) or problems.append(f"{name}: type inconnu {t}"))
        k = fr_abil.get(norm(sp["ability"]))
        if not k:
            problems.append(f"{name}: talent introuvable « {sp['ability']} »")
        r["ability"] = {"const": k, "id": ab_ids.get(k)}
        for lvl, mv in sp["learnset"]:
            k = fr_moves.get(norm(mv)) or fr_moves.get(SPELLING_ALIASES.get(norm(mv), ""))
            if not k:
                problems.append(f"{name}: attaque introuvable en génération 3 « {mv} » (niveau {lvl})")
                r["learnset"].append({"level": lvl, "fr": mv, "const": None, "id": None})
                continue
            d = data.get(k, {})
            r["learnset"].append({"level": lvl, "fr": mv, "const": k, "id": move_ids[k], **d,
                                  "alias_of": SPELLING_ALIASES.get(norm(mv)),
                                  "category": "status" if not d.get("power") else ("special" if d.get("type") in SPECIAL_TYPES else "physical")})
        for n in sp["tm"]:
            r["tm"].append({"tm": n, "bit": n - 1, "move": tms[n - 1]})
        for n in sp["hm"]:
            r["hm"].append({"hm": n, "bit": 50 + n - 1, "move": tms[50 + n - 1]})
        resolved[name] = r
    for name, r in resolved.items():
        print(f"== {name}  types={r['types']}  talent={r['ability']['const']}({r['ability']['id']})")
        for e in r["learnset"]:
            if e["const"]:
                print(f"   {e['level']:>2} {e['fr']:<16} -> {e['const']:<22} #{e['id']:<3} {e['type']:<13} pui {e['power']:>3} {e['category']}")
            else:
                print(f"   {e['level']:>2} {e['fr']:<16} -> ??? (à valider)")
        print("   CT/CS :", ", ".join(f"{('CT%02d' % x['tm']) if 'tm' in x else ('CS%02d' % x['hm'])} {x['move']}" for x in r["tm"] + r["hm"]))
    print("\nPROBLÈMES :" if problems else "\nAucun problème.")
    for p in problems:
        print("  -", p)
    if out_json:
        json.dump({"resolved": resolved, "problems": problems}, open(out_json, "w"), indent=1, ensure_ascii=False)


if __name__ == "__main__":
    main()
