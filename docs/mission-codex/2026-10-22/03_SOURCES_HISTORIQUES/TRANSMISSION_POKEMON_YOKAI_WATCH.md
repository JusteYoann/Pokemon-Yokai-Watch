# DOSSIER DE TRANSMISSION — POKÉMON × YO-KAI WATCH
**Version de contexte : 20 octobre 2026 — pour reprendre la conversation dans un nouveau chat**

> **Mode d'emploi pour le prochain assistant :** ce document synthétise les décisions prises et propositions discutées. Respecter la distinction **VALIDÉ (choisi explicitement par l'utilisateur)**, **PROPOSÉ (idée de l'assistant non confirmée)** et **NON IMPLÉMENTÉ / À VÉRIFIER (ne pas prétendre que c'est codé)**. La chronologie officielle de Yo-kai Watch et les informations du wiki sont des références d'inspiration ; le fangame se déroule dans un **univers alternatif**. Ne pas changer les décisions de l'utilisateur sans lui demander. Le dernier thème étudié était la biographie de **McKraken** ; poursuivre à partir de celle-ci.

## 1. PROJET, OBJECTIF ET CONTEXTE TECHNIQUE

- Fangame / ROM hack de **Pokémon Rouge Feu sur Game Boy Advance**, dans l'univers **Yo-kai Watch** ; 151 espèces de Yo-kai, sprites de face et de dos, icônes, combats, événements, dialogues en français et bande-son Yo-kai Watch.
- Dépôt GitHub : https://github.com/JusteYoann/Pokemon-Yokai-Watch ; branche suivie `dev/reconstruction-finalisation`.
- Codex intervient sur le dépôt ; utilisateur crée et approuve les références visuelles. Important : les **orientations volontairement inversées** de sprites sur ses 151 maquettes doivent **être reproduites**, pas « corrigées ». Parfois ses maquettes emploient un ancien sprite : conserver **placement/orientation** mais employer **la version graphique la plus récente**.
- Cadrages de combat : https://github.com/JusteYoann/Pokemon-Yokai-Watch/tree/dev/reconstruction-finalisation/QA_RECETTE_FINALE/CADRAGE_COMBATS_151/ ; les 151 comparaisons figurent dans le dossier `comparaisons`. D'après un ancien rapport, certaines inversions voulues n'étaient pas respectées et 86 cadrages étaient plafonnés par le format natif 64×64. Ne pas supposer qu'ils ont été corrigés depuis sans vérifier les nouveaux commits.
- Documentation graphique : `QA_RECETTE_FINALE/POST_B13/SESSION_2_GRAPHISMES/README.md` ; graphismes overworld Nathan, Katie, Matt, Ariane et Mafiamille, icônes 151, shiny partiellement finis.
- Audio : 26 OST Yo-kai Watch prévues/intégrées au projet privé, 104 identifiants de musiques réorientés selon le rapport `QA_RECETTE_FINALE/AUDIO_30MIO/README.md` ; présence résiduelle de Pokémon et boucles à contrôler. Garder les bruitages Pokémon. Le rapport indiquait des soucis pour Enma Track et Final Battle – Are You Ready. Audio soumis à limite de ROM 32 Mio.
- Français : début largement traduit, traduction exhaustive et scénario de fin non encore garantis ; voir `QA_RECETTE_FINALE/LOCALISATION_FR/README.md`.
- En local, Windows `C:\YokaiBeta`, WSL Debian `/home/yoann/yokai-build`, scripts environnement `/home/yoann/yokai-outils/env.sh`. Dossiers audio privés `C:\YokaiBeta\audio-prive\full-sources`, `post-b13-integration`, `Yokai_Watch_OST`. Il manque certains WAV `08,09,10,13,14,16,18,19,20` dans `full-sources` selon captures ; ne pas prétendre que cela équivaut à 9 OST actives absentes. Une compilation **sans dossier audio privé** a fonctionné et produit `pokefirered.gba` ; ROM de test copiée/à copier sous nom `C:\YokaiBeta\Pokemon-Yokai-Watch-V1-Test.gba` suivant guide antérieur. **Cette ROM sans OST privée ne valide pas l'ambiance sonore finale**. Ne pas inventer état actuel du disque ou dépôt.
- Projet proche d'une **V1 privée de test** du point de vue technique, MAIS le grand scénario original décrit ci-dessous est un **projet narratif en construction**, pas une fonctionnalité déjà mise en œuvre. Distinguer cette ambition de la ROM actuellement compilable.

