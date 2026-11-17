> **17 novembre — seed à quatre testée :**1711202601,1629 checks. Package Emerald français0.2.1 reçu ; blocage levé. Génération résoluble,36 contrôles serveur à quatre slots avec checks simulés,44 contrôles natifs mGBA Rouge Feu sur cette seed. Les quatre émulateurs simultanés restent non testés. Les anciennes mentions de package absent ci-dessous sont historiques. Voir [rapport](YOKAI_ARCHIPELAGO/DOCUMENTATION/SEED_QUATRE_JEUX_20261117.md).

> **Version de test FR0.5.0 — 16 novembre :**628 checks ; Coupe/Surf/Force/Flash randomisés, Vol utile.620 détecteurs avec redémarrage,44 contrôles réseau,37 protections et finale native testés. Configuration quatre jeux préparée ; génération à quatre bloquée ici par le package Emerald français0.2.1 absent du système de fichiers. Voir [version de test et procédure quatre jeux](YOKAI_ARCHIPELAGO/DOCUMENTATION/FIRERED_VERSION_TEST_4_JEUX.md). Les résultats précédents restent historiques.

## Situation corrigée — retour utilisateur du 16 novembre 2026

Cette mise à jour prévaut sur les anciens états « Emerald en attente » ou « YW2/MKW seulement générés » ci-dessous. Elle rapporte le fonctionnement indiqué par l’utilisateur ; elle n’ajoute pas de tests effectués sur ce poste.

| Jeu | État actuel | Suite |
|---|---|---|
| Pokémon Yo-kai Emerald | Fonctionnel selon le retour utilisateur | Conserver l’intégration existante |
| Yo-kai Watch 2 : Spectres Psychiques EUR | Fonctionnel selon le retour utilisateur | Conserver l’intégration existante |
| Mario Kart Wii | Archipelago fonctionnel selon le retour utilisateur | Ajouter le mod visuel Yo-kai dans la même installation |
| Pokémon Rouge Feu × Yo-kai Watch | Intégration en développement,625 checks actifs et tests natifs/réseau documentés | Poursuivre la couverture et les essais de progression |
| Yo-kai Watch 1 EUR | Seule intégration de jeu encore absente ; prototype technique présent | Développer l’intégration jouable |

Le test collectif final avec les cinq jeux reste à réaliser après l’intégration de YW1. Ne pas redemander les fichiers Emerald pour cette simple correction de statut, ni recommencer les intégrations déclarées fonctionnelles. Les limites et preuves locales des anciens essais restent conservées comme historique.

> **Jalon courant — import massif du 16 novembre :** [rapport et limites](YOKAI_ARCHIPELAGO/DOCUMENTATION/FRLG_IMPORT_MASSIF.md). 625 checks par défaut (626 avec Terr’heure),74 anciens IDs conservés ; transport3, sauvegarde1 et registre256 dresseurs. Les descriptions15/74 ci-dessous sont historiques. Le graphe de progression reste regroupé et les cinq jeux ensemble ne sont pas validés.

Tests du jalon :617 détecteurs natifs et persistance à froid,2057 assertions ;37 protections ;36 contrôles avec vrai serveur/mGBA dont Wyatt et un dresseur ordinaire joués ;5 seeds résolubles à trois mondes. Captures et256 victoires sont vérifiées par fixtures natives, pas par166 captures et256 combats joués.

# Passation active — Yo-kai Multiworld, cinq jeux

Mise à jour : 14 novembre 2026. Base Claude : `4617e348fa6da7c9c1990078e097091ac01b0cca`.
Branche de travail : `codex/archipelago-five-games-20261114`. Le fangame principal et master sont intacts.

## Décision de périmètre

1. A — Yo-kai Watch 1, 3DS européenne. Remplace définitivement Yo-kai Watch 3.
2. B — Yo-kai Watch 2 : Spectres Psychiques, 3DS européenne. Réutiliser l’intégration V3 existante.
3. C — Mario Kart Wii PAL, avec personnages Yo-kai dans la même installation Dolphin.
4. D — Pokémon Rouge Feu × Yo-kai, fangame personnel.
5. E — Pokémon Yo-kai Emerald, six Yo-kai. Fonctionnel selon le retour utilisateur du16 novembre ; conserver cette intégration.

## Acquis et limites

