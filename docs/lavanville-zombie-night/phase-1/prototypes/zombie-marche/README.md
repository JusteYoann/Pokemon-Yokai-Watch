# Marche du zombie overworld validé

[Planche des 12 poses sur fond clair](planche-directions-x6.png) · [Planche native transparente](planche-native-transparente.png) · [Quatre cycles sur place](quatre-directions-marche.gif).

[Marche réelle dans mGBA](marche-reelle-mgba.gif) · [Quatre orientations dans mGBA](quatre-directions-mgba-x2.png).

## Ressources créées

Trois poses (repos, pas 1, pas 2) pour face, dos, gauche, droite. Cellules 32 × 32, silhouette de 20 pixels de haut, pieds à y=30, palette commune issue du sprite validé. Matrices natives dans `graphics/yokai_zombies/errant/overworld-grid.json`, PNG individuels dans `graphics/yokai_zombies/errant/mouvement/`.

La face au repos est pixel pour pixel identique à `front.png`. La tête et la flamme de face ne changent pas pendant les pas : seuls bras/jambes sont animés. Les nouvelles vues ont été construites sur matrices natives ; l'étude générée d'orientations a servi de guide et n'a pas été réduite pour produire ces fichiers.

**Contours noirs conservés : index 1 = noir opaque ; index 0 = transparent.** Les deux entrées ont la même valeur RGB (0,0,0), mais une fonction différente. Ne jamais fusionner leurs indices lors d'une conversion, sous peine d'effacer le contour. Les 12 PNG contiennent des pixels noirs opaques ; leur nombre est enregistré dans `CONTROLE_GRAPHIQUE.json`.

## Format FRLG

`overworld.png` contient neuf images de 32 × 32, dans l'ordre natif : face, dos, gauche au repos ; deux pas de face ; deux pas de dos ; deux pas de gauche. La droite utilise le miroir horizontal natif, avec PNG explicites fournis pour examen. `overworld.4bpp` = 4 608 octets ; `overworld.gbapal` = 32 octets. Cycle de marche : pas1 → repos → pas2 → repos, huit images par pose pour l'animation standard, vitesse modulée par le moteur.

## Test réel

Le test utilise un objet natif 32 × 32 à neuf images comme coquille temporaire (ID172) puis charge la nouvelle table d'images et la palette en RAM. Contrôle des quatre orientations et du flip droit, puis 12 actions natives `WALK_NORMAL` autour d'un carré libre à Lavanville. Les coordonnées d'arrivée ont été contrôlées après chaque action, ainsi que la persistance de la table d'images et de la palette. Voir `TEST_MGBA.json`.

Ce GIF provient de véritables déplacements mGBA, sans montage. L'autre GIF montre les cycles de poses assemblés pour inspection graphique. Aucun fichier de ROM ni carte/script de production modifié ; pas encore de patrouille, détection hostile ou combat réaffrontable. Les nouvelles orientations/marches restent à approuver artistiquement.
