# Gorgouille : sprite statique de face

[PNG natif transparent](gorgouille-face.png) — [aperçu ×8](gorgouille-face-x8.png).

Une seule pose de face, sans massue, dans le même gabarit natif que les autres oni : case de 32 × 32 pixels, silhouette de 22 pixels et même ligne de pieds. Corps doré, crête rouge, détails violets et défenses claires issus de la référence du chat.

Source générée conservée et conversion reproductible par `python tools/yokai/convertir_gorgouille_statique.py` : recadrage, réduction au plus proche voisin et palette de quinze couleurs plus transparence. Hauteur, base, transparence et indices de palette vérifiés. Il s'agit d'une nouvelle ressource overworld : les graphismes de combat, les statistiques et le statut jouable de Gorgouille restent inchangés. Aucun événement ajouté, aucune nouvelle ROM publiée ni fusion sur master.

## Gabarit corrigé

La première silhouette était trop élancée. Le dessin a été repris sur la pose de repos de face de Gargaros : tête large, torse court, bras épais et petites jambes, avec une crête rouge compacte. L'emprise visible est maintenant exactement celle de cette pose de Gargaros : 18 × 22 pixels, du point (7,9) au point (25,31) exclu, à l'intérieur de la case 32 × 32. Une seule pose, sans massue.

[Comparaison des quatre oni à la même échelle](comparaison-quatre-oni-x6.png), de gauche à droite : Gargaros, Ogralos, Orqanos, Gorgouille. Cette planche compare les assets natifs ; aucune capture en jeu n'est revendiquée.
