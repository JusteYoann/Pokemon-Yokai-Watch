# Cadrage définitif des 151 combats

Point de restauration des dessins récents : `602bc12e26910ee751fac0565c9db0db05e2d6b5`.
Les deux archives fournies couvrent exactement les numéros 001 à 151, sans doublon.

- `references/` : maquettes utilisateur normalisées en 240×160, uniquement pour comparaison ; jamais importées comme dessins du jeu.
- `avant/` : **151 captures réelles mGBA**, action de combat atteinte, même espèce alliée/adverse, forme normale. Les 302 tampons graphiques décompressés et les palettes ont été comparés aux ressources actives. Le JSON conserve ROM, empreinte et positions natives.
- `sources/ETAT_AVANT.json` : empreintes des PNG originaux, palettes et ressources natives avant correction.
- `sources/sprite_presentation.json` et tables de coordonnées : sauvegarde du cadrage précédent.

Les maquettes peuvent contenir des dessins anciens ou une orientation accidentelle. Seuls leur cadrage et leurs proportions servent de guide. Les dessins, palettes et orientations récents restent la référence.

Les mesures automatiques des contours dans `MESURES_REFERENCES_BRUTES.json` sont des guides géométriques, pas une validation artistique. La limite actuelle est une tuile de combat de 64×64 pixels par combattant ; certaines maquettes la dépassent. Ces écarts devront être documentés individuellement.

État : cadrages intégrés, captures avant/après disponibles, contrôles techniques terminés avec les réserves artistiques détaillées ci-dessous.

## Intégration et limites

302 profils individuels sont calculés depuis les contours de chaque maquette : échelle propre à chaque dessin, centre horizontal et ancrage vertical. Les formes gardent leur rapport largeur/hauteur. Le cadrage des dos suit le haut du sujet, avec un bas de corps masqué au premier plan lorsque nécessaire. Aucun retournement d'axe.

`AJUSTEMENTS_302.csv` et `.json` donnent les coordonnées demandées, le gabarit source, les paramètres retenus et les limites par vue. **86 références de face demandent un agrandissement incompatible avec le carré natif 64×64 en conservant le rapport du dessin récent.** Leur échelle est bornée pour garder toute la silhouette ; elles ne reproduisent donc pas exactement la maquette. Exemple : Robonyan28 demande environ91×62 pixels, contre64 pixels de largeur disponibles. Modifier le système de sprites pour dépasser64px demanderait une autre intervention et des régressions sur les masques et animations. Ce chantier ne modifie pas ce système.

Les maquettes de Robonyan28, Brumette, Tryptik et Turboss, notamment, n'ont pas exactement le même dessin que les dernières ressources : les dessins récents sont conservés. Les dessins et palettes normaux sont inchangés. Après la dernière décision utilisateur, les cinq dessins shiny indépendants (019,099,100,101,126) sont **retirés des ressources actives**, tout en conservant des variantes de couleur sur les silhouettes normales. Voir le détail ci-dessous.

## Vérifications réalisées

- Compilation réussie avec26 OST privées existantes :31 281 611octets, soit29,832Mio, sous32Mio. EWRAM261052octets et IWRAM29888octets ; pas de coût RAM ajouté par les profils calculés à la compilation.
- `apres/` :151 nouvelles captures mGBA de la compilation corrigée ;302 tampons graphiques et palettes normales vérifiés contre les ressources liées. Aucun sprite vide.
- `comparaisons/comparatif-01.png` à `comparatif-19.png` :151 triptyques **maquette / capture avant / capture après**. Les colonnes mGBA viennent du moteur, pas d'un montage des sprites sur un décor.
- Les19 planches comparatives ont été examinées visuellement. Les limites64px et les différences de dessin restent visibles et ne sont pas présentées comme une égalité artistique parfaite.
- Les fichiers sources de gameplay, d'audio et d'overworld sont préservés. Seuls les profils, les liens vers leurs dérivés et les décalages de présentation changent.

