# Récupération Pokémon × Yo-kai Watch

**17 octobre 2026 — RÉCUPÉRATION PARTIELLE. Le jeu personnalisé complet n'est pas retrouvé.**

Branche de travail : `recovery/sauvegarde-elements-retrouves`. Ne pas fusionner cette branche sur `master` comme une version finale du hack.

## Résultat principal

Les sources de la recette finale conservées uniquement dans l'ancien environnement ne sont pas accessibles dans cette instance. En revanche, les graphismes historiques des 151 espèces, les propositions artistiques, de nombreux documents validés et les archives d'origine ont été récupérés et regroupés. Aucun développement des nouvelles OST ou des dix quêtes n'est commencé.

Cette branche est la collection de récupération la plus complète actuellement assemblée, **pas une base jouable complète des fonctionnalités Yo-kai**. Le moteur actif demeure celui de Rouge Feu d'origine ; les sources Yo-kai manquantes n'ont pas été remplacées par une reconstruction improvisée.

## Branches et versions retrouvées

Voir [BRANCHES_RETROUVEES.csv](BRANCHES_RETROUVEES.csv) et [REFERENCES_DISTANTES.txt](REFERENCES_DISTANTES.txt).

| Branche | Commit | Contenu spécifique retrouvé |
|---|---|---|
| master | 037335f4c | Rouge Feu d'origine |
| preview/yokai-84-contact-sheets | 2f8b5b391 | Planches des 84 sprites |
| preview/yokai-gallery-151 | d9d4673e1 | Galerie et instantané indexé des 151 espèces |
| art/yokai-sprite-rework-phase1 | 773cb21b1 | Galerie + 51 propositions artistiques |
| audio/audit-musical-publication | f7e99e62b | Analyses, comptes rendus et aperçus audio antérieurs |

Toutes ces branches ont **zéro différence** avec master dans `src/`, `include/`, `data/`, `graphics/` et `sound/`. Les fichiers sous `docs/` ne prouvent donc pas une intégration au jeu. Aucune fusion de ces branches ne peut restaurer à elle seule les scripts et le moteur personnalisés manquants.

Le commit `145044ec29f4ad7ee03c1942e8a925d15a9f89e1` de `qa/recette-finale` et le commit audio `6d11139e2c257f5887ce7e26b56e8c56a8eab46d` ne sont ni présents localement ni récupérables par leur SHA depuis GitHub (`upload-pack: not our ref`). Les rapports publics documentent leur ancienne existence locale, sans contenir leurs sources.

## Ressources effectivement récupérées et contrôlées

- **906 ressources GBA** du snapshot galerie : 151 faces, 151 dos, 151 icônes à deux frames, 151 empreintes, 151 palettes normales et 151 palettes shiny. Trois palettes d'icônes partagées s'ajoutent. SHA256 vérifiés ; 302 sprites de combat non vides, canevas 64×64, indices 4bpp. Le fichier ZIP de 910 membres comprend ces 909 ressources et son manifeste.
- **14 redesigns approuvés** : 28 PNG indexés 64×64 et leurs 28 palettes historiques retrouvés. La liste blanche numérique est enregistrée dans [REDESIGNS_APPROUVES_RECUPERES.json](REDESIGNS_APPROUVES_RECUPERES.json). Les 37 autres propositions restent archivées comme essais non approuvés ; aucun dessin n'est appliqué au jeu.
- **151 correspondances canoniques** : numéros, `SPECIES_*` et IDs concordent avec la galerie. L'instantané porte encore 21 noms anciens : leur détail est consigné, sans écraser cet instantané historique. Le CSV canonique reste la référence des noms.
- **151 lignes de statistiques/types/talents**, toutes avec six statistiques numériques et un total BST cohérent ; **56 relations évolutives** récupérées en CSV.
- **151 entrées CT/CS** dans le fichier source fourni, et le CSV d'obtention de 151 espèces, accompagné du registre validé.
- Le premier CSV d'attaques ne couvre que **21 espèces / 282 lignes**. Les **154 captures** de l'archive d'attaques sont récupérées séparément : elles ne sont pas présentées comme 151 learnsets déjà transcrits ou intégrés.
- Documents validés : équipes de boss, caméos, protagonistes, noms canoniques, adaptation textuelle, shiny et recette finale. Les réponses explicites du créateur sont résumées dans [VALIDATIONS_CONVERSATION.md](VALIDATIONS_CONVERSATION.md).
- **Huit archives de références non musicales**, contenant **530 membres**, sont conservées avec leurs hashes : données, attaques et images des Yo-kai, shiny, protagonistes et caméos. Leur intégrité et celle de tous leurs membres ont été vérifiées sans exécuter ni modifier leur contenu.

