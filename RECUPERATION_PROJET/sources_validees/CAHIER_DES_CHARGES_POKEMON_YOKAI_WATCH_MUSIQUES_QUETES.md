# CAHIER DES CHARGES — Pokémon Rouge Feu × Yo-kai Watch
## Intégration musicale DPCM (20 OST candidates) + 10 quêtes + sprites + dialogues + recette

**Statut :** mandat d'implémentation conditionnel, à valider par les tests.  
**Projet :** `JusteYoann/Pokemon-Yokai-Watch`  
**Référence visuelle à fournir séparément :** image du personnage **Juste Yoann**. Ne pas inventer son apparence ni finaliser son sprite avant de la recevoir.

## 0 — Principes intangibles

1. Préserver toutes les modifications déjà produites, les 151 espèces Yo-kai, leurs statistiques/équilibrages validés, les équipes des boss, le gameplay, les événements, les musiques Pokémon préservées et les conditions de déblocage existantes. Inventorier branches et état du travail avant de commencer ; branche dédiée, commit(s) de sauvegarde et jalons distincts.
2. Ne pas écraser le travail local ou distant, ni supposer que `master` possède toutes les fonctionnalités. Repérer et réutiliser les fichiers de cahier des charges antérieurs, données des espèces, listes canoniques, sprites existants et scripts de cameos. Aucune fusion ou publication sur `master` sans instruction explicite.
3. Le but n'est pas d'obtenir seulement une compilation réussie, mais des événements accessibles, jouables, cohérents, des musiques déclenchées correctement, des dialogues fiables et des graphismes vérifiés dans mGBA.
4. Si une spécification demeure ambiguë (emplacements, équipes, récompenses), proposer une solution documentée sans inventer des modifications incompatibles avec les acquis ; solliciter validation pour les choix structurants.
5. Ne pas déposer dans GitHub public des MP3 ou des samples contenant des enregistrements protégés ni de ROM commerciale complète. La distribution publique de compositions, adaptations et personnages protégés peut nécessiter des autorisations, même via patch. Garder les sources audio et les versions de test dans un espace local privé, et préciser les conditions nécessaires à toute diffusion.

## 1 — Bande-son : méthode et politique de priorité

**Méthode choisie par le créateur : B**, audio échantillonné DPCM, testé à l'écoute et jugé nettement meilleur que le prototype de transcription MP3→MIDI qui était méconnaissable. L'atténuation de netteté évoquant le rendu GBA est voulue tant que mélodie, percussions et voix restent intelligibles. Paramètre de référence : **13 379 Hz**, à ajuster uniquement après comparatif motivé et validation. Ne pas relancer la méthode A automatiquement.

**Objectif : intégrer au maximum 20 OST**. Mesurer la ROM et l'espace utilisable, compresser et boucler intelligemment sans perdre les introductions essentielles, puis retirer les OST les moins prioritaires si nécessaire. **L'ordre ci-dessous décrit la sélection historique et non un ordre de sacrifice définitivement approuvé**. Avant toute suppression, produire un classement définitif à valider par le créateur ; les titres explicitement appréciés (*Somewhere A Bit Dodgy* et les thèmes du scientifique) ne doivent pas être sacrifiés automatiquement à cause de leur ancien numéro. Une fois l'ordre validé, retirer la dernière, puis la précédente, sans trous, si stockage, performance ou stabilité l'imposent. Ne pas faire de suppression arbitraire.

### 1.1 — Les 20 OST candidates et déclencheurs

