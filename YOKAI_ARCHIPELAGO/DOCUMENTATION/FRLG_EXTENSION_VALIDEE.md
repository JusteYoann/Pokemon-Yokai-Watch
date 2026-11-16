# Extension des checks Rouge Feu — 16 novembre 2026

Le tableau demandé a été enregistré **avant les modifications** au commit `88ba5698` : [tableau comparatif](FRLG_COMPARAISON.md), [correspondance complète JSON](FRLG_COMPARAISON.json). Référence communautaire : Vyneras/Archipelago, branche `frlg-stable`, commit `3d1359cf0606cee11eebfecc0d820063bef7c2a2`, port FRLG1.1.5 sous MIT. Même famille de décompilation, mais patch binaire incompatible avec notre ROM. Son fonctionnement en jeu vanilla n’a pas été testé ici. Aucun patch binaire ni offset ROM vanilla n’est appliqué.

## Comparaison et réutilisation

| Groupe | Décision |
|---|---|
| 1 715 entrées du port | Correspondance complète avec catégories, clés symboliques, IDs amont, régions et preuves dans nos sources |
| 15 checks historiques | Tous les IDs numériques conservés, badges natifs préservés |
| Objets ordinaires encore présents | Extension progressive aux cartes auditées ; récompense locale remplacée |
| Quatrième badge | Source réelle : Tour de Lavanville, pas l’arène de Céladopole |
| Coupe | Remise dans la quête Philosovni, pas importée depuis le capitaine vanilla |
| Scope / Flûte | La source physique du Scope donne la Flûte ; aucune deuxième récompense fantôme |
| Assistants Chen | Seuils natifs de 10,20,30,40,50 captures ; accès et récompenses adaptés |
| Bingo-kai | Accueil déterministe, pièces natives conservées comme introduction protégée, check AP séparé |
| Jibanyan | Amitié conclue, cadeau natif conservé, check AP séparé |
| Terr’heure aléatoire | Option désactivée par défaut, emplacement exclu de toute progression même si activé |
| Quête Oni/Alyzon | Désactivée : son appel réel est post-Ligue |
| Îles, grotte postgame, sources non résolues | Désactivées ; certaines îles pourraient être pré-Ligue, mais ne sont pas supposées sûres |
| Bateau à accès potentiellement perdable, objets cachés renouvelables/sous les pieds | Pas activés dans cette tranche |

Les identifiants symboliques, catégories et identifiants de régions amont sont réutilisés dans notre catalogue. Les IDs AP numériques historiques Yo-kai ne sont pas renumérotés : l’ID amont figure dans la correspondance. Pour les nouvelles sources classiques, l’ID reste `0x594B2000 + flag natif`. Les deux systèmes de badges/flags de récompense du port vanilla ne sont pas confondus.

Le graphe complet FRLG n’est **pas** importé aveuglément : les régions de nos checks sont reprises, avec des règles adaptées à Flash/Surf et au scénario natif conservé. Les autres clés restent natives, donc les étapes narratives ne sont pas encore décrites une par une. Ce modèle exprime la possibilité d’atteindre les checks, pas leur disponibilité immédiate ni une durée.

## Périmètre compilé

**74 checks par défaut** : 45 objets visibles, 13 objets cachés, don Surf du Safari, cinq assistants, accueil Bingo-kai, amitié Jibanyan, huit badges. Avec `random_terreur: true`, total75 ; ce check ne reçoit aucun objet de progression ni piège. Aucun check postgame ne fait partie de cette tranche.

Surf et Flash sont les deux objets de progression du pool. Les autres récompenses remplacées alimentent le pool par leur véritable identifiant d’objet natif ; les CT et cadeaux utiles restent classés utiles. Les clés nécessaires aux cinématiques et les autres CS sont conservées aux sources natives, hors pool. Pas de modification des statistiques, types, talents, évolutions, rencontres, équipes, cartes ou scénario.

## Assistants : captures réelles

Les rencontres sauvages de la Tour sont capturables : `src/battle_setup.c:CheckSilphScopeInPokemonTower` retourne explicitement FALSE dans ce fangame. Le Silph Scope vanilla n’est donc pas une exigence de collection à réintroduire.

Le code natif `GetPokedexCount` place le **nombre capturé**, et non vu, dans VAR_0x8006. Le premier nom `REQUIRED_SEEN_MONS` était trompeur. Les cinq tests de seuil sont conservés ; seule la remise de l’objet est remplacée. Recevoir Flash à distance ne valide pas le check de l’assistant et ne provoque pas de deuxième Flash chez lui.

