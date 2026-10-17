# Pokémon Rouge Feu × Yo-kai Watch — Répartition validée pour Codex

**Version : 2.1 — 16 octobre 2026**  
**Statut : décisions de game design validées, pas une confirmation d'intégration au jeu.**

Ce document est le registre cumulatif des lieux d'obtention approuvés. À chaque nouvelle zone validée, mettre à jour **ce même document** et conserver ses décisions antérieures. Ne pas considérer les propositions contenues dans d'anciens tableaux comme validées lorsqu'elles contredisent les choix consignés ci-dessous.

## Règles essentielles pour Codex

- Conserver les numéros des 151 Yo-kai, les noms et les constantes techniques `SPECIES_*` définis dans `01_POKEDEX_151.csv`. **Ne pas échanger les entrées du Pokédex.**
- Pour modifier une obtention, éditer la rencontre, le script d'interaction, le cadeau, le fossile ou la boutique **localement**. Une espèce donnée par script peut utiliser une constante différente de celle du Pokémon qui occupait initialement ce script.
- Préserver les évolutions validées dans `03_EVOLUTIONS` et les autres données gameplay confirmées.
- Objectif : rendre les **151 Yo-kai obtenables dans une seule partie**, sans échange obligatoire avec une autre version.
- Les niveaux des rencontres fixes, les taux des rencontres, les prix non décidés et les détails de scripts restent à vérifier ou décider. Ne pas les inventer.
- Ce fichier **n'est pas une instruction d'appliquer les changements immédiatement** : il prépare leur intégration ultérieure par Codex.

## 1. Starters du Professeur Chen — VALIDÉS

| Événement | Yo-kai donné | N° fixe | Constante technique cible | Décision |
|---|---|---|---|---|
| Poké Ball de Bulbizarre au laboratoire | **Komasan** | 005 | `SPECIES_CHARMELEON` | **VALIDÉ : emplacement exact** |
| Une des deux autres Poké Balls | **Padrezo** | 029 | `SPECIES_NIDORAN_F` | **VALIDÉ : espèce starter ; emplacement précis restant à préciser** |
| L'autre Poké Ball | **Kappacap** | 087 | `SPECIES_DEWGONG` | **VALIDÉ : espèce starter ; emplacement précis restant à préciser** |

**À traiter :** adapter les scripts de distribution et la logique du rival. Les deux starters non choisis doivent pouvoir être obtenus ultérieurement dans la même partie ; méthode et lieu **non encore validés**.

## 2. Rencontres fixes / légendaires — VALIDÉES

| Rencontre d'origine | Lieu | Yo-kai cible | N° fixe | Constante technique cible |
|---|---|---|---|---|
| Ronflex n°1 | Route 12 | **Misterre** | 033 | `SPECIES_NIDORINO` |
| Ronflex n°2 | Route 16 | **Misterre** | 033 | `SPECIES_NIDORINO` |
| Artikodin | Îles Écume | **Mademoaiselle** | 147 | `SPECIES_DRATINI` |
| Électhor | Centrale | **Octorgone** | 015 | `SPECIES_BEEDRILL` |
| Sulfura | Mont Braise | **Kyubi** | 016 | `SPECIES_PIDGEY` |
| Mewtwo | Caverne Azurée | **Enma** | 150 | `SPECIES_MEWTWO` |

**Précisions :** les deux Ronflex deviennent **Misterre**. **Enma est Psy pur, BST 680**. Conserver les conditions d'accès et mécaniques d'interaction d'origine, sous réserve de vérifier leur compatibilité avec les nouveaux Yo-kai. Les niveaux exacts et apparences overworld ne sont pas fixés ici.

## 3. Fossiles — ESPÈCES VALIDÉES, AFFECTATION PARTIELLEMENT OUVERTE

| Source / interaction | Yo-kai obtenu | N° fixe | Constante technique cible | Statut |
|---|---|---|---|---|
| Fossile Dôme **ou** Nautile (Mont Sélénite) | **Tristos** | 115 | `SPECIES_KANGASKHAN` | Espèce validée, fossile précis **à décider** |
| L'autre fossile (Mont Sélénite) | **Sorcophage** | 070 | `SPECIES_WEEPINBELL` | Espèce validée, fossile précis **à décider** |
| Vieil Ambre | **Potofeu** | 032 | `SPECIES_NIDORAN_M` | **VALIDÉ** |
| Achat ultérieur du fossile non choisi | Fossile Dôme ou Nautile manquant | — | — | Principe validé ; **boutique, prix et conditions à décider** |

**Pour Codex :** modifier les espèces obtenues par résurrection, ne pas s'appuyer sur les anciennes constantes Omanyte, Kabuto ou Aerodactyl pour identifier automatiquement les cibles.

## 4. Dojo de Safrania — VALIDÉ

| Ancienne récompense | Nouveau Yo-kai | N° fixe | Constante technique cible | Statut |
|---|---|---|---|---|
| Kicklee | **Scatcheur** | 080 | `SPECIES_SLOWBRO` | **VALIDÉ** |
| Tygnon | **Coléroptere** | 078 | `SPECIES_RAPIDASH` | **VALIDÉ** |

