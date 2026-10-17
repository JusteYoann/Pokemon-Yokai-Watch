# Développement actif Pokémon × Yo-kai Watch

Branche : `dev/reconstruction-finalisation`. **NON PRÊT — reconstruction en cours.** `master` et la branche de récupération restent préservés. Les rapports de récupération décrivent un instantané historique ; leurs contrôles d'identité avec Rouge Feu original ne s'appliquent plus à cette branche modifiée.

## Compiler et contrôler

Debian 13 amd64 : `bash RECUPERATION_PROJET/scripts/configurer_outils_debian.sh`, puis `source /workspace/.setup/env.sh` et `make -j4`. Les instructions générales des autres plateformes restent dans INSTALL.md. La ROM est un dérivé local ignoré ; ne pas la publier.

`python3 tools/yokai/verifier_rom.py` contrôle les données réellement liées dans la ROM, les 151 noms abrégés, statistiques et talents, les 56 évolutions et les 906 ressources graphiques. Ce contrôle est distinct d'une recette dans mGBA. Ne pas utiliser `firered.sha1` comme hash attendu du hack.

## Premier jalon reconstruit

- 151 noms canoniques dans les sources, avec abréviations de 10 caractères terminées par un point si nécessaire ; correspondances SPECIES_* inchangées. Table des noms affichés dans data/yokai/noms_affiches.json.
- Statistiques, types et talents validés actifs pour les 151 espèces.
- 56 évolutions actives, sans les anciennes évolutions croisées vers des espèces hors roster. Méthode Noko : amitié >=220 et Œuf Chance tenu, montée de niveau, objet non consommé.
- 151 listes CT/CS actives.
- 151 faces et dos, icônes et empreintes récupérés intégrés. 14 redesigns approuvés appliqués exclusivement. Les 137 autres graphismes normaux et les icônes/empreintes sont comparés aux octets historiques.
- Croissance harmonisée MEDIUM_FAST pour les 151 afin d'éviter des sauts de niveau lors d'une évolution entre anciens emplacements aux courbes incompatibles ; choix secondaire non fixé par les CSV, documenté ici.

## Reste à reconstruire et vérifier

Obtentions/scripts/rencontres et équipes validées ; graphismes Nathan/Katie/Matt ; caméos ; dialogues français ; shiny finaux ; musiques DPCM ; dix quêtes ; recette complète et contrôle d'un clone propre.

Les palettes shiny actuellement raccordées sont HISTORIQUES, pas une validation de la direction artistique finale. Aucune fonctionnalité non testée ne doit être annoncée terminée. Les états et preuves sont conservés dans QA_RECETTE_FINALE/RECONSTRUCTION/.

Les fichiers PNG/palettes sont les sources maintenables. Les .4bpp/.gbapal/.lz sont générés par le build et ignorés. Le script outils/yokai est `tools/yokai/reconstruire_base.py` ; il reconstruit le premier jalon depuis les sources validées et l'instantané original. Ne pas le relancer aveuglément après des retouches ultérieures : il réécrit ses fichiers de sortie, dont les palettes historiques.

## Moteur : deuxième jalon

- Multi Exp. permanent dans le chemin réel de distribution : participants se partagent le gain complet ; chaque réserve vivante non-œuf reçoit 50 %. Objets Œuf Chance, bonus dresseur et bonus d'échange préservés. Le test en combat réel est reproduit par tester_combat_mgba.py ; l'équilibrage du parcours reste à effectuer.
- Matt imposé à la création et dans le placeholder des dialogues ; étape de choix du prénom rival sautée dans l'introduction. Le nom du joueur reste personnalisable. L'introduction complète et les affichages secondaires restent à tester.
- 84 espèces shiny autorisées dérivées des références et des familles ; 67 exclues au niveau des PID générés, des palettes, du résumé et des étoiles de combat. Appak justifie la famille Kappacap ; la référence propre à Kappacap est ignorée. Noko reste exclu. Le dessin des 84 shiny n'est pas terminé.
- Tests natifs dans mGBA : les quatre cas limites Noko, les 151 statuts shiny avec PID forcés, le maintien nature/sexe et une sauvegarde/relecture Flash native passent. Ce sont des fixtures par appel des fonctions du jeu, pas une partie de validation.

Pour reconstruire mGBA : disposer de CMake et d'un compilateur C/C++, activer les outils de compilation, puis `bash tools/yokai/installer_mgba.sh`. Le commit du core est fixé. Si le répertoire diffère, définir MGBA_LIBRETRO_PATH vers mgba_libretro.so. Exécuter `python3 tools/yokai/tester_mgba.py`. Versions/hashes dans QA_RECETTE_FINALE/RECONSTRUCTION/OUTILS_MGBA.json. Aucun BIOS commercial n'est requis : mode HLE du core.

## Apprentissages et libellés français

