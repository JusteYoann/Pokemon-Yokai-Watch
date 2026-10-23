# Champions de Kanto — intégration et validation

**Les Champions approuvés sont intégrés sur `feature/champions-yokai-watch`. Les deux ROM compilent et tous les contrôles joints passent. Aucun merge sur `master`.**

Base : `d32774305` (Lavanville validée). Implémentation : `21eb877ab2bbddbe5b0520882c9456d679942e4c`. [Accord du créateur](../VALIDATION_UTILISATEUR.md) · [Fichiers modifiés](FICHIERS_MODIFIES.txt) · [Synthèse machine](VALIDATION.json).

## Voir le résultat

- **Bérénice** : [sur la carte](public/berenice-overworld-x3.png), [portrait de combat](public/berenice-portrait-x3.png), [quatre orientations enregistrées](public/berenice-quatre-orientations.gif).
- **Colosse d’Alyzon** : [sprite et barre de PV au niveau31](public/alyzon-colosse-x3.png), [réplique enregistrée dans le moteur](public/alyzon-replique-colosse.gif), [fin de la réplique](public/alyzon-replique-fin-x3.png).
- **Dialogues des variantes** : [Katie](public/katie-introduction-complete-x3.png), [Nathan](public/nathan-introduction-complete-x3.png), [Nathaniel](public/nathaniel-introduction-complete-x3.png), [Michael](public/michael-introduction-complete-x3.png).

Ce sont des captures natives mGBA, agrandies par pixels entiers pour la lecture. Les équipes du joueur dans les preuves de combat sont des équipes QA renforcées ; ce ne sont pas des captures d’équilibrage normal.

| Champion | Version publique | Version privée |
|---|---|---|
| Wyatt | [Carte](public/wyatt-overworld-x3.png) · [Portrait](public/wyatt-portrait-x3.png) · [Victoire](public/wyatt-victoire-x3.png) · [Continuer](public/wyatt-continuer-x3.png) | [Portrait](prive/wyatt-portrait-x3.png) · [Continuer](prive/wyatt-continuer-x3.png) |
| Katie — garçon | [Carte](public/katie-overworld-x3.png) · [Portrait](public/katie-portrait-x3.png) · [Victoire](public/katie-victoire-x3.png) · [Continuer](public/katie-continuer-x3.png) | [Portrait](prive/katie-portrait-x3.png) · [Continuer](prive/katie-continuer-x3.png) |
| Nathan — fille | [Carte](public/nathan-overworld-x3.png) · [Portrait](public/nathan-portrait-x3.png) · [Victoire](public/nathan-victoire-x3.png) · [Continuer](public/nathan-continuer-x3.png) | [Portrait](prive/nathan-portrait-x3.png) · [Continuer](prive/nathan-continuer-x3.png) |
| Ariane | [Carte](public/ariane-overworld-x3.png) · [Portrait](public/ariane-portrait-x3.png) · [Victoire](public/ariane-victoire-x3.png) · [Continuer](public/ariane-continuer-x3.png) | [Portrait](prive/ariane-portrait-x3.png) · [Continuer](prive/ariane-continuer-x3.png) |
| Alyzon | [Carte](public/alyzon-overworld-x3.png) · [Portrait](public/alyzon-portrait-x3.png) · [Victoire](public/alyzon-victoire-x3.png) · [Continuer](public/alyzon-continuer-x3.png) | [Portrait](prive/alyzon-portrait-x3.png) · [Continuer](prive/alyzon-continuer-x3.png) |
| Bérénice | [Carte](public/berenice-overworld-x3.png) · [Portrait](public/berenice-portrait-x3.png) · [Victoire](public/berenice-victoire-x3.png) · [Continuer](public/berenice-continuer-x3.png) | [Portrait](prive/berenice-portrait-x3.png) · [Continuer](prive/berenice-continuer-x3.png) |
| Nathaniel — garçon | [Carte](public/nathaniel-overworld-x3.png) · [Portrait](public/nathaniel-portrait-x3.png) · [Victoire](public/nathaniel-victoire-x3.png) · [Continuer](public/nathaniel-continuer-x3.png) | [Portrait](prive/nathaniel-portrait-x3.png) · [Continuer](prive/nathaniel-continuer-x3.png) |
| Michael — fille | [Carte](public/michael-overworld-x3.png) · [Portrait](public/michael-portrait-x3.png) · [Victoire](public/michael-victoire-x3.png) · [Continuer](public/michael-continuer-x3.png) | [Portrait](prive/michael-portrait-x3.png) · [Continuer](prive/michael-continuer-x3.png) |
| Koga, préservé | [Carte](public/koga-overworld-x3.png) · [Portrait](public/koga-portrait-x3.png) · [Victoire](public/koga-victoire-x3.png) · [Continuer](public/koga-continuer-x3.png) | [Portrait](prive/koga-portrait-x3.png) · [Continuer](prive/koga-continuer-x3.png) |
| Don Morléone, préservé | [Carte](public/don-overworld-x3.png) · [Portrait](public/don-portrait-x3.png) · [Victoire](public/don-victoire-x3.png) · [Continuer](public/don-continuer-x3.png) | [Portrait](prive/don-portrait-x3.png) · [Continuer](prive/don-continuer-x3.png) |

