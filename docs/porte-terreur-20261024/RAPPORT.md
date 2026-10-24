# Porte coulissante : prototype dans le jeu

La première pose représente une porte **complètement fermée** : panneau opaque crème et or couvrant toute l'ouverture, liseré vert décoratif autour du cadre, aucune fente de portail blanc. Le sprite visible mesure 26 pixels de haut, contre 19 pour Nathan.

[Aperçu mGBA ×3](public/ouverture-fondu-mgba-x3.gif) — [porte fermée](public/fermee-x3.png) — [panneau en cours de coulissement](public/coulissement-x3.png) — [porte ouverte](public/ouverte-x3.png) — [fondu blanc](public/fondu-blanc-x3.png).

L'interaction par A crée un panneau temporaire reprenant exactement les mêmes tuiles que le panneau fermé. Le moteur le translate vers la droite de 16 pixels, un pixel toutes les deux images, devant un cadre fixe. Après l'ouverture, il lance un fondu blanc sur toutes les palettes. Le panneau temporaire est détruit et la porte réinitialisée sous le blanc, puis le script appelant reprend. La destination reste à définir : aucun warp n'est ajouté.

Le script de démonstration attend brièvement sur le blanc puis revient à la même scène, libère les commandes et permet une nouvelle ouverture. Aucun événement de carte permanent ne référence cette porte : l'emplacement à Bourg Palette est préparé uniquement dans la RAM de l'émulateur. Le script d'interaction, la ressource et le special sont disponibles pour une intégration ultérieure.

## Vérification ciblée

Compilation publique réussie. La capture provient de mGBA, sans montage du sprite sur le décor ni injection des positions intermédiaires ou du fondu. Le banc remplace temporairement un modèle d'acteur de carte, place le joueur devant la porte, et l'ouvre par une vraie pression sur A.

Contrôles : tuiles de porte fermée inchangées avant interaction ; tentative de déplacement bloquée devant son acteur ; coulissement natif observé de 0 à 16 pixels ; image uniformément blanche et toutes les palettes matérielles égales à `0x7FFF` ; coordonnées et carte du joueur inchangées ; retour à la pose fermée ; reprise des commandes ; panneau temporaire détruit ; seconde ouverture réussie. [Résultats et empreinte de la ROM de démonstration](public/TEST.json).

Les captures fermée / intermédiaire / ouverte ont été inspectées visuellement. Cet essai valide le prototype à Bourg Palette, sans encore tester une destination ou l'intégrer à un chapitre. Aucune sauvegarde utilisateur chargée, aucune musique modifiée, aucune ROM publiée, aucune fusion sur master.

Sources : `src/porte_terreur.c`, `data/scripts/porte_terreur.inc`, `graphics/yokai_characters/porte_terreur/`. Conversion : `python tools/yokai/convertir_porte_terreur.py`. Après compilation, capture : `python tools/yokai/capturer_porte_terreur_mgba.py`.