Les 151 listes sont actives : 1 977 lignes transcrites des captures récupérées, avec provenance et corrections OCR documentées. Octorgone utilise bien la version Dragon (Dracosouffle 24, Dracogriffe 46). Les lignes à l’évolution et les quatre apprentissages à évolution +2 niveaux sont intégrés, avec mémorisation du niveau d’évolution dans un champ réservé existant, sans changement de format de sauvegarde. Les tests natifs comparent les 151 jeux de capacités et vérifient les cas différés, y compris une évolution tardive. La totalité des lignes OCR n’a pas fait l’objet d’une double relecture humaine : cette réserve est explicite.

Les 354 capacités et les talents utilisent leurs noms français, abrégés avec un point si le libellé dépasse les 12 caractères du moteur. Noms complets et affichés : data/yokai/libelles_attaques_talents.json. Les puissances et identifiants techniques restent ceux du moteur Gen III.

## Obtentions : reconstruction des sources

Les 454 tables sauvages (voir le nombre de slots dans le rapport de couverture) des deux versions sont retargetées vers les 151 Yo-kai, en conservant tous les niveaux et taux originaux. La Route 1 ne contient que Chiperpiou ; la Forêt de Jade seulement les quatre espèces validées. Les trois starters occupent chacun un slot à 5 % du Canyon Sesor, après la Ligue. Les espèces de base voisines réutilisées dans les tables non spécifiées sont identifiées `neighbor_fallback` dans data/yokai/rencontres_appliquees.json. Les fréquences rares retenues sont des choix secondaires documentés (2 % dans les dernières cases terrestres).

Les cadeaux Jibanyan (trois copies), Robonyan, les deux récompenses du Dojo, le marchand Castelius III, Castelius Max au Casino, l’échange Potache → Humainequin et les cinq remplacements statiques sont raccordés. Kyubi reste au Mont Braise et Mademoaiselle aux Îles Écume, confirmation définitive de l’utilisateur. Les autres lots du Casino et échanges susceptibles de distribuer un starter avant le postgame ou une évolution réservée sont adaptés à des bases ordinaires ; noms des lots synchronisés.

Choix secondaires : Nautile → Tristos, Dôme → Sorcophage, Ambre → Potofeu ; vente des deux fossiles par le scientifique du salon de Cramois’Île (10 000 chacun). La résurrection vérifie l’inventaire et les trois résurrections indépendantes, plutôt que l’ancien choix exclusif du Mont Sélénite. Pierre Lune (6 000) et Œuf Chance (12 000) ajoutés au magasin d’évolution de Céladopole pour garantir les conditions d’évolution. Ces prix et les libellés vivent dans items.json, source du fichier généré items.h.

Douze rencontres répétables et capturables sont ajoutées aux cartes sans herbes : Silph, Repaire Rocket, souterrains, Océane, Piste cyclable et Nyada au Canyon Sesor. Leurs capsules visuelles sont PROVISOIRES : les nouveaux overworld spécifiques ne sont pas encore finalisés. Positions contrôlées dans les tuiles de collision ; parcours réel de tous les points encore requis. Le graphe des sources couvre 151 espèces, sans constituer une preuve de complétion en une partie.

Tests mGBA du jalon obtentions : blocage sauvage avant Ligue pour les trois starters et les trois espèces exclusives testées ; trois Jibanyan puis refus du quatrième ; compteur conservé en Flash ; équipe de six et 420 places PC pleines sans consommation du cadeau ; les deux récompenses du Dojo envoyées au PC sur la vraie carte avec flags indépendants. Les adversaires du Dojo sont marqués vaincus dans la fixture ; leur combat et l’approche des objets restent à tester. Commande : python3 tools/yokai/tester_obtentions_mgba.py.

## Équipes de dresseurs : sources actives

639 équipes actives reconstruites, soit 591 dresseurs ordinaires, les 17 boss verrouillés, 21 variantes des sept combats pré-Ligue du rival, six variantes Champion/revanche et quatre revanches du Conseil 4. Les 70 membres des 17 boss conservent exactement espèces, niveaux, ordre, attaques, talents sélectionnés, objets tenus et sac validés dans la synthèse. Le choix du second talent est appliqué à la création native de l’adversaire. Aucun changement de format de sauvegarde.

Les huit étapes de Matt respectent la continuité Cigalopin → Cigallard, puis disparition inexpliquée ; Jibanyan et Navétéran restent non évolués avant la Ligue ; Camaïeul apparaît seulement au Champion. Les trois variantes de starter sont conservées. Détails secondaires choisis : niveaux 58/59/60/60/61/63 au Champion, une Guérison dans le sac, Baie Sitrus seulement sur le starter final ; revanches à +10 niveaux avec la même composition. Les attaques non verrouillées proviennent des apprentissages validés au niveau du combattant.

Les dresseurs ordinaires conservent nombre de membres, niveaux, IV et objets tenus d’origine, avec pools par classe et formes adaptées au niveau ; les sets d’attaques viennent des données Yo-kai. Aucun changement des scripts, des combats doubles ou des flags de victoire. Les anciennes déclarations restent dans le fichier pour l’archive mais les entrées actives pointent sur sYokaiParty_*. Les placeholders Ruby/Saphir inutilisés sont laissés inchangés.

