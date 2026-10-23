# Sépia constant pendant les combats de Cramois

Demande finale retenue : **garder le sépia sur les Yo-kai pendant tout le combat**, plutôt que le retirer. Branche `feature/cramois-ile-passe`, base `61ef33372`, sans merge sur master.

Trois chemins expliquaient les changements de couleur : les Yo-kai passent de leurs sprites OBJ à des décors d'animation utilisant les palettes BG8/9 ; ces copies écrivent parfois directement dans la palette matérielle ; la validation d'une attaque réécrit également toute la palette dans `BeginNormalPaletteFade`. Ces écritures directes contournaient la conversion effectuée pendant VBlank.

La conversion couvre désormais les palettes BG8/9 et les écritures directes des deux plans d'animation. L'envoi immédiat des fondus utilise également la conversion locale. Le contexte d'affichage se fonde sur l'écran de combat actif (son callback VBlank), afin de conserver la teinte lors de changements temporaires du callback principal. Les buffers de couleurs originaux ne sont jamais recolorés : la teinte ne s'accumule pas et les effets natifs de luminosité continuent de fonctionner.

Les Yo-kai, Dresseurs et décors gardent le sépia sur l'île ; les interfaces et le Sac gardent leurs couleurs normales. Hors de Cramois, les copies et palettes natives restent inchangées. Aucun sprite, palette graphique, proportion d'Hovernyan, équipe, dialogue, donnée des 151 Yo-kai, musique ou format de sauvegarde n'est modifié.

- [GIF Charge](public/move_tackle.gif).
- [GIF Aéropique](public/move_aerial_ace.gif).
- [GIF Ball’Ombre avec changement de fond](public/move_shadow_ball.gif).
- [Yo-kai et décor sépia au repos](public/yokai-sepia-constant-x4.png).
- [Même teinte sur le plan d'animation BG1](public/copie-bg1-x4.png) et [BG2](public/copie-bg2-x4.png).
- [Sac de combat en couleurs normales](public/sac-combat-couleurs-normales-x4.png).
- [Couleurs normales hors de l'île](public/hors-ile-couleurs-normales-x4.png).

Les captures viennent de mGBA, sans simulation. Les combats filmés utilisent uniquement les touches, sans appel de diagnostic pendant l'enregistrement. Les fixtures annoncées sont une nouvelle partie, la position dans l'Arène, Jibanyan niveau 100, Hovernyan niveau 45 et le choix préalable de l'attaque. Les PV adverses et les résultats ne sont pas forcés. Chaque attaque est menée jusqu'à une véritable fin de combat et au retour sur l'île.

Les contrôles ciblés vérifient la palette matérielle image par image : OBJ0/1 et BG8/9 doivent correspondre à la même conversion sépia, avec la couleur de la trame précédente admise pour la latence normale du transfert. Ils couvrent aussi les copies natives BG1/BG2, les portraits, le Sac et son retour, le sépia de la carte et l'absence de teinte résiduelle ailleurs. Les quarante contrôles de phase A sont rejoués avec le nouveau masque de combat (les rapports historiques restent intacts).

[Tests publics](public/TEST_MGBA.json) · [Tests privés](prive/TEST_MGBA.json) · [Régressions publiques](regressions/phase-a/public/apres/TEST_MGBA.json) · [Régressions privées](regressions/phase-a/prive/apres/TEST_MGBA.json) · [Validation et mémoire](VALIDATION.json).

**54 contrôles passent dans chaque version : 14 ciblés et 40 régressions.** Les versions publique et privée compilent. EWRAM inchangée : 261368 octets, **776 libres**. IWRAM inchangée : 29824 publique, 29888 privée. Pas de ressource graphique ni d'allocation permanente supplémentaire. La couverture ne prétend pas rejouer toutes les attaques et tous les combats de la campagne ; les trois attaques choisies couvrent le transfert des Yo-kai sur les plans d'animation, les fondus, les effets de palette et un remplacement de fond. Pas de validation sur GBA physique.
