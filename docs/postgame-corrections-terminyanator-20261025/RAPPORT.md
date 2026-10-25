# Corrections postgame et Terminyanator

## Changements

- Chen est visible au laboratoire dans le postgame, y compris avec les anciens états de progression 7, 8 ou 9. Matt n’y apparaît plus ; sa présence pendant l’histoire et son rôle de Maître de la Ligue sont conservés.
- Après validation des **151 Yo-kai possédés**, Chen félicite le joueur, présente le diplôme, puis annonce que quelqu’un attend chez lui. Le retour depuis le diplôme reprend le dialogue et termine l’invitation correctement.
- Dans la Grotte de Glace, Alizon Bie remplace Olga. Ses répliques sont directes et combatives ; le combat contre la Mafiamille et la progression de l’entrepôt sont conservés.
- Le scientifique quitte les trois lieux en marchant. Son trajet tient compte du sol et des autres personnages ; il est retiré après avoir quitté l’écran. À Carmin, il s’approche de l’arbre, utilise l’animation et le son de Coupe, puis poursuit son chemin. Si l’arbre était déjà coupé, il emprunte directement le passage.
- Les crédits ont de nouvelles captures : Nathan sur le chemin de la Tour Pokémon, Nathan sur une case praticable à Cramois’Île, Léo humain à la place de Jibanyan, puis Maître Nyada et Démophage côte à côte à leur nouvel emplacement, avec le joueur devant. Les versions garçon et fille sont mises à jour.
- **Les 35 objets motard du jeu** utilisent Terminyanator, avec dix poses natives de **32 × 32 pixels**, les déplacements et les collisions des motards. La partie inférieure de la moto et ses roues sont reprises du graphisme d’origine. Tous les portraits de combat de motard sont remplacés par son portrait en moto, en **64 × 64**. Équipes, niveaux et progression de ces dresseurs sont conservés.

## Extraits avec son

| Extrait | Durée |
| --- | --- |
| [Matt, Maître de la Ligue](matt-champion.mp4) | 6 min 29 s |
| [Chen : cadeau de Jibanyan](chen-jibanyan.mp4) | 1 min 20 s |
| [Chen : 151 Yo-kai, diplôme et invitation](chen-151.mp4) | 48 s |
| [Alizon Bie et les Mafiamille dans la grotte](alizon-grotte.mp4) | 3 min 24 s |
| [Scientifique : Coupe et départ à Carmin](scientifique-2.mp4) | 37 s |

Les extraits sont enregistrés dans mGBA avec le son natif, à vitesse normale. Les prérequis et l’équipe de test niveau 100 sont préparés sur des parties isolées ; pendant la capture, seules les commandes du jeu sont utilisées. L’extrait du scientifique prépare explicitement son retour de victoire pour montrer le départ. Ces vidéos ne sont pas une aventure continue.

## Aperçus

- [Terminyanator : déplacements dans les quatre directions](terminyanator-quatre-directions-mgba.gif)
- [Portrait de combat en jeu](terminyanator-en-combat.png)
- [Planche des sprites](terminyanator-planche-x4.png)
- [Portrait agrandi](terminyanator-portrait-x8.png)
- [Crédits : Tour Pokémon](garcon-credit-12-native.png)
- [Crédits : Cramois’Île](garcon-credit-21-native.png)
- [Crédits : Léo humain](garcon-credit-7-native.png)
- [Crédits : nouvel emplacement de Nyada et Démophage](garcon-credit-28-native.png)

## Vérifications

Compilation réussie. Contrôles mGBA des deux personnages joueurs et des trois anciens états du laboratoire, conservation de Matt pendant l’histoire et largeur native des textes. Onze départs testés depuis les côtés accessibles, dont Carmin avec l’arbre présent et déjà coupé : pas de case de collision traversée, pas de superposition avec un personnage, retrait après sortie de l’écran. Vérification des poses de Terminyanator en mémoire vidéo, de sa palette et de son portrait au combat. Les cinq vidéos ont été décodées intégralement ; chaque vidéo contient une piste sonore stéréo et un décalage de durée audio/vidéo inférieur à 0,15 seconde.

Les résultats détaillés sont dans TESTS_CHEN.json, TESTS_DEPARTS.json, TESTS_TERMINYANATOR.json et VERIFICATION_VIDEOS.json. PHOTOS_CREDITS.json conserve la provenance des captures prises avant la dernière correction de retour du diplôme.

[ROM mise à jour](Pokemon_Yokai_Watch_Beta_0.1_Postgame_Terminyanator.gba) — empreinte dans SHA256.txt.