## 2. LE MONDE ET SES RÈGLES — VALIDÉ

- Chronologie **alternative** à celle des jeux originaux Yo-kai Watch.
- Les **humains et les Yo-kai coexistent ouvertement**, tous connaissent les Yo-kai ; leurs mondes ne font qu'un, dans une paix/harmonie générale dont l'équilibre se fragilise.
- Le professeur **Chen** a inventé le **modèle le plus récent de Yo-kai Watch**, et confie la montre au joueur (Nathan ou Katie). Il lui remet une **ancienne relique, le Médallium**, qu'il demande d'aider à compléter. La montre peut servir à lier/invoquer les Yo-kai (proposition cohérente, détails à finaliser).
- Depuis la mort d'**Enma l'Ancien**, l'équilibre politique s'est fragilisé. **Seigneur Enma** lui succède, est favorable à la coexistence humains–Yo-kai. Respecter le canon familial : **Enma l'Ancien est son grand-père** (utilisateur l'a explicitement corrigé et accepté), pas son père.
- Don Morleone cherche à prendre le contrôle de Kanto et à **réveiller Soranaki**, ancien dieu Yo-kai banni par Enma l'Ancien il y a des siècles.
- **Course aux trophées** annuelle, tradition ancienne : affronter huit Champions, rassembler **8 trophées obligatoires** (confirmé explicitement), obtenir droit d'entrer au **Temple Céleste** ; vaincre ses épreuves donne accès au **souhait** du Panthéon. Aucun accès à 4 trophées : variante abandonnée.
- Matt (Matthieu Descartes) est le rival amical du joueur, veut obtenir les trophées avant lui.

## 3. SCÉNARIO PRINCIPAL — TRAME VALIDÉE ET DÉTAILS À PRÉCISER

**Début — Bourg Palette :** Chen remet Yo-kai Watch et Médallium ; début d'aventure inspiré de Rouge Feu, rencontres, progression dans Kanto.

**Argenta, juste après la Forêt de Jade :** grand rassemblement public. **Don Morleone** arrive entouré d'une troupe de Mafiamilles, déclare vouloir conquérir Kanto et réveiller **Soranaki**, bannie autrefois par Enma l'Ancien. Il somme les villageois de rejoindre la Mafiamille et les menace de conséquences en cas de refus, puis part. **Seigneur Enma sous apparence humaine/civile** (visuels fournis dans le chat ; nécessite deux sprites) approche le protagoniste, lui demande s'il est nouveau, contextualise mort d'Enma l'Ancien et ambitions de Morleone, explique les huit trophées, Temple et souhait, l'encourage et disparaît sans révéler son identité. IMPORTANT : Enma humain a une apparence de référence fournie dans deux images utilisateur et ne doit pas être redessiné arbitrairement.

**Voyage dans Kanto :** quête de Médallium, course aux trophées, combats réguliers contre Matt, affrontements et scènes avec la Mafiamille. Les arènes doivent devenir huit mini-aventures originales.

**Jadielle, huitième trophée :** Don Morleone est Champion. Après défaite, remet le trophée à contrecœur, reconnaît la force du héros, révèle avoir lui aussi 8 trophées et se rend au Temple. Son histoire officielle : chef mafieux il y a 555 ans, banni dans l'espace par Enma l'Ancien, revient avec OVNI / Pierre Philosovni. Pour cohérence, **il a reformé récemment la Mafiamille** plutôt que l'avoir créée pour la première fois (proposition d'ajustement, à confirmer). Ses motivations détaillées de contrôle de Soranaki sont proposées mais pas officiellement arrêtées.

