"""Client Archipelago minimal (prototype C) : protocole réseau d'Archipelago 0.6.x en direct
(websockets), sans dépendre de CommonClient, branché sur une boîte aux lettres (mailbox.py).

Ce que fait une itération :
  1. lit la boîte (une lecture groupée) ;
  2. checks = bits persistants du jeu -> LocationChecks (renvoyés après chaque reconnexion) ;
  3. objets reçus (ReceivedItems, index AP) -> file de dons ; le jeu les applique et compte ;
  4. bit de victoire -> StatusUpdate CLIENT_GOAL (une fois par connexion).
Les doublons sont impossibles côté jeu (compteur dans la sauvegarde) ; côté serveur, LocationChecks
est idempotent. Une coupure réseau ou un redémarrage du jeu se rattrapent sans état local.
"""
from __future__ import annotations

import asyncio
import json
import logging
import uuid
from dataclasses import dataclass, field

import websockets

from .mailbox import Mailbox, STATUS_GOAL

log = logging.getLogger("ykap")
CLIENT_GOAL = 30


@dataclass
class Session:
    server: str
    slot: str
    game: str
    password: str = ""
    items_handling: int = 0b111       # objets d'autres mondes + les nôtres (+ départ) : le jeu ne donne pas les siens
    # état réseau (reconstruit à chaque connexion)
    received: list[tuple[int, int]] = field(default_factory=list)   # (index AP, id objet AP)
    slot_locations: list[int] = field(default_factory=list)          # ids AP triés : code local = position
    checked: set[int] = field(default_factory=set)
    goal_sent: bool = False
    seed_link: int = 0
    stats: dict = field(default_factory=lambda: {"connections": 0, "checks_sent": 0, "items": 0})


class ApBridge:
    def __init__(self, session: Session, mailbox: Mailbox, poll: float = 0.1):
        self.s, self.box, self.poll = session, mailbox, poll
        self.ws = None
        self.connected = asyncio.Event()
        self.stop = asyncio.Event()

    async def _send(self, *msgs: dict) -> None:
        await self.ws.send(json.dumps(list(msgs)))

    async def _on(self, msg: dict) -> None:
        cmd = msg["cmd"]
        if cmd == "RoomInfo":
            self.s.seed_link = int.from_bytes(msg["seed_name"].encode()[-4:].rjust(4, b"\0"), "little") or 1
            await self._send({"cmd": "Connect", "password": self.s.password, "game": self.s.game,
                              "name": self.s.slot, "uuid": str(uuid.uuid4()),
                              "version": {"major": 0, "minor": 6, "build": 0, "class": "Version"},
                              "items_handling": self.s.items_handling, "tags": [], "slot_data": True})
        elif cmd == "Connected":
            self.s.slot_locations = sorted(set(msg["missing_locations"]) | set(msg["checked_locations"]))
            self.s.checked = set(msg["checked_locations"])
            self.s.received.clear()
            self.s.goal_sent = False
            self.s.stats["connections"] += 1
            self.connected.set()
            log.info("connecté : %d locations, %d déjà faites", len(self.s.slot_locations), len(self.s.checked))
        elif cmd == "ConnectionRefused":
            raise ConnectionError(f"refusé : {msg.get('errors')}")
        elif cmd == "ReceivedItems":
            start = msg["index"]
            if start == 0:
                self.s.received.clear()
            if start != len(self.s.received):                 # trou : on redemande tout
                await self._send({"cmd": "Sync"})
                return
            for it in msg["items"]:
                self.s.received.append((len(self.s.received), it["item"]))
            self.s.stats["items"] = len(self.s.received)

    async def _reader(self) -> None:
        async for raw in self.ws:
            for msg in json.loads(raw):
                await self._on(msg)

    async def _game_loop(self) -> None:
        await self.connected.wait()
        beat = 0
        while not self.stop.is_set():
            snap = self.box.snapshot()
            if snap["valid"]:
                if snap["save_link"] == 0:
                    self.box.link(self.s.seed_link)          # partie neuve : on la lie à cette graine
                elif snap["save_link"] == self.s.seed_link:  # sinon : autre partie, on ne touche à rien
                    done = {self.s.slot_locations[i] for i in Mailbox.done_locations(snap)
                            if i < len(self.s.slot_locations)}
                    new = sorted(done - self.s.checked)
                    if new:
                        await self._send({"cmd": "LocationChecks", "locations": new})
                        self.s.checked |= set(new)
                        self.s.stats["checks_sent"] += len(new)
                    self.box.post_gifts(self.s.received, snap["applied"])
                    if snap["status"] & STATUS_GOAL and not self.s.goal_sent:
                        await self._send({"cmd": "StatusUpdate", "status": CLIENT_GOAL})
                        self.s.goal_sent = True
            beat += 1
            self.box.heartbeat(beat)
            await asyncio.sleep(self.poll)

    async def run_once(self) -> None:
        """Une connexion ; rend la main à la déconnexion."""
        self.connected.clear()
        async with websockets.connect(self.s.server, max_size=None) as ws:
            self.ws = ws
            reader = asyncio.create_task(self._reader())
            game = asyncio.create_task(self._game_loop())
            done, pending = await asyncio.wait({reader, game, asyncio.create_task(self.stop.wait())},
                                               return_when=asyncio.FIRST_COMPLETED)
            for t in pending:
                t.cancel()
            for t in done:
                if t.exception() and not isinstance(t.exception(), websockets.ConnectionClosed):
                    raise t.exception()

    async def run_forever(self) -> None:
        delay = 1.0
        while not self.stop.is_set():
            try:
                await self.run_once()
                delay = 1.0
            except (OSError, websockets.ConnectionClosed) as e:
                log.warning("déconnecté (%s), nouvel essai dans %.0f s", e, delay)
                await asyncio.sleep(delay)
                delay = min(delay * 2, 30)
