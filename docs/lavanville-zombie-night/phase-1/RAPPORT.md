# Lavanville — audit et propositions, phase 1

**État : aucune intégration du chapitre.** Seuls ce dossier documentaire, ses outils et les prototypes ont été ajoutés. Les graphismes, équipes, dialogues et solutions techniques doivent être approuvés avant la phase 2. Aucun fichier du moteur, carte, combat, audio ou des 151 Yo-kai n'est modifié. Aucune nouvelle ROM compilée pour cette phase.

## Base et protection

Branche dédiée `feature/lavanville-zombie-night`, créée depuis `49535014b9c5fd6add06464fb32f9ea85ca69078`, dernière base locale et distante validée avec la correction de palette/position de Matt. Elle inclut la finale mentionnée au commit antérieur `cb97d4883`. Ni fusion, ni modification des autres branches. Branche audio `audio/integration-31-ost` conservée à `837bd1757`.

Les ROM existantes de cette base servent uniquement aux captures : publique **16 777 216 octets**, privée **31 658 395 octets** (30,192 Mio), marge jusqu'à 32 Mio **1 896 037 octets**. Ne pas confondre cette marge terminale avec un budget de placement déjà garanti : alignements, sections et zone réservée à l'audio doivent être revérifiés au linkage.

Références fournies : neuf artworks officiels, hachages dans [references-manifeste.json](references-manifeste.json). Zomgralos et sa seconde pose constituent **un seul personnage**. Originaux conservés localement dans `/workspace/artifacts/lavanville-phase1/references`, hors dépôt. Aucune licence de redistribution n'est présumée. Les deux références CraftPix ajoutées ensuite servent de guide de corpulence, sans extraction du pack ; l'accès au site des licences a échoué (proxy HTTP 403), aucune autorisation de réutilisation directe du pack n'a donc été établie. Les deux dernières planches fournies fixent le style **FRLG exclusivement**, pas RSE.

## Inventaire complet des cartes et événements

[Inventaire JSON](inventaire-cartes.json) : chaque objet, coordonnées, graphisme, script, flag, connexion, porte, événement de case et panneau des 23 cartes examinées. [Dépendances et lignes de code](dependances-code.json), [repères source cliquables](PREUVES-SOURCES.md). Les noms de labels historiques `Rocket` et `Giovanni` ne signifient pas que leurs graphismes ou équipes n'ont pas été remplacés par la Mafiamille : ces labels sont conservés dans le projet actuel.

| Carte | Objets | Portes/warps | Déclencheurs de cases | Affectation actuelle / action proposée |
|---|---:|---:|---:|---|
| Lavanville extérieur | 3 | 6 | 0 | Mystic Grove, soleil → Zombie Night, nuit/brume et quatre patrouilles |
| Maison 1 | 2 | 3 | 0 | Humaine et Yo-kai ; dialogue dépend de Fuji → occupation zombie |
| Maison 2 | 1 | 3 | 0 | Spécialiste surnoms → zombie non hostile, service préservé |
| Boutique | 4 | 3 | 0 | Marchand + clients → zombies, achats inchangés |
| Centre 1F | 5 | 4 | 0 | Soins + PNJ dont commérage postgame → personnel zombie, soins conservés |
| Centre 2F | 4 | 3 | 0 | Trois réceptionnistes, livreur Cadeau Mystère → habillages zombies, systèmes de liaison préservés |
| Maison de Fuji | 6 | 3 | 0 | Fuji, trois humains et deux Yo-kai → habitation infestée, retrait du don de Flûte |
| Tour 1F | 5 | 4 | 0 | PNJ ordinaires, pas de combat → zombies non obligatoires |
| Tour 2F | 2 | 2 | 2 | Matt + médium ; combat rival existant et explication Scope |
| Tour 3F | 4 | 2 | 0 | Trois Dresseurs, Corde Sortie |
| Tour 4F | 6 | 2 | 0 | Trois Dresseurs, trois objets |
| Tour 5F | 7 | 2 | 17 | Quatre Dresseurs, médium de repos, Pépite et Rune Purifiante |
| Tour 6F | 5 | 2 | 2 | Trois Dresseurs, deux objets ; barrière fantôme scénarisée à supprimer |
| Tour 7F | 4 | 1 | 0 | Trois sbires + Fuji → trois Dresseurs zombies + Alyzon |
| Arène Céladopole | 11 | 3 | 0 | Erika, sept Dresseurs, trois arbres Coupe → résidence avec Matt puis Alyzon |
| Casino Céladopole | 11 | 4 | 0 | Affiche, passage du repaire et sbire conservés ; ajouter condition badge |
| Repaire B1F | 8 | 6 | 0 | Cartes/équipes inchangées |
| Repaire B2F | 6 | 5 | 0 | Cartes/équipes inchangées |
| Repaire B3F | 6 | 2 | 0 | Cartes/équipes inchangées |
| Repaire B4F | 10 | 3 | 0 | Don et ses combats conservés ; objet Scope remplacé par obtention de Flûte |
| Safrania | 15 | 15 | 0 | Le déplacement du garde dépend encore du sauvetage de Fuji |
| Route 12 | 14 | 4 | 0 | Misterre dépend de `FLAG_GOT_POKE_FLUTE` |
| Route 16 | 10 | 5 | 0 | Même dépendance, rencontre séparée |

