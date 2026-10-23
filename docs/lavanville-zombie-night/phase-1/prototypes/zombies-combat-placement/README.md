# Placement des quatre zombies en combat — références du créateur

[Quatre captures réelles mGBA](quatre-combats-mgba-x2.png). Le fond/interface viennent de la ROM du projet, le cadrage des zombies suit les montages fournis.

| Variante | Centre écran (240 × 160) | Agrandissement matériel | Boîte visible réelle | Flamme hors cadre haut |
|---|---|---:|---|---|
| errant | [170, 31] | ×1.3763 | [140, 0, 201, 70] | oui |
| sprinteur | [173, 30] | ×1.4382 | [136, 0, 209, 71] | oui |
| colosse | [174, 29] | ×1.3763 | [135, 0, 214, 68] | oui |
| spectral | [169, 29] | ×1.4382 | [141, 0, 197, 70] | oui |

Les points d’ancrage et l’échelle ont été relevés visuellement sur les quatre montages montrés dans la conversation puis transposés à l’écran natif 240 × 160. Les fichiers binaires originaux des montages ne sont pas présents localement : il ne s’agit pas d’une mesure certifiée pixel pour pixel de ces fichiers. Les boîtes de ce tableau sont, elles, mesurées sur les captures mGBA en comparant le rendu avec/sans l’OBJ de test.

## Technique et conservation

Le profil est conservé dans `graphics/yokai_zombies/battle-presentation.json`. L’agrandissement utilise une matrice affine matérielle GBA, avec fenêtre OBJ double taille : un simple agrandissement d’un OBJ normal 64 × 64 aurait coupé les côtés des grandes variantes. Les valeurs de matrice sont quantifiées par le matériel ; les facteurs réellement obtenus sont indiqués ci-dessus. Un seul zombie est affiché par essai, une matrice dédiée par sprite.

Les quatre PNG64×64, leurs tuiles4bpp et leurs palettes restent inchangés. Les flammes sont complètes dans les ressources ; leur partie supérieure est masquée par le bord de l’écran avec ce cadrage, comme sur les montages de référence. Aucun redessin ni recadrage destructif des sprites. Le sprite overworld et ses poses restent inchangés.

Les captures sont de vrais rendus mGBA, non des montages. Le test réutilise un gabarit d’adversaire en RAM, comme lors du précédent contrôle d’affichage. Noms/niveau/stats et options du menu proviennent de ce test, pas d’une intégration fonctionnelle de nouveaux ennemis. Aucun fichier ROM, carte, équipe, statistique, musique ou mécanique de combat de production modifié. Le profil sera à réutiliser lors de l’intégration des rencontres et à vérifier aussi pendant les animations d’attaques.

Reproduction :

```sh
source /workspace/.setup/env.sh
YOKAI_QA_ROM=/workspace/Pokemon-Yokai-Watch-spiraton/pokefirered_audio.gba YOKAI_ZOMBIE_PRESENTATION_PROFILE="$PWD/graphics/yokai_zombies/battle-presentation.json" YOKAI_ZOMBIE_BATTLE_REPORT="$PWD/docs/lavanville-zombie-night/phase-1/prototypes/zombies-combat-placement" python docs/lavanville-zombie-night/phase-1/outils/verifier_zombies_combat_mgba.py
```
