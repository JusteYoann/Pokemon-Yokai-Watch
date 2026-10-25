# Placement de l’entrepôt et nom du Short Oni

Le Mafiamille devant la console de l’entrepôt de l’Île 5 est déplacé de (27,16) à **(27,17)**. Le joueur se place juste en dessous, en **(27,18)**. Les deux cases sont praticables ; la collision empêche de traverser le personnage. Le combat a été gagné dans mGBA, et les deux flèches (26,20) et (27,20) sont bien activées après sa défaite.

Le **SHORT ONI** conservait une fiche provisoire « ???????? » et ITEM_NONE à l’index 53. Sa fiche utilise désormais ITEM_SHORT_ONI, le nom **SHORT ONI** et une description de son effet. La remise par Alizon, son affichage dans le Sac, son équipement et son retrait ont été vérifiés avec les fonctions natives.

- [Placement corrigé dans le jeu](placement-corrige-mgba-x3.png)
- [Remise du SHORT ONI](short-oni-remise-mgba-x3.png)
- [SHORT ONI dans le Sac](short-oni-sac-mgba-x3.png)
- [Bilan des vérifications des cinématiques](../verification-cinematiques-20261025/RAPPORT.md)
- [ROM mise à jour](Pokemon_Yokai_Watch_Beta_0.1_Short_Oni_Entrepot.gba)

Les tests utilisent des parties isolées ; le combat de vérification emploie une équipe niveau 100. Aucune sauvegarde utilisateur n’est modifiée. Empreinte de la ROM dans SHA256.txt ; résultats dans VERIFICATION.json et VERIFICATION_SHORT_ONI.json.
