# Plan de transmission et d'intégration à Codex — ne pas casser l'existant

## Objectif

Adapter le dépôt `JusteYoann/Pokemon-Yokai-Watch` (`dev/reconstruction-finalisation`) à la nouvelle campagne narrative. **Ne pas repartir de zéro** et ne pas faire passer pour terminée une fonctionnalité qui n'a été documentée qu'en conversation.

## Règles globales pour Codex

1. **Lire avant de modifier :** `README.md`, `DEVELOPPEMENT_YOKAI.md`, `RECUPERATION_PROJET/README.md`, `docs/yokai-characters/README.md`, `QA_RECETTE_FINALE/CADRAGE_COMBATS_151/README.md`, `QA_RECETTE_FINALE/POST_B13/README.md` et les rapports de musique les plus récents.
2. **Préserver les 151 espèces** et leur correspondance actuelle avec les constantes `SPECIES_*`; le 001–151 est un registre fixe. Vérifier `RECUPERATION_PROJET/sources_validees/01_POKEDEX_151.csv` et `02_STATS_TYPES_TALENTS.csv`.
3. **Ne pas écraser en bloc** les PNG, palettes, sprites shiny, animations et ressources des protagonistes déjà approuvées. La politique de cadrage inclut des orientations voulues par le créateur.
4. **Respecter la carte blanche level design** : proposer des créations pour les huit arènes et les grands donjons, mais garder la géographie de Lavanville et de Cramois'Île (deux époques).
5. **Ne pas prétendre intégrer la campagne entière en une PR monolithique.** Scinder en étapes vérifiables, conserver un journal des modifications et les anciennes scènes tant que la nouvelle continuité n'est pas prête.
6. **Aucune ROM privée ni audio privé sur GitHub.** Les assets protégés restent dans un stockage privé approprié ; l'export public doit être reproductible avec ses sons de repli licites.
7. **Ne jamais prétendre « testé » sur simple compilation.** Ajouter preuves mGBA ou parcours manuel pour les scènes critiques.

## Préflight avant toute modification

- Obtenir commit SHA de branche et date.
- Établir une carte des dépendances (dresseurs, flags, warps, textes, assets, audio).
- Lister les composantes historiques en place et celles à modifier. En particulier : anciens Champions Pierre/Ondine/.../Giovanni, Conseil 4 Olga/Aldo/Agatha/Peter, Matt Champion, caméos Ariane Route 25, Nathan/Katie Céladopole, Enma Mont Braise, Don Morleone postgame Île 5, Nathaniel/Michael à Parmanie.
- Relever les limitations graphiques : sprites combat 64×64, VRAM, palettes, taille ROM maximale 32 Mio. Dernier rapport musical disponible environ 29,82 Mio avec 26 OST privées ; refaire mesure exacte au commit choisi.
- Vérifier le système de sauvegardes, les flags disponibles, les structures d'équipe, les scripts de combat et d'évolution.
- Corriger les ambiguïtés listées dans `12_CONFLITS_ET_QUESTIONS.md` avant remplacement des événements concernés.

## Étapes techniques proposées

### Jalon A — moteur et registre de migration

- Créer des identifiants cohérents pour les huit trophées et leurs flags ; adapter les vérifications de l'accès au Temple.
- Inventorier les scripts d'anciens dresseurs et leur relation aux maps. Ne pas renommer ou écraser irréversiblement les anciennes équipes tant qu'elles servent à d'autres tests.
- Mettre en place la condition Nathan/Katie pour le Champion nº2 et Nathaniel/Michael pour le nº7.
- Valider le comptage exact des huit trophées dans l'état de sauvegarde.

### Jalon B — début, Argenta, rival, première partie

- Adapter la remise Yo-kai Watch / Médallium par Chen sans casser l'intro native existante.
- Créer l'événement Morleone à Argenta et l'apparition humaine d'Enma.
- Adapter les premiers Champions et leurs récompenses.
- Insérer la récurrence d'Agent X à des emplacements scénarisés après arbitrage.
- Valider les deux routes protagoniste sur une nouvelle partie réelle.