Test natif mGBA : 639 équipes, 1 649 instances, comparaison des espèces, niveaux, attaques, talents, objets et sacs. Cette construction native ne signifie pas que les 639 combats ont été joués. Commande : python3 tools/yokai/tester_equipes_mgba.py. Données lisibles : data/yokai/equipes_boss_validees.json et equipes_appliquees.json.

## Matt : graphismes originaux intégrés

Référence Protagoniste/Matt Descartes.webp ouverte et comparée à Blue dans les sources. Trois poses originales de combat 64×64 et neuf frames overworld 16×32 sont intégrées dans graphics/yokai_characters/matt/. Elles remplacent les trois ressources de combat du rival et le graphisme OBJ_EVENT_GFX_BLUE dans toutes ses apparitions. Les fichiers originaux restent archivés, sans remplacer les palettes partagées des autres PNJ. Palette propre à Matt, 15 couleurs RGB555 + index transparent.

La grande planche générée est conservée intégralement dans source/generated-sheet.png. Son format réel différait du quadrillage demandé ; les rectangles de découpe audités, l’échantillonnage sans lissage et la conversion GBA sont reproductibles par tools/yokai/convertir_matt.py. Les tons orange du casque et les tons olive sont conservés dans une palette commune. Aperçu opaque sur damier : preview-checkerboard.png. Une frame de marche orientée à droite est retournée via les commandes d’animation du moteur, sans dessiner un autre personnage.

Un défaut d’ordre des tuiles a été détecté sur les captures en jeu et corrigé par une règle explicite de conversion des frames 16×32 dans spritesheet_rules.mk. Les captures corrigées montrent les quatre orientations et trois cycles de marche sur place, ainsi que les trois portraits dans de vrais combats mGBA. Tous les sprites liés sont aussi comparés aux pixels des PNG. Les apparitions scénarisées complètes restent à tester. Nathan et Katie ne sont pas encore dessinés/intégrés ; leurs anciennes ressources restent actives à ce stade.

## Outils QA et synchronisation

Après l’installation de compilation, bash tools/yokai/installer_tests_debian.sh installe CMake (si absent) dans le sysroot utilisateur et construit le core mGBA fixé. Les paquets Debian sont vérifiés par empreintes. Pillow est une dépendance Python de la QA et des conversions PNG (tools/yokai/requirements.txt), pas du build du jeu. Ne pas exiger les fichiers privés ou un BIOS pour compiler/tester les sources publiques actuelles.

Le clone indépendant depuis GitHub a reproduit octet pour octet le jalon 3f65e9015 : voir REPRODUCTIBILITE_EQUIPES.json. Une vérification du jalon graphique suivant est distincte. Les enregistrements musicaux restent privés ; à ce stade aucune OST Yo-kai ni quête finale n’a encore été intégrée.

## Premier caméo restauré : Ariane et Usapion

Ariane et son accompagnateur Usapion sont visibles au Cap de la Route 25 (57,7 et 59,7), sans gêner la maison de Léo ni les PNJ existants. Sprites originaux : un portrait de combat 64×64, trois orientations stationnaires 16×32, Usapion 32×32 ; une palette commune dédiée, indépendante des autres PNJ. Les références de l’archive ont été ouvertes avant dessin. Sources et aperçu sur damier dans graphics/yokai_characters/ariane/.

Les équipes validées sont actives : aventure 100/28/145 aux niveaux 17/18/20 ; postgame 101/28/110/30/145 aux niveaux 56/57/58/59/60. Le postgame est sélectionné même lors d’une première visite tardive. Combat volontaire Oui/Non, une seule victoire nécessaire pendant l’aventure, revanches postgame à volonté. Pierre Lune unique, récupérable plus tard sans refaire le combat si le sac était plein. Les deux IDs de dresseurs proviennent de placeholders Ruby/Saphir sans ancien événement, sans agrandir les structures de sauvegarde. Registre : data/yokai/registre_identifiants.json.

Recette mGBA par vraie interaction sur la carte : refus avec équipe valide ; victoire avec 42 emplacements d’objets pleins ; retour après libération d’une place ; absence de cadeau dupliqué ; revanches répétées ; premier combat directement en postgame ; défaite et retour après K.O. sans victoire fictive ni récompense ; flags conservés en sauvegarde Flash. La fixture de victoire utilise volontairement un combattant surpuissant : elle valide les scripts, pas la difficulté. L’attente du pilote suit désormais la fin réelle des dialogues, au lieu d’une durée supposée.

Les noms/descriptions des cinq pierres d’évolution, de l’Œuf Chance et des trois fossiles sont traduits. Les identifiants techniques et mécanismes sont conservés ; Fossile Nautile est abrégé « Foss. Nauti. » pour les 13 caractères disponibles. Les boutons généraux affichent Oui/Non. Le reste de la traduction reste à faire.

Les autres caméos, Nathan/Katie, les shiny définitifs, les 20 OST DPCM et les dix quêtes restent incomplets. Ariane est un caméo de la base à restaurer, pas l’une des dix nouvelles quêtes. Le verrou supplémentaire d’Enma lié à son futur combat caméo reste encore à intégrer.
