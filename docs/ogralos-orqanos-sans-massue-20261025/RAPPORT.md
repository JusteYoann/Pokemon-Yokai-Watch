# Ogralos et Orqanos sans massue

Deux nouvelles variantes préparées à partir des références du chat, dans le même gabarit que Gargaros : 12 poses par personnage, cases de 32 × 32 pixels, silhouette visible de 22 pixels de haut et même ligne de pieds.

- [Ogralos bleu : planche ×6](ogralos-planche-x6.png), [PNG natif transparent](ogralos-planche-native.png).
- [Orqanos noir : planche ×6](orqanos-planche-x6.png), [PNG natif transparent](orqanos-planche-native.png).

Dans chaque planche : face, dos, gauche et droite, avec deux pas et une pose de repos par direction. Ogralos garde sa peau bleue, ses cheveux rouges, ses deux cornes jaunes et son vêtement vert ; Orqanos sa peau noire, ses cornes jaunes, ses détails de visage gris/rouges, ses cheveux violets et son vêtement rouge. Aucun ne porte de massue.

Les illustrations source sont générées ; le convertisseur découpe et réduit au plus proche voisin, puis attribue une palette commune de quinze couleurs opaques plus transparence par personnage. Contrôle des 24 images : hauteur et base identiques à Gargaros, index de transparence zéro, indices de palette inférieurs à seize. Les planches natives ont été inspectées visuellement. [Détails de conversion](CONVERSIONS.json).

Ces nouveaux assets sont conservés dans les dossiers `ogralos_sans_massue` et `orqanos_sans_massue`. Aucun sprite existant d'Orqanos n'est écrasé et aucun événement, script, ROM ou personnage n'est remplacé à ce stade. Il s'agit de la création des ressources ; aucune démonstration en jeu n'est présentée comme testée. Aucune fusion sur master.

Conversion reproductible : `python tools/yokai/convertir_ogralos_orqanos_sans_massue.py`.