**Temple Céleste, remplaçant la Ligue** — VALIDÉ : lieu suprême sacré gardé par Zazel et/ou Enma, immense temple/labyrinthe d'épreuves, 8 trophées obligatoires ; **les quatre affrontements ne sont PAS contre des dieux**. Ce sont quatre antagonistes de Yo-kai Watch associés à Don Morleone :
1. **Laure et Marge** (Kin et Gin) — duo qui manipule le temps, les salles et les mécanismes temporels.
2. **Lady Perpetua** (Dame Dedtime) — supérieure canonique de Laure et Marge, rancune liée à une injustice humaine passée, capacités temporelles, forme Lady Démona.
3. **McKraken** — président tyrannique du monde Yo-kai dans YW1, partisan de la supériorité Yo-kai, méprise humains et Yo-kai amis des humains, boss à deux formes dans l'original.
4. **Agent X** — second de Don Morleone, obstacle juste avant sanctuaire.
Les quatre sont des **intrus / alliés de circonstance**, et NON des gardiens divins légitimes. Labyrinthes de temple prévus (détails encore non validés). L'alliance exacte, les motivations individuelles et la question de leur éventuelle trahison restent à écrire.

**Sanctuaire final :** Don Morleone a déjà invoqué Soranaki. Agent X est vaincu juste avant selon structure Temple ; **Matt arrive et soigne l'équipe du joueur** avant Soranaki (VALIDÉ). Soranaki peut se transformer en plusieurs Yo-kai en conservant ses propres couleurs, dispose d'une **énorme barre de vie** (fonctionnalités ambitieuses, à programmer). Après premier combat, prend une **forme humaine**, prononce un discours de mépris puis **second affrontement plus difficile SANS soin entre les deux phases**. Soranaki disparaît définitivement, Don Morleone et Agent X quittent salle furieux. **Enma révèle sa véritable identité**, félicite le protagoniste et l'amène au Panthéon. Ne pas faire passer les nouvelles mécaniques boss comme déjà codées ; leur faisabilité technique n'est pas garantie.

## 4. LES HUIT CHAMPIONS — PERSONNAGES VALIDÉS, VILLES EN PARTIE PROPOSÉES

Tous les personnages ci-dessous sont sélectionnés pour le casting, mais les lieux précis pour certains restent **des propositions** ; ne pas les figer à tort :

| Trophée suggéré | Champion | Ville proposée | Événement / identité |
|---|---|---|---|
| 1 | **Wyatt Cardamom** (Buck Hazeltine) | Argenta | aventurier terrain, musée, OVNI, exploration ; réaction publique possible contre Don Morleone |
| 2 | **Katie si joueur Nathan / Nathan si joueur Katie** | Azuria | dialogues conditionnels, relation d'amitié et admiration comique de Nathan pour Katie |
| 3 | **Bérénice Bélier** (Diana Gately) | Carmin-sur-Mer | scientifique énergique des **Portes Mystères**, épreuve dimensionnelle et téléporteurs, pas simple arène électrique |
| 4 | **Ariane Célestin** (Hailey Anne Thomas) | Safrania | passionnée d'espace, mangas/animés, Sailor Cuties et **Usapyon** ; arène station spatiale avec téléporteurs |
| 5 | **Inspecteur Giraud** (Detective Holdit) | Parmanie | enquête policière et labyrinthe ; caractéristiques du personnage encore à documenter par biographie |
| 6 | **Alyzon Bie** (Dr. Francesca Stein) | Lavanville | **Zombie Night** scénarisée, recherches sur zombies ; arène à implanter (Lavanville n'a PAS d'arène dans Rouge Feu) |
| 7 | **Nathaniel Adams si joueur Nathan / Michael Forester si joueur Katie** | Cramois'Île **dans le passé** | Triptic-tac et voyage temporel ; Hovernyan ; les versions âgées vivent dans le présent |
| 8 | **Don Morleone** | Jadielle | chef Mafiamille et adversaire clé |

