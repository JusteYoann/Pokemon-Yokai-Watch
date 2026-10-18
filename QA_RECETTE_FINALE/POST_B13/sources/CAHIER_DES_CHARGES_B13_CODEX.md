# Pokémon × Yo-kai Watch — Cahier des charges après playtest B13

**Destinataire :** Codex — dépôt `JusteYoann/Pokemon-Yokai-Watch`, branche de travail `dev/reconstruction-finalisation` (vérifier la branche active avant toute modification)  
**Date :** 18 octobre 2026  
**Nature :** retours d'une première session de test manuel sur mGBA sous Windows. Ce document décrit des observations et des souhaits, **pas des corrections déjà validées**.

> **Mandat principal : PRIORITÉ ABSOLUE À L'AMBIANCE SONORE ET AUX SPRITES.**
> Le jeu est jouable dans la bêta B13, mais les disparités de volume et de rendu visuel empêchent une expérience homogène. Traiter ces deux chantiers avant la finition narrative ou les ajouts secondaires. Corriger l'ensemble du système, pas seulement les espèces montrées en capture.

## 0. Règles incontournables et décisions définitives

1. **Taille ROM maximale : 33 554 432 octets (32 Mio).** Mesurer la taille exacte à chaque build. Garder une réserve si possible ; ne pas ajouter de système expérimental pour dépasser la limite.
2. **Multi Exp. permanent : À CONSERVER.** La demande de retour au partage d'expérience classique a été annulée après test du premier champion ; ne pas la réintroduire.
3. **Identité sonore : quasi exclusivement Yo-kai Watch**, y compris villes, routes, bâtiments, intro, combats et personnages. **Réutiliser volontairement** les mêmes pistes dans plusieurs zones et événements ; éviter la multiplication de morceaux coûteux.
4. **Continuité musicale :** l'OST d'une ville doit continuer sans coupure et sans redémarrage dans **tous ses bâtiments ordinaires**, y compris maisons, laboratoires (dont celui de Chen), boutiques et **Centres Pokémon / centres de soins**, et certaines routes voisines définies explicitement. Les lieux scénaristiques spéciaux restent des exceptions raisonnées.
5. **Ressources audio Yo-kai Watch privées** : ne pas committer des MP3 protégés, des ROM commerciales ou des ressources extraites non redistribuables dans le dépôt public. La compilation privée sous Windows/WSL utilise les fichiers locaux de l'utilisateur.
6. Préserver les 151 espèces, le scénario, les événements déjà validés, les sauvegardes et le fonctionnement mGBA. Ne pas lancer les quêtes supplémentaires reportées (Red, caméo Juste Yoann, Coach Antonic, etc.).
7. **Pas de faux positifs QA :** distinguer compilation réussie, inspection statique, rendu d'image, exécution mGBA et test manuel complet. Ne pas déclarer une couverture de 151 sprites testés visuellement sans en fournir la preuve.
8. Garder une copie de référence de B13 et des sauvegardes ; créer une nouvelle bêta distincte. Ne pas modifier les sauvegardes de test originales.

## 1. P0 — Refonte de l'ambiance sonore et des transitions

### 1.1 Problème principal observé : énormes écarts de volume

Au Mont Sélénite, la musique d'exploration Yo-kai Watch est calme/basse. L'arrivée d'un combat avec la musique Pokémon d'origine provoque un **saut de volume brutal, désagréable**. Même défaut à plusieurs transitions de zones. Les petits cris de créatures de la grotte et les sons d'interface (« tic » à chaque pression) paraissent trop forts relativement à la musique.

