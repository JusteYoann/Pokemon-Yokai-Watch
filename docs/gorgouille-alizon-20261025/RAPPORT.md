# Gorgouille, Alizon Bie et musique de Domniscian

## Modifications

- Alizon est absente à l’arrivée au sommet. À trois cases de Gorgouille, elle entre par le passage et rejoint la case à droite du joueur ; tous deux regardent Gorgouille. Le joueur se décale temporairement lorsque le passage est étroit.
- Ses déplacements utilisent les cases praticables et les positions actuelles des personnages et des rochers. Un passage déjà dégagé est privilégié. Si nécessaire, elle pousse réellement les rochers avec le son de Force. Les rochers restent à leurs nouvelles positions après la scène et le joueur peut suivre le passage.
- Après la capture, le dialogue est suivi de son départ à pied jusqu’à l’entrée. Elle ne disparaît qu’à cet endroit.
- Gorgouille est retiré avant la première image du retour de combat après capture ou K.O. Après un K.O., il réapparaît à la prochaine visite ; après capture, il reste absent.
- Pour les combats contre Domniscian utilisant « Vs Hinozall », chaque boucle complète est suivie de 896 rafraîchissements GBA de silence, soit **15,001 secondes**. Les effets sonores et cris restent actifs. La première lecture commence normalement. Les autres adversaires conservent leurs boucles habituelles.

## Vérification native mGBA

Les quatre scénarios de `TESTS_MGBA.json` passent : capture et départ avec poussées, chemin déjà dégagé, arrivée latérale, K.O. puis nouvelle visite. Aucun chevauchement de cases de personnages ni traversée de terrain bloqué n’a été détecté pendant les scènes testées. Aucun retour visible de Gorgouille après combat n’a été détecté. Le chemin de sortie est praticable par le joueur.

`TEST_AUDIO.json` mesure la fin naturelle du morceau, les 896 images de pause et sa reprise. Le signal musical est nul pendant la pause ; une action réelle dans le menu produit bien un effet sonore pendant celle-ci. Un autre adversaire utilisant le même morceau conserve la boucle normale.

## Démonstrations

- [Arrivée, capture et départ de Gorgouille, avec son](gorgouille-arrivee-capture-depart-mgba.mp4) : séquence continue à vitesse normale. Prérequis de quête, équipe niveau 100, Master Ball et passage déjà dégagé préparés avant le film ; déplacements et capture exécutés par les commandes normales du jeu.
- [Pause de 15 secondes de Domniscian, avec son](domniscian-pause-15s-mgba.mp4) : extrait autour de la fin naturelle du morceau, du silence et de la reprise. Un effet sonore de menu est déclenché pendant le silence.
- [ROM compilée](Pokemon_Yokai_Watch_Beta_0.1_Gorgouille_Domniscian.gba) et [empreinte](COMPILATION.json).

Les fichiers de travail bruts ne sont pas publiés. Les tests utilisent des parties isolées préparées et ne constituent pas un parcours intégral de l’aventure.
