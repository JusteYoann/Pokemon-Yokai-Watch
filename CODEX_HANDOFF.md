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

Développer les quatre autres jeux sans attendre Emerald. Vérifier les projets YW1 existants, démarrer son APWorld avec états expérimentaux explicites ; réutiliser YW2 et MKWii ; développer le transport Rouge Feu sur une copie du snapshot exact et tester ses dons/checks avec mGBA si possible. Chaque résultat distingue calcul de logique, protocole simulé, émulation réelle et test Windows.
