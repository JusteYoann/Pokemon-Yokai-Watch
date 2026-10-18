#!/usr/bin/env bash
# Installation utilisateur, sans sudo ; Debian 13 amd64.
set -euo pipefail
repo_root=$(cd "$(dirname "$0")/../.." && pwd)
setup_root=${YOKAI_SETUP_DIR:-/workspace/.setup}
mkdir -p "$setup_root"
setup_root=$(cd "$setup_root" && pwd)
case "$repo_root:$setup_root" in *' '*) echo 'Choisir des chemins sans espaces pour agbcc.' >&2; exit 1;; esac
test "$(dpkg --print-architecture)" = amd64
for executable in git make gcc g++ dpkg-deb apt-get python3; do command -v "$executable" >/dev/null; done
test -f /usr/include/zlib.h || { echo 'Installer zlib1g-dev selon INSTALL.md.' >&2; exit 1; }
test -f /usr/share/keyrings/debian-archive-keyring.gpg
mkdir -p "$setup_root/apt/lists/partial" "$setup_root/apt/cache/archives/partial" "$setup_root/apt/etc" "$setup_root/sysroot"
printf '%s\n' 'deb [signed-by=/usr/share/keyrings/debian-archive-keyring.gpg] https://deb.debian.org/debian trixie main' > "$setup_root/apt/etc/sources.list"
apt_args=(-o "Dir::Etc::sourcelist=$setup_root/apt/etc/sources.list" -o Dir::Etc::sourceparts=- -o Dir::Etc::parts=- -o "Dir::State::lists=$setup_root/apt/lists" -o "Dir::Cache=$setup_root/apt/cache" -o "APT::Sandbox::User=$(id -un)")
apt-get "${apt_args[@]}" update
(
 cd "$setup_root/apt/cache/archives"
 apt-get "${apt_args[@]}" download 'binutils-arm-none-eabi=2.44-3+23+b1' 'libpng-dev=1.6.48-1+deb13u5' 'libpng16-16t64=1.6.48-1+deb13u5'
)
python3 - "$repo_root" "$setup_root" <<'PY'
import hashlib, json, pathlib, shlex, subprocess, sys
repo, setup = map(pathlib.Path, sys.argv[1:])
lock = json.loads((repo/'RECUPERATION_PROJET/OUTILS_DEBIAN.json').read_text())
for item in lock['packages']:
    package = setup/'apt/cache/archives'/item['file']
    assert hashlib.sha256(package.read_bytes()).hexdigest() == item['sha256'], package
    subprocess.run(['dpkg-deb', '-x', str(package), str(setup/'sysroot')], check=True)
prefix = shlex.quote(str(setup/'sysroot'))
(setup/'env.sh').write_text(
    f'export PATH={prefix}/usr/bin:$PATH\n'
    f'export CPATH={prefix}/usr/include:{prefix}/usr/include/libpng16${{CPATH:+:$CPATH}}\n'
    f'export LIBRARY_PATH={prefix}/usr/lib/x86_64-linux-gnu${{LIBRARY_PATH:+:$LIBRARY_PATH}}\n'
    f'export LD_LIBRARY_PATH={prefix}/usr/lib/x86_64-linux-gnu${{LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}}\n'
    f'export PKG_CONFIG_PATH={prefix}/usr/lib/x86_64-linux-gnu/pkgconfig\n'
    f'export PKG_CONFIG_SYSROOT_DIR={prefix}\n')
PY
source "$setup_root/env.sh"
agbcc_commit=da598c1d918402c42c0c0d7128ba14567f3175e9
if [ ! -d "$setup_root/agbcc/.git" ]; then git clone https://github.com/pret/agbcc.git "$setup_root/agbcc"; fi
if [ "$(git -C "$setup_root/agbcc" rev-parse HEAD)" != "$agbcc_commit" ]; then
 test -z "$(git -C "$setup_root/agbcc" status --porcelain)"
 git -C "$setup_root/agbcc" fetch origin "$agbcc_commit"
 git -C "$setup_root/agbcc" checkout --detach "$agbcc_commit"
fi
if [ ! -x "$setup_root/agbcc/agbcc" ] || [ ! -f "$setup_root/agbcc/libc.a" ]; then
 (cd "$setup_root/agbcc" && bash ./build.sh)
fi
# libc's upstream Makefile uses an unsorted find; pin member order so the
# ARM/Thumb linker veneers match the tested B13 on ext4/WSL/overlay filesystems.
python3 "$repo_root/tools/yokai/normaliser_bibliotheques_b13.py" --lib-dir "$setup_root/agbcc" --lock "$repo_root/QA_RECETTE_FINALE/BETA_13_OST/BIBLIOTHEQUES_B13_LOCK.json"
(cd "$setup_root/agbcc" && bash ./install.sh "$repo_root")
arm-none-eabi-as --version | head -1
printf 'Installation terminee. Activer avec : source %s/env.sh\n' "$setup_root"
