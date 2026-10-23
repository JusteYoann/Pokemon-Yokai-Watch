# Enma : taille et position en combat

Le montage fourni fixe deux cadrages distincts : Enma adverse est agrandi et remonté ; Enma de dos est davantage agrandi, avec le bas du corps derrière la boîte de dialogue.

| Vue | Centre en combat simple | Agrandissement uniforme | Silhouette complète |
|---|---|---|---|
| Face adverse | `(170, 36)` | `256/225`, environ 114 % | 70 × 65 px |
| Dos joueur | `(78, 97)` | `256/170`, environ 151 % | 83 × 87 px avant masquage par l’interface |

Le dessin, les couleurs, les PNG sources et les textures indexées restent inchangés. Seule la géométrie de l’espèce nº150 évolue, via le mécanisme existant qui applique la même présentation aux sprites GBA et à leur silhouette copiée sur un fond pendant certaines animations. Les autres espèces et le portrait de Domniscian ne sont pas modifiés. Les paramètres sont enregistrés dans `data/yokai/battle_geometry_overrides.json` et dans la table générée correspondante.

[Capture mGBA publique](public/placement-face-dos-x4.png) · [Animation publique](public/combat-placement.gif) · [Capture privée](prive/placement-face-dos-x4.png) · [Animation privée](prive/combat-placement.gif).

## Vérification

Les versions publique et privée compilent. [Résultats publics](public/TEST_MGBA.json) et [privés](prive/TEST_MGBA.json), chacun avec SHA256 de la ROM testée :

- Centres, textures originales et matrices matérielles uniformes vérifiés pour les deux vues dans un véritable combat mGBA.
- Copies natives des deux silhouettes d’animation vérifiées pixel par pixel ; occupation de 2592 et 3872 octets, dans la limite existante de 4096 octets.
- Une attaque offensive réelle jouée au contrôleur inflige des dégâts puis revient au menu d’action ; les deux vues conservent leur agrandissement après l’animation.

Le lieu, les équipes et les capacités du joueur sont des fixtures de test. Le test ne modifie ni les sprites affichés, ni les PV adverses, ni le résultat du combat. Il ne constitue pas une recette complète du jeu.

```bash
source /workspace/.setup/env.sh
make -j6
make -j6 YOKAI_AUDIO_DIR=/workspace/private-audio/lavanville-integration
python3 tools/yokai/tester_enma_placement_mgba.py
YOKAI_QA_ROM="$PWD/pokefirered_audio.gba" python3 tools/yokai/tester_enma_placement_mgba.py
```
