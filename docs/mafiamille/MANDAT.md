# POKÉMON × YO-KAI WATCH — IMPLÉMENTATION DE LA MAFIAMILLE

## 1. AUTORISATION OFFICIELLE

Je valide ton audit de remplacement de la Team Rocket par la Mafiamille et je t'autorise à commencer l'implémentation.

**Base de référence :**
`6f143452a026a41c08f1db38f9809959809a31b6`

Crée une nouvelle branche dédiée à partir de ce commit :

`feature/mafiamille-kanto`

Ne modifie pas directement `master`, les branches de restauration ou la branche audio `audio/integration-31-ost` au commit `837bd1757`.

L'objectif est de remplacer intégralement la Team Rocket par la Mafiamille, sans modifier les autres éléments du jeu.

## 2. PERSONNAGES ET SPRITES

Remplace :

- Giovanni par **Don Morléone** dans ses trois apparitions principales.
- Tous les sbires Rocket, masculins et féminins, par le **sbire Mafiamille classique** dans le monde.
- Le recruteur du Pont Pépite par ce même sbire.
- Les portraits de combat des sbires par les trois portraits Mafiamille existants, répartis entre les adversaires.
- Les portraits de Giovanni par celui de Don Morléone.

N'invente aucune variante féminine, aucun nouveau grade ni aucun personnage supplémentaire.

Conserve les identifiants techniques Rocket et Giovanni lorsqu'ils sont nécessaires au fonctionnement des événements et des sauvegardes.

### Animations de marche

Je t'autorise à récupérer sélectivement les animations de marche de Don Morléone et du sbire classique présentes dans le commit `740c257b2`, à condition de :

- Conserver l'apparence et les pixels des poses initiales validées.
- Ne récupérer aucun changement scénaristique de ce commit.
- Vérifier les quatre orientations et les déplacements.
- Fournir des captures et des aperçus animés.

**Les animations doivent être soumises à ma validation artistique avant d'être considérées comme définitives.**

## 3. ÉQUIPES DE DON MORLÉONE — VALIDÉES

Je valide définitivement les trois équipes actuellement présentes dans la base.

### Premier combat — Repaire de Céladopole

- Felipaix — niveau 24
- Pachycoul — niveau 25
- Crocho — niveau 29

### Deuxième combat — Sylphe SARL

- Bouh — niveau 35
- M. Felipaix — niveau 37
- Pachypipi — niveau 37
- Crocho — niveau 41

### Troisième combat — Arène de Jadielle

- Pachycoul — niveau 41
- M. Felipaix — niveau 42
- Crocho — niveau 44
- Pachypipi — niveau 45
- Tryptik — niveau 49

**Ne modifie ni les espèces ni les niveaux de ces trois équipes.**

Conserve également l'équipe existante du combat bonus postgame, sans modification.

## 4. ÉQUIPES DES SBIRES — VALIDATION DU PLAN

Je valide les compositions proposées dans ton audit pour les 27 équipes ordinaires à modifier, ainsi que les deux administrateurs et les deux sbires postgame concernés.

Les 16 espèces caractéristiques de la Mafiamille sont :

1. Bandinyan
2. Bouh
3. Nihilistik
4. Émousstik
5. Raltesse
6. Loubarbare
7. Racaïd
8. Lulugubre
9. Toumou
10. Lamlam'mou
11. Chiperpiou
12. Rapiaf
13. Crocho
14. Couchtar
15. Noctambill
16. Bonneto

Respecte les compositions exactes de ton audit.

Conserve les niveaux, le nombre de Yo-kai par équipe, les paramètres d'IA, les récompenses et les autres réglages existants, sauf problème technique démontré.

Vérifie que les capacités attribuées sont compatibles avec les espèces et leurs niveaux.

Ne modifie pas les 151 espèces, leurs statistiques ou leurs évolutions.

## 5. ADAPTATION INTÉGRALE DES DIALOGUES

Je t'autorise à réécrire les dialogues liés à la Team Rocket dans l'ensemble de Kanto et des îles Sevii.

Cela comprend :

- Les sbires et leurs dialogues de combat.
- Don Morléone.
- Les témoins, habitants et victimes.
- Le Casino et son repaire.
- La Tour Pokémon.
- La Sylphe SARL.
- L'arène de Jadielle.
- Les événements des îles Sevii.
- Les références indirectes à la Team Rocket.
- Le Memorydex, le journal de reprise, les noms de lieux et les descriptions concernées.