Extérieur : carte **24 × 20 cases**, entrées par Route 10 au nord, Route 8 à l'ouest et Route 12 au sud ; six portes conservées (Tour, Centre, maison de Fuji, deux maisons, boutique). Prévoir aussi Vol, Téléportation, sortie de combat/soins et chargement d'une sauvegarde. Les quatre panneaux incluent une annonce Scope devenue obsolète. Les événements de livres de la maison de Fuji nécessitent une adaptation, pas seulement le retrait de son objet personnage.

La Tour possède **13 médiums + 3 sbires = 16 placements de Dresseurs**, plus le combat de Matt (une des trois équipes selon le starter) et un combat fantôme scénarisé au 6F. Le plan garde les 16 placements, conserve le combat/les équipes de Matt et remplace le fantôme par un passage libre. La présence humaine de Matt au 2F entre toutefois en tension avec « aucun humain ordinaire » : proposition de conserver cette exception scénaristique, sans modifier son équipe ; à confirmer. Alyzon constitue le combat de badge déplacé de Céladopole, pas un neuvième Champion.

### Répartition proposée, non intégrée

| Étage | Emplacements existants → nouveau personnage |
|---|---|
| 3F | Patricia → Zombigo T ; Carly → Zombigo T ; Hope → Clochemar |
| 4F | Paula → Zombigo T ; Laurel → Clochemar ; Jody → Supermanager |
| 5F | Tammy → Zombigo T ; Ruth → Supermanager ; Karina → Clochemar ; Janae → Zomgralos |
| 6F | Angelica → Zomgralos ; Emilia → King Deadward ; Jennifer → Supermanager |
| 7F | sbire 19 → King Deadward ; sbire 20 → Zomgralos ; sbire 21 → Encore Dead ; Fuji → Alyzon |

Totaux : Zombigo T 4, Clochemar 3, Supermanager 3, Zomgralos 3, King Deadward 2, Encore Dead 1. Pas de nouveaux combats obligatoires ajoutés à ces emplacements. Conserver les portées d'approche existantes au départ ; les patrouilles répétables concernent les errants extérieurs, pas automatiquement les Dresseurs de la Tour. Ne pas modifier les tables d'équipes Mafiamille communes : de nouveaux enregistrements réservés à ces placements évitent d'altérer d'autres scènes et permettent de garder l'historique des flags de victoire.

## Scope, Fuji, Flûte et progression

### Scope : deux mécanismes distincts

`src/battle_setup.c`, `CheckSilphScopeInPokemonTower` : test des sept étages et de l'objet pour déclencher les combats fantômes des rencontres ordinaires. `StartWildBattle` l'appelle ; supprimer l'obligation nécessite de neutraliser ce test pour la Tour, pas de changer uniquement les dialogues.

`StartMarowakBattle` et les deux événements de cases de `PokemonTower_6F` créent un second verrou, dont le résultat repousse le joueur sans victoire. Retirer ces déclencheurs et leur dépendance de progression. Ne pas supprimer l'objet Scope, les fonctions génériques de fantôme ni les effets nécessaires à d'autres combats. Ne pas toucher à l'apparence ou au fonctionnement des rencontres Yo-kai existantes.