**Règle impérative :** les **deux** Yo-kai doivent pouvoir être reçus dans la même sauvegarde, sans choix définitivement exclusif. Le mécanisme exact de remise du second Yo-kai reste **à décider**.

## 5. Cadeaux, boutiques et achats spéciaux — VALIDÉS

| Interaction d'origine | Lieu | Yo-kai cible | N° fixe | Constante technique cible |
|---|---|---|---|---|
| Évoli offert | Résidences de Céladopole | **Jibanyan** | 001 | `SPECIES_BULBASAUR` |
| Lokhlass offert | Sylphe SARL, Safrania | **Robonyan** | 017 | `SPECIES_PIDGEOTTO` |
| Porygon vendu contre des jetons | Casino de Céladopole | **Castelius Max** | 105 | `SPECIES_MAROWAK` |
| Magicarpe vendu par le marchand | Route 4 | **Castelius III** | 102 | `SPECIES_EXEGGCUTE` |

Les modalités d'achat d'origine peuvent être conservées si techniquement compatibles, mais aucun nouveau prix n'est validé ici. Prévoir le cas échéant la mise à jour du nom affiché et des messages des PNJ.

**Précision v1.8 sur Robonyan :** Robonyan n°017 (`SPECIES_PIDGEOTTO`) doit être **exclusif au cadeau remplaçant Lokhlass à la Sylphe SARL**, sans apparition sauvage à la Centrale ni ailleurs. Les propositions d'apparition sauvage de Robonyan sont révoquées. Son statut exclusif ne supprime pas la possibilité de faire évoluer le Robonyan offert.

**Modification v1.1 :** le cadeau Évoli distribue désormais **Jibanyan n°001** au lieu de Whisper n°008. Cette décision remplace l’ancienne attribution : **Whisper est désormais placé dans les rencontres sauvages de la Forêt de Jade (validation v1.3)**. Le nouveau cadeau ne change pas le n°001 de Jibanyan dans le Pokédex ; il donne `SPECIES_BULBASAUR` depuis le script du cadeau Évoli.

## 6. Interaction abandonnée — VALIDÉE

- **Carmin sur Mer : échange PNJ de Canarticho.** L'idée antérieure d'y obtenir **Whisper** est **ANNULÉE** ; **Whisper est désormais capturable dans la Forêt de Jade**, car Jibanyan occupe le cadeau de Céladopole.
- **À décider :** conserver l'échange avec une autre récompense, le modifier, ou le supprimer totalement. **Ne pas inscrire Whisper comme récompense de cet échange.**

## 7. Répartition des rencontres sauvages par zone — VALIDATIONS PROGRESSIVES

Les décisions ci-dessous priment sur les propositions des anciens tableaux. Les zones non validées sont toujours à définir. **Jibanyan n°001 ne doit pas figurer Route 1 : son obtention validée est le cadeau de Céladopole.**

| Zone | Yo-kai sauvages validés | État |
|---|---|---|
| **Route 1** | **Chiperpiou n°091 uniquement** (`SPECIES_CLOYSTER`) | **VALIDÉ : espèce unique en rencontre sauvage** |
| Route 2 | — | À définir |
| **Forêt de Jade** | **Cigalopin n°009** (`SPECIES_BLASTOISE`), **Nihilistik n°045** (`SPECIES_VILEPLUME`), **Vertipiou n°118** (`SPECIES_GOLDEEN`), **Whisper n°008** (`SPECIES_WARTORTLE`) | **VALIDÉ : quatre espèces uniquement en rencontre sauvage** |

**Instructions Route 1 pour Codex :** dans la table sauvage de Rouge Feu `MAP_ROUTE1` (rencontres terrestres / `land_mons`), la seule espèce sauvage doit être **Chiperpiou n°091**, correspondant à la constante `SPECIES_CLOYSTER` dans `01_POKEDEX_151.csv`. Tous les créneaux de rencontre terrestre doivent aboutir à Chiperpiou, soit **100 % des rencontres terrestres de la route**, sans changer le numéro de l’espèce ni remplacer globalement Roucool/Rattata sur les autres cartes. Le niveau exact, le taux global de déclenchement des rencontres et toute autre adaptation technique ne sont **pas encore validés** : conserver provisoirement leurs paramètres originaux jusqu’à décision.

**Instructions Forêt de Jade pour Codex :** dans la table sauvage de Rouge Feu `MAP_VIRIDIAN_FOREST` (`land_mons`), seules les espèces techniques `SPECIES_BLASTOISE` (Cigalopin n°009), `SPECIES_VILEPLUME` (Nihilistik n°045), `SPECIES_GOLDEEN` (Vertipiou n°118) et `SPECIES_WARTORTLE` (Whisper n°008) sont autorisées. Les répartir entre les créneaux existants **sans ajouter une cinquième espèce**. **Taux relatifs, niveaux et taux global de déclenchement des rencontres non décidés** : ne pas leur attribuer de valeurs présentées comme validées ; conserver provisoirement les paramètres d’origine quand cela est possible jusqu’à arbitrage. Modifier uniquement les créneaux de cette carte, sans remplacer globalement les constantes dans le jeu.

D'autres zones seront ajoutées progressivement au fil de la validation. Les événements fixes ci-dessus sont déjà verrouillés, même si les rencontres sauvages de leur zone restent à définir.

