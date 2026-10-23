# Phase C — Nathaniel/Michael et Arène de Cramois

Phase B approuvée visuellement. Phase C intégrée sur `feature/cramois-ile-passe`, proposée pour revue visuelle et scénaristique. Aucun merge sur master. La phase D exhaustive n'est pas commencée.

Base : `a8c97b3ca`. Audit : `b916838d7`. Intégration : `3d3685a8d`. Ajustement des indices d'animation natifs : `f2bcea8cc`.

## Résultat à examiner

- [Rencontre avec Nathaniel — extrait court](public/rencontre-nathaniel-courte.gif) · [défi complet](public/rencontre-nathaniel-et-defi.gif).
- [Rencontre avec Michael — extrait court](public/rencontre-michael-courte.gif) · [défi complet](public/rencontre-michael-et-defi.gif).
- [Victoire et don d'Hovernyan — extrait court](public/victoire-et-don-court.gif) · [revanche complète](public/revanche-et-don-hovernyan.gif).
- [Quiz : première bonne réponse](public/quiz-1-bonne-reponse.gif), [erreur et combat](public/quiz-1-erreur-combat.gif), [sixième question](public/question-6-x4.png).
- [Nathaniel et Hovernyan](public/nathaniel-hovernyan-x4.png), [Michael et Hovernyan](public/michael-hovernyan-x4.png), [dos et cape couvrante dans le moteur](public/compagnon-dos-cape-x4.png).
- [Don dans l'équipe](public/hovernyan-recu-x4.png), [boîtes pleines](public/boites-pleines-x4.png), [envoi au PC après libération d'une place](public/hovernyan-envoye-pc-x4.png).
- [Planche transparente face/dos, taille native](../../../graphics/yokai_characters/hovernyan/overworld.png) ; [agrandissement](../../../graphics/yokai_characters/hovernyan/apercu-x8.png).

Les mêmes captures/rapports sont disponibles dans [prive](prive). Les PNG natifs sont en 240 × 160, les agrandissements au plus proche voisin. Les GIF contiennent de véritables images de mGBA, échantillonnées et agrandies sans simulation du jeu ; l'échantillonnage et la lecture peuvent modifier leur cadence par rapport au temps réel. Les combats longs peuvent être échantillonnés davantage pour limiter leur poids.

## Rencontre et compagnon

Conformément à la correction du créateur, aucune date, aucun écart de soixante ans, aucune explication ni mention de voyage temporel ne sont prononcés. Le protagoniste, choqué, lâche « …Grand-père ?! ». Le Champion rit, pense à une confusion et présente Hovernyan. Il ne reconnaît pas le protagoniste comme son descendant. La réplique initialement envisagée sur le « moi du futur » est écartée selon cette consigne plus récente.

La scène est jouée une fois, avant le premier défi. Les introductions et dialogues déjà validés du Champion, l'équipe Métaurolog 40 / Sirénité 41 / Sal de bain 41 / Brumella 42 / Faux Kappa 43 / Hovernyan 45, le Badge Volcan, la CT38, le point de soin et la suite native avec Léo restent conservés. Le sexe du joueur résout Nathaniel ou Michael comme auparavant, y compris lors du rechargement des objets sauvegardés.

Hovernyan occupe la case immédiatement à droite du Champion. Aucun Champion ne se déplace dans ces scènes : aucun gestionnaire de suivi n'est ajouté. Le compagnon reste présent avant/après combat, sauvegarde, menu plein écran et don postgame. Les anciens événements de Parmanie ne sont pas modifiés.

Le nouvel overworld est une adaptation de la référence face/dos fournie dans le chat. Le créateur a demandé que la cape retombe sur tout le dos : cette correction est intégrée. Dessin adapté avec imagegen puis converti au format GBA : deux vues de 24 × 26 pixels utiles dans des cellules 32 × 32, quinze couleurs RGB555 et une transparence. Les entrées d'animation natives réutilisent ces deux vues fixes ; aucun nouveau cycle de marche, aucun profil inventé. Aucune ressource validée préexistante ni sprite de combat d'Hovernyan n'est modifié. Le sépia approuvé teinte normalement le compagnon sur l'île.

## Quiz

Les formulations et réponses proviennent du cahier des charges initial ; aucune nouvelle question définitive n'est inventée. Seuls les retours à la ligne/au défilement sont adaptés à la fenêtre GBA.

| Salle | Question | Réponse |
|---|---|---|
|1|Jibanyan possède-t-il seulement deux fusions différentes ?|NON|
|2|Whisper est-il resté enfermé pendant plus de 200 ans ?|OUI|
|3|Steve Jaws est-il le créateur de la Yo-kai Watch moderne ?|OUI|
|4|Le Bingo-kai est-il indispensable pour compléter le Médallium ?|OUI|
|5|Hovernyan s'est-il déjà fait appeler Méga-nyan ?|OUI|
|6|L'équipe des Blasters de Coach Antonic apparaît-elle dans plus de trois jeux différents ?|OUI|

Les portes, les collisions, les déplacements des Dresseurs, les combats et leurs routines de victoire sont ceux d'origine. Une réponse correcte ouvre sans combat ; une erreur lance le combat natif et la victoire ouvre le passage. Un défi direct conserve la même issue. Les portes restent ouvertes après Save/Continue.

## Revanche et don

Le joueur doit avoir remporté le premier défi de l'Arène, reçu la CT38 et terminé la Ligue (`FLAG_SYS_GAME_CLEAR`). Un échange OUI/NON propose un second combat contre la même équipe validée, avec le bon nom et portrait selon le sexe du joueur. Aucune équipe postgame nouvelle n'est inventée. Une défaite ou un refus ne débloque rien.

Après victoire, un drapeau propre mémorise le droit à la récompense. `givemon` remet Hovernyan niveau 45 dans l'équipe, ou l'envoie au PC si nécessaire. Si l'équipe et les 420 emplacements de PC sont pleins, le don reste en attente, même après Save/Continue ; il suffit de libérer une place et de reparler au Champion sans refaire le combat. Un second drapeau est posé uniquement après réussite du transfert et bloque tout doublon. L'overworld du compagnon ne dépend jamais de ces drapeaux : les apparitions du passé ne disparaissent pas rétroactivement.

Les trois drapeaux utilisent des bits persistants déjà disponibles : rencontre `0x32C`, revanche gagnée `0x32D`, don effectué `0x32E`. Ils sont indépendants des drapeaux et récompenses de l'apparition secondaire de Parmanie. Le format de sauvegarde est inchangé.

## Validation et mémoire

[Résumé final](VALIDATION.json) · [Tests publics](public/TEST_MGBA.json) · [Tests privés](prive/TEST_MGBA.json) · [Vérifications visuelles/interactions](public/VISUELS_MGBA.json) · [Préservation](PRESERVATION.json) · [Compilation publique](COMPILATION-public.txt) · [Compilation privée](COMPILATION-prive.txt) · [Liste exacte des fichiers](LISTE_FICHIERS.txt).

**136 contrôles passent dans chaque version** : 37 de phase C, 10 contrôles visuels/interactions, 40 de phase A, 35 de phase B et 14 d’Ariane. Les contrôles natifs couvrent les deux variantes, les vrais combats gagnés et une revanche réellement perdue, l'absence de don avant la Ligue/avant une deuxième victoire, les six bonnes réponses et six mauvaises réponses, les six défis directs, les portes, les sauvegardes, les deux destinations de don, les boîtes pleines et les tentatives répétées. Les vues de face/dos, collisions, interaction d'Hovernyan, retour du Sac et six questions affichées sont capturées séparément. Les lignes de l'Arène ont été mesurées avec la police native dans les deux variantes : 286 lignes, maximum 197 pixels pour une limite de 208.

Les suites approuvées de [phase A](regressions/phase-a), [phase B](regressions/phase-b) et [suivi d'Ariane](regressions/ariane) sont rejouées sur les nouvelles ROM dans un dossier distinct. Les rapports historiques ne sont pas écrasés.

| Mémoire statique | Avant C | Après C | Écart |
|---|---:|---:|---:|
|EWRAM, publique et privée|261368 octets|261368 octets|0|
|Marge EWRAM|776 octets|776 octets|0|
|IWRAM publique|29824 octets|29824 octets|0|
|IWRAM privée|29888 octets|29888 octets|0|

Hovernyan utilise un emplacement d'objet et un sprite natifs déjà préalloués, 512 octets de tuiles OBJ pendant son affichage et une banque de palette réservée (8), distincte de celle du Champion. Les deux vues occupent 1024 octets de graphismes 4bpp en ROM. Le don réutilise l'allocation temporaire native d'un Pokémon et ses commandes de stockage. Aucun nouveau traitement par image ni allocation EWRAM statique.

Le contrôle de préservation compare les 5821 PNG/palettes préexistants, les cartes/layouts, toutes les équipes, les données des 151 Yo-kai, les sauvegardes, les scripts de Carmin, Lavanville, la Mafiamille et la finale. Les routines des phases A/B sont inchangées. Seuls trois fichiers de la carte de l'Arène évoluent ; la géométrie, les warps et les neuf acteurs précédents sont conservés. Les 31 flux audio privés sont vérifiés à leur emplacement réel dans la ROM. Aucun audio ni ROM privée n'est publié.

## Limites explicites

Les tests partent de nouvelles parties natives mais utilisent des fixtures annoncées : positionnement sur carte, équipe du joueur renforcée et drapeau de Ligue pour le postgame. Les réponses et combats sont exécutés dans le moteur avec les touches ; les PV adverses et les issues ne sont pas forcés. Le cas d'échec utilise réellement un Yo-kai niveau 1 avec Trempette. Les boîtes pleines sont une fixture de remplissage, puis une place est libérée avant d'exécuter à nouveau le véritable script de don. Les pointeurs de stockage sont relus après chargement natif, car le moteur les déplace.

Les défis directs et certains retours au Champion sont lancés par la commande native de contexte de script, avec le bon objet sélectionné ; ils ne constituent pas une preuve d'un parcours intégral de l'Arène à pied. Les choix du quiz et les premières rencontres utilisent les véritables interactions sur carte. Les changements d'orientation d'Hovernyan dans les captures face/dos sont une fixture utilisant les actions natives : la scène proposée reste stationnaire. Les sauvegardes sont testées aux états stables ; le contrôle natif verrouille le joueur pendant les dialogues et combats.

La Ligue complète, la résurrection des fossiles, le Manoir jusqu'à la Clé et toute la progression annexe ne sont pas rejoués dans cette phase ; leurs sources sont préservées. Les limites déjà documentées des suites A/B restent applicables. Aucune validation sur GBA physique ni certification d'écoute audio supplémentaire. Les deux vues du compagnon sont disponibles ; une future scène comportant de vrais déplacements ou profils devra être traitée explicitement.

**Arrêt pour validation visuelle et scénaristique de phase C. Aucun merge sur master, aucune phase D exhaustive engagée.**

[Audit](AUDIT.md) · [Demande](DEMANDE.md) · [Plan global](../PLAN.md).
