> **Statut utilisateur du16 novembre :** Emerald, YW2 et Mario Kart Wii sont déclarés fonctionnels. Le mod visuel Yo-kai de MKW manque encore ; YW1 est la seule intégration absente. Préserver ces acquis. Les anciens états de gel et les limites des essais locaux ci-dessous sont historiques ; ne pas les confondre avec le statut actuel communiqué par l’utilisateur. Voir `YOKAI_ARCHIPELAGO/DOCUMENTATION/ETAT_DU_PROJET.md`.

> **Jalon courant — import massif du 16 novembre :** [rapport et limites](YOKAI_ARCHIPELAGO/DOCUMENTATION/FRLG_IMPORT_MASSIF.md). 625 checks par défaut (626 avec Terr’heure),74 anciens IDs conservés ; transport3, sauvegarde1 et registre256 dresseurs. Les descriptions15/74 ci-dessous sont historiques. Le graphe de progression reste regroupé et les cinq jeux ensemble ne sont pas validés.

Tests du jalon :617 détecteurs natifs et persistance à froid,2057 assertions ;37 protections ;36 contrôles avec vrai serveur/mGBA dont Wyatt et un dresseur ordinaire joués ;5 seeds résolubles à trois mondes. Captures et256 victoires sont vérifiées par fixtures natives, pas par166 captures et256 combats joués.

# AGENTS.md — consignes pour les agents (Codex, Claude…)

Lire d'abord `CODEX_HANDOFF.md` (état exact, décisions, blocages) puis
`YOKAI_ARCHIPELAGO/DOCUMENTATION/ETAT_DU_PROJET.md`.

## Ce dépôt

- La racine est une décompilation **pret/pokefirered** (Rouge Feu vanilla) appartenant à l'utilisateur. Son code
  (`src/`, `include/`, `data/`, `graphics/`, `Makefile`…) n'a **pas** été modifié par le projet Multiworld :
  ne pas y toucher sans demande explicite.
- Le projet Multiworld vit dans :
  - `YOKAI_ARCHIPELAGO/` — produit (APWORLDS, CONNECTORS, PATCHES, CONFIG, SCRIPTS, TESTS, DOCUMENTATION) ;
  - `research/yokai-3ds/` — études et prototypes 3DS réutilisables (YW1/YW2 ; YW3 historique uniquement) ;
  - `research/yokai-emerald/` — audit et équilibrage de Pokémon Yo-kai Emerald.
- Branche de départ : `claude/archipelago-multiworld` à `4617e348`. Branche Codex : `codex/archipelago-five-games-20261114`. Ne jamais pousser sur `master`, ne jamais réécrire l'historique
  publié (`push --force` interdit).

## Fichiers à ne pas modifier sans raison

| Fichier | Pourquoi |
|---|---|
| `research/yokai-emerald/balance/yokai_balance.json` | fiches des 6 Yo-kai **validées par l'utilisateur** : toute modification exige son accord |
| `research/yokai-emerald/balance/yokai_balance.resolved.json` | régénéré par `resolve_names.py`, ne pas éditer à la main |
| `YOKAI_ARCHIPELAGO/PATCHES/pokemon_yokai_emerald/player_gfx_offsets.json` | adresses mesurées dans le hack (SHA-1 `ff71db05…`) |
| `YOKAI_ARCHIPELAGO/PATCHES/pokemon_yokai_emerald/yokai_source_patch.py` | générateur testé (73/73) : ajouter des étapes, ne pas changer les ancres sans rebuild + vérification |
| `research/**/*.md` | rapports datés (historique) : compléter par de nouveaux documents plutôt que réécrire |

## Interdits

- Aucune ROM, ISO, dump 3DS, sauvegarde, `base_patch.bsdiff4` contenant des graphismes du créateur, `.apworld` construit
  avec ces données, capture de jeu ou clé dans git. `.gitignore` de `research/yokai-emerald/` les exclut déjà ;
  vérifier `git status` avant chaque commit.
- Ne pas présenter un test simulé ou non exécuté comme réussi : chaque document distingue testé / non testé.
- Ne pas remplacer silencieusement une attaque, une stat ou un emplacement validé.

## Éviter les conflits entre les cinq jeux

Un dossier par jeu dans chaque catégorie (`APWORLDS/<jeu>/`, `PATCHES/<jeu>/`, `DOCUMENTATION/chantiers/<lettre>_<jeu>.md`).
Un agent ne modifie que le dossier de son chantier ; les fichiers communs (`CONFIG/`, `SCRIPTS/` génériques,
`ETAT_DU_PROJET.md`, `CODEX_HANDOFF.md`) sont modifiés par un seul coordinateur à la fois. Noms de jeux Archipelago
distincts (« Pokemon Yo-kai Emerald » ≠ « Pokemon Emerald ») et clés de réglages distinctes pour que tous les mondes
coexistent dans `custom_worlds/`.

## Tests

```sh
# Yo-kai Emerald (après build) — 73 contrôles
python3 YOKAI_ARCHIPELAGO/TESTS/verify_emerald_build.py <build>/pokeemerald_ap_flit.gba <build>/pokeemerald_ap_flit.map --hack <hack.gba>
# Patcheur binaire du hack (variante sans AP) — 93 contrôles
python3 research/yokai-emerald/balance/patch_rom.py <hack.gba> out.gba && python3 research/yokai-emerald/balance/verify_rom.py <hack.gba> out.gba
# Client AP minimal 3DS contre un vrai serveur (jeu simulé)
python research/yokai-3ds/poc/run_poc.py --archipelago <Archipelago> --multidata <AP_xxx.zip>
# Génération Multiworld
cd <Archipelago> && SKIP_REQUIREMENTS_UPDATE=1 python Generate.py --player_files_path Players --outputpath out
```

