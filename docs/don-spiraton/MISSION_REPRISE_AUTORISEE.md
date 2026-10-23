# POKÉMON × YO-KAI WATCH — REPRISE ET FINALISATION DU PROTOTYPE DON SPIRATON

## 1. Contexte

Dépôt GitHub : `JusteYoann/Pokemon-Yokai-Watch`

Branche de travail :
`feature/boss-final-don-spiraton`

Dernier commit annoncé :
`1a3ea491f`

Le développement du boss final Don Spiraton a été interrompu à la suite d'une indisponibilité de l'environnement.

Un commit a été créé localement, mais sa publication sur GitHub n'a pas été confirmée.

Des optimisations et corrections supplémentaires pourraient également être restées uniquement dans l'environnement local.

**Ta priorité absolue est de récupérer, vérifier et sécuriser le travail existant avant toute nouvelle modification.**

## 2. Étape A — Récupération et sécurisation

Commence par examiner :

- L'état du dépôt local.
- La branche actuellement active.
- L'existence du commit `1a3ea491f`.
- Sa présence éventuelle sur GitHub.
- Les différences entre la branche locale et la branche distante.
- Les fichiers modifiés non commités.
- Les commits locaux non publiés.
- Les éventuels conflits ou fichiers temporaires.

Si des modifications locales existent encore, préserve-les avant toute opération susceptible de les écraser.

Ne lance pas de `reset --hard`, de nettoyage destructif ou de rebase risqué.

Ne recrée pas le prototype si ses fichiers sont récupérables.

Si l'ancien environnement local est inaccessible et que certaines corrections ont été perdues, distingue clairement ce qui est récupérable de ce qui doit être reconstruit.

**Fournis un premier bilan de récupération avant de poursuivre.**

## 3. État du prototype à retrouver

Le dernier rapport annonçait les éléments suivants :

- Don Spiraton possède un système spécial de huit formes.
- Son entrée en combat ne comporte pas d'envoi adverse par Poké Ball.
- Le véritable sprite de Don Spiraton apparaît au début du combat.
- Sa première métamorphose intervient après que le joueur a choisi son action, au début du tour 1.
- La capture et la fuite sont interdites.
- Les transformations suivantes sont prévues à la fin des tours.
- Le nom du combattant reste Don Spiraton.
- Les formes doivent changer de types, statistiques, capacités et PV.
- La musique prévue est `Vs. Zazelmare`.

**Vérifie chacun de ces éléments dans le code et les tests.**

Ne considère pas une fonctionnalité comme terminée simplement parce qu'elle a été annoncée précédemment.

## 4. Nouvelle mise en scène définitive de la fusion

Je confirme qu'aucun sprite overworld de Don Spiraton ne doit être créé.

Aucun sprite intermédiaire de fusion n'est nécessaire.

La transformation doit être représentée par une transition entre la carte et l'écran de combat.

### Déroulement exact

Après la première victoire contre Don Morléone :

1. Matt entre dans la salle du Maître.
2. Matt soigne entièrement l'équipe du joueur, PV, PP et statuts compris.
3. Don Morléone reprend la parole.
4. Il s'écrie : « MAFIAMILLE ! À MOI ! »
5. Les sbires présents se précipitent vers Don Morléone.
6. Au moment où ils l'atteignent, un flash blanc recouvre entièrement l'écran.
7. Le flash masque la disparition de Don Morléone et de ses sbires.
8. La transition vers le combat final commence.
9. La musique **Vs. Zazelmare** démarre.
10. Le sprite de combat de Don Spiraton apparaît, sous sa véritable apparence.
11. Le message « Don Spiraton apparaît ! » est affiché.
12. Le joueur accède normalement au menu de combat.

### Contraintes

