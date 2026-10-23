# Alyzon Bie — reprise de zéro sur le gabarit de Red

Cette série est une nouvelle proposition. Elle ne reprend pas les grilles des essais précédents. La référence de proportions est le sprite FRLG original `graphics/object_events/pics/people/red_normal.png` ; l'artwork `Alyzon_Bie.webp` guide uniquement le costume et l'identité.

## Mesures et construction

Les neuf cellules de Red sont mesurées directement dans son PNG indexé. La face au repos occupe x1..14 et y12..30 dans une cellule 16 × 32 : **14 × 19 pixels**, douze couleurs opaques. Les autres dimensions et positions exactes figurent dans `graphics/alyzon_bie/reprise-red/CONSTRUCTION.json`. Le bas des pas descend jusqu'à y31 ; les poses au repos finissent à y30.

Alyzon est dessinée directement sous forme de grilles littérales de quatorze colonnes sur dix-neuf lignes, dans des cellules **16 × 32** : ni illustration réduite ni ancien sprite redimensionné. Face et dos : 14 × 19 ; profils : 12 × 19. Une étude générée avec Red et l'artwork a aussi été consultée comme guide de direction, sans en extraire ou réduire les pixels. Les livrables natifs proviennent exclusivement des matrices du script `creer_alyzon_base_red.py`.

Coiffure blonde asymétrique, œil cyan visible à droite de l'image de face, mèche masquant l'autre œil, blouse blanche compacte, haut violet et bas bleu. Le profil gauche masque l'œil ; le droit le montre. Le visage est plat, sans nez saillant. La palette comporte au maximum quinze couleurs opaques RGB555 plus une transparence distincte des contours. Les contours sont d'un pixel, brun sombre dans les cheveux et presque noir pour les vêtements.

Quatre orientations × trois poses : repos et deux pas. La tête conserve exactement ses pixels entre les pas, avec un décalage vertical d'un pixel pendant la marche comme les cellules de Red. Seuls pieds et petites ombres des mains changent dans la grille.

## Livrables

- `graphics/alyzon_bie/reprise-red/` : douze PNG natifs transparents et `douze-poses.png` (48 × 128, quatre lignes de directions, trois colonnes de poses).
- `overworld.png` (144 × 32), `.4bpp` (2 304 octets), `.gbapal` (32 octets) : neuf cellules standards FRLG. Les trois PNG droits restent séparés, car le simple miroir de gauche ne respecte pas l'asymétrie des cheveux.
- `douze-poses-x10.png` : présentation agrandie sans lissage.
- `comparaison-red-x8.png` : comparaison native agrandie, Red original et quatre orientations au repos.
- `marche-quatre-directions.gif` : animation des PNG.
- `marche-reelle-mgba.gif` : douze déplacements natifs, trois par direction, capturés dans mGBA. Le titre est ajouté hors du cadre du jeu.

## Vérification et limites

Le test mGBA utilise les PNG natifs 16 × 32 centrés dans une cellule de test 32 × 32, sans mise à l'échelle. Les douze coordonnées d'arrivée et les phases d'animation passent les contrôles ; la palette reste stable. SHA-256 de la ROM inchangée : `af807f4b8e2b6f7367208c1b25355a93b90b9937241295dd23e34b382df906cf`.

Il s'agit d'un essai en RAM : pas d'inscription graphique permanente, de changement de carte, de scénario ou de sauvegarde. Les profils asymétriques sont sélectionnés avant les clips indépendants ; une future intégration devra conserver cette distinction. Les anciennes propositions restent archivées sans modification. La qualité artistique de cette nouvelle série reste à valider par le créateur.
