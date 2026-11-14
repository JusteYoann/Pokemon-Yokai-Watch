"""Banc d'essai des prototypes A (pont RPC Azahar, contre un FAUX Azahar) et C (client Archipelago,
contre un VRAI serveur Archipelago local). Le jeu est SIMULÉ (mailbox.SimulatedGameSide).

    python run_poc.py --archipelago <dépôt Archipelago> --multidata <AP_xxx.zip> [--python <python du venv>]

Chaque étape affiche OK/ÉCHEC ; le code de sortie est 0 seulement si tout passe.
Rien ici ne prouve qu'un jeu Yo-kai Watch réel réagit : voir PROTOTYPE_RESULTS.md.
"""
from __future__ import annotations

import argparse
import asyncio
import json
import logging
import os
import subprocess
import sys
import time
import uuid
from pathlib import Path

import websockets

sys.path.insert(0, str(Path(__file__).parent))
from ykap.ap_client import ApBridge, Session                       # noqa: E402
from ykap.azahar_rpc import AzaharRpc                               # noqa: E402
from ykap.fake_azahar import FakeAzahar                             # noqa: E402
from ykap.games import TITLES                                       # noqa: E402
from ykap.mailbox import Mailbox, SimulatedGameSide, STATUS_GOAL, OFF_STATUS   # noqa: E402

YW2_EUR = 0x00040000001B2900
BASE = 0x00A0_0000            # adresse fictive de la boîte dans la mémoire simulée
PORT = 38281
results: list[tuple[str, bool, str]] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    results.append((name, ok, detail))
    print(f"[{'OK' if ok else 'ÉCHEC'}] {name}" + (f" — {detail}" if detail else ""), flush=True)


class Direct:
    """Accès direct du « jeu » simulé à la mémoire du faux Azahar (le jeu n'utilise pas le RPC)."""
    def __init__(self, fake: FakeAzahar):
        self.m = fake.mem
    def read(self, a, n):
        return bytes(self.m[a:a + n])
    def write(self, a, d):
        self.m[a:a + len(d)] = d


async def partner_checks_everything(server: str) -> int:
    async with websockets.connect(server) as ws:
        await ws.recv()   # RoomInfo
        await ws.send(json.dumps([{"cmd": "Connect", "password": "", "game": "APQuest", "name": "Partner",
                                   "uuid": str(uuid.uuid4()), "items_handling": 0, "tags": [], "slot_data": False,
                                   "version": {"major": 0, "minor": 6, "build": 0, "class": "Version"}}]))
        while True:
            for m in json.loads(await ws.recv()):
                if m["cmd"] == "Connected":
                    locs = m["missing_locations"]
                    await ws.send(json.dumps([{"cmd": "LocationChecks", "locations": locs}]))
                    await asyncio.sleep(0.5)
                    return len(locs)


async def wait_for(pred, timeout=8.0) -> bool:
    end = time.monotonic() + timeout
    while time.monotonic() < end:
        if pred():
            return True
        await asyncio.sleep(0.05)
    return False


