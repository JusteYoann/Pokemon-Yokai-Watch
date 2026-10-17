#!/usr/bin/env bash
# Optional native QA tools, separately from the game compiler; no sudo required.
set -euo pipefail
repo_root=$(cd "$(dirname "$0")/../.." && pwd)
setup_root=${YOKAI_SETUP_DIR:-/workspace/.setup}
test -f "$setup_root/env.sh" || bash "$repo_root/RECUPERATION_PROJET/scripts/configurer_outils_debian.sh"
source "$setup_root/env.sh"
if ! command -v cmake >/dev/null; then
 apt_args=(-o "Dir::Etc::sourcelist=$setup_root/apt/etc/sources.list" -o Dir::Etc::sourceparts=- -o Dir::Etc::parts=- -o "Dir::State::lists=$setup_root/apt/lists" -o "Dir::Cache=$setup_root/apt/cache" -o "APT::Sandbox::User=$(id -un)")
 apt-get "${apt_args[@]}" update
 (
  cd "$setup_root/apt/cache/archives"
  apt-get "${apt_args[@]}" download 'cmake=3.31.6-2' 'cmake-data=3.31.6-2' 'librhash1=1.4.5-1' 'libjsoncpp26=1.9.6-3' 'libuv1t64=1.50.0-2'
 )
 python3 - "$repo_root" "$setup_root" <<'PY'
import hashlib,json,pathlib,subprocess,sys
repo,setup=map(pathlib.Path,sys.argv[1:])
metadata=json.loads((repo/'QA_RECETTE_FINALE/RECONSTRUCTION/OUTILS_MGBA.json').read_text())
for item in metadata['cmake_packages_verified_by_signed_apt_metadata']:
    path=setup/'apt/cache/archives'/item['filename']
    assert hashlib.sha256(path.read_bytes()).hexdigest()==item['sha256'],str(path)
    subprocess.run(['dpkg-deb','-x',str(path),str(setup/'sysroot')],check=True)
PY
fi
python3 -c 'import PIL' || { echo 'Installer Pillow selon tools/yokai/requirements.txt dans un environnement Python local.' >&2; exit 1; }
MGBA_SETUP_ROOT="$setup_root" bash "$repo_root/tools/yokai/installer_mgba.sh"