- Réutiliser les sprites overworld Mafiamille déjà validés.
- Réutiliser les animations de déplacement existantes.
- Ne pas créer de sprite overworld de Don Spiraton.
- Ne pas créer de sprite de fusion.
- Ne pas modifier les graphismes Mafiamille validés.
- Ne pas afficher de Poké Ball adverse.
- Ne pas rendre Don Spiraton capturable.
- Ne pas permettre la fuite.
- Ne pas déclencher la première métamorphose avant le choix du joueur.

Le flash doit être suffisamment visible pour masquer la disparition des personnages, mais ne doit pas laisser l'écran blanc bloqué.

## 5. Première métamorphose

Don Spiraton commence le combat sous sa véritable apparence.

Le joueur choisit son action.

Au début du premier tour, avant les attaques, Don Spiraton se transforme automatiquement en une première espèce volontairement faible.

Cette transformation :

- Réutilise l'animation de Morphing.
- Ne consomme pas l'action de Don Spiraton.
- Ne dépend pas de sa Vitesse.
- Ne compte pas comme une neuvième forme.
- Ne déclenche aucun K.O.

Message :

« Don Spiraton se transforme en [Yo-kai] ! »

**La première espèce n'est pas encore définitivement choisie. Ne la sélectionne pas arbitrairement.**

Prévois une configuration explicite et facilement modifiable pour cette espèce.

## 6. Les sept transformations suivantes

Don Spiraton possède huit formes à vaincre au total.

Niveaux successifs :

56, 57, 58, 59, 60, 61, 62 et 63.

Lorsqu'une barre atteint zéro :

- Aucun K.O. traditionnel n'est déclenché.
- Aucun gain d'expérience n'est accordé.
- Aucune Poké Ball n'apparaît.
- Aucune proposition gratuite de changement de Yo-kai n'est offerte.
- L'action restante de la forme vaincue est annulée.
- La transformation est mise en attente jusqu'à la fin du tour.
- Les effets de fin de tour doivent être résolus sans appliquer de dégâts à une forme déjà épuisée.
- Don Spiraton analyse uniquement le Yo-kai actuellement sur le terrain.
- Il sélectionne le meilleur contre parmi les 151 Yo-kai.
- Il utilise l'animation de Morphing.
- Il adopte les types, statistiques et attaques légales de la nouvelle espèce.
- Il récupère une nouvelle barre de PV complète.
- Le tour suivant commence.

Une forme déjà vaincue ne peut pas être réutilisée.

Les dégâts excédentaires ne passent jamais à la barre suivante.

## 7. Gestion des attaques et des statuts

Le nom affiché doit rester **Don Spiraton**, quelle que soit sa forme.

Exemple :

« Don Spiraton utilise Tempête de Sable ! »

Les attaques disponibles peuvent provenir de l'apprentissage naturel ou des CT compatibles avec l'espèce empruntée.

Aucune attaque impossible à apprendre ne doit être attribuée.

À chaque transformation, les altérations de statut de Don Spiraton disparaissent.

Affiche un message approprié lorsqu'un statut est supprimé.

Exemple :

« Don Spiraton n'est plus brûlé ! »

Vérifie également les effets temporaires, les capacités à plusieurs coups, les dégâts différés, les changements forcés et les situations où le Yo-kai du joueur est mis K.O. pendant un tour de transformation.

## 8. Les huit couches de vie

La première barre est verte et la deuxième orange.

Les six autres couleurs restent soumises à validation artistique.

Les barres doivent être visuellement superposées, avec la couche active au premier plan.

Lorsqu'une couche est épuisée, elle disparaît et révèle la suivante.

Le joueur doit comprendre qu'il affronte un boss unique, pas huit adversaires classiques.

Prépare une prévisualisation fidèle du système dans l'interface de combat.

N'impose pas définitivement les couleurs restantes sans mon accord.

## 9. Sprite de combat de Don Spiraton

Nous avons déjà réalisé un sprite de combat de Don Spiraton.

Une version graphiquement simplifiée est également à l'étude pour mieux correspondre au style de nos autres Yo-kai.

**Ne remplace pas le sprite existant sans validation.**

