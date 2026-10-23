# Reprise Don Spiraton — 23 octobre 2026

Le prototype existant est récupéré, corrigé et prolongé par une scène de développement exécutée dans mGBA. **La première conquête normale n'est pas encore remplacée : l'entrée de production demeure celle de Matt.** Le vrai sprite de combat natif manque et les dialogues exacts de conclusion ne sont pas approuvés. Aucun de ces éléments n'est inventé ou présenté comme terminé.

## Récupération et protection

- Branche exclusive : `feature/boss-final-don-spiraton`, base `d2f590d8b`.
- `1a3ea491f2d253140033c3dacfca14d0ba5fdef6` retrouvé localement et confirmé sur GitHub par `git ls-remote`.
- Modifications locales préservées dans `/workspace/spiraton-recovery-20261023.patch` et liste d'état associée, hors dépôt. Aucun reset, nettoyage destructif ou rebase.
- Optimisations et correction du tampon récupérées, testées puis publiées dans [0b0f99524](https://github.com/JusteYoann/Pokemon-Yokai-Watch/commit/0b0f9952465b7a86cfb312fb3372fb0bf774e1a0).
- Aucun travail perdu à reconstruire. Aucun conflit Git trouvé.
- `master`, Mafiamille, Argenta et audio31 conservent leurs commits de référence ; aucune fusion.

## Corrections effectivement réalisées

1. Sélection accélérée : statistiques précalculées et élimination des attaques dominées pour le classement des contres. Comparaison avec le calcul exhaustif : mêmes résultats sur 1 208 cas, checksum `495816fb`. Trois séquences ARM : deux images d'émulation par sélection sur les cibles testées. Pas une garantie sur toutes les configurations possibles.
2. Messages de guérison : chaînes dédiées plutôt que copie de textes longs dans `gBattleTextBuff1`, limité à 16 octets. Le débordement potentiel du jalon précédent est corrigé.
3. Scène native ajoutée dans [spiraton.inc](../../../data/maps/PokemonLeague_ChampionsRoom/spiraton.inc), avec appel explicite de développement uniquement. Aucun déclencheur de production ne l'appelle.
4. Palette Matt séparée localement dans cette salle, comme à Argenta : banque6 pour Matt, banque10 pour Don/sbires. Pixels, palettes sources et animations existants inchangés.
5. Présentation du HUD corrigée : le nom initial était encore Bouh avant la première métamorphose ; DON SPIRATON est désormais affiché dès le premier choix. Aucun agrandissement global des surnoms ou du format de sauvegarde.
6. Fin du boss : routine native de fin sans faire revenir un portrait de Dresseur fictif ni imprimer son faux dialogue de défaite. Musique de victoire native conservée ; les restrictions Dresseur restent actives.
7. Espèce initiale centralisée dans [spiraton_config.h](../../../include/spiraton_config.h). Après clarification pendant la reprise, le créateur a reconfirmé Bouh et les huit couleurs antérieurement approuvées.

## État fonctionnel

| Élément | État constaté | Preuve / limite |
|---|---|---|
| Don Morléone Ligue | Fonctionnel en diagnostic | Six membres et capacités validés, nouvel identifiant743 ; anciennes équipes intactes |
| Matt entre après Don | Fonctionnel en scène de développement | Déplacements natifs, répliques préalablement approuvées |
| Soin complet | Vérifié dans mGBA | PV, PP avec bonus, statuts ; inclut un équipier K.O./empoisonné/sans PP |
| « MAFIAMILLE ! À MOI ! » | Intégré | Texte validé, sans nouveau dialogue de conclusion |
| Convergence | Vérifiée | Trois sbires finissent en (5,8), (7,8), (6,7), autour de Don(6,8) |
| Flash et disparition | Vérifiés | Fondu natif blanc ; retrait de Don et trois gardes hors champ, plus de99 % des pixels blancs ; pas de blocage |
| Overworld/fusion Don Spiraton | Aucun créé | Quatre acteurs ajoutés réutilisent uniquement Don et les sbires existants |
| Entrée visuelle sauvage | Fonctionnelle | Pas de portrait initial, pas d'envoi adverse par Ball ; message d'apparition vérifié |
| Vraie apparence initiale | **Manquante** | Bouh reste une image de diagnostic ; la proposition artistique v2 n'est pas une ressource GBA native validée |
| Premier choix / Morphing | Vérifié | Pause180 images au menu ; aucune transformation avant choix ; transition native avant attaques, sans consommer une action |
| Huit formes56–63 | Vérifiées | Huit espèces distinctes, pas de K.O./EXP/remplacement intermédiaire, surplus perdu |
| Sept transitions suivantes | Vérifiées en fin de tour | Nouvelle vie complète, statistiques normales, types, talent primaire, quatre capacités légales et PP |
| Sélection du contre | Fonctionnelle selon le score actuel | Parcours des151 espèces hors formes utilisées ; test du remplaçant actif après K.O. ; voir limites ci-dessous |
| CT | Catalogue vérifié | 3 929 entrées espèce/capacité légales ; CT compatibles et apprentissage naturel, pas d'ajout arbitraire de CS/tuteurs |
| Cinq statuts | Vérifiés dans mGBA | Brûlure, poison, paralysie, sommeil, gel : retrait et messages natifs observés ; statuts injectés comme fixtures explicites |
| Attaques multiples | Vérifiées | Une attaque ne retire pas plusieurs couches |
| Huit couleurs / couches | Vérifiées | Vert, orange, cyan, bleu, violet, magenta, rouge, ivoire ; palette dédiée au HUD adverse |
| Fuite | Refus vérifié par manette | Pas de première transformation déclenchée par la tentative refusée |
| Capture | Garde native vérifiée | Master Ball conduit au blocage Dresseur ; appel du gestionnaire avec fixture, **pas** parcours complet du sac |
| K.O. simultané | Vérifié | Explosion : joueur sans remplaçant perd, pas de victoire prématurée ni nouvelle phase |
| Remplaçant du joueur | Vérifié | Explosion avec équipier valide, remplacement par manette avant sélection ; contre conforme au nouvel actif |
| Conclusion première conquête | **Non raccordée** | Répliques exactes à valider ; aucune nouvelle réplique inventée |
| Panthéon / crédits / sauvegarde | Routines natives vérifiées après victoire | **Saut QA explicite** qui contourne la conclusion en attente ; crédits jusqu'aux états17/18, sauvegarde Flash, véritable Continuer vers le postgame |
| Matt postgame | Vérifié | GAME_CLEAR suffit, sans échange RS ; trois variantes de revanche inchangées, niveaux68/69/70/70/71/73 ; Decisive Battle |

La scène de diagnostic s'arrête sans accorder GAME_CLEAR. C'est seulement le parcours QA optionnel du Panthéon qui produit la sauvegarde de fin. Un utilisateur d'une partie normale ne rencontre donc pas une version incomplète du nouveau final.

## Musiques et compilation

Les trois rôles sont contrôlés dans le mélangeur privé réel :

| Rôle | Identifiant | Ressource privée | Résultat |
|---|---|---|---|
| Don Morléone | MUS_YOKAI_GHOULFATHER349 | mus_yokai_03 | En-tête et canal DPCM actifs |
| Don Spiraton | MUS_YOKAI_ZAZELMARE352 | mus_yokai_06 | En-tête et canal DPCM actifs |
| Matt revanche | MUS_YOKAI_DECISIVE_BATTLE361 | mus_yokai_15 | En-tête et canal DPCM actifs |

Aucune fusion audio31. Aucune modification des échantillons, boucles ou gains. Les31 flux encodés et les378 réglages de gain sont comparés octet par octet à la ROM privée Argenta de référence.

- Publique : **16 777 216 octets** ; compilation réussie, audio de secours public conservé.
- Privée : **31 651 655 octets**, environ30,185 Mio ; compilation réussie.
- Marge sous32 Mio : **1 902 777 octets**.
- EWRAM :261124/262144 octets ; IWRAM :29824/32768 octets. La marge EWRAM reste faible ; aucune nouvelle allocation statique nécessaire pour la scène.
- SHA publique : `0fc1184760ccb0af5793912153f6b2010f1776bf714a27fb9f506b5cb587803f`.
- SHA privée : `a282492e81fc96c5685839c327189dd91334eeca183c673579055a041719cc04`.
- 6 040 ressources protégées contrôlées, dont graphismes et données permanentes des151 espèces ; anciennes équipes préservées. Les quatre modèles d'acteurs de diagnostic sont la seule extension de la carte du Maître, dont les événements originaux sont conservés.

## Preuves et reproduction

Les tests Python suivants pilotent **réellement mGBA/libretro**. Ils utilisent des fixtures natives et des équipes renforcées ; ce n'est pas une partie normale ni une écoute humaine.

- [Scène publique](scene/SCENE_MGBA.json), [scène privée avec Panthéon](scene-privee/SCENE_MGBA.json).
- [Combat public huit couches](COMBAT_PROTOTYPE_MGBA.json), [combat privé](prive/COMBAT_PROTOTYPE_MGBA.json), [coups multiples](multicoups/COMBAT_PROTOTYPE_MGBA.json).
- [Limites et remplacement](limites/LIMITES_MGBA.json), [noyau ARM](CORE_MGBA.json), [Don/revanches](LIGUE_MGBA.json).
- Cinq dossiers `statut-burn`, `statut-poison`, `statut-paralysis`, `statut-sleep`, `statut-freeze` : messages et combats complets.
- [Mélangeur privé](MUSIQUES_MGBA.json), [préservation](PRESERVATION.json).
- Régression Argenta : quatre arrivées exécutées après l'extension locale des palettes ; son rapport porte le SHA du jalon immédiatement antérieur à la dernière correction du HUD de combat. Ne pas le confondre avec un test Argenta rejoué sur le dernier binaire.
- Les dossiers `recuperation-brulure` et les captures de jalons précédents sont historiques. Chaque JSON porte son propre SHA.

```sh
source /workspace/.setup/env.sh
python3 tools/yokai/generer_spiraton_catalogue.py --check
make -j6
make -j6 YOKAI_AUDIO_DIR=/workspace/private-audio/argenta-integration
python3 tools/yokai/tester_spiraton_scene_mgba.py
YOKAI_QA_ROM=$PWD/pokefirered_audio.gba YOKAI_SPIRATON_TEST_HOF=1 \
 YOKAI_SPIRATON_SCENE_REPORT_DIR=QA_RECETTE_FINALE/DON_SPIRATON/scene-privee \
 python3 tools/yokai/tester_spiraton_scene_mgba.py
python3 tools/yokai/tester_spiraton_limites_mgba.py
python3 tools/yokai/tester_spiraton_combat_mgba.py
python3 tools/yokai/tester_spiraton_ligue_mgba.py
YOKAI_QA_ROM=$PWD/pokefirered_audio.gba python3 tools/yokai/tester_spiraton_musiques_mgba.py
python3 tools/yokai/verifier_spiraton_preservation.py
```

Le profil ASan/UBSan hôte vérifie1 208 cas ; ce contrôle est distinct des tests ARM et des combats rendus.

## Ce qui reste à faire

**Avant activation dans une partie normale :**

1. Fournir/valider un véritable sprite natif de combat, puis relier cette présentation initiale sans créer de neuvième couche ni de sprite overworld. La direction v2 seule ne suffit pas.
2. Valider les répliques exactes de conclusion, puis raccorder le déclencheur de première conquête, l'arrivée de Chen et le Panthéon. Les dialogues de la proposition historique ne sont pas intégrés.
3. Rejouer ce parcours de production sans saut QA, vérifier sa défaite/reprise et ses sauvegardes.

**Limites techniques encore à vérifier :**

- Difficulté avec une équipe normale ; les équipes999/LV100 ou999/LV65 des fixtures n'évaluent pas l'équilibrage.
- Le classement des contres considère types, statistiques estimées, vitesse, puissance et précision. Il ne simule pas exhaustivement talents, météo, boosts et effets particuliers. L'adaptateur ne fournit pas encore l'historique des attaques révélées au noyau. Aucun accès aux capacités cachées, objets, actions choisies ou équipe de réserve du joueur.
- Nettoyage des effets temporaires via la routine native ; pas de recette exhaustive de Requiem, Prélèvement Destin, dégâts différés et tous changements forcés. Le K.O. simultané et le remplacement après Explosion sont en revanche réellement couverts.
- La capture est interdite par les règles Dresseur et le gestionnaire natif testé ; le parcours complet de l'interface du sac reste à couvrir.
- Aucune écoute humaine des transitions musicales et aucune validation artistique du véritable sprite.

Le prototype est sécurisable et reproductible dans ce périmètre. **La mission complète de finale jouable n'est pas déclarée terminée.**
