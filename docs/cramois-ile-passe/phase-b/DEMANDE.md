# CODEX — Cramois'Île : phase B, frontière temporelle maritime

## 1. Contexte du projet

Dépôt GitHub : `JusteYoann/Pokemon-Yokai-Watch`

Branche existante : `feature/cramois-ile-passe`

Référence du prototype validé : `1f335d268`

Rapport :
`docs/cramois-ile-passe/README.md`

La phase A est terminée : le sépia brun doré fonctionne sur les treize cartes de Cramois'Île, ses intérieurs, ses PNJ et ses combats. Les interfaces conservent leurs couleurs normales.

Les versions publique et privée ont passé les 40 contrôles du prototype et les 14 tests de régression du suivi d'Ariane. La dernière mesure indiquait 796 octets d'EWRAM libres.

**Mission : implémenter exclusivement la phase B, c'est-à-dire la brume maritime et les transitions temporelles.**

Ne pas commencer la phase C ni modifier les dialogues, les équipes ou le quiz.

## 2. Concept artistique

Cramois'Île se trouve 60 ans dans le passé.

Lorsqu'un joueur s'en approche par la mer, il traverse une zone de brume épaisse représentant la frontière entre deux époques.

À l'intérieur de cette frontière, il découvre Cramois'Île dans sa palette sépia nostalgique.

Lorsqu'il repart, il traverse de nouveau la brume avant de retrouver le Kanto actuel et ses couleurs normales.

La brume représente **le passage entre les époques**.

Le sépia représente **le passé**.

Ces deux effets doivent rester visuellement distincts.

## 3. Emplacement de la brume

Identifier précisément les accès maritimes à Cramois'Île, notamment :

- Route 20, à l'est de l'île.
- Route 21, au nord de l'île.

La brume doit apparaître dans une zone maritime proche de Cramois'Île, et non sur toute la longueur de ces routes.

Elle doit fonctionner dans les deux sens :

- Kanto actuel → Cramois'Île.
- Cramois'Île → Kanto actuel.

**Règle absolue : aucune brume permanente à l'intérieur de Cramois'Île.**

Le joueur doit pouvoir parcourir normalement l'extérieur, l'Arène, le Manoir, le laboratoire des fossiles et les autres bâtiments, avec une visibilité parfaite et le sépia déjà validé.

Ne pas introduire de brume dans les intérieurs ou pendant les combats.

## 4. Rendu visuel attendu

Créer une brume :

- Blanche ou gris clair.
- Dense et mystérieuse.
- Douce, légèrement animée si techniquement possible.
- Suffisamment opaque pour évoquer une traversée temporelle.
- Compatible avec le pixel art GBA.
- Sans coloration verte.
- Sans altérer durablement les palettes du jeu.

Je souhaite que l'arrivée à Cramois'Île soit une véritable petite expérience visuelle.

### Déroulement souhaité

1. Le joueur navigue sur une route maritime normale.
2. À l'approche de l'île, la brume commence à apparaître.
3. La visibilité diminue progressivement.
4. Le joueur traverse une portion de mer enveloppée de brume.
5. La brume se dissipe.
6. Cramois'Île apparaît dans son ambiance sépia brun doré.

La transition inverse doit être aussi cohérente.

Privilégier une animation progressive plutôt qu'un changement brutal d'état.

La brume ne doit pas nécessiter d'interaction, de dialogue ou de confirmation du joueur.

## 5. Contraintes techniques

Avant d'implémenter, auditer les possibilités du moteur Pokémon Rouge Feu et les systèmes déjà ajoutés au ROM hack.

Réutiliser les capacités existantes du moteur lorsque c'est possible.

Éviter :

- Les allocations EWRAM permanentes importantes.
- Les traitements coûteux à chaque image.
- Les conflits de palettes.
- Les conflits avec les effets météorologiques existants.
- Les ralentissements visibles.
- Les effets qui restent actifs après un changement de carte.
- Les modifications des graphismes validés sans nécessité.

Ne pas réutiliser directement la brume verte de Lavanville : son atmosphère nocturne et son système doivent rester indépendants.

Le prototype sépia de Cramois'Île doit conserver exactement son comportement actuel.

La transition doit gérer correctement les changements de cartes, les palettes matérielles, les effets de fondu et la reprise après sauvegarde.

Si une animation très dense est impossible sans risque pour la stabilité, proposer une alternative techniquement sûre qui conserve l'impression de frontière temporelle.

