"""Boîte aux lettres jeu <-> client : PROPOSITION de protocole commun aux trois jeux 3DS.

Inspirée de l'architecture éprouvée du mod Yo-kai Watch 2 Archipelago (boite_protocole.py : zone fixe
en mémoire du jeu, dons numérotés, compteur « déjà livré » gardé dans la sauvegarde, journal des
checks + relecture de bits persistants), mais SIMPLIFIÉE et indépendante de son code. Le côté « jeu »
n'existe pas encore : il faudra l'écrire en patch de code (code.bps) pour chaque jeu et chaque région.

Disposition (little-endian), à une adresse BASE choisie par jeu (zone libre, ex. fin de .bss étendue
via exheader). C = écrit par le client, G = écrit par le jeu.

  +0x000 u32 magic 'YKAP' (G)          +0x004 u16 version (G), u16 game_id (G)
  +0x008 u32 save_link (G, lu depuis la sauvegarde ; C l'écrit une fois sur partie neuve, voir link())
  +0x00C u32 applied_count (G, PERSISTÉ dans la sauvegarde : nb d'objets AP déjà appliqués)
  +0x010 u32 gift_count (C, écrit EN DERNIER)   +0x014 u32 journal_count (G, monotone)
  +0x018 u32 status (G : bit0 = moment sûr pour donner, bit1 = victoire, bit2 = sauvegarde chargée)
  +0x01C u32 heartbeat (C)
  +0x040 gifts[32]  : {u32 ap_index, u32 item_code}   (C)
  +0x140 journal[64]: u32 location_code               (G, anneau : entrée i % 64)
  +0x240 bits[128 octets] : 1024 locations persistantes (G, reflet des flags de la sauvegarde)

Règles qui empêchent les doublons et survivent aux déconnexions :
- le jeu n'applique un don que si ap_index == applied_count, puis incrémente applied_count dans la
  MÊME écriture de sauvegarde que l'objet (atomique du point de vue du joueur) ;
- le client réécrit sans risque toute la file à chaque tour : un don déjà appliqué est ignoré ;
- les checks sont reconstruits depuis `bits` à chaque connexion : un journal perdu ne perd rien.
"""
from __future__ import annotations

import struct
from typing import Protocol

MAGIC = int.from_bytes(b"YKAP", "little")
VERSION = 1
OFF_MAGIC, OFF_VERSION, OFF_LINK, OFF_APPLIED, OFF_GIFT_COUNT, OFF_JOURNAL_COUNT, OFF_STATUS, OFF_HEARTBEAT = (
    0x000, 0x004, 0x008, 0x00C, 0x010, 0x014, 0x018, 0x01C)
OFF_GIFTS, GIFT_CAP = 0x040, 32
OFF_JOURNAL, JOURNAL_CAP = 0x140, 64
OFF_BITS, BITS_BYTES = 0x240, 128
SIZE = OFF_BITS + BITS_BYTES
STATUS_SAFE, STATUS_GOAL, STATUS_LOADED = 0x1, 0x2, 0x4


class Memory(Protocol):
    def read(self, address: int, size: int) -> bytes: ...
    def write(self, address: int, data: bytes) -> None: ...


