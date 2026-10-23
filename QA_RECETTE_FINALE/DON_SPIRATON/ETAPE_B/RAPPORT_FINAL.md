# Étape B — finale de la Ligue et Don Spiraton

## Résultat

La première conquête est activée et terminable normalement : Lance → Don
Morléone → arrivée et soin de Matt → convergence/flash → Don Spiraton → huit
formes → conclusion → départ de la Mafiamille → Chen → Panthéon → crédits →
sauvegarde/Continuer → postgame. Aucun déclenchement QA n'est nécessaire au jeu.

Le parcours mGBA public et privé part d'une position préparée devant Lance avec
une équipe renforcée, puis gagne réellement les combats. Aucun flag de victoire,
résultat forcé, pointeur de script ou warp QA intermédiaire ne remplace la
nouvelle finale. Le test n'est pas présenté comme une partie depuis le starter.
Une fixture d'équipier K.O./empoisonné/PP0 vérifie le soin de Matt ; l'option
native Fixe simplifie le pilotage. Voir `jalon3/*/FINALE_NORMALE_MGBA.json`.

## Graphisme et combat

Le fichier harmonisé approuvé est inchangé, sans nouveau dessin. Toile128×96,
silhouette112×76,15 couleurs+transparence. Le battler adverse lui-même porte les
quatre OBJ : aucune doublure décorative. Centre(176,38) : les quatre lignes
initialement recadrées sont visibles, sans réduction, bas du dessin ày75 avant
le HUD joueur ày76. Palette native adverse, aucun banc supplémentaire.

Le grand sprite reste jusqu'au choix de la première action. Le premier Morphing
reprend la tâche et les sons natifs, avec mosaïque OBJ pour cette seule grande
image (le clone BG natif est limité à64×64). Le remplacement graphique se fait
au point natif de changement d'espèce ; les6144octets de tuiles temporaires sont
libérés. Bouh apparaît au niveau56, avant les attaques, sans action consommée.
Sept transformations supplémentaires suivent en fin de tour, niveaux57–63.
Les huit couleurs et le nom HUD volontaire `D. SPIRATION` sont conservés.
La palette normale est rétablie après chaque Morphing.

Les déclenchements sont observés dans les mélangeurs SE : un `se_m_teleport`
puis un `se_m_minimize` par transformation, exactement8 de chaque pendant les
huit Morphing. Les sons identiques éventuellement employés par d'autres
attaques sont exclus du comptage. Aucune écoute humaine n'est revendiquée.
Le mélangeur privé garde `mus_yokai_06` (Vs. Zazelmare), puis passe à
`mus_yokai_07` à la victoire (`jalon4/mixeur-victoire-prive`).

## Recette

| Vérification | Public | Privé | Preuve / portée |
|---|---|---|---|
| Lance, porte réelle, entrée normale et deux combats | OK | OK | jalon3, aucune victoire injectée |
| Soin HP/PP/statuts des six membres | OK | OK | K.O./poison/PP0 préparés côté joueur |
| Flash masque Don et gardes | OK | OK | écran >99% blanc, aucun OW Spiraton |
| Vraie apparence puis Bouh après le choix | OK | OK | jalons1/3 et tests combat jalon4 |
| Huit espèces distinctes, niveaux, couleurs, palettes finales | OK | OK | tests combat, jamais de neuvième barre |
| Pas d'EXP intermédiaire, coups multiples | OK | contrôle partagé | multicoups-public + code identique |
| Brûlure, poison, paralysie, sommeil, gel effacés | cinq cas OK | brûlure/sommeil OK | statuts-public, statut-prive, mixeur-victoire-prive |
| Couche épuisée par Toxic natif | OK | OK | residuel-*, HP ennemis jamais écrits |
| Fuite refusée par les touches | OK | OK | limites-* |
| Master Ball bloquée | OK | OK | commande native injectée, pas parcours complet du sac |
| Explosion/K.O. simultané et remplacement avant contre | OK | OK | limites-*, choix selon remplaçant actif |
| Défaites contre Don et Spiraton, whiteout et reprise Don classique | OK | OK | defaites-*, faiblesse du joueur préparée |
| Conclusion, départ des quatre PNJ, arrivée de Chen | OK | OK | jalon3 ; répliques du document autorisé |
| Panthéon, crédits17/18, Flash et vrai Continuer | OK | OK | jalon3 |
| Matt, trois équipes postgame et niveaux conservés | OK | OK | matt-* ; scénarios starter préparés |
| Exil depuis la sauvegarde réelle de cette finale | OK | OK | postgame-*, aucun flag de déblocage injecté |
| Refus, deux revanches sans sortir, Flash save/load à l'exil | OK | OK | postgame-* |
| Combat sauvage ordinaire après boss/exil | OK | OK | Turboss, aucun résidu du composite |
| Ghoulfather/Zazelmare/Decisive Battle dans le mélangeur | — | OK | musiques/MUSIQUES_MGBA.json |

Le test pur du noyau passe1208 cas (151 cibles×8phases), légalités naturel/CT,
espèces distinctes, débordement perdu et sélection déterministe ; checksum
`495816fb`. Catalogue vérifié :3929 entrées légales. Les hooks ne lisent que le
combattant actif du joueur. Le moteur de score existant n'est pas une simulation
exhaustive des talents, météos et effets de toutes les attaques.

Les essais de reprise utilisent un lieu de soin préparé sur l'Île6 et affaiblissent
uniquement le joueur pour provoquer une défaite native, sans résultat forcé.
Les tests d'exil commencent par un déplacement QA à l'extérieur de la maison,
puis utilisent sa vraie porte : aucun trajet en bateau n'est revendiqué.
Les anciennes sauvegardes GAME_CLEAR sans victoire744 gardent le résident
original ; le déblocage reste bien Panthéon ET victoire Spiraton.