- Les dépendances de Claude sont épinglées dans `YOKAI_ARCHIPELAGO/CONFIG/dependencies.lock.json`.
- La branche Codex est créée et son premier jalon poussé.
- Génération réelle YW2 + Mario Kart Wii réussie avec Archipelago 0.6.9 ; échanges calculés par le générateur, pas encore exécutés dans ces deux jeux.
- Sources exactes Rouge Feu retrouvées localement : ROM SHA-1 `40c59a9f240d29a7b16d1dd299b1125513a280c4`, SHA-256 `4192f6ac785eed8a431fdbb322712818c31c4bfd9573e647ee791b04452ed329`. Ce n’est pas le moteur vanilla de la racine. 301 espèces actives. Ne pas copier ses graphismes/musiques ni la ROM dans Git.
- Avant mise en attente d’Emerald : base française officielle recompilée au SHA-1 `ca666651374d89ca439007bed54d839eb7bd14d0`. Base AP × français compile aussi, sans couche Yo-kai, sans preuve de connexion en jeu. Traduction partielle, textes AP spécifiques encore à finir.
- Client Emerald généré corrigé (Panthéon, Steven, gardes mémoire, extension et manifeste). Huit tests avec mémoire simulée réussis ; aucune réception en jeu attestée.
- Connecteur Lua mGBA : messages TCP fragmentés et ports distincts ; sept tests Lua simulés réussis. `connect_emerald.py` est un outil de test préparé, pas un résultat de test réel.
- Quatre tests de contrat de traduction et cinq tests de préflight réussis. Pipeline complet avec ROMs Emerald non exécuté dans cette session.

## Fichiers de départ

Lire `AGENTS.md`, `YOKAI_ARCHIPELAGO/DOCUMENTATION/ETAT_DU_PROJET.md`, puis `YOKAI_ARCHIPELAGO/DOCUMENTATION/REPRISE_CODEX_20261114.md`.
Les rapports de la session Claude et ses pins restent dans `YOKAI_ARCHIPELAGO/DOCUMENTATION/historique/CODEX_HANDOFF_CLAUDE_20261114.md`. Leur ancien périmètre YW3 et leurs permissions refusées sont historiques.

## Règles

Développer dans les dossiers Multiworld, jamais dans le fangame principal. Pas de ROM, ISO, sauvegarde, capture, clé ou package incorporant des graphismes de jeu dans Git. Ne pas retoucher les six fiches validées d’Emerald. Ne jamais pousser sur master ni forcer l’historique.

## Priorité actuelle

Priorité Rouge Feu : poursuivre l’inventaire et la randomisation au-delà des quinze checks actuels. Ne pas repartir du mode bonus. Surf est randomisé et ses sources natives sont supprimées ; les autres clefs sont encore natives. Chaque nouvelle clef exige de tracer aussi ses restaurations automatiques et les accès avant d’étendre le pool. YW1 est la seule intégration encore absente selon le retour utilisateur du16 novembre. Emerald, YW2 et MKW sont déclarés fonctionnels ; le mod visuel MKW reste à ajouter. Le test collectif des cinq jeux reste à réaliser.


## Dernier jalon : récompenses ordinaires et Surf

Lire `YOKAI_ARCHIPELAGO/DOCUMENTATION/FIRERED_PROGRESSION_ET_OBJETS.md` et `GUIDE_FIRERED_ARCHIPELAGO_FR.md`. La demande intégrale est conservée dans `CAHIER_DES_CHARGES_FIRERED_20261114.md`.

- Coordonnateur public : branche Codex ci-dessus, jalon transport `f71f7169`.
- Vrai fangame : worktree local `/workspace/archipelago-work/firered-source-branch`, branche `codex/firered-archipelago-randomizer-20261114`, commit `d14b93cb803f60188e50917be2870c507eb6e748`, parent snapshot RC1 `a589cf0057fd0f579d003d8dd58616b3f4649ea2`. Le source complet n’est pas poussé sur le dépôt public de coordination.
- Build Surf SHA256 `0f6f0bfb739d246af3a73a7503db5c311c277133b9ce7befca1fcb79facd6c57`. Profil mesuré local `build.json`, package sans graphismes compilable avec `make_apworld.py`. Les données de jeu, le scénario et les cartes n’ont pas été remplacés.
- Quinze checks : 8 badges, 6 objets forêt remplacés, 1 don Safari remplacé. Surf progression AP unique, autres clefs natives. Le quatrième badge est dans `PokemonTower_7F`, pas Céladopole.
- Sauvegarde AP64 octets : SB2 +0xE20, entre Blasters et monstre aspiré. Voir audit et assertions. Contrôles de session, index/idempotence, sac plein différé, reprise Flash à froid testés dans le C réel.
- Réseau réel : serveur AP, client officiel, mémoire mGBA native via adaptateur Python. Potion et Surf reçus, badge Wyatt gagné par le moteur, collecte visible/cachée et don Safari validés sans donner l’objet original, Goal envoyé après vrai record Panthéon. Équipe, positions et contextes de scripts sont préparés par fixtures. Le dernier boss n’a pas été joué dans ces tests ciblés, ni toute la Ligue. Windows/Lua graphique reste non testé.
- Cinq seeds à trois mondes + une génération avec les noms des créateurs réussies. Analyse des sphères livrée ; aucun nombre de sphères ne représente une durée. Le graphe Kanto reste volontairement regroupé tant que les autres objets restent natifs.
- 33 tests unitaires réussis, dont les tests Emerald existants à mémoire simulée (aucune reprise du chantier gelé).
- YW1 : APWorld expérimental, génération refusée par défaut ; sonde Azahar en lecture seule au title ID EUR 0004000000167800. Aucun jeu EUR testé. YW2 : réutilisation V3, génération testée ; réception en jeu non testée.
- MKW : assembleur local de mods visuels RMCP01/Riivolution avec tests synthétiques ; aucun asset téléchargé ni visibilité en jeu validée. Les mêmes Dolphin et disque PAL devront héberger AP et les remplacements visuels.