## 8. Derniers Yo-kai des champions d’arène et de la Ligue — CHOIX VALIDÉS

**Objet :** fixer les espèces constituant le dernier Yo-kai de chaque boss. Ce ne sont **pas** des rencontres sauvages ni la validation de l'ensemble de leurs équipes. Le joueur n'a pas nécessairement accès à l'espèce lorsqu'il affronte le boss. Codex ne doit pas déduire de ces choix qu'une modification des équipes est déjà intégrée.

| Boss | Dernier Yo-kai validé | N° fixe | Constante `SPECIES_*` | Condition d'obtention / répartition côté joueur |
|---|---|---|---|---|
| Pierre | **Passpa** | 025 | `SPECIES_PIKACHU` | Évolution de Nanpart ; Mont Sélénite souhaité pour Nanpart, table à valider. Pas de blocage post-Ligue demandé. |
| Ondine | **Sirénité** | 067 | `SPECIES_MACHOKE` | Évolution de Siréné ; Siréné doit être obtenable par **pêche**, lieu exact non fixé. Pas de blocage post-Ligue demandé. |
| Major Bob | **Parantonn** | 075 | `SPECIES_GRAVELER` | Évolution d'Antonnerre ; **Centrale** demandée pour Antonnerre, table à valider. Pas de blocage post-Ligue demandé. |
| Erika | **Misterre** | 033 | `SPECIES_NIDORINO` | Obtention validée par les rencontres fixes Ronflex des Routes 12 et 16 ; ne pas ajouter d'obtention précoce implicite. |
| Koga | **Slurpent** | 048 | `SPECIES_VENONAT` | **VERROU VALIDÉ : aucune obtention par le joueur avant d'avoir vaincu la Ligue une première fois ; lieu postgame à choisir.** |
| Morgane | **Savantard** | 145 | `SPECIES_ZAPDOS` | **VERROU VALIDÉ : aucune obtention par le joueur avant d'avoir vaincu la Ligue une première fois ; lieu postgame à choisir.** |
| Auguste | **Kyubi** | 016 | `SPECIES_PIDGEY` | Rencontre fixe déjà validée à la place de Sulfura au Mont Braise ; ne pas déplacer cette interaction. |
| Giovanni | **Trytik** | 084 | `SPECIES_DODUO` | **POSTGAME demandé** ; Caverne Azurée **emplacement envisagé, à confirmer**. Le nom correct du Pokédex est Trytik (pas « Tryptik »). |
| Olga | **Blizzaria** | 027 | `SPECIES_SANDSHREW` | Évolution d'Angelik ; **Îles Écume** souhaitées pour Angelik ; table à valider. |
| Aldo / Bruno | **Turboss** | 086 | `SPECIES_SEEL` | **Îles Écume proposées par l'utilisateur**, placement précis **à valider**. Rang communiqué : A/S. |
| Agatha | **Potofeu** | 032 | `SPECIES_NIDORAN_M` | Résurrection du **Vieil Ambre**, déjà validée. |
| Peter | **Octorgone** | 015 | `SPECIES_BEEDRILL` | Rencontre fixe déjà validée à la place d'**Électhor à la Centrale** ; ne pas la confondre avec Artikodin des Îles Écume (remplacé par Mademoaiselle). |

**Instructions contraignantes pour la répartition à venir :**

- Les verrous « postgame uniquement » de **Slurpent** et **Savantard** sont **VALIDÉS**. Ne créer aucune rencontre sauvage, cadeau, boutique, échange, reproduction ou autre voie d'acquisition permettant au joueur de les obtenir avant sa première victoire à la Ligue. Même principe à retenir pour **Trytik**, destiné au postgame ; sa carte exacte reste ouverte.
- Ne pas interdire automatiquement les pré-évolutions des autres derniers Yo-kai de boss : **Nanpart**, **Siréné**, **Antonnerre** et **Angelik** restent à placer conformément à la progression, et leurs évolutions se font suivant `03_EVOLUTIONS`.
- **Misterre**, **Kyubi**, **Potofeu** et **Octorgone** conservent strictement les interactions déjà validées aux sections 2 et 3. Les derniers Yo-kai des boss ne justifient pas d'inverser ces événements.
- **Turboss aux Îles Écume** et **Trytik à la Caverne Azurée** sont des intentions de placement à discuter lors de la validation de ces zones, et non de nouvelles tables sauvages déjà approuvées.
- Aucun niveau ni taux de rencontre, aucun changement d'équipe des boss et aucun nouveau script n'est déclaré exécuté.

## 9. Règle de game design — ÉVOLUTIONS SAUVAGES À ÉVITER (REMPLACE LA V1.5)

**VALIDÉ (2026-10-16, correction de la règle v1.5) :** **ne pas utiliser des espèces évoluées pour combler les listes de rencontres sauvages**. Favoriser quasi exclusivement les **formes de base, les espèces sans évolution et les espèces dont le statut n'est pas celui d'une forme évoluée**. L'objectif artistique est que le joueur découvre surtout les évolutions en combat contre les dresseurs importants, avec un **effet de surprise**.

