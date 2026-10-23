# Alyzon Bie — les trois sprites choisis

## Référence réellement utilisée

Le créateur a désigné la planche à trois poses (profil gauche, dos, profil droit) et demandé qu'elle serve à préparer la marche. La source correspondante est conservée sans modification dans `graphics/alyzon_bie/sources/trois-poses-choisies.png` ; son SHA-256 est enregistré dans `graphics/alyzon_bie/poses-planche-validee/EXTRACTION.json`.

Cette proposition ne repart pas des matrices des versions v1 à v4. Chaque pose au repos est extraite des cases de la planche source. La grille de cette image agrandie n'est pas parfaitement régulière ; ses limites de cellules sont explicites et vérifiables dans le script et le manifeste. Les centres de cellules sont échantillonnés, sans redessiner les poses ou appliquer une réduction globale. La grille reconstruite est haute de 23 pixels, dans des cellules GBA 32 × 32.

L'image source est une étude agrandie, pas un PNG indexé natif : il serait faux de garantir une identité binaire de pixels ou de RGB après conversion. Les couleurs sont adaptées à une palette commune de quinze couleurs opaques RGB555 et une entrée transparente. Noir opaque, œil cyan, haut violet et bas bleu disposent de couleurs distinctes. Le fichier source original reste intact pour comparaison.

## Marche

Neuf PNG transparents : repos et deux pas pour chacun des deux profils et le dos. Les cheveux et le visage restent identiques au repos pendant les pas ; les pieds alternent sur le bas de la silhouette. La face du créateur n'est pas redessinée. Les anciennes propositions restent archivées séparément.

`planche-native-x8.png` présente les neuf poses ; `marche-trois-poses.gif` est une animation des PNG. `marche-reelle-mgba.gif` montre les déplacements réels dans mGBA, successivement à gauche, de dos, puis à droite.

L'aperçu mGBA utilise un objet temporaire avec des graphismes en RAM. Comme les profils sont asymétriques, la table de profil est sélectionnée avant chaque clip ; il ne s'agit pas encore d'un enregistrement permanent avec sélection automatique de toutes les orientations. Le bandeau est ajouté hors de l'image de jeu native. Aucun fichier ROM, carte, scénario ou sauvegarde n'est remplacé. Voir `TEST_MGBA_MARCHE.json` pour les coordonnées, les phases de marche observées et le hash de la ROM.
