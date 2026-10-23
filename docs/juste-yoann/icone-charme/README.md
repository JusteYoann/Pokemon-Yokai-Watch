# Icône du Charme Chroma

L’icône provisoire du Grelot Zen est remplacée par une étoile turquoise suspendue à un cordon bleu, selon la nouvelle référence de l’utilisateur.

Le sac GBA impose 24 × 24 pixels et 16 indices de palette, dont un transparent. Une déclinaison GBA existante du même objet est utilisée : ses détails sont simplifiés par rapport à l’image haute résolution du chat. Il ne s’agit pas d’une extraction pixel pour pixel de cette dernière. La provenance et le SHA256 sont consignés dans [SOURCE.json](SOURCE.json). Les pixels opaques du fichier GBA et leurs couleurs sont conservés ; l’indice de fond devient transparent.

L’icône et sa palette propres sont reliées à `ITEM_SHINY_CHARM` uniquement. La description complète est conservée : elle utilise la petite police native sans espacement supplémentaire pour éviter le débordement de la troisième ligne. Les autres objets gardent leur présentation.

[Capture publique du sac](public/charme-dans-sac-x4.png) · [Capture privée](prive/charme-dans-sac-x4.png).

Compilations publique et privée réussies. Les [tests publics](public/TEST_MGBA.json) et [privés](prive/TEST_MGBA.json) vérifient les pointeurs d’icône et palette, la largeur du texte, la présence dans la vraie poche des objets importants, le contenu chargé en VRAM et l’ouverture du menu de l’objet. Le cadeau dans l’inventaire et la sélection de poche sont des fixtures ; les graphismes de l’interface ne sont pas remplacés par le test.

Ce complément termine l’icône du charme. L’intégration du PNJ Juste Yoann et de son portrait requiert toujours le fichier original de leur référence, comme indiqué dans le rapport de quête.

```bash
source /workspace/.setup/env.sh
python3 tools/yokai/tester_charme_icone_mgba.py
YOKAI_QA_ROM="$PWD/pokefirered_audio.gba" python3 tools/yokai/tester_charme_icone_mgba.py
```
