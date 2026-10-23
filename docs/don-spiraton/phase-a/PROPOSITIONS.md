# Don Spiraton — étape A, propositions à valider

Branche : `feature/boss-final-don-spiraton`. Base contrôlée localement et sur GitHub : `b3396ac9ff2ad83083bd62a3dbb3a0499879c286`. Dépôt propre au début de l'étape. Aucune fusion ; aucune activation de la finale normale ou installation postgame.

## Proposition graphique

La source locale conservée est la direction v2 précédemment approuvée. [Sa copie inchangée](source-v2-inchangée.png) est identique octet par octet à `docs/don-spiraton/propositions/direction-artistique-v2-non-validee.png`. Le nom historique « non validée » concerne le sprite natif définitif ; la direction artistique avait été approuvée. La nouvelle image de combat jointe par le créateur sert de référence visuelle de cadrage ; ce n'est pas une capture du moteur.

- [Source et candidate côte à côte](comparaison-source-harmonisee.png) : source à gauche, candidate à droite ; dimensions de présentation seulement.
- [Candidate native128×96](sprite-harmonise-128x96-candidat.png) et [agrandissement×6](sprite-harmonise-x6.png).
- [Véritable capture mGBA240×160](../../../QA_RECETTE_FINALE/DON_SPIRATON/PHASE_A/don-spiraton-candidat-natif.png), [agrandissement×4 nearest-neighbor](../../../QA_RECETTE_FINALE/DON_SPIRATON/PHASE_A/don-spiraton-candidat-x4.png).
- [Turboss et Don Spiraton, deux captures mGBA×3](../../../QA_RECETTE_FINALE/DON_SPIRATON/PHASE_A/comparaison-combats-reels-x3.png), sans modification des personnages rendus.

### Méthode et limites artistiques

Édition assistée de la source v2 pour enlever le halo et simplifier les groupes de couleurs, puis adaptation calibrée à112×76 pixels, contours nets sans interpolation lissée, palette explicite de15 couleurs opaques, transparence binaire et conversion4bpp/RGB555. Le fichier de travail agrandi issu de l'édition est conservé dans `harmonisation-source-candidate.png`. Après conversion, retouches locales sur la grille native : front mauve au lieu des taches claires issues de la réduction, pupilles et dents séparées pour garder le regard menaçant. L'état avant ces retouches est conservé dans `native-avant-retouches-visage.png`. Le processus n'est pas présenté comme un dessin réalisé intégralement pixel par pixel à la main.

La silhouette générale, les bras segmentés, mains, visage violet, yeux et dents jaunes, cornes, flammes, spirale magenta, motifs dorés et base turquoise/rose sont conservés. Des micro-détails internes disparaissent à la résolution finale, notamment autour du front et des dents. Les teintes claires de métal, dents et col partagent un ton ; le maillage doré est allégé. Il s'agit d'une **candidate**, soumise au jugement du créateur, pas d'une ressource artistique définitivement validée.

### Solution GBA réellement exécutée

| Propriété | Valeur |
|---|---|
| Toile native |128×96 pixels |
| Silhouette opaque |112×76, boîte(8,10)–(120,86), borne supérieure exclue |
| Palette |15 couleurs opaques + index0 transparent, RGB555 |
| Construction matérielle |2 objets64×64 +2 objets64×32, un seul sprite logique |
| Tuiles |192 tuiles4bpp,6 144 octets OBJ |
| Position du centre logique |(176,34) |
| Boîte opaque à l'écran |x120–231, y−4–71 |
| Recadrage |4 lignes supérieures hors écran, aux pointes des cornes ; base entière au-dessus du HUD joueur |
| Palette de l'aperçu observée |Banque7 ; HUD boss séparé, inchangé |
| Allocation de tuiles observée |Début469,192 tuiles ; dans les1 024 tuiles OBJ |
| Matrices affines supplémentaires |Aucune pour l'aperçu statique |
| EWRAM statique supplémentaire |Aucun nouveau global EWRAM |

Cette dimension retrouve l'occupation de la zone adverse du montage fourni : grands bras visibles, visage dans la partie supérieure droite, base au-dessus du HUD joueur et aucun recouvrement des menus. La comparaison au montage fourni est visuelle ; aucun recalage pixel à pixel automatisé n'est revendiqué.

`SpiratonArtPreviewShow()` n'a aucun appel depuis le gameplay. Seul le pilote QA le lance explicitement au premier menu du boss. Le sprite diagnostique Bouh est temporairement masqué, puis restauré quand l'aperçu est retiré. Les graphismes permanents ne sont pas remplacés.

**Morphing depuis cette représentation composée n'est pas encore intégré.** Après validation, l'étape B devra faire suivre les quatre objets par la présentation du combattant, masquer/libérer l'ensemble au moment approprié dans l'animation et vérifier son interaction avec substitut, effets d'attaque et nettoyage du combat. La capture statique ne constitue pas cette validation.

## Deux maisons proposées

### 1 — Chemin d'O, Île6 — recommandée

Carte : `SixIsland_WaterPath_House2`. Maison extérieure déjà accessible par la porte(11,19) de `SixIsland_WaterPath`. Intérieur `LAYOUT_HOUSE3`, sortie(4,7), occupant actuel en(7,4).

