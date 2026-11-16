# Installer et tester le jalon Rouge Feu Archipelago

État actuel : [extension FRLG validée](FRLG_EXTENSION_VALIDEE.md), 74 checks, Surf/Flash randomisés, transport2 et sauvegarde1. Une nouvelle seed est nécessaire. Les étapes de compilation et de transport restent les mêmes.

**Version de développement, pas encore la distribution définitive pour les cinq créateurs.** Le vrai serveur et mGBA libretro ont été testés sous Linux. La procédure graphique mGBA/Lua et Windows ci-dessous reste à valider sur PC. Ne pas réserver le tournage sur cette seule base.

## Ce qu’il faut préparer

- Sources complètes privées de la ROM05 RC1, avec `SOURCE_ROM05.json`, `SOURCE_FILES_SHA256.json`, graphismes et OST déjà autorisés localement. Ce n’est pas le code vanilla à la racine du dépôt Multiworld. Ne pas télécharger une ROM commerciale pour remplacer ces sources.
- Branche `codex/archipelago-five-games-20261114` du dépôt Multiworld.
- Archipelago 0.6.9 au commit du fichier `CONFIG/dependencies.lock.json`. L’exécution des outils Python ci-dessous utilise **le dépôt source Archipelago et ses dépendances**, pas seulement son installateur Windows.
- agbcc au commit `da598c1d918402c42c0c0d7128ba14567f3175e9`, construit selon ses instructions ; binutils ARM 2.44, GCC hôte 14.2, Make 4.4.1 et Python 3.12 correspondent au banc vérifié. Pillow est nécessaire à des générateurs graphiques du fangame.
- Pour le jeu graphique : mGBA 0.10 ou supérieur **avec Lua**, et les modules `base64.lua`, `json.lua` du dossier `Archipelago/data/lua`.

Les sources privées existent sur le poste de développement, mais ne sont pas republiées dans cette branche publique. Le script refuse une autre variante du fangame plutôt que d’écraser ses changements. Si vous disposez seulement de la ROM, ces instructions ne recréent pas magiquement son code source.

## Reconstruire localement sous Linux ou WSL

Depuis le dépôt Multiworld, adapter les trois chemins :

```sh
bash YOKAI_ARCHIPELAGO/SCRIPTS/build_firered.sh \
  /chemin/sources-completes-RC1 /chemin/agbcc /chemin/nouveau-build-AP
```

Le dossier de sortie doit être absent. Le script vérifie les entrées du snapshot, copie le jeu, ajoute les hooks AP, installe agbcc, compile et exporte les adresses mesurées. Il crée localement :

- `pokefirered_audio.gba` : jeu compilé, à ne pas publier ;
- `build.json` : profil lié à ce binaire ;
- `dist/pokemon_yokai_firered.apworld` : code AP et profil, aucune ROM ni image ;
- `YOKAI_AP_SOURCE_PATCH.json` : liste exacte des sources modifiées.

Reconstruction complète depuis une copie neuve également vérifiée, résultat byte pour byte identique (`preuves/firered_reconstruction_v2.json`). Build validée : SHA256 `d85d62c7638f8290f7b62e635f170b73a3f5100c555374dfceb8af2f6b603972`. Source complète locale : branche `codex/firered-archipelago-checks-20261114`, commit `9a35394a01e4c3c10985287c09b42277a6ae6006`, depuis `a589cf0057fd0f579d003d8dd58616b3f4649ea2`. Les binaires hôtes du compilateur sont réinstallés localement ; ils ne font pas partie du changement de gameplay.

Un autre hash demande une vérification ; ne pas contourner le contrôle en saisissant des offsets vanilla. Aucun patch binaire de distribution n’est publié à ce jalon : les générateurs sources sont livrés, les ressources privées restent locales.

## Installer le monde et générer

Copier **le package issu de cette compilation** dans `Archipelago/custom_worlds/`, sur le poste générateur/serveur et sur le poste client. Ne pas mélanger le package de l’ancien mode bonus avec la version Surf. Pour réutiliser aussi YW2 et MKW épinglés :

```sh
python YOKAI_ARCHIPELAGO/SCRIPTS/install_worlds.py \
  --dependencies /chemin/dependances --archipelago /chemin/Archipelago \
  --firered-apworld /chemin/nouveau-build-AP/dist/pokemon_yokai_firered.apworld
```

Une installation différente n’est pas écrasée silencieusement ; sauvegarder ses fichiers puis employer `--replace` si nécessaire. Les réglages par créateur sont dans `CONFIG/createurs/`. Le sous-dossier `jouables/` contient uniquement les trois YAML de développement. Les modèles YW1/Emerald sont séparés dans `en_attente/` et ne doivent pas être passés au générateur tant que ces mondes ne sont pas jouables. Les générations vérifiées concernent YW2, MKW et Rouge Feu.

Exemple YAML Rouge Feu :

```yaml
name: RougeFeu
game: Pokemon Yo-kai FireRed
Pokemon Yo-kai FireRed:
  progression_balancing: 65
  accessibility: full
```

