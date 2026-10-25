# Couleurs de Don Morléone : repaire et Yopple

## Résultat

L’arrivée normale au repaire par la sortie de l’ascenseur, puis la marche jusqu’à Don Morléone, produit un affichage correct. Nathan se place sur le sol à (19, 5), face à Don ; la conversation et le combat se déroulent normalement. Les bandes de décor de la compilation provenaient de la préparation de sa prise par chargement direct et mauvaise position, pas de cette entrée du jeu. Le test comporte 24 déplacements réels depuis l’ascenseur.

La palette de Don au repaire était déjà correcte. Chez Yopple, les employés écrasaient la palette partagée par Don et la Mafiamille. La correction isole la Mafiamille dans la banque 6, tandis que Domniscian et ses employés conservent la banque 10. Elle s’applique au chargement, aux changements de graphismes et à la reconstruction des sprites. Les autres cartes conservent leur affectation de palettes.

## Vérification mGBA

- Repaire : sortie réelle de l’ascenseur, marche jusqu’au bureau, interaction avec A et victoire native. Palette correcte sur les 1 252 images de scène observées ; capture de l’approche jointe.
- Yopple : entrée réelle par le téléporteur du 7e étage, marche de 19 déplacements, déclenchement par la case prévue et victoire native. Palette correcte sur les 1 158 images de scène observées, y compris au retour du combat.
- Ordres opposés de rechargement de Don et des deux employés : couleurs propres à chaque groupe conservées. Reconstruction du terrain et des sprites vérifiée.
- Après le combat, Don est retiré et Domniscian ainsi que ses employés conservent leurs propres couleurs.

Les parties sont isolées ; les prérequis de portes/sbires déjà vaincus et une équipe niveau 100 sont préparés. Les entrées, déplacements, interactions et combats utilisent les commandes du jeu. Aucun résultat, palette, graphisme ni caméra n’est imposé pendant ces scènes. Les rechargements de sprites constituent des contrôles techniques séparés, décrits dans le script de test.

[Repaire : approche normale](RocketHideout_B4F-approche.png) · [Yopple : avant](SilphCo_11F-avant.png) · [Yopple : couleurs corrigées](SilphCo_11F-approche.png)

[ROM corrigée](Pokemon_Yokai_Watch_Beta_0.1_Morleone_Couleurs.gba) · [Tests](TESTS_MGBA.json) · [Empreinte](COMPILATION.json)

Aucune nouvelle vidéo ni modification de la compilation existante.
