# ARCHIPELAGO_COMPATIBILITY — Pokémon Émeraude dans Archipelago

## 1. Les intégrations existantes

| Intégration | Où | Version | Licence | Code C du patch de base |
|---|---|---|---|---|
| **Officielle** « Pokemon Emerald » (Zunawe) | `ArchipelagoMW/Archipelago` `worlds/pokemon_emerald` | monde **2.6.0**, AP ≥ 0.6.1 (testé avec 0.6.9, `f5b97c5`) | MIT (monde) | **non trouvé** publiquement (recherche GitHub et web) ; seul `base_patch.bsdiff4` est livré |
| « Pokémon Emerald Version (Flit's ver.) » | `FlitPix/ap-pokeemerald` (`c62beb1`, 2026-11-07) | monde séparé, installable en `custom_worlds` | MIT (monde) | **public** : `FlitPix/pokeemerald`, branche `combo` (`fd64301`) — fork de pret, **sans fichier de licence** |
| Ancien essai | `luctowers/pokeemerald-archipelago` | 2023, inactif | — | — |

## 2. Fonctionnement du monde officiel (lu dans le code)

| Aspect | Constat | Référence |
|---|---|---|
| ROM requise | **Émeraude US**, MD5 `605b89b67018abcea91e693a4dd25be3` | `rom.py:100`, `__init__.py:88-92` |
| Patch | `.apemerald` = `base_patch.bsdiff4` (ROM entière modifiée) + jetons par graine (objets aux emplacements, options) | `rom.py` (`procedure`) |
| Nom écrit dans la ROM | `pokemon emerald version / AP 5` en `0x108` ; le client refuse toute autre ROM | `client.py:23` |
| Données du jeu | `data/extracted_data.json` **généré depuis la build du patch** : 412 espèces, 1 364 emplacements, adresses RAM/ROM | `data.py` |
| Emplacements | objets au sol/cachés, dons de PNJ, badges, CT/CS, et selon options : dresseurs, Pokédex (dexsanity), baies… | `locations.py`, `options.py` |
| Victoire | champion, Steven, Norman, légendaires… (option `goal`) | `options.py`, `client.py` |
| Détection des checks | lecture des **flags** de la sauvegarde (`SaveBlock1 + 0x1450`, 2×0x96 octets) ; Pokédex `SaveBlock2 + 0x28` (0x34 octets = 412 bits) | `client.py:258-286` |
| Réception | le client écrit **un** objet dans `gArchipelagoReceivedItem` (id, index, plein, affichage) ; le **compteur d'objets reçus est dans la sauvegarde** (`SaveBlock1 + 0x3778`) | `client.py:495-528` |
| Anti-doublon / reprise | l'index envoyé = compteur + 1 ; après reconnexion, le serveur renvoie la liste et le jeu reprend au compteur | idem |
| Sécurité | lectures et écritures **gardées** (pointeurs de sauvegarde inchangés, dans le terrain) | `bizhawk.guarded_read/write` |
| Émulateur | **BizHawk** (client « BizHawk Client ») ; **mGBA possible** via le script `connector_bizhawkclient_mgba.lua` (`Zunawe/bhc-substitutes`, MIT, mGBA ≥ 0.10) | `docs/setup_en.md` ; `bhc-substitutes/mgba/README.md` |
| Changements du jeu | sac agrandi (**format de sauvegarde changé**), évolutions par échange remplacées, nombreux raccourcis… | `docs/rom_changes_en.md` |

## 3. Le hack peut-il être utilisé tel quel ? Non (testé)

Tests **réels** (PROTOTYPE_RESULTS.md, C1-C3) :
1. Validation Archipelago de la ROM du hack : **refusée** (`File hash does not match`).
2. En forçant l'application du patch sur le hack : la ROM obtenue n'a que **16 %** d'octets en commun avec la vraie
   ROM AP. Dans mGBA, elle reste sur un **écran blanc** (aucun démarrage en 15 s).
3. Contrôle : la même graine appliquée à l'Émeraude vanilla compilée est **acceptée** et **démarre** jusqu'à
   l'écran titre dans mGBA.

Raisons structurelles, indépendantes du hash :
- le patch est un **bsdiff de la ROM entière** depuis la vanilla : il réécrit le code et les tables aux adresses de
  la vanilla, alors que le hack a tout déplacé (build modern, ROM_ANALYSIS.md §2) ;
- les adresses RAM/ROM du client (`extracted_data.json`) et les offsets de sauvegarde codés en dur ne
  correspondent pas (sauvegarde du hack +4 octets, Pokédex de 418 espèces = 53 octets au lieu de 52) ;
- le monde ne connaît que 412 espèces : ni rencontres Yo-kai, ni dexsanity Yo-kai, ni mélange des Yo-kai.

## 4. Ce qu'il faut pour un « Pokémon Yo-kai Emerald » Archipelago

1. **Un patch de base reconstruit** = décompilation + code AP + contenu Yo-kai, compilé.
2. **Un monde forké** (MIT) : nom de jeu distinct (« Pokemon Yo-kai Emerald »), `extracted_data.json` régénéré
   depuis **notre** build (418 espèces, adresses), hash de la ROM de base attendue (française si base
   `pokeemeraude`), lecture du Pokédex sur 53 octets, nom de ROM distinct pour le client.
3. **Le client** : celui du monde forké (BizHawkClient), utilisable avec BizHawk **ou** mGBA + connecteur Lua.
4. Les **légendaires ajoutés en sauvage** par le hack (Jirachi ×2, Celebi, Ho-Oh : 4 emplacements, plus Muciole
   à la place de Lumivole Route 117) sont à retirer ou à intégrer à la logique (ils pourraient court-circuiter les
   options de légendaires).

## 5. Choix du patch de base AP

| | Officiel (Zunawe) | Flit |
|---|---|---|
| Monde dans Archipelago officiel | oui (testé ici : génération OK) | non (custom_worlds) |
| Code C disponible | **non trouvé** → demander à Zunawe | **oui**, public, sans licence → demander à Flit |
| Outil d'extraction des données | inconnu | à vérifier dans `FlitPix/pokeemerald` |

Décision proposée : **commencer par le fork de Flit** (seul code C disponible) et **écrire aux deux auteurs**. Si
Zunawe publie ou partage le code officiel, basculer dessus : c'est le monde que la communauté connaît.
