"""Injecte des points d'interception dans le C émis par `recomp emit` (Clockwork), AVANT compilation.
f_XXXXXXXX devient f_XXXXXXXX_orig ; un nouveau f_XXXXXXXX appelle ykap_hook(addr, phase, ctx) autour
de l'original. Les appelants directs et la table lookup.c passent donc par le crochet sans être modifiés.
    python inject_hooks.py <dossier généré> <adresse hex>...
"""
import re, sys
from pathlib import Path

gen = Path(sys.argv[1]); addrs = [int(a, 16) for a in sys.argv[2:]]
for c in gen.glob("*.c"):
    if c.name == "lookup.c":
        continue
    src = c.read_text()
    for a in addrs:
        name = f"f_{a:08x}"
        pat = f"void {name}(Ctx *RECOMP_RESTRICT ctx) {{"
        if pat in src:
            src = src.replace(pat, f"void {name}_orig(Ctx *RECOMP_RESTRICT ctx) {{", 1)
            src += (f"\nvoid ykap_hook(uint32_t addr, int phase, Ctx *ctx);\n"
                    f"void {name}(Ctx *RECOMP_RESTRICT ctx) {{\n"
                    f"    ykap_hook(0x{a:08x}u, 0, ctx);\n    {name}_orig(ctx);\n    ykap_hook(0x{a:08x}u, 1, ctx);\n}}\n")
            src = src.replace(f'#include "funcs.h"', f'#include "funcs.h"\nvoid {name}_orig(Ctx *RECOMP_RESTRICT ctx);', 1)
            print(f"crochet posé sur {name} ({c.name})")
    c.write_text(src)