Les dossiers `public/` et `prive/` contiennent aussi chaque adversaire au moment du combat et les captures individuelles des orientations de Bérénice.

## Comportement livré

| Badge conservé | Champion | Équipe, niveaux et ordre |
|---|---|---|
| Roche1 | Wyatt | **Équipe exacte de Pierre** : Felipaix8, Bouh10, Passpa12 |
| Cascade2 | Katie pour un garçon ; Nathan pour une fille | Noko14, Crocho16, **Jibanyan21** |
| Foudre3 | Ariane Célestin | Antonnerre18, Padrézo19, Parantonn21, **Usapion23** |
| Prisme4 | Alyzon Bie | Potofeu27, Whisper28, Triptic-tac29, **Zombie Colosse31** |
| Âme5 | Koga | Inchangé |
| Marais6 | Bérénice Bélier | **Équipe exacte de Morgane** : Baku36, Ed Mémoire37, Fourchelangue38, Mognyan39, Savantard42 |
| Volcan7 | Nathaniel pour un garçon ; Michael pour une fille | Métaurolog40, Sirénité41, Sal de bain41, Brumella42, Faux Kappa43, **Hovernyan45** |
| Terre8 | Don Morléone | Inchangé |

Les appellations du registre restent « Métaureaulog » nº34, « Sirènité » nº67 et « Usapyon » nº100. Aucun renommage global des151 Yo-kai. Types réels préservés, notamment Jibanyan Feu, Usapion Acier et Hovernyan Vol. Les attaques et talents validés de la proposition sont intégrés, avec vérification des apprentissages par niveau réalisée à l’étape1.

Les paramètres, objets et attaques de Wyatt et Bérénice sont conservés intégralement. Le générateur natif utilise le nom du Dresseur dans le calcul de personnalité : les graines historiques PIERRE et MORGANE sont explicitement préservées. La comparaison dans mGBA confirme aussi l’identité de leurs personnalités, natures, statistiques, PP, talents et objets. Les variantes Katie/Nathan et Nathaniel/Michael produisent des équipes **strictement identiques entre les deux sexes**.

Jibanyan, Usapion, le Colosse et Hovernyan sont observés en dernier. L’IA et le choix de remplacement forcé réutilisent un ordre ciblé sur ces quatre combats. Aucun changement de cette politique pour Wyatt, Bérénice, Koga ou Don.

Les CT39,03,34,19,06,04,38 et26 restent attribuées par leurs Arènes respectives. La spécialité des Champions ne remplace pas automatiquement leur CT. Les drapeaux de défaite, de CT et les huit badges conservent leurs ID historiques. Une victoire sauvegardée n’est pas rejouable par une nouvelle interaction.