async def scenario(server: str) -> None:
    # --- Prototype A (simulation) : le protocole RPC tel que packet.h le décrit ---
    with FakeAzahar(YW2_EUR) as fake:
        rpc = AzaharRpc(port=fake.port, timeout=0.5)
        procs = rpc.processes()
        check("A1 RPC : liste des processus et identification du titre",
              len(procs) == 1 and procs[0].title_id == YW2_EUR, TITLES.get(procs[0].title_id, "?"))
        fake.mem[0x00815244:0x00815248] = (0x1234).to_bytes(4, "little")
        check("A2 RPC : lecture u32 (lecture seule, aucune écriture)", rpc.read_u32(0x00815244) == 0x1234)
        big = bytes(range(256)) * 200            # 51 200 octets : plus que 32 Kio, découpé en plusieurs paquets
        rpc.write(0x00200000, big)
        check("A3 RPC : lecture/écriture > 32 Kio découpées", rpc.read(0x00200000, len(big)) == big)

        # --- Prototype C : vrai serveur Archipelago, jeu simulé derrière le faux Azahar ---
        game = SimulatedGameSide(Direct(fake), BASE, game_id=2, n_locations=32)
        box = Mailbox(rpc, BASE)
        sess = Session(server=server, slot="YokaiPoC", game="APQuest")
        bridge = ApBridge(sess, box, poll=0.05)

        async def game_frames():
            while True:
                game.frame()
                await asyncio.sleep(0.02)
        gtask = asyncio.create_task(game_frames())
        btask = asyncio.create_task(bridge.run_forever())

        ok = await wait_for(lambda: game.save["link"] != 0)
        check("C1 connexion au serveur et liaison d'une sauvegarde neuve", ok, f"link=0x{game.save['link']:08X}")
        n_slot = len(sess.slot_locations)

        for loc in (0, 1, 2):
            game.complete(loc)
        ok = await wait_for(lambda: sess.stats["checks_sent"] >= 3)
        check("C2 trois missions finies -> LocationChecks", ok, f"{sess.stats['checks_sent']} envoyés / {n_slot} locations")

        sent_by_partner = await partner_checks_everything(server)
        ok = await wait_for(lambda: len(sess.received) > 0 and game.save["applied"] == len(sess.received))
        check("C3 objets d'un autre joueur reçus et appliqués dans l'ordre", ok,
              f"partenaire a fait {sent_by_partner} checks ; reçus {len(sess.received)}, appliqués {game.save['applied']}")
        before = list(game.save["inventory"])

        await bridge.ws.close()                      # coupure réseau
        ok = await wait_for(lambda: sess.stats["connections"] >= 2, timeout=10)
        await asyncio.sleep(0.5)
        check("C4 reconnexion automatique sans doublon", ok and game.save["inventory"] == before,
              f"connexions={sess.stats['connections']}, inventaire {len(before)} -> {len(game.save['inventory'])}")

        game.restart()                               # le jeu est relancé : zone reconstruite depuis la sauvegarde
        await asyncio.sleep(0.5)
        check("C5 redémarrage du jeu : rien de réappliqué, checks gardés",
              game.save["inventory"] == before and {0, 1, 2} <= game.save["flags"])
        check("C6 inventaire = exactement la liste reçue du serveur",
              game.save["inventory"] == [c for _, c in sess.received])

        for loc in range(3, n_slot):
            game.complete(loc)
        game.mem.write(BASE + OFF_STATUS, (STATUS_GOAL | 1 | 4).to_bytes(4, "little"))
        ok = await wait_for(lambda: sess.goal_sent and sess.stats["checks_sent"] == n_slot)
        check("C7 toutes les locations + victoire envoyées", ok, f"{sess.stats['checks_sent']}/{n_slot}")

        # sauvegarde d'une AUTRE partie AP : le client ne doit rien donner
        game.save.update(link=0xDEADBEEF, applied=0, inventory=[])
        game.restart()
        await asyncio.sleep(0.6)
        check("C8 sauvegarde liée à une autre graine : aucun objet donné", game.save["inventory"] == [])

        bridge.stop.set()
        gtask.cancel()
        await asyncio.gather(btask, return_exceptions=True)
        rpc.close()
        print(f"   (requêtes RPC servies par le faux Azahar : {fake.requests})")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--archipelago", required=True)
    ap.add_argument("--multidata", required=True)
    ap.add_argument("--python", default=sys.executable)
    a = ap.parse_args()
    logging.basicConfig(level=logging.WARNING)
    env = dict(os.environ, SKIP_REQUIREMENTS_UPDATE="1")
    log_path = Path(a.multidata).with_suffix(".server.log")
    with open(log_path, "w") as log_file:
        srv = subprocess.Popen([a.python, "MultiServer.py", "--port", str(PORT), "--loglevel", "info", a.multidata],
                               cwd=a.archipelago, stdin=subprocess.DEVNULL, stdout=log_file, stderr=subprocess.STDOUT,
                               env=env)
        try:
            asyncio.run(asyncio.wait_for(_wait_port(), 60))
            asyncio.run(scenario(f"ws://127.0.0.1:{PORT}"))
        finally:
            srv.terminate()
            srv.wait(10)
    text = log_path.read_text(errors="replace")
    check("C9 le serveur a enregistré la victoire (journal du serveur)", "has completed their goal" in text)
    print(f"\n{sum(ok for _, ok, _ in results)}/{len(results)} étapes réussies ; journal serveur : {log_path}")
    return 0 if all(ok for _, ok, _ in results) else 1


async def _wait_port() -> None:
    while True:
        try:
            async with websockets.connect(f"ws://127.0.0.1:{PORT}"):
                return
        except OSError:
            await asyncio.sleep(0.5)


if __name__ == "__main__":
    sys.exit(main())