Ne pas contourner une difficulté en supprimant des PNJ, des événements ou des fonctionnalités existantes.

## 6. Déplacements particuliers

Examiner explicitement les cas suivants :

- Arrivée par Surf depuis la Route 20.
- Arrivée par Surf depuis la Route 21.
- Départ par chacune de ces routes.
- Demi-tour pendant la traversée de la brume.
- Entrées et sorties répétées de la zone.
- Sauvegarde et chargement près de la frontière.
- Sauvegarde et chargement à Cramois'Île.
- Entrée et sortie des bâtiments.
- Vol vers Cramois'Île, si accessible.
- Téléport, Tunnel et Corde Sortie lorsque les mécaniques du jeu les autorisent.
- Retour sur l'île après la Ligue.

Ne pas forcer artificiellement un passage par la brume lorsque le joueur utilise un moyen de déplacement qui ne traverse pas physiquement la frontière maritime.

Dans ce cas, l'état temporel et les palettes doivent simplement être corrects à l'arrivée.

## 7. Préservation des fonctionnalités existantes

Préserver sans régression :

- Les 151 Yo-kai et leurs données.
- Les équipes des Dresseurs et Champions.
- La Mafiamille.
- L'enquête de la Pierre Philosovni.
- Le suivi d'Ariane.
- Le combat duo avec Usapion.
- La remise de Coupe.
- La nuit et la brume verte de Lavanville.
- Le Manoir Pokémon.
- Le laboratoire des fossiles.
- La Clé Secrète.
- L'Arène de Cramois'Île.
- Les combats sauvages et de Dresseurs.
- Le sépia de la phase A.
- La Ligue et Don Spiraton.
- Les musiques privées.

Ne pas modifier les 5 821 ressources graphiques validées ni les données existantes sans justification technique explicite.

Ne pas agrandir le format de sauvegarde.

## 8. Validation mGBA

Compiler les versions publique et privée.

Tester réellement dans mGBA :

1. Traversée de la Route 20 vers Cramois'Île.
2. Traversée de la Route 21 vers Cramois'Île.
3. Départ par les deux routes.
4. Demi-tour dans la brume.
5. Traversées répétées sans dégradation visuelle.
6. Dissipation complète de la brume à l'arrivée.
7. Absence de brume sur les treize cartes de l'île.
8. Sauvegarde et reprise à proximité de la frontière.
9. Sauvegarde et reprise à l'intérieur de l'île.
10. Conservation du sépia dans les intérieurs.
11. Conservation du sépia en combat.
12. Interfaces de combat et menus en couleurs normales.
13. Absence de brume ou de sépia résiduel ailleurs à Kanto.
14. Préservation de l'effet nocturne de Lavanville.
15. Absence de régression dans le suivi d'Ariane et l'enquête de Carmin-sur-Mer.

Tester également les déplacements spéciaux applicables.

Les tests doivent distinguer clairement les contrôles réellement exécutés des cas non couverts.

Mesurer la mémoire statique et documenter toute augmentation de consommation.

## 9. Captures et GIF obligatoires

Fournir des captures natives mGBA montrant :

- La mer avant la brume.
- L'entrée dans la brume.
- Le moment où la brume est la plus dense.
- La sortie de la brume.
- L'arrivée à Cramois'Île en sépia.
- Le retour vers Kanto avec ses couleurs normales.

Créer au minimum deux GIF :

**GIF 1 — Arrivée à Cramois'Île**

Navigation normale → brume → disparition de la brume → Cramois'Île sépia.

**GIF 2 — Départ de Cramois'Île**

Cramois'Île sépia → brume → retour aux couleurs normales.

Les GIF doivent provenir de véritables captures mGBA et non d'une simulation graphique.

Fournir les captures et rapports pour les deux versions lorsque pertinent.

## 10. Livrables et arrêt de phase

À la fin :

- Fournir les commits réalisés.
- Mettre à jour le dossier `docs/cramois-ile-passe/`.
- Ajouter un rapport spécifique `phase-b`.
- Fournir les captures et les deux GIF.
- Documenter les résultats de tests.
- Comparer les consommations mémoire avant/après.
- Signaler les limitations restantes.

**Ne pas fusionner sur `master`.**

**Ne pas démarrer la phase C.**

Arrêter le travail après la validation technique de la phase B et me présenter le résultat visuel pour approbation.

La priorité est de créer une frontière temporelle convaincante, tout en préservant la stabilité du jeu et le sépia déjà développé.