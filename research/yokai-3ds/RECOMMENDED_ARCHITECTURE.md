# RECOMMENDED_ARCHITECTURE — architecture recommandée et justification

## 0. Résumé

La question « Azahar ou Clockwork ? » est mal posée pour un Archipelago : ce qui décide, c'est **où l'on peut
faire tourner un patch de code du jeu et lui parler depuis Python**. Sur ce critère :

- **Azahar** : patchs de code chargés (`code.bps` + `exheader.bin`), RPC mémoire et stub GDB, save states, outils de
  débogage. C'est **la meilleure plateforme de développement** et une plateforme de jeu validée pour YW2.
- **Clockwork** : aujourd'hui **aucune** surface de modding de code (patchs de code refusés, pas de hooks, pas
  d'API), EUR non testée, un mois d'existence. **Non recommandé** pour l'instant.
- **Zakuro** (découvert pendant l'audit, utilisé par le mod YW2) : « code PC » comme Clockwork, **mais** charge les
  mêmes patchs qu'Azahar, offre des overrides de fonctions documentés, retombe sur un interpréteur au lieu de
  planter, et liste YW2 et YW3 EUR comme « Playable ». C'est **la meilleure plateforme de jeu PC** pour YW2/YW3.

Comme Azahar et Zakuro lisent **le même dossier de mods** (`mods/<titleID>/code.bps`, `exheader.bin`, `romfs_ext/`),
un même patch et un même client (transport GDB, plus RPC pour Azahar) servent les deux. On développe sur Azahar,
on joue sur celui qui passe le test de partie complète.

## 1. Choix par jeu

| Jeu | Recommandation | Repli | Justification |
|---|---|---|---|
| **YW2 Spectres Psychiques (EUR)** | **Mod YW2 Archipelago V3 existant**, APWorld FR, sur **Zakuro** fourni par son lanceur | **Azahar 2124.3** (sans l'option `blasters` tant que #170 n'est pas levée en EUR) | Intégration jouable et terminable qui existe (CONFIRMÉ) ; Clockwork BLOQUANT (patch refusé) |
| **YW3 (EUR)** | Développer un patch `code.bps` + client sur **Azahar** (débogage), cible de jeu **Zakuro et Azahar** | celui des deux qui passe la phase 1 | Zakuro le déclare « Playable » ; Azahar non vérifié ; Clockwork n'apporte rien sans fork |
| **Blasters (EUR, 2.0 Moon Rabbit Crew)** | **Décision après la phase 1** : même chaîne qu'YW3 si Azahar ou Zakuro font tourner une mission solo + un boss + sauvegarde | **Clockwork + fork de crochets** seulement si c'est le seul moteur stable | Aucune compatibilité EUR vérifiée nulle part ; c'est le seul cas où Clockwork pourrait se justifier |

Le tableau ne force pas une technologie commune : si Blasters ne tourne bien que sous Clockwork, il aura sa propre
chaîne (prototype B montre la faisabilité du crochet), au prix d'un fork à maintenir.

## 2. Architecture logicielle

```
                         ┌──────────────── Serveur Archipelago (0.6.9+) ────────────────┐
                         │  APWorlds : yokaiwatch2 (existant), yokaiwatch3, yokaiwatchblasters,  │
                         │             mario kart wii, pokémon rouge feu × yo-kai                │
                         └───────────────┬──────────────────────────────────────────────┘
                                         │ websocket
        ┌────────────────────────────────┴───────────────────────────────┐
        │ ykap-core (Python, MUTUALISÉ)                                  │
        │  • client AP (Connect, LocationChecks, ReceivedItems, Sync,    │
        │    StatusUpdate, DeathLink, reconnexion)          ← ykap/ap_client.py
        │  • protocole de boîte générique (liaison, compteur,
        │    dons, journal, bits persistants)               ← ykap/mailbox.py
        │  • transports : RPC Azahar (UDP) | GDB (Azahar, Zakuro)
        │    | socket Clockwork (si un jour)                ← ykap/azahar_rpc.py + gdb.py du mod YW2
        │  • outils ROM : rom3ds, level5 (ARC0), bps, t2b   ← installation/* du mod YW2 (MIT)
        │  • installeur mods/<titleID>/ avec retour arrière ← installer.py du mod YW2
        └──────┬───────────────────────┬────────────────────────┬────────┘
               │ profil YW2            │ profil YW3             │ profil Blasters
        (client du mod YW2,     table d'adresses EUR,     table d'adresses EUR 2.0,
         inchangé)              ids locations/items        ids missions/items
               │                       │                        │
        patch YW2 (existant)    patch YW3 (À ÉCRIRE)      patch Blasters (À ÉCRIRE)
        boîte 0x0091C000        boîte YKAP v1             boîte YKAP v1
```

### Ce qui est mutualisé
1. Client réseau Archipelago et boucle de synchronisation (indépendants du jeu).
2. Protocole de boîte **YKAP v1** (`mailbox.py`) : même disposition pour YW3 et Blasters ; seule l'adresse de base
   et la signification des codes changent. YW2 garde son protocole v10 (on ne le réécrit pas).
3. Transports mémoire (RPC + GDB).
4. Outils de lecture ROM et formats Level-5 (mêmes archives ARC0 et `.cfg.bin` sur les trois jeux ; Albatross les
   couvre tous).
5. Installation et désinstallation propres dans `mods/<titleID>/`.
6. Méthode de rétro-ingénierie (scripts Ghidra, sonde RPC, diff mémoire).

### Ce qui ne l'est pas (ne jamais supposer)
Adresses, structures de sauvegarde, systèmes de quêtes/missions, fonctions internes, tables de flags : **propres à
chaque jeu, chaque région et chaque version** (`clockwork:games.h:30-35`).

## 3. Ordre de développement (justifié)

1. **Phase 0 — tests sur votre PC (1-2 semaines)** : compatibilité réelle des trois jeux EUR sur Azahar 2124.3,
   Azahar récent, Zakuro, Clockwork ; vérifier RPC. *Tout le reste en dépend, surtout Blasters.*
2. **Phase 1 — YW2 dans le multiworld** : installer le mod existant, faire une partie de test avec un autre jeu.
   *Valeur immédiate, risque minimal, valide le serveur et l'organisation des joueurs.*
3. **Phase 2 — ykap-core** : extraire les prototypes en bibliothèque, ajouter le transport GDB (réutiliser
   `gdb.py`), tests automatiques (`run_poc.py` en CI).
4. **Phase 3 — YW3 « MVP »** : 20-30 locations (chapitres + boss d'histoire), victoire = fin de l'histoire, objets
   = consommables + quelques clés ; puis élargir. *Zakuro Playable : meilleure chance de résultat terminable.*
5. **Phase 4 — Blasters** : selon la phase 0 ; boucle mission → location très adaptée à AP.
6. En parallèle, indépendants : Pokémon Rouge Feu × Yo-kai (décompilation : le plus simple techniquement),
   Mario Kart Wii (rechercher un monde communautaire existant d'abord).

## 4. Risques susceptibles de rendre le projet irréalisable

| Risque | Probabilité | Impact | Parade |
|---|---|---|---|
| Blasters EUR ne tourne correctement sur **aucun** moteur | Moyenne | Jeu retiré du multiworld | Phase 0 d'abord ; tester aussi la version USA comme indicateur ; plan B Clockwork |
| Rétro-ingénierie ARM de YW3/Blasters trop lourde (fonctions donner/finir introuvables) | Moyenne | Mois de retard | Commencer par des locations lues en **flags** (sans patch) et des objets simples ; contacter l'auteur du mod YW2 et la communauté Albatross/Tinifan |
| Dépendance à des projets d'un seul mainteneur (Zakuro, mod YW2) | Moyenne | Plus de correctifs | Tout garder compatible Azahar (même patch) ; MIT : fork possible |
| Version Azahar : 2124.3 seule validée, RPC peut-être absent | Faible-moyenne | Transport | GDB en repli (déjà éprouvé) |
| Désynchronisation sauvegarde / objets (doublons, pertes) | Faible si compteur dans la sauvegarde | Partie gâchée | Règle « index == compteur », écrite avec l'objet ; tests C4-C8 |
| Juridique | — | — | Jamais de ROM, de code.bin ni de code recompilé distribués ; patchs BPS appliqués chez le joueur, vérifiés sans octet du jeu (pratique du mod YW2) |