- `shiny/TEST_MGBA.json` :151 combats supplémentaires avec une demande shiny ;84 espèces conservent ce statut,67 le refusent. Pour les deux camps, le tampon graphique est identique à celui de la forme normale ; la palette native attendue est vérifiée.151 captures et19 planches normal/shiny.
- `interfaces-couleurs-seules/` :20 captures réelles PC/résumé pour les cinq espèces retirées, formes normale/shiny ;20 chargements génériques face/dos comparés aux mêmes ressources normales.30 contrôles consignés.
- `animations/` :28 cas natifs, sept scripts (106,107,151,211,232,293,334), deux côtés, normal/shiny. Tous se terminent et restaurent tuiles/palettes, sans erreur. Les planches Armure et Griffe Acier ont été examinées ; ces essais ne valident pas visuellement toutes les attaques ni toutes les silhouettes.

Ces tests utilisent une vraie initialisation de nouvelle partie puis des fixtures explicites d'équipe et de combat ; ils ne constituent pas un parcours complet de l'aventure.

## Décision finale : shiny par couleurs uniquement

Confirmation utilisateur : «Retirer les dessins dédiés, conserver les variantes de couleur».

- 019 Robonyan28,099 Coach Antonic,100 Usapyon,101 Emperor et126 Jojojoyeux utilisent désormais leurs pixels normaux, de face et de dos, y compris PC/résumé/autres chemins de chargement.
- Les dix bitmaps spécifiques ne sont plus liés à la ROM ; le hook de compatibilité retourne toujoursFALSE et ne remplace aucun pixel. Les PNG historiques restent dans le dépôt pour restauration, sans rôle actif.
- Cinq palettes shiny ont été réindexées pour les indices des sprites normaux, en réutilisant uniquement des couleurs de leurs palettes précédentes. Une palette destinée à un autre dessin ne pouvait pas être appliquée telle quelle. Les correspondances complètes et anciennes couleurs sont dans `data/yokai/shiny_artwork_policy.json`.
- Robonyan28 garde des tons sombres et dorés, Coach Antonic un vêtement turquoise, Usapyon des couleurs proches de ses couleurs habituelles, Emperor une combinaison dorée et Jojojoyeux des tons gris/noir/blanc. Les cornes supplémentaires, vêtements redessinés, cape et expressions spécifiques sont supprimés avec leurs dessins ; une palette ne recrée pas ces formes.
- Les151 palettes normales,146 autres palettes shiny,302 PNG normaux,éligibilité84/67,gameplay,overworld et audio sont inchangés. Les convertisseurs historiques refusent de réactiver les dessins retirés.
- Les planches comparatives ont été régénérées après ce changement.

ROM privée testée :SHA-256 `a65eb4c0fb5a73762fed444a43edff16fd9b9be9e7d7c418b52c213dab2c7e75`. Aucun fichier ROM/audio n'est publié.

**Bilan : contrôles techniques réussis ; rapprochement artistique avec réserves64×64 et dessins récents différents des anciennes maquettes. Pas une certification de fin du jeu.**

## Reproduction

Environnement de compilation habituel, ressources audio privées fournies séparément :

```sh
source /workspace/.setup/env.sh
python3 tools/yokai/appliquer_shiny_couleurs_seules.py
python3 tools/yokai/appliquer_cadrage_definitif_151.py
make -j4 YOKAI_AUDIO_DIR=/chemin/vers/audio-prive
YOKAI_QA_ROM=$PWD/pokefirered_audio.gba YOKAI_QA_ELF=$PWD/pokefirered_audio.elf python3 tools/yokai/preparer_cadrage_definitif_151.py --stage apres --capture
python3 tools/yokai/comparer_cadrage_definitif_151.py
YOKAI_QA_ROM=$PWD/pokefirered_audio.gba YOKAI_QA_ELF=$PWD/pokefirered_audio.elf python3 tools/yokai/verifier_cadrage_151_mgba.py
```

La sauvegarde `ETAT_AVANT.json` est protégée contre une réécriture accidentelle. Les sorties après peuvent être actualisées explicitement. Aucun fichier ROM ou audio n'est publié.
