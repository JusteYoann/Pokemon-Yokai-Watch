# Référence officielle — zombies errants

Le créateur valide sa propre retouche montrée dans `mgba-nuit-sandgs-zombies-x4.png` comme référence officielle des zombies errants sur la carte.

- Reprendre les deux poses visibles dans sa capture, sans les redessiner ni réinterpréter les contours, proportions, visages, couleurs ou flammes.
- Conserver exactement leur taille relative à Nathan telle que montrée dans la capture retouchée.
- Les propositions générées précédentes sont des études, pas la référence finale à intégrer.
- Ne pas extrapoler des orientations ou des animations à partir de cette seule validation de face.

## État technique

Décision artistique enregistrée. Le PNG retouché est visible dans la conversation mais son fichier binaire n’est pas disponible dans le workspace ; le chemin Windows fourni ne désigne pas un fichier accessible dans l’environnement Linux. Extraction exacte, comptage des pixels, palette et intégration en attente du PNG source téléchargeable. Aucun sprite du moteur n’est remplacé par une approximation.

Une fois le fichier reçu : conserver l’original, extraire sans redessin les deux silhouettes de la capture (en comparant au fond mGBA propre déjà disponible si nécessaire), retrouver la grille native sans lissage, vérifier transparence et palette, charger les ressources et confirmer l’échelle dans une capture réelle mGBA.

## Grille du créateur reçue ensuite

Le créateur a affiché une grille agrandie : silhouette relevée sur 14 colonnes et 20 lignes. Une transcription native a été créée dans `graphics/yokai_zombies/errant`, avec matrice éditable, PNG transparent et exports GBA. Elle a été chargée dans une capture réelle mGBA à côté de Nathan, pieds alignés. Le fichier original binaire demeure absent : correspondance des couleurs et transcription à contrôler, sans prétendre une extraction exacte depuis le PNG d’origine. Aucune nouvelle orientation ni animation ajoutée.
