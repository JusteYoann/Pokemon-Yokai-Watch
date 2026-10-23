# Zombie errant — référence officielle du créateur

Le créateur a désigné sa propre retouche comme référence officielle des zombies errants et en a fixé l’échelle relativement à Nathan. La grille affichée ensuite a servi à une transcription manuelle native.

- `front-grid.json` : matrice explicite de 14 × 20 cases, transparente hors silhouette. C’est la source éditable ; pas une illustration réduite.
- `front-native.png` : silhouette 14 × 20, PNG indexé transparent.
- `front.png` : cellule moteur 32 × 32, silhouette x=9..22 / y=11..30, pieds à y=30.
- `front.4bpp` : 512 octets, ordre des tuiles GBA.
- `front.gbapal` : palette RGB555 de 32 octets, index 0 transparent.
- `front-x8.png` : agrandissement nearest-neighbor de contrôle.

**Fidélité à vérifier :** la forme a été relevée case par case sur l’image quadrillée visible dans la conversation. Le fichier source original n’est toujours pas disponible en binaire ; les valeurs RGB ont été relevées visuellement et arrondies aux couleurs GBA. Cette transcription n’est pas déclarée identique au pixel/couleur près au fichier original. Le dessin du créateur reste la référence en cas d’écart.

Cette face remplace les anciennes propositions comme direction de production. Aucune orientation ni animation n’a été inventée ; pas d’intégration de patrouille ou de scène. La ressource a été réellement chargée dans mGBA par les fonctions graphiques natives via une scène RAM temporaire. Les déclarations et objets de production attendent les autres orientations et la phase d’intégration validée.

Reconstruction : `python docs/lavanville-zombie-night/phase-1/outils/construire_zombie_errant.py`.

## Déplacements ajoutés

`overworld-grid.json` fournit les matrices des vues face/dos/profils et des pas. `mouvement/` contient les 12 PNG transparents. `overworld.png`, `overworld.4bpp` et `overworld.gbapal` sont au format neuf images standard FRLG, droite par miroir natif. La face existante n'a pas changé. Les contours noirs sont explicitement opaques à l'index 1 ; l'index 0 reste transparent, même si les deux valeurs RGB sont noires.

Contrôle des orientations et 12 déplacements natifs réalisés dans mGBA via une table d'images d'instance temporaire en RAM ; captures/GIF dans `docs/lavanville-zombie-night/phase-1/prototypes/zombie-marche`. Pas encore de déclaration d'un nouveau GFX ID de production ni de modification des événements de Lavanville.