### Jalon C — autres Champions et scénarios locaux

- Construire les défis imaginés par Codex, avec previews/présentations pour validation créative.
- Intégrer Bérénice, Ariane, Giraud et les conflits éventuels avec leurs anciens caméos.
- Zombie Night : mêmes coordonnées de Lavanville, états de PNJ, combats au contact, sortie propre.
- Voyage temporel : même structure de Cramois'Île, variante de décor/PNJ, 7e trophée, retour permanent, restrictions de mouvement.
- Don Morleone 8e Champion ; aucune arène neuvième à Céladopole.

### Jalon D — Temple et boss final

- Construire quatre salles / sous-donjons ; combattre Laure/Marge, Lady Perpetua, McKraken, Agent X comme **dresseurs simples**.
- Prototype puis intégration des deux phases de Soranaki avec support dédié : barre de PV exceptionnelle, transformations colorées, enchaînement sans soin.
- Scène Matt soignant avant phase 1, fuite des méchants, révélation Enma.
- Cinématique Bingo-kai : non-utilisation du souhait, Hall of Fame et crédits préservés.

### Jalon E — postgame

- Limbes + boss rematch Soranaki.
- Paradis Divin + Enma l'Ancien.
- Enma souverain dresseur sur Île 7.
- Rencontres fixes Kyubi/Mademoaiselle/Octorgone après arbitrage des lieux.
- Grand-père âgé en arène du présent, Domniscian caméo discret.
- Répartir deux ou trois Yo-kai exclusifs par donjon, sans interrompre la possibilité d'obtenir les 151.

### Jalon F — recette intégrale et équilibrage

- Route complète depuis Bourg Palette jusqu'au Panthéon en **Nathan et Katie**.
- Vérification de toutes les arènes, trophées, transitions, équipe de Matt, double combat Soranaki, postgame, captures fixes, Médallium 151, évolutions, bugs graphiques/audio, sauvegardes et retours de version.
- Tester combats de dresseurs réels avec difficulté normale : la plupart des fixtures existantes utilisent volontairement des équipes surpuissantes et **ne valident pas l'équilibrage**.
- Relever la ROM réelle, version exacte, checksum, fichiers créés/modifiés, captures et réserves.

## Protocole de validation d'un level design

Chaque arène/donjon soumis par Codex devrait fournir : plan de salles et connections, description de la progression, échantillon de tilesets, liste d'événements, captures en jeu et arguments sur la cohérence avec le Champion. Le créateur approuve l'idée et les visuels ; **Codex reste libre de concevoir l'espace**, sans revenir demander au créateur de dessiner tous les plans lui-même.

## Cas de non-régression impératifs

- Sauvegarde au milieu de Zombie Night → rechargement → fin → réapparition des PNJ normaux.
- Sauvegarde à Cramois'Île passée → rechargement → pas de sortie illégitime → retour permis après septième trophée.
- Dans la route Katie, Nathan est Champion et **Michael jeune** à l'époque passée ; dans la route Nathan, Katie est Championne et **Nathaniel jeune**.
- Tous les huit trophées requis au Temple. Pas de neuvième trophée.
- Matt guérit avant boss mais **aucune guérison entre les deux phases de Soranaki**.
- Les quatre adversaires Temple ne se transforment jamais en boss multicouches.
- Passage Panthéon sauvegarde équipe et générique natifs.
- Après fin, postgame disponible sans réinitialisation des états essentiels.
- Aucun changement indésirable des 151 sprites/empreintes/icônes, des fichiers audio privés, des palettes, ou des IDs d'espèces.

## Définition de « terminé »

Une fonctionnalité n'est finalisée que si son code, ses ressources, ses dialogues, ses conditions de déclenchement, son build, sa sauvegarde et ses tests réels sont livrés ensemble. Les rapports d'anciennes sessions ne prouvent pas l'état du nouveau code après migration.