| N° historique | Morceau / origine | Destination | Précisions |
|---|---|---|---|
| 1 | **Bicycle Theme** — YW1 | Vélo | Démarrer directement à la section énergique si approprié ; rétablir la musique de zone à la descente. |
| 2 | **Vs. Hinozall (English)** — Blasters | Combat **Domniscian** | Thème personnel ; préserver introduction et identité du chant si l'audio reste lisible. |
| 3 | **vs. The Ghoulfather** — YW3 | Combat **Don Morleone** | Thème personnel du boss. |
| 4 | **Infinite Tunnel** — YW2 | **Tour Pokémon, Lavanville** | Préférence du créateur par rapport à Terror Time ; comparer la transition avec les alentours. |
| 5 | **Enma Track** — Blasters | Dialogue/présentation d'Enma | Musique d'événement, pas à confondre avec son combat. |
| 6 | **Vs. Zazelmare** — Blasters | Combat d'Enma | Choix actuel candidat, comparer si nécessaire à *Final Battle – Are You Ready*. |
| 7 | **Nate's House** — YW1 | Maison du protagoniste Nathan | Respecter le personnage et les variantes liées au sexe du protagoniste. |
| 8 | **Katies House** — YW1 | Maison de Katie | Respecter le personnage et la logique de protagoniste. |
| 9 | **Blasters Hideout** — Blasters | Zone/base d'entraînement de **Coach Antonic** | Entrée, exploration et retour après combat. Comparer *Blasters Basecamp* seulement si besoin. |
| 10 | **Yo-kai Watch Blasters! Theme** — Blasters | Combat Coach Antonic | Si l'écoute démontre que ce n'est pas un bon thème de combat, proposer une piste alternative sans remplacer tacitement. |
| 11 | **Bada-Bing Tower** — YW3 | Sylphe SARL occupée par la Team Rocket | Ne pas changer la musique de lieux non visés partageant un même identifiant. |
| 12 | **Blossom Heights** — YW1 | Extérieur de Céladopole | Transition avec bâtiment/repaire. |
| 13 | **Enma Villa** — YW3 | Approche ou mise en scène d'Enma | À utiliser seulement si contexte et script le justifient ; ne pas imposer un troisième morceau sur un événement très court. |
| 14 | **Mount Wildwood in the Past** — YW2 | Bois Baies / forêt adaptée Sevii | Vérifier que le thème choisi surpasse le thème conservé / l'ancienne proposition Mystic Grove. |
| 15 | **Decisive Battle** — Sangokushi | Moment majeur de la Ligue / Conseil 4 | Conserver le thème Pokémon si meilleur. Ne pas toucher aux combats ordinaires de Matt. |
| 16 | **Harrisville** — YW2 | Île 2 ou localité rurale Sevii | Assigner précisément à la bonne carte. |
| 17 | **Somewhere A Bit Dodgy (BBQ)** — YW3 | Repaire Rocket de Céladopole | Association **validée positivement par le créateur** après écoute ; ne plus rejeter comme trop loufoque. |
| 18 | **Messenger from the Future ~ Robonyan Arrives** — YW2 | Dialogues du scientifique récurrent | Quatre rencontres ; jouer aussi après chaque combat avant retour à la ville, si logique moteur. |
| 19 | **Vs. Robonyan 3000** — Blasters | Quatre combats contre le scientifique | Robonyan → Robonyan → Robonyan 28 → Robonyan 28 shiny. |
| 20 | **Mini Boss Battle** — Sangokushi | Employés de Domniscian **et** Mafiamille | Un même thème pour les subordonnés ; bosses gardent leurs thèmes dédiés. |

### 1.2 — Comportements audio obligatoires

- Boucles musicales propres, sans silence ni clic, inspectées aux frontières, testées sur **au moins cinq itérations** ; vérifier en ROM, pas seulement dans un WAV d'aperçu. Une estimation statistique de répétition MP3 n'est pas une validation de boucle.
- Pour les combats importants, conserver **INTRO UNE FOIS → PARTIE PRINCIPALE → RÉPÉTITION DE LA PARTIE PRINCIPALE** si la structure réelle du morceau le permet. Ne pas supprimer une introduction pour économiser quelques kilo-octets sans arbitrage. Pour le vélo, démarrage direct à la section principale suivant l'expérience originale souhaitée.
- Transitions correctes dialogue → combat → dialogue/postcombat → thème de la carte ; éviter de relancer une musique à chaque boîte de dialogue, ou de conserver un thème spécial après sortie de zone.
- Audio compatible avec les effets sonores, les cris/sons de combat, les animations et la sauvegarde ; contrôler la charge CPU et la disponibilité des canaux voix.
- Le thème original Pokémon des combats **ordinaires contre Matt** est conservé. Variation pour son combat final : **projet distinct**, ne pas l'inventer dans cette mission. Plateau Indigo : **majestueux, solennel, prestigieux** ; ne remplacer l'original que si meilleur choix avéré, et ne pas engager une nouvelle composition hors de la liste sans aval.
- Séparer les modifications de scripts de déclenchement locaux des identifiants partagés pour éviter les remplacements involontaires dans d'autres cartes.

### 1.3 — Contraintes et preuves

