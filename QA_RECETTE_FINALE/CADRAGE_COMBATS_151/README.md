# Cadrage définitif des 151 combats

Point de restauration des dessins récents : `602bc12e26910ee751fac0565c9db0db05e2d6b5`.
Les deux archives fournies couvrent exactement les numéros 001 à 151, sans doublon.

- `references/` : maquettes utilisateur normalisées en 240×160, uniquement pour comparaison ; jamais importées comme dessins du jeu.
- `avant/` : **151 captures réelles mGBA**, action de combat atteinte, même espèce alliée/adverse, forme normale. Les 302 tampons graphiques décompressés et les palettes ont été comparés aux ressources actives. Le JSON conserve ROM, empreinte et positions natives.
- `sources/ETAT_AVANT.json` : empreintes des PNG originaux, palettes et ressources natives avant correction.
- `sources/sprite_presentation.json` et tables de coordonnées : sauvegarde du cadrage précédent.

Les maquettes peuvent contenir des dessins anciens ou une orientation accidentelle. Seuls leur cadrage et leurs proportions servent de guide. Les dessins, palettes et orientations récents restent la référence.

Les mesures automatiques des contours dans `MESURES_REFERENCES_BRUTES.json` sont des guides géométriques, pas une validation artistique. La limite actuelle est une tuile de combat de 64×64 pixels par combattant ; certaines maquettes la dépassent. Ces écarts devront être documentés individuellement.

État de ce premier jalon : références et captures avant sauvegardées ; corrections et captures après en cours. Aucun résultat après ne doit être déduit des images avant.