- **Par défaut, aucune nouvelle forme évoluée en rencontre sauvage** dans les propositions de répartition, même en zone avancée. Si la liste d'une zone est courte, elle peut rester courte : ne pas la remplir artificiellement avec des évolutions.
- **Exception uniquement si l'utilisateur la valide expressément pour une espèce et une zone.** Ne jamais considérer l'ancienne autorisation v1.5 comme encore valable.
- **Ne pas empêcher le joueur de faire lui-même évoluer ses Yo-kai** : toutes les méthodes de `03_EVOLUTIONS` restent inchangées.
- **Ne pas annuler les cadeaux, fossiles, récompenses, boss fixes ou événements explicitement validés**, même si la cible est une évolution ou une espèce puissante (ex. Castelius Max au Casino, Misterre Routes 12/16). Les équipes des dresseurs peuvent utiliser des formes évoluées pour préserver l'effet « waouh ».
- Lors du contrôle final des 151 espèces, comptabiliser les formes accessibles **par évolution** ; il n'est pas nécessaire de les ajouter en sauvage pour compléter le Pokédex.

**Statut : règle VALIDÉE.** Aucun placement sauvage supplémentaire n'est validé par cette décision. **Exception explicite exprimée ensuite en v1.8 : Canastelle n°054 directement sur la Route 11** ; cette permission individuelle ne rétablit pas la règle abandonnée de remplissage avec des évolutions.

## 10. Préférences de placement communiquées — À SOUMETTRE À VALIDATION PAR ZONE

Ces intentions, formulées par l'utilisateur, sont prioritaires par rapport aux propositions de l'assistant, mais **ne sont pas encore les tables d'apparition complètes et validées**. Certaines zones nécessitent des rencontres supplémentaires, des cadeaux ou des scripts : choisir le mécanisme après arbitrage. Ne pas inventer de taux/niveaux.

| Zone / environnement souhaité | Espèces préférées de l'utilisateur | Statut |
|---|---|---|
| Mont Sélénite | Nanpart n°024 | Préférence, hors interactions fossiles déjà validées |
| Manoir Pokémon | Feulion n°028, Crocho n°031 | Préférences |
| Îles Écume | Angelik n°026, Chihuaglagla n°063 ; Turboss n°086 envisagé auparavant | Préférences, Mademoaiselle fixe reste validée |
| Accès Piste cyclable / Route 16 | Terminyanator n°133 | Préférence de zone ; **ne remplace pas** les deux Misterre fixes validés |
| Route Victoire | Démophage n°040, **Fouetar n°059**, **Gorgouille n°065**, **Fourchelang n°136** | Préférences explicites ; Gorgouille confirmé ici (déjà proposé), Fourchelang transféré depuis l’ancienne proposition Routes 7–8 ; Fouetar quitte la proposition Route 22 |
| Route 23 (avant la Route Victoire) | **Volroulo n°141** | **Nouvel emplacement choisi par l’assistant avec autorisation explicite de l’utilisateur** ; rang A, haute herbe de fin d’aventure, présence avant-Ligue souhaitée |
| Route 8 (Lavanville–Safrania) | **Rocky Badboya n°116**, rang B | **Proposition d’emplacement choisie par l’assistant à la demande du joueur de le rendre accessible vers le milieu du jeu**, et non plus dans la proposition de la Route Victoire ; espèce, niveaux et taux non encore définitivement validés |
| Grotte, provisoirement Tunnel Roche | Couchtar n°057 | Préférence ; nom exact de la grotte à confirmer |
| Tour Pokémon | Brumette n°041, Télémir n°043, Dracounet n°013 **rare**, **Chaipo n°124** | Préférences ; Chaipo quitte la proposition du Mont Sélénite |
| Sylphe SARL | Mognyan n°051, Arbrézo n°108 | Préférences ; Robonyan reste le cadeau validé |
| Parc Safari | Noko n°082, Doyaris n°139, Faux Kappa n°020 | Préférences |
| Caverne Azurée | Trytik n°084 | Préférence, **exclusivité post-Ligue demandée** ; Enma fixe maintenu |
| Repaire Rocket | Lulugubre n°142, Espreschiot n°110 | Préférences |
| Cave Taupiqueur | Potache n°094, **Métaurolog n°034** | Préférences ; Métaurolog quitte la proposition du Souterrain N–S |
| Centrale | Antonnerre n°074, **Tontonnerre n°073** | Préférences ; Tontonnerre quitte la proposition de L’Océane ; Octorgone reste le fixe validé ; **Robonyan ne doit pas y apparaître** |
| Routes avant Ondine | Lacanne n°053 | Préférence, route à choisir |
| Hautes herbes, route adaptée au rang | Sabrille n°135 | Préférence, route à choisir |
| Eaux marines / océan | Murhaine n°011, Raton Glandeur n°117, Sabruine n°134, **Navétéran n°096** | Préférences marines ; **Navétéran est aussi obtenable sur les routes maritimes 19–21**, en plus de L’Océane ; décision explicite de v1.9 |
| L’Océane (navire) | **Navétéran n°096** | Souhait explicite ; remplace Tontonnerre de la proposition antérieure. **La seconde obtention maritime est désormais autorisée : le départ du navire ne verrouille pas l’espèce.** |
| Zone de pêche (à déterminer) | **Siréné n°066** | Rencontre par **pêche** demandée ; aucune route ou étendue d’eau précise fixée. |
| Routes 5–6 | **Raltesse n°151** | Remplace Yvantouse dans la proposition de l’assistant. |
| Souterrain E–O | **Yvantouse n°055** | Remplace Raltesse dans la proposition de l’assistant ; absence de rencontres sauvages d’origine, mécanisme à décider. |
| Route 11 | **Canastelle n°054** | Remplace Coach Antonic ; **EXCEPTION EXPLICITE : forme évoluée (de Lacanne) autorisée directement** sur cette route. |
| Manoir Pokémon | Feulion n°028, Crocho n°031, **Coach Antonic n°099** | Coach Antonic remplace Tête de lard de la proposition antérieure. |
| Souterrain N–S | **Tête de lard n°093** | Remplace Métaurolog dans la proposition antérieure ; mécanisme à décider faute de rencontres sauvages natives. |

