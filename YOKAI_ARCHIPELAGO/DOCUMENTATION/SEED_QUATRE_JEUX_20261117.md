# Première seed à quatre — test du17 novembre 2026

**Seed1711202601 générée et résoluble selon les quatre APWorlds.** Identifiant du serveur : `40446171867215790995`. Les quatre slots participent aux échanges de progression. YW1 n’est pas inclus.

| Slot | Jeu | Checks |
|---|---|---:|
| Juste Yoann | Yo-kai Watch2 : Spectres Psychiques |444|
| RougeFeu | Pokémon Rouge Feu × Yo-kai Watch0.5.0 |628|
| Krackonyx | Mario Kart Wii |288|
| Dejais | Pokémon Yo-kai Emerald français0.2.1 |269|
| **Total** | | **1629** |

L’APWorld Emerald a été reçu en pièce jointe, identifié puis installé localement. Signature vérifiée : `pokemon emerald / yokai ap fr2`. SHA256 du package : `6fc85d334553f29491743cd5acac5eb804e3642a921f50d0700dfa98930e8224`. Le précédent blocage de fichier absent est levé. Ce package et le patch Emerald généré contiennent des ressources privées : ils ne sont pas publiés sur GitHub.

## Ce qui est effectivement testé

1. **Génération officielle AP0.6.9 à quatre mondes.** Victoire collective possible selon les règles installées, ensemble des emplacements accessible selon le solveur, participation de chaque slot à la réception et à l’envoi de progression. Le pool compte103 placements de progression distants sur11 directions. Les16 sphères sont des étapes logiques, pas une durée de jeu. Le modèle FR reste regroupé autour des capacités et étapes natives ; il ne prouve pas un parcours manuel de chaque lieu.
2. **Vrai serveur et quatre clients réseau :36 contrôles réussis.** Onze checks choisis dans les placements de cette seed sont envoyés par des clients de test ; leurs objets de progression arrivent aux destinataires prévus. Les doublons n’accordent aucun objet supplémentaire. Les quatre reconnexions restituent les objets et checks, puis une vraie sauvegarde serveur et son redémarrage restituent les mêmes données. Aucun don administrateur ni faux Goal utilisé pour ce test.
3. **Rouge Feu réel dans mGBA sur cette même seed :44 contrôles réussis.** Client officiel, réception des CS, conservation du check d’Ariane après Coupe distante, sac plein avec checks sortants, reconnexion, scripts d’objets, Wyatt et un dresseur ordinaire réellement combattus, acquittement des captures préparées par fixture, et Goal après record Panthéon. Position, équipe et certains prérequis restent des fixtures. Cette série utilise ses propres dons administrateur pour les tests de remise ; elle est distincte du routage sans dons administrateur du point2.

**Le point2 simule les accomplissements de jeu.** Il vérifie les vrais paquets et la persistance du serveur, pas la lecture mémoire d’Emerald/YW2/MKW. Seul Rouge Feu est émulé dans cette campagne. Les quatre émulateurs simultanés, la réception des objets dans les trois autres jeux, et une campagne complète ne sont pas testés ici. Leurs tests ciblés antérieurs indiqués par l’utilisateur restent valables dans leur propre périmètre. Le mod visuel MKW manque encore ; il n’affecte pas cette génération.

## Fichiers et reprise

Les fichiers privés restent dans `/workspace/exports/archipelago-quatre-jeux-20261117/` : archive officielle avec spoiler réservé à l’organisateur, `Seed_4_jeux_joueurs_sans_spoiler.zip` avec données serveur/patch Emerald/quatre YAML, et manifeste des hashes. Aucun fichier `.apsave` du banc d’essai n’est distribué. Commencer avec de nouvelles sauvegardes et conserver son propre `.apsave` pour la vraie partie.

La ROM FR AP est compilée depuis les sources complètes RC1, SHA256 `94e9cec46c19b351b0ef655c6b11df88237552746e2cdd18c0dac258ad16fc2b`. Elle n’est pas publiée. Le package FR et le profil doivent venir de cette build ; le patch Emerald correspond uniquement à cette seed et à sa base française compatible. Les autres packages sont épinglés dans le manifeste de génération.

Pour lancer le serveur, utiliser le `.archipelago` du ZIP sans spoiler avec `MultiServer.py`, puis les clients des quatre intégrations et les noms exacts du tableau. Conserver le même package/ROM/seed/slot après reprise. Les ports mGBA distincts du [guide quatre jeux](FIRERED_VERSION_TEST_4_JEUX.md) restent valables. L’organisateur garde le spoiler de côté ; les joueurs utilisent le ZIP sans spoiler.

Attention au banc de test : AP0.6.9 parse `--savefile` mais son point d’entrée ne l’applique pas. Le nouveau test copie donc les données serveur dans un dossier temporaire et vérifie la sauvegarde voisine automatique, puis nettoie ses états. Cela évite de mélanger les checks simulés avec la vraie partie. Le premier essai ayant révélé ce comportement a été corrigé ; seul le résultat complet après correction est présenté comme réussi.

## Reproduire les contrôles

Depuis le dépôt, avec les mêmes dépendances et les quatre APWorlds installés localement :

```sh
python YOKAI_ARCHIPELAGO/SCRIPTS/generate_four_game_seed.py --archipelago <AP> --out <sortie> --seed 1711202601
python YOKAI_ARCHIPELAGO/TESTS/verify_four_game_server.py --archipelago <AP> --multidata <seed.archipelago> --out <rapport.json>
python YOKAI_ARCHIPELAGO/TESTS/verify_firered_network.py --archipelago <AP> --multidata <seed.archipelago> --build <build_FR> --libretro <mgba_libretro.so> --slot RougeFeu --test-worlds yokaiwatch2,mkwii,pokemon_yokai_firered,pokemon_yokai_emerald --out <rapport_FR.json>
```

Le dernier script désactive la sauvegarde du serveur de test ; il n’est pas la commande de lancement d’une vraie partie. Ne pas utiliser de sauvegarde personnelle dans les fixtures.

Preuves publiées sans ROM ni ressources privées : [génération](preuves/generation_quatre_jeux_20261117.json), [serveur quatre slots](preuves/serveur_quatre_slots_20261117.json), [mGBA Rouge Feu](preuves/firered_seed_quatre_jeux_natif_20261117.json).
