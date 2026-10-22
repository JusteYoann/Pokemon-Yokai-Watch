# POKÉMON ROUGE FEU × YO-KAI WATCH
## Mission Codex — Audit final, corrections, équilibrage EXP et validation de bout en bout

**Version 1.1 — Statut : cahier des charges de recette finale avant publication, comprenant l’audit complet des animations des capacités.**

### But
Le jeu est censé être presque terminé. Ta mission n'est **pas** de repartir de zéro : inspecte le dépôt actuel, identifie les problèmes, corrige les défauts techniques et visuels, implémente le **Multi Exp. permanent**, ajuste modérément la progression EXP, puis **teste autant que réellement possible une partie complète**, du lancement au postgame. Je veux un verdict étayé, pas une simple compilation verte ni un « tout fonctionne » sans démonstration.

**Projet :** dépôt `JusteYoann/Pokemon-Yokai-Watch` — adaptation de Pokémon Rouge Feu en Pokémon × Yo-kai Watch, 151 Yo-kai.

**Documents à consulter dans le dépôt s'ils s'y trouvent :** le Pokédex 151 et les tables types/stats/attaques/évolutions ; `NOMS_CANONIQUES_151_YOKAI_CODEX.csv`, `CORRECTION_NOMS_YOKAI_CODEX.md`, `REPARTITION_YOKAI_VALIDEE_CODEX.md`, `SYNTHESE_EQUIPES_BOSS_YOKAI_WATCH_CODEX.md`, `CAMEOS_YOKAI_WATCH_CODEX.md`, `PERSONNAGES_PRINCIPAUX_YOKAI_WATCH_CODEX.md`, `ADAPTATION_DIALOGUES_YOKAI_WATCH_CODEX.md`, `SHINY_YOKAI_REFERENCES_CODEX.md`, et le dossier `VISUELS_FINAUX_YOKAI_WATCH` s'il existe. Utilise les noms et chemins réels présents dans le dépôt : **ne suppose pas qu'un document absent a déjà été intégré.** Les choix les plus récents explicitement validés priment sur les propositions historiques ; en cas de contradiction, signale-la.

---

## 0 — Méthode de travail et exigences de preuve

