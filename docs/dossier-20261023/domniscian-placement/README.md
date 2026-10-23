# Placement du portrait de Domniscian

Référence validée par l’utilisateur : reprendre à la fois la taille et le placement du montage fourni.

Le portrait adverse utilise désormais un centre `(180, 28)` au lieu de `(176, 40)` et un agrandissement uniforme d’environ `4/3`. La couronne atteint le bord supérieur, comme sur le montage. Le PNG source 64×64 et sa palette restent inchangés ; le moteur GBA applique la transformation affine, sans étirement différent selon l’axe. Le changement est limité au portrait de Domniscian dans le contrôleur adverse, à l’entrée en combat et lors de son retour pour la réplique de défaite. Les sprites overworld et les transitions de Champion ne sont pas modifiés.

## Vérification native mGBA

Les résultats des versions [publique](public/TEST_MGBA.json) et [privée](prive/TEST_MGBA.json) portent sur les ROM identifiées par leur SHA256. Les cartes, les drapeaux et l’équipe du joueur sont des fixtures de test ; le contrôleur joue les combats, sans modification des PV adverses ou du résultat.

- Combat initial et revanche : placement et matrice affine vérifiés lors des deux apparitions du portrait ; victoire obtenue et retour sur la carte.
- Envoi du premier Yo-kai : le portrait disparaît, le menu de combat devient utilisable.
- Régression Bérénice : centre et matrice d’origine conservés, premier Yo-kai envoyé et menu utilisable.

[Capture publique](public/champion-portrait-x3.png) · [Entrée en combat publique](public/champion-intro.gif) · [Revanche publique](public/revanche-intro.gif) · [Capture privée](prive/champion-portrait-x3.png).

Ces vérifications ciblées ne remplacent pas la recette graphique globale et les deux signalements de sprites suspects consignés dans le rapport principal.

```bash
source /workspace/.setup/env.sh
make -j6
make -j6 YOKAI_AUDIO_DIR=/workspace/private-audio/lavanville-integration
python3 tools/yokai/tester_domniscian_placement_mgba.py
YOKAI_QA_ROM="$PWD/pokefirered_audio.gba" python3 tools/yokai/tester_domniscian_placement_mgba.py
```
