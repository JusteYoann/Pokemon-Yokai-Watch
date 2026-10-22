# Reprise du scénario — 22 octobre 2026

Base distante vérifiée : `dev/reconstruction-finalisation`, `ef68432c21a5f7b7e67ff0e21e4bdcb5019ee7e6`.
Branche de reprise : `codex/reprise-scenario-2026-10-22`.

## Premier ensemble intégré

- Introduction : coexistence publique humains/Yo-kai ; annonce du Médallium ancien, de la montre récente, des huit trophées et du Temple. Chen ne prétend plus avoir inventé une montre pour rendre visibles des êtres cachés.
- Laboratoire : remise narrative de la montre portée au poignet, fanfare et tutoriel avant le choix du partenaire. Pas de nouvel objet de sac ni de nouveau pouvoir technique inventé. Le Médallium ancien utilise le menu et le déblocage natifs après le colis ; les starters et leur correspondance restent inchangés.
- Matt : course amicale aux trophées, invitation à prendre la Carte chez lui. Suppression de la menace de priver le héros de carte et de la filiation avec Chen dans l'introduction.
- Entrée future du Temple : contrôle des huit flags natifs de badges sur le passage et dans le dialogue du garde. Le passage est refusé si un seul manque. Aucun changement de format de sauvegarde.

## Validation réelle

Compilation publique réussie, ROM locale ignorée de 16 Mio, sans les musiques privées absentes de cette machine. Les SHA de chaque exécution figurent dans les JSON. La compilation privée, le budget avec les 26 OST et les performances matérielles ne sont pas revérifiés.

- `TEST_ACCES_TEMPLE_MGBA.json` : 256 combinaisons par exécution du script natif ; huit franchissements refusés avec un trophée différent manquant ; franchissement réel vers la première salle avec les huit ; sauvegarde/relecture Flash. Première tentative de banc incorrecte : initialisation directe CB2_NewGame sans mixeur valide, transition bloquée. Corrigée en passant par `mgba_new_game.new_game`, sans modification du moteur audio.
- `TEST_PROLOGUE_MGBA.json` : Nathan et Katie ; introduction réelle, puis position et progression préparées explicitement ; scène automatique de remise de la montre, interaction A avec Chen pour le colis/Médallium, déblocage du menu, cinq Balls, consommation du colis et persistance Flash. Largeur native des 37 lignes réécrites du laboratoire avec prénom de sept W. Le combat initial et le parcours jusqu'à Jadielle ne sont pas couverts par ce test.
- `TEST_INTRODUCTION_MGBA.json` : choix des deux sexes, saisie de prénom et arrivée sur la carte initiale aux boutons ; Matt fixe.
- `LARGEURS_INTRODUCTION_CHEN.json` : 33 lignes, police native, prénom maximal.
- Captures mGBA des remises et de l'accès examinées. Aucun nouveau sprite n'est revendiqué.

`tools/yokai/verifier_rom.py` échoue sur `(1, front, linked file mismatch)` : il compare encore aux anciens bitmaps, alors que la base active utilise le rendu étendu (`yokai_graphics_rules.mk`, `src/data/graphics/pokemon.h` lie `graphics/yokai/001/front-display.4bpp.lz` avec transformation). Ce contrôle global historique n'est pas déclaré réussi ; aucun sprite n'a été altéré pour le satisfaire. Les tests du présent lot ne remplacent pas les contrôles du rendu étendu.

Rejouer depuis la racine, après `source /workspace/.setup/env.sh` et `make -j4` :

```sh
python3 tools/yokai/tester_acces_temple_mgba.py
python3 tools/yokai/tester_prologue_scenario_mgba.py
python3 tools/yokai/tester_introduction_mgba.py
python3 tools/yokai/tester_textes_introduction_mgba.py
```

Les deux derniers outils historiques écrivent dans RECONSTRUCTION ; leurs résultats actuels ont été copiés ici pour préserver les preuves historiques. Les tests sont des fixtures déclarées, pas une aventure intégrale.

## Références et arbitrages

Les documents du dossier maître sont dans `docs/SCENARIO_ORIGINAL_2026/`. Les images restent dans les ZIP extraits hors dépôt ; aucun artwork de tiers n'est ajouté à Git. Le second ZIP apporte le classement descriptif des 41 images supplémentaires, sans changement des documents du scénario. Son index est conservé ; les désignations descriptives ne sont pas des identités officielles validées. Les logos restent hors chantier.

Le créateur a explicitement validé pendant cette reprise : Céladopole sans trophée ; Alyzon donne le sixième au sommet de la Tour ; la cloche termine Zombie Night. Décisions ajoutées à `00_DECISIONS_VALIDEES.md`. Les autres questions restent ouvertes.

## Ce qui reste réellement à développer

Le scénario complet n'est pas intégré. La première salle accessible reste celle d'Olga ; le contrôle d'entrée ne constitue pas le nouveau Temple. Les anciennes arènes donnent encore leurs badges historiques, y compris Céladopole : migrer sa récompense avec celle d'Alyzon, sans supprimer l'unique source d'un trophée avant son remplacement.

Ensembles suivants :
1. Argenta : discours de Morleone, Mafiamille, Enma incognito ; premier Champion Wyatt et épreuve. Sprite humain d'Enma à produire selon la référence exacte, sans substituer sa forme royale.
2. Champions 2 à 5 et leurs véritables épreuves, variantes de protagoniste ; migration des caméos en évitant les doublons ; Agent X récurrent.
3. Lavanville : habitants temporairement absents, zombies au contact, ambiance, cloche et Alyzon ; aucune explication inventée reliant le phénomène aux antagonistes.
4. Cramois'Île passée : géographie conservée, variantes Nathaniel/Michael, restrictions de toutes les sorties, trophée 7 et retours sans softlock.
5. Morleone Champion 8 ; Temple explorable original et quatre adversaires prescrits ; Soranaki à deux phases sans soin intermédiaire, soin préalable de Matt, révélation Enma, Bingo-kai sans souhait consommé et Panthéon.
6. Limbes, Paradis Divin, boss optionnels, Île 7, rematches et distributions exclusives ; conserver les 151 espèces et leurs identifiants.
7. Parcours intégral pour les deux protagonistes, équilibrage, sauvegardes et tests de non-blocage.

Les autres motivations/scènes encore ouvertes dans `12_CONFLITS_ET_QUESTIONS.md` doivent être arbitrées avant leur écriture définitive. Aucune promesse de livraison automatique au 28 octobre ni aucun test intégral n'est revendiqué.

## Environnement

Outils de compilation et mGBA installés par les scripts existants ; versions, signatures APT et SHA épinglés conservés. `install_script` et `start_skill` sauvegardés dans le brouillon de configuration cloud. Cette sauvegarde n'est pas une publication. Aucun service permanent nécessaire, aucun secret demandé.
