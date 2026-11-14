"""FAUX serveur RPC Azahar (SIMULATION) : implémente le même format de paquets que
azahar/src/core/rpc (version 2) sur une mémoire en bytearray, pour tester le pont sans émulateur
ni jeu. Ce n'est PAS Azahar : réussir contre lui prouve seulement que l'encodage du client suit
packet.h / rpc_server.cpp, jamais que le jeu répond.
"""
from __future__ import annotations

import socket
import struct
import threading

from .azahar_rpc import HEADER, MAX_DATA, PROCESS_LIST, PROTOCOL_VERSION, READ_MEMORY, SET_GET_PROCESS, WRITE_MEMORY

GUEST_SIZE = 0x0100_0000        # 16 Mio simulés à partir de 0 (le jeu réel : .text à 0x00100000)


class FakeAzahar:
    def __init__(self, title_id: int, port: int = 0):
        self.mem = bytearray(GUEST_SIZE)
        self.title_id = title_id
        self.pid = 0x28
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("127.0.0.1", port))
        self.port = self.sock.getsockname()[1]
        self.requests = 0
        self._stop = False
        self._thread = threading.Thread(target=self._loop, daemon=True)

    def __enter__(self):
        self._thread.start()
        return self

    def __exit__(self, *exc):
        self._stop = True
        self.sock.close()

    def _loop(self) -> None:
        while not self._stop:
            try:
                raw, peer = self.sock.recvfrom(HEADER.size + MAX_DATA)
            except OSError:
                return
            if len(raw) < HEADER.size:
                continue
            ver, rid, kind, size = HEADER.unpack_from(raw)
            data = raw[HEADER.size:]
            if ver != PROTOCOL_VERSION or size != len(data):     # udp_server.cpp ignore ces paquets
                continue
            self.requests += 1
            a1, a2 = struct.unpack_from("<II", data) if len(data) >= 8 else (0, 0)
            reply = b""
            if kind == READ_MEMORY and 0 < a2 <= MAX_DATA:
                if a1 + a2 <= GUEST_SIZE:
                    reply = bytes(self.mem[a1:a1 + a2])
            elif kind == WRITE_MEMORY and 0 < a2 <= len(data) - 8:
                if a1 + a2 <= GUEST_SIZE:
                    self.mem[a1:a1 + a2] = data[8:8 + a2]
            elif kind == PROCESS_LIST:
                name = b"ctrapp\0\0"
                reply = struct.pack("<I", 1) + struct.pack("<IQ8s", self.pid, self.title_id, name) if a1 == 0 else struct.pack("<I", 0)
            elif kind == SET_GET_PROCESS:
                reply = struct.pack("<I", self.pid) if a1 == 0 else b""
            else:
                continue
            self.sock.sendto(HEADER.pack(ver, rid, kind, len(reply)) + reply, peer)
