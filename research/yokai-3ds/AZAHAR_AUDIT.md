# AZAHAR_AUDIT — l'émulateur et ses moyens de communication

Audit du 2026-11-14 sur `azahar-emu/azahar@11eceda` (2026-11-12, dernier tag `2127.0-rc3`).
Notation des références : `azahar:<chemin>:<ligne>`. Sauf mention « test », tout ce qui suit vient de la
lecture du code, pas d'une exécution d'Azahar (aucun jeu ni binaire Azahar n'a été lancé ici).

## 1. Identité du projet

| Point | Constat | Preuve |
|---|---|---|
| Existence, activité | Actif : dernier commit le 2026-11-12 ; 1 595 issues et 1 009 PR au total | `git log`, recherche GitHub |
| Licence | **GPLv3** (en-têtes « GPLv3 or any later version ») | `azahar:LICENSE.txt`, `azahar:src/core/rpc/packet.h:2` |
| Nature | Émulateur HLE 3DS, successeur de Citra ; JIT ARM (dynarmic) | `azahar:README.md` |
| Plateformes | Windows (MSVC/MXE), macOS, Linux, Android | `azahar:README.md` |

Conséquence de la GPL : modifier Azahar et distribuer le binaire oblige à publier ces modifications sous GPL. Un
client **externe** qui parle à Azahar par réseau n'est pas concerné. `dist/scripting/AzaharRPC.py` est lui-même
GPL : le prototype n'en copie rien et réimplémente le protocole à partir de `packet.h`.

## 2. Interfaces permettant de communiquer avec un programme externe

### 2.1 Serveur RPC (UDP 45987) — la meilleure voie, **existe réellement**

| Élément | Constat | Preuve |
|---|---|---|
| Requêtes | `ReadMemory`, `WriteMemory`, `ProcessList`, `SetGetProcess`, `TakeScreenshot`, `ReadScreenshot`, `GetPerfStats`, `SetFreeCam`, `SaveState`, `LoadState`, `SetInput` | `azahar:src/core/rpc/packet.h:15-28` |
| Taille | 32 Kio par requête | `packet.h:126-128` |
| Port | 45987, fixe (« TODO: Make configurable ») | `azahar:src/core/rpc/udp_server.cpp:17-19` |
| Activation | Réglage **désactivé par défaut** : Émulation > Configurer > Débogage > « Enable RPC server » | `azahar:src/common/settings.h:699`, `src/citra_qt/configuration/configure_debug.cpp:136` |
| Compilation | `ENABLE_SCRIPTING` **ON** par défaut, `ENABLE_SCRIPTING_SYNC` ON | `azahar:CMakeLists.txt:137-138` |
| Cohérence | Les requêtes qui touchent l'état émulé sont exécutées **sur le thread d'émulation**, entre deux tranches (`ProcessPendingWork`) : pas d'arrêt du jeu nécessaire, pas d'écriture coupée en deux | `azahar:src/core/core.cpp:318-334` |
| Récence | `SaveState`/`LoadState` ajoutés le 2026-10-28, `SetInput` le 2026-10-29 | `git log -- src/core/rpc` |
| Processus | Lit/écrit dans le processus courant, ou celui choisi par `SetGetProcess` | `rpc_server.cpp:54-105` |

**Non vérifié** : la présence du serveur RPC et de la case dans les binaires officiels de **2124.3** (version que
le mod YW2 valide). Le code est hérité de Citra, mais la synchronisation sur le thread d'émulation et plusieurs
requêtes sont récentes. Test à faire sur le PC (voir NEXT_STEPS.md, étape 1).

### 2.2 Stub GDB (TCP 24689) — **existe et est utilisé en production par le mod YW2**

| Élément | Constat | Preuve |
|---|---|---|
| Compilation | `ENABLE_GDBSTUB` ON par défaut | `azahar:CMakeLists.txt:140` |
| Traitement | Paquets traités dans la même boucle `ProcessPendingWork` | `core.cpp:324-328` |
| Usage réel | Le client YW2 Archipelago lit et écrit la mémoire par ce stub ; il a documenté ses pièges : le stub **se ferme quand le client se déconnecte** (il faut relancer Azahar), les écritures `M` ne sont acceptées **que jeu interrompu**, chaque paquet fige brièvement le jeu | `Yo-kai-Watch-2-Archipelago:source/archipelago/client/gdb.py:1-40` |
| Version validée par le mod | **2124.3 seulement** | `…/installation/azahar.py:30` |
| Bug connu | Plantage d'Azahar 2126.1.2 en connectant Ghidra avec « Pause next non-sysmodule process at start » (sur Yo-kai Watch 1 EUR) | issue azahar #2586 (fermée) |

Le RPC (2.1) évite les trois défauts du stub (pas d'arrêt requis pour écrire, pas de fermeture à la déconnexion,
lectures groupées de 32 Kio). Recommandation : **RPC en priorité, GDB en repli** pour les builds où le RPC
n'existerait pas.

### 2.3 Cheats (format Gateway)

`azahar:src/core/cheats/gateway_cheat.cpp` : écritures/conditions périodiques. Utile pour l'exploration
(ex. 60 FPS, déblocages), **inadapté** à un échange bidirectionnel avec Archipelago (pas de canal de sortie).

### 2.4 Pas d'API de script interne

Aucun Lua / plugin chargé dans le processus : toute logique « dans le jeu » doit être un **patch du code du jeu**
(2.5) ; toute logique « hors du jeu » passe par RPC/GDB.

## 3. Modification du jeu sans toucher à la cartouche

| Mécanisme | Constat | Preuve |
|---|---|---|
| Patch de code | `load/mods/<titleID>/` : `code.bin`, `code.ips`, `code.bps`, aussi dans `exefs/`, et chemins Luma | `azahar:src/core/file_sys/ncch_container.cpp:549-559` |
| Exheader | `exheader.bin` remplaçable (code agrandi) — utilisé par le mod YW2 | `…/installation/installer.py:1-30` |
| LayeredFS | `romfs/` (fichiers entiers) et `romfs_ext/` (patchs .ips/.bps) | `ncch_container.cpp:668` ; usage par le mod YW2 |
| Mises à jour / DLC | installées comme sur console (Moon Rabbit Crew = mise à jour de Blasters) | comportement standard d'Azahar, non testé ici |

C'est exactement la chaîne qu'utilise le mod YW2 : patch BPS appliqué **chez le joueur** à sa propre ROM, déposé dans
`load/mods/00040000001B2900/` (`installer.py:10`). Rien de la ROM n'est distribué.

## 4. Débogage et diagnostic

- Stub GDB (Ghidra / gdb-multiarch) pour points d'arrêt et pas-à-pas : indispensable pour trouver les fonctions
  « donner objet », « fin de quête » de YW3 et Blasters.
- Journal `log/azahar_log.txt` ; le mod YW2 y lit la version (`azahar.py:7-10`).
- Save states (aussi par RPC) : reproductibilité des tests (revenir juste avant une fin de quête).
  Attention : le mod YW2 déconseille les save states en partie réelle (liés à la version exacte du patch).

## 5. Problèmes connus pertinents pour nos jeux

| Issue | Jeu | Effet | État |
|---|---|---|---|
| #170 | YW2 | **Mode Ψ Blasters de YW2 cassé** : le jeu ouvre une connexion locale même en solo | ouverte |
| #1636 | YW2 Shin'uchi (JPN) | écran brun + blocage contre Dame Dredful et McKraken (2e forme), 2124+ | fermée (correctif non vérifié) |
| #2172 | YW1 et autres | plantages aléatoires après cinématiques sous **Vulkan** ; OpenGL les évite | ouverte |
| #1107/#1108 | YW2 | caméra saccadée | fermées |

Aucune issue spécifique à **Yo-kai Watch 3** ni à **Yo-kai Watch Blasters** (jeu autonome) n'a été trouvée
(recherches « yo-kai », « yokai », « blasters »). C'est un indice faible de bonne compatibilité, **pas une preuve**.

## 6. Bilan pour Archipelago

| Besoin | Possible avec Azahar ? | Statut |
|---|---|---|
| Lire la progression | RPC `ReadMemory` / GDB `m` | Confirmé (code) ; RPC testé contre un faux serveur, GDB utilisé en prod par YW2 |
| Écrire (dons) | RPC `WriteMemory` sans arrêt / GDB avec arrêt | Confirmé (code) |
| Appeler des fonctions internes du jeu | **Non** depuis l'extérieur ; oui via un patch de code (code.bps) qui les appelle | Confirmé (architecture YW2) |
| Hooks d'évènements | Pas d'API ; patch de code + boîte aux lettres en mémoire | Confirmé (YW2) |
| Pont Python | Oui, bibliothèque standard seule (UDP ou TCP) | Prototype A |