Les cinq créateurs ont cinq slots : Yochix/YW1, Juste Yoann/YW2, RougeFeu (Kammy64 ou Petit Shiny), Krackonyx/MKW, Dejais/Emerald. `CONFIG/createurs/jouables/` contient seulement les trois YAML utilisables pour le développement. Les deux modèles non jouables sont séparés dans `en_attente/`. Le générateur officiel peut lire aussi des fichiers dont l’extension n’est pas YAML ; ne pas lui donner un dossier contenant des README ou modèles en attente.

## Travaux à poursuivre

Finir l’audit des 351 objets et 67 macros de dons, compléter les sources C, activer progressivement les sources pré-Ligue sûres. Détailler les régions et randomiser les autres CS/clefs sans récompense en double. Étendre le canal de checks au-delà de ses 16 bits avant de dépasser huit collectes. Tester le parcours manuel et le chemin graphique Lua/Windows. Poursuivre YW1/YW2/MKW avec les transports éprouvés et les copies locales fournies à terme ; ne pas redemander les fichiers Emerald. Aucune intégration à cinq jeux n’est déclarée fonctionnelle.


## Correctif transport après le jalon Surf `8e82d34e`

Un sac plein doit différer les dons entrants sans bloquer les checks sortants. Le client l’autorise désormais et affiche un avertissement. Le test réseau complet passe 24 contrôles : Potion en attente pendant Wyatt, badge envoyé malgré cette attente, remise reprise après libération du sac, collectes et Safari, puis Goal effectivement journalisé par MultiServer. La fixture restaure les quantités par les fonctions natives : le chiffrement peut changer pendant un combat, donc recopier un ancien sac chiffré serait invalide.

`build_firered.sh` a été exécuté sur un dossier neuf depuis le snapshot : ROM identique byte pour byte au build testé. Preuve `firered_reconstruction.json`. Le code C et son commit local `d14b93cb` sont inchangés par ce correctif client. Lors d’une extension de protocole future, séparer version de sauvegarde et version de transport ou prévoir une migration explicite, afin de conserver le ledger existant.


## Reprise du 16 novembre 2026 — extension FRLG validée

État actif : `YOKAI_ARCHIPELAGO/DOCUMENTATION/FRLG_EXTENSION_VALIDEE.md`. Tableau comparatif enregistré avant l’implémentation au commit `88ba5698`. Port MIT Vyneras `frlg-stable` / `3d1359cf`, inventaire1715 et régions symboliques réutilisés ; aucun patch vanilla ni code C non licencié importé.

74 checks par défaut, 75 avec `random_terreur`. Les quinze IDs historiques sont inchangés. 45 objets visibles, 13 cachés, Safari, cinq assistants Chen, accueil Bingo, amitié Jibanyan, huit badges. L’enquête Alyzon/Gorgouille est postgame et exclue. Le premier événement Terr’heure est aléatoire, optionnel, jamais progression. Surf ET Flash randomisés ; autres clefs natives.

Source complet local : `/workspace/archipelago-work/firered-source-branch`, branche `codex/firered-archipelago-checks-20261114`, commit `9a35394a01e4c3c10985287c09b42277a6ae6006`. SHA256 `d85d62c7638f8290f7b62e635f170b73a3f5100c555374dfceb8af2f6b603972`, reconstruction propre identique dans `firered-expanded-repro`.

Transport2, sauvegarde1, même bloc64 octets SB2+0xE20. Bitmap64 octets RAM et empreinte catalogue contrôlée ROM/profil/seed. Ne pas réutiliser le package/profil du mode Surf précédent. Le getter Yopple ajouté est purement en lecture : l’ancienne garde confondait carte compatible avec Aspirateur réellement occupé et bloquait toutes les grottes. Le journal de reprise suspend la distribution ; tests de l’état journal explicitement préparé, pas une preuve d’un don reçu pendant une vraie lecture de journal.

211 contrôles natifs vérifient les66 sources déterministes, les seuils capturés (pas vus), les remises supprimées et les marqueurs après redémarrage. 37 contrôles de protections natifs et37 tests unitaires passent. 10 seeds à trois mondes +5 avec Terr’heure optionnelle sont terminables selon la logique ; aucun progrès dans le check RNG. Le vrai test réseau valide aussi Flash, l’assistant10 captures, les événements Bingo/Jibanyan et leur idempotence. Voir les preuves dédiées `*_extensions*` et `*_v2`.

Les essais utilisent contextes, positions et bits de capture préparés : pas un parcours manuel de toutes les cases, ni cinquante captures jouées. Les événements RNG natifs ne sont pas joués. Windows/Lua et cinq jeux ensemble non validés. Emerald toujours gelé. Le reste des candidats/clefs nécessite un audit, notamment les restaurations automatiques et les endroits à visite unique (bateau exclu). Le graphe conserve des étapes narratives regroupées tant que leurs clefs restent natives.
