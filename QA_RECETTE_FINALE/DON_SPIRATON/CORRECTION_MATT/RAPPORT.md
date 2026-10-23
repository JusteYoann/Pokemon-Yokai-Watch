# Matt — couleurs après combat et position de compagnon

Le défaut signalé est un conflit de palette lors de la reconstruction des
sprites overworld après le combat contre Don Spiraton. Le premier chargement
de Matt utilisait correctement le banc6, distinct du banc10 de Don/sbires.
`SpawnObjectEventOnReturnToField` reprenait toutefois le banc spécial10 de sa
fiche graphique. Le retour de Don rechargeait ensuite ce même banc : Matt se
retrouvait dessiné avec les couleurs de Don. Le contrôle précédent vérifiait les
palettes à l'arrivée de Matt, mais pas à ce retour du combat.

La règle locale de palette est désormais partagée entre l'apparition,
la reconstruction au retour du combat et le rafraîchissement de graphics ID.
Elle reste limitée à Matt à Argenta et dans la salle du Maître. Aucun pixel,
fichier de palette ou tableau d'animation n'est modifié.

Matt rejoint maintenant(5,11), juste à gauche du joueur(6,11), et se tourne vers
le nord comme lui pour regarder Don. Il conserve cette position et orientation
après le combat, pendant la reconnaissance de défaite de Don. Une fois Don et
les sbires partis, il se tourne vers le joueur pour ses propres félicitations.
Le chemin de Chen passe une ligne plus bas avant de contourner le duo : aucune
traversée de la case de Matt.

## Recette réelle

Les ROM publique et privée sont recompilées. Le parcours Lance → porte normale
→ Don → soin de Matt → fusion → huit vies → conclusion → Chen → Panthéon →
crédits → Continuer passe dans les deux. Aucune victoire injectée. L'équipe et
la position initiale devant Lance sont des fixtures QA renforcées, comme pour
l'étape B ; ce n'est pas une évaluation de l'équilibrage.

Les nouvelles assertions aux étapes3 et6 vérifient Matt immédiatement à gauche,
sur la même ligne, les deux personnages face au nord, les bancs6/10 distincts,
les32octets de chaque palette normale et l'absence de superposition d'acteurs.
L'étape6 vérifie explicitement le retour de combat précédemment manquant.
Voir `public/FINALE_NORMALE_MGBA.json`, `prive/FINALE_NORMALE_MGBA.json` et les
captures `matt-couleurs-position-etape-{3,6}.png`.

Argenta : arrivée réelle par la Route2, colonne21, scène terminée et bancs6/10
corrects. Les trois autres colonnes ne sont pas rejouées pour cette correction.
Les graphismes, scripts et affectations d'Argenta sont inchangés.

`PRESERVATION.json` confirme les151 données/graphismes, les équipes, les fichiers
de la maison d'exil, l'art harmonisé et les31 flux DPCM/gains binaires préservés.
EWRAM261128, IWRAM29824 public/29888 privé : aucune augmentation. ROM publique
16777216octets ; privée31658395octets, toujours sous32Mio.

Les clips de la finale sont recapturés depuis la ROM corrigée ; l'archive GitHub
reste sans audio pour ne pas publier les OST privées. Aucun changement à la
branche audio ni aucune fusion de branche.