## Variantes, dialogues et graphismes

Le sexe du joueur est lu depuis sa sauvegarde pour résoudre le nom, le portrait, la classe affichée et les dialogues des deux Arènes à variantes. Les textes utilisent des marqueurs dédiés pour les noms d’Azuria et de Cramois’Île ; ils ne consomment pas les variables de texte utilisées par les objets et récompenses.

Sur la carte, le moteur résout les anciens ID graphiques des cinq Champions uniquement dans leur Arène. Les cartes, `localId`, coordonnées, objets sérialisés et identifiants de victoire restent compatibles avec les sauvegardes. Le même mécanisme est exécuté lors de la reconstruction des sprites après « Continuer » et après un combat. Les captures et les comparaisons VRAM/palettes vérifient ces retours.

Bérénice utilise exactement le lot retrouvé dans le commit `2647bc1627050f193cc9606f8c0f5f1151986047`, sans reprendre ses anciens événements. Sa conversion est découpée en cellules16×32 ; les neuf poses sont conservées. Les quatre orientations visibles sont contrôlées par les animations natives et comparées aux pixels PNG effectivement chargés en VRAM. Le miroir natif du profil droit est vérifié. Le portrait64×64 est enregistré sous l’ID162 ; l’overworld sous l’ID175, avec une palette dédiée0x112D en banque7.

Wyatt, Ariane, Nathaniel et Michael gardent leurs trois orientations déjà intégrées, avec miroir natif du profil. Aucune marche supplémentaire n’est inventée pour ces Champions immobiles. Les sprites de Nathan et Katie, dont le dos de combat de Nathan, ne sont pas redessinés.

Les introductions des quatre variantes sont contrôlées par l’adresse du dialogue effectivement sélectionné dans le moteur et par une capture de sa première page complète. Le Fame Checker, les statues, panneaux et références aux anciens Champions sont adaptés. Les écrans courts utilisent ARIANE et BÉRÉNICE ; les dialogues et fiches utilisent leurs noms complets.

Les apparitions secondaires restent en place : Ariane et Usapion Route25, Katie/Nathan à Céladopole, Nathaniel/Michael à Parmanie, Wyatt à Cramois’Île. Leurs ID de Dresseur, victoires, objets et musiques ne sont pas confondus avec ceux des Champions.

## Colosse : représentation isolée

`src/yokai_champions.c` décrit uniquement le quatrième monstre du combat de Dresseur `TRAINER_LEADER_ERIKA`. Le gabarit temporaire interne est personnalisé après la génération de la partie adverse : **niveau31, Spectre/Lévitation, PV140, Atq80, Déf80, Vit25, AtqSp36, DéfSp54**, sans objet tenu. Attaques : Écras’Face, Jet-Pierres, Groz’Yeux, Étonnement.

Le rendement d’EXP de cette instance vaut **156**, comme l’ancien Mémogre, dans le calcul natif d’EXP. Ce n’est pas une nouvelle espèce et aucun Potofeu global n’est remplacé : le premier emplacement d’Alyzon reste son vrai Potofeu. Le surnom affiché est `Z. COLOSSE` pour respecter la barre de PV.

Le prédicat utilise le type de combat Dresseur, l’identifiant d’Alyzon, le côté adverse et l’index3 de la partie. Graphisme, palette, cadrage et EXP sont ciblés par cette identité. La présentation spéciale respecte le leurre de Clonage et s’efface quand un monstre transformé utilise un autre graphisme. Le sprite et la palette du Colosse proviennent des ressources de combat validées, sans retouche.

**Le drapeau `BATTLE_TYPE_LAVENDER_ZOMBIE` n’est pas activé.** Les trois premiers adversaires restent des Yo-kai normaux. La capture et la fuite sont refusées par les règles natives d’un combat de Championne ; les tentatives réelles de fuite et de Master Ball ont été exécutées dans les deux ROM. Comme dans le comportement natif de Rouge Feu, une Ball bloquée par un Dresseur peut être consommée.