Choisir Kammy64 ou Petit Shiny comme nom lors de la préparation de la vraie seed ; garder exactement le même nom dans le client. Les objets importants sont placés librement sous contraintes de logique. Aucun piège FR. Désactiver explicitement les pièges MKW/YW2 dans leurs YAML.

Lancer le générateur officiel `Generate.py` avec le dossier des YAML et conserver son ZIP, son spoiler privé et sa seed. Lancer ensuite `MultiServer.py` avec ce ZIP. Le nom du fichier fourni au serveur est celui généré, pas un nom inventé. En production, **ne pas utiliser `--disable_save`**, réservé aux tests isolés : conserver le fichier `.apsave` du serveur pour la reprise.

## Lancer dans mGBA sur le PC du joueur

1. Ouvrir **la ROM AP recompilée**, commencer une nouvelle partie et sauvegarder depuis le menu du jeu. Une sauvegarde de la ROM normale ou d’une autre seed n’est pas une entrée compatible.
2. Copier `CONNECTORS/mgba/connector_bizhawkclient_yokai.lua` dans `Archipelago/data/lua/`, à côté de `base64.lua` et `json.lua`.
3. Dans la fenêtre de scripts mGBA, charger un petit fichier Lua local comme celui-ci (adapter le chemin ; garder les `/` sous Windows) :

```lua
YOKAI_CONNECTOR_PORT = 43056
package.path = "C:/Archipelago/data/lua/?.lua;" .. package.path
dofile("C:/Archipelago/data/lua/connector_bizhawkclient_yokai.lua")
```

4. Avec le Python possédant les dépendances Archipelago, lancer le client de ce dépôt. Exemple PowerShell, à adapter :

```powershell
python "C:/Projet/YOKAI_ARCHIPELAGO/CONNECTORS/mgba/connect_firered.py" --archipelago "C:/ArchipelagoSource" --server "adresse-du-serveur:38281" --slot "RougeFeu" --emulator-port 43056
```

Le serveur distant doit être joignable depuis chaque PC. L’interface émulateur/client reste **locale** ; il n’est pas nécessaire d’exposer le port 43056 sur Internet. En cas de mot de passe, utiliser localement la variable `YOKAI_AP_PASSWORD` ; ne pas la committer.

Attendre le message de connexion avant la première collecte. Un mauvais profil, une mauvaise seed ou un mauvais slot bloque les écritures. Si le client annonce une séquence incohérente, arrêter et conserver les logs ; ne pas modifier la sauvegarde ou les compteurs à la main.

## Jouer, sauvegarder, reprendre

Une récompense peut arriver pendant un combat ou une cinématique : elle attend un état sûr. Si le sac est plein, elle reste en attente ; le client demande de libérer de la place. Les checks sortants continuent d’être envoyés pendant cette attente. Fermer les dialogues/cinématiques natifs pour reprendre la distribution en état sûr. Le compteur n’avance qu’après la remise réussie. Les collectes déjà validées sont renvoyées de façon idempotente au serveur après reconnexion. Surf exige toujours le cinquième badge.

Sauvegarder normalement, fermer proprement mGBA et conserver la sauvegarde `.sav`. Pour reprendre, relancer le même serveur et sa sauvegarde AP, la même ROM, la même sauvegarde et le même slot. Aucun savestate, retour arrière ou changement de seed en cours. Comme dans le jeu original, un arrêt brutal avant la sauvegarde perd les actions non sauvegardées.

La victoire est la fin de Ligue suivie du véritable enregistrement au Panthéon. Le signal réseau peut attendre le retour à un état sûr de l’overworld. Le postgame reste présent, mais ne contient aucun check FR de ce jalon.

## Indices pendant la vidéo

Après 20 minutes de blocage réel, demander un indice natif AP avec `!hint` et le nom exact de l’objet ; le serveur indique les coûts et restrictions éventuels. Vers 30 minutes, faire un point collectif. Vers 45 minutes, l’organisateur consulte le spoiler et donne une seule indication ciblée. Ces durées sont une règle de tournage, pas un minuteur programmé dans la ROM.

## Résultats et limites

Voir `preuves/firered_native_surf.json`, `firered_reseau_surf.json`, `firered_pantheon_surf.json`, `generation_trois_mondes_surf.json`. Le transport testé est un adaptateur Python relié à la vraie mémoire mGBA libretro, avec le vrai client officiel et un vrai serveur. Les contextes d’interaction, l’équipe et les positions sont préparés par fixtures. Les scripts, récompenses, flags, sauvegardes et échanges sont traités par les vrais programmes. Aucun parcours intégral ni test Windows/Lua graphique n’est revendiqué.

Surf et Flash sont randomisés ; les autres objets clés restent natifs. Les sources candidates ne sont pas toutes activées. La réception native YW1/YW2/MKW et le Multiworld à cinq jeux restent à valider. Emerald demeure en attente.
