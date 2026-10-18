# POKÉMON × YO-KAI WATCH — MISSION FINALE : TERMINER ET PRODUIRE LA PREMIÈRE ROM JOUABLE

Je te confie maintenant la mission de finalisation complète de Pokémon × Yo-kai Watch, version 1.0.

**Mon objectif est que tu termines tous les travaux restants au cours de cette session si cela est techniquement possible, puis que tu génères enfin la première ROM finalisée et jouable du projet.**

Je souhaite que tu privilégies l'exécution concrète plutôt que de multiplier les audits, les comptes rendus intermédiaires et les demandes de validation.

Ce message remplace les anciennes priorités de développement lorsqu'elles sont contradictoires.

Il ne remet pas en cause les choix déjà validés concernant les 151 Yo-kai, les personnages, leurs équipes, leurs statistiques ou les événements existants.

## 1. REPRENDRE LE DERNIER ÉTAT SANS PERDRE LE TRAVAIL

Dépôt : `JusteYoann/Pokemon-Yokai-Watch`

Branche : `dev/reconstruction-finalisation`

Dernier jalon connu : `c3fd5e8957`. Vérifie le véritable dernier commit avant de commencer.

Récupère les éventuelles modifications locales non publiées et sauvegarde-les si elles sont valides.

Vérifie rapidement la compilation et les tests existants.

Ne recommence pas les développements déjà terminés.

Les 151 Yo-kai, leurs données, les protagonistes, Matt, les équipes, les caméos et les événements déjà intégrés doivent être préservés.

**Travaille directement sur les tâches inachevées.**

## 2. PÉRIMÈTRE DÉFINITIF DE LA VERSION 1.0

La version 1.0 doit comprendre :

- L'aventure principale de Bourg Palette jusqu'à la victoire contre Matt, Champion de la Ligue.
- Les 151 Yo-kai, leurs attaques, statistiques, talents et évolutions.
- La possibilité d'obtenir les 151 Yo-kai sur une seule sauvegarde.
- Nathan et Katie comme protagonistes.
- Matt comme rival fixe.
- Les champions d'arène, la Team Rocket et le Conseil 4.
- Les Îles Sevii et le postgame existant.
- Les caméos déjà développés et leurs combats.
- Le Seigneur Enma et son protégé, Enma capturable.
- Les rencontres statiques personnalisées.
- Le Médallium des Yo-kai.
- Le système de partage d'expérience permanent.
- Les 15 OST définitivement sélectionnées.
- Les graphismes, textes et mécanismes nécessaires au bon déroulement du jeu.
- Une sauvegarde fiable et compatible avec toute la version 1.0.

**Sont officiellement reportés et ne doivent plus bloquer la version 1.0 :**

- Les dix nouvelles quêtes secondaires.
- La quête du scientifique avec Robonyan.
- Le quartier général et la quête de Coach Antonic.
- Le combat supplémentaire contre Red.
- Le caméo supplémentaire de Juste Yoann.
- La nouvelle cinématique d'introduction.
- Les musiques non retenues dans la sélection définitive.

Conserve cependant tous les événements et caméos historiques déjà implémentés et fonctionnels.

Ne développe aucune nouvelle quête.

Ne supprime pas arbitrairement des éléments importants déjà validés.

## 3. FINALISER LA SÉLECTION DÉFINITIVE DE 15 OST

Notre sélection musicale définitive est maintenant fixée.

### Sept OST déjà intégrées à conserver

1. **Bicycle Theme** — vélo.
2. **Vs. Hinozall (English)** — combat contre Domniscian.
3. **Infinite Tunnel** — Tour de Lavanville.
4. **Vs. Zazelmare** — combat contre Seigneur Enma.
5. **Bada-Bing Tower** — Sylphe SARL occupée.
6. **Decisive Battle** — combats du Conseil 4 et revanches.
7. **Somewhere A Bit Dodgy (BBQ)** — Repaire Rocket de Céladopole.

### Huit OST à intégrer

8. **San Fantastico** — Carmin sur Mer.
9. **Uptown Springdale** — Céladopole, extérieur.
10. **Vs. The Ghoulfather** — combat contre Don Morleone.
11. **Enma Track** — dialogues avec le Seigneur Enma.
12. **Mystic Grove** — Caverne Azurée.
13. **Hoppers Gorge** — Mont Sélénite.
14. **Final Battle – Are You Ready?** — combat final contre Matt lorsqu'il est Champion de la Ligue.
15. **36. Take Care, Grandpa 1 — Yo-kai Watch 2 OST** — séquence de conclusion après la victoire contre Matt.

