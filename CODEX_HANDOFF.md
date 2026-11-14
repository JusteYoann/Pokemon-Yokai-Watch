# CODEX_HANDOFF — Yo-kai Watch Multiworld Archipelago (5 jeux)

Passation du 2026-11-14. Auteur des travaux : session Claude Code `session_01C2Mwkw76TmDEcTocvmv5Np`.
Dépôt : `JusteYoann/Pokemon-Yokai-Watch` — branche de passation : `claude/archipelago-multiworld`.

Légende utilisée partout : **✅ TERMINÉ ET TESTÉ** (exécuté et vérifié dans un conteneur Linux) · **🟡 PARTIEL** (code
écrit, partiellement ou pas testé) · **📋 ENVISAGÉ** (analyse/plan seulement) · **⛔ BLOQUÉ** (cause identifiée).
Aucun jeu n'a été testé en jeu avec un serveur Archipelago connecté : voir §6.

---

## 1. Objectif

Un seul joueur humain, **cinq slots Archipelago** sur un même serveur (mode solo), cinq jeux joués en alternance sur un
PC Windows, avec de vrais échanges d'objets de progression entre les jeux, sauvegarde/reprise, et cinq conditions
de victoire :

| # | Jeu | Plateforme / émulateur | Version voulue |
|---|---|---|---|
| A | Yo-kai Watch 2 : Spectres Psychiques | 3DS — Zakuro ou Azahar | EUR (française) |
| B | Yo-kai Watch 3 | 3DS — Zakuro ou Azahar | EUR (française) |
| C | Mario Kart Wii × Yo-kai Watch | Wii — Dolphin | PAL (exigé par la seule intégration trouvée) |
| D | Pokémon Rouge Feu × Yo-kai Watch | GBA — mGBA | fangame personnel de l'utilisateur (« Yo-kai Watch GBA 1.0 ») |
| E | Pokémon Yo-kai Emerald | GBA — mGBA | version française personnalisée du fangame de SnappleRainKirby (@KirbyLemonRain) |

Usage **strictement personnel** (vidéo YouTube + partie privée) : aucune distribution de ROM ni de patch prévue.

## 2. Architecture

```
Archipelago officiel (0.6.9, non forké)  <-- serveur, génération, clients
   custom_worlds/
     yokaiwatch2.apworld            (A, tiers : doryan-meunier, MIT)
     yokaiwatch3                    (B, à créer)
     mkwii.apworld                  (C, tiers : toent/Archipelago-MKWii, MIT)
     pokemon_yokai_firered          (D, à créer)
     pokemon_yokai_emerald.apworld  (E, fork MIT du monde de Flit, construit localement)
Connecteurs : 3DS = stub GDB (Zakuro/Azahar 2124.3) ou RPC UDP Azahar ; Wii = dolphin_memory_engine ;
              GBA = BizHawkClient d'Archipelago + script Lua mGBA (Zunawe/bhc-substitutes, MIT)
```

Principe commun (prouvé par l'intégration YW2 et le patch AP d'Émeraude) : le jeu (patché) expose une zone mémoire ;
le client lit les **flags** (checks) et écrit **un objet à la fois** ; un **compteur d'objets reçus est stocké dans la
sauvegarde du jeu** -> pas de doublon, reprise après déconnexion/redémarrage.

## 3. Dépôts, branches et pistes de code

