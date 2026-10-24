# Patrouille Oni : quatre orientations dans mGBA

[Aperçu dans le jeu, agrandi ×3](public/quatre-directions-mgba-x3.gif) : face, dos, gauche, droite. La créature reste sur place au-dessus de Nathan à Bourg Palette. [Planche transparente](quatre-vues.png).

Les quatre vues viennent de la planche générée du chat : conversion au plus proche voisin en quatre images de 32 × 32 pixels, silhouette de 22 pixels, quinze couleurs opaques et une transparence. Le dos n'a pas d'œil et les profils conservent leurs images distinctes.

L'acteur est temporaire dans le banc de démonstration. Aucun événement d'aventure, sauvegarde utilisateur ou personnage existant n'est modifié. Le nouvel identifiant graphique est disponible pour une intégration ultérieure. La table d'orientation est enregistrée dans le moteur des poses immobiles pour que les rotations natives mettent effectivement les tuiles à jour ; aucune nouvelle animation de marche n'est inventée.

Compilation publique réussie et aperçu enregistré dans mGBA : chargement des quatre images et de leur palette, contrôle des tuiles réellement affichées pour chaque orientation, visibilité et rectangle entièrement à l'écran, présence des pixels violets sur chacune des 60 captures. Les quatre vues ont également été inspectées visuellement. [Résultats et empreinte de la ROM de démonstration](public/TEST.json).

Les images du GIF sont des captures du moteur. La version ×3 applique seulement un agrandissement au plus proche voisin. Aucun montage de la créature sur le décor. Aucune ROM publiée et aucune fusion sur master.

Reproduction après compilation : `python tools/yokai/capturer_patrouille_oni_mgba.py`. Conversion reproductible : `python tools/yokai/convertir_patrouille_oni.py`.
