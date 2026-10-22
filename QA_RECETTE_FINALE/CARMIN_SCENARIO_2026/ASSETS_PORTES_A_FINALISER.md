# Portes Mystères — habillage final restant

Le jeu dispose de trois passages fonctionnels, accessibles par interaction, avec des dimensions originales et des destinations fixes. Les motifs roses natifs de l'arène de Safrania servent actuellement de terminaux provisoires dans le laboratoire. Ils ne reproduisent pas la porte officielle à œil et serrure : cet asset n'est pas déclaré terminé.

Référence examinée : `04_IMAGES_ADDITIONNELLES_IDENTIFIEES/05_MINI_JEU_SALLE_DES_PORTES.jpeg`, indexée dans `docs/SCENARIO_ORIGINAL_2026/INDEX_IMAGES_ADDITIONNELLES.csv`. L'image montre des portes latérales en bois brun, un œil blanc, une serrure noire et une porte centrale verte à fronton décoré. L'illustration privée ne doit pas être ajoutée au dépôt.

Fichiers de production attendus :

- `graphics/yokai_characters/portes_mysteres/doors.png` : planche96x96, trois colonnes de32pixels et deux rangées de48pixels ; portes fermées au-dessus, ouvertes dessous. Les deux colonnes latérales reprennent les portes brunes ; la colonne centrale reprend la porte verte. Aucune inscription ajoutée au dessin.
- `graphics/yokai_characters/portes_mysteres/doors.pal` : palette GBA de16 couleurs, couleurs compatibles avec une profondeur4bpp et transparence d'index0 pour la source. Les proportions tête/corps de Red concernent les personnages ; ces portes sont des décors de32x48.
- `data/tilesets/secondary/mystery_lab/tiles.png`, palettes, metatiles et attributs : tileset secondaire dérivé du laboratoire, ajoutant les trois portes tout en conservant les sols, collisions et sorties de l'arène.

Les portes occupent les colonnes1–2,4–5 et7–8, rangées9–11, dans la salle11x21. Leurs points d'interaction restent (2,11), (5,11) et (8,11), approchés depuis la rangée12. Les rectangles de décor peuvent dépasser d'une case à gauche ; ne pas déplacer les destinations de retour (2,12), (5,12), (8,12).

La validation artistique doit contrôler l'œil, la serrure, les teintes bois/vert, le fronton de la porte centrale et la lisibilité à l'échelle1:1. La conversion ne doit pas être présentée comme une validation visuelle. Après intégration, rejouer les trois départs/retours, les collisions, la sauvegarde dans chaque dimension et le passage vers Bérénice.
