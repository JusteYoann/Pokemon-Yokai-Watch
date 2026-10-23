# Quête secrète Juste Yoann et Charme Chroma

**Intégrée et vérifiée par des tests ciblés mGBA sur les versions publique et privée.** Branche `feature/juste-yoann-charme-chroma`, sans merge sur master.

[Demande intégrale](demande/CAHIER_DES_CHARGES.md) · [Audit](AUDIT.md) · [Fichiers modifiés](FICHIERS_MODIFIES.txt).

## Personnage et déblocage

Juste Yoann est immobile et toujours de face en `(6,2)`, contre le mur du haut de la chambre. Le PC et l’escalier restent accessibles. Son apparition requiert les **151 espèces obtenues**, puis la nouvelle conversation avec Chen au laboratoire. Les bits « aperçu » et le compteur du diplôme ne sont pas utilisés à la place de cette condition. L’invitation ne se répète pas ; les autres événements de Chen restent en place.

Les deux graphismes proviennent de la **reproduction autorisée puis approuvée dans le chat**, avec la peau du visage et des mains presque blanche. Ce ne sont pas des copies pixel pour pixel du premier aperçu. La source approuvée est conservée dans `graphics/juste_yoann/source/reproduction-peau-claire.png`. La conversion technique utilise le voisin le plus proche et une palette RGB555 commune : PNJ de 19 pixels de haut dans une frame 32×32, portrait de 60 pixels de haut dans une frame 64×64. Une seule image de face est utilisée ; aucune marche n’est créée.

[Capture du PNJ dans la chambre](integration/public/juste-yoann-chambre-x3.png) · [Variante fille](integration/public/juste-yoann-variante-fille-x3.png) · [Portrait en combat](integration/public/victoire-joueur-portrait-x3.png) · [Introduction animée](integration/public/victoire-joueur-introduction.gif).

## Combat et conclusion

Équipe exacte, dans l’ordre : **Démophage 70, Fouétar 70, Camaïeul 70, Terminyanator 70, Démophage 70, Seigneur Enma nº150 70**. IA classique (`CHECK_BAD_MOVE`), aucun objet tenu ou de soin, attaques natives de montée en niveau, paramètre IV 100. Les statistiques de base restent inchangées.

Le refus permet de revenir ; une défaite entraîne le comportement natif de retour après K.O. et conserve la possibilité de retenter le duel. Après la première victoire, le discours et le fondu progressent avec les textes. Les palettes de texte restent lisibles. **THANK FOR PLAY** apparaît sur fond blanc pendant trois secondes avec un court silence, puis la chambre retrouve ses couleurs. Juste Yoann remet le Charme Chroma et reste présent. Les conversations suivantes ne proposent ni revanche ni nouveau discours ni second cadeau.

[GIF du discours, du fondu et de THANK FOR PLAY](integration/public/discours-fondu-cadeau.gif) · [GIF de l’obtention du charme](integration/public/obtention-charme.gif) · [Chambre après la scène](integration/public/chambre-apres-victoire-x3.png) · [Sac après la scène](integration/public/sac-apres-scene-x3.png).

## Charme Chroma et sauvegarde

L’objet important nº52 remplace un emplacement réservé inutilisé. Il ne peut pas être vendu, jeté ou consommé via les menus natifs. [Icône dédiée et vérifications du sac](icone-charme/README.md). Le cadeau est protégé par un drapeau ; si la poche est pleine, il reste disponible en reparlant au PNJ sans rejouer le discours. L’invitation, la victoire, le cadeau et l’objet sont conservés après sauvegarde Flash et Continuer. Aucun SaveBlock n’est agrandi ; les bits persistants `0x331` à `0x334` sont utilisés.

Le charme applique jusqu’à trois tirages de personnalité, en conservant le premier succès. Chaque tentative bénéficie du bonus Safari dans les quatre cartes du Parc. L’OT et le fonctionnement shiny de troisième génération sont conservés. Les cadeaux, rencontres statiques et Dresseurs restent hors de ce chemin. La politique existante des 84 espèces shiny autorisées ainsi que toutes les palettes et images shiny sont préservées.