- Intérêt scénaristique : petite maison à l'écart de la ville ; exil discret hors de Kanto, sans suggérer que Don dirige encore la Mafiamille.
- Intérêt technique : aucun script de carte, objet de quête ou combat dans cette maison ; un seul habitant et une conversation sur sa taille. Entrée/sortie existantes, aucune construction ou retouche du terrain nécessaire.
- Point à décider : cohabitation avec l'habitant existant. La proposition conserve cet habitant et ajoute Don seulement après la victoire finale ; elle ne transforme pas d'office cette maison en propriété privée de Don.
- Accès : Île6 appartient au circuit postgame tardif des Îles Sevii, avec les conditions normales de navigation. Une défaite de Don ne rendrait pas automatiquement cette île accessible plus tôt.
- [Intérieur existant](../../../QA_RECETTE_FINALE/DON_SPIRATON/PHASE_A/ile6-chemin-o-interieur-existant.png) · [extérieur existant](../../../QA_RECETTE_FINALE/DON_SPIRATON/PHASE_A/ile6-chemin-o-exterieur-existant.png).

### 2 — Petite maison, Île5

Carte : `FiveIsland_House2`. Porte extérieure existante(22,9) de `FiveIsland`. Intérieur `LAYOUT_HOUSE3`, sortie(4,7). Un vieil homme se promène près de(2,3).

- Intérêt scénaristique : maison modeste hors de Kanto, dans un secteur où la Mafiamille était déjà présente ; plus facile à retrouver pendant le postgame.
- Intérêt technique : aucune quête ou récompense dans cette maison ; pas de nouvelle porte, carte ou bâtiment nécessaire.
- Réserve scénaristique : proximité de l'ancien entrepôt, qui peut donner une impression de repli près de ses anciens réseaux plutôt que d'isolement. Le propriétaire parle aussi du pré familial et des malfaiteurs ; ce voisinage doit être assumé, sans réécrire son dialogue arbitrairement.
- Réserve technique : son trajet errant devra être conservé ou localement borné avec accord si Don gêne son passage. Aucune collision définitive d'un Don ajouté n'est encore testée puisque ce PNJ n'est pas installé.
- Même accès normal aux Îles Sevii postgame ; aucun raccourci ajouté.
- [Intérieur existant](../../../QA_RECETTE_FINALE/DON_SPIRATON/PHASE_A/ile5-maison2-interieur-existant.png) · [extérieur existant](../../../QA_RECETTE_FINALE/DON_SPIRATON/PHASE_A/ile5-maison2-exterieur-existant.png).

### Emplacements écartés

- `SevenIsland_UnusedHouse` : intérieur sans objet **et sans aucun warp**, donc pas une maison accessible réutilisable sans travaux d'accès.
- `SevenIsland_SevaultCanyon_House` : danse/soin Leveinard, PNJ et Poing Chance à préserver.
- `SevenIsland_House_Room1` : pièce et accès liés au Dresseur e-Reader ; événement existant à préserver.
- Maison de Selphy, Île5 : quête et majordome existants, occupation narrative plus contraignante.

Les cartes et scripts de toutes ces maisons restent inchangés. Les deux propositions principales ont été chargées dans mGBA, et leurs sorties réelles ont été parcourues ; aucune installation de Don n'est simulée comme déjà fonctionnelle.

## Préparation des étapes suivantes

Les nouvelles consignes autorisent après validation du sprite une conclusion où Don reconnaît sa défaite, s'exile, puis Chen félicite le joueur ; l'ancienne réprimande de Matt doit disparaître. La proposition de texte fournie est conservée dans [MISSION.md](MISSION.md). Aucun dialogue supplémentaire n'est rédigé ni intégré à cette étape.

Après validation de la maison : réutiliser l'équipe743 avec ses paramètres actuels, musique Ghoulfather, confirmation oui/non et condition de victoire finale + GAME_CLEAR. Ne pas utiliser la seule victoire du premier combat contre Don pour débloquer l'exil. `TRAINER_BATTLE_SINGLE_NO_INTRO_TEXT` lance directement le combat sans test préalable du flag de victoire ; sa répétabilité devra être exercée deux fois en recette sans effacer les flags de Ligue. Aucun dialogue de revanche définitif n'est rédigé.

## Tests et compilation

- [Rapport mGBA public](../../../QA_RECETTE_FINALE/DON_SPIRATON/PHASE_A/TEST_MGBA.json) et [privé](../../../QA_RECETTE_FINALE/DON_SPIRATON/PHASE_A/prive/TEST_MGBA.json) : aperçu réel, premier tour toujours en attente, zones HUD/menus identiques à l'image avant aperçu, palette RGB555 chargée, libération/restauration, rendu de Turboss existant, deux sorties de maisons.
- [Préservation](../../../QA_RECETTE_FINALE/DON_SPIRATON/PHASE_A/PRESERVATION.json) : graphismes,151 espèces, cartes, scripts, équipes et code du boss précédent inchangés ; les31 flux audio et378 gains privés restent identiques à Argenta.
- Publique :16 777 216 octets ; privée :31 658 447 octets ; marge32 Mio :1 895 985 octets.
- EWRAM :261124/262144 ; IWRAM privée :29888/32768. Aucun global de scène ajouté.
- Aucun test de première conquête normale revendiqué : l'étape B attend la validation graphique.
- Aucun test d'une revanche dans une maison revendiqué : l'étape C attend l'emplacement et le dialogue.
- L'équipe QA de la capture est renforcée ; elle sert à l'aperçu graphique, pas à l'équilibrage.

## Validation demandée

1. Valider ou corriger la candidate graphique et son cadrage réel, avant toute substitution définitive et avant l'étape B.
2. Choisir la maison, avant tout ajout de PNJ ou changement d'événement pour l'étape C.

Aucune finale complète n'est annoncée comme terminée à cette étape.

## Nom court demandé par le créateur

Le HUD affiche désormais « D. SPIRATION », selon la dernière instruction. Ce libellé spécifique est séparé du nom complet utilisé dans les messages. L'aperçu et les compilations publique/privée ont été revérifiés dans mGBA. Cette décision ne vaut pas validation de l'ensemble de la candidate graphique ni choix de la maison.
