# ROM_ANALYSIS — analyse technique de « Pokémon Yo-kai Emerald »

Audit du 2026-11-14. Fichier reçu : `pokeemerald.zip` (SHA-1 `03d3270d…`) contenant **deux fichiers identiques**
(`pokemon_emerald.gba` et `pokemon_emerald_jibanyan_audio.gba`, même SHA-1 `ff71db05…`, 0 octet différent) :
le nom « jibanyan_audio » ne correspond à **aucune** différence de contenu.

Méthode : comparaison avec une Émeraude **compilée localement** depuis la décompilation `pret/pokeemerald`
(commit `731ad5bfd`), sans aucune ROM téléchargée. Reproductible avec `tools/analysis/compare_with_vanilla.py`
et `tools/yokai_extract.py`. Les deux ROM de référence restent hors du dépôt.

## 1. Identité de la ROM

| Point | Résultat | Preuve |
|---|---|---|
| Code jeu / révision | `BPEE`, révision 0 : **Pokémon Émeraude US (anglais)** | en-tête `0xAC`, `0xBC` |
| Langue (en-tête GF) | `2` = anglais | `rom_header_gf.c`, `0x104` |
| Hashes | SHA-1 `ff71db053a6d4d0f31368d95b39c6b7d6038da13`, MD5 `fbe2aa2dd8c5a1caf4afd4e4ec141448` | `sha1sum`, `md5sum` |
| ≠ Émeraude officielle | officielle : SHA-1 `f3ae0881…`, MD5 `605b89b6…` (reproduite **à l'octet** par notre build agbcc) | build local |
| Taille utile | jusqu'à `0xCBFD94` (officielle : `0xE3CF64`) | octets `0xFF` de fin |
| **Origine** | **construite depuis la décompilation pret/pokeemerald avec `make modern`** (GCC ARM moderne) | voir §2 |

## 2. Preuve : une build « modern » de la décompilation, pas un patch binaire

1. Une build `make modern` de pret/pokeemerald s'arrête à `0xCB25D8` ; le hack à `0xCBFD94` (+55 Kio).
2. Les tables du hack sont **décalées de quelques Kio seulement** par rapport à la build modern
   (`gSpeciesInfo` `0x77DF14` → `0x784610`, `gSpeciesNames` `0x639024` → `0x63EB6C`), mais de plusieurs Mio par
   rapport à l'officielle (`0x3203CC`).
3. La table d'évolution a des entrées de **8 octets** (structure de 6 octets arrondie à 4 par l'ABI `apcs-gnu`
   des builds modern) : 40 octets par espèce, comme dans notre build modern.
4. Le code ne correspond qu'à 669 fonctions sur 5 376 à pointeurs près : **le compilateur n'est pas le même que
   le nôtre** (arm-none-eabi-gcc 13.2.1). Conséquence : **impossible d'affirmer ou d'exclure par le binaire une
   modification du moteur** (les différences de génération de code masquent les autres).

## 3. En-tête GF (rom_header_gf.c) : différences

| Champ | Vanilla | Hack | Signification |
|---|---|---|---|
| `pokedexCount` | 386 | **392** | Pokédex national +6 |
| `saveBlock2Size` | `0xF2C` | `0xF30` | sauvegarde modifiée (drapeaux Pokédex agrandis) |
| `saveBlock1Size` | `0x3D88` | `0x3D8C` | idem |
| `frontierStatusOffset`, `gcnLinkFlagsOffset` | `0xCA8`, `0xA8` | `0xCAC`, `0xAC` | décalés de 4 |
| `flagsOffset`, `varsOffset`, `partyOffset`… | — | **inchangés** | |

**Le format de sauvegarde diffère** de l'Émeraude officielle : une sauvegarde vanilla ou Archipelago n'est pas
interchangeable avec celle du hack.

## 4. Données comparées table par table

