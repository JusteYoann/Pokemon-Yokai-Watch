# Mafiamille — chantier autorisé

Base : `6f143452a026a41c08f1db38f9809959809a31b6`. Branche :
`feature/mafiamille-kanto`. Mandat : [autorisation du créateur](MANDAT.md).

La branche audio 31 OST reste indépendante et intacte à `837bd1757`.
La présente branche conserve les 26 OST de sa base. Aucune fusion.

Les marches de Don Morléone et du sbire classique sont intégrées et
**définitivement validées par le créateur**, sans modification supplémentaire.
Le chapeau approuvé remplace les R du Casino et du repaire. L’entrepôt a un mur
restauré sans emblème. Probabilités, gains, équipes, événements et musiques
inchangés. [Clôture graphique et captures mGBA](../../QA_RECETTE_FINALE/MAFIAMILLE_KANTO/finalisation/README.md).

Suivi et preuves : `QA_RECETTE_FINALE/MAFIAMILLE_KANTO/`.

## Corrections de cadrage constatées en mGBA

- La liste de sélection du Memorydex ne laisse que56pixels après le curseur.
  Elle affiche « Morléone » ; les notices compatibles gardent « Don Morléone ».
- Les deux nouveaux noms de lieux dépassaient le bandeau d’entrée de104pixels
  en police normale. Seuls ces deux bandeaux utilisent la petite police native,
  avec le nom complet. Les autres lieux gardent leur police et leur présentation.
- Les anciens identifiants de portraits Rocket/Giovanni renvoient aussi aux
  nouvelles images et palettes, pour les chemins de compatibilité et de
  classes de la Tour des Dresseurs. Aucun combat ou adversaire n’est ajouté.

## Livraison

[Bilan complet et limites de la recette](../../QA_RECETTE_FINALE/MAFIAMILLE_KANTO/BILAN.md).
