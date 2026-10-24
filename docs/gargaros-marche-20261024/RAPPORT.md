# Gargaros : aperçu de marche dans le jeu

Gargaros sans massue, issu de la planche générée montrée dans le chat. Conversion native sans redessiner les formes : découpe des douze poses, réduction au plus proche voisin, palette commune de 15 couleurs opaques et une transparence. Chaque image occupe une case de 32 × 32 pixels ; la silhouette visible mesure 22 pixels de haut, comme Orqanos, et les pieds partagent sa ligne de base.

Les douze poses sont conservées : deux pas et un repos pour la face, le dos, la gauche et la droite. Les animations utilisent leurs images propres, sans retourner les profils. Le sprite est enregistré sous un nouvel identifiant graphique ; aucun personnage existant n'est remplacé et aucun événement de carte ou rôle scénaristique n'est ajouté.

## Aperçus

- [Marche dans mGBA, agrandie ×3](public/marche-mgba-x3.gif).
- [Marche à la résolution native](public/marche-mgba.gif).
- [Comparaison avec Nathan et Orqanos](public/comparaison-orqanos-nathan-x3.png).
- [Planche native transparente](planche-native.png) et [agrandissement ×6](planche-x6.png).

La scène à Bourg Palette utilise deux acteurs temporaires créés par le banc de démonstration. Gargaros traverse réellement les cases par les actions normales du moteur, sur un rectangle de douze pas ; les images ne sont pas collées sur une capture et la marche n'est pas une simple animation sur place. Nathan et Orqanos restent visibles pour le gabarit. Aucun fichier de sauvegarde utilisateur n'est chargé ou modifié.

## Correction du cadrage

Le premier GIF publié ne montrait pas Gargaros : le banc lui avait transmis des coordonnées sans le décalage interne de sept cases, puis commencé l'enregistrement alors qu'il était hors champ. Le déplacement en mémoire et les images en VRAM étaient valides ; ce contrôle ne suffisait pas à vérifier la vidéo livrée.

Le placement est corrigé et le trajet tient entièrement dans la vue. Chacune des 156 captures vérifie maintenant les indicateurs de visibilité, le rectangle écran complet du sprite et la présence effective de ses pixels rouges dans le rendu. Le contrôle confirme aussi au moins 48 pixels de déplacement horizontal. Les images du GIF réencodé ont été inspectées visuellement.

## Vérification ciblée

Compilation publique réussie. Dans mGBA : douze images 4bpp chargées, palettes de Gargaros et Orqanos distinctes et vérifiées, déplacement réel d'une case à chaque action, trois images observées dans chaque direction et aucune image d'une autre direction pendant son cycle. Le contrôle des tuiles commence après les deux premières images de transfert au changement de direction ; toutes les images capturées restent dans la vidéo. [Résultats et empreinte de la ROM de démonstration](public/TEST.json).

Le GIF contient 156 captures du moteur. Seul l'agrandissement au plus proche voisin est appliqué à la version ×3. Cet essai ne valide pas une nouvelle scène d'aventure. Aucune ROM n'est publiée et master reste inchangé.

Pour reproduire, compiler puis lancer `python tools/yokai/capturer_gargaros_marche_mgba.py` dans l'environnement du projet. L'illustration source et les paramètres de conversion se trouvent dans `graphics/yokai_characters/gargaros/` ; `tools/yokai/convertir_gargaros.py` régénère les fichiers natifs.