Aucun placement proposé par l'assistant en réaction à ces préférences n'est validé par défaut. La Forêt de Jade reste strictement limitée aux quatre Yo-kai validés en section 7. L'utilisateur a en outre fourni des visuels et une classification par types/rangs pour guider les futures propositions ; se référer aux documents et décisions de référence, sans recomposer les numéros du Pokédex.

## 11. Échange PNJ — MARCI (Route 2) — CHOIX DE GAME DESIGN

**Intention décidée par l’utilisateur :** conserver l’échange en jeu situé sur la Route 2 qui remet traditionnellement M. Mime contre Abra, mais le réaffecter pour que le joueur reçoive **Humainequin n°047**, rang B, constante **`SPECIES_PARASECT`**.

**Contrepartie choisie à la demande de l’utilisateur : Potache n°094**, rang E, constante **`SPECIES_GENGAR`**. La raison du choix est géographique : Potache a été souhaité par l’utilisateur à la **Cave Taupiqueur**, proche de l’accès à l’échange de la Route 2 ; c’est une étape réalisable autour de Carmin-sur-Mer, sans distribuer Humainequin dès le départ.

| Élément | Affectation |
|---|---|
| PNJ | Marci, Route 2, dans l’interaction d’échange M. Mime / Abra d’origine |
| Espèce demandée au joueur | **Potache n°094** — `SPECIES_GENGAR` |
| Espèce donnée par le PNJ | **Humainequin n°047** — `SPECIES_PARASECT` |
| Mode d’obtention | Échange PNJ, **pas** rencontre sauvage sur la Route 2 |
| Répétabilité | Conserver le principe de l’échange unique d’origine, sauf décision contraire |
| Prérequis | Vérifier l’accès réel au PNJ dans les scripts de Rouge Feu ; ne pas inventer de conditions supplémentaires |
| Dépendance | Potache à la Cave Taupiqueur est une préférence de placement déjà exprimée, mais sa table exacte reste à valider |

**Pour Codex :** identifier la donnée / le script de l’échange original de la Route 2, adapter les espèces exigée et reçue, les dialogues et tout nom affiché. Ne pas remplacer globalement `SPECIES_ABRA` ni `SPECIES_MR_MIME`. Les constantes cibles des deux Yo-kai sont **`SPECIES_GENGAR`** et **`SPECIES_PARASECT`**, quels que soient leurs numéros ou emplacements Pokémon d’origine. Aucun code n’a été modifié à ce stade.

**Statut :** Humainequin comme récompense de Marci est **décidé par l’utilisateur** ; Potache en contrepartie est **choisi par l’assistant à la demande de l’utilisateur**. Si le placement final de Potache change, revérifier l’accessibilité de l’échange. Cette entrée n’implique aucune apparition sauvage supplémentaire d’Humainequin.

## 12. Révisions précises de la proposition de répartition — 2026-10-16 (v1.8)

**Origine :** l’utilisateur corrige le tableau global précédemment proposé par l’assistant. **Ces affectations sont des préférences explicites à intégrer à la prochaine version du tableau**, pas des niveaux/taux/scripts validés. Lorsqu’un ancien emplacement est nommé, **le retirer de la proposition** ; ne pas dupliquer accidentellement l’espèce entre son nouvel emplacement et l’ancien.

| Espèce | N° | Constante technique | Nouvelle zone/méthode demandée | Ancien placement proposé à annuler |
|---|---:|---|---|---|
| **Navétéran** | 096 | `SPECIES_DROWZEE` | **L’Océane, navire**, décidé en v1.8 | Les routes maritimes avaient été temporairement retirées en v1.8, puis **réautorisées explicitement en v1.9** (obtention double : navire + routes 19–21) |
| **Tontonnerre** | 073 | `SPECIES_TENTACRUEL` | **Centrale** | L’Océane |
| **Chaipo** | 124 | `SPECIES_JYNX` | **Tour Pokémon** | Mont Sélénite |
| **Siréné** | 066 | `SPECIES_MACHOP` | **Zone de pêche**, emplacement exact **à choisir** | Proposition de présence terrestre Routes 24–25 ou Îles Écume : non retenue comme obtention terrestre |
| **Fouetar** | 059 | `SPECIES_ARCANINE` | **Route Victoire** | Route 22 |
| **Raltesse** | 151 | `SPECIES_MEW` | **Routes 5–6** | Souterrain E–O |
| **Yvantouse** | 055 | `SPECIES_GOLDUCK` | **Souterrain E–O** | Routes 5–6 |
| **Canastelle** | 054 | `SPECIES_PSYDUCK` | **Route 11**, malgré son statut d’évolution de Lacanne | Coach Antonic occupe la Route 11 dans la version antérieure |
| **Coach Antonic** | 099 | `SPECIES_KINGLER` | **Manoir Pokémon** | Route 11 ; remplace Tête de lard dans le Manoir |
| **Tête de lard** | 093 | `SPECIES_HAUNTER` | **Souterrain N–S** | Manoir Pokémon ; remplace Métaurolog au Souterrain N–S |
| **Métaurolog** | 034 | `SPECIES_NIDOKING` | **Cave Taupiqueur** | Souterrain N–S |
| **Robonyan** | 017 | `SPECIES_PIDGEOTTO` | **Cadeau Lokhlass exclusivement** à la Sylphe SARL (**déjà validé et maintenant déclaré exclusif**) | Toute apparition sauvage proposée à la Centrale ou ailleurs |