La réplique « Et maintenant, je vais te présenter mon petit préféré ! Hihi ! » est insérée après l’animation d’envoi, avant les effets d’entrée et la reprise du tour. Elle passe par le moteur de texte de combat, sur deux pages. Un booléen temporaire, remis à zéro à chaque combat, empêche sa répétition. Aucune nouvelle scène overworld, aucun nouveau portrait d’intervention, aucune nouvelle musique et aucun champ de sauvegarde.

Les quatre combats errants restent distincts et identiques : niveau24, statistiques, attaques, variantes, immunité, capture/fuite et retour au terrain. Le Colosse errant conserve notamment ses valeurs110/62/62/19/28/42.

## Résultats des tests

Tous les rapports ci-dessous portent les SHA256 des ROM finales, contrôlés lors de l’assemblage de ce dossier.

| Famille | Publique | Privée | Ce qui est vérifié |
|---|---|---|---|
| Champions | [11 contrôles](public/TEST_CHAMPIONS_MGBA.json) | [11 contrôles](prive/TEST_CHAMPIONS_MGBA.json) | Dix combats gagnés par commandes, portraits, noms, espèces/niveaux, signatures, CT, badges, sauvegarde Flash, Continuer, interaction déjà terminée ; puis vérification des huit badges gagnés |
| Variantes de dialogue | [4 cas](public/VARIANTES_DIALOGUES_MGBA.json) | [4 cas](prive/VARIANTES_DIALOGUES_MGBA.json) | Katie/Nathan et Nathaniel/Michael selon le sexe réel de la nouvelle partie |
| Effets et Colosse | [12 contrôles](public/EFFETS_MGBA.json) | [12 contrôles](prive/EFFETS_MGBA.json) | Orientations de Bérénice, bonus natifs des badges, seuils d’obéissance, fuite et capture bloquées, portée du marqueur Colosse |
| Textes | [840 lignes](public/DIALOGUES_MGBA.json) | [840 lignes](prive/DIALOGUES_MGBA.json) | Police native, plafond208pixels, deux sexes, noms développés et réplique du Colosse ; aucune ligne déborde |
| Lavanville | [28 scénarios](regressions/lavanville/public/TEST_MGBA.json) | [28 scénarios](regressions/lavanville/prive/TEST_MGBA.json) | Intro, nuit/brume, zombies, Tour, capture normale dans la Tour, soins, Alyzon, badge4, résidence, garde des escaliers, Flûte, Misterre, repaire verrouillé/déverrouillé, ancienne sauvegarde |
| Finale | [Passée](regressions/finale/public/FINALE_NORMALE_MGBA.json) | [Passée](regressions/finale/prive/FINALE_NORMALE_MGBA.json) | Victoire réelle contre le quatrième membre du Conseil, entrée normale, Don Morléone, soin de Matt, fusion masquée, huit formes de Don Spiraton, Chen, Panthéon, crédits, sauvegarde et Continuer |
| Équipes générées | [Données natives](public/EQUIPES_MGBA.json) | [Données natives](prive/EQUIPES_MGBA.json) | Comparaison avec [la ROM Lavanville de référence](EQUIPES_REFERENCE_MGBA.json), conservation des équipes et identité entre variantes |

Les bonus de statistiques sont exécutés dans les fonctions natives avec une situation contrôlée : attaque physique17→18, dégâts reçus physiques17→16, attaque spéciale19→21, dégâts spéciaux reçus19→18. Le bonus de Vitesse du Badge Foudre inverse l’ordre entre100 et105 de Vitesse. Les seuils d’obéissance10/30/50/70/100 sont testés avec un Yo-kai d’un autre Dresseur, et avec des tirages au-dessus des seuils. Ce sont des tests de mécanique séparés des vraies victoires de Champions ; leurs drapeaux/statistiques de fixture sont explicitement documentés.

La correspondance des CS et le code de contrôle de leurs badges sont inchangés, comme les SaveBlock et les constantes de drapeaux. Le dossier ne prétend pas à une traversée manuelle de Kanto avec chaque CS ni à une aventure normale complète.