### Anciennes musiques à retirer de la ROM musicale

- **Mount Wildwood in the Past** — Bois Baies.
- **Harrisville** — Île 2.
- **Mini Boss Battle** — employés de Domniscian et Mafiamille.

Rétablis une musique native appropriée sur ces emplacements, sans modifier les événements ou les combats.

Les musiques des maisons de Nathan et Katie sont également retirées des objectifs de la version 1.0. Leurs maisons peuvent conserver les thèmes natifs.

Les musiques des quêtes reportées et Enma Villa ne doivent pas être intégrées pour cette version.

### Exigences techniques

Utilise la méthode DPCM déjà validée, à partir du pipeline existant.

Optimise les boucles pour limiter la taille de la ROM tout en préservant les introductions importantes.

Les musiques doivent être réellement audibles dans les lieux et les combats prévus.

**Pour Matt :** la nouvelle OST doit se déclencher uniquement lors de son combat de Champion, pas lors de ses précédents combats de rival.

**Pour la conclusion :** Take Care, Grandpa 1 doit commencer après la victoire contre Matt, à un moment narrativement cohérent, sans interrompre le combat ni perturber le Panthéon et les crédits.

Pour les nouveaux titres, commence par vérifier la disponibilité et l'identité exacte des enregistrements privés. Ne remplace jamais un morceau manquant par une piste approximative en prétendant qu'il s'agit de la musique demandée.

Si certains fichiers audio sont absents, poursuis les autres travaux indépendants et précise les sources nécessaires. Ne télécharge pas automatiquement de copies non autorisées.

Teste dans mGBA les boucles, transitions, fanfares, bruitages, retours de combats, volumes et sauvegardes.

Vérifie que la ROM reste dans la capacité prévue de 32 Mio.

Les enregistrements protégés et les données audio qui en dérivent doivent rester privés. Ne les publie pas sur GitHub.

## 4. TERMINER L'ADAPTATION SCÉNARISTIQUE

### Professeur Chen

Il est l'inventeur de la Yo-kai Watch.

Cette invention permet au joueur de voir les Yo-kai normalement invisibles.

Au cours de précédentes explorations, Chen a découvert une relique ancienne : le Médallium des Yo-kai.

Il souhaite que le joueur participe à la Ligue Yo-kai et complète parallèlement le Médallium en répertoriant les 151 espèces.

Conserve le déroulement fonctionnel du début du jeu.

La montre agit comme une justification narrative passive, sans nouvelle mécanique complexe.

### Léo

Léo est l'inventeur du PC et des Boîtes Yo-kai.

Lorsqu'on le rencontre sur la Route 25, son expérience scientifique l'a accidentellement transformé en Yo-kai.

Choisis un Yo-kai reconnaissable parmi les 151, sans utiliser une rencontre légendaire ou secrète.

Remplace son apparence transformée et adapte ses dialogues.

Préserve le système original qui permet au joueur de le ramener à sa forme humaine.

### Seigneur Enma

Le Seigneur Enma est le personnage rencontré au Mont Braise.

Le Yo-kai Enma de la Caverne Azurée est une créature céleste artificielle issue d'une expérience ayant cherché à reproduire la puissance du Seigneur Enma à partir de Jibanyan.

Après s'être échappé, ce Yo-kai a été recueilli par le Seigneur Enma.

Cela explique pourquoi il figure dans son équipe.

Après sa défaite, le Seigneur Enma doit féliciter chaleureusement le joueur, se montrer fier de ses progrès et lui confier qu'il compte sur lui pour préserver l'équilibre entre humains et Yo-kai.

Sa victoire débloque la rencontre capturable d'Enma dans la Caverne Azurée.

Les deux entités doivent conserver des sprites, interactions et mécaniques distincts.

Ne crée aucune seconde capture ou récompense automatique.

### Conclusion de la Ligue

Vérifie que la victoire contre Matt en tant que Champion donne lieu à une véritable conclusion cohérente.

La musique Take Care, Grandpa 1 doit contribuer à l'émotion de cette séquence.

Conserve le Panthéon, les crédits et la possibilité de poursuivre le postgame.

Ne transforme pas cette scène en nouvelle quête.

