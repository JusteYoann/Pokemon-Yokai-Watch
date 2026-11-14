"""Client minimal du serveur RPC d'Azahar (UDP), écrit à partir du format décrit dans
azahar/src/core/rpc/packet.h et rpc_server.cpp (pas de copie de dist/scripting/AzaharRPC.py, GPL).

Format (protocole version 2, little-endian) :
    en-tête 16 octets : u32 version, u32 id, u32 type, u32 taille_des_données
    ReadMemory  (1) : données = u32 adresse, u32 taille (1..32 Kio)      -> réponse = octets lus
    WriteMemory (2) : données = u32 adresse, u32 taille, octets          -> réponse vide
    ProcessList (3) : données = u32 début, u32 max                        -> u32 n, n x {u32 pid, u64 title_id, char[8]}
    SetGetProcess (4) : u32 opération (0 = lire, 1 = choisir), u32 pid    -> u32 pid (lecture)

Le serveur traite les requêtes sur le thread d'émulation, entre deux tranches d'exécution
(System::ProcessPendingWork, core.cpp) : une lecture ou une écriture n'est jamais coupée en deux
par le code du jeu. Il doit être activé dans Azahar : Émulation > Configurer > Débogage >
« Enable RPC server » (désactivé par défaut, settings.h : enable_rpc_server{false}).

Bibliothèque standard seulement.
"""
from __future__ import annotations

import random
import socket
import struct
from dataclasses import dataclass

PROTOCOL_VERSION = 2
DEFAULT_PORT = 45987            # udp_server.cpp : port fixe
HEADER = struct.Struct("<IIII")
MAX_DATA = 32 * 1024            # packet.h : MAX_PACKET_DATA_SIZE
READ_MEMORY, WRITE_MEMORY, PROCESS_LIST, SET_GET_PROCESS = 1, 2, 3, 4


class RpcError(Exception):
    pass


@dataclass(frozen=True)
class Process:
    pid: int
    title_id: int
    name: str


class AzaharRpc:
    def __init__(self, host: str = "127.0.0.1", port: int = DEFAULT_PORT, timeout: float = 1.0, retries: int = 3):
        self.addr = (host, port)
        self.timeout = timeout
        self.retries = retries
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(timeout)

    def close(self) -> None:
        self.sock.close()

    # -- transport --------------------------------------------------------------------------
    def _request(self, kind: int, payload: bytes) -> bytes:
        if len(payload) > MAX_DATA:
            raise ValueError("requête trop grande")
        rid = random.getrandbits(32)
        packet = HEADER.pack(PROTOCOL_VERSION, rid, kind, len(payload)) + payload
        for _ in range(self.retries + 1):
            self.sock.sendto(packet, self.addr)
            try:
                while True:
                    raw = self.sock.recv(HEADER.size + MAX_DATA)
                    if len(raw) < HEADER.size:
                        continue
                    ver, got_id, got_kind, size = HEADER.unpack_from(raw)
                    # une réponse tardive à une requête précédente est ignorée (id différent)
                    if ver == PROTOCOL_VERSION and got_id == rid and got_kind == kind and size == len(raw) - HEADER.size:
                        return raw[HEADER.size:]
            except socket.timeout:
                continue
        raise RpcError(f"pas de réponse du serveur RPC {self.addr} (activé dans Azahar ? jeu lancé ?)")

    # -- requêtes ---------------------------------------------------------------------------
    def read(self, address: int, size: int) -> bytes:
        out = bytearray()
        while size > 0:
            n = min(size, MAX_DATA)
            data = self._request(READ_MEMORY, struct.pack("<II", address, n))
            if len(data) != n:
                raise RpcError(f"lecture refusée à 0x{address:08X} ({n} octets)")
            out += data
            address += n
            size -= n
        return bytes(out)

    def write(self, address: int, data: bytes) -> None:
        step = MAX_DATA - 8
        for off in range(0, len(data), step):
            chunk = data[off:off + step]
            self._request(WRITE_MEMORY, struct.pack("<II", address + off, len(chunk)) + chunk)

    def read_u32(self, address: int) -> int:
        return struct.unpack("<I", self.read(address, 4))[0]

    def processes(self) -> list[Process]:
        out: list[Process] = []
        start = 0
        while True:
            data = self._request(PROCESS_LIST, struct.pack("<II", start, 0x7FFFFFFF))
            if len(data) < 4:
                break
            (count,) = struct.unpack_from("<I", data)
            if count == 0:
                break
            for i in range(count):
                pid, tid, name = struct.unpack_from("<IQ8s", data, 4 + i * 0x14)
                out.append(Process(pid, tid, name.rstrip(b"\0").decode("ascii", "replace")))
            start += count
        return out

    def current_process(self) -> int:
        return struct.unpack("<I", self._request(SET_GET_PROCESS, struct.pack("<II", 0, 0)))[0]

    def select_process(self, pid: int) -> None:
        self._request(SET_GET_PROCESS, struct.pack("<II", 1, pid))