ATTENTION : tableau de villes discuté à plusieurs reprises et jamais finalisé intégralement. Rouge Feu possède à l'origine des arènes à **Argenta, Azuria, Carmin-sur-Mer, Céladopole, Parmanie, Safrania, Cramois'Île, Jadielle** ; Lavanville n'en a pas : déplacer ou ajouter une arène sans produire un 9e trophée et sans casser progression. Les propositions de villes Safrania/Ariane et Lavanville/Alyzon créent un besoin de réorganisation de Céladopole. L'ordre narratif 4/5/6 peut être retravaillé.

## 5. ZOMBIE NIGHT À LAVANVILLE — VALIDÉ ET PRÉCISIONS

- Événement scénaristique unique (pas ville zombie permanente ni mini-jeu rejouable à ce stade).
- Fidèle à l'ambiance de **Zombie Night de Yo-kai Watch 3** : soudain, tous les habitants humains ont **disparu**, seule une population de **zombies mystérieux** est visible ; **origine du phénomène non expliquée**. Ne PAS lier artificiellement à Mafiamille, Soranaki ou pollution, et ne pas prétendre que les habitants ont eux-mêmes été transformés. La première proposition de l'assistant « Mafiamille provoque une pandémie de zombies » a été **rejetée** par clarification de l'utilisateur.
- **Alyzon Bie** est la figure qui explique le phénomène au joueur, comment survivre et comment en sortir. Canon : elle adore ses sujets d'étude, trouve les zombies « mignons », est solitaire, nocturne, passionnée de recherche, utilise parfois la force (marteau), a connu Bérénice Bélier à l'université.
- Mécanique validée : **quand un zombie touche le joueur, un combat s'enclenche immédiatement** contre le zombie, qui commande des Yo-kai. Les zombies peuvent errer/avancer ; détection dynamique est faisable mais non triviale sur moteur GBA. Sortie par **cloche** à la tour (référence canon) : **proposition, à confirmer**. Sort en revenant dans ville normale. En cas de défaite, retour au point de départ : proposition non confirmée. Zombie battu : disparition temporaire ou réapparition encore à décider.
- Alyzon, Championne d'arène de Lavanville, peut inviter au combat après sortie de Zombie Night. Elle aime et étudie zombies, ne souhaite pas nécessairement éliminer le phénomène.

## 6. CHAPITRE VOYAGE TEMPOREL À CRAMOIS'ÎLE — VALIDÉ

- Au présent, PNJ indique **Champion absent**, souvent aperçu au **Manoir Pokémon**. Joueur se rend au manoir et interagit avec **Triptic-tac (Miradox)**.
- **Flash blanc**, le joueur est au **même endroit** mais avec un filtre visuel **vieilli/sépia** ; bâtiments/manoir et PNJ sont aussi légèrement différents : joueur a voyagé dans le passé.
- En reparlant à Triptic-tac, celui-ci **refuse de ramener** le joueur. Le joueur explore Cramois'Île passée, affronte le Champion du passé : **Nathaniel jeune si protagoniste Nathan ; Michael (Kenny Forester) jeune si protagoniste Katie**. Ils sont deux alternatives liées au protagoniste, pas obligatoirement un duo co-Champions.
- Champion remet **7e trophée**, accepte alors d'aller convaincre Triptic-tac, qui rétablit le passage. Retour au présent.
- **Déblocage permanent** après quête : reparler à Triptic-tac pour voyager librement entre **deux versions de Cramois'Île uniquement**, pas tout Kanto.
- **Yo-kai qui bloquent les sorties** de l'île du passé, à la manière de Misterre ; interdire Surf, Vol, Téléport ou autres contournements. Sécuriser état de sauvegarde/transitions.
- **Nathaniel jeune** : déterminé, fan de Moximous Mask, fier, méfiant, ami de Hovernyan, lien familial grand-père de Nathan. **Michael jeune** : personnage équivalent du côté Katie, grand-père de Katie, passion Moximous Mask, Hovernyan.
- Les **versions âgées de Nathaniel ET Michael sont vivantes dans le présent** de notre continuité (canon officiel différent : décédés). Possibles retrouvailles avec joueur au retour ; **combat rematch postgame de Nathaniel âgé**, demandé et approuvé par utilisateur, potentiellement réitérable ; équivalent Michael âgé **proposé** dans route Katie (à confirmer). Ne pas supposer qu'un seul ou les deux sont Champions dans la même partie sans décision utilisateur.
- En canon, Nathaniel / Michael ont inventé premiers prototypes de Yo-kai Watch dans leurs chronologies alternatives ; dans fangame, Chen invente **dernier modèle** : complément possible, à fixer.

