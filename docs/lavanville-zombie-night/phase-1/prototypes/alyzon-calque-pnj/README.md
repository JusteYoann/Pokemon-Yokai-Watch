# Alyzon Bie — décalque direct d'un PNJ de Rouge Feu

La base choisie est la femme blonde FRLG (`graphics/object_events/pics/people/beauty.png`). Les douze poses sont dérivées directement de ses cellules natives 16 × 32. Le fichier source n'est pas modifié ; son hash et l'indice de cellule utilisé pour chaque pose sont consignés dans `graphics/alyzon_bie/calque-pnj/CONSTRUCTION.json`.

Cette série conserve la géométrie réelle du corps du PNJ, ses mouvements de bras et de jambes, ses pieds et les phases d'animation d'origine. Les vêtements sont repeints sur les pixels existants : jupe/tenue devient blouse blanche à ombres grises, haut violet et partie centrale bleu sombre. Les contours restent ceux du corps de base. La palette est RGB555 avec transparence séparée du noir.

La coiffure blonde de la base est conservée et prolongée localement pour masquer l'œil à gauche de l'image de face ; l'autre reçoit un iris cyan. Le profil gauche cache l'œil, le droit le montre. Trois pixels saillants du visage sont retirés sur les profils afin de conserver un visage plat sans nez marqué. Ces retouches portent sur la tête ; le masque du corps à partir du cou est contrôlé comme identique à celui de chaque cellule source.

La première rangée de la pointe de cheveux est retirée seulement lorsque le PNJ source est haut de vingt pixels, pour ramener la silhouette au repos à dix-neuf pixels, comme Nathan. Les cellules de marche gardent la géométrie et les positions des pieds de la base. Aucun redimensionnement ou lissage n'est appliqué.

## Fichiers

- `base-et-calque-x8.png` : PNJ original puis les quatre orientations au repos.
- `douze-poses-x10.png` : repos et deux pas pour chaque direction.
- `marche-quatre-directions.gif` : animation des PNG.
- `marche-reelle-mgba.gif` : douze vrais déplacements natifs dans mGBA, trois par direction ; bandeau ajouté hors de l'image du jeu.
- `graphics/alyzon_bie/calque-pnj/douze-poses.png` : les douze PNG transparents réunis en grille native 48 × 128.
- `overworld.png` (144 × 32), `.4bpp` (2304 octets) et `.gbapal` (32 octets) : neuf cellules standards, avec les trois profils droits distincts exportés séparément.

## Portée du test

Les douze déplacements, coordonnées, phases d'animation et palettes passent les contrôles mGBA. Les images 16 × 32 sont centrées dans une cellule de test 32 × 32 sans mise à l'échelle. Les profils sont sélectionnés séparément dans les clips pour respecter l'asymétrie des cheveux.

Il s'agit de graphismes temporaires en RAM, sans intégration permanente. ROM et sauvegardes inchangées, aucun scénario, carte ou élément de gameplay modifié. Les précédentes propositions restent archivées séparément. Le décalque reste une proposition artistique à valider.

## Retouches légères pour rapprocher l'apparence de l'artwork

La base et ses silhouettes restent celles de la version décalquée. Le blond est éclairci et légèrement désaturé ; quelques groupes de pixels forment une mèche diagonale plus lisible et des reflets sur les pointes. Les manches sont repeintes en blanc/gris sur les pixels de bras existants, en conservant les mains. L'encolure violette gagne une rangée et une boucle grise apparaît à la taille. Aucun déplacement de pixels de contour ou changement de proportions n'est ajouté.

`RETOUCHES.json` compare les douze images au commit du premier décalque : transparences/silhouettes, position des iris et rangées des pieds restent identiques. Les changements d'indices sont localisés ; la palette des cheveux est commune à toutes les poses. Le nouvel aperçu mGBA passe à nouveau douze déplacements natifs.
