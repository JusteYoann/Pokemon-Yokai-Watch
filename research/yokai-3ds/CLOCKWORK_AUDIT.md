# CLOCKWORK_AUDIT — la recompilation statique et ses possibilités de modding

Audit du 2026-11-14 sur `watchmakerers/clockwork@3047d9e` (2026-11-08). Références : `clockwork:<chemin>:<ligne>`.

**Rappel terminologique.** Clockwork est une **recompilation** statique : le code machine ARM du jeu est traduit
mécaniquement en C (une fonction C par fonction du jeu, nommée par son adresse : `f_00100038`). Ce n'est **pas** une
**décompilation** : il n'y a ni noms de fonctions, ni structures, ni code lisible ; la connaissance du jeu reste à
faire, exactement comme sous émulateur.

## 1. Identité du projet

| Point | Constat | Preuve |
|---|---|---|
| Âge | **17 commits**, premier le **2026-10-14** (un mois) | `git log` |
| Auteurs | comptes « Clockwork » / « watchmakerer » | `git log --format=%an` |
| Licence | MIT (ajoutée le 2026-11-04) ; ImGui MIT | `clockwork:LICENSE`, commit `9292b54` |
| Taille | ~24 700 lignes (runtime C++, outils Rust) | `wc -l` |
| Issues | 7 au total, dont « Mods don't work » (#6) et écrans qui s'étirent (#7) ouvertes ; 3 sur des GPU non détectés sous Windows | recherche GitHub |
| Nightly | publiée à chaque push, auto-mise à jour | `clockwork:README.md`, commit `eb063d3` |

Un projet jeune et rapide, sans historique de stabilité.

## 2. Fonctionnalités : annoncées vs vérifiables

| Fonctionnalité annoncée | Ce que le code montre | Statut |
|---|---|---|
| YW1, YW2 (3 versions), Blasters, YW3, Busters 2, 4 régions | Table `KNOWN_DUMPS` avec les title IDs EUR : YW2 PS `…1B2900`, Blasters `…1CEC00`/`…1CF000`, YW3 `…1D6800` | Présent dans le code |
| Versions européennes | « **The USA releases (and Busters 2) are the tested ones; the other regions are recognized and built the same way but are new.** » | **Non testé par l'auteur** (`clockwork:README.md:30`) |
| Jeu le plus testé | « Psychic Specters is the most played and tested; the others are newer here. » | `README.md:33` |
| Mises à jour (Moon Rabbit Crew) | recompilation du code de la mise à jour | Annoncé (`README.md:41`) ; non testé ici |
| Sauvegardes | une par jeu, import Checkpoint/JKSM | Annoncé (`README.md:60`), `runtime/src/frontend/saves.h` |
| Mods | **RomFS seulement** (fichiers entiers, fichiers dans les archives ARC0, textures) | `clockwork:runtime/src/mods.h:1-14` |
| **Patchs de code** | **Refusés explicitement** : « changes the game's code, which is recompiled ahead of time; it isn't applied » | `clockwork:runtime/src/mods.cpp:136-139` |
| Sans fil local (Rooms) | relais maison ; HLE `nwm::UDS` qui gère Pia (Blasters) | `runtime/src/hle/uds.cpp`, `docs/PLAN.md` |
| Vérification du recompilateur | test différentiel contre `qemu-arm` : instructions de calcul/VFP ; **mémoire et flot de contrôle non couverts** | `clockwork:docs/PHASE1.md:85-99` |
| Couverture (YW2 USA) | 96,7 % de `.text`, **734 sauts indirects non résolus** | `docs/PHASE1.md:45-58` |

## 3. Architecture et conséquences pour le modding

- **Pas d'interpréteur de secours.** Un saut vers une adresse non recompilée arrête le programme
  (`clockwork:runtime/include/recomp.h` : « aborts with the address if it wasn't recompiled » ;
  `docs/ARCHITECTURE.md`). Tout chemin de code rare (fin de jeu, boss d'après-jeu, contenu de mise à jour) est un
  risque de plantage tant qu'il n'a pas été joué.
- **Appels directs = appels C directs.** `bl` devient `f_XXXXXXXX(ctx);` (`clockwork:tools/recomp/src/emit.rs:202,592,606`).
  Seuls les appels indirects passent par `recomp_call_indirect` et la table `lookup.c`. **Il n'existe donc aucun point
  d'interception à l'exécution** pour la plupart des fonctions.
- **Module de jeu.** Le jeu est une bibliothèque partagée compilée chez le joueur ; l'interface hôte
  (`ClockworkHost`) n'expose que `svc`, `call_indirect`, `unhandled`, `coproc`, `trace_enter`
  (`clockwork:runtime/include/recomp_module.h`). **Aucune API de mod, de plugin ou de hook.**
- **Mémoire.** Le jeu adresse un bloc réservé de 4 Gio (`recomp_mem + adresse_guest`) : les **mêmes adresses que
  sous émulateur** (`recomp.h`). Un programme externe ne le voit pas sans aide (adresse de base aléatoire du processus).
- **Réseau.** Le runtime contient déjà du code socket (`runtime/src/net/`), utilisé pour les Rooms : techniquement
  réutilisable, mais rien n'est exposé.

## 4. Méthodes possibles pour Archipelago (toutes à développer)

| Méthode | Principe | Existe ? | Effort / risque |
|---|---|---|---|
| B1. Réécrire le C généré | renommer `f_X` en `f_X_orig` et insérer un crochet `f_X` (avant compilation) | **Testé** sur code synthétique avec le vrai `recomp` (PROTOTYPE_RESULTS.md, B) | Moyen ; fragile si Clockwork change son émetteur ; à refaire à chaque recompilation |
| B2. Ajouter au recompilateur une table de crochets | option `emit --hooks hooks.txt` qui fait B1 proprement | Non | Moyen ; à proposer en amont (MIT) ou à maintenir en fork |
| B3. Serveur local dans le runtime | exposer lecture/écriture de `recomp_mem` par socket (comme le RPC d'Azahar) | Non | Moyen ; fork du runtime |
| B4. Lecture mémoire par le système | `ReadProcessMemory` (Windows) en retrouvant la base | Non | Fragile ; antivirus ; déconseillé |
| B5. Patch de code avant recompilation | appliquer un `code.bps` au `code.bin` extrait, puis `recomp emit` | Non (refusé à l'exécution, `mods.cpp:136`) | Élevé : code ajouté non découvert/recompilé correctement = plantage sans interpréteur |

Point positif réel : une fois un crochet posé, **appeler une fonction interne du jeu** (ex. « donner objet ») depuis
du C natif est trivial et rapide (`f_X(ctx)` avec les registres préparés) : démontré sur code synthétique.

## 5. Bilan

| Besoin Archipelago | Clockwork aujourd'hui | Statut |
|---|---|---|
| Lire la progression | Impossible sans développement (B3/B4) | Non vérifié → à développer |
| Détecter un évènement | Possible par crochets (B1/B2), **à développer** | Probable (prototype synthétique) |
| Recevoir/appliquer des objets | Possible en appelant les fonctions du jeu depuis un crochet, **à développer** | Probable |
| Réutiliser le patch de code du mod YW2 | **Non** : Clockwork n'applique aucun patch de code | **Bloquant** pour YW2 tel quel |
| Version EUR | Reconnue, **non testée par l'auteur** | Non vérifié |
| Stabilité sur partie complète | Aucune donnée publique ; pas d'interpréteur de secours | Non vérifié (risque élevé) |

Clockwork est prometteur comme « port PC », mais **n'offre aujourd'hui aucune surface de modding de code**. Il
exigerait de maintenir un fork du recompilateur et du runtime, pour un projet d'un mois dont l'émetteur peut changer.

## 6. Le troisième candidat découvert : Zakuro (+ 3dsrecomp)

L'intégration YW2 Archipelago existante fournit **Zakuro** (`fearkov/zakuro@565320f`, MIT, 374 commits depuis
2026-09-24), émulateur 3DS en Rust qui exécute du code **recompilé à l'avance par 3dsrecomp** (`fearkov/3dsrecomp@d24e562`, MIT)
avec **retour à l'interpréteur** pour ce qui n'est pas recompilé. Il combine les avantages :

| Point | Zakuro | Preuve |
|---|---|---|
| Jeux Yo-kai **EUR** | YW1, **YW2 PS (`…1B2900`) et YW3 (`…1D6800`) « Playable » avec recompilation** ; Blasters **absent** de la liste | `zakuro:COMPATIBILITY.md:36-38` |
| Patchs de code | `code.bin`/`code.ips`/`code.bps` + `exheader.bin` (dossiers d'Azahar) ; « recompile the game with the mod already in its folder » | `zakuro:README.md` |
| Hooks officiels | **`RECOMP_OVERRIDE(adresse)`** + `RECOMP_ORIGINAL` : remplacer/encadrer n'importe quelle fonction en C | `3dsrecomp:docs/overrides.md` |
| Sécurité | ce qui n'est pas recompilé passe par l'interpréteur (pas d'arrêt brutal) | `3dsrecomp:README.md` |
| Pont externe | stub GDB ajouté **par le mod YW2** (patch 0001), pas en amont | `Yo-kai-Watch-2-Archipelago:source/zakuro/patches/0001-ykw2-gdb-recompile.patch` |
| Blasters de YW2 en solo | patch 0005 « uds solo » (sans fil local seul) | `…/patches/0005-zakuro-uds-solo.patch` |
| Maturité | un auteur principal (349/374 commits) ; « personal experimental project » | `zakuro:README.md`, `git log` |

Zakuro est **en production** pour YW2 EUR + Archipelago (V3.0.0, bêta de 31 versions). C'est l'option « code PC »
la plus crédible aujourd'hui pour YW2 et YW3 ; Clockwork reste l'option à surveiller pour Blasters (voir
RECOMMENDED_ARCHITECTURE.md).
