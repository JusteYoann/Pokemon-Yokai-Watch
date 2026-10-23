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

La scène Don → Matt/soin → convergence/flash → boss de diagnostic existe maintenant dans `data/maps/PokemonLeague_ChampionsRoom/spiraton.inc`, sans déclencheur de production. Les deux combats enchaînés, le soin, les trois trajets, le flash et le retrait masqué des acteurs ont été exécutés dans mGBA. La véritable apparence et la conclusion restent à intégrer après validation. Les répliques approuvées avant fusion sont conservées dans `data/yokai/spiraton/dialogues_valides_a_integrer.json`. La conclusion exacte doit suivre la nouvelle direction validée et être proposée séparément.

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

Non encore vérifiés : première conquête normale complète et véritable sprite, raccord de production de la conclusion, difficulté normale, ensemble des interactions Requiem/Prélèvement Destin/changements forcés, interface du sac pour toutes les Balls, et écoute humaine. Le K.O. simultané et le remplacement du joueur avant le choix du contre sont désormais testés. Panthéon/crédits/sauvegarde sont testés après victoire par un saut QA explicite qui contourne la conclusion en attente. Ne pas marquer la mission terminée.

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
3. La scène de Ligue est montée et testée en développement. Après validation du vrai sprite et de la conclusion, la raccorder au déclencheur de première conquête ; ne pas activer sa version de diagnostic dans une partie normale.
4. Proposer les répliques finales selon la nouvelle direction ; relier ensuite Panthéon/flags/postgame sans relancer Matt en première conquête.
5. Recette de sauvegardes et de l'ensemble des deux combats, avec captures natives et conditions normales.

## Récupération du 23 octobre 2026

Le commit `1a3ea491f2d253140033c3dacfca14d0ba5fdef6` a été retrouvé localement et confirmé par `git ls-remote` sur la branche distante. Les modifications locales récupérées ont été sauvegardées hors dépôt dans `/workspace/spiraton-recovery-20261023.patch`.

Corrections récupérées : sélection accélérée par statistiques précalculées et élimination des attaques dominées (même type/priorité), vérifiée contre le calcul exhaustif : 1 208 cas, checksum `495816fb` identique. Trois séquences ARM mesurent deux images par sélection dans mGBA. Les longs messages de guérison utilisent maintenant des identifiants de chaînes dédiés : aucun texte long n'est copié dans le tampon de 16 octets. Une nouvelle exécution du combat natif avec brûlure confirme son retrait et son message après cette correction. ROM publique et privée recompilées.

Le nouveau document avait remis la première espèce et les six couleurs supplémentaires en attente. Après clarification, le créateur a répondu « Conserver les choix précédents » : Bouh et les huit couleurs sont reconfirmés. Le véritable sprite initial manque toujours ; Bouh demeure une image de diagnostic uniquement.

## Nouvelle scène de développement

Appel explicite : `ScriptContext_SetupScript(PokemonLeague_Spiraton_DevelopmentEntry)` dans une salle de diagnostic préparée, joueur en (6,10), déclencheur Matt existant désarmé par la fixture. Aucun PNJ, menu ou déclencheur de production ne lance cette entrée. Quatre modèles d'acteurs Don/sbires réutilisent les graphismes existants et sont cachés normalement par FLAG_TEMP_6. La palette Matt en banque6 est étendue localement à cette salle sèche, Don/sbires gardent leur banque10.

`tester_spiraton_scene_mgba.py` exécute les deux combats avec une équipe QA renforcée, vérifie la guérison d'un membre K.O./empoisonné/sans PP, les coordonnées finales des trois gardes, les palettes séparées et plus de 99 % de pixels blancs lors du retrait. La victoire du boss utilise la fin native sans faire réapparaître un portrait de Dresseur fictif. Aucun texte de conclusion n'est ajouté.

Option `YOKAI_SPIRATON_TEST_HOF=1` : après victoire, saut QA explicite au Panthéon natif, crédits complets, sauvegarde Flash puis véritable Continuer et contrôle de GAME_CLEAR. Ce saut n'est PAS le raccord de production de la finale. Les rapports distinguent ces deux éléments.

`tester_spiraton_limites_mgba.py` vérifie le refus de Fuite par manette ; le rejet Master Ball par appel natif du gestionnaire (fixture relâchant le contrôleur, pas un test complet du sac) ; Explosion avec défaite simultanée ; puis Explosion avec équipier valide, remplacement par manette et sélection du contre sur cet équipier uniquement.

Le rapport de clôture de cette reprise est `RAPPORT_REPRISE.md`. Les anciens rapports et captures sont des jalons historiques ; les SHA des ROM dans chaque JSON permettent de les distinguer des preuves finales.
