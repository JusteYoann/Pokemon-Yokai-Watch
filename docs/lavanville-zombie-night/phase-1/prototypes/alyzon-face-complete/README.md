# Alyzon Bie — face au repos et deux pas, planche de douze poses

La face suit la capture `Screenshot 2026-10-23 114647.png`, confirmée par le créateur : mèche couvrant l'œil à gauche de l'image, œil cyan à droite, blouse blanche ouverte, haut violet, bas bleu sombre. Elle est haute de 19 pixels au repos, comme Nathan, et enregistrée dans une cellule transparente de 32 × 32.

Il s'agit d'une **transcription visuelle de la capture**, pas d'une extraction exacte du PNG original : le fichier binaire n'est pas disponible dans l'environnement. La grille transcrite et cette limite sont explicites dans `FACE.json` et le script de construction. Les couleurs utilisent la même palette RGB555 que les autres orientations. Cette face doit être comparée visuellement à la référence du créateur avant toute intégration ; aucune identité des pixels d'origine n'est prétendue.

Trois PNG ajoutés dans `graphics/alyzon_bie/taille-nathan/` : `face-repos.png`, `face-pas-1.png`, `face-pas-2.png`. Les cheveux, le visage et le torse sont identiques entre les trois poses. Les pas alternent seulement les pieds et le bas de la blouse. Les neuf poses latérales/de dos précédemment produites ne changent pas.

La planche `douze-poses-x8.png` montre les douze poses. `marche-quatre-directions.gif` anime les PNG ; `marche-reelle-mgba.gif` filme douze déplacements natifs dans mGBA. Les fichiers ROM, sauvegardes et tables graphiques du jeu restent inchangés : ce sont des essais en RAM. Les profils asymétriques sont sélectionnés avant les clips indépendants, comme dans les aperçus précédents.

`overworld.png` et `overworld.4bpp` exportent les neuf frames standards FRLG (face/dos/gauche) ; le profil droit distinct reste fourni dans ses trois PNG et nécessite une sélection spécifique pour ne pas devenir un simple miroir de la gauche. Cet export ne constitue pas une intégration permanente.
