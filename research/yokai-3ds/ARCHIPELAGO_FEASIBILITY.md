# ARCHIPELAGO_FEASIBILITY — faisabilité des intégrations

Références : `ArchipelagoMW/Archipelago@f5b97c5` (version **0.6.9**, `Utils.py:58`),
`doryan-meunier/Yo-kai-Watch-2-Archipelago@6d12594` (V3.0.0, MIT).

## 1. Ce qu'Archipelago exige d'un jeu

| Notion | Rôle | Où ça vit |
|---|---|---|
| **APWorld** | paquet Python : items, locations, régions, règles, options, victoire, `slot_data` | `worlds/<jeu>/` ou `.apworld` dans `custom_worlds` |
| **Location** | un endroit qui « donne » quelque chose (coffre, quête, mission, boss) ; id numérique stable | APWorld |
| **Item** | ce qui est donné ; *progression*, *useful*, *filler*, *trap* | APWorld |
| **Règles** | ce qu'il faut posséder pour atteindre une location ; doivent refléter de **vrais verrous du jeu** | APWorld (`rules`) |
| **Victoire** | condition envoyée par `StatusUpdate` (CLIENT_GOAL = 30) | client |
| **Client** | lit le jeu, envoie `LocationChecks`, reçoit `ReceivedItems`, applique | programme à côté du jeu |
| **Synchro** | `ReceivedItems` porte un **index** ; trou → `Sync` ; le serveur renvoie tout à la connexion | `CommonClient.py:1084-1098` |
| **Reconnexion** | `Connected` donne `checked_locations` / `missing_locations` ; les checks locaux non confirmés sont renvoyés | `CommonClient.py:1050-1080` |
| **Persistance** | côté serveur : checks et objets envoyés ; côté jeu : **c'est au client/jeu** de savoir quels objets sont déjà appliqués | — |

Il n'existe **aucun** jeu 3DS ni client Citra/Azahar dans le dépôt officiel (recherche « citra|azahar|3ds » dans
`worlds/` : rien). Précédents utiles : clients **BizHawk** (`worlds/_bizhawk`, GBA — pertinent pour le hack Rouge
Feu) et **Dolphin** via `dolphin_memory_engine` (`worlds/tww/TWWClient.py` — pertinent pour Mario Kart Wii).

## 2. Le schéma qui marche (prouvé par YW2, reproduit par le prototype C)

```
 Serveur AP ──websocket── Client Python ──RPC/GDB (mémoire)── [boîte aux lettres en RAM du jeu]
                                                                    │
                                              patch de code du jeu (code.bps) : lit la boîte,
                                              appelle les fonctions INTERNES (donner objet, poser flag),
                                              écrit le journal des checks, garde le compteur dans la SAUVEGARDE
```

Les huit besoins de la mission, et la réponse de ce schéma :

| # | Besoin | Mécanisme | Statut |
|---|---|---|---|
| 1 | Détecter une mission/quête finie | flags persistants du jeu (relus) + journal écrit par le patch | Confirmé (YW2 : `synchro.py` point 4) |
| 2 | Identifier l'évènement | id de flag / de quête → id de location dans l'APWorld | Confirmé (YW2) |
| 3 | Envoyer au client AP | `LocationChecks` | Confirmé (prototype C, serveur réel) |
| 4 | Recevoir un objet | `ReceivedItems` (index) | Confirmé (prototype C) |
| 5 | Appliquer dans le jeu | file de dons lue par le patch, qui appelle la fonction interne « donner » | Confirmé (YW2) ; simulé (prototype C) |
| 6 | Enregistrer définitivement | compteur « déjà livré » **dans la sauvegarde**, écrit avec l'objet | Confirmé (YW2 : `synchro.py` point 3) |
| 7 | Éviter les doublons | n'appliquer que l'index == compteur | Confirmé (YW2) ; testé (prototype C : C4, C5, C6) |
| 8 | Reprendre après déconnexion | tout se reconstruit depuis la sauvegarde + `Connected` | Testé (prototype C : C4, C5) |

Plus une règle de sûreté apprise du mod YW2 : **lier la sauvegarde à la graine** (identifiant écrit dans la
sauvegarde ; une autre partie ne reçoit rien) — testé (prototype C : C8).

## 3. L'intégration Yo-kai Watch 2 : ce qui est réutilisable

Inventaire de `source/` (31 820 lignes Python publiées) :