1. Établis un **inventaire de l'état actuel** (branche, commit, build, sous-systèmes, assets effectivement référencés). Fais d'abord compiler le projet sans toucher inutilement au gameplay.
2. Travaille sur une **branche ou des commits identifiables** afin que toutes les corrections restent traçables et réversibles.
3. Procède par cycles : **constat → reproduction → correctif minimal → compilation → test ciblé → régression**.
4. Tu peux corriger directement les bugs, les déplacements de sprites, les erreurs de données, les textes fautifs, les blocages de scripts et les problèmes techniques qui ne changent pas nos décisions créatives. **Ne change pas silencieusement** les espèces, boss, teams validées, lieux des Pokémon/Yokai spéciaux, noms canoniques, couleurs shiny validées, récompenses importantes ou événements scénaristiques. Soumets toute refonte majeure ou arbitrage créatif avant application.
5. Ne confonds jamais : **audit de fichiers**, **compilation**, **test automatisé**, **démarrage en émulateur**, **partie complète réellement jouée**. Documente exactement ce qui a été fait et les limites de l'environnement.
6. Si tu peux utiliser un émulateur GBA (par exemple mGBA et ses possibilités d'automatisation/scripting), installe/configure ou exploite celui qui est déjà disponible si autorisé, et exécute de vrais scénarios de jeu. Si l'environnement ne permet pas une partie réelle de bout en bout, **dis-le explicitement** et compense par des validations statiques, tests automatisés et captures réelles quand c'est possible. **N'invente ni session de jeu, ni capture, ni verdict.**
7. Sauvegarde les rapports de QA et preuves dans un dossier du dépôt, proposé : `QA_RECETTE_FINALE/` ; conserve intact le dossier de bibliothèque de visuels finaux si déjà constitué.

---

## 1 — Vérification de tous les sprites : priorité critique

### 1.1 Exhaustivité, liens et rendu
- Recense les **151 espèces** et vérifie leur sprite de face, sprite de dos, leur(s) palette(s), leur icône et leurs éventuelles variantes réellement utilisées.
- Vérifie que le moteur charge le bon visuel pour la bonne espèce, sans inversion de numéros, graphique manquant, sprite corrompu, palette croisée, compression incorrecte, bord parasite, clignotement, transparence défectueuse ou crash.
- Vérifie aussi les sprites de Yo-kai **statiques sur la carte**, les cadeaux, les rencontres scénarisées, et tous les sprites ajoutés pour PNJ, événements et caméos.
- Contrôle les positions et dimensions **en émulateur, au moins sur des échantillons représentatifs ; idéalement pour les 151 espèces via un banc de capture automatisé**. Une simple validation PNG ne suffit pas à confirmer le placement dans le moteur.

### 1.2 Taille visuelle et centrage en combat
- Vérifie chaque sprite en condition réelle : **pas trop petit, pas coupé, pas trop haut/bas, ni décentré**, bon ancrage au sol / en l'air selon son design, cohérence face/dos et avec l'interface.
- Contrôle les tailles **par famille d'évolution** : une évolution destinée à être plus grande, complexe ou impressionnante ne doit pas sembler paradoxalement plus petite ou moins lisible que sa sous-évolution, sauf choix artistique manifestement intentionnel.
- Les Yo-kai massifs, légendaires et boss doivent **avoir de la présence visuelle**. Évite qu'un Yo-kai imposant paraisse minuscule face à une créature normalement petite.
- Respecte les limites de sprites/palettes/VRAM du moteur. Utilise les ajustements adaptés (canevas, coordonnées/offset, centrage, échelle pixel art en nearest-neighbor si techniquement nécessaire) et **évite toute déformation ou flou**.
- Le front et le back doivent être convaincants : les backs ne doivent pas être minuscules, hors cadre ni masquer anormalement les jauges.

### 1.3 Éléments de preuve
- Produis une **planche-contact des 151 sprites de face**, une des 151 sprites de dos, une des icônes, et si possible des **captures de combats rendues dans l'émulateur** montrant les corrections de taille/position.
- Fournis dans `QA_RECETTE_FINALE/SPRITES_AUDIT.csv` une ligne par espèce (#, nom canonique, front OK, back OK, icône OK, shiny OK, placement OK, taille relative OK, remarque, correctif), ainsi qu'un petit rapport des cas retouchés.
- Vérifie également graphismes de héros, vélos, surf, pêche, marche/course, dresseurs et caméos (sprite de combat et overworld) dans chaque direction/animation réellement utilisée.

---

## 1 bis — Audit COMPLET des animations des capacités (priorité critique)

**Je souhaite vérifier non seulement que chaque attaque produit le bon effet de gameplay, mais aussi que son animation fonctionne réellement sur les nouveaux sprites Yo-kai.** Comme les 151 sprites ont été remplacés, il faut détecter les animations du moteur Rouge Feu qui utilisent les dimensions, palettes, masques ou silhouettes du combattant.

### 1 bis.1 Tous les mouvements réellement disponibles dans le hack
- Dresse l'inventaire de **toutes les capacités effectivement présentes et utilisables** via apprentissage, CT/CS, tuteurs, boss, cadeaux ou événements. Si le jeu expose aussi des capacités jamais apprises, signale-les séparément : ne prétends pas les avoir testées.
- Pour **chaque capacité jouable**, vérifie : lancement, ciblage, synchronisation animation/son, graphiques et couleurs, résultat visuel, dégâts/soin/statuts/bonus, fin de l'animation et retour normal à l'interface. Inclure capacités offensives, statuts, multi-coups, météo, changements de forme/effets si présents, attaques sans impact direct, échecs, immunités, K.O., coups critiques et variantes pertinentes.
- Contrôle les **animations du Pokémon actif et de l'adversaire** : sprite de dos du joueur et sprite de face adverse ; tests contre des sprites petits, grands, très larges, allongés, flottants et asymétriques, plus shiny lorsque pertinent.
- Contrôle aussi les CT/CS et les animations de capacités utilisées hors combat si le jeu en a.

### 1 bis.2 Cas prioritaire : voile / texture métallique prenant la forme du Yo-kai
- **Exemple explicite du rendu qui m'inquiète :** certaines animations de type **Acier** appliquent un **voile / une texture métallique suivant exactement la silhouette du Pokémon**. Après les remplacements graphiques, confirme que cet effet épouse la **silhouette du Yo-kai actuel**, et non celle de l'ancien Pokémon, un rectangle, l'ancien masque, une forme décalée ou une silhouette coupée.
- Vérifie le **masquage, la transparence, les palettes, la composition des couches, la priorité d'affichage, les coordonnées et la durée de l'effet**. Vérifie qu'aucun pixel parasite, ancien contour, flicker, décalage ou corruption de palette ne reste visible pendant ou après l'attaque.
- Répète les essais avec plusieurs **formes très différentes**, devant et derrière, **normales et shiny** (notamment grands Yo-kai et modèles avec excroissances, accessoires, cornes ou flammes). Si le moteur calcule l'effet directement à partir du sprite, démontre-le avec une inspection technique ET une capture sur émulateur.
- Étends la recherche à **toute animation utilisant une silhouette, un masque, une recoloration temporaire, un clignotement, une texture, une déformation, un déplacement ou une superposition liée au sprite** — et pas seulement aux attaques Acier.
- Ne retire **pas** une animation d'origine pour masquer le problème : corrige le mécanisme graphique, les offsets, les palettes ou les ressources nécessaires, en préservant la qualité visuelle prévue et la compatibilité GBA.

### 1 bis.3 Méthode de vérification et preuves
- Fais d'abord un **audit du code des scripts d'animation**, des ressources graphiques, des callbacks, des offsets de sprites et des contraintes mémoire/palettes pour repérer les attaques dépendantes de la silhouette.
- **Teste les capacités réellement en émulateur**, idéalement via un banc d'essai reproductible pouvant forcer un combat, sélectionner une espèce et déclencher une capacité. Si une automatisation exhaustive est possible, parcours toutes les capacités jouables ; pour les effets liés aux silhouettes, teste une matrice représentative d'espèces/formes, puis les cas extrêmes. Signale clairement ce qui n'a pas été testé visuellement : un audit de code ne vaut pas validation visuelle.
- Produis des **captures comparables** (avant / pendant / après l'animation), ou de courts enregistrements si faisable, pour les effets complexes et au minimum pour l'effet métallique suivant la silhouette.
- Crée `QA_RECETTE_FINALE/ANIMATIONS_ATTAQUES_AUDIT.csv` : ID/nom de la capacité, source d'apprentissage, type d'animation, dépendance au sprite/masque, cible, front/back, normal/shiny testé, test statique, test émulateur, résultat, défaut, correction, référence de preuve, état **VALIDÉ / ÉCHEC / NON TESTÉ**.
- Ajoute `QA_RECETTE_FINALE/ANIMATIONS_ATTAQUES_RAPPORT.md` : nombre total de capacités présentes, testées visuellement, couvertes uniquement statiquement, erreurs relevées, correctifs, captures et **liste exacte des animations non vérifiées**.
- Pour toute capacité déclarée **VALIDÉE**, une preuve ou une procédure reproductible doit exister. **Aucune validation globale « toutes les animations marchent » sans couverture réelle.**

---

## 2 — Shiny : présence, absence et cohérence des familles

Source de vérité : **dernière version de `SHINY_YOKAI_REFERENCES_CODEX.md` et archive de références correspondante**, après retrait/exclusion de Kappacap et Noko selon les consignes validées.

- **Seules les familles évolutives représentées par une référence conservée dans le ZIP** doivent avoir une **apparence shiny distincte**, sauf exceptions explicitement approuvées dans le cahier des charges. Si une forme est référencée, harmonise ses autres stades avec elle.
- Une famille **sans référence conservée** n'a **pas de shiny visuellement différent** : ses palettes shiny doivent **reproduire l'apparence normale**. Il ne s'agit **pas** de désactiver la probabilité, le statut shiny, les étoiles ou la capture d'un shiny ; seul le **visuel alternatif** disparaît.
- Pour Kappacap et Noko, ignore leurs anciennes références : si une autre forme de leur famille possède une référence conservée, dérive la palette de cette forme selon les règles ; sinon aucune apparence distincte.
- Contrôle les cas approuvés : Robonyan/Robonyan F dorés, Robonyan 28 noir + or + cornes ; Usapyon au regard d'Emperor sans grosse recoloration ; Coach Antonic en tenue de plage ; Jojojoyeux en costume sans confettis ; Brumella noir/blanc sans robe ; Télémir et Triptic-tac en **couleurs uniquement** ; Couchtar couleurs + sourire ; les lignes Komasan et Loubarbare/Racaïd cohérentes. Inspecte les autres règles détaillées du document.
- Teste les rencontres et le rendu shiny, les dos et les portraits/icônes si les variantes sont prises en charge. Attention à l'application des palettes shiny dans l'affichage de combats et Pokédex.
- Vérifie que les shiny restent obtenables via **la mécanique de rencontre prévue**, avec un taux cohérent avec le projet. Utilise si nécessaire un **mode test temporaire non livré** pour forcer l'affichage shiny ; **supprime-le de la version finale**.
- Produis `QA_RECETTE_FINALE/SHINY_AUDIT.csv` : numéro, nom, famille, référence retenue oui/non, shiny distinct oui/non, contrôle visuel, remarques et preuves.

---

## 3 — Gameplay : toute l'aventure doit marcher

### 3.1 Progression complète
Vérifie du début (sélection garçon/fille, maison, laboratoire, premier rival) jusqu'au Conseil 4, au Champion, au Hall of Fame, au postgame et à tous les événements exclusifs du hack :
- démarrage, scripts d'introduction, dialogues, sauvegarde/chargement, transitions ;
- progression des 8 arènes, badges, objets-clés, niveaux et conditions de déblocage ;
- Team Rocket, repaires et Sylphe SARL ;
- événements du rival, lieux, ordre, équipes évolutives, accès aux combats ;
- Conseil 4, Champion et suite postgame, Îles Sevii, PNJ/admins Rocket supplémentaires, Dojo et rencontres statiques ;
- caméos, dialogues **Oui/Non** et refus sans lancement de combat, récompenses, revanches, prérequis, combats des employés/Mafiamille, Seigneur Enma et son déblocage de la rencontre Enma dans la Grotte Azurée ;
- absence de softlocks, objets essentiels introuvables, téléportations incorrectes, flag déjà utilisé, mauvais personnage ou dialogues d'une autre variante.

### 3.2 Protagonistes et rival
- **Red remplacé par Nathan**, **Leaf par Katie**, **Blue par Matt** ; cohérence des sprites partout (intro, overworld, course, vélo, pêche, surf, combat, carte dresseur, Hall of Fame selon disponibilité).
- Le joueur peut personnaliser **son propre prénom** ; le rival doit **toujours s'appeler Matt**, sans invite de renommage.
- Vérifie les variantes des caméos : héros Nathan → Katie + Nathaniel ; héroïne Katie → Nathan + Michael.
- Les **huit combats du rival** doivent suivre les choix validés ; ne réintroduis pas un Yo-kai absent du roster final de son équipe (p. ex. ne fais pas réapparaître Cigallard après sa disparition scénaristique). Ses évolutions finales doivent respecter la progression prévue, notamment Camaïeul dévoilé au Champion.

### 3.3 Dialogues
- Tous les textes affichés doivent utiliser les noms canoniques (en particulier **Saumhonni n°012**, **Sergent Rampant n°098**, **Matt**, etc.) et une terminologie Yo-kai naturelle.
- Corrige les incohérences de noms de Pokémon présents dans les scènes, sans casser les codes de contrôle ni les lignes d'affichage.
- **Conserve Kanto** et les noms des villes de Rouge Feu.

---

## 4 — Tous les 151 Yo-kai obtenables sur UNE sauvegarde

**Exigence absolue :** un joueur doit pouvoir posséder ou enregistrer **les 151 Yo-kai dans une seule partie**, sans échange avec une autre cartouche, sans événement externe, sans code de triche et sans devoir redémarrer.

- Construis une **preuve d'obtention pour chacune des 151 espèces** depuis une sauvegarde unique : rencontre sauvage, évolution accessible, don, récompense de caméo, fossile, reproduction si le hack la gère, échange PNJ interne si prévu, rencontre statique, etc.
- Traite les difficultés habituelles : **les 3 familles de starters**, embranchements d'évolutions, pierres d'évolution en quantité suffisante ou renouvelables, espèces exclusives de version du jeu original, échanges/évolutions par échange, choix uniques de cadeaux/fossiles/dojo, objets indispensables ratables, Pokémon/Yo-kai uniquement accessibles après événements facultatifs.
- **Aucun choix irréversible ne doit empêcher le 100 %**. Si un cadeau propose deux espèces, les deux doivent rester accessibles plus tard sur la même sauvegarde.
- Vérifie la cohérence et les conditions des fixes spécifiques déjà définis (ex. Mademoaiselle au Mont Braise, Kyubi aux Îles Écume, Octorgone à la Centrale, Enma dans la Grotte Azurée après l'événement approprié), sans modifier leur rôle scénaristique.
- Assure-toi que chaque stade d'une ligne est enregistrable ; une famille avec une pierre rare ne doit pas être impossible à compléter.
- Produis `QA_RECETTE_FINALE/OBTENTION_151.csv` : numéro/nom, méthode(s), lieu, prérequis, disponibilité avant/après Ligue, méthode renouvelable si nécessaire, éventuel verrou, **preuve de faisabilité sur la même sauvegarde**, statut. Relever les risques avant toute modification significative du placement des espèces.
- Ne te contente pas de compter 151 entrées définies dans le code : **prouve l'obtention réelle** par les chemins du gameplay.

---

## 5 — NOUVELLE FONCTIONNALITÉ À IMPLÉMENTER : MULTI EXP. PERMANENT

Je souhaite un fonctionnement comparable au **Multi Exp. moderne, activé par défaut**, pour tous les combats donnant normalement de l'expérience :

- Tout **Yo-kai vivant et éligible dans l'équipe** reçoit automatiquement de l'EXP, **même sans participer au combat** ; **aucun objet à équiper ni activation manuelle**.
- **Référence de départ à tester** : le Yo-kai participant reçoit 100 % de sa part normale d'EXP et les membres non participants reçoivent chacun environ **50 % de cette part**, sans soustraire leur gain à celui du participant (logique moderne). Ajuste proprement si le moteur, les doubles ou l'équilibrage nécessitent une implémentation légèrement différente, en documentant exactement la formule.
- Précise le comportement des Pokémon/Yo-kai ayant participé à un même combat, des doubles, des changements, des Yo-kai K.O., des œufs, du niveau 100 et des objets **Multi Exp.** hérités du jeu original : **évite les doubles versements involontaires** et les exploits.
- Vérifie la distribution et les affichages d'EXP/gains de niveau, effets d'apprentissage d'attaques, évolutions, limites de niveau, sauvegarde/chargement, et la robustesse avec 1 à 6 membres.
- Conserve des animations/messages fluides et lisibles ; si le fonctionnement moderne réclame des fenêtres de niveau/attaques répétées, veille à ne pas casser le combat ni le rythme.
- Ne distribue aucune EXP pour un combat qui n'est pas censé en donner. Ne change pas les conditions de montée de niveau hors de ce qui est nécessaire à cette mécanique.
- Ajoute une série de tests reproductibles `QA_RECETTE_FINALE/EXP_MULTI_TESTS.md` avec calculs de gains attendus vs observés pour différents types de combats.

---

## 6 — Ajustement LÉGER de l'EXP et courbe de niveau

Je veux pouvoir avancer dans **toute l'histoire et le postgame**, en affrontant les dresseurs accessibles et en participant aux événements, **sans sessions de farming obligatoire**.

**Objectif de confort :** la montée vers **les niveaux 60–70** doit être naturelle **en fin de parcours / postgame** pour une équipe habituelle d'environ 6 Yo-kai ; la Ligue et les dernières zones doivent rester intéressantes et demander une stratégie, pas devenir triviales.

- Commence par évaluer le rythme d'EXP **avec le nouveau Multi Exp.**, qui augmente déjà sensiblement la progression. **N'applique pas aveuglément un multiplicateur en plus.**
- Simule et si possible joue un parcours représentatif : 6 Yo-kai, pas de farm de sauvages, combats des dresseurs normalement rencontrés, principaux détours et événements. Note le niveau de l'équipe avant les 8 badges, avant le Conseil 4, à l'entrée du postgame et après les principales quêtes finales.
- Si l'expérience est encore insuffisante, ajuste **modérément** la formule globale, le rendement de certaines classes de combats ou dresseurs, ou des récompenses EXP. Par exemple, évalue une hausse **indicative** de 10–25 % seulement si les tests montrent qu'elle est nécessaire ; ce n'est **pas** une valeur imposée.
- Attention : avec cinq réservistes recevant chacun de l'EXP supplémentaire, une hausse globale trop forte peut créer du **sur-leveling** dès les premières arènes.
- Vérifie toutes les catégories de combats, le niveau des boss et de leurs équipes, les courbes de croissance des espèces, les Pokémon/Yo-kai puissants et la difficulté des arènes 1 à 8, du Conseil 4, du Champion et des super-boss postgame.
- Préserve les niveaux, les identités et la composition des **équipes de boss validées**, sauf nécessité technique clairement démontrée et soumise à validation. L'équilibrage doit privilégier le système EXP et des correctifs limités avant de modifier ces choix.
- Fournis un tableau `QA_RECETTE_FINALE/PROGRESSION_NIVEAUX.csv` comparant **avant / après** par jalon, avec hypothèses explicites (équipe choisie, combats affrontés, activités facultatives réalisées, nombre de K.O., absence de farm).

---

## 7 — CT / CS, capacités et blocages de progression

- Audit complet de toutes les **CT et CS** : obtention dans la progression, objets correctement remis, description/numéro/nom, enseignement compatible avec les Yo-kai, moves corrects en combat, puissance, PP, type, catégorie selon moteur, animations et effets.
- Vérifie qu'il existe des Yo-kai **obtenables à temps** pouvant utiliser chaque CS nécessaire : Coupe, Surf, Force, Flash selon route, Vol, Éclate-Roc et Cascade selon progression et moteur ; vérifie aussi les badges et leurs conditions.
- Contrôle qu'un joueur avec un des trois starters et un recrutement raisonnable peut avancer **sans être bloqué faute de porteur de CS**.
- Vérifie les éventuels changements d'espèces, de types et de learnsets qui ont rendu des CT/CS impossibles ou incohérentes ; corrige uniquement les incompatibilités clairement nécessaires et documente-les.
- Audite les évolutions naturelles, par pierre, par échange modifié, les apprentissages de capacités en montant de niveau et les capacités apprises au moment de l'évolution. Attention aux limites de longueur des noms et aux commandes de texte.
- Aucun boss ne doit posséder une capacité ou un talent invalide pour l'état technique actuel du projet.

---

## 8 — Équilibrage, stabilité et qualité générale

Vérifie aussi :

**Combat :** attaques, talents, immunités, résistances, statuts, priorités, précision, critique, changements, objets tenus, IA des dresseurs, récompenses, transitions, musiques, écran de capture, Pokédex, élevage/reproduction si présents ; équilibrage raisonnable des trois starters sur toute l'aventure.

**Interface :** menus, liste d'équipe, boîtes PC, noms de Yo-kai, icônes, statuts, sprites shinys, détails Pokédex, textes longs et caractères accentués, affichage des objets et cadeaux.

**Carte :** collisions, transitions, portes, téléportations, routes, accès aux arènes, grottes, îles, sprites overworld, PNJ bloquants, drapeaux d'événements, respawn éventuel, musique et palettes.

**Sauvegarde :** nouvelle partie, chargement, multiples états de progression, cadeaux, captures, shiny, évolutions, victoire de Ligue, champion, drapeaux postgame, reprise d'une sauvegarde créée avant correction si pertinent.

**Robustesse :** pas de crash, freeze, boucle de dialogue, erreur de script, softlock, sprite absent, corruption de mémoire/palette, inconsistance entre combats et overworld ; vérifier sur build propre et en émulation.

**Qualité des dialogues :** aucune référence incohérente à Pokémon comme créatures à la place des Yo-kai, noms canoniques, Matt fixe, Kanto conservé, options Oui/Non qui fonctionnent.

**Difficulté :** pas d'arènes faciles uniquement parce que le Multi Exp. suralimente l'équipe ; progression agréable sans aller-retour de farming ; super-boss réellement exigeants, mais possibles avec le niveau normalement atteint.

---

## 9 — Parcours de validation obligatoire

Je veux **deux niveaux distincts de validation**, avec preuves.

### A. Validation technique / automatisée
- Compilation propre après chaque bloc, puis compilation finale.
- Tests statiques de cohérence de données : 151 espèces, sprites, palettes, noms, talents, stats, CT/CS, items d'évolution, compositions des boss, tables de rencontre, flags, cadeaux, shiny.
- Scénarios reproductibles de combats, XP, évolutions et déclenchements d'événements.
- Validation graphique par planches-contact, plus rendus émulateur dès que possible.
- Registre de toutes les erreurs détectées/résolues et des points non testables.

### B. Véritable recette de jeu (émulateur)
**Si ton environnement le permet**, lance le ROM construit et réalise une **partie de vérification de bout en bout**, à la main, via script d'émulateur ou des scénarios assistés :
1. Démarrage de Nathan, choix du starter, Matt et premières routes.
2. 8 badges et tous les événements nécessaires à leur obtention.
3. Conseil 4, Champion, séquences de fin et déblocage du postgame.
4. Îles Sevii, rencontres spéciales, cadeaux, caméos et leurs revanches, progression vers Enma.
5. Recommence les **chemins différents** essentiels sur une sauvegarde séparée (Katie, variantes de caméos, autres starters), sans prétendre que cela démontre l'obtention des 151 sur la sauvegarde unique principale.
6. Mesure la progression de niveau et de difficulté en cours de partie.
7. Démonte les cas limites : refus d'un combat facultatif, récompense prise, événement rejoué/non rejoué, capture d'un Yo-kai unique, chargement après sauvegarde, équipe pleine, PC rempli si possible, inventaire et pierres limitées.

**Ne marque « partie complète validée » que si un parcours complet a réellement été exécuté dans l'émulateur.** Sinon indique précisément les zones non parcourues et les méthodes alternatives utilisées. Ne prétends jamais avoir « tout joué » après une simple lecture du code.

---

## 10 — Livrables à ajouter au dépôt

Crée `QA_RECETTE_FINALE/` (ou chemin équivalent explicite) et remplis au minimum :

1. `README.md` : périmètre, commit testé, méthode, commandes de build/test et statut global.
2. `SPRITES_AUDIT.csv` : audit individuel des 151 sprites, dos, icônes et placements.
3. `SHINY_AUDIT.csv` : audit des familles, références retenues et absence d'alternatives non voulues.
4. `OBTENTION_151.csv` : preuve de l'obtention de chaque Yo-kai **sur une sauvegarde**.
5. `EXP_MULTI_TESTS.md` : mécanique implémentée, formule, cas limites, tests et résultats.
6. `PROGRESSION_NIVEAUX.csv` : niveaux de l'équipe à chaque jalon, comparatif avant/après et hypothèses.
7. `CT_CS_EVOLUTIONS.md` : contrôle et anomalies CT/CS, attaques et évolutions.
   **Et obligatoirement :** `ANIMATIONS_ATTAQUES_AUDIT.csv` et `ANIMATIONS_ATTAQUES_RAPPORT.md` pour l’examen exhaustif des capacités, des masques, des effets de silhouette et des rendus en combat.
8. `PARCOURS_TESTS.md` : zones et événements réellement testés en émulateur, preuves, save states pertinents si utilisables, cases non testées.
9. `BUGS_ET_CORRECTIONS.md` : priorité (bloquant / majeur / mineur), reproduction, fichiers touchés, résolution, preuve.
10. `VERDICT_FINAL.md` : verdict explicite **PRÊT / PRÊT AVEC RÉSERVES / NON PRÊT**, nombre de tests réussis/échoués/non réalisés, bugs ouverts, liste précise des points bloquants.
11. Des **captures ou planches-contact** accessibles et versionnables si elles sont raisonnablement petites ; ne surcharge pas le dépôt en ROM, savestates gigantesques ou captures redondantes. Ne livre pas d'artefacts commerciaux propriétaires ni de ROM de jeu originelle dans les rapports.

Ajoute, si pertinent, scripts de test réutilisables dans un sous-dossier `QA_RECETTE_FINALE/scripts/`. Les fichiers CSV doivent comporter des **résultats vérifiables**, et non des « OK » supposés sans contrôle.

---

## 11 — Règles de priorité pour terminer le jeu

**Ordre souhaité :**

1. Audit initial, risques bloquants et build.
2. Réparation des erreurs de scripts/progression et des incohérences d'obtention à 100 %.
3. Vérification et corrections graphiques, proportion et centrage (toutes les espèces + personnages).
4. Audit de **toutes les animations de capacités**, notamment masques et voiles métalliques prenant la silhouette du Yo-kai, puis vérification shiny selon la liste des familles autorisées.
5. Implémentation et tests du Multi Exp. permanent.
6. Calibration du gain d'EXP **à partir de tests**, sans sur-leveling.
7. Vérification CT/CS, **animations d’attaques**, équilibrage et tests de régression.
8. Partie de validation en émulateur et second parcours ciblé si possible.
9. Rapport final et commits traçables.

Tu peux réordonner ponctuellement en fonction des dépendances techniques, mais évite de valider des sprites ou des combats avant les correctifs susceptibles de les casser.

**Conclusion demandée :** à la fin, je veux savoir précisément **si le jeu est vraiment prêt à être considéré comme terminé**, ce qui a été réparé, ce qui reste non vérifié, et comment je peux moi-même reproduire les tests importants.