Le compteur hérité est **Kanto, premières151 entrées nationales**, pas l’ensemble des301 Yo-kai. Cette règle d’origine n’est pas modifiée silencieusement. Le modèle vérifie la capacité de capturer : 20 espèces actives accessibles sans Flash, 53 avant Surf en incluant des évolutions naturelles au niveau30 au maximum. Les preuves proviennent des rencontres réelles FireRed du fangame, excluent les espèces retirées, et sont intégrées dans `checks.json`. Le joueur doit effectivement effectuer les captures avant d’obtenir le check. Les tests d’émulation préparent les bits vus/capturés ; ils ne jouent pas cinquante captures.

L’assistant Flash est accessible sans Flash ; les seuils plus élevés demandent la capacité de collection correspondante. Les régions de la Grotte Sombre et la suite de campagne utilisent Flash dans la logique. Le Panthéon demande Flash et Surf dans le solveur. Le jeu garde son comportement natif, y compris la possibilité de se déplacer dans le noir : cette exigence logique est conservatrice.

## Sauvegarde et transport

Transport2, **schéma de sauvegarde1 inchangé**, 64 octets toujours à SB2+0xE20. Les quinze marqueurs historiques restent présents. Un bitmap de64 octets en RAM expose les nouveaux flags/variables persistants ; aucun espace d’Aspirateur, Blasters ou monstre aspiré n’est réutilisé. Empreinte de catalogue contrôlée entre ROM, profil et seed. Une nouvelle génération est nécessaire pour la liste étendue ; ne pas mélanger anciennes seeds, ROMs et APWorlds.

La garde Yopple vérifie désormais l’état réellement occupé de l’Aspirateur par un getter en lecture seule. Le précédent `YoppleInDungeon` signifiait seulement qu’une carte était compatible avec l’appareil et bloquait toutes les grottes. Les remises sont aussi suspendues pendant la lecture du journal. Aucun comportement de l’Aspirateur ou du journal n’est réécrit.

## Vérifications et limites

- Compilation réussie, reconstruction complète dans un dossier neuf **byte pour byte identique**.
- 37 contrôles natifs de protections : replay, mauvaise seed/slot, séquences, sac plein, état Aspirateur, état journal préparé, sauvegarde à froid, régions protégées.
- 211 contrôles de scripts natifs : 66 sources déterministes, seuil insuffisant même avec151 espèces vues, remises supprimées, absence de doublons, flags et variables persistants après fermeture et reprise.
- 37 tests unitaires réussis.
- 10 seeds à trois mondes sans Terr’heure optionnelle +5 avec elle : terminables selon la logique, aucune progression dans l’emplacement aléatoire. Les positions de Surf/Flash et sphères figurent dans les rapports.
- Serveur MultiServer réel, client officiel, mémoire réelle mGBA via adaptateur Python : réceptions, badge Wyatt, collectes, événements et Goal. 31 contrôles réseau passent, dont le check de l’assistant10 et l’absence de nouvel envoi après répétition de l’accueil Bingo.

Les scripts sont exécutés avec positions et contextes d’interaction préparés. Le parcours manuel jusqu’à chaque case, les captures réelles, le déclenchement aléatoire de la Terr’heure, le Lua graphique Windows et une partie à cinq jeux ne sont pas validés. Les autres jeux ne sont pas supposés tous fonctionnels. Aucun résultat de génération ne garantit à lui seul l’absence de tout bug natif.

## Reconstruction et sources

Source complet privé : branche `codex/firered-archipelago-checks-20261114`, commit `9a35394a01e4c3c10985287c09b42277a6ae6006`, depuis le précédent jalon RC1. Générateur public dans `PATCHES/pokemon_yokai_firered/`. SHA256 compilé : `d85d62c7638f8290f7b62e635f170b73a3f5100c555374dfceb8af2f6b603972`.

Utiliser le même `SCRIPTS/build_firered.sh` avec les sources privées complètes RC1, puis installer l’APWorld produit par **cette** compilation. Les dépendances sont épinglées. La licence MIT du port de référence est jointe dans `THIRD_PARTY/` et dans le package APWorld, sans ressources commerciales. Voir le guide français pour le transport ; sa validation graphique reste à faire.
