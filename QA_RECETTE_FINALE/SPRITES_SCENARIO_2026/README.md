# Sprites du scénario — 22 octobre 2026

[Galerie personnages](GALERIE_PERSONNAGES.png) · [Comparaison Red / Enma / Domniscian](COMPARAISON_RED_ANCIENS.png) · [Inventaire](INVENTAIRE.csv)

## Ressources créées

- 13 ensembles de personnages : Bérénice, Giraud, Alyzon, Enma humain, Laure, Marge, Lady Perpetua, McKraken, Agent X, Zazel, Enma l'Ancien, Nathaniel âgé, zombie.
- Deux formes de Soranaki : carte, aperçu combat 64×64 et maîtres indexés 128×128 liés dans la ROM. Leur comportement de boss, les métamorphoses et l'enchaînement des phases demandent encore l'implémentation du scénario/moteur.
- Chaque nouvel ensemble de personnage/boss possède neuf poses sur une planche 144×32 : sud/nord/ouest immobiles, deux pas par direction. L'est utilise le miroir natif. Le spectre Soranaki flotte ; ses poses verticales de déplacement conservent volontairement sa silhouette de spectre.
- Bingo-kai : quatre images 32×32 et animation de manivelle/distribution ; capsule fermée/ouverte : deux images 16×16 ; Triptic-tac : trois orientations et une pose lumineuse 32×32, animation de flash. Ces objets/créatures conservent leur silhouette de référence.
- Enma royal et Domniscian : nouvelles planches de neuf images ; proportions tête/corps explicitement ramenées au gabarit Red, sans modification des portraits de combat ni des palettes historiques. Domniscian conserve son bureau, son ordinateur, sa tasse et ses crânes flottants dans son objet 32×32.

Total produit : **163 images de carte** réparties sur 20 planches (135 nouvelles images de personnages/boss, dix images d'objets/créature, dix-huit images pour les deux adaptations anciennes), **15 portraits 64×64** nouveaux et **deux maîtres 128×128**. Les autres graphismes approuvés du dépôt sont conservés ; voir l'inventaire. Aucune nouvelle espèce, aucun logo, aucun changement de sprite des 151 Yo-kai.

Les dessins ont été créés à partir des références des ZIP. Les originaux de génération et les paramètres de conversion sont conservés dans `graphics/yokai_characters/scenario_2026/`. Les artworks de référence privés ne sont pas ajoutés au dépôt. Les versions précédentes d'Enma/Domniscian sont conservées dans `scenario_2026/legacy/` ; les anciens fichiers `approved_overrides` restent présents. La sélection de reconversion a été mise à jour pour conserver la nouvelle demande de proportions lors d'une reprise.

## Gabarit et format

Les personnages de carte utilisent les bornes de chaque image du Red original : cadre 16×32, silhouette d'environ 19 pixels, ancrage des pieds identique, gros plan de tête et corps court. La réduction peut retirer un pixel de contour ; les tests vérifient la présence et l'enveloppe native, sans prétendre mesurer automatiquement une validation artistique.

Pour Enma royal/Domniscian, la conversion conserve des repères explicites : tête avec chevelure/couronne sur dix pixels et corps sur neuf, neuf pixels de tête dans les deux pas horizontaux comme le Red source. Le bureau de Domniscian déborde latéralement ; son personnage reste à hauteur de Red. La division des deux bandes est documentée dans `ANCIENS_RED.json`.

PNG indexés 4bpp, quinze couleurs opaques RGB555 et index zéro transparent. Portraits : palette dédiée par personnage. Nouveaux objets de carte : palette commune permettant leur affichage simultané entre eux. Les banques spéciales historiques d'Enma/Morleone/Domniscian sont distinctes : lors du raccordement des scènes mêlant anciens et nouveaux groupes, il faudra affecter une palette commune adaptée à chaque groupe ; l'actuel moteur réserve une seule banque NPC spéciale. Cette contrainte existante n'est pas résolue par une simple création de PNG.

## Vérifications effectuées

- Compilation publique réussie ; aucune musique privée nécessaire et aucune ROM publiée.
- `TEST_MGBA.json` : **17 ensembles** affichés dans le moteur natif, quatre directions, miroir est, cycles d'animation dans les quatre directions, chargement du portrait, palette OBJ et gabarit PNG contrôlés. Les quinze nouveaux ensembles et les deux adaptations anciennes sont couverts.
- `TEST_OBJETS_MGBA.json` : trois objets/créature affichés et animations jouées par le moteur ; les deux maîtres boss 128×128 sont liés, décompressés et comparés aux ressources binaires.
- Captures complètes et GIF natifs conservés pour chaque ensemble. Les premières captures avaient un portrait qui chevauchait partiellement le personnage de carte : leurs positions de fixture ont été corrigées avant de remplacer les preuves.
- Un premier test d'animation restait sur l'image immobile : le callback de mouvement stationnaire et le drapeau de pause du banc réinitialisaient l'animation. Le banc désactive ces deux éléments pour observer les cycles natifs ; aucun assouplissement des assertions d'animation n'a été fait.
- Les contrôles de gabarit ont détecté des fragments de cellules voisines et un ancrage horizontal différent dans le Red original : découpe principale et repères corrigés, puis compilation et tests rejoués.

Ce sont des essais de rendu et d'animation avec objets temporaires sur Bourg Palette et portraits dans un visualiseur natif. Ils ne valident pas les placements narratifs, les combats scénarisés, les quêtes, les métamorphoses de Soranaki ni une aventure intégrale. Les dessins restent soumis à la revue artistique du créateur ; ils ne sont pas présentés comme déjà approuvés par lui.

## Reproduction

Depuis la racine du dépôt :

```sh
source /workspace/.setup/env.sh
python3 tools/yokai/convertir_sprites_scenario.py
python3 tools/yokai/convertir_objets_scenario.py
python3 tools/yokai/enregistrer_sprites_scenario.py
python3 tools/yokai/convertir_anciens_scenario_red.py
make -j4
python3 tools/yokai/tester_sprites_scenario_mgba.py
python3 tools/yokai/tester_objets_scenario_mgba.py
python3 tools/yokai/galerie_sprites_scenario.py
```

Les scripts de conversion ne régénèrent pas les dessins : ils réemploient les PNG source suivis et enregistrent les découpes. Les identifiants historiques sont préservés ; les nouveaux identifiants `OBJ_EVENT_GFX_SCENARIO_*` et `TRAINER_PIC_SCENARIO_*` sont déclarés dans les constantes du moteur. Aucun dresseur ou combat n'est ajouté implicitement par la déclaration d'un portrait.

## Correction de liaison lors du chapitre de Carmin

Les exports GBA des 18 nouveaux objets et les entrées d’animation des 15 portraits ont été corrigés. Les anciennes vérifications de présence de symboles et de palette ne suffisaient pas à garantir leur rendu. Voir `../CARMIN_SCENARIO_2026/TEST_SPRITES_LIES_MGBA.json` : frames PNG comparées aux données liées et à la VRAM native, avec captures dans `SPRITES_SCENARIO_NATIFS.png`. Bérénice est également testée en combat réel ; Enma humain est revérifié dans Argenta.
