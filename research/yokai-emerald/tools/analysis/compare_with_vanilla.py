#!/usr/bin/env python3
"""Rejoue l'audit de ROM_ANALYSIS.md : compare la ROM Yo-kai à une Émeraude US compilée depuis pret/pokeemerald.

    python3 compare_with_vanilla.py <pokeemerald_modern.gba> <pokeemerald_modern.map> <rom_yokai.gba> <pokeemerald/>

<pokeemerald/> : le dépôt pret/pokeemerald (pour data/maps/map_groups.json) compilé avec `make modern`
(commit 731ad5bfd utilisé pour ROM_ANALYSIS.md). Aucune ROM n'est téléchargée : la vanilla est compilée localement.
"""
import json
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from g3text import dec            # noqa: E402
from gfheader import parse        # noqa: E402
from locate import symbols        # noqa: E402
import wild                       # noqa: E402

R = lambda p: p - 0x08000000


def main(vrom, vmap, hrom, repo):
    V, H = open(vrom, "rb").read(), open(hrom, "rb").read()
    S = symbols(vmap)
    a, b = parse(V), parse(H)
    print("== En-tête GF (champs scalaires différents)")
    for k in a:
        if isinstance(a[k], int) and a[k] != b[k] and not (0x08000000 <= a[k] < 0x0A000000):
            print(f"  {k}: {a[k]:#x} -> {b[k]:#x}")

    print("== Tables vanilla : entrées modifiées")
    for label, key, size, n in (("noms d'espèces", "monSpeciesNames", 11, 412), ("statistiques", "speciesInfo", 28, 412),
                                ("noms d'attaques", "moveNames", 13, 355), ("attaques", "moves", 12, 355),
                                ("noms de talents", "abilityNames", 13, 78)):
        diff = [i for i in range(n) if V[R(a[key]) + i * size:R(a[key]) + (i + 1) * size]
                != H[R(b[key]) + i * size:R(b[key]) + (i + 1) * size]]
        print(f"  {label}: {len(diff)} / {n}")
    nnew = b["pokedexCount"] - a["pokedexCount"]
    names = [dec(H, R(b["monSpeciesNames"]) + sp * 11, 11) for sp in range(412, 412 + nnew)]
    print(f"== Espèces ajoutées ({nnew}) : {', '.join(names)}")

    print("== Rencontres sauvages modifiées")
    va = wild.parse(V, R(S["gWildMonHeaders"]))
    hs = wild.find_headers2(V, H, R(S["gWildMonHeaders"]))
    hb = wild.parse(H, hs)
    mg = json.load(open(os.path.join(repo, "data/maps/map_groups.json")))
    mapn = {(gi, ni): m for gi, g in enumerate(mg["group_order"]) for ni, m in enumerate(mg[g])}
    nm = lambda sp: dec(H, R(b["monSpeciesNames"]) + sp * 11, 11)
    yk = 0
    for e, v in zip(hb, va):
        for k in wild.COUNTS:
            if e.get(k) != v.get(k):
                for j in range(wild.COUNTS[k]):
                    if e[k][j] != v[k][j]:
                        yk += e[k][j][2] >= 412
                        print(f"  {mapn[(e['group'], e['num'])]:30s} {k:5s} {j:2d}: "
                              f"{nm(v[k][j][2])} L{v[k][j][0]}-{v[k][j][1]} -> {nm(e[k][j][2])} L{e[k][j][0]}-{e[k][j][1]}")
    print(f"  ({yk} emplacements Yo-kai)")

    print("== Dresseurs (en-têtes + équipes)")
    vt, n = R(S["gTrainers"]), 855
    first = V[vt + 40 * 1:vt + 40 * 1 + 16]
    ht = H.find(first) - 40
    def party(D, t):
        size, p = D[t + 32], R(struct.unpack_from("<I", D, t + 36)[0])
        sz = 16 if D[t] & 1 else 8
        return [struct.unpack_from("<HHH", D, p + i * sz)[1:] for i in range(size)]
    nd = sum(1 for i in range(n) if V[vt + 40 * i:vt + 40 * i + 32] != H[ht + 40 * i:ht + 40 * i + 32]
             or party(V, vt + 40 * i) != party(H, ht + 40 * i))
    print(f"  {nd} dresseur(s) modifié(s) sur {n}")


if __name__ == "__main__":
    if len(sys.argv) != 5:
        sys.exit(__doc__)
    main(*sys.argv[1:])
