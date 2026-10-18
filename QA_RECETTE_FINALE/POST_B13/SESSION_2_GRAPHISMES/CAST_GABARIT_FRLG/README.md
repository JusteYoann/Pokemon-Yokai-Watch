# Personnages overworld — gabarits Rouge Feu

Révision après validation du nouveau Nathan : Matt, Ariane, Katie, Domniscian, Seigneur Enma (roi humain), Nathaniel, Michael, Wyatt, Don Morleone, trois Mafiamilles et deux employés. **14 personnages, 104 images d'animation dans 19 PNG actifs.** Nathan est conservé exactement.

Les références officielles de l'archive caméos et de Protagoniste ont été examinées. Les dessins source sont dans `graphics/yokai_characters/overworld_frlg_v2/source/`. Dessin par imagegen, puis conversion technique reproductible par `python tools/yokai/convertir_cast_base_frlg.py` : découpage, réduction nearest, indexation sur les palettes existantes, conservation des dimensions et nombres d'images. Les PNG ne sont pas une simple recoloration des anciens personnages.

- [Toutes les images au format natif, agrandies x3 sur gris](CAST_NATIF_X3.png).
- [Rendu natif mGBA après, quatre orientations](../overworld/cast-apres/planche-22-acteurs.png) ; [avant](../overworld/cast-avant/planche-22-acteurs.png). Les 8 autres acteurs de cette galerie servent de témoins inchangés.
- [Conversion et cadres individuels](CONVERSION.json).
- [Preuve de préservation au niveau des octets ROM](PRESERVATION.json).
- [Tests des déplacements et actions de Katie](katie/mgba/TEST_PROTAGONISTES_MGBA.json), [images et animations](katie/mgba/preuves/).
- [Surf réel : entrée depuis la rive, quatre directions, sortie à la manette](katie/surf/TEST_MGBA.json), [captures sur l'eau](katie/surf/quatre-directions.png).

Les proportions utilisent Blue pour Matt, Leaf pour Katie, et les gabarits fille, garçon, homme, gentleman ou homme corpulent selon le rôle des PNJ. Domniscian conserve son bureau et sa silhouette spéciale 32×32. Les autres utilisent des images 16×32, sauf les équipements de Katie en 32×32. Les trois Mafiamilles conservent des corpulences différentes. Les employés conservent leur tête de fantôme, leurs costumes rouge/bleu et leurs accessoires.

Katie : 9 marche, 14 surf/course/regards, 9 vélo, 6 action Cherch'VS, 12 pêche, 9 objet. Matt : 9 images de marche. Chaque autre PNJ : 3 orientations source, quatrième par miroir natif. Ces PNJ stationnaires ne reçoivent pas artificiellement un nouveau cycle de marche.

Les anciens miroirs compensant les défauts des dessins de Matt et Katie sont corrigés uniquement dans les commandes visuelles hFlip ; les durées, tables et scripts restent identiques. Les anciennes réductions supplémentaires d'Ariane/Matt/Wyatt sont supprimées : les nouvelles images ont déjà leur gabarit natif.

## Vérifications effectuées

Compilation privée avec les 19 OST : **27 718 259 octets**, taille inchangée, sous 32 Mio. SHA-256 `431ba94236270358f2fa091cf612ad1fbaf2ed40bcfffd071efbc8bc552a2142`. Compilation publique avec musiques de secours également réussie.

mGBA démarre par une vraie nouvelle partie. Galerie native des 22 acteurs × 4 orientations, avant/après ; Katie : marche/course/vélo, animations objet/Cherch'VS, tâche pêche dans quatre directions et retour à la normale. Surf supplémentaire réellement déclenché au bord de l'eau, déplacements/orientations et sortie à terre. Les captures ont été ouvertes et inspectées.

Comparaison à `2e95fcfb9bb89759bdc1776307055d49a9da3cd5` : **13 818 octets ROM modifiés, exclusivement dans les 19 tableaux graphiques overworld et commandes hFlip ciblées**. Aucun changement de données, code moteur, gameplay, son, intro/titre, portrait/dos de combat, palette ou Nathan. 5 641 autres images et palettes restent identiques au contenu Git (fins de ligne des palettes normalisées selon .gitattributes).

Cette vérification graphique ciblée ne constitue pas une nouvelle partie complète ni une validation intégrale des événements de l'aventure. ROM et audio protégés restent privés.