Produire les tailles de fichiers réellement encodés (et non les seules extrapolations), taille ROM avant/après, espace réellement disponible, capacité et marge conservées ; démontrer si 20, 19, ... sont viables. Ne pas affirmer qu'une ROM est jouable juste parce qu'elle compile. En cas d'impossibilité technique d'une boucle DPCM, rendre compte honnêtement et proposer une solution compatible plutôt qu'un raccord audible déclaré « validé ».

## 2 — Dix quêtes à implémenter

Toutes les quêtes ont dialogues d'introduction, étapes, conditions de succès, contrôle des cas limites, récompense/retour, dialogue après succès, et état persistant dans la sauvegarde. Garder les Yo-kai, légendaires et personnages déjà existants ; **ne pas multiplier les apparitions incompatibles**. La distinction « amie avec » signifie possession/entrée reconnue par le jeu, sans retirer le Yo-kai au joueur ; préciser la logique exacte.

### Quête 1 — Professeur Chen, Médallium
Chen demande de compléter les **151 Yo-kai** du Médallium (remplaçant le Pokédex). Quête fil rouge, avec retour spécial une fois la collection complète et vérification sur une sauvegarde unique ; récompense éventuelle à proposer et valider. Ne pas introduire une 152e espèce.

### Quête 2 — Fan de Jibanyan
PNJ fan passionnée, exubérante mais attachante, souhaite voir **toutes les variantes de Jibanyan effectivement présentes dans les 151 espèces** (liste exacte à extraire du projet). Vérifier la collection sans retirer les créatures. Récompense garantie **Shogunyan shiny**, obtenu légalement, enregistré correctement et techniquement shiny (pas une nouvelle espèce). Si l'apparence de Shogunyan shiny n'est pas déjà validée, signaler la règle des références shiny et demander validation du visuel ; pas de recoloration inventée contredisant les directives existantes.

### Quête 3 — Le grand-père disparu
Une personne demande de retrouver son grand-père dans **une île Sevii** ; enquête courte, exploration, confrontation avec le grand-père, combat adapté au niveau de la zone, conclusion auprès du donneur de quête. Équipe et récompense à proposer selon les 151 et l'équilibrage ; non validées par défaut.

### Quête 4 — Le scientifique obstiné, quatre combats
Scientifique théâtral, prétentieux, susceptible ; rencontres successives dans des **villes différentes**, sans dépendance impossible ni doublons ; définir positions et prérequis. Combats : (1) Robonyan ; (2) Robonyan ; (3) Robonyan 28 ; (4) Robonyan 28 **shiny**, dernière étape idéalement postgame. Niveaux et moves progressifs ; forme chromatique non assimilée à un gain intrinsèque de puissance. Sa frustration évolue après chaque défaite. OST dialogue #18, OST combat #19 ; reprendre le thème de carte ensuite. S'assurer que la version shiny de Robonyan 28 respecte le design noir/doré et les cornes déjà validées.

### Quête 5 — Spécialiste des chromatiques
PNJ pédagogique présentant les shiny de façon accessible, et expliquant qu'ils peuvent être très rares ou visuellement identiques selon les familles / références approuvées. Demande de **présenter un Yo-kai shiny**, réalisable grâce au **Shogunyan shiny de la quête 2** ; autoriser tout autre véritable shiny éligible. Vérification d'état et récompense à définir, sans exiger une chasse aléatoire forcée.

### Quête 6 — Octorgone et Kyubi
PNJ passionné demande à rencontrer **Octorgone et Kyubi**. Ne pas déplacer leurs rencontres fixes validées : Octorgone à la **Centrale électrique**, Kyubi aux **Îles Écume**. Vérifier enregistrement/possession selon logique validée, pas de confiscation ni deuxième exemplaire requis.

### Quête 7 — Red, adversaire secret original Pokémon
PNJ énigmatique découvert dans un lieu isolé du postgame ; révélation qu'il s'agit de **Red**. Dialogues volontairement sobres, silence caractéristique. Il combat avec **de vrais Pokémon originaux** (équipe classique à définir et valider), **leurs vrais sprites, espèces, types, statistiques, attaques et capacités**, sans contaminer le bestiaire des 151 Yo-kai. Faire un audit technique de la faisabilité : espèces additionnelles ou représentation réservée au combat qui préserve la compatibilité des sauvegardes, des index et des données espèces. Ne pas simuler de faux Pokémon uniquement visuels ni écraser une espèce Yo-kai existante. Si cette architecture est risquée, isoler en phase distincte et demander autorisation avant refonte lourde. OST Pokémon originale adaptée à Red, pas une OST Yo-kai arbitraire.