## 5. TERMINER L'HARMONISATION DU VOCABULAIRE

Je souhaite que tous les textes normalement visibles par le joueur soient adaptés à l'univers Yo-kai Watch.

Notamment :

- Pokémon → Yo-kai.
- Pokédex → Médallium.
- Poké Ball → Yo-kai Ball.
- Centre Pokémon → Centre Yo-kai.
- Ligue Pokémon → Ligue Yo-kai.
- Dresseur Pokémon → Dresseur de Yo-kai.
- Boîtes Pokémon → Boîtes Yo-kai.
- Pokémon sauvage → Yo-kai sauvage.

Cela concerne les dialogues, menus, messages de combat, objets, descriptions, interfaces et tutoriels.

Ne réalise pas de remplacements aveugles susceptibles d'endommager le code.

Les noms techniques internes peuvent rester inchangés.

Adapte naturellement les formulations françaises et respecte la taille des fenêtres et les limites du moteur GBA.

Teste les textes réellement affichés, pas seulement les fichiers sources.

## 6. FINALISER LES GRAPHISMES MANQUANTS

### Yo-kai statiques

Vérifie que les rencontres suivantes utilisent les bons sprites sur la carte :

- Misterre sur les Routes 12 et 16, à la place de Ronflex.
- Mademoaiselle aux Îles Écume, à la place d'Artikodin.
- Octorgone à la Centrale, à la place d'Électhor.
- Kyubi au Mont Braise.
- Enma capturable dans la Caverne Azurée.

Le Seigneur Enma au Mont Braise reste un personnage distinct du Yo-kai Enma.

### Léo transformé

Intègre son nouveau sprite Yo-kai, sans casser la séquence originale.

### Variantes shiny

Termine les variantes graphiques shiny prévues par les références validées.

Respecte la liste des espèces autorisées et interdites.

Le système shiny doit rester fonctionnel, avec les bonnes palettes, y compris lors de la capture, de l'affichage de l'équipe et des combats.

Privilégie la fidélité aux références plutôt que des recolorations arbitraires.

Conserve les graphismes déjà validés de Nathan, Katie, Matt et des autres personnages.

## 7. ÉQUILIBRER ET VÉRIFIER LE GAMEPLAY

Contrôle les niveaux des adversaires, leurs équipes, leurs attaques et les objets.

Vérifie que le partage d'expérience permanent permet de progresser naturellement.

La difficulté doit rester intéressante sans nécessiter de longues séances de progression répétitive.

Ne modifie pas arbitrairement les statistiques validées des 151 Yo-kai.

Vérifie les trois starters, leurs évolutions et leur équilibre.

Contrôle les objets d'évolution, les fossiles, les cadeaux, les échanges adaptés, les rencontres rares et les légendaires.

Les 151 espèces doivent réellement pouvoir être obtenues sur une seule sauvegarde.

Aucun Yo-kai ne doit devenir définitivement inaccessible à cause d'une erreur d'événement ou d'évolution.

## 8. RECETTE COMPLÈTE ET CORRECTION DES BUGS

Cette étape est obligatoire avant toute déclaration de version finale.

Réalise autant que possible une véritable partie de validation dans mGBA, du début de l'aventure jusqu'à la victoire contre Matt et au Panthéon.

Vérifie ensuite les Îles Sevii, les rencontres statiques, les caméos existants et le postgame.

Complète cette vérification par des tests automatisés reproductibles.

Contrôle notamment :

- Création de personnage, Nathan ou Katie.
- Choix du prénom et Matt comme rival.
- Introduction et laboratoire du Professeur Chen.
- Obtention de la Yo-kai Watch et accès au Médallium.
- Rencontres sauvages et captures.
- Évolutions et attaques.
- Huit arènes.
- Team Rocket.
- Combat final contre Matt.
- Panthéon, crédits et sauvegarde.
- Îles Sevii.
- Seigneur Enma et capture de son protégé.
- Rencontres statiques.
- Obtention possible des 151 Yo-kai.
- Système shiny.
- Toutes les musiques retenues et leurs transitions.
- Absence de régressions graphiques et de blocages.

**Les tests ciblés avec téléportation ou équipe surpuissante ne constituent pas à eux seuls une recette complète.**

Si une partie entière ne peut pas être testée, signale clairement cette limite et ne prétends pas l'avoir réalisée.

Corrige les bugs bloquants avant de considérer la ROM comme terminée.

