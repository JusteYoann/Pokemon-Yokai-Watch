# Laure, Marge et Agent X — brouillons de face

Les références des cinq personnages demandés sont désormais disponibles dans la conversation : les deux sœurs, Agent X, Perpétua et McKraken. Aucun nouveau fichier de référence n’est nécessaire pour comprendre leur apparence.

- [Premières propositions de face](faces-proposition.png) : sœur dorée/rouge, sœur argentée/turquoise, Agent X. La disposition de l’artwork est conservée sans déduire ici l’attribution individuelle des noms.
- [Essai simplifié d’Agent X](agent-x-essai-simplifie.png).

Ces deux dessins ont été réellement créés avec l’outil graphique. **Ce ne sont pas des sprites natifs terminés.** Le premier comporte encore trop de pixels et de détail pour le gabarit de Nathan. Le second simplifie la silhouette mais conserve une grille irrégulière et des textures dans les aplats. Une simple réduction donnerait une ressource approximative. Aucune extraction ni réduction automatique n’a donc été mise dans le jeu.

## Limite constatée et méthode de reprise

L’outil de génération ne maintient pas fidèlement les cellules du gabarit fourni, même après un essai réduit à un seul personnage. Il faut reprendre ces dessins dans un éditeur à résolution native (Aseprite ou LibreSprite), sur une cellule de 16 × 32 : silhouette de 19 pixels de haut comme Nathan, pieds à y=30, 15 couleurs visibles au maximum et indice 0 transparent. Dessiner d’abord face/dos/profil, puis de vrais pas alternés, contrôler le miroir est et exporter la planche indexée dans l’ordre du moteur. Le portrait de combat est une autre ressource et reste à produire.

Il faut conserver les coiffures, bijoux et vêtements distinctifs des sœurs et le chapeau, les cheveux verts, le visage mauve et la cravate d’Agent X, en simplifiant les détails qui ne tiennent pas à cette taille.

Aucune palette active, donnée de gameplay, carte, animation ou musique n’a changé. Aucune nouvelle compilation ni validation mGBA ne s’impose pour ces seules propositions hors moteur ; aucun test en jeu n’est revendiqué.
