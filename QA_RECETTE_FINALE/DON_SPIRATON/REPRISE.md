# Don Spiraton — état technique et reprise

Branche : `feature/boss-final-don-spiraton`, base `d2f590d8b`. Premier jalon : `86e28fd1d` (noyau). Aucune fusion. Lire les décisions actualisées dans `docs/don-spiraton/DECISIONS_VALIDEES.md` avant toute reprise.

## Fonctionnel dans le prototype isolé

- Huit formes, niveaux 56–63, début par Bouh validé.
- Adaptation en fin de tour uniquement, zéro PV sans K.O./expérience/remplacement intermédiaire, action restante annulée, coups multiples arrêtés à la couche vaincue, surplus perdu.
- Métamorphose native ; affichage permanent DON SPIRATON malgré la limite des surnoms.
- PV, statistiques sans bonus, types, talent primaire, quatre capacités légales et PP complets à chaque forme. IV24, EV0, nature neutre. Palette normale : OT prédéfini non shiny.
- Statuts retirés avec message ; nettoyage des effets de l'ancienne forme via la routine native. Pas de réinitialisation globale du terrain.
- Huit couleurs approuvées ; palette dédiée au seul HUD adverse, affichage de la couche suivante derrière la partie vidée de la couche active.
- Entrée visuelle sauvage, sans portrait de Dresseur ni envoi adverse par Ball ; message « Don Spiraton apparaît ! ». Les drapeaux de combat Dresseur demeurent actifs pour interdire capture et fuite.
- La métamorphose initiale attend le premier choix. Elle ne se produit pas pendant l'introduction.

## Don, Matt et Sevii

- Nouvel identifiant Don Ligue743 et équipe indépendante 56/57/56/58/57/60, capacités approuvées, Ghoulfather. Chargement natif en combat vérifié. Aucun ancien Dresseur/équipe modifié.
- Matt postgame : trois équipes de revanche conservées, déclenchées par GAME_CLEAR même si les échanges RS ne sont pas débloqués ; texte de revanche validé ; Decisive Battle.
- Ancien caméo de Don retiré de l'entrepôt : objet, déclenchement et dialogues spécifiques. Trois Mafiamille bonus, drapeaux réservés, ressources communes et événements Saphir conservés. Métadonnées actualisées ; anciens pilotes ne recherchent plus le caméo retiré.

## Activation et limites — IMPORTANT

**La première finale de l'aventure n'est PAS encore remplacée.** Le nouveau combat est accessible uniquement par une fixture native qui appelle `SpiratonBattleArmPrototype()` puis le Dresseur diagnostic744. Aucun script du jeu ne l'arme. Le booléen informatif `production_entry_enabled` reste faux.

Le prototype utilise Bouh comme image initiale de diagnostic, et non une imitation de la vraie forme. La direction artistique v2 et le cadrage du créateur sont validés, mais le sprite natif de combat ne l'est pas encore. Aucun sprite overworld/fusion n'est à produire.

La scène complète Don → Matt/soin → convergence/flash → vrai boss → conclusion/Panthéon reste à brancher et tester. Le flash et la disparition des acteurs ne sont pas encore implémentés dans les scripts de la salle. Les répliques approuvées avant fusion sont conservées dans `data/yokai/spiraton/dialogues_valides_a_integrer.json`. La conclusion exacte doit suivre la nouvelle direction validée et être proposée séparément.

L'algorithme du noyau est déterministe et n'accède à aucune équipe : son API reçoit seulement espèce/niveau/types et éventuelles attaques révélées. L'adaptateur de combat ne remplit pas encore l'historique des attaques révélées. L'évaluation actuelle utilise puissance/précision, statistiques estimées, vitesses et table des types de génération III, avec les immunités Spectre après le marqueur Clairvoyance. Elle ne simule pas encore exhaustivement talents, météo, boosts visibles et effets particuliers : ne pas la présenter comme un calcul parfait du meilleur contre.

## Tests et preuves