## Équilibrage exploratoire — aucune modification appliquée

Équipe testée : Jibanyan, Komastar, Passpa, Triptic-tac, Antonnerre, Usapyon.
Création native : IV24, EV0, statistiques normales, quatre attaques légales
naturel/CT choisies parmi les plus puissantes avec couverture de types.
Sans objets tenus, sans objets de soin, sans changement volontaire. Le pilote
choisit une estimation simple des dégâts visibles et remplace ses K.O. par les
touches. Les deux adversaires sont testés séparément avec une équipe soignée.

| Niveau des six | Don classique | Durée indicative | Spiraton | Durée indicative | Phases atteintes |
|---|---|---:|---|---:|---|
|56|défaite|4min50|défaite|4min36|1–4|
|60|défaite|6min17|défaite|4min12|1–4|
|63|défaite|6min51|défaite|3min58|1–4|

Les durées viennent des itérations du pilote /59,7275Hz ; les quelques frames
ajoutées par les appels d'observation RPC ne sont pas incluses. Elles sont des
ordres de grandeur, pas des chronométrages audio exacts.

Ces six défaites sont un signal de difficulté à faire examiner par un joueur,
avec ses EV accumulés, ses objets et sa stratégie. Elles ne démontrent pas une
impossibilité stratégique. Les contres adaptatifs mettent cette équipe en
échec dès la quatrième phase. La difficulté réelle de la huitième phase n'est
pas évaluée par ces essais normaux ; sa fonctionnalité est vérifiée par les
tests renforcés. Le soin complet de Matt est confirmé techniquement et donne
une équipe fraîche pour huit vies, sans garantir leur équilibrage.

Recommandation : essai humain de cette finale avant tout ajustement chiffré.
Si la difficulté est jugée excessive, discuter séparément les paramètres du
boss ; aucune statistique des151 ni équipe validée n'a été changée.

## Taille, mémoire et préservation

| | Public | Privé31 OST |
|---|---:|---:|
|ROM, octets|16777216|31658395|
|Marge sous32Mio|16777216|1896037|
|EWRAM|261128/262144|261128/262144|
|IWRAM|29824/32768|29888/32768|

EWRAM : +4octets par rapport au commit4289f076d,1016 octets libres.
Graphisme transitoire :192tuiles OBJ=6144octets, palette adverse existante.
Pas de nouveau buffer statique de toile. Les tuiles disparaissent au Morphing,
et le nettoyage de combat couvre aussi la fin/défaite.

`PRESERVATION.json` contrôle les seules sources autorisées, l'identité binaire
du sprite approuvé et des trois fichiers de la maison d'exil, les151 données et
graphismes, les équipes, Argenta et les31 flux DPCM ainsi que les378 gains.
Les31 flux/gains compilés sont comparés octet pour octet au privé Argenta ;
masque audio actif31bits. Aucun fichier audio, ROM ou sauvegarde n'est publié.
Les sources audio privées restent dans `/workspace/private-audio/argenta-integration`.

## Captures, reproduction et commits

- `jalon1/*/PREMIER_MORPHING.gif` : capture réelle du grand sprite vers Bouh.
- `jalon3/public/parcours-complet-captures.png` : montage de captures réelles.
- `jalon3/*/etape-6.png`, `etape-8.png`, `pantheon-natif.png` : conclusion/Chen/Panthéon.
- Vidéo native avec mixage privé, hors Git :
  `/workspace/artifacts/spiraton-etape-b/premier-morphing/premier-morphing-mgba-audio.mp4`.
- États QA après le vrai Continuer, hors Git :
  `/workspace/artifacts/spiraton-etape-b/postgame-{public,prive}.state.gz`.

Sources des captures : harnais `tools/yokai/tester_spiraton_finale_normale_mgba.py`,
`tester_spiraton_postgame_reel_mgba.py` et `capturer_spiraton_premier_morphing.py`.
Pour reproduire : charger `/workspace/.setup/env.sh`, `make -j6`, puis
`make -j6 YOKAI_AUDIO_DIR=/workspace/private-audio/argenta-integration` ; lancer
le harnais finale, puis postgame avec `YOKAI_QA_ROM` pour choisir la ROM privée.
Les autres tests et leurs noms sont regroupés dans `jalon4/`.

Commits publiés sur `feature/boss-final-don-spiraton` :

1. `b6e9c3aa7` — battler véritable et premier Morphing.
2. `b13c23dd3` — entrée normale et cinématique partagée.
3. `8cc264b83` — conclusion et parcours natif jusqu'au postgame.
4. Le commit portant ce rapport — recette finale, mesures et état de reprise.

Aucune branche fusionnée. Master, Mafiamille, Argenta et audio31 ne sont pas
modifiés. La liste des fichiers figure dans `FICHIERS_MODIFIES.txt`.
Les diagnostics d'échec des anciennes versions du pilote sont archivés hors
Git ; les rapports finaux de recette correspondent aux tests réussis.

## Points restants

**Bloquant fonctionnel constaté : aucun dans la recette décrite.**

**Non bloquants / validations humaines :** équilibrage à essayer avec stratégie
et objets ; écoute du son Morphing dans le mixage privé ; appréciation artistique
des raccords. Les tests automatisés ne sont pas une écoute humaine. L'aventure
entière depuis le starter, les voyages Sevii et toutes les interactions possibles
avec chaque attaque ne sont pas revendiqués comme parcourus.
