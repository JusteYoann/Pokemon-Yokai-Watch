# Nouvelle face cohérente avec les trois poses choisies

Le créateur a demandé une **nouvelle face**, basée sur les deux profils et le dos choisis. Cette proposition ne prétend plus copier la capture de face antérieure : elle redessine une vue frontale avec les mêmes masses de cheveux, pointes évasées, ombres dorées, blouse blanche à contours noirs, haut violet et bas bleu sombre. Un œil cyan reste visible à droite de l'image ; l'autre est masqué par la mèche.

Une étude frontale a été générée avec `graphics/alyzon_bie/sources/trois-poses-choisies.png` comme référence. Elle est conservée dans `graphics/alyzon_bie/face-coherente/etude-face.png`. Le script reconstruit une grille de 19 × 23 cellules puis calibre le candidat en nearest-neighbor à une silhouette de 17 × 19 pixels dans une cellule transparente 32 × 32. La palette est exactement celle des trois orientations adaptées à Nathan. La construction et ses étapes sont explicites ; aucune prétention de dessin initial natif à 19 pixels n'est faite.

Livrables : `face-repos.png` (PNG transparent natif), `face-repos.4bpp` (512 octets), `face-repos.gbapal` (32 octets). `face-x16.png` montre le candidat agrandi sans interpolation lissante ; `comparaison-quatre-poses-x8.png` l'aligne avec les trois orientations existantes. `CONTROLE.json` enregistre grille, palette et dimensions.

Il s'agit d'un nouveau candidat au repos uniquement. Aucun des treize PNG existants de `taille-nathan/`, dont les trois orientations et leurs pas, n'a changé. Aucun remplacement permanent dans le jeu, aucune animation ajoutée ou supprimée, aucune modification de ROM.