## 9. GITHUB ET REPRODUCTIBILITÉ

Travaille exclusivement sur une branche adaptée à la finalisation, sans écraser directement `master`.

Préserve l'historique et les archives de récupération.

Sauvegarde régulièrement les modifications sur GitHub.

Chaque étape fonctionnelle importante doit faire l'objet d'un commit.

Vérifie que les sources publiques permettent toujours de compiler leur version sans audio privé, avec les musiques natives de remplacement.

Vérifie également la reconstruction de la version musicale privée à partir des enregistrements légalement disponibles dans l'environnement.

Ne publie ni ROM ni enregistrements protégés sur le dépôt public.

Documente les dépendances et la procédure permettant de reconstruire les deux variantes.

## 10. CONDITION DE FIN : PRODUIRE LA PREMIÈRE ROM FINALISÉE

**C'est le résultat final que j'attends de cette mission.**

Une fois toutes les tâches obligatoires terminées et les tests de stabilité suffisamment concluants :

1. Compile une véritable ROM privée de Pokémon × Yo-kai Watch version 1.0, avec les 15 OST sélectionnées.
2. Vérifie qu'elle démarre normalement dans mGBA.
3. Vérifie qu'une sauvegarde peut être créée, rechargée et poursuivie.
4. Vérifie que l'aventure principale peut être terminée et que le postgame reste accessible.
5. Contrôle les musiques, les graphismes et l'absence de bugs bloquants connus.
6. Calcule son empreinte SHA-256 et sa taille.
7. Conserve la ROM dans un emplacement privé clairement identifié.
8. Fournis-moi cette ROM compilée comme pièce jointe privée, si ton environnement autorise sa transmission et si les droits sur son contenu le permettent. Sinon, fournis une méthode locale de reconstruction ou un patch approprié qui ne redistribue pas les ressources protégées.
9. Publie les derniers fichiers sources redistribuables et les rapports techniques sur GitHub.

**N'annonce pas une ROM comme « version 1.0 finale » si elle présente encore un bug bloquant ou si ses tests indispensables sont incomplets.**

Dans ce cas, conserve une version de développement testable, documente les problèmes restants et poursuis les corrections si ton temps d'exécution le permet.

La sortie finale doit correspondre au jeu réellement développé, et pas à Rouge Feu d'origine ou à une simple ROM expérimentale.

## 11. AUTONOMIE ET EXÉCUTION EN UNE SESSION

Je souhaite que tu réalises le maximum de ce travail **durant cette seule session**, idéalement jusqu'à la génération de la ROM 1.0.

Ne t'arrête pas après chaque étape pour me demander une nouvelle validation.

N'effectue pas de nouveaux audits complets si les contrôles existants sont suffisants.

Passe directement au développement, à l'intégration, aux tests et aux corrections.

Prends les décisions techniques secondaires nécessaires pour avancer, sans modifier les choix artistiques et scénaristiques validés.

Si certaines tâches sont indépendantes, organise-les pour avancer efficacement.

Si une fonctionnalité secondaire menace la stabilité du jeu, privilégie la stabilité.

Si ton quota ou ton environnement interrompt le travail :

- Sauvegarde immédiatement toutes les modifications fonctionnelles sur GitHub.
- Consigne exactement le dernier commit et l'état des tests.
- Identifie les tâches réellement terminées et celles qui restent.
- Fournis un point de reprise permettant de poursuivre sans recommencer le travail.

Ne déclare jamais une tâche terminée uniquement parce que son code compile.

**Je te demande de viser une version finale réellement jouable, pas simplement un pourcentage d'avancement élevé.**

## OBJECTIF ULTIME

Je veux enfin pouvoir lancer Pokémon × Yo-kai Watch et vivre l'aventure que nous avons construite.

Une aventure complète avec les 151 Yo-kai, Nathan ou Katie, Matt, les personnages emblématiques, le Médallium, la Ligue Yo-kai, le postgame et nos 15 musiques sélectionnées.

Je souhaite pouvoir utiliser cette version pour mes tournages de décembre.

**Ta mission est de terminer tous les éléments encore nécessaires, de vérifier le jeu, puis de produire la première ROM finalisée et jouable si les critères de validation sont remplis.**

Commence maintenant. Ne t'arrête pas à un simple rapport d'avancement : développe, intègre, teste, corrige et livre le résultat le plus complet possible.