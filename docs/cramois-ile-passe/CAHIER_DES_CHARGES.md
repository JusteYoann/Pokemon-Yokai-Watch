# CODEX — Cramois'Île : 60 ans dans le passé

## 1. Objectif général

Transformer intégralement Cramois'Île, dans notre ROM hack Pokémon Rouge Feu × Yo-kai Watch, en une zone temporelle située **60 ans dans le passé**.

L'objectif est de créer une expérience cohérente, visuellement marquante et jouable, inspirée de l'ambiance de **Vieux Granval dans Yo-kai Watch 2**.

Cramois'Île ne doit plus ressembler à une ville ordinaire de Kanto : en traversant une épaisse brume maritime, le joueur pénètre dans une époque révolue.

Cette anomalie reste permanente, y compris après la victoire contre le Champion, la Ligue et durant le postgame.

**Important : il s'agit d'une véritable transformation de l'île entière, pas simplement d'un filtre appliqué à la carte extérieure.**

## 2. Git et préservation

Dépôt : `JusteYoann/Pokemon-Yokai-Watch`

1. Examiner l'état actuel du dépôt et identifier la branche contenant les fonctionnalités les plus récentes et validées.
2. Préserver impérativement l'enquête de la Pierre Philosovni, le suivi d'Ariane, le combat duo, la remise de Coupe et toutes les fonctionnalités précédemment validées.
3. Créer une branche dédiée, par exemple `feature/cramois-ile-passe`.
4. Ne jamais fusionner dans `master` sans autorisation.
5. Ne supprimer ni remplacer aucun des 151 Yo-kai existants.
6. Ne pas modifier les autres Arènes, les équipes validées, la Mafiamille, Lavanville, la Ligue, Don Spiraton, les musiques privées ou les fonctionnalités du postgame.

Faire un audit des ressources graphiques, des palettes, des scripts et de la mémoire avant toute modification.

Le précédent rapport du suivi d'Ariane indique une marge EWRAM très faible : **796 octets libres**. Ne pas présumer que cette marge est encore identique. La mesurer à nouveau et éviter toute allocation permanente inutile.

## 3. L'anomalie temporelle

Toute Cramois'Île existe 60 ans dans le passé.

Les habitants vivent normalement à leur époque et ignorent qu'une anomalie temporelle affecte leur île.

Le joueur peut librement entrer et sortir de cette zone.

### Frontière maritime

À l'approche de Cramois'Île depuis n'importe quelle route maritime accessible :

- Une brume blanche ou gris clair, très épaisse, apparaît progressivement.
- La visibilité diminue pour représenter le franchissement d'une frontière temporelle.
- Le joueur traverse cette brume avant de découvrir l'île aux couleurs du passé.
- À la sortie, la transition inverse ramène le joueur dans le Kanto actuel.

La brume doit fonctionner dans les deux sens et ne pas bloquer Surf, les collisions ou la progression.

**Aucune brume ne doit être présente à l'intérieur de Cramois'Île.**

Ne pas réutiliser la brume verte permanente de Lavanville. Les deux effets doivent être indépendants.

La transition doit également rester cohérente lors d'un retour sur l'île, après une sauvegarde et lors des déplacements spéciaux autorisés par le jeu.

## 4. Direction artistique : sépia intégral

Appliquer à Cramois'Île une palette **brun doré nostalgique**, proche de Vieux Granval.

Ce traitement est permanent et concerne :

- La carte extérieure et tous ses éléments.
- Les bâtiments, routes, végétation, eau et animations.
- Le Centre Pokémon et la Boutique.
- Les maisons et tous les intérieurs.
- Le Manoir Pokémon.
- L'Arène.
- Le laboratoire des fossiles.
- Les PNJ et leurs sprites overworld.
- Les arrière-plans des combats sauvages.
- Les arrière-plans des combats contre les Dresseurs.
- Les sprites des Yo-kai en combat.
- Les sprites des Dresseurs et du Champion.

### Palette recherchée

- Végétation vert olive désaturé.
- Eau gris-beige.
- Bâtiments ocre, beige et brun chaud.
- Ombres brunes légèrement plus profondes.
- Luminosité douce, sans obscurcir les lieux.
- Contrastes suffisants pour conserver le pixel art et les détails.