### Quête 8 — Épreuve du Seigneur Enma
Enrichir **l'événement Enma déjà prévu**, ses dialogues, conditions et combats ; ne pas dupliquer l'événement. Enma est énergique, joueur, sûr de sa puissance, accessible et curieux des humains, capable de devenir sérieux au combat ; ni tyran froid ni monarque pompeux. Musiques : **Enma Track** (dialogue), **Vs. Zazelmare** (combat), **Enma Villa** seulement si séquence adéquate. Le déblocage de la rencontre statique légendaire d'Enma dans la **Grotte Azurée** après le combat cameo doit rester correct.

### Quête 9 — Juste Yoann, humour et revanche
Personnage cameo **Juste Yoann** : une première équipe volontairement troll/absurde ; autodérision et besoin comiquement excessif d'être préféré à **Nyleco**, présenté comme probablement meilleur en stratégie/Nuzlocke. Réplique-source à adapter naturellement : « Nyleco est probablement meilleur que moi en combat Yo-kai... Mais je reste le premier dans ton cœur, hein ? Je t'en supplie !! » ; ne pas dénigrer Nyleco. Après victoire, **revanche disponible à volonté**, avec une équipe *réellement stratégique* et une personnalité toujours drôle mais plus compétente. Niveaux/moves/équipes à concevoir et documenter, soumis à validation. **Sprite du personnage : image de référence fournie ultérieurement par le créateur ; attendre l'image avant de fixer l'apparence**. Produire un sprite overworld avec directions/animations nécessaires et un visuel de dresseur pour le combat. L'identité du cameo n'a pas besoin de faire une publicité intrusive.

### Quête 10 — Coach Antonic et les Blasters
Créer une vraie zone d'entraînement avec **Coach Antonic**, **Jibanyan**, **Komasan** et **Whisper** visibles sur la carte (sprites et courtes animations de mise en scène), chacun avec des lignes propres. Whisper est l'ancien chef **autoproclamé** des Blasters avant l'arrivée du Coach : en jouer pour l'humour. Coach Antonic : ton énergique, entraînement intense, ordres, encouragements ; transformer la défaite en leçon, pas en humiliation. Combat contre une équipe Blasters composée uniquement de Yo-kai réellement présents parmi les 151 et cohérents avec les personnages ; équipe définitive à valider. OST **Blasters Hideout** dans la zone, **Yo-kai Watch Blasters! Theme** au combat, retour à l'ambiance de base après victoire. **Usapyon ne figure pas comme accompagnateur dans cette scène** : le placer visiblement **auprès d'Ariane Célestin** lors de son propre cameo, en adaptant le script existant sans le dupliquer.

## 3 — Écriture et personnalités : une vraie direction dialoguée

- Avant de rédiger, documenter les personnalités des personnages officiels à partir de sources fiables (jeux, références officielles, sources secondaires clairement identifiées) et des indications explicites du créateur. Ne pas inventer comme canon ce qui n'est pas établi ; adapter le français et la cohérence avec la localisation française des noms.
- Exiger de **vraies scènes quand nécessaire** : entrée en matière, situation, motivation, répliques personnalisées, propositions de combat Oui/Non si pertinentes, réaction à la victoire/défaite, conclusion, et dialogues spécifiques après quête et lors des revisites. Aucune obligation artificielle de faire court, mais respecter le rythme et la capacité des fenêtres GBA.
- Chaque réaction **après combat** doit être propre au personnage : Enma enthousiaste et admiratif, Antonic tonitruant et pédagogue, scientifique frustré et évolutif, Domniscian fier/égocentrique et méta, Don Morleone autoritaire/théâtral, Juste Yoann dramatique mais autodérisoire, Red silencieux, fan de Jibanyan surexcitée, grand-père avec tempérament inventé cohérent.
- Respecter la distinction entre les dialogues conditionnels selon le personnage principal (**Nathan** ou **Katie**) et le rival **Matt** toujours nommé Matt, sans écran de nommage de rival. Localités Kanto **non renommées**. Ne pas remplacer arbitrairement les lignes canoniques de l'histoire principale sans intégrer les directives d'adaptation déjà existantes.
- Toutes les boîtes de dialogue doivent être relues dans le jeu : limites de largeur, sauts de ligne, ponctuation, accents, encodage, rythme, gestion des Oui/Non, textes quand le joueur revient après une défaite, après la victoire et après accomplissement.
- Produire un fichier séparé de **script narratif** pour validation et une table « personnage → tempérament → ton → scène d'intro → avant/après combat → revisite ».