### Fuji : dépendance hors Lavanville

Le sommet cache Fuji, le fait réapparaître chez lui, positionne `FLAG_RESCUED_MR_FUJI`, puis ramène le joueur à sa maison. Tous ces appels doivent disparaître du nouveau sommet. La maison, ses livres, Maison 1, le Centre et les entrées du Mémorydex/Fame Checker contiennent aussi des références. Hors ville : photo du laboratoire de Cramois'Île, photo Auguste/Fuji et journal à Cramois'Île. Proposition : retirer les interactions de fiche Fuji devenues sans objet et réécrire leurs textes localement ; conserver les identifiants historiques dans la sauvegarde pour éviter de décaler d'autres données.

**Point critique :** `SaffronCity_OnTransition` et son garde utilisent encore `FLAG_RESCUED_MR_FUJI` pour libérer l'accès. Proposition de remplacer uniquement cette condition par `FLAG_GOT_POKE_FLUTE`, étape équivalente de progression après le repaire. Ne pas simplement laisser le flag Fuji éternellement faux. Autre solution possible : flag de chapitre indépendant, mais il faudrait en définir la migration. Aucune des deux n'est appliquée en phase 1.

### Badge et nouvelle résidence

Réutiliser `TRAINER_LEADER_ERIKA` (417), `FLAG_DEFEATED_ERIKA` (0x4B3) et `FLAG_BADGE04_GET` (0x823). Conserver `set_gym_trainers 4` et les effets du badge sur Force, obéissance et contrôle des huit badges. Les sept combats de l'ancienne Arène sont retirés de cette résidence ; ne pas les ajouter ailleurs arbitrairement. Proposition de masquer les trois arbres Coupe intérieurs devenus inutiles tout en gardant bâtiment/layout, à approuver.

Récompense CT19 et ses flags : proposition de les conserver avec Alyzon pour éviter une perte de récompense, même si la spécialité change ; ne pas inventer une nouvelle CT sans accord. Le parcours Fame Checker d'Erika doit être adapté explicitement. Avant le badge : Matt seul, aucun combat. Après : Alyzon, aucun rematch. Après Ligue : emplacement réservé à une future revanche, **aucune équipe ni combat activé** avant validation.

### Repaire et Flûte

L'affiche du Casino ouvre actuellement le passage sans test de badge (`FLAG_OPENED_ROCKET_HIDEOUT`). Il faut conditionner **l'ouverture et l'accès effectif** au badge 4 ; contrôler les anciennes sauvegardes dont le passage est déjà ouvert. Une sauvegarde déjà dans le repaire doit pouvoir ressortir, jamais être emprisonnée par la migration.

Au B4F, Don fait actuellement apparaître l'objet Scope. Proposition de réutiliser cette récompense au sol pour la Flûte, après Don, avec test de place, attribution réelle de `ITEM_POKE_FLUTE`, puis `FLAG_GOT_POKE_FLUTE`. Conserver les flags/objets déjà obtenus en ancienne sauvegarde ; si Don est déjà vaincu et la Flûte absente, rendre la récompense récupérable sans refaire ce combat. Ne pas lier naïvement son apparition à `FLAG_HIDE_SILPH_SCOPE`, déjà consommé sur certaines sauvegardes.

Les Misterre des Routes 12 et 16 sont bien `SPECIES_NIDORINO` (33), niveau 30 dans les scripts, et vérifient **le flag**, pas uniquement le sac. Conserver leurs rencontres, cries, animations, récompenses et flags individuels. La fonction de réveil de la Flûte et sa fanfare restent intactes.

Parcours proposé sans Scope : accès Lavanville → Tour → Alyzon/badge 4 → Céladopole/repaire/Don → Flûte et flag → routes 12/16. Le passage souterrain Route 8/Route 7 permet d'atteindre Céladopole sans dépendre de la Flûte. Ne pas imposer artificiellement l'ordre des trois premiers badges au-delà des conditions existantes.

## Nuit et brume : solution proposée

