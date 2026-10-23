# Maison d'exil de Don Morléone

Branche exclusive : `feature/boss-final-don-spiraton`, base distante et locale confirmée `7f2c7d69be797389717d5e802024221522431445`. Dépôt propre au départ ; aucune fusion.

La maison `SixIsland_WaterPath_House2` possède désormais un remplacement conditionnel de son habitant par Don Morléone. Le remplacement est prêt pour les flags de fin de Ligue ; **la finale normale complète n'est pas déclarée terminée ou activée par ce changement**.

## Comportement intégré

- Avant déblocage, le PNJ original conserve sa position(7,4), ses orientations natives et son dialogue existant, inchangé.
- Après victoire finale et Panthéon, Don utilise le même emplacement(7,4), orienté vers l'entrée. Son sprite overworld existant est réutilisé sans modification.
- Les deux modèles d'événement s'excluent : **un seul PNJ est réellement chargé**, en plus du joueur. Aucun sbire ou sprite de fusion.
- La maison, son mobilier, ses murs, ses collisions et ses warps sont inchangés. L'extérieur du Chemin d'O n'est pas modifié.
- Le dialogue de revanche est celui fourni par le créateur, avec coupures de lignes seulement. OUI lance le combat ; NON affiche « Une autre fois, peut-être... ».
- Chaque revanche réutilise directement le Dresseur743 de la Ligue. Aucune copie d'équipe ni nouvel identifiant de Dresseur.
- `trainerbattle_no_intro`, mode `TRAINER_BATTLE_SINGLE_NO_INTRO_TEXT`, lance la revanche sans test préalable du flag743 : aucune remise à zéro de ce flag n'est nécessaire.
- Après victoire, Don reste disponible ; après défaite, les règles normales de retour au Centre Yo-kai s'appliquent. Les flags de Ligue ne sont ni effacés ni réécrits par les scripts de la maison.

## Flags

| Référence | Adresse | Utilisation |
|---|---:|---|
| `FLAG_SYS_GAME_CLEAR` |0x82C |Lecture : Panthéon/postgame validé |
| Victoire Dresseur `TRAINER_DON_SPIRATON_PROTOTYPE`744 |0x7E8 |Lecture : victoire enregistrée par le retour natif du combat final |
| Victoire Dresseur `TRAINER_DON_MORLEONE_LEAGUE`743 |0x7E7 |Ne débloque **pas** la maison ; reste le flag natif du combat classique réutilisé |
| `FLAG_TEMP_6` |0x006 |Masque le modèle du résident original |
| `FLAG_TEMP_7` |0x007 |Masque le modèle de Don |

Condition exacte : `GAME_CLEAR && trainer_defeated(744)`.

Les flags temporaires sont recalculés à chaque entrée. Aucun nouveau flag permanent, aucune variable de navigation et aucun changement du format de sauvegarde. Une ancienne sauvegarde ayant seulement vaincu Matt à la Ligue ne remplace pas le résident tant que le flag744 manque.

Le moteur pose le flag744 au retour d'une victoire contre le boss. Les restrictions capture/fuite et les huit couches du boss restent celles du prototype existant ; ce travail ne les modifie pas. La maison n'écrit jamais ce flag.

## Équipe et musique

| Espèce | Niveau |
|---|---:|
| Mademoaiselle147 |56 |
| Sorcophage70 |57 |
| Doyen Doyagari140 |56 |
| Fourchelangue136 |58 |
| Tristos115 |57 |
| Turboss86 |60 |

Les24 capacités, les objets tenus et les paramètres du Dresseur restent ceux du combat743 validé. Les tables de Dresseurs/équipes sont identiques à la base. Musique du combat : `MUS_YOKAI_GHOULFATHER`349 ; dans la compilation privée, `mus_yokai_03`, avec canal DPCM actif observé pendant les deux revanches et la défaite. La compilation publique conserve ses secours audio habituels.

Aucun appel à Don Spiraton depuis la maison : le test vérifie explicitement que l'adaptateur du boss est inactif pendant les revanches.

## Tests réels mGBA

[Rapport public](public/TEST_MGBA.json) · [Rapport privé](prive/TEST_MGBA.json) · [Préservation](PRESERVATION.json).