## 4 — Sprites et cartes

- Inventorier les sprites existants et réutiliser les ressources valides. Créer uniquement les nouveaux sprites overworld, trainer front et animations réellement nécessaires. Style Pokémon Rouge Feu/GBA : palettes, proportions, orientations, ombrage et transparence cohérents ; tests in-game.
- Coach Antonic et ses trois accompagnateurs **Jibanyan, Komasan, Whisper** visibles et positionnés sans collisions, petites réactions aux dialogues et au combat ; **Usapyon auprès d'Ariane**.
- Scientifique récurrent : sprite cohérent à chacune des quatre apparitions, éventuelles poses/émotions si faisable, sans duplications d'état absurdes après progression.
- Red : sprite fidèle à son rôle et combat techniquement distinct.
- **Juste Yoann : impérativement consulter l'image de référence que le créateur joindra à Codex ; ne jamais inventer son visage, coiffure ou tenue si elle manque.** Fournir un aperçu de sprite pour approbation avant intégration définitive.
- Les nouveaux PNJ doivent apparaître/disparaître correctement selon les flags de quête, fonctionner avec toutes les directions d'interaction et être accessibles sans softlock.

## 5 — Phasage recommandé, sans pertes de données

1. **Audit préparatoire** : versions/branches, compilabilité, ressources, inventaire des 20 fichiers, tailles et marges ROM, événements existants à préserver, dépendances.
2. **Design document** : emplacement de chaque quête, étapes exactes, flags/variables, équipes et récompenses à soumettre ; classement définitif de sacrifice musical pour validation (protéger les pistes explicitement validées), architecture du combat contre Red.
3. **Intégration audio** : DPCM, boucles, triggers, tests individuels et charge moteur ; réduire progressivement le nombre seulement selon classement approuvé.
4. **Quêtes / scripts / visuels** : implémenter par lots cohérents, avec checkpoints et preuves ; ne pas attendre le visuel de Juste Yoann pour travailler aux autres scènes, mais garder son sprite en attente de l'image.
5. **Recette finale** : tests de parcours depuis une sauvegarde neuve et des sauvegardes de progression, y compris avec Nathan/Katie, morts/défaites, manque de place dans l'équipe/boîte à réception de Shogunyan shiny, quête 5 accomplie avant ou après quête 2, retours post-combat, revanches et resets, flags et répétitions musicales. Vérifier tous les 151 Yo-kai obtenables et le postgame, sans simplement supposer leur faisabilité.

## 6 — Livrables et critères d'acceptation

- ROM de test **compilée localement et vérifiée**, sans fournir de ROM commerciale à la diffusion publique ; instructions de reproduction légale et patch distribué seulement avec autorisations appropriées.
- Rapport de taille et d'intégration des OST (piste, destination, échantillonnage, taille brute/finale, intro, loop start/end, nombre de répétitions testées, comportement après combat). Nombre effectif ≤20.
- Tableau des quêtes (localisation, prérequis, flags, récompenses, personnages, scripts, état de validation), et fichier de dialogues complets pour revue créative.
- Aperçus avant/après des nouveaux sprites, capture des événements de la carte et des écrans de combat ; notes des ressources manquantes.
- Journal de tests mGBA : audio, scripts, triggers, combat, sauvegarde/chargement, récurrence, softlocks, reprises après combat, compatibilité Nathan/Katie.
- Tableau transparent « TERMINE / PARTIEL / NON FAIT / BLOQUÉ », avec preuves ; ne pas déclarer l'intégration finale si les cartes, combats ou déclencheurs n'ont pas été réellement testés.

**Décision finale réservée au créateur :** validation des équipes des nouveaux PNJ, emplacements et récompenses encore ouverts ; approbation du sprite basé sur image de Juste Yoann ; classement musical définitif si limitation. Le créateur fournira cette image en pièce jointe au message Codex.