Réutiliser `WEATHER_FOG_HORIZONTAL` et ses ressources. **20 sprites météo de 64 × 64**, 2 048 octets de tuiles OBJ partagées, une palette OBJ météo ; aucun nouveau buffer d'image plein écran. Les pointeurs sont déjà présents dans l'union de `struct Weather`. La brume défile nativement d'un pixel toutes les quatre mises à jour. Proposition de ralentir uniquement à Lavanville à un pixel toutes les huit mises à jour ; conserver les autres météos. Alpha proposé léger, coefficients 4/16 au prototype, à ajuster à l'écran. Le moteur utilise du mélange matériel OBJ, pas une image translucide géante.

Appliquer la teinte bleu-violet via le chemin de chargement des palettes de terrain, avec un garde strict extérieur Lavanville. Gérer fonds et palettes des personnages séparément pour préserver la peau, l'œil bleu d'Alyzon et les yeux des zombies. Conserver lisibles fenêtres et menus. Ne jamais recalculer la teinte à partir d'une palette déjà teintée. Restaurer par le chargement normal des palettes lors de chaque sortie, combat, menu, fondu et retour de sauvegarde ; ne pas réintroduire le bug de palette partagé Matt/Don.

Charger météo/teinte à l'initialisation de carte avant son premier affichage et avant l'introduction. Le drapeau de scène unique ne commande **pas** la nuit : la nuit dépend seulement de la carte. Intérieurs traités séparément, sans héritage automatique de la brume.

### Prototype réellement exécuté

[Captures/GIF mGBA](galerie.html) et [résultat JSON](prototypes/TEST_PROTOTYPE_MGBA.json) : ROM privée de la base inchangée, nouvelle partie créée, téléportations de test, météo native et palettes temporaires injectées en RAM. 20 sprites météo mesurés, animation visible pendant 480 images. Au retour Route 8, météo native 2 et **palettes BG identiques au témoin** ; captures complètes non identiques, notamment à cause des états animés des objets. Ce résultat ne prouve pas encore les retours par menus/combats/rechargements : les hooks de production n'existent pas.

Les fichiers préfixés **MONTAGE** sont des compositions artistiques, jamais des captures d'intégration. La capture de combat utilisée comme fond provient d'un combat ordinaire de la base, avec adversaire rendu invisible temporairement en RAM pour les montages ; aucun nouveau zombie ni portrait n'est chargé par le moteur.

## Patrouilles et combat des errants

[Étude des patrouilles](patrouilles-faisabilite.json) : les chemins proposés sont sur des cases marchables du layout original. Énumération des **720 combinaisons** des quatre positions : les trois accès représentatifs et les six abords de portes restent reliés en considérant les zombies comme quatre obstacles d'une case. Une première proposition traversait l'abord de la maison de Fuji et a été corrigée avant livraison. C'est une vérification statique ; elle ne valide pas encore l'esquive des cônes de vision, les changements d'élévation ou le temps de réaction.

| Variante | Zone proposée (coordonnées carte) | Comportement / vision proposée |
|---|---|---|
| Errant | rectangle (5–7, 7–8) | marche lente, arrêt 60 images à chaque angle, vision 2 cases pendant l'arrêt |
| Sprinteur | segment (12–16, 12) | pause/avertissement 60 images, course jusqu'au bout, récupération 90 images ; aucune poursuite infinie |
| Colosse | segment (17–20, 8) | marche très lente, vision 1 case, longue pause de demi-tour |
| Spectral | rectangle (14–16, 17–18) | flottement lent, rotation annoncée, vision 2 cases ; murs jamais traversés |

Fenêtre de protection proposée : trois secondes après tout retour de combat, extension tant que le joueur reste dans la case de contact, remise en position sûre du zombie avant reprise. Détection neutralisée lors des scènes, dialogues, portes, et dans une zone de deux cases autour d'un point d'arrivée. Vérifier ligne de vue et collisions avant l'approche. Un seul combat à la fois. Pas de flag Dresseur définitivement vaincu pour ces quatre ennemis ; les Dresseurs de Tour restent un système distinct.

### Données des quatre ennemis