Les 417 fichiers récupérés des branches GitHub et les 18 documents récupérés des pièces jointes possèdent des manifestes de provenance. Les 19 fichiers d'écoute/archives audio déjà publiés ne sont pas recopiés sur cette nouvelle branche. Aucun nouvel enregistrement musical ni ROM n'est publié.

## Fonctionnalités réellement actives / manquantes

La table [FONCTIONNALITES.csv](FONCTIONNALITES.csv) distingue chaque donnée récupérée de son intégration. Les fichiers actifs de noms, données d'espèces, évolutions, rencontres, équipes et partage d'expérience sont toujours identiques à master d'origine.

**Non retrouvés :** derniers fichiers source du moteur personnalisé, intégration des noms et sprites, learnsets C définitifs, conditions d'évolution spéciales, rencontres personnalisées et cadeaux, équipes intégrées, personnages GBA complets, sprites statiques et overworld créés, scripts des caméos et leurs flags, traduction intégrale rédigée, dernier travail shiny et verrou des 67 espèces, Multi Exp. permanent et réglages XP, correctifs QA et bancs privés mGBA, assets DPCM expérimentaux et outils privés de lecture.

Les palettes shiny du snapshot **précèdent la direction artistique finale**. Leur présence pour 151 espèces ne prouve ni les derniers designs ni le blocage du statut shiny pour les 67 exclues. Les références de Nathan/Katie/Matt sont des images, pas leurs séries GBA complètes. Le document de recette récupéré est un cahier des charges, pas le rapport de tests manquant.

Les 20 OST, dix quêtes, nouveau Red et Juste Yoann relèvent de la phase suivante ; aucune intégration de ces nouveautés n'est revendiquée. L'image Juste Yoann est reçue dans la conversation.

## Recherche des sauvegardes et portée de l'audit

Recherche effectuée dans les checkouts et emplacements accessibles de `/workspace`, `/tmp`, `/home/agent`, `/mnt` et les dossiers partagés. Aucune autre copie de projet ni ancienne ROM Yo-kai complète retrouvée. Les trois petits fichiers `.gba` déjà présents dans `data/` sont des ressources du dépôt d'origine, pas la ROM personnalisée recherchée. Les caches et répertoires d'identifiants ne sont pas lus.

Les objets Git et reflogs accessibles ne contiennent pas de commit QA orphelin. Les références distantes annoncées comprennent HEAD et cinq branches ; aucune référence tag/pull supplémentaire n'est annoncée. L'API GitHub des pull requests est inaccessible par cette connexion (403 du proxy) : les éventuels artefacts Actions, PR supprimées ou historiques d'autres environnements ne sont donc pas déclarés exhaustivement inspectés. Aucun outil disponible ici ne permet de reconnecter un ancien environnement ou de parcourir l'ensemble des autres sessions ; l'historique utilisé est celui de cette conversation et les rapports récupérés.

**Aucune perte définitive n'est démontrée.** Les fichiers sont non retrouvés dans le périmètre vérifié ; une ancienne instance, un export utilisateur ou une sauvegarde indépendante peut encore les contenir.

