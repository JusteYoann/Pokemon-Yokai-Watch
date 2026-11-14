# Reprise Codex — 14 novembre 2026

Base distante vérifiée : `claude/archipelago-multiworld` à `4617e348fa6da7c9c1990078e097091ac01b0cca`.
Branche de développement : `codex/archipelago-five-games-20261114`, dans un clone séparé.
`CODEX_HANDOFF.md`, `AGENTS.md` et l’état du projet ont été lus. Le code du fangame principal est préservé.

## Éléments nouveaux vérifiés

- Les dépendances sont récupérées aux commits de la passation, et recensées dans `CONFIG/dependencies.lock.json`.
- Le code et l’ELF de la ROM Rouge Feu ont été retrouvés dans l’environnement de travail : le SHA-1 RC1 est exactement
  `40c59a9f240d29a7b16d1dd299b1125513a280c4`, celui du jeu audité par Claude. Le snapshot source a été recompilé
  avec un SHA-256 `4192f6ac785eed8a431fdbb322712818c31c4bfd9573e647ee791b04452ed329`. Les sources existent donc ;
  elles ne sont pas copiées dans ce dépôt public avec les graphismes/musiques. Une intégration se fera sur une copie.
- Le comptage d’espèces actives de ce snapshot Rouge Feu est 301 ; les 304 cases repérées dans l’audit binaire ne
  doivent pas être automatiquement assimilées à 304 espèces jouables.

## Test prioritaire Emerald

Les ROMs Emerald et la build AP de la session Claude ne sont pas présentes dans cette machine. Le hack requis est
`ff71db053a6d4d0f31368d95b39c6b7d6038da13`. Leur emplacement a été demandé à l’utilisateur.
Le test réel mGBA ↔ serveur reste **non exécuté** tant qu’une build correspondant au jeu ne peut pas être lancée.
Aucune simulation ne sera étiquetée « jeu testé ».

## Périmètre

Les autorisations anciennes refusées dans l’environnement Claude ne sont pas des échecs de compilation établis.
La mission actuelle autorise à poursuivre les cinq chantiers. Les exécutions possibles seront testées ici ; les
fichiers personnels toujours absents resteront des prérequis explicites. Aucune modification des six fiches Yo-kai
validées d’Emerald, de leurs attaques ou de leurs emplacements n’a été décidée.
