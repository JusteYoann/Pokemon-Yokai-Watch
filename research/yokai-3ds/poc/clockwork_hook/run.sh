#!/usr/bin/env bash
# Prototype B : crochet sur du C émis par le recompilateur de Clockwork, avec un programme ARM SYNTHÉTIQUE.
# Usage : ./run.sh <dépôt clockwork>     (demande : cargo, clang, llvm-mc, ld.lld, llvm-objcopy, python3)
set -euo pipefail
CW=$(cd "$1" && pwd); cd "$(dirname "$0")"
(cd "$CW" && cargo build --release -q -p recomp)
llvm-mc -triple=armv6k-none-eabi -filetype=obj synthetic.s -o synthetic.o
ld.lld -Ttext=0x100000 synthetic.o -o synthetic.elf 2>/dev/null
llvm-objcopy -O binary --only-section=.text synthetic.elf text.bin
mkdir -p extracted && python3 - <<'EOF'
import struct
text = open('text.bin', 'rb').read()
code = bytearray(0x2000); code[:len(text)] = text
open('extracted/code.bin', 'wb').write(code)
ex = bytearray(0x400)            # seuls les champs lus par tools/recomp/src/image.rs
struct.pack_into('<I', ex, 0x10, 0x100000); struct.pack_into('<I', ex, 0x18, len(text))
struct.pack_into('<I', ex, 0x20, 0x101000); struct.pack_into('<I', ex, 0x30, 0x101000)
struct.pack_into('<I', ex, 0x38, 0x100)
open('extracted/exheader.bin', 'wb').write(ex)
EOF
rm -rf gen && "$CW/target/release/recomp" emit extracted gen
python3 inject_hooks.py gen 00100020 00100038
clang -O2 -std=c17 -w -I"$CW/runtime/include" -Igen harness.c gen/recomp_0010.c "$CW/runtime/src/arm_ops.c" -o harness -lm
./harness && echo "PROTOTYPE B : OK (simulation, code synthétique)"