**Règles qui découlent de ces corrections :**

- **Canastelle n°054 est l’exception individuelle clairement autorisée à la règle « évolutions sauvages à éviter »**, et peut être directement rencontrée sur la Route 11. Conserver en parallèle la méthode normale d’évolution Lacanne → Canastelle du document `03_EVOLUTIONS`.
- **Robonyan n°017 ne doit pas apparaître en sauvage** : son unique source d’obtention par le joueur est le cadeau Lokhlass remplacé à la Sylphe SARL. Ne pas confondre le cadeau avec les autres espèces qui peuvent être proposées dans la Sylphe SARL.
- **Siréné n°066 :** la **méthode « pêche » est choisie**, mais le lieu exact et la canne requise ne sont pas encore décidés. Ne pas inventer une zone ni un objet requis.
- **Navétéran n°096 :** le problème de l’Océane manquable est **résolu dans la version 1.9** : les routes maritimes 19–21 constituent une **seconde obtention validée**, même après le départ du navire. La méthode précise (surf / pêche / type de rencontre) et les niveaux/taux restent à décider.
- **Souterrains N–S et E–O :** pas de rencontres sauvages terrestres standard dans Rouge Feu. Ajouter un script, objet, PNJ ou une nouvelle table sauvage uniquement après validation de la mécanique de distribution.
- Les rencontres fixes existantes (**Misterre**, **Octorgone**, **Mademoaiselle**, **Kyubi**, **Enma**) ne changent pas. Les lieux restants de la proposition globale ne sont pas approuvés par implication.

## 13. Nouveaux placements explicitement retenus — 2026-10-16 (v1.9)

**Ces placements ont été expressément demandés ou délégués par l’utilisateur** : ils prennent le pas sur les propositions plus anciennes de l’assistant. La **présence de l’espèce dans la zone est décidée** ; les taux, niveaux et détails techniques des rencontres ne le sont pas. Respecter les formes de base et sans évolution sauf exceptions déjà validées.

| Lieu | Espèce | Rang | Constante technique cible | Décision et gestion des doublons |
|---|---|---|---|---|
| **Route 23** (approche de la Route Victoire, après 8 badges) | **Volroulo n°141** | A | `SPECIES_KABUTOPS` | **Nouvelle zone choisie par l’assistant sur délégation explicite du joueur.** Retirer Volroulo de l’ancienne *proposition* de la Route Victoire. Aucune autre nouvelle zone décidée pour cette espèce. |
| **Route Victoire** | **Gorgouille n°065** | A | `SPECIES_ALAKAZAM` | **Placement souhaité explicitement et maintenant confirmé** ; figurait déjà dans la proposition initiale Route Victoire, mais n’était pas inscrit comme choix ferme. |
| **Route Victoire** | **Fourchelang n°136** | B | `SPECIES_FLAREON` | **Placement souhaité explicitement** ; retirer Fourchelang de la *proposition* antérieure Routes 7–8. |
| **L’Océane** (navire) | **Navétéran n°096** | C | `SPECIES_DROWZEE` | **Conserver** le placement sur le navire précédemment demandé. |
| **Routes maritimes 19–21**, océan | **Navétéran n°096** | C | `SPECIES_DROWZEE` | **Ajouter une deuxième méthode d’obtention expressément demandée** (en plus du navire). L’accès permanent résout l’obstacle du bateau manquable. Distinguer de la Route 19/20/21 exacte et du mode eau/pêche, à définir ultérieurement. |

**Ce qui ne change pas :** Route Victoire contient également Démophage n°040 et Fouetar n°059 selon les préférences précédentes ; Misterre, Octorgone, Mademoaiselle, Kyubi, Enma, les cadeaux et l’échange Marci restent inchangés. Aucune apparition sauvage nouvelle d’une forme évoluée n’est ajoutée par cette révision.

**Ne pas interpréter comme modification du code déjà effectuée.** À transmettre à Codex pour application future au moment où les listes de chaque zone seront définitivement validées. Les anciennes versions du grand tableau servent de brouillon et non de source de vérité sur ces cinq décisions.

## 14. Correction de progression — ROCKY BADBOYA (v2.0)

