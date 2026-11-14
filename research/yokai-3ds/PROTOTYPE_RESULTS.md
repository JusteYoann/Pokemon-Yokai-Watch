# PROTOTYPE_RESULTS — ce qui a été réellement exécuté

Environnement : conteneur Linux, Python 3.13, Archipelago 0.6.9 (`f5b97c5`) lancé depuis les sources, Rust 1.97,
clang/llvm. **Aucun jeu Yo-kai Watch, aucun Azahar, aucun Zakuro et aucun binaire Clockwork n'ont été exécutés** :
pas de dump disponible (et aucun téléchargé). Chaque ligne indique la nature du test.

| Légende | Signification |
|---|---|
| **RÉEL** | composant réel exécuté (vrai serveur Archipelago, vrai recompilateur Clockwork) |
| **SIMULÉ** | remplacé par un double (faux Azahar, jeu simulé, programme ARM synthétique) |

## Prototype C — client Archipelago (RÉEL côté serveur, SIMULÉ côté jeu)

Reproduire : générer une partie à 2 joueurs APQuest (`Generate.py`), puis
`python research/yokai-3ds/poc/run_poc.py --archipelago <Archipelago> --multidata <AP_xxx.zip>`.

| Étape | Résultat | Nature |
|---|---|---|
| C1 connexion + liaison d'une sauvegarde neuve | OK | serveur RÉEL, jeu SIMULÉ |
| C2 3 missions finies → `LocationChecks` | OK (3/6) | idem |
| C3 objets d'un autre joueur reçus et appliqués dans l'ordre | OK (4 reçus, 4 appliqués) | idem |
| C4 coupure websocket → reconnexion auto sans doublon | OK (2 connexions, inventaire 4 → 4) | idem |
| C5 redémarrage du jeu → rien de réappliqué, checks conservés | OK | idem |
| C6 inventaire = exactement la liste du serveur | OK | idem |
| C7 toutes les locations + victoire | OK (6/6) | idem |
| C8 sauvegarde d'une autre graine → aucun objet donné | OK | idem |
| C9 victoire enregistrée par le serveur (« YokaiPoC (Team #1) has completed their goal ») | OK | journal du serveur RÉEL |

Extrait du journal serveur : `Partner sent Sword to YokaiPoC (Top Middle Chest)` … `YokaiPoC sent Sword to
Partner (Bottom Right Room Left Chest)` … `YokaiPoC (Team #1) has completed their goal.`

**Ce que cela prouve** : le client, le protocole de boîte (liaison, compteur dans la sauvegarde, file de dons
idempotente, bits persistants) et la reprise après coupure fonctionnent contre un **vrai** serveur Archipelago.
**Ce que cela ne prouve pas** : qu'un jeu Yo-kai Watch exécute la partie « jeu » ; elle reste à écrire en patch ARM.
Le jeu utilisé côté serveur est APQuest (monde de démonstration officiel), pas un APWorld Yo-kai.

## Prototype A — pont vers Azahar (SIMULÉ)

`ykap/azahar_rpc.py` implémente le protocole RPC d'Azahar (version 2) à partir de `packet.h`/`rpc_server.cpp`.
Testé contre `ykap/fake_azahar.py`, un faux serveur qui suit le même format :

| Étape | Résultat | Nature |
|---|---|---|
| A1 liste des processus, titre `00040000001B2900` reconnu | OK | SIMULÉ |
| A2 lecture d'un u32 sans aucune écriture | OK | SIMULÉ |
| A3 lecture/écriture de 51 200 octets (découpage > 32 Kio) | OK | SIMULÉ |
| Sonde `probe_azahar.py info/read` contre le faux serveur ; message clair si le serveur ne répond pas | OK | SIMULÉ |

**Objectif minimal de la mission (« lire un indicateur de progression de manière fiable, sans modifier la
sauvegarde ») : NON atteint ici**, faute de jeu et d'émulateur. L'outil `probe_azahar.py` (lecture seule, aucune
commande d'écriture) est prêt pour le faire sur votre PC : NEXT_STEPS.md, étape 1.3. Une source indépendante
confirme que la lecture mémoire d'Azahar fonctionne sur YW2 EUR : le client YW2 lit sa boîte en `0x0091C000` par
GDB en production (`gdb.py`).

## Prototype B — interception d'évènement avec Clockwork (RÉEL pour l'outil, SIMULÉ pour le jeu)

Reproduire : `research/yokai-3ds/poc/clockwork_hook/run.sh <dépôt clockwork>`.

1. Compilation du vrai recompilateur `tools/recomp` de Clockwork (`3047d9e`) : OK (RÉEL).
2. Programme ARM **synthétique** (`synthetic.s` : `complete_mission(7)`, `give_item(42)`, `give_item(43)`),
   lié à `0x100000`, présenté à `recomp` avec un `code.bin`/`exheader.bin` fabriqués : `recomp emit` → 3 fonctions
   C (`f_00100000`, `f_00100020`, `f_00100038`) : OK (RÉEL). On y voit les appels directs `f_00100038(ctx);`.
3. `inject_hooks.py` renomme les fonctions ciblées en `_orig` et insère un crochet ; compilation avec
   `runtime/include/recomp.h` et `runtime/src/arm_ops.c` de Clockwork : OK.
4. Exécution :
   ```
   {"event":"location_done","mission":7,"flags":"0x00000080"}
   {"event":"item_given","item":42}
   {"event":"item_given","item":43}
   {"event":"item_given","item":99}      ← objet « reçu d'Archipelago » donné en appelant la fonction interne
   {"state":{"flags":"0x00000080","inventory_count":3,"last_item":99}}
   ```

**Ce que cela prouve** : avec le code émis par Clockwork, on peut intercepter n'importe quelle fonction et appeler
les fonctions internes du jeu, **à condition de réécrire le C généré avant compilation** (aucun mécanisme natif).
**Ce que cela ne prouve pas** : que les fonctions équivalentes existent et sont identifiables dans YW2/YW3/Blasters,
ni que le runtime Clockwork (non compilé ici : SDL3, etc.) se comporte bien avec ces crochets. Limite observée :
un crochet « après » voit les registres modifiés par la fonction ; il faut relever les arguments dans la phase « avant ».

## Fichiers

| Fichier | Rôle |
|---|---|
| `poc/ykap/ap_client.py` | client AP minimal (websockets) branché sur une boîte |
| `poc/ykap/mailbox.py` | protocole YKAP v1 (proposition) + côté jeu SIMULÉ |
| `poc/ykap/azahar_rpc.py` | client RPC Azahar (réimplémentation, MIT) |
| `poc/ykap/fake_azahar.py` | faux Azahar (tests seulement) |
| `poc/ykap/games.py` | title IDs EUR/USA |
| `poc/run_poc.py` | banc d'essai A + C |
| `poc/probe_azahar.py` | **sonde lecture seule pour votre PC** |
| `poc/clockwork_hook/` | prototype B (`run.sh`, `synthetic.s`, `inject_hooks.py`, `harness.c`) |
