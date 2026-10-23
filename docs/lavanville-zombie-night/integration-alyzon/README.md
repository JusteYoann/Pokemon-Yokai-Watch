# Intégration graphique d'Alyzon Bie

La planche overworld et le portrait de combat retrouvés sur `codex/reprise-scenario-2026-10-22` sont désormais enregistrés dans le moteur de la branche `feature/lavanville-zombie-night`. Les ressources proviennent du commit source `2647bc1627050f193cc9606f8c0f5f1151986047`. Une correction est appliquée à la seule pose latérale n° 7 : son orientation était opposée à celles des poses 2 et 8, ce qui faisait se retourner Alyzon pendant un pas. Cette pose est retournée horizontalement dans sa boîte occupée, sans déplacer son emplacement, changer sa palette ou redessiner ses pixels. Les huit autres poses et le portrait restent inchangés. Les animations standard du jeu restent intactes.

## Ressources actives et identifiants

| Ressource | Fichier | Enregistrement |
|---|---|---|
| Déplacements | `graphics/yokai_characters/alyzon/overworld.png` | `OBJ_EVENT_GFX_YOKAI_ALYZON` **173** |
| Palette carte | `graphics/yokai_characters/alyzon/overworld.pal` | Tag **0x112B**, banque OBJ **7** |
| Portrait combat | `graphics/yokai_characters/alyzon/battle.png` | `TRAINER_PIC_YOKAI_ALYZON` **160** |
| Palette combat | `graphics/yokai_characters/alyzon/normal.pal` | Table native des portraits |

Neuf images 16 × 32, 256 octets chacune : face au repos (0), dos (1), profil (2), deux pas de face (3/4), de dos (5/6), de profil (7/8). La droite utilise le miroir horizontal prévu par le jeu et par la planche retrouvée. Le portrait est 64 × 64, décompressé à 2 048 octets. Les indices libres de la branche actuelle sont utilisés ; les anciens numéros de la branche scénario ne sont pas recopiés.

La palette carte est chargée à l'apparition, au changement d'identifiant graphique, à la création d'un objet virtuel et lors du retour au terrain. Elle occupe une banque distincte de Nathan (0), Matt dans les scènes existantes d'Argenta/Ligue (6) et Don (10). La banque 7 est réservée à Alyzon dans les scènes qui l'utilisent ; c'est normalement la banque de reflet du deuxième PNJ. Une future scène avec des reflets d'eau concurrents devra tenir compte de cette réservation. La restauration de palette utilise le tag d'Alyzon tant que son objet est actif. Aucun état persistant ni espace EWRAM supplémentaire n'est ajouté.

## Compilation et contrôles

| Version | Taille de la ROM | SHA-256 |
|---|---:|---|
| Publique | 16 777 216 octets | `5957c9178727e33d24849dc517a17f5e86d15c66d373f102ab85ff008b826807` |
| Privée, ressources audio existantes | 31 659 467 octets | `840408d401db979bbc7f06b41fbda8724f1e91ba2686c2bda6c78c613fc06f40` |

Limite : 33 554 432 octets. Marge privée : **1 894 965 octets**. EWRAM : **261 128 octets**, identique au socle. IWRAM publique/privée : **29 824 / 29 888 octets**, identique au socle. Les sources musicales ne sont pas modifiées.

Dans chaque version, 18 vérifications natives mGBA passent :

- Présence des données retenues et corrigées dans la ROM et cohérence des références d'identifiants, données graphiques et palette.
- Douze déplacements natifs, trois par direction : coordonnées d'arrivée, neuf frames observées en VRAM, contrôle du miroir à chaque frame (gauche sans miroir, droite avec miroir) et stabilité de la palette.
- Changement d'identifiant graphique vers un autre PNJ puis retour à Alyzon.
- Retour au terrain par `CB2_ReturnToField`, avec reconstruction native des sprites et de la palette.
- Création d'un objet virtuel à partir de l'identifiant enregistré.
- Cohabitation avec Matt et Don : contrôle des trois banques, y compris après rechargement d'Alyzon ; la palette du joueur et celles des PNJ standards sont aussi contrôlées à l'apparition.
- Chargement du portrait par `DecompressTrainerFrontPic`, création du sprite avec le modèle natif de combat, vérification de ses données VRAM, de son animation et de sa palette.

Les images et palettes ne sont pas remplacées par des données injectées en RAM durant ces tests. Les positions de démonstration et le décor de combat sont des fixtures RAM. Pour le portrait, le chargeur natif reçoit l'identifiant 160 dans le contexte d'une ouverture de combat existante ; aucun nouveau combat/nom/équipe d'Alyzon n'est inventé ou assigné.

Preuves :

- [Marche publique](public/marche-enregistree-mgba.gif) et [marche privée](prive/marche-enregistree-mgba.gif).
- [Portrait dans le moteur de combat](public/portrait-charge-moteur-x3.png).
- [Alyzon avec Matt, Don et Nathan](public/palettes-alyzon-matt-don-x3.png).
- [Contrôles publics](public/TEST_MGBA.json) et [privés](prive/TEST_MGBA.json).

## Protection du projet et prochaine étape

Aucun changement de carte, dialogue, équipe, espèce, statistique, arène, badge, progression, scénario ou musique. Les branches audio, Mafiamille et boss final ne sont pas modifiées ou fusionnées. Les essais artistiques précédents restent archivés mais ne sont pas les ressources enregistrées d'Alyzon. Le portrait et l'identifiant de carte sont disponibles pour les prochains scripts.

La cinématique et le placement permanent d'Alyzon restent la prochaine étape. Aucun événement de l'ancienne refonte scénaristique n'est repris automatiquement. La qualité du raccord narratif, les dialogues, l'équipe et les déclencheurs ne sont pas validés par cet audit graphique.

Commandes de reproduction (ressources privées nécessaires uniquement pour le deuxième mode) :

```
make -j6
make -j6 YOKAI_AUDIO_DIR=/workspace/private-audio/argenta-integration
YOKAI_QA_ROM=$PWD/pokefirered.gba python tools/yokai/verifier_alyzon_integration_mgba.py
YOKAI_QA_ROM=$PWD/pokefirered_audio.gba python tools/yokai/verifier_alyzon_integration_mgba.py
```
