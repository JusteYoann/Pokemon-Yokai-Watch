# GAME_COMPATIBILITY — les trois jeux, version européenne

Statuts : **Confirmé** (preuve dans le code, la doc d'un projet qui l'utilise, ou un test), **Probable** (indices
concordants, pas de test), **Non vérifié**, **Bloquant**. Aucun jeu commercial n'a été exécuté pendant cet audit :
les dumps ne sont pas disponibles ici et n'ont pas été téléchargés. Tout « fonctionne en jeu » ci-dessous vient de
sources tierces citées.

Identifiants de titre (EUR) — `clockwork:runtime/src/frontend/games.h:51-58`, `zakuro:COMPATIBILITY.md` :

| Jeu | Title ID EUR | Archives de langue |
|---|---|---|
| Yo-kai Watch 2 : Spectres Psychiques | `00040000001B2900` | `yw2_lg_<lg>.fa` dont `fr` (`…/installation/installer.py`) |
| Yo-kai Watch 3 | `00040000001D6800` | `yw_lg_<lg>.fa` (Albatross `YW3.cs`) |
| Blasters : Peloton du Chat Rouge | `00040000001CEC00` | `ywb_lg_<lg>.fa` (Albatross `YWB.cs:42`) |
| Blasters : Escadron du Chien Blanc | `00040000001CF000` | idem |
| Mise à jour d'un titre (ex. Moon Rabbit Crew) | `0004000E` + 8 derniers chiffres du titre | convention 3DS (`ykap/games.py`) |

Chaque région est un **code.bin différent** (`games.h:30-35` : « Each region's release is its own code (laid out
differently) »). Aucune adresse USA ne doit être réutilisée pour l'EUR sans vérification.

---

## Jeu A — Yo-kai Watch 2 : Spectres Psychiques (EUR)

| Question | Azahar | Clockwork | Zakuro (3e option) |
|---|---|---|---|
| Exécution | **Confirmé** : le mod YW2 AP V3 valide Azahar **2124.3** sur la version EUR (`README.md` du mod, `azahar.py:30`) | **Probable** : reconnu (`games.h:55`) ; « the most played and tested » mais **USA** ; EUR « new » (`README.md:30-33`) | **Confirmé** : « Playable », recompilé (`COMPATIBILITY.md:37`) ; défaut du lanceur du mod |
| Textes français | **Confirmé** : langue de la console = Français (archive `yw2_lg_fr.fa` patchée par le mod) | **Probable** : « European releases are shown in the language picked on the Library tab » | **Confirmé** : réglage « Langue du jeu » (`INSTALLATION_FR.md:208`) |
| Sauvegardes | **Confirmé** (le mod y lie la progression ; « sauvegardez en jeu ») | **Probable** : par jeu ; import Checkpoint/JKSM | **Confirmé** (`%APPDATA%\ykw2-ap\zakuro`) ; **séparées** d'Azahar |
| Cinématiques / évènements | **Probable** (partie complète jouée par la bêta du mod) ; bugs connus : boss JPN #1636, Vulkan #2172 | Non vérifié en EUR | **Probable** (même source) |
| Ψ Blasters intégré à YW2 | **Bloquant probable** : issue #170 ouverte (sans fil local cassé) | Probable (HLE UDS + Pia, `uds.cpp`) — non testé | **Confirmé** : patch 0005 « Blasters joués seul » |
| Intégration AP existante | **Confirmé** : GDB stub, patch code.bps, boîte en `0x0091C000` | **Bloquant** : Clockwork n'applique pas les patchs de code (`mods.cpp:136-139`) | **Confirmé** : intégration par défaut |
| Adaptation possible | — | Seulement en refaisant le patch en crochets C (CLOCKWORK_AUDIT §4) : des mois | — |

**Conclusion A** : le travail existe et marche sur Azahar et Zakuro. Pour nous, YW2 se **réutilise**, il ne se
redéveloppe pas (voir ARCHIPELAGO_FEASIBILITY.md §3 sur les conditions de réutilisation).

## Jeu B — Yo-kai Watch 3 (EUR)

