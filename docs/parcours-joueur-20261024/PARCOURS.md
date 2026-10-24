# Partie de recette complète — progression réelle

ROM testée : `Pokemon_Yokai_Watch_Beta_0.1_FR.gba`, SHA-256
`5e350381135282f916616c221ef59db974fec501b73579a406c533e5104469e5`.
Base source : `1859040f5c83f412b524da6cdb52b0be5dea8ac1`.
Branche de recette : `test/parcours-joueur-complet-20261024`.

## Méthode

Nouvelle partie garçon, progression par les commandes uniquement. Le pilote
interdit les appels injectés, les écritures en RAM du jeu, les téléportations et
les équipes/drapeaux fabriqués. Les lectures servent à observer les menus,
la position, les données accessibles dans les fiches et les collisions pour guider les déplacements. Au départ, seul le champ visible
était mémorisé. À partir de la Forêt de Jade, une assistance lit la géométrie
de la carte courante pour limiter les détours, sans déplacer le joueur ni
changer les scripts, rencontres ou combats. Les captures montrent le moteur mGBA.
Les instantanés de l'émulateur conservent la session entre les relances du pilote ;
ils ne remplacent pas les fichiers `.sav` livrés. Ceux-ci sont exportés après
utilisation du menu SAUVER et seront rechargés avec CONTINUER pour vérification.

Les entrées et commandes sont conservées dans les artefacts de recette :
`ENTREES.jsonl`, `COMMANDES.jsonl` (chaîne de hachages) et `COURANT.json`.
Le premier combat du rival a été perdu ; la partie a continué normalement,
sans retour en arrière pour imposer une victoire. Premier partenaire : Komasan.
Son surnom saisi au clavier est `AAAAAAAAAA`, joueur `AA`.

## Étapes et sauvegardes prévues

L'ordre sera celui des événements effectivement rencontrés dans la partie.
Chaque ligne reste à faire tant qu'une sauvegarde réelle et ses preuves ne sont
pas présentes. Aucun stade final n'est considéré comme testé par anticipation.

- Début : premier partenaire, premier combat, colis de Chen et Médallium.
- Avant la Forêt de Jade ; avant le discours d'Argenta ; avant/après Wyatt.
- Avant le Mont Sélénite ; avant Azuria et son Arène ; rencontre de Léo.
- Avant Carmin sur Mer et la première conversation de quête avec Ariane ;
  enquête, Océane et progression de l'Arène.
- Avant la Grotte Sombre ; avant l'entrée à Lavanville et la Zombie Night ;
  sauvegarde distincte avant son affrontement décisif.
- Avant Céladopole ; Casino, Arène et Tour Yo-kai selon les prérequis réels.
- Avant Parmanie, Parc Safari, Surf/Force et Arène.
- Avant Safrania ; Yopple, libération et Arène de Domniscian.
- Avant Cramois'Île ; rencontre, exploration et Arène du passé.
- Avant la dernière Arène ; avant la Route Victoire et avant la Ligue.
- Avant le Conseil ; avant le combat final (sauvegarde de jeu quand le script
  autorise le menu, sinon dernière sauvegarde légale explicitement documentée).
- Après le générique : reprise en post-game ; quêtes des Îles Sevii,
  employés de Yopple, revanches, événements et rencontres uniques accessibles.
- Collection naturelle des 151 : rencontres, captures, cadeaux, évolutions et
  échanges du jeu ; avant chaque rencontre unique importante.
- Médallium 151/151 ; récompenses de collection et quête de Juste Yoann ;
  sauvegarde finale à 100 % après vérification des objectifs réellement disponibles.

## Avancement actuel

Le laboratoire, le colis de Chen, le Médallium et la première capture ont été
parcourus normalement. Granpapéti a été capturé sur la Route 2. La démonstration
du vieil homme et les cinq Dresseurs de la Forêt de Jade ont été rencontrés.
Le discours d’Argenta s’est terminé dans cette partie.

Le retour Argenta → Route 2 a été vérifié après les soins au Centre et une
entrée payante au musée : déplacements vers le sud, menu Start fonctionnel,
puis retour à Argenta. Ce contrôle ne valide pas les autres cinématiques par
anticipation. Le premier Dresseur de l’Arène d’Argenta est battu, mais les trois
premières tentatives contre Wyatt ont été perdues. La progression continue sans
recharger une ancienne issue pour obtenir une victoire. L’équipe s’entraîne
sur la Route 2 ; aucun Badge acquis et seulement deux Yo-kai obtenus à ce stade.

Huit sauvegardes natives ont été exportées après le menu SAUVER et rechargées
avec CONTINUER dans une nouvelle instance mGBA : laboratoire avant rival,
Médallium débloqué, avant la Forêt, première capture, porte de la Forêt,
avant le discours d’Argenta, avant l’Arène après vérification du retour Route 2,
et devant Wyatt avant le premier affrontement. Les positions, niveaux, PV et
le nombre de membres sont comparés, et le fichier fourni reste inchangé.

mGBA fonctionne sans limite de cadence. Les trajets groupés observés tournent
autour de x21 à x35 ; les entrées, menus, rencontres et récompenses restent ceux
du jeu. Les choix et interfaces inattendues interrompent la séquence pour
inspection. Cette vitesse ne signifie pas que le parcours à 100 % est terminé.

Les essais de capture ratés, les achats de Balls et les défaites ont consommé
leurs ressources normalement. Les deux surnoms `AAAAAAAAAA` proviennent de
saisies trop rapides du pilote dans l’écran de nommage, pas d’un défaut du jeu.
Le pilote a été corrigé pour refuser les surnoms lors des captures suivantes.
L’aventure, le post-game et la collection complète restent en cours.
