# Zombies errants — ressources graphiques

## Overworld validé comme direction

`errant/front-grid.json` et `errant/front.png` : transcription de la grille du créateur, silhouette 14 × 20 dans une cellule 32 × 32. Ces fichiers n'ont pas été modifiés lors de la création des sprites de combat. Les orientations/marches restent à produire ; aucune variante overworld supplémentaire n'est implicitement validée par les images de combat.

## Quatre fronts de combat créés

Chaque dossier `errant`, `sprinteur`, `colosse`, `spectral` contient :

- `battle-front.png` : PNG indexé transparent, 64 × 64, au plus 15 couleurs opaques compatibles RGB555.
- `battle-front.4bpp` : tuiles GBA, 2 048 octets.
- `battle-front.gbapal` : palette GBA, 32 octets, index 0 transparent.
- `battle-front-x6.png` : agrandissement nearest-neighbor pour examiner les détails.

Direction : mêmes critères d'échelle, contour, ombrage et palette que les sprites de combat des 151 Yo-kai. Références stylistiques examinées : Jibanyan, Brumette, Slurpent, Tristos, Toumou, Sorcophage. Identité zombie issue du sprite overworld approuvé et de l'artwork Zombifdge fourni par le créateur : peau verte tachetée, orbites sombres, yeux rouges et flamme rose. Les quatre poses distinguent lenteur, course, puissance et flottement.

Les concepts ont été générés puis préparés en sprites indexés à résolution GBA. Extraction des quatre silhouettes par composantes alpha, sans contamination entre colonnes ; échantillonnage nearest-neighbor, palette limitée sans dithering, source conservée dans `sources/quatre-zombies-combat-source.png`. Ce procédé n'est pas présenté comme un dessin manuel initial sur grille 64 × 64. La validation artistique définitive du créateur reste à obtenir.

## Vérification réelle mGBA

Captures dans `docs/lavanville-zombie-night/phase-1/prototypes/zombies-combat/`. Les quatre ressources ont été chargées via les fonctions natives de tuiles/palette/OBJ pendant des combats de test. Aucun montage dans ces captures. L'adversaire emploie explicitement une espèce existante comme gabarit temporaire en RAM : aucun des 151 n'est modifié et aucun ID de zombie de production n'est attribué. Noms et niveau 25 sont des éléments de test visuel, pas des données de combat validées. Fuite/capture/AI/EXP/rencontres restent hors du périmètre de ce test.

Aucune ROM modifiée ou recompilée, aucune fusion de branche, aucun changement des équipes, statistiques, cartes ou OST.
