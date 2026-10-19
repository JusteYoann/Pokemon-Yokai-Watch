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

## Intégration et limites

302 profils individuels sont calculés depuis les contours de chaque maquette : échelle propre à chaque dessin, centre horizontal et ancrage vertical. Les formes gardent leur rapport largeur/hauteur. Le cadrage des dos suit le haut du sujet, avec un bas de corps masqué au premier plan lorsque nécessaire. Aucun retournement d'axe.

`AJUSTEMENTS_302.csv` et `.json` donnent les coordonnées demandées, le gabarit source, les paramètres retenus et les limites par vue. **86 références de face demandent un agrandissement incompatible avec le carré natif 64×64 en conservant le rapport du dessin récent.** Leur échelle est bornée pour garder toute la silhouette ; elles ne reproduisent donc pas exactement la maquette. Exemple : Robonyan28 demande environ91×62 pixels, contre64 pixels de largeur disponibles. Modifier le système de sprites pour dépasser64px demanderait une autre intervention et des régressions sur les masques et animations. Ce chantier ne modifie pas ce système.

Les maquettes de Robonyan28, Brumette, Tryptik et Turboss, notamment, n'ont pas exactement le même dessin que les dernières ressources : les dessins récents sont conservés. Les palettes normales et shiny sont inchangées. Les cinq dessins shiny indépendants (019,099,100,101,126) ont leurs dérivés de cadrage adaptés ; leurs dessins originaux restent intacts.

## Vérifications réalisées

- Compilation réussie avec26 OST privées existantes :31 290 807octets, soit29,841Mio, sous32Mio. EWRAM261052octets et IWRAM29888octets ; pas de coût RAM ajouté par les profils calculés à la compilation.
- `apres/` :151 nouvelles captures mGBA de la compilation corrigée ;302 tampons graphiques et palettes normales vérifiés contre les ressources liées. Aucun sprite vide.
- `comparaisons/comparatif-01.png` à `comparatif-19.png` :151 triptyques **maquette / capture avant / capture après**. Les colonnes mGBA viennent du moteur, pas d'un montage des sprites sur un décor.
- Les19 planches comparatives ont été examinées visuellement. Les limites64px et les différences de dessin restent visibles et ne sont pas présentées comme une égalité artistique parfaite.
- Les fichiers sources de gameplay, d'audio et d'overworld sont préservés. Seuls les profils, les liens vers leurs dérivés et les décalages de présentation changent.

Tests shiny et régression d'animations : rapport complémentaire à la fin du chantier. Une capture au menu de combat ne prouve pas toutes les animations, ni une aventure complète.

## Reproduction

Environnement de compilation habituel, ressources audio privées fournies séparément :

```sh
source /workspace/.setup/env.sh
python3 tools/yokai/appliquer_cadrage_definitif_151.py
make -j4 YOKAI_AUDIO_DIR=/chemin/vers/audio-prive
YOKAI_QA_ROM=$PWD/pokefirered_audio.gba YOKAI_QA_ELF=$PWD/pokefirered_audio.elf python3 tools/yokai/preparer_cadrage_definitif_151.py --stage apres --capture
python3 tools/yokai/comparer_cadrage_definitif_151.py
YOKAI_QA_ROM=$PWD/pokefirered_audio.gba YOKAI_QA_ELF=$PWD/pokefirered_audio.elf python3 tools/yokai/verifier_cadrage_151_mgba.py
```

La sauvegarde `ETAT_AVANT.json` est protégée contre une réécriture accidentelle. Les sorties après peuvent être actualisées explicitement. Aucun fichier ROM ou audio n'est publié.