| Question | Azahar | Clockwork | Zakuro |
|---|---|---|---|
| Version EUR | **Non vérifié** (aucune issue trouvée, aucune liste de compatibilité consultée ne la cite) | **Non vérifié** (reconnue, « new ») | **Confirmé (déclaratif)** : « Playable », recompilé (`COMPATIBILITY.md:38`) |
| Stabilité générale | Non vérifié | Non vérifié | « Playable = from the start through the game » selon l'auteur ; non testé ici |
| Fonctions de Clockwork opérationnelles | — | Lancement + rendu supposés ; aucun rapport public d'une partie complète | — |
| Modifier les récompenses | **Probable** : récompenses en données (`.cfg.bin` dans `yw_a.fa`), éditables par Albatross (YW3 supporté) et livrables par `romfs`/`romfs_ext` ; ou patch code | Données : **Probable** (mods RomFS/ARC0 supportés) ; code : à développer | Comme Azahar (mêmes dossiers de mods) |
| Détecter les évènements | Patch de code + boîte, ou lecture de flags par RPC | Crochets C à développer | Patch de code + overrides 3dsrecomp |
| Client AP | Faisable (même schéma que YW2) | Faisable avec fork | Faisable (pont GDB du mod YW2 à réutiliser) |

Spécificités YW3 qui pèsent sur l'APWorld : deux héros (Nate / Hailey) et histoires alternées ; Busters T (mode
Blasters intégré) ; chapitres et quêtes **différents** de YW2 : aucune adresse ni table du mod YW2 ne s'applique.
Sauvegarde : `yw_save --game yw3` déchiffre/chiffre (support **japonais** confirmé ; EUR **non vérifié**).

## Jeu C — Yo-kai Watch Blasters (EUR) : Chat Rouge / Chien Blanc / Moon Rabbit Crew

| Question | Azahar | Clockwork | Zakuro |
|---|---|---|---|
| Version EUR | **Non vérifié** (aucune issue spécifique trouvée) | **Non vérifié** (reconnue) ; issue #5 : Blasters « unselectable » sous Windows v0.5.0 (fermée) | **Non vérifié** : **absent** de `COMPATIBILITY.md` |
| Moon Rabbit Crew | Mise à jour v2.0 installée comme sur console : Probable | « Blasters' Moon Rabbit Crew » cité explicitement (`README.md:41`) : annoncé | « drop updates in the same folder » : Probable |
| Missions, boss | Non vérifié | Non vérifié | Non vérifié |
| Jeu solo et sans fil local | **Risque** : Blasters s'appuie sur Pia/UDS ; la même famille de bug casse le Blasters de YW2 (#170) | HLE UDS conçue en traçant Blasters (`uds.cpp:545,709`) : Probable | Patch 0005 du mod YW2 pour le Blasters **de YW2** : à éprouver sur le jeu autonome |
| Récompenses | Données (`yw_a.fa`, `ywb_lg_*.fa`) éditables par Albatross (YWB supporté) | idem (mods RomFS) | idem |
| Sauvegardes | `yw_save --game ywb` / `ywb_getto` (JPN Busters / Getto-gumi = Moon Rabbit) ; EUR **non vérifié** ; `head.yw` requis | Import JKSM/Checkpoint | idem Azahar |

**Les deux éditions** partagent un exécutable chez Clockwork (« versions released together in one region share
one », `games.h:31-35`) : code commun, donc **une seule adaptation de code** est probable, avec des **tables de
données différentes** (Yo-kai exclusifs, boss). **Moon Rabbit Crew** change le code (mise à jour) : les adresses
d'une partie en 1.0 et en 2.0 diffèreront. Il faut **choisir une seule base** (recommandé : 2.0 avec Moon Rabbit
Crew, version que tout joueur à jour possède) et refuser les autres, comme le mod YW2 refuse une ROM mise à jour.

## Ce qu'il faut tester sur votre PC (aucun ne peut l'être ici)

1. YW3 EUR et Blasters EUR (+ mise à jour 2.0) sur Azahar **2124.3** et sur la dernière version : démarrage,
   1re heure, une mission Blasters solo, un boss, sauvegarde/rechargement, langue française.
2. Les mêmes sur Zakuro (dernière release) **et** sur Clockwork nightly.
3. Le Ψ Blasters de YW2 sur Azahar (confirmer #170 en EUR).
Protocole détaillé : NEXT_STEPS.md, phase 1.