Démarrage sans écran : `research/yokai-emerald/poc/mgba_drive.sh <rom> <dossier> "<étapes>"` (Xvfb + xdotool,
`audioSync=0`, `SDL_AUDIODRIVER=dummy` ; voir l'en-tête du script).

## Compiler

Voir `CODEX_HANDOFF.md` §8-9. Résumé : `YOKAI_ARCHIPELAGO/SCRIPTS/build_emerald.sh <hack> <base> us|fr <travail>`.
Les décompilations se compilent avec **agbcc** (`pret/agbcc`, `./build.sh` puis `./install.sh <decomp>`) ; `make extract`
du fork de Flit demande Node.js et `bsdiff4` (Python) et la ROM de base copiée en `pokeemerald.gba` à la racine du build.

## Reprendre sans repartir de zéro

1. Ne pas réauditer : les rapports existent (§3 et §4 de `CODEX_HANDOFF.md`).
2. Priorité actuelle : randomisation Rouge Feu selon `YOKAI_ARCHIPELAGO/DOCUMENTATION/CAHIER_DES_CHARGES_FIRERED_20261114.md`, puis YW1 EUR, YW2 EUR et Mario Kart Wii PAL. Emerald est en attente à la demande de l’utilisateur ; ne pas redemander immédiatement ses fichiers.
3. Mettre à jour `ETAT_DU_PROJET.md` et le journal du chantier à chaque jalon, avec les commits.

## Périmètre définitif — décision du 14 novembre 2026

A : Yo-kai Watch 1 EUR ; B : Yo-kai Watch 2 Spectres Psychiques EUR ; C : Mario Kart Wii PAL avec mods visuels Yo-kai ; D : fangame Rouge Feu ; E : Yo-kai Emerald (en attente). Yo-kai Watch 3 est abandonné. Conserver seulement son historique utile aux transports 3DS.

Ne pas supprimer les corrections Emerald déjà réalisées : les geler et documenter leur niveau de test. Les anciennes permissions refusées dans l’environnement Claude ne sont pas des refus applicables automatiquement à la mission actuelle. Une génération ou un test mémoire simulée ne prouve pas une communication avec un jeu réel.


## Jalon Rouge Feu et limites à préserver

Le code AP est dans `YOKAI_ARCHIPELAGO/PATCHES/pokemon_yokai_firered/` ; l’appliquer au snapshot complet RC1, jamais au moteur vanilla de cette racine. Branche du vrai source locale `codex/firered-archipelago-randomizer-20261114` depuis `a589cf00`, jalon `d14b93cb`. Le code d’intégration est publié sur la branche de coordination ; les assets du snapshot restent locaux.

Quinze checks actifs, Surf seul objet de progression randomisé. Ne pas réintroduire sa remise gratuite au Safari. Les autres clefs sont encore natives : avant de les retirer, vérifier restaurations, cinématiques et accès. L’APWorld n’est pas un randomizer Kanto complet. Les 301 espèces actives et les systèmes du fangame sont intacts.

La sauvegarde AP occupe SB2+0xE20 sur64 octets. Ne pas utiliser SB1 unused_3A94 (Aspirateur), ni le début/fin de filler_B20 (Blasters/monstre aspiré). Étendre le bitmap de checks exige une nouvelle étude du protocole, actuellement 8 badges +7 collectes. Les tests réseau préparent le contexte d’interaction mais exécutent réellement les scripts natifs, sans poser leurs flags.

Le groupe compte cinq personnes et cinq slots, pas un joueur à cinq jeux. Voir `CONFIG/createurs/`. Garder les modèles non jouables hors du dossier fourni à Generate.py. Les trois mondes YW2/MKW/FR se génèrent réellement ; cela ne valide pas une partie à cinq jeux.


## Priorité active — extension du 16 novembre 2026

Le jalon quinze checks décrit plus haut est historique. Lire `DOCUMENTATION/FRLG_EXTENSION_VALIDEE.md` sous YOKAI_ARCHIPELAGO :74 checks, Flash/Surf randomisés, sauvegarde1/transport2. Source locale `codex/firered-archipelago-checks-20261114`, commit `9a35394a`. Les IDs initiaux restent immuables. Le tableau comparatif FRLG est un inventaire avant extension, pas une liste de checks tous validés.

Terr’heure RNG : option désactivée par défaut ; item_rule et EXCLUDED interdisent progression/pièges. Aucune quête postgame. Les assistants emploient le compteur Kanto natif des captures (premières151 entrées), pas le nombre vu ni toutes301 espèces. Ne pas étendre silencieusement ce compteur. Le pool doit garder un exemplaire de Surf et de Flash, avec leurs remises originales supprimées.

La liste publiée et le bitmap natif sont liés par SHA256 ; régénérer ROM/profil/package/seed ensemble après modification. La sauvegarde64octets et sa version1 sont indépendantes du protocole2. Ne pas remplacer la garde YoppleAPBusy par YoppleInDungeon (ce dernier est vrai dans les simples grottes). Ne pas distribuer pendant les états temporaires du journal.
