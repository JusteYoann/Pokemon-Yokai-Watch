# Couleurs normales après Morphing

Décision du créateur : conserver l'éclaircissement pendant la transformation, puis rétablir les couleurs normales à sa fin.

Modification localisée dans `src/spiraton_battle.c`, étape2 du contrôleur du boss : après la fin des commandes de l'animation native et avant le message de transformation, recharger la palette compressée de l'espèce courante, avec son OT/personnalité. `LoadCompressedPalette` rétablit les tampons normal et affiché de la palette OBJ1. Aucun nouveau global EWRAM ni changement des ressources graphiques.

L'effet Morphing natif n'est pas modifié. Les autres combattants conservent leur comportement. Les règles des huit formes, leurs choix, statistiques, capacités, couleurs de PV et musiques restent inchangées. La grande représentation initiale reste un aperçu artistique statique en attente de raccordement.

## Vérifications réelles mGBA

- `public/COMBAT_PROTOTYPE_MGBA.json` et `prive/COMBAT_PROTOTYPE_MGBA.json` : huit formes distinctes56–63 vaincues jusqu'à la victoire, avec une équipe QA renforcée.
- Pour chacune des huit transitions, le test observe la palette éclaircie native pendant l'animation, puis compare les deux tampons de palette aux32 octets de la palette réelle décompressée de l'espèce à l'étape du message final. Les16 entrées sont identiques, sans éclaircissement résiduel.
- La vérification de fin est volontairement située juste après Morphing : les autres animations d'attaques peuvent temporairement modifier les couleurs et ne doivent pas être confondues avec un éclaircissement persistant.
- Les huit couleurs du HUD et la première transformation après choix restent vérifiées par le même combat complet.
- `avant-apres.png` : véritables captures avant/après de Bouh vers Saumhonni, à la fin de la deuxième transformation. Source avant : ROM9a7cb8ba9 ; source après : SHA du rapport public. Agrandissement nearest-neighbor et légendes uniquement.
- `PRESERVATION.json` : graphismes,151 espèces, cartes, scripts et équipes protégés ; les31 flux audio et378 gains privés sont identiques à Argenta. Les exceptions de code admises sont limitées au nom court déjà approuvé et au rechargement de palette ici autorisé.

Compilations publique et privée réussies. Publique :16 777 216 octets. Privée :31 658 511 octets ; marge sous32 Mio :1 895 921 octets. EWRAM261124/262144 ; IWRAM privée29888/32768.

```sh
source /workspace/.setup/env.sh
make -j6
make -j6 YOKAI_AUDIO_DIR=/workspace/private-audio/argenta-integration
YOKAI_SPIRATON_REPORT_DIR=QA_RECETTE_FINALE/DON_SPIRATON/PALETTES_NORMALES/public \
 python3 tools/yokai/tester_spiraton_combat_mgba.py
YOKAI_QA_ROM=$PWD/pokefirered_audio.gba \
 YOKAI_SPIRATON_REPORT_DIR=QA_RECETTE_FINALE/DON_SPIRATON/PALETTES_NORMALES/prive \
 python3 tools/yokai/tester_spiraton_combat_mgba.py
YOKAI_SPIRATON_PRESERVATION_DIR=QA_RECETTE_FINALE/DON_SPIRATON/PALETTES_NORMALES \
 python3 tools/yokai/verifier_spiraton_phase_a.py
```

Aucune fusion, activation de première conquête ou modification du grand sprite dans ce correctif.