Pour le moment, utilise les ressources graphiques déjà présentes dans le prototype.

Si le sprite définitif manque, signale-le et prépare uniquement son emplacement technique.

Ne crée aucun nouveau sprite overworld.

## 10. Première conquête et revanche postgame

La première conquête de la Ligue doit opposer le joueur à :

1. Don Morléone, combat traditionnel.
2. Don Spiraton, combat spécial à huit formes.

Matt intervient entre les deux combats pour soigner le joueur.

Après la victoire contre Don Spiraton, le joueur doit pouvoir accéder au Panthéon, aux crédits et au postgame.

Lors des revanches ultérieures, **Matt devient le Maître de la Ligue**.

Sa musique de combat doit être :

**Decisive Battle — Yo-kai Watch**

Conserve ses équipes de revanche et leurs variantes.

Le combat contre Don Spiraton ne doit pas se répéter lors des revanches.

## 11. Musiques

Affectations confirmées :

- Don Morléone : `vs. The Ghoulfather`.
- Don Spiraton : `Vs. Zazelmare`.
- Matt postgame : `Decisive Battle`.

Ne modifie pas les autres utilisations de ces OST.

Ne fusionne pas la branche audio expérimentale.

## 12. Finalisation technique

Une fois le travail récupéré et sécurisé :

1. Termine le raccordement de la cinématique dans la salle du Maître.
2. Implémente la convergence des sbires.
3. Ajoute le flash blanc.
4. Raccorde la transition au combat contre Don Spiraton.
5. Vérifie le fonctionnement des huit formes.
6. Vérifie les conditions de victoire et de défaite.
7. Vérifie le soin complet de Matt.
8. Vérifie les transitions musicales.
9. Vérifie le Panthéon et les crédits.
10. Vérifie les revanches postgame.

Si une fonctionnalité nécessite une décision créative non encore validée, utilise un prototype isolé ou suspends uniquement cette partie.

N'invente pas de dialogues de conclusion.

## 13. Tests obligatoires

Compile les ROM publique et privée.

Vérifie la limite de 32 Mio.

Teste dans mGBA :

- La première entrée dans la salle du Maître.
- Le premier combat contre Don Morléone.
- Le soin de Matt.
- Les déplacements des sbires.
- Le flash blanc.
- L'apparition de Don Spiraton.
- La musique Vs. Zazelmare.
- La première métamorphose.
- Les sept transformations suivantes.
- La sélection des contres.
- Les capacités CT.
- La disparition des statuts.
- Les dégâts excédentaires.
- Les attaques à plusieurs coups.
- Les sauvegardes.
- Le Panthéon.
- Les crédits.
- Les revanches contre Matt.

Fournis des captures réelles mGBA lorsque c'est possible.

Distingue les tests automatisés des tests réellement effectués dans l'émulateur.

## 14. Publication et livrables

Lorsque les modifications sont stabilisées :

- Crée des commits clairement identifiés.
- Publie-les sur `feature/boss-final-don-spiraton`.
- Vérifie que les commits sont réellement présents sur GitHub.
- Fournis les liens vers les commits.
- Fournis un rapport détaillé.
- Indique les fonctionnalités opérationnelles, partielles ou non implémentées.
- Signale les validations artistiques encore nécessaires.

Ne fusionne aucune branche.

Ne modifie pas `master`.

Ne touche pas aux autres branches validées.

## 15. Priorité absolue

**Ne repars pas de zéro.**

Récupère d'abord le travail existant, confirme son état, puis termine les éléments manquants.

Je veux une version techniquement stable du boss final Don Spiraton, tout en conservant le contrôle sur les dernières décisions artistiques.

Si le commit `1a3ea491f` est introuvable ou si des modifications locales importantes sont irrécupérables, arrête-toi et présente-moi la situation avant de reconstruire quoi que ce soit.

Tu peux commencer par la récupération et la vérification du dépôt, puis poursuivre les travaux récupérables sans prendre de décisions créatives non autorisées.