### Direction artistique et narrative

La Mafiamille doit conserver son identité de groupe mafieux issu de Yo-kai Watch.

Les dialogues doivent être naturels, en français, avec une personnalité cohérente :

- Les sbires sont loyaux à leur organisation.
- Don Morléone est autoritaire et charismatique.
- L'humour de Yo-kai Watch peut être présent sans devenir excessif.
- Les personnages extérieurs réagissent à la Mafiamille comme à une véritable organisation menaçante.

Ne te contente pas d'un remplacement automatique de noms lorsque les phrases nécessitent une adaptation.

Ne crée aucun nouvel arc narratif majeur.

### Cohérence de l'histoire

Ne transforme pas la référence au fils de Giovanni en une filiation inventée pour Don Morléone.

Adapte également les dialogues concernant la dissolution de l'organisation afin de préserver la cohérence avec les survivants des îles Sevii et le groupe Mafiamille postgame.

Conserve les événements, les conditions de progression et les récompenses existantes.

## 6. NOMS ET CONTRAINTES TECHNIQUES

Pour les combats :

- Utilise provisoirement **« D. Morléone »** si le champ de nom ne permet pas d'afficher le nom complet.
- Utilise **« Don Morléone »** dans les dialogues et les interfaces compatibles.
- Étudie la possibilité d'afficher son nom complet en combat sans modification risquée du moteur.

Pour les sbires :

- Affichage souhaité : **SBIRE MAFIAMILLE**.
- Tu peux conserver les identifiants techniques existants pour préserver les mécanismes du jeu.

Vérifie les longueurs des textes, les caractères français, les commandes de script et les variables.

## 7. SYMBOLES ROCKET DU CASINO

Tu as identifié des symboles « R » sur les machines à sous et leurs tableaux de gains.

Je valide le principe de les remplacer par un symbole cohérent avec la Mafiamille.

Cependant :

**Présente-moi plusieurs aperçus avant d'intégrer un nouveau symbole.**

Ne modifie pas les probabilités, les gains ou le fonctionnement des machines.

Vérifie également les autres éléments graphiques du repaire et de l'entrepôt susceptibles de contenir des références à la Team Rocket.

## 8. TESTS OBLIGATOIRES

Compile le jeu et effectue des tests dans mGBA.

Vérifie notamment :

- Les 69 acteurs de carte concernés.
- Les 53 fiches d'adversaires Rocket.
- Les trois combats principaux de Don Morléone.
- Les trois portraits Mafiamille en combat.
- Les animations de marche.
- Le recruteur du Pont Pépite.
- Les événements du Mont Sélénite.
- Le repaire de Céladopole.
- La Tour Pokémon et M. Fuji.
- La Sylphe SARL.
- Le huitième Badge à Jadielle.
- Les événements des îles Sevii.
- Le groupe Mafiamille postgame.
- Les récompenses et les sauvegardes.
- Les dialogues et les références indirectes.

Vérifie également la préservation des 151 Yo-kai, des starters, des évolutions, des mécaniques personnalisées, des autres Champions, de la Ligue et des musiques existantes.

N'annonce pas qu'un élément est testé si tu n'as effectué qu'une vérification statique.

## 9. MÉTHODE DE LIVRAISON

Procède par lots cohérents :

1. Branche de travail et protection des ressources.
2. Personnages, portraits et animations.
3. Équipes des sbires.
4. Dialogues et adaptation de l'organisation.
5. Aperçus des symboles du Casino.
6. Tests de progression et rapport final.

Tu peux effectuer les modifications techniques et scénaristiques explicitement autorisées ci-dessus.

En revanche, attends ma validation pour :

- Les animations de marche définitives.
- Le nouveau symbole du Casino.
- Toute modification artistique importante non prévue.
- Toute modification des équipes de Don Morléone.

Publie les commits sur la branche dédiée, sans fusion.

## 10. OBJECTIF FINAL

Je veux que, du point de vue du joueur, **la Team Rocket ait complètement disparu de Pokémon Rouge Feu pour laisser place à la Mafiamille de Yo-kai Watch**.

Tous les sbires, leurs équipes, leurs apparitions, les dialogues et les références doivent être cohérents avec cette transformation.

La structure de Kanto et la progression originale doivent rester intactes.

Une fois l'implémentation terminée, présente-moi un rapport complet avec les captures, les tests, les éléments nécessitant encore ma validation et le commit GitHub final.

**Tu es autorisé à commencer le développement.**