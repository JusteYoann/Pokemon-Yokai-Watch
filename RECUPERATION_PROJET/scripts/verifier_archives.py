#!/usr/bin/env python3
"""Lit les archives d'origine sans extraction et vérifie chaque membre récupéré."""
import ctypes as c
import ctypes.util
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
library = ctypes.util.find_library('archive')
if not library:
    raise SystemExit('Installer libarchive13 (Debian) ou libarchive équivalent.')
L = c.CDLL(library)
for name, args, result in [
    ('archive_read_new', [], c.c_void_p),
    ('archive_read_support_filter_all', [c.c_void_p], c.c_int),
    ('archive_read_support_format_all', [c.c_void_p], c.c_int),
    ('archive_read_open_filename', [c.c_void_p, c.c_char_p, c.c_size_t], c.c_int),
    ('archive_read_next_header', [c.c_void_p, c.POINTER(c.c_void_p)], c.c_int),
    ('archive_entry_pathname_utf8', [c.c_void_p], c.c_char_p),
    ('archive_entry_filetype', [c.c_void_p], c.c_uint),
    ('archive_read_data', [c.c_void_p, c.c_void_p, c.c_size_t], c.c_longlong),
    ('archive_read_free', [c.c_void_p], c.c_int),
]:
    function = getattr(L, name)
    function.argtypes, function.restype = args, result

rows = json.loads((ROOT / 'RECUPERATION_PROJET/ARCHIVES_RECUPEREES.json').read_text())
expected = {(row['archive_path'], row['member']): row for row in rows}
seen = set()
for path in sorted({row['archive_path'] for row in rows}):
    archive = L.archive_read_new()
    L.archive_read_support_filter_all(archive)
    L.archive_read_support_format_all(archive)
    assert L.archive_read_open_filename(archive, str(ROOT / path).encode(), 10240) == 0
    try:
        entry = c.c_void_p()
        while True:
            code = L.archive_read_next_header(archive, c.byref(entry))
            if code == 1:
                break
            assert code == 0, (path, code)
            if L.archive_entry_filetype(entry) != 0o100000:
                continue
            member = L.archive_entry_pathname_utf8(entry).decode()
            key = (path, member)
            assert key in expected and key not in seen, key
            digest, size = hashlib.sha256(), 0
            buffer = c.create_string_buffer(65536)
            while True:
                count = L.archive_read_data(archive, buffer, len(buffer))
                assert count >= 0, key
                if count == 0:
                    break
                digest.update(buffer.raw[:count])
                size += count
            assert size == expected[key]['size'] and digest.hexdigest() == expected[key]['sha256'], key
            seen.add(key)
    finally:
        L.archive_read_free(archive)
assert seen == set(expected)
for record in json.loads((ROOT / 'RECUPERATION_PROJET/PROVENANCE_ARCHIVES.json').read_text()):
    data = (ROOT / record['path']).read_bytes()
    assert len(data) == record['size'] and hashlib.sha256(data).hexdigest() == record['sha256']
print(f'{len(seen)} membres verifies dans {len({p for p, n in seen})} archives, sans extraction.')