**Ne pas appliquer un simple voile brun opaque sur tout l'écran.**

Privilégier une transformation maîtrisée des palettes pour préserver le rendu original des graphismes GBA.

### Exceptions

Conserver les couleurs et la lisibilité des éléments d'interface :

- Menus.
- Textes et fenêtres de dialogue.
- Jauges de PV.
- Informations de combat.
- Indicateurs de statut.
- Écrans de sauvegarde et autres interfaces fonctionnelles.

Le traitement sépia doit dépendre du lieu où se déroule le combat, et non de l'identité du Yo-kai.

Exemple : Hovernyan est teinté sépia lorsqu'il combat à Cramois'Île, mais conserve ses couleurs normales lorsqu'il combat ailleurs dans Kanto.

Aucun effet sépia ne doit déborder sur les autres villes ou sur leurs combats.

## 5. Manoir Pokémon et progression

Conserver le fonctionnement essentiel du jeu original :

1. Le joueur arrive à Cramois'Île.
2. Il découvre que l'Arène est fermée.
3. Il explore le Manoir Pokémon.
4. Il récupère la Clé Secrète.
5. Il utilise cette clé pour accéder à l'Arène.

Préserver les objets, les rencontres sauvages, les événements et les interactions nécessaires à la progression.

Adapter visuellement le Manoir à l'ambiance du passé, sans supprimer son exploration.

Le laboratoire des fossiles doit rester pleinement fonctionnel, avec ses interactions et la résurrection des fossiles.

## 6. Champion : Nathaniel ou Michael

Le Champion de Cramois'Île dépend du sexe du personnage joueur :

- Joueur garçon : **Nathaniel**.
- Joueuse fille : **Michael**.

Ce personnage est le grand-père du protagoniste, rencontré **60 ans avant l'époque actuelle**.

Le joueur le reconnaît immédiatement.

### Scène de rencontre

Prévoir un échange marquant, mêlant surprise et humour.

Le protagoniste peut exceptionnellement prononcer une courte réplique, par exemple :

« …Grand-père ?! »

Nathaniel ou Michael est surpris, puis éclate de rire en entendant l'histoire du joueur.

Il refuse catégoriquement de croire qu'il s'agit de son petit-enfant venu du futur.

Il considère cette affirmation comme une plaisanterie absurde.

**Règle narrative absolue : le grand-père ne croit jamais le joueur.**

Il ne doit pas soudainement reconnaître le protagoniste, avoir une révélation sentimentale ou accepter l'existence du voyage temporel.

Son comportement reste amusé, moqueur et sûr de lui.

Au cours du dialogue, il évoque naturellement l'année de son époque, permettant au joueur de comprendre qu'il a remonté le temps de 60 ans.

### Équipe du Champion

Conserver exactement cette équipe déjà validée :

1. Métaurolog — niveau 40.
2. Sirénité — niveau 41.
3. Sal de bain — niveau 41.
4. Brumella — niveau 42.
5. Faux Kappa — niveau 43.
6. Hovernyan — niveau 45, Yo-kai signature.

Ne pas changer les niveaux, les espèces ou le fonctionnement du combat sans accord.

Conserver la remise du Badge Volcan et les récompenses nécessaires à la progression.

### Dialogue après victoire

Prévoir notamment cette réplique :

« Et si tu croises mon moi du futur, dis-lui qu'il a intérêt à être devenu un sacré Champion ! »

Le grand-père doit toujours penser que le joueur plaisante.

## 7. Quiz de l'Arène

Conserver le mini-jeu de l'Arène de Cramois'Île dans Pokémon Rouge Feu.

Chaque salle présente une question à réponse **OUI / NON**.

- Une bonne réponse permet d'ouvrir la porte sans combattre.
- Une mauvaise réponse entraîne le combat contre le Dresseur concerné.
- Le joueur peut toujours choisir de combattre directement.
- Ne pas modifier inutilement l'architecture et le fonctionnement des portes.

Remplacer les questions Pokémon d'origine par les six questions suivantes, dans cet ordre exact.