class Mailbox:
    """Vue côté client."""

    def __init__(self, mem: Memory, base: int):
        self.mem, self.base = mem, base

    def snapshot(self) -> dict:
        raw = self.mem.read(self.base, SIZE)
        magic, ver_game, link, applied, gifts, jcount, status, _ = struct.unpack_from("<8I", raw)
        return {
            "valid": magic == MAGIC and (ver_game & 0xFFFF) == VERSION,
            "game_id": ver_game >> 16, "save_link": link, "applied": applied, "gift_count": gifts,
            "journal_count": jcount, "status": status,
            "journal": [struct.unpack_from("<I", raw, OFF_JOURNAL + 4 * i)[0] for i in range(JOURNAL_CAP)],
            "bits": raw[OFF_BITS:OFF_BITS + BITS_BYTES],
        }

    @staticmethod
    def done_locations(snap: dict) -> set[int]:
        bits = snap["bits"]
        return {i for i in range(BITS_BYTES * 8) if bits[i >> 3] >> (i & 7) & 1}

    def link(self, seed_link: int) -> None:
        self.mem.write(self.base + OFF_LINK, struct.pack("<I", seed_link))

    def post_gifts(self, items: list[tuple[int, int]], applied: int) -> int:
        """items = [(ap_index, item_code)] reçus du serveur. Écrit ceux >= applied (max GIFT_CAP)."""
        pending = [(i, c) for i, c in items if i >= applied][:GIFT_CAP]
        body = b"".join(struct.pack("<II", i, c) for i, c in pending)
        if body:
            self.mem.write(self.base + OFF_GIFTS, body)
        self.mem.write(self.base + OFF_GIFT_COUNT, struct.pack("<I", len(pending)))   # en dernier
        return len(pending)

    def heartbeat(self, n: int) -> None:
        self.mem.write(self.base + OFF_HEARTBEAT, struct.pack("<I", n & 0xFFFFFFFF))


class SimulatedGameSide:
    """SIMULATION du code qu'il faudra patcher dans le jeu. Sert uniquement aux tests du client.

    `save` imite la sauvegarde : ce qui y est survit à un « redémarrage » (restart())."""

    def __init__(self, mem: Memory, base: int, game_id: int, n_locations: int):
        self.mem, self.base, self.game_id = mem, base, game_id
        self.save = {"link": 0, "applied": 0, "inventory": [], "flags": set()}
        self.n_locations = n_locations
        self.jcount = 0
        self.restart()

    def restart(self) -> None:
        """Le jeu (re)démarre et charge la sauvegarde : la zone est reconstruite depuis celle-ci."""
        hdr = struct.pack("<IHHIIIIII", MAGIC, VERSION, self.game_id, self.save["link"], self.save["applied"],
                          0, self.jcount, STATUS_SAFE | STATUS_LOADED, 0)
        self.mem.write(self.base, hdr + bytes(SIZE - len(hdr)))
        self._write_bits()

    def _write_bits(self) -> None:
        bits = bytearray(BITS_BYTES)
        for loc in self.save["flags"]:
            bits[loc >> 3] |= 1 << (loc & 7)
        self.mem.write(self.base + OFF_BITS, bytes(bits))

    def complete(self, loc: int) -> None:
        """Le joueur finit une mission / quête : flag persistant + entrée de journal."""
        self.save["flags"].add(loc)
        self.mem.write(self.base + OFF_JOURNAL + 4 * (self.jcount % JOURNAL_CAP), struct.pack("<I", loc))
        self.jcount += 1
        self.mem.write(self.base + OFF_JOURNAL_COUNT, struct.pack("<I", self.jcount))
        self._write_bits()

    def frame(self) -> None:
        """Appelé « à chaque image » : consomme les dons dans l'ordre, sans doublon."""
        raw = self.mem.read(self.base, SIZE)
        link = struct.unpack_from("<I", raw, OFF_LINK)[0]
        if self.save["link"] == 0 and link:
            self.save["link"] = link                 # liaison d'une partie neuve
        if link != self.save["link"]:
            return                                   # autre partie AP : on n'applique rien
        count = struct.unpack_from("<I", raw, OFF_GIFT_COUNT)[0]
        for k in range(min(count, GIFT_CAP)):
            idx, code = struct.unpack_from("<II", raw, OFF_GIFTS + 8 * k)
            if idx == self.save["applied"]:
                self.save["inventory"].append(code)  # jeu réel : appel de la fonction interne « donner objet »
                self.save["applied"] += 1            # même écriture de sauvegarde que l'objet
        self.mem.write(self.base + OFF_APPLIED, struct.pack("<I", self.save["applied"]))
