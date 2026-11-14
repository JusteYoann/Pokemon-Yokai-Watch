# Rouge Feu — transport natif confirmé, 14 novembre 2026

Sources : snapshot complet ROM05 RC1 `a589cf0057fd0f579d003d8dd58616b3f4649ea2`, SHA256 original `4192f6ac785eed8a431fdbb322712818c31c4bfd9573e647ee791b04452ed329`. Branche locale réelle du fangame : `codex/firered-archipelago-randomizer-20261114`. Le dépôt de coordination reste sur `codex/archipelago-five-games-20261114` ; son moteur vanilla n’est pas utilisé.

Le transport bonus compilé a le SHA256 `aaed938c8f02fcda2ec5eb2329ad801e4f2b377380f63ce8b83e591df59e9c15`. Preuves JSON dans `preuves/`. Les tests ont été relancés avant la randomisation. Ce jalon conserve encore les récompenses natives : ce n’est pas le randomizer final.

## Sauvegarde auditée et testée

Les 64 octets AP se trouvent dans SaveBlock2 à `0xE20..0xE5F`, soit `filler_B20 + 0x300`. Le début de ce filler est déjà occupé par la sauvegarde de l’équipe Blasters (608 octets). La créature aspirée occupe `+0x380..0x3CF`. SaveBlock1 `unused_3A94` est déjà pris par l’Aspirateur ; la zone Nuzlocke est également préservée. Assertions C et tests natifs vérifient les limites, les voisins, la restauration Blasters et la créature aspirée.

Tests mGBA libretro réels : inventaire, séquences, mauvaise graine/slot, replay, sac plein/réessai, écriture Flash, arrêt de l’émulateur, reprise depuis la batterie et replay après redémarrage. Les données et compteurs sont sauvés ensemble par le moteur ; comme dans le jeu original, les actions depuis la dernière sauvegarde sont perdues en cas d’arrêt brutal. Ne pas employer de savestates pendant une session AP.

## Réseau réellement testé

Archipelago 0.6.9, serveur MultiServer réel et client BizHawk officiel, transport Python vers la mémoire réelle du cœur mGBA. Potion envoyée depuis le serveur, reçue dans le sac ; reconnexion sans doublon. Combat Wyatt joué par le moteur après préparation d’équipe et de position par fixture : aucun flag de badge injecté. Le serveur a enregistré son check et envoyé une Figurine de Photortue au slot YW2. Le jeu YW2 n’était pas connecté : sa réception native n’est pas prouvée.

Non testés : mGBA graphique/Lua sur Windows, cinq jeux simultanés, partie complète, progression randomisée, réception en jeu YW1/YW2/MKW/Emerald. Les tests Lua précédents sont simulés. Emerald reste gelé.