| Table | Résultat |
|---|---|
| Noms d'espèces 0-411, statistiques 0-411 | **identiques** (0/412) |
| Noms d'attaques, données d'attaques (355) | **identiques** |
| Noms de talents (78) | identiques |
| Évolutions 0-411, CT/CS 0-411 | identiques |
| **Espèces 412-417** | **ajoutées** : JIBANYAN, KOMASAN, KOMAJIRO, BLIZZARIA, GARGAROS, WHISPER |
| Correspondances Pokédex | Yo-kai = n° national **387-392**, n° Hoenn **203-208** ; les entrées « vieux Zarbi » sont décalées d'autant |
| Dresseurs (855) | **aucun modifié** (en-têtes et équipes) |
| Starters | inchangés (Arcko, Poussifeu, Gobou) |
| Rencontres sauvages | **106 emplacements Yo-kai** + 5 autres changements (voir YOKAI_CONTENT.md) |
| Scripts de don (`givemon`, `setwildbattle`) | aucun Yo-kai trouvé (les occurrences d'octets trouvées sont dans des données graphiques) |

## 5. Graphismes des protagonistes

Remplacés : illustrations de dresseur avant/arrière de Brendan et May et leurs palettes, et **tous** les sprites de
terrain (marche, course, Vélo Course / Cross, surf, pêche, arrosage, plongée, décoration, attaque de terrain).
Inchangés : les palettes de terrain `gObjectEventPal_Brendan/May` (les nouveaux dessins utilisent les palettes
d'origine) et les graphismes « Rubis/Saphir » de Brendan et May.

Vérification **dans le jeu** (mGBA, voir PROTOTYPE_RESULTS.md) : au choix « garçon / fille », le garçon est un
personnage aux cheveux bruns en épis et chemise rouge rayée, la fille a une queue de cheval avec un nœud rose.
Cela correspond à **Nathan Adams** et **Katie Forester**. C'est une identification visuelle : les noms
« Nathan » et « Katie » n'apparaissent dans **aucun texte** du jeu. Les chaînes `NATHAN` et `KATIE` présentes sont
celles de dresseurs vanilla. Le nom du joueur reste à saisir.

## 6. Textes ajoutés ou modifiés

Différence exhaustive des chaînes ≥ 8 caractères (13 925 en vanilla, 13 939 dans le hack) : 22 nouvelles, dont
6 noms d'espèces, 6 descriptions Pokédex, la catégorie `YOKAI` et **le texte des crédits**. Les autres sont des faux
positifs de découpage. Aucun dialogue de l'histoire n'est modifié.

Crédits, affichés par un **panneau ajouté à Bourg-en-Vol** (Littleroot Town, x=7, y=5 ; 5 panneaux au lieu de 4) :

> Jibanyan based on sprite of: Ludo. / the other sprites by: SonGoku and Nicowico.

## 7. Anomalies détectées (bugs probables du hack)

| Anomalie | Effet | Vérifié en jeu ? |
|---|---|---|
| WHISPER : second type = `255` (invalide) | écran de résumé / calculs de type potentiellement incorrects | Non |
| Pokédex n° 389 (Komajiro) pointe vers la description de **Whisper** ; la description de Komajiro existe mais n'est référencée nulle part | mauvais texte | Non |
| Pokédex n° 392 (Whisper) : catégorie vide, taille et poids 0, **pointeur de description nul** | texte corrompu ou plantage possible à l'ouverture de la page | Non |
| Grotte Tréfonds (salle de glace), emplacement 11 : BLIZZARIA **niveaux 1 à 100** | niveaux aléatoires extrêmes | Non |
| Légendaires ajoutés en sauvage : Jirachi (Route 114, Route 106 surf), Celebi (Route 106 pêche), Ho-Oh (Caverne Profonde) | équilibrage ; incompatibles avec la logique AP des légendaires | Non |
| Statistiques très élevées : GARGAROS 695 (plus que Rayquaza), BLIZZARIA 605 | équilibrage | — |
| Aucune évolution pour les Yo-kai | — | (lecture corrigée : une lecture erronée à 6 octets m'avait fait croire « Jibanyan → Bekipan » ; c'est faux) |

## 8. Ce qui n'a pas pu être établi

- Le **créateur** du hack et sa **publication** : aucune trace trouvée en ligne (recherches web et GitHub). Seuls
  les dessinateurs des sprites sont crédités dans la ROM.
- Une éventuelle **modification du moteur** (code) : non décidable par comparaison binaire (§2.4).
- Les **cris** des Yo-kai : non analysés (et les deux fichiers fournis sont identiques, donc aucun « audio Jibanyan » distinct).