| Salle | Question | Bonne réponse |
|---|---|---|
| 1 | Jibanyan possède-t-il seulement deux fusions différentes ? | NON |
| 2 | Whisper est-il resté enfermé pendant plus de 200 ans ? | OUI |
| 3 | Steve Jaws est-il le créateur de la Yo-kai Watch moderne ? | OUI |
| 4 | Le Bingo-kai est-il indispensable pour compléter le Médallium ? | OUI |
| 5 | Hovernyan s'est-il déjà fait appeler Méga-nyan ? | OUI |
| 6 | L'équipe des Blasters de Coach Antonic apparaît-elle dans plus de trois jeux différents ? | OUI |

**Respecter exactement ces formulations et ces réponses.**

Ne pas ajouter « Dans Yo-kai Watch 1 », « Dans Yo-kai Watch 2 » ou d'autres références aux titres des jeux.

Les questions doivent exister naturellement dans l'univers du ROM hack.

Vérifier la prise en charge des accents, des apostrophes, des sauts de ligne et de la longueur des questions dans les fenêtres GBA.

## 8. Cohérence scénaristique

La cause exacte de l'anomalie temporelle ne doit pas être expliquée.

Il est possible que le joueur fasse un rapprochement avec les phénomènes mystérieux survenus ailleurs à Kanto, mais **ne pas confirmer que la Pierre Philosovni est responsable**.

Le grand-père, qui vit 60 ans dans le passé, ne connaît pas les événements récents liés à l'OVNI et à la Mafiamille.

Ne pas ajouter de révélation sur l'origine de l'OVNI ou sur les occupants du vaisseau.

Préserver le mystère.

## 9. Plan d'implémentation obligatoire

Procéder par étapes clairement séparées.

### Phase A — Prototype visuel

Créer d'abord un prototype fonctionnel du sépia sur :

- L'extérieur de Cramois'Île.
- Au moins un intérieur.
- Le Manoir Pokémon.
- Le laboratoire des fossiles.
- L'Arène.
- Un combat sauvage.
- Un combat contre un Dresseur.

Fournir des captures natives mGBA et, si possible, une courte démonstration animée.

**Ne pas considérer la direction artistique comme définitivement approuvée avant validation visuelle.**

Si une limitation du moteur empêche de teinter correctement certains éléments sans altérer l'interface, la documenter et proposer une solution plutôt que d'introduire une régression.

### Phase B — Frontière temporelle

Implémenter et tester la brume maritime, les transitions aller-retour et la restauration correcte des palettes.

### Phase C — Scénario et Arène

Implémenter les dialogues, la rencontre avec Nathaniel/Michael, les six questions et le fonctionnement complet de l'Arène.

### Phase D — Validation complète

Tester dans mGBA les deux versions de la ROM :

- Entrée dans Cramois'Île depuis les différentes routes possibles.
- Sortie et retour dans le Kanto actuel.
- Sauvegarde et chargement à l'intérieur de l'île.
- Entrée et sortie de chaque bâtiment.
- Fonctionnement du Manoir et de la Clé Secrète.
- Laboratoire des fossiles.
- Combats sauvages et combats de Dresseurs.
- Affichage des menus et des jauges de PV.
- Six bonnes réponses au quiz.
- Six mauvaises réponses et combats correspondants.
- Variante Nathaniel pour le joueur garçon.
- Variante Michael pour la joueuse.
- Combat complet contre le Champion.
- Obtention du Badge Volcan.
- Retour sur l'île après la Ligue.
- Absence d'effets visuels résiduels dans le reste de Kanto.
- Préservation des fonctionnalités de Carmin-sur-Mer et de Lavanville.

Ne pas présenter un test simulé comme une validation réelle en jeu.

## 10. Livrables

Fournir :

1. La branche et les commits réalisés.
2. Un récapitulatif précis des modifications.
3. Des captures mGBA avant/après du rendu sépia.
4. Un GIF montrant les transitions temporelles, si réalisable.
5. Des captures des intérieurs et des combats.
6. Un rapport de tests pour les deux versions.
7. Les mesures de mémoire avant/après.
8. Une liste explicite des limitations et des éléments non vérifiés.

**Ne pas fusionner sur master.**

**Priorité absolue : préserver le projet existant et obtenir un rendu réellement jouable, stable et fidèle à l'ambiance nostalgique de Vieux Granval.**