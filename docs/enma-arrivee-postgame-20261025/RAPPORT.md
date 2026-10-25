# Arrivée du Seigneur Enma au début du postgame

Lors de la première sortie de la maison après la Ligue, Enma entre par le passage nord de Bourg Palette. Il contourne les bâtiments et rejoint une case située deux pas devant le joueur. Nathan ou Katie se tourne vers lui pour le dialogue. Enma repart ensuite à pied vers le nord et est retiré lorsqu’il a quitté l’écran.

Le trajet utilise les collisions réelles du terrain et les positions des habitants, figés pendant la scène. Il peut utiliser l’une ou l’autre case du passage nord et contourner un personnage présent sur le chemin. Le joueur reste devant sa maison. Le dialogue et les conditions de progression restent ceux de l’introduction existante ; la scène ne se rejoue pas après sa conclusion.

Les trois vues royales déjà validées suffisent : face, dos et profil avec retournement horizontal. L’événement utilise désormais leur définition directionnelle, plutôt que la définition statique de la rencontre légendaire. Les images, leur taille et leur palette sont conservées ; aucun nouveau dessin n’a été nécessaire. Le sprite de combat et la rencontre capturable d’Enma conservent leur définition.

## Vérification native mGBA

Deux parties isolées, Nathan puis Katie, avec la Ligue terminée et une équipe préparées : sortie réelle de la maison par les boutons du jeu, arrivée depuis (12, 1), dialogue, départ vers le nord, puis nouvelle entrée/sortie pour vérifier l’absence de répétition. Chaque trajet comporte 31 positions observées, sans saut de case, collision de personnages ni entrée dans une case bloquée. Les quatre orientations et la palette royale sont vérifiées sur les images de scène. Les commandes sont rendues après le départ et les indicateurs de progression sont correctement enregistrés en mémoire de jeu.

Les mesures figurent dans [TESTS_MGBA.json](TESTS_MGBA.json). Aucun personnage, déplacement ni couleur n’est imposé par le test pendant la cinématique : l’observateur lit uniquement les états du jeu.

[Enma devant Nathan](0-devant-maison.png) · [Enma devant Katie](1-devant-maison.png) · [ROM corrigée](Pokemon_Yokai_Watch_Beta_0.1_Enma_Arrivee.gba) · [Empreinte](COMPILATION.json)

Cette ROM conserve aussi la correction des palettes de Don Morléone chez Yopple. Aucune nouvelle vidéo ni modification de la compilation des cinématiques.
