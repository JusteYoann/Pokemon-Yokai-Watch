# Salle de Maître Nyada et taille de Domniscian

La quête Maître Nyada/Démophage a été déplacée du couloir nord-ouest vers la grande salle sud du premier étage de la Grotte Azurée. Maître Nyada se trouve en (20,19), Démophage en (25,19), sur le même sol d’altitude 4. L’équipe peut atteindre et contourner les deux personnages depuis le palier relié à l’échelle. Leurs sprites disposent de quatre rangées de sol dégagé et restent éloignés du décor bloquant. Aucun contenu de carte n’a été supprimé.

La mauvaise couleur venait des deux palettes différentes chargées dans la même banque OBJ 7. Maître Nyada utilise désormais la banque 6 dans cette carte, Démophage conserve la 7. Les palettes sont chargées uniquement dans la banque attribuée : reconstruire un acteur ne recolore plus l’autre. Les apparitions de Maître Nyada sur les autres cartes restent sur leurs emplacements habituels.

Domniscian conserve les trois vues debout de la planche fournie, ramenées à la même hauteur visible que Maître Nyada : **19 pixels**, avec une ligne des pieds commune. La palette partagée et le portrait de combat sont conservés. Le sprite est commun à toutes ses apparitions, et les deux photos de groupe ont été recapturées dans mGBA avec cette taille.

## Vérifications

- [Scène native](TESTS_SCENE.json) : Nathan et Katie atteignent les deux PNJ par déplacement manette depuis le palier ; sol, altitude et emprise des sprites contrôlés ; palettes exactes et distinctes ; reconstruction de chaque acteur, retour terrain puis victoire native contre Démophage ; couleurs conservées après le combat, cadeaux et fin de quête.
- [Domniscian](DOMNISCIAN_MGBA.json) : ressource native vérifiée à l’Arène, dans Yopple et pour la revanche ; musique **Vs Hinozall** conservée dans les deux combats d’Arène.
- [Crédits et retour postgame](TESTS_MGBA.json) : 32 scènes pour les deux protagonistes, nouvelle photo 28 et photo finale vérifiées dans la VRAM, retour blanc devant Juste Yoann, Charme Chroma unique et sauvegarde/reprise. Crédits ordinaires de la Ligue également vérifiés.

Ces vérifications utilisent des parties de test préparées ; elles sont distinctes de l’aventure normale filmée. La vérification de la scène a précédé le réencodage final des photos ; les vérifications Domniscian et crédits portent sur la ROM finale. Les empreintes exactes figurent dans chaque rapport.

[Photo 28 — Nathan](garcon-28-native.png) · [Photo finale — Nathan](groupe/garcon/32.png) · [ROM](Pokemon_Yokai_Watch_Beta_0.1_Postgame_Sprites.gba) · [Compilation](COMPILATION.json).

Branche dédiée, aucune fusion sur master. Aucun format de sauvegarde n’a été modifié et aucune sauvegarde utilisateur n’a été ouverte.