**Décision de progression exprimée par l'utilisateur (2026-10-16) :** **Rocky Badboya n°116, rang B**, doit être disponible **sensiblement plus tôt, vers le milieu de l'aventure**, contrairement à sa présence dans la *proposition antérieure* de la Route Victoire. Il n'y a donc **pas de rencontre sauvage de Rocky Badboya à la Route Victoire** dans le nouveau plan.

**Proposition précise de l'assistant pour répondre à cette demande : Route 8 (entre Lavanville et Safrania)**, en hautes herbes, comme rencontre plutôt rare de rang B. L'emplacement exact **n'a pas été explicitement validé par le joueur** et reste à confirmer s'il souhaite le déplacer. Le rang B et le numéro 116 proviennent du Pokédex communiqué. Constante technique attendue par correspondance indexée Pokémon #116 : `SPECIES_HORSEA` (**vérifier dans `01_POKEDEX_151.csv` avant implémentation**).

**Effet sur la répartition :** enlever Rocky Badboya du brouillon « Route Victoire », sans modifier Démophage n°040, Fouetar n°059, Gorgouille n°065 ni Fourchelang n°136, dont les préférences de présence à la Route Victoire sont enregistrées ; Volroulo n°141 reste Route 23. Ne pas créer deux lieux non voulus pour Rocky Badboya. Aucun taux ou niveau imposé par cette correction.


## 15. Points ouverts à résoudre

1. Attribuer précisément les emplacements Salamèche/Carapuce à Padrezo et Kappacap, si souhaité.
2. Définir la récupération des deux starters non choisis.
3. Associer définitivement Tristos/Sorcophage aux fossiles Dôme/Nautile.
4. Définir la boutique et le prix du fossile non choisi.
5. Définir la façon d'obtenir les deux récompenses du Dojo.
6. Trancher le sort de l'échange de Canarticho à Carmin sur Mer.
7. Continuer de valider les rencontres sauvages **zone par zone** (Route 1 et Forêt de Jade validées), puis les niveaux, taux et tables complètes.
8. Définir les lieux postgame précis de Slurpent et Savantard ; confirmer Caverne Azurée pour Trytik et Îles Écume pour Turboss.
9. Transformer les préférences de zones pour Angelik (Îles Écume), Antonnerre (Centrale) et Nanpart (Mont Sélénite) en tables finales ; pour Siréné (pré-évolution de Sirénité), fixer **la zone et les modalités de pêche**.
10. Vérifier la disponibilité de Potache avant l’échange de Marci et l’accessibilité effective du PNJ Route 2.
11. **Navétéran garanti sur les routes maritimes 19–21 (v1.9) : accès de secours acquis** ; préciser sa méthode de rencontre et décider les interactions des deux souterrains ; supprimer toute apparition sauvage proposée de Robonyan.
12. Auditer à la fin la disponibilité réelle des 151 espèces dans une seule partie, dont celles dont les constantes d'origine n'étaient pas normalement obtenables dans Rouge Feu.

## 16. Export exhaustif d'obtention des 151 Yo-kai — v2.1

**Fichier à fournir à Codex : `REPARTITION_OBTENTION_151_YOKAI_CODEX.csv`**, généré à partir de la copie du fichier utilisateur `01_POKEDEX_151(2).csv`, des 56 transitions de `03_EVOLUTIONS.xlsx`, des rangs communiqués par le joueur et du présent registre. **Le CSV est un plan technique exhaustif à intégrer par étapes, pas un relevé de modifications déjà codées.**

- **151 lignes**, une par Yo-kai, triées 001 → 151 ; **toutes les constantes `SPECIES_*` et les six colonnes d'identité** du Pokédex fourni sont préservées. Séparateur `;`, encodage UTF-8 avec BOM pour tableurs francophones.
- **95 espèces indépendantes ou de base** disposent chacune d'une méthode d'obtention principale proposée ou validée. **56 autres formes** ont leur condition d'évolution extraite de `03_EVOLUTIONS.xlsx` ; elles ne doivent PAS être ajoutées par défaut dans les rencontres sauvages. **Exceptions précises : Canastelle n°054 sauvage sur la Route 11 et Castelius Max n°105 en récompense du Casino**.
- `statut_placement=VALIDE` : interaction ou zone explicitement verrouillée ; `SOUHAIT_UTILISATEUR` : emplacement demandé par le joueur, mécanique non nécessairement définie ; `CHOIX_ASSISTANT` : lieu choisi sur délégation ou conseillé ; `PROPOSITION_A_VALIDER` : complément de répartition de l'assistant ; `EVOLUTION_CONFIRMEE` : mode d'évolution déjà documenté. Ne pas confondre statut de localisation et faisabilité technique.
- Les modifications fermes de Route 1, Forêt de Jade, cadeaux, fossiles, deux Ronflex, légendaires, échange Marci et Dojo restent prioritaires sur les autres propositions. Les corrections successives (Canastelle Route 11, Robonyan cadeau seulement, Rocky Badboya hors Route Victoire, Navétéran routes maritimes, etc.) prévalent sur l'ancienne proposition.
- **Garde-fous Codex :** modifier les entrées de rencontre au niveau exact des cartes et les scripts des événements au bon endroit ; **ne jamais remplacer une constante `SPECIES_*` globalement**. Dans les édifices sans table d'herbe native (Sylphe SARL, Repaire Rocket, Océane, Souterrains N–S/E–O), prévoir des interactions adaptées et vérifier leur possibilité de rattrapage.
- **Inconnues à trancher pour un 100 % vérifié** : sélection exacte de Padrezo/Kappacap dans les deux Poké Balls ; récupération des deux starters non choisis ; obtention de plusieurs Jibanyan pour ses trois évolutions ; obtention de plusieurs Castelius III si nécessaire ; attribution Dôme/Nautile à Tristos/Sorcophage et achat du fossile non choisi ; remise des deux prix Dojo ; zone/canne précises de Siréné (Route 12 simple proposition CSV) ; mécanique des bâtiments sans sauvages ; disponibilité des événements Rocket après progression ; niveaux et taux.
- **Postgame exclusif à appliquer absolument** : Slurpent n°048, Savantard n°145 et Trytik n°084 ne doivent pas être obtenables avant la première victoire à la Ligue (lieux précis proposés ou exprimés, mais les verrous sont obligatoires). **Enma n°150** conserve l'événement de Mewtwo dans la Caverne Azurée.
- Le CSV permet de planifier l'intégration ; **il ne prouve pas encore les 151 réellement capturables dans une sauvegarde**. Codex doit contrôler les embranchements d'évolution, les cadeaux uniques, les scripts manquables et les contraintes des tables, puis lancer les vérifications de compilation et de jeu.

