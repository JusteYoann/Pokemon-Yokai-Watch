# Passation active — Yo-kai Multiworld, cinq jeux

Mise à jour : 14 novembre 2026. Base Claude : `4617e348fa6da7c9c1990078e097091ac01b0cca`.
Branche de travail : `codex/archipelago-five-games-20261114`. Le fangame principal et master sont intacts.

## Décision de périmètre

1. A — Yo-kai Watch 1, 3DS européenne. Remplace définitivement Yo-kai Watch 3.
2. B — Yo-kai Watch 2 : Spectres Psychiques, 3DS européenne. Réutiliser l’intégration V3 existante.
3. C — Mario Kart Wii PAL, avec personnages Yo-kai dans la même installation Dolphin.
4. D — Pokémon Rouge Feu × Yo-kai, fangame personnel.
5. E — Pokémon Yo-kai Emerald, six Yo-kai. **En attente : ne plus demander ses fichiers pour l’instant.**

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

Priorité Rouge Feu : poursuivre l’inventaire et la randomisation au-delà des quinze checks actuels. Ne pas repartir du mode bonus. Surf est randomisé et ses sources natives sont supprimées ; les autres clefs sont encore natives. Chaque nouvelle clef exige de tracer aussi ses restaurations automatiques et les accès avant d’étendre le pool. YW1 et Emerald ne sont pas jouables ; ne pas générer une fausse session à cinq jeux.


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