## 7. PERSONNAGES, SOURCES BIOGRAPHIQUES ET CARACTÈRES

**Professeur Chen** — créateur du dernier modèle de montre, confie montre + Médallium au joueur ; début classique de Rouge Feu.

**Seigneur Enma** — roi des Yo-kai, petit-fils / successeur d'Enma l'Ancien (canon respecté), veut coexistence harmonieuse, jeune, curieux et joueur, visite les humains, capable de fermeté. **Sous forme humaine** au rassemblement d'Argenta, sprite distinct (deux références visuelles fournies). Révèle identité à la fin. Zazel est son conseiller.

**Zazel** — bras droit, chef Conseil Yo-kai, noble, intelligent, politique, froid et défiant les humains en raison de l'influence d'Enma l'Ancien. Gardien du Temple : autorise entrée après 8 trophées. Peut contester Enma sans être traître. Combat postgame éventuel ou épreuve optionnelle : non décidé.

**Don Morleone** — chef Mafiamille, Champion Jadielle, ancien chef de mafia banni il y a 555 ans par Enma l'Ancien dans le canon, Pierre Philosovni, forme Don Spiration. Dans fangame veut conquérir Kanto / ressusciter Soranaki, viser le sanctuaire ; les modalités précises de la pierre, du souhait et de la manipulation de Soranaki restent à déterminer. Don Spiration en postgame = PROPOSITION non validée.

**Agent X** — second de Morleone, quatrième combattant Temple. Biographie détaillée non encore fournie. Distinguer de Zazel.

**Matt / Matthieu Descartes (Edward Archer / Eddie)** — rival du protagoniste dans Course aux trophées : plus studieux et technophile que Nathan, calme, sociable, parfois un peu suffisant, esprit rationnel/scientifique. Progression d'une compétition amicale vers respect mutuel ; **soigne équipe du joueur avant Soranaki**. Dans canon, doute du surnaturel : adapter dans monde où Yo-kai sont visibles pour tous ; pas nier existence des Yo-kai, chercher causes rationnelles de phénomènes.

**Nathan Adams / Katie Forester** — joueur au choix ; **l'autre est Champion d'Azuria** (proposition de ville bien reçue mais rappeler statut), dialogues différents. Nathan bon garçon ordinaire, déteste « banal », veut impressionner Katie, fort lien aux Yo-kai, courageux ; Katie intelligente, gentille, appréciée, joueuse, souvent inconsciente de ses sentiments. Pas de cruauté inutile de Katie ni romance envahissante. Les effets sont des petites scènes comiques, pas le cœur du scénario.

**Wyatt Cardamom (Buck Hazeltine)** — aventurier de plein air, OVNI, artefacts, protecteur amis, initialement réservé/méfiant ; Argenta + musée/expédition serait bonne épreuve, mais pas encore définitivement arrêtée. Distinguer de l'imaginaire SF d'Ariane.

**Bérénice Bélier (Diana Gately)** — scientifique pleine d'énergie, insistante, obsédée par **Portes Mystères / Gates of Whimsy**, recrute assistants, passionnées des dimensions. À l'origine, suggestion de laboratoire électrique puis **réorienté vers Portes Mystères**, beaucoup plus fidèle. Ancienne camarade de fac d'Alyzon ; dialogues croisés possibles.

**Ariane Célestin (Hailey Anne Thomas)** — jeune passionnée espace, ovnis, Sailor Cuties/anime, bavarde, imagination débordante, compagnon Usapyon et agence de détectives. Arène spatiale avec téléporteurs à Safrania (proposition) ; distinguer de Giraud enquêteur et Bérénice universitaire. Usapyon devrait être son partenaire combat.