- Hôte ASan/UBSan : 1 208 cas, 151 cibles, huit formes différentes, attaques légales/distinctes, dégâts excédentaires, déterminisme, immunités de types.
- `CORE_MGBA.json` : trois séquences du noyau ARM ; inclut un comptage des images d'émulation par appel de sélection, à distinguer du temps réel RPC.
- `COMBAT_PROTOTYPE_MGBA.json` et `PROTOTYPE_COMBAT.gif` : véritable combat rendu par mGBA avec joueur QA renforcé. Pas une partie normale ni une validation de difficulté. PV/PP ennemis non forcés pendant le combat.
- Variantes publique/privée, attaques multiples et cinq statuts : dossiers dédiés. Pour les statuts, injection de fixture explicitement déclarée, puis retrait et message exécutés par le moteur.
- La pause au premier menu vérifie que la première transformation attend une action du joueur. Les contrôles des palettes vérifient les huit couleurs natives et leur allocation séparée. Les drapeaux anti-capture/fuite sont vérifiés ; toutes les interactions de sac/fuite n'ont pas encore été parcourues.
- `LIGUE_MGBA.json` : équipe native de Don et trois vrais déclenchements de revanche, pas encore la nouvelle première conquête.
- `MUSIQUES_MGBA.json` : en-têtes et canaux DPCM réels des trois rôles musicaux.
- `PRESERVATION.json` : 6 040 fichiers protégés, anciennes équipes/Dresseurs, cartes hors modifications autorisées, et octets des 31 OST/gains comparés à Argenta.
- `argenta-regression` : régression de la cinématique existante, quatre arrivées.

Non encore vérifiés : première conquête complète, transition de terrain sous flash, véritable sprite, conclusion/Panthéon/sauvegardes de cette nouvelle finale, difficulté normale, ensemble des interactions Requiem/Prélèvement Destin/KO simultanés/changements forcés, et écoute humaine. Ne pas marquer la mission terminée.

## Commandes

```sh
python3 tools/yokai/generer_spiraton_catalogue.py --check
cc -std=c99 -Wall -Wextra -Werror -fsanitize=address,undefined -g \
  -Itests/spiraton/shims -Iinclude -Isrc \
  tests/spiraton/test_core.c src/spiraton_core.c -o /tmp/spiraton-core-test
/tmp/spiraton-core-test
source /workspace/.setup/env.sh
make -j6
make -j6 YOKAI_AUDIO_DIR=/workspace/private-audio/argenta-integration
python3 tools/yokai/tester_spiraton_combat_mgba.py
YOKAI_QA_ROM=$PWD/pokefirered_audio.gba \
  YOKAI_SPIRATON_REPORT_DIR=QA_RECETTE_FINALE/DON_SPIRATON/prive \
  python3 tools/yokai/tester_spiraton_combat_mgba.py
python3 tools/yokai/tester_spiraton_ligue_mgba.py
YOKAI_QA_ROM=$PWD/pokefirered_audio.gba python3 tools/yokai/tester_spiraton_musiques_mgba.py
python3 tools/yokai/verifier_spiraton_preservation.py
```

Ressources audio : mêmes fichiers privés que le jalon Argenta. Aucune nouvelle conversion audio ni modification d'encodage, de boucle ou de gain. Aucun fichier audio, ROM ou sauvegarde à committer.

## Prochain point de reprise

1. Produire le vrai sprite de combat natif selon v2 et le montage validés, sans halo, puis obtenir sa validation ; ne pas créer d'overworld.
2. Compléter l'évaluation des contres et les cas limites du moteur. Préserver la frontière de fin de tour.
3. Monter la scène de Ligue avec les graphismes Don/Matt/gardes existants, soin natif complet, flash blanc et retrait hors champ, puis appel du vrai boss. Réutiliser la correction de palettes locale pour Matt/Don.
4. Proposer les répliques finales selon la nouvelle direction ; relier ensuite Panthéon/flags/postgame sans relancer Matt en première conquête.
5. Recette de sauvegardes et de l'ensemble des deux combats, avec captures natives et conditions normales.