| Où | Quoi |
|---|---|
| `JusteYoann/Pokemon-Yokai-Watch`, branche `claude/archipelago-multiworld` (= `claude/yokai-watch-archipelago-arch-vugpet`, même historique) | **tout le travail** de cette session |
| `master` du même dépôt | intact (fork pret/pokefirered vanilla). **Ne pas modifier.** |
| `YOKAI_ARCHIPELAGO/` | projet Multiworld (structure demandée par l'utilisateur) |
| `research/yokai-3ds/` | étude Azahar / Clockwork / Zakuro + prototypes (client AP minimal, pont RPC Azahar, crochet Clockwork) |
| `research/yokai-emerald/` | audit du hack Émeraude, équilibrage des 6 Yo-kai (spécification JSON, patcheur binaire, vérificateur) |

Dépôts tiers utilisés (non copiés ; commits validés) :

| Dépôt | Commit | Usage |
|---|---|---|
| ArchipelagoMW/Archipelago | `f5b97c5` (0.6.9) | serveur, génération |
| pret/pokeemerald | `731ad5bfd` | référence vanilla, build anglaise |
| pret/agbcc | `da598c1` | compilateur des décompilations |
| FlitPix/pokeemerald (branche `combo`) | `fd64301` | code C du patch AP Émeraude (**sans licence** : usage privé, crédité) |
| FlitPix/ap-pokeemerald | `c62beb1` | monde AP de Flit (MIT), base de notre APWorld E |
| qigast/pokeemeraude | `2ec3c4d9` | décompilation **française** d'Émeraude (cible SHA-1 `ca666651…`) |
| Zunawe/bhc-substitutes | `8954261` | connecteur Lua mGBA pour les BizHawkClient |
| doryan-meunier/Yo-kai-Watch-2-Archipelago | `6d12594` (V3.0.0) | intégration YW2 complète (APWorld + lanceur + Zakuro) |
| toent/Archipelago-MKWii | `a8949c5` (apworld 0.4.0) | intégration Mario Kart Wii |
| fearkov/zakuro, fearkov/3dsrecomp | `565320f`, `d24e562` | émulateur 3DS « code PC » utilisé par YW2 |
| vyneras/pokefirered (`archipelago-dev`) | — | patch AP Rouge Feu communautaire (inapplicable au fangame, voir D) |

Autre session Claude, non centralisée ici : « Pokémon GBA ROM hack project setup » (inactive depuis le 2026-11-09),
probablement liée au fangame Rouge Feu (sprites Yo-kai). Son contenu n'a pas été lu ; demander à l'utilisateur
où se trouve le **code source du fangame**.

## 4. État exact par jeu

### A — Yo-kai Watch 2 : Spectres Psychiques — 🟡

- ✅ Intégration tierce complète et récente : `doryan-meunier/Yo-kai-Watch-2-Archipelago` V3.0.0 (EUR, APWorld FR/EN,
  patch de code BPS appliqué localement, client Python, pont **GDB**, Zakuro fourni, Azahar 2124.3 en repli).
- ✅ Son APWorld français génère dans notre Multiworld (AP 0.6.9) avec Émeraude et avec Yo-kai Emerald.
- ❌ Non testé en jeu ici (pas de dump 3DS). Le patch du jeu (source C) **n'est pas publié** par l'auteur.
- Choix : **réutiliser tel quel** (ne pas recréer). Option Ψ Blasters : seulement sous Zakuro (bug Azahar #170).
- Docs : `research/yokai-3ds/*.md`.

### B — Yo-kai Watch 3 — 📋 / ⛔

- Aucun projet existant. Zakuro déclare YW3 EUR (`00040000001D6800`) « Playable ».
- Plan : patch de code (`code.bps`) + boîte aux lettres en RAM + client (même modèle que YW2), développé sur Azahar
  (stub GDB, RPC UDP 45987), joué sur Zakuro. Sonde lecture seule prête : `research/yokai-3ds/poc/probe_azahar.py`.
- ⛔ Exige le dump de l'utilisateur et de la rétro-ingénierie ARM (fonctions « donner objet », flags de chapitres).
- `yw_save` (YureiResearchInstitute) : déchiffre les sauvegardes YW3 **japonaises** ; EUR non vérifié.

### C — Mario Kart Wii × Yo-kai Watch — 🟡 (recherche) / ⛔ (exécution)

- Base : `toent/Archipelago-MKWii` (MIT, apworld 0.4.0, AP ≥ 0.6.6) — client autonome via `dolphin_memory_engine`,
  **ISO PAL `RMCP01` uniquement**, Dolphin 2512+, 192 checks de coupes + 128 de courses, victoire = N « Victory Trophy ».
- Mods Yo-kai repérés via des extraits de recherche web (pages non lues : `gamebanana.com` bloqué par le réseau de la
  session) : Jibanyan/Luigi (gamebanana 413572), Jibanyan/Toadette (653194), icônes (455364). Compatibles seulement en
  remplacement de fichiers `.szs` via Riivolution (ID `RMCP01` conservé) ; incompatibles avec CTGP, Retro Rewind,
  MKW-SP, Pulsar.
- ⛔ L'exécution de ce monde tiers a été **refusée par une règle de permission** de l'environnement Claude (pas encore
  autorisée par l'utilisateur). Rapport : `YOKAI_ARCHIPELAGO/DOCUMENTATION/chantiers/C_mario_kart_wii.md`.

### D — Pokémon Rouge Feu × Yo-kai Watch — 📋 / ⛔

- ROM « Yo-kai Watch GBA 1.0 » (SHA-1 `40c59a9f…`, 32 Mio, en-tête BPRE) : **build de pret/pokefirered compilée avec
  agbcc** (pas de CFRU), 304 Yo-kai dans les emplacements d'espèces existants, texte français, 760 dresseurs,
  426 cartes, un 19e type ; blocs de sauvegarde de taille vanilla.
- Patch AP Rouge Feu communautaire (Vyneras, apworld 1.1.5) : **inapplicable** (MD5, bsdiff, nom de ROM, sauvegarde).
- Adresses RAM confirmées sous mGBA : `gSaveBlock1Ptr` 0x03005568, `gSaveBlock2Ptr` 0x0300556C, `gMain` 0x03003650.
- ⛔ Intégration complète = **code source du fangame** requis (ou au minimum `.map`/`.elf` de la build 1.0).
  Prototype connecteur-seul possible (flag `FLAG_BADGE01_GET` 0x820 ; compteur `VAR_0x409E` supposé libre, non prouvé).
- Rapport : `YOKAI_ARCHIPELAGO/DOCUMENTATION/chantiers/D_pokemon_yokai_firered.md`.

### E — Pokémon Yo-kai Emerald — ✅ (anglais + AP) / ⛔ (français) / ❌ (communication)

Le hack binaire du créateur ne peut pas recevoir le code AP (testé : refusé par MD5 ; forcé -> ROM non démarrable).
Il est donc **reconstruit en source** :

```
fork AP de Flit (pret + code AP) --[yokai_source_patch.py + ROM du hack de l'utilisateur]--> sources Yo-kai
  -> make (agbcc) -> ROM « pokemon emerald / yokai ap v0.1 »
  -> make extract -> base_patch.bsdiff4 + extracted_data.json (418 espèces)
  -> make_apworld.py -> pokemon_yokai_emerald.apworld
```

Six Yo-kai (n° interne 412-417, Pokédex national 387-392, Hoenn 203-208), fiches **validées par l'utilisateur** dans
`research/yokai-emerald/balance/yokai_balance.json` (+ `.resolved.json`) :

| Yo-kai | Rang | Types | PV/Atq/Déf/AtqSp/DéfSp/Vit (total) | Talent | Zone (niveaux, taux) |
|---|---|---|---|---|---|
| Jibanyan | D | Feu/Combat | 60/85/50/60/50/95 (400) | Brasier | **starter obligatoire** (3 Poké Balls), niv. 5 |
| Komasan | D | Feu | 70/45/65/85/75/55 (395) | Torche | Bois Clémenti (6-8, 15 %) |
| Komajiro | C | Électrik | 65/50/60/100/65/95 (435) | Statik | Route 110 (12-15, 15 %) |
| Whisper | C | Spectre | 85/35/80/70/100/55 (425) | Lévitation | Grotte Granite 1F/B1F/B2F (10-13, 15 %) |
| Blizzaria | A | Glace | 75/45/70/115/105/95 (505) | Lévitation | Route 113 (17-20, 15 %) |
| Gargaros | A | Roche/Ténèbres | 100/135/105/40/90/45 (515) | Intimidation | Sentier Sinuroc (20-23, 15 %) |

Décisions : « Regard Touchant » (6e gén.) -> Rugissement (validé) ; « Protection » = Reflect, « Lance-Boue » = Mud Sport
(noms français de 2005, lecture littérale) ; Whisper niv. 38 = doublon d'Onde Folie (Feinte proposée, non validée) ;
même talent dans les 2 emplacements ; aucune évolution ; Pokédex de Komajiro/Whisper corrigés (bug du hack : pointeur
nul) ; cris empruntés ; crédits SnappleRainKirby/Ludo/SonGoku/Nicowico (panneau de Bourg-en-Vol).

Testé ✅ : build pret anglaise + couche Yo-kai (73/73, sprites identiques au hack, démarre dans mGBA) ; build fork AP +
couche Yo-kai (73/73, nom de ROM) ; `make extract` ; APWorld ; génération YW2 + Yo-kai Emerald (183/187 objets croisés) ;
patch `.apyokaiemerald` appliqué à une Émeraude US vanilla -> 73/73.
⛔ Build française : la compilation de `qigast/pokeemeraude` a été **refusée deux fois par une règle de permission**
de l'environnement Claude (non technique). La ROM France de l'utilisateur est la cible exacte (SHA-1 `ca666651…`,
MD5 `2c00e335…`).
❌ Communication mGBA <-> serveur jamais testée.

Historique également disponible : un patcheur **binaire** du hack (`research/yokai-emerald/balance/patch_rom.py`,
93/93 contrôles) — utile pour jouer au hack équilibré **sans** AP ; la voie retenue pour l'AP est la source.

## 5. Fonctionnalités développées

| Composant | Fichier | État |
|---|---|---|
| Générateur de sources Yo-kai (EN/FR) | `YOKAI_ARCHIPELAGO/PATCHES/pokemon_yokai_emerald/yokai_source_patch.py` | ✅ EN ; 🟡 FR (non compilé) |
| Adresses des sprites de Nathan/Katie dans le hack | `.../pokemon_yokai_emerald/player_gfx_offsets.json` | ✅ |
| Fabrique de l'APWorld E | `YOKAI_ARCHIPELAGO/APWORLDS/pokemon_yokai_emerald/make_apworld.py` | ✅ (`--base us`) ; 🟡 (`--base fr`) |
| Construction bout en bout E | `YOKAI_ARCHIPELAGO/SCRIPTS/build_emerald.sh` | 🟡 (étapes testées une à une, script complet non exécuté ; branche FR jamais exécutée) |
| Vérificateur de build E | `YOKAI_ARCHIPELAGO/TESTS/verify_emerald_build.py` | ✅ |
| Application d'un `.apyokaiemerald` | `YOKAI_ARCHIPELAGO/TESTS/apply_yokai_patch.py` | ✅ |
| Extracteur du hack | `research/yokai-emerald/tools/yokai_extract.py` | ✅ |
| Spécification + résolution des noms FR | `research/yokai-emerald/balance/` | ✅ |
| Client AP minimal + boîte aux lettres + pont RPC Azahar (3DS) | `research/yokai-3ds/poc/` | ✅ contre un vrai serveur, jeu simulé |
| Pilote mGBA sans écran (captures, états) | `research/yokai-emerald/poc/mgba_drive.sh` | ✅ |

## 6. Tests réellement effectués vs restants

| Test de validation (§15 de la mission) | État |
|---|---|
| 1 démarrage des 5 jeux | E ✅ (écran titre) ; D ✅ (menu, par l'agent D) ; A, B, C ❌ |
| 2 connexion des 5 clients au même serveur | ❌ |
| 3 un check réel par jeu | ❌ |
| 4 un objet reçu par jeu | ❌ |
| 5 échanges entre jeux | ✅ dans la logique de génération uniquement ; ❌ en jeu |
| 6 sauvegarde / reconnexion | ❌ (mécanisme compteur-en-sauvegarde documenté) |
| 7 génération 5 slots | 🟡 2 slots OK (YW2 + E) ; C non exécuté ; B, D sans monde |
| 8 logique | ✅ pour les générations faites (playthrough calculé par AP) |
| 9 victoire détectée | ❌ |
| 10 installation sur Windows propre | ❌ |

## 7. Blocages

1. Compilation de la décompilation française d'Émeraude : règle de permission de l'environnement Claude (à lancer
   ailleurs ou à autoriser).
2. Mario Kart Wii : exécution du monde tiers non autorisée dans l'environnement Claude ; ISO **PAL** requis ;
   pages GameBanana inaccessibles depuis ce réseau.
3. Rouge Feu : code source du fangame absent.
4. Yo-kai Watch 3 : dump + rétro-ingénierie.
5. Fusion « code AP de Flit × décompilation française » jamais tentée (risque de conflits sur les textes).
6. Licences : le code C de Flit et les décompilations pret/qigast n'ont pas de fichier de licence (usage privé, crédité) ;
   les graphismes du hack appartiennent à SnappleRainKirby et à ses dessinateurs (lus localement, jamais commités).

## 8. Dépendances et installation (Linux / WSL2 Ubuntu 24.04)

```sh
sudo apt install build-essential git libpng-dev binutils-arm-none-eabi gcc-arm-none-eabi libnewlib-arm-none-eabi \
     nodejs python3-venv xvfb xdotool mgba-qt imagemagick
python3 -m venv .venv && . .venv/bin/activate
pip install pillow bsdiff4
git clone https://github.com/ArchipelagoMW/Archipelago && cd Archipelago && git checkout f5b97c5
pip install -r requirements.txt "setuptools<81" && python ModuleUpdate.py --yes
```

Fichiers personnels nécessaires (jamais dans le dépôt) : ROM du hack Yo-kai Emerald (SHA-1 `ff71db05…`), Émeraude US
(`f3ae0881…`, reproductible à l'octet par `make` dans pret/pokeemerald) et/ou France (`ca666651…`), ROM du fangame
Rouge Feu (`40c59a9f…`), dumps 3DS EUR, ISO MKW PAL.

## 9. Compilation

Pokémon Yo-kai Emerald, version anglaise compatible AP (chaque étape a été exécutée et vérifiée) :

```sh
YOKAI_ARCHIPELAGO/SCRIPTS/build_emerald.sh <hack.gba> <emeraude_US.gba> us <dossier_de_travail>
# -> <travail>/apworld/pokemon_yokai_emerald.apworld ; copier dans Archipelago/custom_worlds
```

Version française : même script avec `fr` et la ROM France (fusion qigast/pokeemeraude ; non testé).
Génération : YAML `game: Pokemon Yo-kai Emerald` + `game: Yo-kai Watch 2` (modèle FR du dépôt doryan-meunier) ;
`SKIP_REQUIREMENTS_UPDATE=1 python Generate.py --player_files_path Players --outputpath out`.
Application d'un patch : `python YOKAI_ARCHIPELAGO/TESTS/apply_yokai_patch.py out/*.apyokaiemerald <base.gba> <sortie.gba>`
(depuis le dossier Archipelago). Vérification : `python3 YOKAI_ARCHIPELAGO/TESTS/verify_emerald_build.py <rom> <map> --hack <hack.gba>`.

## 10. Prochaines étapes prioritaires

1. **E — communication réelle** : mGBA + `connector_bizhawkclient_mgba.lua` + « BizHawk Client » d'Archipelago + serveur
   local ; partie neuve, sortie du camion, recevoir un objet (`/send` sur la console du serveur), envoyer un check,
   sauvegarder, relancer, vérifier l'absence de doublon.
2. **E — version française** : fusion `qigast/pokeemeraude` × fork AP de Flit, traduction des textes AP, `--base fr`.
3. **C** : exécuter `toent/Archipelago-MKWii` (avec l'accord de l'utilisateur), générer avec E + A, tester sous Dolphin
   PAL ; vérifier un mod Jibanyan en remplacement `.szs` via Riivolution.
4. **A** : test en jeu de l'intégration YW2 V3 (sur le PC de l'utilisateur) dans le Multiworld.
5. **D** : obtenir le code source du fangame ; porter le code AP (réception d'objets, compteur en sauvegarde) et créer
   l'APWorld `pokemon_yokai_firered`.
6. **B** : sonde sur le PC de l'utilisateur, rétro-ingénierie, patch + client sur le modèle de YW2.
7. Multiworld 5 slots, scripts Windows de lancement, tutoriel français (non commencé).