**Inspecteur Giraud (Detective Holdit)** — Champion sélectionné, arène-enquête à Parmanie proposée. Sa bio détaillée attendue.

**Alyzon Bie (Dr. Francesca Stein)** — chercheuse Zombie Night à St. Peanutsburg dans canon, solitaire, aime les zombies, marotte insolite, déteste jour, amie/université avec Bérénice, marteau « Whomper », recherche peu orthodoxe. Ne pas la confondre avec Bérénice.

**Nathaniel Adams / Michael Forester** — détails au §6. Canon des versions jeunes et âgées décrit dans biographies. Vivants âgés : choix de chronologie alternative.

**Laure et Marge (Kin/Gin)** — vieilles jumelles maléfiques qui manipulent le temps avec horloge/Pierre temporelle, cruellement rusées, dévalorisent amitié, peuvent réanimer sœur durant boss canon, subordonnées de Lady Perpetua. Dans canon impliquées dans traumatisme passé de Nathaniel/Michael. Première épreuve temporelle de Temple ; mécanique de double combat/retour en arrière encore non spécifiée techniquement.

**Lady Perpetua (Dame Dedtime)** — ancienne humaine injustement emprisonnée, convertie en Yo-kai vengeur, temps volé, contrôle Yo-kai corrompus, forme Lady Démona. Dans Spectres Psychiques existe arc de rédemption (Dame Deartime), pas encore décidé si repris dans fangame ; sans présumer qu'elle a déjà fait la paix. Deuxième épreuve Temple, alliance possible avec Morleone contre promesse de réparer passé = PROPOSITION.

**McKraken** — CHEF/président du Yo-kai World avant qu'il soit vaincu (canon YW1). **Pride suprémaciste Yo-kai : les humains lui semblent inférieurs et les Yo-kai amis avec eux sont des traîtres domestiqués** ; personnalité orgueilleuse, têtue, blagues marines. Dans canon, a saisi pouvoir après mort d'Enma l'Ancien, essayé invasion des humains, deux formes de boss ; devient gérant restauration / services communautaires dans YW3, puis recrutable YW4. **Problème de cohérence à traiter pour le fangame** : Enma est roi et paix humains/Yo-kai règne, donc pourquoi McKraken est libre, allié de Morleone, et a-t-il été pardonné ? On peut adapter sa trajectoire à univers alternatif ; demander utilisateur s'il veut un McKraken encore tyrannique ou ancien tyran récidiviste. Troisième épreuve du Temple. Surtout ne pas le présenter seulement comme « monstre marin fort » sans idéologie politique et antécédents.

**Soranaki** — dieu Yo-kai autrefois banni par Enma l'Ancien, final de l'aventure, métamorphose en autres Yo-kai de sa couleur et seconde forme humaine/combat plus difficile sans soin. Explication précise du lien historique, invocation et souhait encore à travailler.

## 8. PHILOSOPHIE DE CONCEPTION ET ÉTAT DU DÉVELOPPEMENT

- L'utilisateur souhaite **une vraie aventure originale Yo-kai Watch dans Kanto**, pas une simple conversion graphique de Rouge Feu. Conserver structure 8 trophées, village/forêt/routes, progression viable, mais réécrire personnages/dialogues/épreuves ; conserver identité et biographies des personnages du canon lorsque pertinent.
- Le moteur Rouge Feu permet PNJ qui avancent, se tournent, dialogues, combats, flags, maps et téléporteurs. Les idées avancées telles que zombies poursuivant joueur librement, boss Soranaki morphing en direct, énorme barre PV, temple nouveau avec puzzles et sauvegardes demandent refonte/test. Faisabilité **en principe**, pas garantie ni intégrée.
- Révisions prioritaires à planifier avec Codex quand quota revient : récit scénarisé, PNJ + portraits originaux, cartes d'île passée et de Lavanville Zombie Night, remplacement Team Rocket par Mafiamille, arènes, Temple Céleste, scripts/reconstructions et tests de softlocks. Attention taille ROM ~30/32 Mio sans marge importante ; performance, bugs, scripts et compatibilité saves.
- **Ne pas publier une ROM contenant ressources audio privées/copyrightées** sur GitHub. Utiliser dossier privé de compilation.