| Composant | Fichiers | Spécifique à YW2 ? | Réutilisable pour YW3 / Blasters |
|---|---|---|---|
| Pont GDB robuste (une connexion, resynchronisation, transactions) | `client/gdb.py` (514 l.) | Non (Azahar/Zakuro) | **Oui, tel quel** |
| Client réseau AP | `client/ap_reseau.py` (999 l.) | Peu | **Oui** |
| Protocole de boîte | `client/boite_protocole.py` (5 119 l.) | **Oui** (v10, adresses, verrous YW2) | Le **principe** ; pas la disposition |
| Synchronisation | `client/synchro.py` (4 603 l.) | Mélangé | Les règles (liaison, compteur, resynchro) ; à réécrire par jeu |
| Lecture ROM / Level-5 / BPS / T2B | `installation/rom3ds.py`, `level5.py`, `bps.py`, `t2b.py` | Non (formats Level-5 communs) | **Oui** |
| Installation dans `load/mods` avec retour arrière | `installation/installer.py`, `azahar.py`, `zakuro.py` | Title ID en dur | **Oui** avec paramètre |
| Lanceur Tk, tracker, onglets | `lanceur/*` | Interface YW2 | Partiellement |
| APWorld (régions, coffres, logique) | `apworld/yokaiwatch2/*` | **Oui** | Structure seulement |
| **Patch de code du jeu** (`src/archipelago/*.h`, `boite.h`) | **non publié** (« tiré du code du jeu ») | **Oui** | **Non** : à écrire de zéro pour YW3 et Blasters |
| Zakuro adapté | `zakuro/patches/0001..0005` | GDB générique ; UDS solo | **Oui** |

Points d'attention :
- Le cœur de valeur (le patch du jeu) **n'est pas disponible** en source. Pour YW3 et Blasters, il faut refaire
  l'ingénierie inverse : trouver les fonctions « donner objet », « finir quête », les tables de flags, puis écrire
  un patch ARM. C'est le poste de travail principal du projet.
- Le mod a deux APWorlds : jeu « Yo-kai Watch 2 » (FR) et « Yo-kai Watch 2 (English) ». Pour notre multiworld,
  prendre **le monde français** avec la ROM EUR (le mod exige une ROM EUR d'origine, sans mise à jour).
- Licence MIT : réutilisation autorisée avec mention ; prendre contact avec l'auteur (Doteos) évite un fork
  divergent et donnerait peut-être accès aux notes de rétro-ingénierie (`docs/systemes/*.md` cités mais absents du dépôt).
- Le mod indique avoir été écrit presque entièrement avec une IA, testé par une bêta : 3 issues, dont deux sur la
  version anglaise fermées. Fiabilité du monde FR : bonne d'après l'historique (31 bêtas), non vérifiée ici.

## 4. Réception des objets : méthodes par type, par jeu

Règle générale : **appeler la fonction du jeu** (via le patch de code) plutôt qu'écrire des octets dans
l'inventaire : la fonction met à jour les compteurs annexes, les drapeaux « vu », l'affichage, la sauvegarde.

| Type d'objet | Méthode recommandée | Contrainte YW2 (connue) | YW3 | Blasters |
|---|---|---|---|---|
| Objet d'inventaire | fonction interne « ajouter objet » appelée par le patch | faite (dons) | à trouver | à trouver (inventaire de butin par mission) |
| Zone | **verrou** dans le patch (le jeu refuse l'accès tant que le flag AP n'est pas reçu) | faite (train, miroirs, voyage dans le temps) | à concevoir | zones = missions/cartes débloquées |
| Mission / quête | verrou sur le déclencheur de la quête | faite (requêtes) | à concevoir | menu des missions : flag de déblocage |
| Yo-kai | fonction « ajouter ami » (Médaillium + équipe/boîte) | partiellement (mélange de Yo-kai) | à trouver | équipe de Blasters : liste des Yo-kai jouables |
| Capacité / fonction | verrou d'une commande (vélo, canne à pêche, rangs de montre) | faite (verrous J4) | à concevoir | à concevoir |
| Indicateur de progression | flag via la fonction « poser flag » du script du jeu | fait | à trouver | à trouver |
| Cohérence de sauvegarde | tout changement passe par les fonctions du jeu ; compteur AP écrit **avec** l'objet | fait | idem | idem ; deux éditions + mise à jour = variantes de sauvegarde |

Écrire directement en mémoire (sans patch) reste possible pour un **prototype** (flags simples, argent), mais
c'est fragile : pas d'atomicité avec la sauvegarde, structures différentes par région/version.

## 5. Faisabilité par jeu

| Jeu | Faisabilité | Pourquoi |
|---|---|---|
| YW2 | **Élevée** (existant) | intégration jouable et terminable ; à intégrer au multiworld, pas à recréer |
| YW3 | **Moyenne** | émulation EUR crédible (Zakuro « Playable ») ; tout le patch à écrire ; grand jeu = beaucoup de locations à cartographier |
| Blasters | **Moyenne à faible** | compatibilité EUR inconnue partout ; sans fil local/Pia risqué ; boucle de jeu par missions (bien adaptée à AP : 1 mission = 1 location) |

## 6. Les deux autres jeux du multiworld (hors périmètre, impact sur le calendrier)

- **Mario Kart Wii** : pas de monde officiel ; client à base de Dolphin (précédent TWW). À rechercher dans la
  communauté avant tout développement.
- **Pokémon Rouge Feu × Yo-kai Watch** : le dépôt actuel est un fork de `pret/pokefirered` (décompilation), sans
  contenu Yo-kai encore. Pas de monde FRLG dans Archipelago 0.6.9 officiel ; le monde `pokemon_emerald` (BizHawk)
  est le modèle. Une **décompilation** permet d'insérer la boîte aux lettres directement dans le C du jeu : c'est le
  jeu le plus simple techniquement des cinq, mais le hack doit rester compatible avec un monde existant ou en avoir un.