## Préservation

[PRESERVATION.json](PRESERVATION.json) confirme :

- Données globales des151 Yo-kai, types, statistiques, évolutions, noms, attaques et rencontres conservés.
- **5817 fichiers graphiques préexistants PNG/pal** conservés ; PNG identiques en octets, palettes comparées en normalisant seulement LF/CRLF.
- Ressources de Bérénice identiques à celles retenues dans l’audit.
- Tous les Dresseurs non concernés, leurs parties et talents forcés conservés. Équipes de Wyatt, Bérénice, Koga et Don Morléone identiques aussi après génération réelle dans mGBA.
- Cartes et événements protégés de Lavanville, Koga, Don, Flûte, repaire et finale inchangés.
- **31 flux WaveData privés identiques** au pack Lavanville validé, contrôlés dans la ROM compilée. Aucun fichier audio protégé n’est publié ici.
- Code des quatre zombies errants et données de leurs combats inchangés. Aucune extension de sauvegarde ni réattribution d’un drapeau.

## ROM et mémoire

| Mesure | Publique | Privée |
|---|---:|---:|
| Taille ROM | 16777216 octets | 31674139 octets |
| Marge sous32Mio | 16777216 octets | 1880293 octets |
| EWRAM | 261132 /262144 | 261132 /262144 |
| Marge EWRAM brute | 1012 octets | 1012 octets |
| IWRAM | 29824 /32768 | 29888 /32768 |
| Marge IWRAM brute | 2944 octets | 2880 octets |

SHA256 publique : `d2c04bdadd4ba53eca7c8e2f42be8908dcdc3a93805561bf3373dd72bc87cd6f`.

SHA256 privée : `7e6ac59ad79a6930bf772b8bc7debb5189d93e29f80d36d0504e52840887871f`.

L’état temporaire supplémentaire occupe quatre octets alignés en EWRAM. Les marges ci-dessus sont celles de l’édition de liens, pas une réserve garantie pour n’importe quelle allocation future. Le Colosse réutilise le tampon adverse64×64/2048octets et ses banques de palette ; Bérénice utilise un sprite overworld16×32/256octets et un portrait64×64. Aucun second monstre ni portrait supplémentaire n’est alloué pour la réplique. Les comparaisons VRAM et les captures vérifient les ressources réellement affichées.

## Reproduction

```sh
make -j6
make -j6 YOKAI_AUDIO_DIR=/chemin/vers/le/pack-prive-lavanville
python tools/yokai/tester_champions_mgba.py
python tools/yokai/tester_champions_effets_mgba.py
python tools/yokai/capturer_variantes_champions_mgba.py
python tools/yokai/verifier_dialogues_champions_mgba.py
python tools/yokai/tester_champions_lavanville_mgba.py
```

Répéter les vérifications privées avec `YOKAI_QA_ROM=$PWD/pokefirered_audio.gba`. Le pack privé n’est pas inclus ; le préparateur Lavanville existant permet de le reconstituer depuis les ressources privées déjà autorisées. Les builds public et privé doivent être effectués successivement car ils partagent des ressources graphiques générées.

Les tests de finale utilisent `tester_spiraton_finale_normale_mgba.py` avec `YOKAI_FINALE_REPORT_DIR=docs/champions-yokai-watch/validation/regressions/finale/public` ou `prive`. Les scripts de capture d’équipes et de préservation fournissent les comparaisons détaillées ; leurs paramètres figurent dans leurs sources.

**Limites assumées :** les combats fonctionnels utilisent une équipe QA renforcée. Les niveaux et compositions approuvés sont respectés, mais l’équilibrage d’une partie normale et une aventure complète restent à valider humainement. La limitation de boucle musicale Zombie Night déjà documentée dans Lavanville est inchangée : répétition du morceau complet avec son fondu. Aucun contrôle exhaustif de toutes les capacités, animations et tous les menus du jeu n’est revendiqué.
