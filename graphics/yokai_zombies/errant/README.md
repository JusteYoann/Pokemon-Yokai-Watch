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
