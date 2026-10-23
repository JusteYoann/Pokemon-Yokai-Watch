# Sprites corrigés par l’utilisateur

Les deux PNG de `Nouveau dossier (3).rar` remplacent les versions précédentes de Juste Yoann. Les fichiers reçus sont archivés inchangés dans `graphics/juste_yoann/source/corrections-utilisateur-20261024/` : `battle.png` et `overworld.png` (ce dernier nommé `dgvd).png` dans l’archive).

Ils ont déjà les dimensions natives 64×64 et 32×32 et partagent 12 couleurs opaques. La conversion est un **indexage sans perte** : aucun redimensionnement, recadrage, déplacement, lissage ou redessin. Les pixels opaques et l’alpha des PNG de sortie sont vérifiés identiques à ceux reçus. La palette matérielle RGB555 conserve sa précision GBA habituelle. Les sources RGBA originales restent disponibles avec leurs SHA256 dans `graphics/juste_yoann/conversion.json`.

[PNJ corrigé dans la chambre](public/chambre-corrigee-x3.png) · [Portrait corrigé en combat](public/portrait-corrige-x3.png) · [Introduction animée](public/introduction-corrigee.gif).

Les deux versions compilent. [Contrôles publics](public/TEST_MGBA.json) et [privés](prive/TEST_MGBA.json) : rendu réel du PNJ et du portrait, position et face fixes, correspondance exacte des tuiles en VRAM et de la palette chargée avec les ressources converties. L’interaction au bouton A lance le véritable événement du PNJ jusqu’au menu d’action du combat.

Ce lot ne change ni les événements, ni l’équipe, ni le cadeau. Les tests complets de quête restent documentés dans `integration/` sur leurs ROM identifiées ; les nouvelles preuves ci-dessus concernent les graphismes corrigés et possèdent leurs propres SHA256. Aucun nouveau parcours complet de quête n’est revendiqué pour cette modification graphique.

```bash
source /workspace/.setup/env.sh
python3 tools/yokai/convertir_juste_yoann.py
make -j6
make -j6 YOKAI_AUDIO_DIR=/workspace/private-audio/lavanville-integration
python3 tools/yokai/tester_yoann_sprites_corriges_mgba.py
YOKAI_QA_ROM="$PWD/pokefirered_audio.gba" python3 tools/yokai/tester_yoann_sprites_corriges_mgba.py
```