## 9. VIDÉO YOUTUBE — PROJET ASSOCIÉ

- Chaîne **Juste Yoann**, style miniature cartoon, projet vidéo **« J'ai créé un FAN GAME YO-KAI WATCH ! »**, miniature : cartouche GBA bleue inspirée Pokémon Saphir, logo Yo-kai Watch, fond blanc, flèche et « Moi », marque Juste Yoann. L'assistant a validé la composition réaliste comme contraste utile avec chaîne cartoon ; utilisateur a partagé miniature et capture de chaîne.
- Vidéo documentaire « 7 jours » : raconter transformation en étapes : prototype, 151 Yo-kai, personnages, scénario, audio, finitions, test V1 ; **si travail étalé sur semaines, ne pas prétendre faussement une semaine réelle**. L'utilisateur envisage de **reconstituer volontairement sept ROM cumulatives** (Jour 1 à Jour 7) pour montrer progression en vidéo, via historique Git/branches documentaires, sans refaire tout le projet ni falsifier des preuves de dates.
- Fin de vidéo : teaser live découverte à une date et heure à fixer lorsque ROM stable, puis éventuellement vidéo de l'aventure. La nouvelle grande intrigue pourra être montée dans future V1 ou V2 ; ne pas confondre l'ancien build avec les ambitions scénaristiques récentes.

## 10. POINTS À DÉCIDER / CONTRADICTIONS NON RÉSOLUES

1. Répartition spatiale des **8 Champions sur 8 arènes**, déplacement nécessaire pour Alyzon à Lavanville ; sort de Céladopole et de Safrania.
2. Les deux grands-pères sont-ils simultanément présents dans le même univers, et un seul Champion variable selon joueur ? Apparitions/rematch âgé Michael vs Nathaniel.
3. Relation hiérarchique du roi Enma, Zazel, McKraken et Don Morleone à travers 555 ans : éviter chronologie contradictoire.
4. Pourquoi et comment Soranaki est-il invoqué avec souhait/temple ? Motivations de Morleone, sort du souhait final, conséquences postgame.
5. Quatre adversaires Temple : comment les criminels ont infiltré lieu sacré, motivations de chacun, et pourquoi Zazel/Enma ne les arrête pas immédiatement.
6. Lady Perpetua : rancune active ou rédemption passée ? La biographie officielle comporte les deux états à des moments différents.
7. Zombie Night : mode précis de sortie (cloche = proposition), comportement zombie après combat/perte, zone et récompenses.
8. Alternative duo de Champion Nathan/Katie à Azuria, biographies et teams compatibles avec 151 espèces ; 8 trophées exactement.
9. McKraken : rôle politique original et état de sa rédemption dans chronologie alternative — dernier thème discuté.
10. Différencier encore les personnages choisis, les chapitres scénaristiques décidés, les dialogues exemples, les graphismes non intégrés et ROM compilée.

## 11. INSTRUCTION DE REPRISE POUR LE NOUVEAU CHAT

« Je développe un fangame Pokémon Rouge Feu × Yo-kai Watch et je t'ai transmis ma bible de continuité. Lis-la entièrement et considère ses décisions **VALIDÉES** comme notre cadre ; ne présente jamais comme faits implémentés les scènes seulement imaginées. Nous avions fini la lecture des biographies des Champions, Don Morleone, Enma, Zazel, Laure et Marge, Lady Perpetua et venons de recevoir **la biographie complète de McKraken**. Reprenons son analyse, puis poursuivons le travail sur Agent X, Soranaki et les scènes du Temple Céleste. Respecte les noms français et demande confirmation avant de figer des choix que la bible indique comme « proposés ». »

*Fin du dossier de transmission — établi à partir de la conversation jusqu'au 20 octobre 2026. Il synthétise les informations utilisateur et les idées émises par l'assistant ; il ne vérifie pas en direct les tout derniers commits du dépôt.*