---

**Historique :**
- **v2.1 — 2026-10-16 :** export du CSV d’obtention des 151 espèces : statut de chaque placement, condition des 56 évolutions et alertes pour Codex ; aucune modification du dépôt GitHub.
- **v2.0 — 2026-10-16 :** Rocky Badboya n°116, rang B, déplacé hors de la proposition de Route Victoire à la demande de l’utilisateur (« accessible plus tôt, vers le milieu de jeu »). Route 8 proposée par l’assistant comme nouvelle zone à confirmer ; aucune ancienne occurrence sauvage Route Victoire à conserver. Autres choix inchangés.
- **v1.9 — 2026-10-16 :** Volroulo n°141 attribué à la Route 23 ; Gorgouille n°065 et Fourchelang n°136 fixés à la Route Victoire ; Fourchelang retiré de la proposition Routes 7–8, Volroulo retiré de celle de Route Victoire. Navétéran n°096 obtenable à la fois sur L’Océane et sur les routes maritimes 19–21, ce qui résout son caractère manquable. Taux, niveaux et méthode de capture maritime encore ouverts.
- **v1.8 — 2026-10-16 :** 12 corrections de placement souhaitées, dont Navétéran sur l’Océane, Tontonnerre à la Centrale, Chaipo à la Tour Pokémon, Siréné par pêche, Fouetar à la Route Victoire, permutations des deux souterrains / Routes 5–6 / Route 11 / Manoir / Cave Taupiqueur. Canastelle autorisée explicitement comme rare exception d’évolution directement présente Route 11. Robonyan exclusif au cadeau Lokhlass de la Sylphe SARL, aucune rencontre sauvage.
- **v1.7 — 2026-10-16 :** échange PNJ de Marci (Route 2) : reçoit Potache n°094 (`SPECIES_GENGAR`), donne Humainequin n°047 (`SPECIES_PARASECT`) ; dépendance à la capture de Potache dans la Cave Taupiqueur à vérifier.
- **v1.6 — 2026-10-16 :** annulation de la permission d’utiliser des évolutions comme remplissage sauvage. Les formes évoluées restent quasi exclusives aux combats de dresseurs (et aux évolutions du joueur), sauf exception explicitement validée et événements déjà verrouillés.
- **v1.5 — 2026-10-16 :** autorisation ponctuelle de rencontres sauvages d’espèces évoluées lorsque nécessaire ; consignation des préférences de placement (non encore validées zone par zone).
- **v1.4 — 2026-10-16 :** derniers Yo-kai des huit champions et des quatre membres du Conseil 4 validés ; Slurpent et Savantard réservés au postgame, Trytik destiné au postgame avec Caverne Azurée envisagée ; Turboss aux Îles Écume envisagé. Aucune modification des rencontres fixes précédemment validées.
- **v1.3 — 2026-10-16 :** Forêt de Jade validée : Cigalopin n°009, Nihilistik n°045, Vertipiou n°118 et Whisper n°008 comme quatre seules espèces sauvages ; taux et niveaux non décidés. Whisper a désormais un lieu d’obtention validé.
- **v1.2 — 2026-10-16 :** Route 1 validée : uniquement Chiperpiou n°091 (`SPECIES_CLOYSTER`) en rencontre sauvage terrestre ; niveaux et fréquence absolue de rencontre non décidés.
- **v1.1 — 2026-10-16 :** cadeau Évoli (Céladopole) réattribué à Jibanyan n°001 (`SPECIES_BULBASAUR`) ; Whisper n°008 redevient à placer ; aucune présence de Jibanyan Route 1 approuvée.
- **v1.0 — 2026-10-16 :** création du registre ; inscription des starters, rencontres fixes, fossiles, Dojo, cadeaux/boutiques et retrait de Whisper de l'échange de Carmin sur Mer.
