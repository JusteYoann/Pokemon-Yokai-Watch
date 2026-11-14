# BUILD_GUIDE — reconstruire, analyser, tester

Tout se fait à partir de **vos** fichiers : votre ROM du hack, votre cartouche Émeraude. Aucune ROM n'est fournie
ni téléchargée. Sous Windows, utilisez WSL2 (Ubuntu 24.04), comme le recommande pret.

## 0. Prérequis (Ubuntu / WSL2)

```sh
sudo apt install build-essential git libpng-dev binutils-arm-none-eabi gcc-arm-none-eabi libnewlib-arm-none-eabi python3-pip
pip install pillow
```

## 1. Référence vanilla et audit de la ROM du hack

```sh
git clone https://github.com/pret/agbcc && git clone https://github.com/pret/pokeemerald
(cd agbcc && ./build.sh && ./install.sh ../pokeemerald)
cd pokeemerald && git checkout 731ad5bfd && make tools
make -j"$(nproc)"                      # pokeemerald.gba : doit afficher sha1 f3ae0881… (= Émeraude US)
make modern -j"$(nproc)"               # pokeemerald_modern.gba + .map : la référence de comparaison
cd ..
python3 Pokemon-Yokai-Watch/research/yokai-emerald/tools/analysis/compare_with_vanilla.py \
    pokeemerald/pokeemerald_modern.gba pokeemerald/pokeemerald_modern.map <rom_yokai.gba> pokeemerald
python3 Pokemon-Yokai-Watch/research/yokai-emerald/tools/yokai_extract.py <rom_yokai.gba> yokai_out
```

`yokai_out/` contient les données et graphismes du créateur : **ne le versionnez pas** (`.gitignore`).

## 2. Décompilation française (à vérifier sur votre PC)

```sh
git clone https://github.com/qigast/pokeemeraude
(cd agbcc && ./install.sh ../pokeemeraude)
cd pokeemeraude && make tools && make -j"$(nproc)"
sha1sum pokeemeraude.gba               # attendu : ca666651374d89ca439007bed54d839eb7bd14d0
```

Comparez avec le SHA-1 de **votre** cartouche française dumpée (GodMode9 ou GBxCart). Si les deux sont égaux,
votre cartouche peut servir de ROM de base au patch français. *Non vérifié ici (compilation bloquée par une règle
de permission de l'environnement).*

## 3. Test Archipelago du patch officiel (reproduit PROTOTYPE_RESULTS C1-C3)

```sh
git clone https://github.com/ArchipelagoMW/Archipelago && cd Archipelago
python -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt "setuptools<81"
python ModuleUpdate.py --yes
# Players/ : un YAML "game: Pokemon Emerald" (+ un autre jeu)
SKIP_REQUIREMENTS_UPDATE=1 python Generate.py --player_files_path Players --outputpath out
unzip out/AP_*.zip -d out
python ../Pokemon-Yokai-Watch/research/yokai-emerald/poc/ap_patch_check.py out/*.apemerald <rom_yokai.gba> ../pokeemerald/pokeemerald.gba --out patched
```

## 4. Lancer et capturer dans mGBA

- **Sur votre PC** : ouvrez la ROM dans mGBA (0.10 ou plus).
- **Sans écran (Linux)** : `poc/mgba_drive.sh <rom> <dossier> "<étapes>"`. Il demande `mgba-qt`, `xvfb` et
  `xdotool`, avec dans `<dossier>/home/.config/mgba/qt.ini` :
  `audioSync=0`, `videoSync=0`, `displayDriver=0`, `pauseOnFocusLost=0`, et `SDL_AUDIODRIVER=dummy`. Sans carte
  son, l'émulation ne tourne pas tant que `audioSync` est actif.
  Exemple jusqu'au choix garçon/fille : `"wait:4 key:Return:1 wait:2 key:Return:1 wait:2 key:x:1 wait:2 key:x:86 wait:2 shot:boy key:Down:1 wait:2 shot:girl"`.

## 5. Archipelago dans mGBA (pour le jalon 1)

1. Téléchargez `connector_bizhawkclient_mgba.lua` (`Zunawe/bhc-substitutes`, dossier `mgba/`) dans
   `Archipelago/data/lua/`.
2. mGBA : Outils > Scripting… > Fichier > Charger le script… > ce fichier.
3. Lancez « BizHawk Client » depuis le lanceur d'Archipelago, connectez-vous au serveur.
4. Testez : sauvegarde neuve, un check (premier objet au sol), un objet envoyé (`/send` depuis la console du
   serveur), sauvegarde, fermeture, reconnexion. Le compteur d'objets reçus en sauvegarde empêche les doublons.

## 6. Distribution (plus tard)

Patch **BPS ou bsdiff** depuis la ROM de base du joueur (US pour le jalon 1, FR pour le jalon 2), produit par
notre build. Avant toute publication :
- vérifier que le patch ne contient pas d'asset non autorisé (comparer avec une build sans couche Yo-kai) ;
- ne jamais publier de `.gba` ;
- inclure les crédits (CREDITS dans ROADMAP.md).
