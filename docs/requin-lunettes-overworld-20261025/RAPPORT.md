# Requin à lunettes : sprites overworld et marche

[GIF en jeu, agrandi x3](quatre-directions-mgba-x3.gif) · [Planche des poses](planche-x6.png) · [Planche native](planche-native.png)

Le personnage possède deux verres argentés décalés vers le museau, avec les yeux visibles au-dessus. Les vues de dos et de gauche validées sont conservées. Le côté droit est le miroir matériel exact du profil gauche : les mêmes images et les mêmes poses de pas sont retournées par le moteur GBA.

## Format

Neuf images uniques de 32 × 32 pixels : trois poses de face, trois de dos et trois de profil gauche. Les trois poses de droite sont obtenues par retournement horizontal. La hauteur visible de chaque image est de **19 pixels**, avec le même alignement des pieds que Maître Nyada. La palette comporte quinze couleurs opaques et une entrée transparente. La planche présentée rassemble les douze poses, droite comprise.

Les dessins viennent des planches générées jointes à `graphics/yokai_characters/requin_lunettes/source/`. La conversion découpe les cellules, réduit au plus proche voisin et applique la palette GBA ; elle ne redessine pas les silhouettes. La planche de face corrigée est utilisée pour la face, et la source des profils validés pour le dos et le profil gauche.

## Vérification native mGBA

Le GIF montre de vraies images de la ROM : acteur temporaire sur une zone praticable de Bourg Palette, marche sur les quatre axes et Maître Nyada présent comme référence de taille. Chaque pas couvre une case réelle. Les trois poses de chaque direction sont reconnues dans la VRAM, le retournement horizontal est vérifié pour la droite, les palettes restent distinctes et le personnage demeure visible dans les images enregistrées. Le sol est vérifié avant les déplacements. Les couleurs bleues du sprite sont contrôlées dans son rectangle d’affichage.

La démonstration prépare et anime deux acteurs temporaires ; elle n’ajoute pas de rencontre permanente ni de rôle de quête à ce nouveau personnage. Son graphisme est enregistré sous `OBJ_EVENT_GFX_REQUIN_LUNETTES` pour une utilisation ultérieure. La ROM conserve les corrections précédentes, dont le placement de Maître Nyada et Démophage et l’arrivée d’Enma.

[Tests](TESTS_MGBA.json) · [ROM avec le graphisme intégré](Pokemon_Yokai_Watch_Beta_0.1_Requin_Lunettes.gba) · [Empreintes](COMPILATION.json)