## Meilleure base et méthode de récupération

1. Priorité à la restauration de la vraie base QA `145044ec…` ou d'un export plus récent : c'est la seule façon de récupérer exactement le code ancien, les dialogues et les correctifs.
2. Sauvegardes historiques à rechercher dans l'ancienne instance : `sources-and-derived.tar.gz` et son `manifest.json`, sous `/workspace/scratch/music-before/`, ou un export complet des sources. Le bundle `branches-before.bundle` avait été créé avant le commit qui sauvait les modifications non committées : il ne suffit pas seul à restaurer ces modifications.
3. Vérifier hashes et listes de fichiers avant import ; créer une branche de restauration séparée. Garder les fichiers conflictuels et leurs provenances ; éviter toute extraction aveugle sur les fichiers courants et tout reset destructif.
4. Ajouter les documents et ressources ici récupérés par chemins disjoints, puis les modifications manquantes de la base complète ; ne jamais appliquer automatiquement toutes les propositions artistiques.
5. Si aucune base complète n'est retrouvée : une **reconstruction partielle depuis les données validées est possible**, mais ce serait une nouvelle intégration à autoriser après ce rapport, pas une récupération exacte. Stats, correspondances, CT/CS et graphismes disposent de sources concrètes ; événements, traductions et correctifs exigeraient un travail neuf, et certains détails devraient être revalidés. Ne pas le commencer dans cette mission.

## Vérifications et compilation

Les contrôles réellement exécutés sont dans [CONTROLES_EXECUTES.json](CONTROLES_EXECUTES.json). Rejouer :

```sh
python3 RECUPERATION_PROJET/scripts/verifier_recuperation.py
python3 RECUPERATION_PROJET/scripts/verifier_archives.py
```

Python 3, Pillow et libarchive sont nécessaires pour ces contrôles. Ils n'exigent ni ROM ni fichiers cachés de l'ancien environnement. La portée reste l'intégrité des ressources et données ; ils ne valident pas le fonctionnement du hack.

La préparation de la chaîne de compilation et le contrôle d'un clone GitHub propre sont en cours. Le résultat sera ajouté à ce rapport. Si le moteur d'origine compile, cela validera uniquement sa reproductibilité, pas les fonctionnalités Yo-kai absentes. Aucun parcours mGBA ni test de gameplay de la version personnalisée n'a été exécuté ici.

## Sauvegarde GitHub et exception musicale

La sauvegarde est effectuée sur la branche dédiée, sans pousser de version incomplète sur master. Une référence de sauvegarde distincte de master est créée. L'état exact de publication et de vérification depuis un clone figure dans le rapport de synchronisation ajouté à ce dossier.

Les sources et ressources actuellement retrouvées sont publiables sur la branche de récupération. Les sources manquantes ne peuvent pas être incluses par une simple synchronisation. Les sauvegardes locales sont complémentaires, jamais une preuve de sauvegarde distante.

Les MP3 sources, échantillons et conversions d'enregistrements protégés doivent rester dans un paquet externe sauvegardé par le créateur hors dépôt public. Leurs chemins privés et les démos MP3 ne permettent pas de reconstituer exactement les fichiers binaires de travail. Voir [COMPILATION_ET_AUDIO_EXTERNE.md](COMPILATION_ET_AUDIO_EXTERNE.md) pour l'état réel et le contrat nécessaire. Sans les ressources externes appropriées, une future compilation ne pourra pas être strictement identique musicalement à une version utilisant ces OST.

Après restauration : commits/push réguliers de tous les fichiers nécessaires, vérification des fichiers ignorés, contrôle depuis un clone séparé, publication du SHA et du résultat de build ; conserver les designs en attente explicitement marqués. Une fusion vers master ne sera préparée qu'après validation de la base complète, compilation et vérification des fonctionnalités, puis accord du créateur pour reprendre le développement.