| Test | Public | Privé |
|---|---|---|
| Avant Ligue : résident seul et dialogue original |Réussi |Réussi |
| Après premier Don743 seulement : résident seul |Réussi |Réussi |
| Ancienne Ligue validée, sans victoire744 : résident seul |Réussi |Réussi |
| Victoire744 sans Panthéon : résident seul |Réussi |Réussi |
| Victoire744 + Panthéon : Don seul |Réussi |Réussi |
| Entrée par la porte réelle du Chemin d'O |Réussi |Réussi |
| Chemin jusqu'à Don, conversation et sortie réelle |Réussi |Réussi |
| Choix NON, sans combat ni changement de progression |Réussi |Réussi |
| Première revanche : équipe,24 capacités, objets, victoire et retour |Réussi |Réussi |
| Deuxième revanche immédiate, sans sortir ni effacer le flag743 |Réussi |Réussi |
| Flags permanents comparés avant/après les victoires |Identiques |Identiques |
| Sauvegarde Flash, rechargement natif, retour par la porte |Réussi |Réussi |
| Défaite réelle, retour au Centre de l'Île6 et soin |Réussi |Réussi |
| Don toujours présent à la visite suivant la défaite |Réussi |Réussi |
| Trois variantes de revanche de Matt : déclenchement, équipes et musique |Réussi |Réussi |

Les tests de Matt contrôlent les véritables entrées en combat et les trois équipes68/69/70/70/71/73 avec Decisive Battle ; ils ne rejouent pas trois combats complets. [Public](matt-public/LIGUE_MGBA.json) · [Privé](matt-prive/LIGUE_MGBA.json).

La sauvegarde est écrite par `TrySavingData`, puis relue par `LoadGameSave` avec vérification des flags et réentrée réelle dans la maison. Ce contrôle n'est pas présenté comme un redémarrage au menu « Continuer ».

Les portes, interactions et combats sont réellement exécutés dans mGBA/libretro. Les états de progression sont des fixtures explicites : cela ne représente pas une première conquête complète de la Ligue. Équipe QA renforcée pour les victoires, équipe très faible pour provoquer une défaite ; l'équilibrage n'est pas validé par ces fixtures.

## Captures

- [Maison avant la Ligue](public/avant-ligue.png).
- [Don après la victoire finale](public/apres-victoire-finale.png).
- [Dialogue OUI/NON](public/dialogue-oui-non.png).
- [Deuxième revanche](public/revanche-2-combat.png).
- [Rechargement de sauvegarde](public/apres-sauvegarde-rechargement.png).
- [Centre Yo-kai après défaite](public/defaite-centre-pokemon.png).

Les images et JSON portent sur les ROM dont les SHA sont dans les rapports.

## Compilation et protection

- Publique :16 777 216 octets.
- Privée :31 658 511 octets, sous32 Mio ; marge1 895 921 octets.
- EWRAM :261124/262144 ; IWRAM privée :29888/32768.
- Aucun changement du code moteur, des graphismes, des151 espèces, des équipes, des Champions, des trophées, des légendaires ou de l'audio.
- Les31 flux audio et378 gains privés sont comparés octet par octet à Argenta ; ils sont identiques.
- Toutes les autres cartes et leurs événements sont identiques à la base, notamment l'extérieur du Chemin d'O, les événements des autres îles, Argenta et la salle du Maître. Les huit arènes et la Ligue ne sont pas retouchées ici.
- Aucun accès anticipé à l'Île6, ni changement des conditions de navigation. Le voyage normal en bateau n'est pas rejoué par ces fixtures.

## Fichiers

Intégration :

- `data/maps/SixIsland_WaterPath_House2/map.json`
- `data/maps/SixIsland_WaterPath_House2/scripts.inc`
- `data/maps/SixIsland_WaterPath_House2/text.inc`

Tests et transmission :

- `tools/yokai/tester_exil_morleone_mgba.py`
- `tools/yokai/verifier_exil_morleone.py`
- `tools/yokai/tester_spiraton_ligue_mgba.py` : répertoire de rapport configurable, aucun comportement du jeu modifié.
- `docs/don-spiraton/exil/MISSION_AUTORISEE.md`
- `docs/don-spiraton/DECISIONS_VALIDEES.md`
- Ce dossier de preuves.

## Limite de progression à conserver

L'apparition est raccordée aux flags existants du boss et du Panthéon. Le véritable sprite initial, la conclusion et l'activation de la première finale normale restent des missions distinctes. Tant que cette première finale n'est pas activée, une partie normale ancienne ne peut pas obtenir le nouveau flag744 en terminant seulement la Ligue actuelle ; elle conserve donc son résident d'origine. Les tests du déblocage simulent explicitement les états attendus.

```sh
source /workspace/.setup/env.sh
make -j6
make -j6 YOKAI_AUDIO_DIR=/workspace/private-audio/argenta-integration
python3 tools/yokai/tester_exil_morleone_mgba.py
YOKAI_QA_ROM=$PWD/pokefirered_audio.gba \
 YOKAI_EXILE_REPORT_DIR=QA_RECETTE_FINALE/DON_SPIRATON/EXIL/prive \
 python3 tools/yokai/tester_exil_morleone_mgba.py
python3 tools/yokai/verifier_exil_morleone.py
```