| Situation | Probabilité |
|---|---:|
| Sans bonus | 1/8192 |
| Safari seul | 3/8192, environ 1/2731 |
| Charme seul | `1-(1-1/8192)^3`, environ 1/2731 |
| Safari et charme | `1-(1-3/8192)^3`, environ 1/911 |

## Vérification mGBA et préservation

[Quête publique](integration/public/TEST_MGBA.json) · [Quête privée](integration/prive/TEST_MGBA.json) · [Tirages publics](integration/public/SHINY_NATIF.json) · [Tirages privés](integration/prive/SHINY_NATIF.json) · [Régressions publiques](integration/regressions/public/COMPLEMENTS_MGBA.json) · [Régressions privées](integration/regressions/prive/COMPLEMENTS_MGBA.json).

Par version, les treize contrôles de quête passent : absence avant complétion, absence avec 151 aperçus, absence avant validation de Chen malgré 151 obtenus, interaction réelle avec Chen, position/face immobile, persistance de l’invitation, refus, défaite réelle, victoire réelle sur les six adversaires et scène complète, persistance de la victoire et du charme, absence de répétition, sac utilisable après le blanc, variante fille. Les adversaires, leurs PV et le résultat ne sont pas modifiés par les tests. Une équipe joueur faible sert à tester la défaite et une équipe forte à raccourcir le test de victoire ; ce n’est pas une validation d’équilibrage en partie normale.

Les calculs shiny sont testés sur les ROM finales : quatre situations × deux graines × deux millions de tirages par version, dans une tolérance de six écarts-types. Il s’agit d’appels au RNG natif et au calcul de PID, pas de millions de captures naturelles.

Dix contrôles de régression natifs passent par version, notamment les sprites/palettes de Zazel, Enma l’Ancien, Orqanos, Maître Nyada et Kyubi, le Multi Exp conservé, Yopple, la sauvegarde et les fiches personnages. Les 49 contrôles de préservation du dossier précédent passent également : identifiants et données des 151, Cramois/Hovernyan, scripts protégés, Champions et équipes de Don préservés. La numérotation des graphismes et Dresseurs existants est conservée ; les nouveaux sont ajoutés en fin de tables.

Ces fixtures ne remplacent pas la recette globale du jeu, l’obtention naturelle des 151 espèces ou l’équilibrage. La future quête de Maître Nyada et les signalements graphiques précédents hors de ce lot restent distincts.

## Mémoire et compilation

Les versions publique et privée compilent. [Mesures exactes et SHA256 des ROM finales](integration/MEMOIRE.json).

| Mesure | Public | Privé |
|---|---:|---:|
| Fichier ROM | 16777216 | 31751591 |
| Sections ROM occupées | 9784328 | 29777102 |
| EWRAM utilisée / libre | 261368 / 776 | 261368 / 776 |
| IWRAM utilisée / libre | 29824 / 2944 | 29888 / 2880 |

La RAM statique reste inchangée. La scène utilise une tâche temporaire et une petite fenêtre de 2688 octets, retirées à son terme. Les musiques existantes ne sont pas remplacées : pause et reprise natives pendant l’écran blanc.

## Reproduction

```bash
source /workspace/.setup/env.sh
make -j6
make -j6 YOKAI_AUDIO_DIR=/workspace/private-audio/lavanville-integration
python3 tools/yokai/tester_yoann_quete_mgba.py
YOKAI_QA_ROM="$PWD/pokefirered_audio.gba" python3 tools/yokai/tester_yoann_quete_mgba.py
YOKAI_QA_PROOFS=docs/juste-yoann/integration python3 tools/yokai/tester_yoann_shiny_mgba.py
YOKAI_QA_PROOFS=docs/juste-yoann/integration YOKAI_QA_ROM="$PWD/pokefirered_audio.gba" python3 tools/yokai/tester_yoann_shiny_mgba.py
python3 tools/yokai/verifier_dossier_preservation.py
```

Les anciens dossiers `core/` et `icone-charme/` conservent les preuves des étapes précédentes avec leurs propres SHA256 ; `integration/` contient celles de la quête intégrée.