Conserver les statistiques/types fournis comme **hypothèses**, non activées : Errant 65/70/75/35/55/30 Poison/Spectre ; Sprinteur 50/85/40/35/40/95 Poison/Ténèbres ; Colosse 100/100/105/25/45/15 Poison/Combat ; Spectral 60/40/50/90/80/65 Spectre. Ordre PV/Att/Déf/AtSp/DéfSp/Vit. La vitesse du sprinteur et les défenses du colosse peuvent être sévères au niveau 30 : commencer les essais aux niveaux 22/24/26/25 respectivement, sans les figer avant tests.

Attaques natives proposées pour les essais : errant Étonnement/Griffe/Gaz Toxik/Étreinte ; sprinteur Vive-Attaque/Morsure/Griffe/Groz'Yeux ; colosse Écrasement/Coup d'Boule/Poing-Karaté/Groz'Yeux ; spectral Ombre Nocturne/Étonnement/Entrave/Malédiction. Malédiction et le harcèlement par statut nécessitent une revue d'équilibrage ; on peut tester sans cette attaque au premier passage. Les libellés définitifs doivent suivre ceux du projet, les constantes moteur sont la source de vérité.

**Emplacements dédiés :** les quatre anciens placeholders `SPECIES_OLD_UNOWN_B` à `_E` (252–255) sont hors des 151, mais ne sont pas « vides » : tables d'espèces, icônes, learnsets, conversion Pokédex et cris leur donnent déjà un comportement. Aucun appel explicite à ces quatre espèces n'a été trouvé dans les scripts/cartes/équipes examinés ; cela ne suffit pas à garantir l'absence d'appel calculé. Proposition préférée à soumettre à un spike technique : réserver explicitement ces quatre IDs, documenter leur caractère ennemi non collectionnable et traiter toutes leurs tables de présentation/EXP/cris/Pokédex sans décaler d'ID. Ne rien écrire dans les 151. Le code `SpeciesToCryId` et les conversions nationales demandent une garde ciblée, pas un déplacement des espèces.

Alternative si cette réservation s'avère fragile : adaptateur de combat temporaire à métadonnées ROM séparées, reprenant les points d'entrée de Don Spiraton sans réutiliser ses états. Il faudrait alors annoncer explicitement son gabarit interne et auditer chaque lookup de statistiques/types/graphismes ; ce n'est pas une solution déjà validée. **Aucun des deux schémas n'est implémenté.**

Dans les deux cas : entrée de combat sauvage scénarisé, ni type Dresseur ni Ball adverse, interdiction de fuite et capture dans menus ET fonctions d'objets, sortie K.O./défaite vers carte, aucune inscription Pokédex ni récompense capturable. EXP/argent à décider : proposition EXP faible sans EV, pas d'argent pour éviter un farm dominant, à valider. Ne pas étendre le système des huit formes de Don Spiraton à ces ennemis.

## Budget et limites mémoire

Mesures ELF de la base : EWRAM statique **261 128 / 262 144**, marge **1 016 octets** ; IWRAM privée **29 888 / 32 768**, marge nominale **2 880 octets** (ne pas y allouer sans réserve de pile). Publique IWRAM 29 824. Pas de gros état global nouveau : chemins et métadonnées en ROM, petites valeurs dans les données de tâche existantes ; aucune allocation par image. Le prototype n'ajoute rien à l'ELF.

Budget brut indicatif : onze OW sur neuf poses de 32 × 32 à 4 bpp = 50 688 octets ; onze images de combat 64 × 64 = 22 528 octets ; palettes OW/combat ≈704 octets, soit **73 920 octets** avant alignements, sources compilées et compression. Il s'agit d'une borne de travail, pas d'un gain mesuré au linker ; la plupart des humains peuvent rester en 16 × 32, et les vues latérales symétriques économiser des images si leur design le permet. Quatre images de combat zombie et sept portraits de Dresseurs/Championne expliquent les onze images. Les candidats de ce dossier ne sont pas encore les neuf poses de marche.

20 sprites météo sur les 64 structures `gSprites`, plus joueur/NPC/effets : marge à mesurer au pic, pas à déduire seulement de la limite matérielle de 128 OAM. Les métasprites consomment parfois plusieurs entrées OAM. En production, tester le compte, les matrices affines et les allocations OBJ avec apparition, portes, combats et menus. Une palette par sprite n'est pas garantie disponible simultanément ; proposer quatre palettes partagées pour les errants, puis regrouper les palettes des figurants et les Dresseurs par étage. Le prototype météo utilise la banque 12, **ce numéro n'est pas à coder en dur**.

