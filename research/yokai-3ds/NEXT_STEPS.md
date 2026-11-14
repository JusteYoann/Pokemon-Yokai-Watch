# NEXT_STEPS — plan concret pour démarrer l'intégration

Légende : 🖥 = manipulation **sur votre PC** (impossible depuis ce conteneur : pas de jeu, pas de Windows, pas de GPU).

## Phase 0 — Préparer (🖥, une soirée)

1. Dumper **vos** cartouches avec GodMode9 (`[C:] GAMECART` → *Dump cart (trimmed)*, puis *Decrypt file*) :
   YW2 Spectres Psychiques, YW3, Blasters Chat Rouge **et/ou** Chien Blanc. Dumper la **mise à jour 2.0 de Blasters**
   (Moon Rabbit Crew) : *Title manager* → `0004000E…` → *Build CIA (decrypted)*.
2. Noter le SHA-1 de chaque dump (`certutil -hashfile fichier.3ds SHA1`) dans un fichier `dumps.txt` **local**
   (jamais commité).
3. **Copier les sauvegardes** existantes avant tout test (dossier `sdmc`/`nand` d'Azahar, `%APPDATA%\zakuro`,
   `%APPDATA%\yw2-recomp`). Ne jamais tester sur une sauvegarde unique.
4. Installer : Azahar **2124.3** (version validée par le mod YW2) et la **dernière** Azahar en version portable dans
   deux dossiers séparés ; Zakuro (dernière release) ; Clockwork (nightly) + Build Tools de Visual Studio ;
   Python 3.11+ ; Archipelago 0.6.9.

## Phase 1 — Mesurer la compatibilité (🖥, 1-2 semaines)

Pour chaque couple jeu × moteur (YW3 et Blasters × Azahar 2124.3, Azahar récente, Zakuro, Clockwork ; YW2 × Azahar
pour #170), remplir une ligne de `research/yokai-3ds/resultats_phase1.csv` :

| Test | Critère « OK » |
|---|---|
| 1.1 Démarrage, écran titre, langue française | textes FR |
| 1.2 Nouvelle partie, 1 h de jeu | aucun plantage ; noter FPS (Azahar : RPC `GetPerfStats`) |
| 1.3 **Sonde** (Azahar, RPC coché) : `python poc/probe_azahar.py info` puis `snap`/`diff` avant/après une quête | le titre est reconnu ; au moins une adresse change de façon reproductible (indicateur de progression lu **sans écrire**) |
| 1.4 Un boss | victoire sans écran figé (cf. #1636) |
| 1.5 Blasters : une mission **solo** + Moon Rabbit Crew | pas d'erreur de connexion |
| 1.6 Sauvegarder, quitter, recharger | progression conservée |
| 1.7 Vulkan puis OpenGL (Azahar) | noter les différences (#2172) |

Livrable : le CSV. **Décision Blasters** à la fin de cette phase (RECOMMENDED_ARCHITECTURE.md §1).

## Phase 2 — YW2 dans le multiworld (🖥, quelques jours)

1. Installer le mod YW2 AP **V3.0.0** (lanceur exe, Zakuro inclus) en suivant `docs/INSTALLATION_FR.md` du mod.
2. Générer une partie test : YW2 (YAML FR) + un monde simple (APQuest) ; jouer jusqu'à 10 checks, couper le réseau,
   relancer le jeu, vérifier : pas de doublon, pas de perte.
3. Décider si l'option `blasters` (Ψ Blasters de YW2) est active : **seulement sur Zakuro**.
4. Prendre contact avec l'auteur du mod (issues du dépôt) : notes de rétro-ingénierie, conventions de boîte,
   coordination si nous réutilisons son code (MIT : garder la mention de copyright).

## Phase 3 — Socle commun `ykap-core` (dans ce dépôt, 1-2 semaines)

1. Déplacer `research/yokai-3ds/poc/ykap` vers un paquet `ykap/` ; ajouter le transport **GDB** (adapter
   `gdb.py` du mod YW2, MIT) à côté du RPC ; interface `Memory` commune.
2. Brancher le client sur `CommonClient` d'Archipelago (interface `/connect`, journal, intégration Launcher) ou garder
   le client autonome pour le lanceur — choisir après la phase 2.
3. CI : `run_poc.py` sur chaque push (serveur AP réel + jeu simulé).
4. Réutiliser `rom3ds.py`, `level5.py`, `bps.py` du mod YW2 pour lire les ROM du joueur.

## Phase 4 — Yo-kai Watch 3 « MVP » (le gros morceau)

1. 🖥 Ghidra + stub GDB d'Azahar : charger le `code.bin` **de votre dump** (jamais commité). Trouver, avec la sonde
   et des points d'arrêt sur écriture : (a) le tableau de flags de progression, (b) la fonction « ajouter objet »,
   (c) le moment où un chapitre/une quête se termine. Consigner les adresses dans un fichier de profil **sans octet du
   jeu** (adresses et tailles seulement).
2. APWorld `yokaiwatch3` minimal : ~20-30 locations (fins de chapitre, boss d'histoire), objets = consommables +
   argent, victoire = fin de l'histoire. Logique : linéaire au départ (pas de verrou) — **jouable avant d'être riche**.
3. Client : profil YW3 = lecture des flags (sans patch) pour les locations ; pour les objets, un premier patch
   `code.bps` minimal qui implémente la boîte YKAP v1 et appelle « ajouter objet ».
4. Tester sur Azahar **et** Zakuro (même `mods/00040000001D6800/`).
5. Ensuite seulement : verrous (zones, Yo-kai, fonctions), quêtes secondaires, Busters T.

## Phase 5 — Blasters (si la phase 1 l'autorise)

Même méthode ; locations = missions et boss ; objets = Yo-kai jouables, objets de butin, déblocages de missions.
Base unique : version **2.0** (Moon Rabbit Crew). Une seule adaptation de code pour les deux éditions, tables
séparées par édition. Si seul Clockwork fait tourner Blasters : forker son recompilateur avec une option de crochets
(généraliser `poc/clockwork_hook/inject_hooks.py`) et un serveur socket dans le runtime.

## À ne pas faire

- Ne pas recréer le mod YW2.
- Ne pas viser Clockwork pour YW2/YW3 tant qu'il refuse les patchs de code et qu'il n'a pas de hooks.
- Ne jamais commiter de ROM, `code.bin`, exheader, RomFS, code recompilé ni sauvegarde.
- Ne pas écrire en mémoire du jeu sur une vraie partie sans copie de la sauvegarde.
