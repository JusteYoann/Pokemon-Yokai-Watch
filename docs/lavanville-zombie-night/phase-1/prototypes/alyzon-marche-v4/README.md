# Alyzon Bie — dernier idle fourni, capture 114647

Cette proposition suit la dernière pose de face fournie : œil cyan visible à droite de l'image, autre œil sous la mèche. Le profil gauche cache donc l'œil, tandis que le droit le montre. Les volumes restent compacts, avec les mèches évasées et la blouse ouverte sur le haut violet et le bas bleu.

Neuf PNG transparents 32 × 32 : gauche, dos, droite, avec repos et deux pas. Sources : `graphics/alyzon_bie/declinaisons-v4/`. Matrices natives et palette dans `grilles.json`. Le haut de la silhouette reste fixe pendant les pas. Noir opaque distinct de la transparence, palette limitée. La dernière face du créateur sert de référence visuelle ; elle n'est pas redessinée ou remplacée ici. Le PNG original n'est pas disponible localement : les couleurs sont adaptées à la palette native existante.

Une étude d'orientation générée a été demandée séparément à partir de cette dernière référence. Elle n'est pas réduite pour fabriquer les PNG natifs, produits directement par matrices.

Le GIF est un aperçu de poses, pas un enregistrement mGBA. Aucune ROM, table de sprites ou carte n'est modifiée. Les propositions précédentes sont conservées séparément.

## Déplacement réel mGBA

`marche-reelle-mgba.gif` montre successivement trois pas à gauche, trois vers le haut (dos), et trois à droite dans Lavanville. Les images de jeu sont capturées depuis mGBA ; seul le bandeau descriptif est ajouté à l'extérieur du cadre natif. Les clips séparés sont disponibles sous `marche-reelle-{gauche,dos,droite}-mgba.gif`.

Test de neuf déplacements natifs `ObjectEventSetHeldMovement`, avec contrôle des coordonnées et de la palette ; les deux phases d'animation du moteur ont été observées. Le visage et les trois pixels de contour corrigés ne sont pas redessinés. ROM de référence inchangée : SHA-256 `af807f4b8e2b6f7367208c1b25355a93b90b9937241295dd23e34b382df906cf`.

Il s'agit d'un objet temporaire et de graphismes chargés en RAM. Les deux profils étant asymétriques, la table d'images de profil est sélectionnée avant chaque clip indépendant pour compenser le miroir automatique FRLG. Une intégration permanente devra conserver cette distinction au changement de direction. Ni inscription définitive dans la table graphique, ni comportement de PNJ, ni modification de sauvegarde n'est effectuée. La face du créateur n'est pas substituée par une nouvelle transcription ; cet aperçu concerne uniquement les profils et le dos.