`NUM_TRAINERS=745`, `MAX_TRAINERS_COUNT=768` : réserve nominale de 23 entrées sans étendre les flags de sauvegarde. Seize nouveaux enregistrements de Tour pourraient tenir dans cette réserve, Alyzon réutilisant 417 ; vérifier les éventuelles réservations avant attribution. Les flags de victoire/migration doivent rester cohérents avec les anciennes sauvegardes. Pas d'extension aveugle du format de sauvegarde.

## Musiques : écarts constatés

| Zone | Actuel | Souhait / état |
|---|---|---|
| Lavanville extérieur | Mystic Grove, ID 369 | Zombie Night (Town), ID 360, après validation de sa boucle |
| Sept étages de Tour | **Infinite Tunnel** | Le document dit « conserver Mystic Grove » ; passer à Mystic Grove serait donc un changement réel à confirmer |
| Intérieurs de Lavanville | Mystic Grove | Conservation proposée, sauf décision explicite |
| Alyzon | combat Championne d'origine via routage existant | Thème à choisir, aucune nouvelle affectation faite |

Zombie Night est le slot privé 14, source « 41. Zombie Night (Town) - Yo-Kai Watch 3 OST ». Il est actuellement en réserve non affectée et en **lecture unique**, 1 318 984 échantillons à 13 379 Hz, environ **98,586 s**, sans point de boucle. Une ambiance permanente s'arrêterait donc après ce délai si l'on changeait seulement le champ musique de la carte. Il faut rechercher un raccord puis le faire écouter avant activation ; aucun redémarrage/fondu artificiel ajouté. La compilation publique redirige 360 vers 369 via la table de secours : préserver ce repli et ne pas modifier globalement Mystic Grove, utilisé ailleurs. Les 31 flux, gains et autres affectations restent inchangés.

## Direction artistique et état réel des ressources

[Galerie](galerie.html), [contrôle technique des candidats](controle-graphique.json). Quatre variantes en quatre vues, six OW de face et six portraits, Alyzon trois vues et deux poses de portrait, quatre fronts de combat d'errants. Soit **37 images candidates initiales**, complétées par **quatre nouvelles faces compactes ciblant FRLG** (41 candidats au total) avec transparence binaire, palettes ≤15 couleurs opaques, formats 32 × 32 / 64 × 64 pour l'évaluation. Les agrandissements sont sans lissage.

**Limitation artistique explicite :** les planches sources ont été générées en grande résolution ; les fichiers natifs en sont des extractions rééchantillonnées sans lissage et limitées en palette, afin de comparer l'échelle. Ils ne sont pas présentés comme du pixel art natif finalisé, ni comme des ressources intégrées. Certains yeux, contours et flammes perdent encore en lisibilité. Le dernier choix du créateur impose FRLG : tête compacte vue de dessus, yeux bas, bras/jambes courts, palette modérée et peu de nuances. Les silhouettes CraftPix ne remplacent pas ce gabarit. **Retouche native pixel par pixel indispensable avant acceptation**, volume identique entre vues puis animation seulement après validation. Ces candidats servent à choisir une direction, pas à valider une finition qui n'existe pas.

**Mesure du gabarit présent au dépôt :** première image de `red_normal.png`, cellule 16 × 32, silhouette **14 × 19 pixels**, boîte x=1..14 / y=12..30, pieds à y=30, 12 couleurs opaques. Voir [mesure JSON](gabarit-frlg.json). Les premières études OW montent jusqu’à 28 pixels : elles sont donc trop grandes pour être acceptées telles quelles au gabarit standard. Une nouvelle proposition de face est fournie dans `FRLG-comparaison-red-natif.png` et son agrandissement ×6 : Red et quatre faces compactes, pieds à y=30, limite 14 × 19 pour les variantes ordinaires et 18 × 20 pour le colosse. Les dos/profils précédents doivent être repris sur ce nouveau gabarit après choix, ils ne constituent pas déjà une série cohérente validée. Les petites faces restent des prototypes générés et ajustés, pas une finition pixel par pixel certifiée.

