# Fichiers privés de Pokémon Yo-kai Emerald : où ils sont, comment les régénérer

Ces fichiers ne sont **pas** dans git (ROM, graphismes du créateur, code et données de Pokémon Émeraude). Ils ont été
remis directement à l'utilisateur dans l'archive `yokai_emerald_private.zip` (38 Mio,
SHA-1 `f18207f2c78d7a89c3b359eb66d73054e387edd2`), à transmettre à Codex hors GitHub. Contenu détaillé et sommes de
contrôle : `LISEZMOI.md` et `MANIFEST_SHA1.txt` dans l'archive.

| Fichier attendu par Codex | Dans l'archive | Régénération à partir du dépôt |
|---|---|---|
| ROM originale du hack (SHA-1 `ff71db05…`) | `roms/hack_original_pokemon_yokai_emerald.gba` | non régénérable : fichier de l'utilisateur (publication de SnappleRainKirby sur X) |
| Build compatible Archipelago (`pokemon emerald / yokai ap v0.1`) | `build_ap_en/pokeemerald_yokai_ap.gba` (`393fc878…`) | `SCRIPTS/build_emerald.sh <hack> <emeraude_US> us <travail>` -> `<travail>/build/pokeemerald_ap_flit.gba` |
| Fichiers `.map` | `build_ap_en/pokeemerald_yokai_ap.map`, `build_pret_en/pokeemerald_yokai_sans_ap.map` | produits par `make` dans le dossier de build |
| `.apworld` | `apworld/pokemon_yokai_emerald.apworld` (`ef18c5b4…`, base US) | même script -> `<travail>/apworld/pokemon_yokai_emerald.apworld` |
| `base_patch.bsdiff4`, `extracted_data.json` | `build_ap_en/` | `make extract` (Node.js + bsdiff4 ; Émeraude US copiée en `pokeemerald.gba`) |
| Couche Yo-kai en sources | `source_layer/yokai_layer_on_flit_fd64301.patch` (`git apply` sur FlitPix/pokeemerald `fd64301`) | `PATCHES/pokemon_yokai_emerald/yokai_source_patch.py <decomp> <hack> --lang en` |
| Partie de test + ROM patchée | `test_multiworld/` | `Generate.py` avec `CONFIG/` puis `TESTS/apply_yokai_patch.py` |
| Émeraude US vanilla (`f3ae0881…`) | **absente** (ROM commerciale non fournie par l'utilisateur) | `git clone https://github.com/pret/pokeemerald && git checkout 731ad5bfd && make` (agbcc), ou dump personnel |
| Émeraude France (`ca666651…`) | **absente** (déjà en possession de l'utilisateur) | dump personnel |

Rappel : ne jamais placer ces fichiers dans le dépôt (voir `AGENTS.md`, « Interdits »).
