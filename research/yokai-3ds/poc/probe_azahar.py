"""Sonde EN LECTURE SEULE pour Azahar + jeu réel (à lancer sur votre PC). N'écrit jamais en mémoire,
ne touche pas à la sauvegarde. Python 3.10+, bibliothèque standard seulement.

Préalable dans Azahar : Émulation > Configurer > Débogage > cocher « Enable RPC server », puis lancer le jeu.

    python probe_azahar.py info                         # processus, titre reconnu, test de lecture
    python probe_azahar.py read 0x00815244 64           # vidage hexadécimal
    python probe_azahar.py snap 0x08000000 0x400000 avant.bin   # instantané d'une plage
    python probe_azahar.py diff avant.bin apres.bin 0x08000000  # octets qui ont changé entre deux instantanés
    python probe_azahar.py watch 0x00815244 4 [--interval 0.5]  # affiche chaque changement (Ctrl+C pour finir)

Méthode pour trouver un indicateur de progression : `snap` juste avant de finir une quête, `snap` juste
après, `diff` ; recommencer avec une autre quête et garder les adresses qui changent de façon cohérente.
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from ykap.azahar_rpc import AzaharRpc, RpcError   # noqa: E402
from ykap.games import TITLES                       # noqa: E402


def hexdump(base: int, data: bytes) -> None:
    for off in range(0, len(data), 16):
        row = data[off:off + 16]
        print(f"{base + off:08X}  {row.hex(' '):<47}  {''.join(chr(b) if 32 <= b < 127 else '.' for b in row)}")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--host", default="127.0.0.1")
    p.add_argument("--port", type=int, default=45987)
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("info")
    r = sub.add_parser("read"); r.add_argument("addr"); r.add_argument("size")
    s = sub.add_parser("snap"); s.add_argument("addr"); s.add_argument("size"); s.add_argument("out")
    d = sub.add_parser("diff"); d.add_argument("a"); d.add_argument("b"); d.add_argument("base")
    w = sub.add_parser("watch"); w.add_argument("addr"); w.add_argument("size"); w.add_argument("--interval", type=float, default=0.5)
    a = p.parse_args()
    num = lambda x: int(x, 0)

    if a.cmd == "diff":
        x, y, base = Path(a.a).read_bytes(), Path(a.b).read_bytes(), num(a.base)
        changes = [(i, x[i], y[i]) for i in range(min(len(x), len(y))) if x[i] != y[i]]
        for i, old, new in changes[:500]:
            print(f"{base + i:08X}: {old:02X} -> {new:02X}")
        print(f"{len(changes)} octets modifiés")
        return 0

    rpc = AzaharRpc(a.host, a.port, timeout=1.0)
    try:
        if a.cmd == "info":
            procs = rpc.processes()
            for pr in procs:
                print(f"pid {pr.pid:3d}  {pr.title_id:016X}  {pr.name:8s}  {TITLES.get(pr.title_id, '')}")
            games = [pr for pr in procs if pr.title_id in TITLES]
            if not games:
                print("Aucun jeu Yo-kai Watch reconnu parmi les processus.")
                return 1
            print("Processus courant du RPC :", rpc.current_process())
            print("Début de .text (0x00100000) :", rpc.read(0x00100000, 16).hex(" "))
        elif a.cmd == "read":
            hexdump(num(a.addr), rpc.read(num(a.addr), num(a.size)))
        elif a.cmd == "snap":
            data = rpc.read(num(a.addr), num(a.size))
            Path(a.out).write_bytes(data)
            print(f"{len(data)} octets écrits dans {a.out}")
        elif a.cmd == "watch":
            addr, size, last = num(a.addr), num(a.size), None
            while True:
                cur = rpc.read(addr, size)
                if cur != last:
                    print(time.strftime("%H:%M:%S"), cur.hex(" "), flush=True)
                    last = cur
                time.sleep(a.interval)
    except RpcError as e:
        print("Erreur :", e)
        return 2
    except KeyboardInterrupt:
        return 0
    finally:
        rpc.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