Pour finaliser proprement : partir d'un OW FRLG existant à sa taille réelle, conserver ligne des pieds/tête/yeux, redessiner les masses sur une grille 16 × 32 ou 32 × 32, réserver 15 couleurs + transparent, contrôler en juxtaposition avec Nathan natif sur la carte. Retoucher manuellement les pixels critiques plutôt que poursuivre les seules réductions de planches. Le runner doit paraître rapide par sa posture, pas seulement par la vitesse du moteur ; le colosse peut être plus large sans devenir plus haut que tous les PNJ. Les trois faces/couronnes d'Encore Dead doivent rester lisibles.

## Validation à obtenir avant phase 2

1. Direction graphique **FRLG confirmée** ; choix/retouche des quatre zombies sur la nouvelle base et acceptation des autres personnages encore nécessaires.
2. Distribution des six Dresseurs ; exception Matt au 2F ; retrait des sept combats de l'ancienne Arène ; conservation CT19 et service de repos.
3. Équipes proposées A/B d'Alyzon et bases des six Dresseurs, statistiques/moves/récompenses des errants.
4. Dialogues de première arrivée et résidence.
5. Nuit/brume et réservation d'IDs ennemis après spike ; migrations et remplacement du flag Fuji à Safrania par obtention Flûte.
6. Confirmer Mystic Grove dans la Tour (elle joue actuellement Infinite Tunnel), choisir le thème d'Alyzon, valider à l'écoute une boucle de Zombie Night avant affectation permanente.

Les derniers messages confirment FRLG et la base de corpulence, **pas l'ensemble de ces décisions techniques ou scénaristiques**. Aucun de ces choix en attente ne sera déduit d'un silence.

## Plan de recette phase 2

| Domaine | Vérifications requises avant validation |
|---|---|
| Entrées | Nord/ouest/sud, Vol/Téléportation, maison, Continue, défaite : ambiance avant image et avant dialogue, scène une seule fois |
| Météo | Animation légère, portes/joueur visibles, menus/fondus non teintés à tort, sortie normale toutes directions, retour combat et rechargement |
| Patrouilles | Toutes phases et vitesses, chaque porte et passage toujours praticable, avertissement sprinteur, pas de détection à travers mur, arrêt pendant scène |
| Errants | Pas de Ball adverse, capture interdite par chaque type de Ball et rappel d'item, fuite interdite et talents/objets concernés, K.O., défaite, protection, reprise et réaffrontements |
| Tour | Accès sans Scope, rencontres visibles, disparition du verrou 6F, 16 placements et équipes approuvées, repos fonctionnel, Matt préservé |
| Badge | Victoire/défaite Alyzon, badge 4 unique, total huit, Force/obéissance/Route23, CT19 et sac plein |
| Résidence | Matt avant badge sans combat, Alyzon après, postgame sans rematch non validé, pas de personnages simultanés incohérents |
| Repaire | Entrée fermée avant badge, ouverte après ; anciennes sauvegardes passage déjà ouvert ou joueur dedans ; cartes/sbires/Don inchangés |
| Flûte | Sac plein, remise effective + flag, anciens Don/Scope/Fuji déjà terminés, aucune duplication, réveil des deux Misterre, défaite/retour |
| Safrania | Garde et accès Sylphe après nouvelle étape Flûte ; Thé et libération Sylphe inchangés |
| Audio | 31 pistes préservées, Zombie Night >3 cycles si boucle validée, transitions/fanfares/combats, vraie différence publique/privée et pas d'écoute humaine inventée |
| Mémoire | Linker public/privé <32 Mio, EWRAM/IWRAM + pile, heap au pic, OBJ/VRAM/OAM/palettes, fuite après répétition de visites/combats |
| Régression | Huit badges, 151 données/art/évolutions, autres Champions, toutes équipes Mafiamille hors trois placements locaux autorisés, finale Don Spiraton et Panthéon |

Ce dossier prépare ces tests ; ils ne sont pas annoncés réussis. Seuls l'audit de sources, les contrôles de format des prototypes, la connectivité statique et l'essai visuel RAM mGBA ci-dessus ont été effectués.
