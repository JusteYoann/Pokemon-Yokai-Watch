#!/usr/bin/env bash
set -euo pipefail
base=${MGBA_SETUP_ROOT:-/workspace/.setup}
commit=7a12d6d4b9acb14c0ae62c9166b6a2f3d08007f6
command -v cmake >/dev/null || { echo 'Installer CMake et les outils C/C++ (voir DEVELOPPEMENT_YOKAI.md).' >&2; exit 1; }
if [ ! -d "$base/mgba-libretro/.git" ]; then
 git clone https://github.com/libretro/mgba.git "$base/mgba-libretro"
 git -C "$base/mgba-libretro" checkout --detach "$commit"
fi
test "$(git -C "$base/mgba-libretro" rev-parse HEAD)" = "$commit"
cmake -S "$base/mgba-libretro" -B "$base/mgba-build" -DCMAKE_BUILD_TYPE=Release -DBUILD_LIBRETRO=ON -DBUILD_QT=OFF -DBUILD_SDL=OFF -DBUILD_GL=OFF -DBUILD_GLES2=OFF -DBUILD_GLES3=OFF -DBUILD_SHARED=OFF -DUSE_FFMPEG=OFF -DUSE_ZLIB=OFF -DUSE_MINIZIP=OFF -DUSE_PNG=OFF -DUSE_LIBZIP=OFF -DUSE_SQLITE3=OFF -DUSE_ELF=OFF -DUSE_LUA=OFF -DUSE_JSON_C=OFF -DUSE_FREETYPE=OFF -DUSE_LZMA=OFF -DUSE_DISCORD_RPC=OFF
cmake --build "$base/mgba-build" -j4
printf 'Exporter MGBA_LIBRETRO_PATH=%s/mgba-build/mgba_libretro.so\n' "$base"
