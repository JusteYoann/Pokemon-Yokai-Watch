# Azuria — deuxième trophée, 22 octobre 2026

## Contenu intégré

La porte existante de l'Arène d'Azuria mène à une nouvelle salle d'entraînement, dans les dimensions originales (17 × 20). La ville et ses connexions restent celles de Rouge Feu. Katie occupe le rôle de Championne pour Nathan ; Nathan celui de Champion pour Katie. Un seul apparaît, avec les sprites de carte et de combat déjà intégrés au projet et les dialogues amicaux propres à chaque variante.

L'épreuve comporte trois foyers symboliques sur pupitres : Feulion à gauche, Whisper à droite, Jibanyan au centre. Le guide et les assistants expliquent l'ordre. Une erreur éteint les foyers et permet immédiatement de recommencer. La progression et le rendu survivent à une sortie et à une sauvegarde/reprise. Le passage central et l'interaction avec le Champion exigent le premier trophée et la séquence complète. Une ancienne sauvegarde possédant déjà le deuxième trophée n'a pas à refaire la nouvelle épreuve.

Les deux variantes affrontent Feulion niveau 16, Whisper niveau 16 et Jibanyan niveau 18. Les espèces suivent l'équipe proposée dans le dossier ; niveaux, attaques et IV0 sont des choix d'implémentation provisoires. Les Champions n'utilisent pas d'objets de soin ni d'objets tenus. Les textes français suivent les intentions du scénario ; leur formulation reste disponible pour relecture créative.

La victoire remet réellement le deuxième trophée et la CT03, en conservant les indicateurs historiques permettant notamment Coupe. La CT reste récupérable si le Sac est plein, sans nouveau combat ni duplication. Le panneau extérieur n'ajoute plus une ancienne fiche d'Ondine au Fame Checker.

Le décor utilise les tuiles natives chaudes de Cramois'Île, dans une disposition nouvelle, avec des pupitres symboliques. Le tileset dérivé possède ses propres attributs pour conserver les trois sorties natives. Aucun nouvel artwork de personnage n'est présenté comme créé dans ce chapitre.

## Continuité des anciennes parties

Les anciens tableaux d'équipe d'Ondine et des caméos Nathan/Katie restent dans les sources historiques. L'équipe active est explicitement décrite dans `data/yokai/scenario_azuria.json`. Katie utilise l'ancien emplacement415 ; Nathan un emplacement factice inutilisé21. Une victoire fixe les deux indicateurs de combat et le trophée, évitant une répétition indue.

Les deux anciens acteurs de Céladopole sont masqués. Leurs équipes de revanche postgame à six membres sont déplacées dans l'arène, avec choix Oui/Non et possibilité de rejouer. La Pierre Plante historique reste unique, avec ses anciens indicateurs. Un cadeau déjà gagné mais non reçu dans une ancienne partie reste récupérable ; les nouvelles parties gagnent cette Pierre après la revanche postgame. Les anciens combats de caméo avant le postgame ne sont plus proposés à Céladopole.

La première reprise d'une sauvegarde antérieure dans l'arène recharge la disposition et les objets actuels, puis place le joueur à l'entrée. Les reprises suivantes conservent sa position. Une reprise antérieure à Céladopole recharge les objets pour masquer les doublons, en conservant la position du joueur. Aucun changement du format de sauvegarde.

## Recette

- `TEST_CHAPITRE_MGBA.json` : entrée et sortie par la porte réelle ; Champion opposé exclusif ; refus avant premier trophée/foyers ; erreur de séquence ; sauvegarde Flash, callback Continuer et sortie/reprise ; combat natif, trophée, CT, Sac plein et non-duplication, pour Nathan et Katie.
- `TEST_MIGRATION_MGBA.json` : défaite réelle sans récompense, refus aux étapes intermédiaires, remise à zéro des lumières, anciennes sauvegardes construites explicitement puis sauvegardées/reprises nativement, disparition des doublons à Céladopole et revanche postgame dans les deux variantes.
- `TEST_EQUIPES_ACTIVES_MGBA.json` : construction native des 640 équipes actives, espèces, niveaux, attaques, talents, objets et inventaire des Dresseurs. Ce contrôle ne joue pas 640 combats.
- `CONTROLE_SOURCES.json` : graphe indépendant des collisions, accès aux pupitres et sorties, fermeture du passage, retour depuis le Champion, attributs des trois sorties et conservation des tableaux historiques.
- `LARGEURS_DIALOGUES.json` : 92 lignes mesurées avec la police native et un nom de joueur de sept W.
- `REGRESSION_CONTINUE_ARGENTA_MGBA.json` : migration/reprise d'Argenta rejouée après l'extension du traitement de Continuer.

Les combats du deuxième trophée utilisent Kappacap niveau 20, Whisper niveau 18 et Nihilistik niveau 18, IV15 et statistiques ordinaires, avec réorganisation d'attaques déjà apprises. Le pilote choisit un partenaire vivant après une mise K.O. par les boutons de l'interface ; il n'écrit pas les résultats des combats. Pour les seules revanches postgame, Hovernyan niveau 100 dispose explicitement de PV/statistiques de 999 et d'Aéropique : vérification des événements et récompenses, aucune validation d'équilibrage postgame. Les diagnostics conservés montrent une erreur initiale du pilote bloqué sur un partenaire K.O.

Reproduire depuis la racine :

```sh
source /workspace/.setup/env.sh
make -j4
python3 tools/yokai/verifier_azuria_sources.py
python3 tools/yokai/tester_textes_azuria_mgba.py
python3 tools/yokai/tester_azuria_scenario_mgba.py
python3 tools/yokai/tester_azuria_migration_mgba.py
python3 tools/yokai/tester_equipes_mgba.py
python3 tools/yokai/tester_argenta_continue_mgba.py
```

Les deux derniers outils historiques écrivent dans leurs anciens dossiers ; leurs nouveaux résultats ont été copiés ici pour préserver les preuves antérieures. Après une régénération intentionnelle des anciennes équipes globales, réappliquer `appliquer_equipe_argenta.py`, puis `appliquer_equipe_azuria.py` avant compilation. Les spécifications historiques verrouillées restent inchangées.

## Limites et suite

La recette utilise des fixtures déclarées ; elle ne constitue pas une partie continue depuis Bourg Palette, ni une sauvegarde archivée d'un joueur, ni un équilibrage exhaustif des trois starters. Aucun fichier de partie historique n'a été fourni. Le parcours complet et l'équilibrage global restent à vérifier. Le vérificateur général historique des sprites conserve son incompatibilité connue avec certaines nouvelles présentations ; aucun succès global n'est revendiqué.

Prochain ensemble scénaristique : Bérénice Bélier à Carmin-sur-Mer, Portes Mystères et troisième trophée. La suite du scénario, le nouveau Temple et le postgame complet restent à intégrer. ROM locale de recette uniquement ; aucun binaire ROM publié.