**Demandes :**
- Auditer le volume **perçu**, et non seulement le volume crête, de toutes les pistes d'exploration, de combat, événements, jingles et sons pertinents.
- Normaliser soigneusement les niveaux entre ressources Pokémon d'origine et OST importées. Ne pas compenser aveuglément en amplifiant les pistes douces jusqu'à saturation.
- **Baisser légèrement les bruitages d'interface répétitifs** : curseur, validation, annulation, sac, équipe, Médallium, PC. Ils doivent rester audibles, sans dominer.
- Rééquilibrer cris et bruitages ambiants (en particulier les petits cris à l'intérieur des grottes), ainsi que les sons des attaques/captures.
- Valider en jeu à volume mGBA constant : exploration → rencontre → combat → victoire → exploration ; ouverture/fermeture du menu ; entrées/sorties de bâtiments ; sauvegarde/rechargement.
- Documenter les paramètres modifiés, la méthode de mesure et les extraits de parcours testés. Ne pas prétendre à une mesure objective si seule une écoute subjective a été effectuée.

### 1.2 Direction artistique : remplacer presque toutes les musiques Pokémon

Objectif : **ne plus ressentir une bande-son de Pokémon Rouge Feu simplement ponctuée de quelques OST Yo-kai Watch**. Attribuer des thèmes Yo-kai Watch à l'introduction, à l'écran titre, aux villes, aux routes, aux grottes, aux bâtiments, aux combats sauvages, aux dresseurs, aux champions, aux événements et aux personnages.

**Réutiliser des pistes, pas besoin d'une piste exclusive par ville ou par grotte.** Une musique peut couvrir plusieurs grottes, un thème de combat peut servir pour tous les combats sauvages, un thème de dresseur pour tous les dresseurs ordinaires, etc. Préserver les thèmes spéciaux des grands affrontements.

**Attributions déjà décidées à conserver :**

| Piste | Utilisation |
|---|---|
| San Fantastico | Carmin-sur-Mer et sa zone musicale |
| Uptown Springdale | Céladopole et sa zone musicale |
| Hoppers Gorge | Mont Sélénite (ses salles) |
| Infinite Tunnel | Tour Pokémon de Lavanville |
| Mystic Grove | Caverne Azurée |
| Bicycle Theme | Vélo |
| Bada-Bing Tower | Sylphe SARL occupée par la Team Rocket |
| Somewhere A Bit Dodgy (BBQ) | Repaire Rocket de Céladopole |
| Vs Hinozall (English) | Combat Domniscian |
| Vs The Ghoulfather | Combat Don Morleone |
| Vs Zazelmare | Combat Lord Enma |
| Decisive Battle | Conseil 4 et rematches |
| Enma Track | Dialogue de Lord Enma |
| Final Battle – Are You Ready? | **Uniquement** combat final de Champion contre Matt, jamais ses affrontements précédents |
| Take Care, Grandpa 1 | Séquence de conclusion après victoire sur Matt |

Ce tableau reprend **15 thèmes sélectionnés**, pas une affirmation que les 15 sont déjà dans B13. Vérifier l'état réel des ressources et des événements.

**Nouvelle répartition à proposer :** Bourg Palette, Jadielle, Argenta, Azuria, Lavanville hors Tour, Safrania, Parmanie, Cramois'Île, Plateau Indigo, routes, grottes ordinaires, centres de soins, bâtiments spéciaux, musique sauvage, musique dresseur, musique champion, jingle de victoire, introduction, écran titre, thèmes récurrents de personnages. Présenter **avant arbitrage** un tableau cartographique « carte actuelle → piste actuelle → future piste → raison → statut des ressources ».

### 1.3 Règle exacte de continuité musicale

La demande n'est **pas** de changer de piste lorsque le joueur entre dans un bâtiment, puis de revenir à la ville ; c'est l'inverse : **aucun changement, aucune coupure ni redémarrage de la piste** à travers les zones liées.

- **Bourg Palette :** extérieur, maison du joueur, maison voisine, **laboratoire de Chen**, et **Route 1** si rattachée à la même zone sonore.
- **Carmin-sur-Mer :** extérieur, maisons, boutiques, **Centre Pokémon / centre de soins**, autres bâtiments ordinaires et **Route 11** : **San Fantastico en lecture continue**.
- **Céladopole :** extérieur, commerces, maisons, centre de soins et bâtiments ordinaires : **Uptown Springdale en lecture continue**.
- Étendre à d'autres villes et routes voisines selon une répartition explicite ; prévoir les frontières lorsque deux villes partagent une route.
- Les arènes, repaires, événements importants et donjons à forte identité peuvent être des exceptions **justifiées**, pas les centres de soins et laboratoires par défaut.
- Même musique de part et d'autre d'une porte = conserver sa position de lecture ; après combat, reprise correcte de l'ambiance de la carte courante. Vérifier aussi téléportation/vol, entrées multiples et restauration après chargement.

### 1.4 Effets sonores et cris : identité Yo-kai Watch

Étudier le remplacement des sons Pokémon résiduels en combat et environnement : apparitions, cris, sons d'attaques adaptés à leurs éléments, dégâts, K.O., Yo-kai Ball/capture, victoire, montée de niveau, évolution, sonneries particulières, et sons ambiants. **Les MP3 de musiques disponibles ne garantissent PAS la présence de bruitages.** Inventorier d'abord ; si ressources manquantes, indiquer précisément lesquelles et ne pas inventer un résultat ou insérer un son arbitraire. Respecter qualité GBA, stabilité audio et budget ROM. Les sons d'interface doivent être **plus discrets**, même si leur nature n'est pas remplacée.

### 1.5 Auditer et libérer l'espace avant ajout massif

B13 mesurée : **24 400 776 octets ≈ 23,27 Mio**, donc marge brute ≈ **8,73 Mio** jusqu'à 32 Mio ; cette marge n'est pas entièrement dédiée à l'audio. Audit obligatoire des musiques Pokémon devenues inutilisées, données musicales orphelines, doublons et éventuels sprites/icônes/palettes Pokémon encore compilés. **Ne compter que les économies mesurées sur le fichier ROM après reconstruction.** Un ancien sprite déjà remplacé ne libère pas deux fois de l'espace. Ne retirer aucune ressource encore référencée ; produire avant/après en octets, vérification de la table de ressources et tests de non-régression.

## 2. P0 — Harmonisation visuelle exhaustive des sprites

La B13 présente des problèmes **systémiques** de position, gabarit et cadrage. Contrôler **les 151 Yo-kai** avec leurs sprites de face, sprites de dos et icônes d'équipe ; traiter les sprites overworld des personnages et Yo-kai déjà intégrés. Une simple vérification que les PNG ont les bonnes dimensions est insuffisante.

### 2.1 Front sprites (combat adverse)

- Comparer les silhouettes dans le cadre de combat réel, pas uniquement des images isolées.
- Ajuster taille apparente, ancrage sur l'ovale adverse, centrage horizontal/vertical, marges transparentes, proportions selon le gabarit naturel et cohérence entre évolutions.
- Préserver contours, lisibilité pixel art, palette, orientation et sprites déjà satisfaisants ; **pas de redimensionnement aveugle ni de lissage**.

**Cas relevés :**
- **Cigalopin :** paraît trop massif pour une petite espèce de début d'aventure ; réduction légère à étudier.
- **Baku :** apparaît trop petit et mal centré.
- **Pitou :** paraît disproportionnellement grand pour son gabarit.

### 2.2 Back sprites (combat allié)

- Cadrage cohérent avec la présentation de Rouge Feu : les bipèdes/humanoïdes devraient souvent être visibles principalement à partir du bassin/de la taille lorsque c'est approprié ; **éviter pieds/corps entiers inutilement visibles** et l'effet « sprite collé à la plateforme ».
- Adapter à chaque morphologie (quadrupèdes, volants, formes atypiques) ; **ne jamais appliquer une translation ou un zoom identique aux 151**.
- Inspecter centrage visuel réel (queues, accessoires, flammes), hauteur, échelle et niveau de détail.

**Cas relevés :**
- **Komasan :** pieds/bas du corps trop visibles ; cadrage de dos à revoir.
- **Cigalopin :** back sprite mal cadré, revoir hauteur et portion visible.
- **Nihilistik :** back sprite semblant trop haut ; position à revoir selon capture.
- **Komaous :** dessin reconnaissable mais corps presque entier visible et silhouette déséquilibrée par queue/flammes ; comparer visuellement à Komasan et Komastar.

**Attention aux retours contradictoires de position :** selon l'espèce, le problème peut être trop haut, trop bas, trop petit ou mal centré. Le critère est le résultat observé en combat, pas un décalage global.

### 2.3 Icônes de menu / équipe

Sur la capture d'équipe, les icônes de plusieurs Yo-kai remplissent les cases de façon très inégale. Harmoniser la taille apparente, le centre de masse graphique, l'identification de chaque espèce et la cohérence entre icônes. Vérifier équipe, PC et autres menus. Les petites et grandes espèces peuvent conserver une différence voulue ; éviter simplement les incohérences involontaires.

### 2.4 Overworld et personnages sur les cartes

Uniformiser tous les nouveaux sprites de cartes déjà présents avec les conventions graphiques de Rouge Feu : proportions tête/corps, taille d'une case, épaisseur des contours, ombrage, mouvement de marche, silhouette et interaction avec le décor.

**Personnages à vérifier si effectivement intégrés :** Nathan, Katie, Matt, Ariane, Lord Enma, Domniscian/employés, Don Morleone/Mafiamille, Nathaniel/Michael, Wyatt et autres NPC personnalisés existants. Les caméos et quêtes reportés ne doivent pas être créés par ce chantier.

**Corrections nominatives :**
- **Léo transformé en Jibanyan :** sprite overworld clairement trop grand dans le bâtiment, réduire au gabarit crédible des NPC et de l'intérieur sans perdre son identité.
- **Usapyon près d'Ariane :** semble un peu grand, contrôler sa proportion avec Ariane et le joueur.
- **Misterre (apparition remplaçant Ronflex) :** silhouette générale et intégration appréciées. **Retirer uniquement les éléments verts assimilés à des yeux et les remplacer par du marron/bois ; supprimer également la bouche.** Ne pas refaire le sprite entier ni rajouter une expression faciale.

### 2.5 Preuve de la vérification globale

Produire des planches de comparaison exploitables pour les 151 espèces (front, back, icône), un registre « espèce / défaut / intervention / état / capture de contrôle ». Comparer à de vrais rendus mGBA de tailles fixes. Si la totalité des 151 n'a pas été inspectée visuellement, indiquer celles qui restent. Après chaque série de corrections, vérifier la ROM en jeu, pas seulement le PNG.

## 3. P1 — Traduction française complète et terminologie

Durant le test, subsistent de l'anglais dans les menus et les textes de combats, ainsi que **les descriptions des attaques** et le Médallium.

- Traduire absolument tous les éléments visibles par le joueur : dialogues, introductions, menus, combat, efficacités, statuts, apprentissage, évolutions, PC, objets, lieux, CT/CS, Médallium, fin/postgame, écrans d'aide.
- **Noms ET descriptions d'attaques** intégralement en français, selon leurs effets réels, avec un texte qui tient à l'écran.
- Utiliser dans l'interface **Yo-kai, Médallium, Yo-kai Ball, Ligue Yo-kai**, sans rebaptiser imprudemment les constantes et symboles internes du moteur.
- Vérifier typographie, accents, largeur GBA, troncatures, chaînes partagées et cohérence partout.
- **Usapyon** : une scène avec Ariane utilise « Usapion » ; uniformiser **Usapyon** et confirmer que l'événement de Pierre Lune reste fonctionnel.

## 4. P1 — Médallium : classification par habitat et traduction

Le Médallium possède un index « habitats » dérivé de FireRed, encore partiellement en anglais (*Grassland Yo-kai, Forest Yo-kai, Water's-edge Yo-kai, Sea Yo-kai, Cave Yo-kai, Mountain Yo-kai, Rough-terrain Yo-kai, Urban Yo-kai, Rare Yo-kai* ; contrôles *PICK/CANCEL*, etc.). La répartition semble suivre les anciens Pokémon plutôt que la nature des 151 Yo-kai.

**Demande :** revoir chaque espèce d'après son habitat/écologie dans l'univers Yo-kai Watch et sa place dans **ce** jeu, non selon l'espèce Pokémon remplacée :
- **Kappa** et autres créatures d'eau douce → eaux douces/rivières/étangs.
- **Poissons marins** → mer/océan.
- Forêts, prairies, grottes, montagnes, terrains arides, milieux urbains selon cohérence.
- **« Yo-kai rares » : véritables exceptions**, et non toute créature puissante, très évoluée ou de rang élevé. La capture montrant Savantard et Loupépin dans cette section justifie de revoir les critères ; ne pas supposer que l'un ou l'autre doit y rester sans validation.
- Respecter le nombre de rubriques et les contraintes du moteur (ou documenter tout changement requis), maintenir numéros du Médallium, progression et capture.
- Traduire catégories et contrôles en français. Exemples de libellés courts : Prairies, Forêts, Rivières, Mer, Grottes, Montagnes, Terrains arides, Villes, Rares — à adapter au nombre de caractères disponible.
- **Fournir un tableau des 151 affectations actuelles / proposées avant tout arbitrage discutable**, avec signalement des incertitudes.

## 5. P1 — Gameplay : premier champion

La progression initiale donne surtout accès à des espèces **Insecte** et le combat contre **Pierre** paraît trop difficile ou mal adapté à cette diversité limitée. **Conserver le Multi Exp. permanent.**

**Modification envisagée : remplacer Passpa par Nanpart dans l'équipe de Pierre.** Vérifier avant d'agir quelle espèce occupe réellement ce slot, les types, statistiques, capacités, niveaux, la relation évolutionnelle réelle de ces espèces dans le projet, et les solutions disponibles avant Argenta. Le but est un premier champion exigeant mais faisable sans entraînement abusif, pas un combat trivial. Éviter les modifications générales de toutes les rencontres si un changement ciblé suffit. Documenter la décision.

## 6. P2 — Intro, écran titre et écran d'aide

**Cette finition est souhaitée, mais après les urgences audio/visuelles.**

- **Écran titre :** remplacer le logo Pokémon FireRed et Dracaufeu par une identité visuelle Pokémon × Yo-kai Watch, avec une composition adaptée aux contraintes GBA. Personnages emblématiques possibles, mais ne pas révéler Kyubi, Octorgone, Enma ou surprises de fin.
- **Intro :** brève cinématique originale à l'atmosphère mystérieuse (nuit, silhouettes ou yeux lumineux discrets, présence invisible des Yo-kai, révélation de la Yo-kai Watch), sans copier dialogues de films existants ni dévoiler les boss. Priorité à un résultat court et stable, plutôt qu'à un programme graphique complexe.
- **Écran initial d'aide/instructions :** remplacer Pikachu par Jibanyan ; traduire le texte visible.
- Prévoir une musique Yo-kai Watch cohérente pour intro et écran titre dans le budget sonore global.

## 7. Ordre d'exécution et critères d'acceptation

### Phase 1 — Audit et baseline

- Identifier branche, commit, état de B13, génération locale des OST, taille ROM exacte et méthode de reconstruction Windows/WSL.
- Vérifier et archiver état des 15 OST envisagées : déjà intégrées / à intégrer / absentes localement.
- Cartographier thèmes actuels et ressources compilées, y compris musiques et sprites Pokémon encore présents.
- Préparer les planches de sprites et une liste de défauts traçable.
- Conserver B13 et sauvegardes pour comparaison.

### Phase 2 — P0 audio

- Corriger immédiatement les **différences de volume** et les bruitages « tic » trop forts.
- Définir puis intégrer les zones sonores continues et la réutilisation des thèmes Yo-kai Watch, sans dépasser la limite ROM.
- Remplacer progressivement combats et ambiance par les musiques Yo-kai Watch disponibles.
- Inventorier/adapter cris et SFX quand les ressources le permettent.
- Tester notamment **Mont Sélénite → combat → retour**, **Carmin → centre de soins → Route 11**, **Bourg Palette → labo de Chen → Route 1**.

### Phase 3 — P0 sprites

- Corriger les exemples constatés et conduire un audit **global 151 espèces**.
- Ajuster front/back et icônes, puis overworld.
- Tester Baku, Pitou, Cigalopin, Komasan, Komaous, Nihilistik, Jibanyan, Usapyon et Misterre en jeu.

### Phase 4 — P1 / P2

- Traductions complètes (descriptions d'attaques et Médallium incluses).
- Nouveau classement habitat, sous réserve de validation des cas discutables.
- Contrôle Pierre/Passpa/Nanpart, **sans retirer Multi Exp.**
- Intro, écran titre, écran d'aide après stabilisation prioritaire.

### Phase 5 — Non-régression et livraison

Exécuter autant que possible : lancement, nouvelle partie, sauvegarde/chargement, menus, icônes, combats sauvages/dresseurs/champions, captures, évolutions, CT/CS, Médallium, musiques/transitions, portes/vol, scénario Ariane/Usapyon, Léo/Jibanyan, Misterre, événements spéciaux, Conseil 4, Matt, crédits. Documenter quels tests sont automatisés, lesquels ont vraiment été joués et lesquels restent à faire par l'utilisateur.

**Conditions indispensables avant livraison :**
- ROM compilée **≤ 33 554 432 octets**, valeur affichée en octets et sha256.
- Pas de pics sonores importants entre exploration, combat et bruitages de menu, vérifiés en mGBA.
- Continuité musicale dans les bâtiments ordinaires, **y compris centres de soins et laboratoire Chen** ; routes sélectionnées sans redémarrage intempestif.
- Preuves d'une passe de vérification globale des sprites, avec liste des espèces/ressources révisées et des exceptions restantes.
- Traduction contrôlée, notamment descriptions d'attaques et Médallium.
- Multi Exp. permanent conservé.
- Aucun fichier sonore protégé ni ROM propriétaire ajoutés à GitHub public.
- Instructions reproductibles pour créer **une nouvelle Bêta privée** sur le Windows de l'utilisateur, et bilan honnête des tâches non terminées.

## 8. Livrables à remettre par Codex

1. **Rapport d'audit initial** : commit, ROM B13, ressources et budget audio/mémoire.
2. **Tableau des musiques** : toutes cartes et événements pertinents, musique avant/après, continuité, exceptions et provenance locale.
3. **Rapport de normalisation sonore** : gains et niveaux de SFX, méthode et transitions réellement testées.
4. **Planche et registre QA sprites** pour 151 espèces (front/back/icône) et overworld personnalisés ; changements individualisés.
5. **Inventaire de traduction** et contrôles de débordements.
6. **Tableau des 151 catégories d'habitats**, à valider pour les cas ambigus.
7. **Décision argumentée sur Pierre et Passpa/Nanpart**, sans retirer Multi Exp.
8. **Mesure ROM avant/après** en octets + SHA-256, ressources retirées, tests de stabilité.
9. **Nouvelle bêta privée ou procédure exacte pour la recompiler**, sans publier les ressources audio propriétaires.
10. **Liste résiduelle honnête** des corrections impossibles ou non terminées, sans les déclarer achevées.

**Instruction finale :** Commence par l'audit et la priorisation. Tu peux corriger et tester de façon autonome les sujets qui ne nécessitent pas de choix créatif. Pour les attributions musicales nouvelles ou les catégorisations réellement discutables, propose un tableau à validation plutôt que d'inventer une décision. Avance par lots vérifiables ; **priorise l'audio et le repositionnement/harmonisation des sprites avant toute finition secondaire**.
