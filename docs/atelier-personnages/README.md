# Atelier graphique — tous les personnages avant la suite du scénario

La décision du créateur du 22 octobre 2026 donne maintenant la priorité à la préparation de toutes les ressources graphiques des personnages. Le Dr Jobard reste en pause. Le développement déjà présent est conservé ; aucune réécriture des événements, aucun remplacement automatique des sprites actifs dans cette étape.

## Consulter les ressources

- [Galerie par personnage et tenue](GALERIE.md) : tous les fichiers natifs dédiés retrouvés, avec leurs cases complètes.
- [Vue d’ensemble des personnages de carte existants](APERÇU_PERSONNAGES_EXISTANTS.png).
- [Casting et besoins de production](PERSONNAGES_ET_BESOINS.csv) : protagonistes, rival, champions, antagonistes, caméos, PNJ de quêtes et acteurs Yo-kai de scène.
- [Inventaire de tous les fichiers recensés](RESSOURCES_EXISTANTES.csv) : ressources personnalisées et ressources des PNJ/dresseurs d’origine, dimensions, couleurs, empreintes et références dans les sources.
- [Gabarit humanoïde](gabarits/humanoide-nathan-4-directions-x8.png) ; [version native transparente](gabarits/humanoide-nathan-4-directions.png).

Les planches sont des montages de fichiers, pas des captures mGBA. Les gris de fond ne sont jamais ajoutés aux sprites du jeu. Une ressource référencée par une directive INCBIN n’est pas nécessairement utilisée par un événement actif. Un dossier absent sous un identifiant ne prouve pas la perte du dessin : vérifier les alias, les archives et les PNJ génériques réutilisables.

## Règles de production

1. Garder Nathan comme référence de proportions tête/corps des personnages humanoïdes sur la carte : case de 16 × 32, silhouette fixe de référence 12 × 19, pieds à y30. Le gabarit est un masque technique extrait des poses existantes, pas un nouveau personnage à intégrer. Les poses en action peuvent déborder autrement dans les cases prévues par le moteur.
2. Pour chaque personnage, distinguer le dessin de face, de dos et de profil, puis les vraies images de marche. Un retournement horizontal est acceptable seulement si le costume et le visage le permettent. Trois poses immobiles ne constituent pas une marche complète. Les actions scénarisées demandent leurs propres images seulement lorsqu’elles sont nécessaires.
3. Nathan et Katie : vérifier marche, course/surf, vélo, Cherche VS à vélo (`vs_seeker_bike` : outil de revanche), pêche, action terrain/objet, apparition de combat, animation de lancer de dos, introduction, crédits et icône région. Les noms techniques restent ceux du dépôt. Ne pas inventer de nouvelles catégories de mouvements à partir des seuls noms de fichier.
4. Matt : carte et marche, trois sprites de combat existants selon progression, introduction et crédits. Pas de série de vélo/pêche pour chaque PNJ sans besoin dans ses scènes.
5. Les autres personnages : carte et orientations ; marche et actions selon leurs scènes ; dessin de combat pour les personnages combattus. Portraits de dialogue et tenues supplémentaires seulement lorsqu’ils sont prévus par les spécifications. Ne pas imposer un nouveau système de portraits à tous les dialogues.
6. Garder les anciens designs choisis d’Enma et Domniscian. Les trois Mafiamilles partagent le design de carte choisi (ancien Mafiamille 3) et gardent des dessins distincts en combat. Employés : silhouette commune, couleurs distinctes sur la carte, dessins de combat différenciés.
7. Distinguer le Seigneur Enma narratif, sa tenue civile, Enma capturable et Enma l’Ancien. Les Yo-kai de scène et rencontres statiques conservent leur morphologie ; ne pas les comprimer arbitrairement dans le gabarit humain.
8. Contours foncés lisibles, petits groupes de pixels cohérents, absence de lissage à l’agrandissement. Examiner à taille native ET agrandie sur plusieurs fonds. Un grand dessin de proposition n’est pas une preuve de lisibilité à 12 × 19 pixels.
9. Formats et palettes selon le consommateur réel : normalement 16 couleurs dont index 0 transparent pour les sprites 4bpp ; vérifier les ressources d’introduction séparément, certaines utilisent le 8bpp. Ne pas imposer 64 × 64 aux ressources de carte ou aux animations verticales de dos.
10. Réutiliser les bonnes ressources et références retrouvées, sans refaire systématiquement tous les habitants de Kanto. Les PNJ génériques d’origine sont recensés et conservés tant qu’aucun remplacement n’est demandé. L’Usapyon décoratif retiré n’est pas réintroduit.

## Ordre du chantier

1. Protagonistes : arrêter une fiche cohérente de Nathan et Katie puis compléter chaque série d’action. Le contrôle des proportions vient avant la déclinaison en dizaines d’images.
2. Matt, puis alliés et champions : Ariane, Wyatt, Nathaniel/Michael, Bérénice, Steve, Mark, Whisper majordome et Alyzon.
3. Seigneur Enma et tenue civile ; Don Morleone, Mafiamilles et employés, en préservant les sélections explicites.
4. Zazel et personnages du Temple ; Domniscian et autres caméos ; personnages des quêtes et acteurs de scène. Jobard reste hors des retouches pour l’instant.
5. Relecture globale de toutes les séries côte à côte : taille, identité, mouvement, palette et équipement. Garder une liste d’images à créer, de propositions à revoir et de dessins explicitement acceptés ; ne pas assimiler « fichier présent » à « terminé ».

Les sprites supplémentaires seront préparés comme propositions hors des chemins actifs, puis intégrés par séries cohérentes après leur vérification. Aucune approbation artistique n’est déduite de la seule réussite d’un contrôle technique.

## Premier constat visuel

La première lecture de la planche avait sous-estimé les équipements de Nathan. L’examen des fichiers agrandis confirme que les roues et les cannes existent bien chez Nathan et Katie : leur finesse ne justifie pas un remplacement systématique. Les essais mGBA de production contrôlent réellement marche, course, vélo, pêche dans quatre directions, actions et entrée en combat. Voir `QA_RECETTE_FINALE/PERSONNAGES_PRODUCTION/PROTAGONISTES_AVANT`.

La référence de Juste Yoann a déjà été envoyée dans la conversation : il faut la retrouver dans les pièces disponibles avant de dessiner, sans lui inventer une apparence. Les formes spéciales de Soranaki, les variantes d’Oni et la composition visuelle du duo Laure/Marge demandent également une vérification de leurs références et besoins exacts avant dessin.

## Vérification de ce premier lot

Le script `tools/yokai/preparer_atelier_personnages.py` lit les PNG et produit cet inventaire ainsi que les planches. Résultats chiffrés dans [INVENTAIRE.json](INVENTAIRE.json). Il ne dessine pas de nouveaux personnages et ne modifie ni le moteur ni les ressources actives.

Les contrôles de ce lot portent sur le décodage des fichiers, les chemins, les empreintes et la génération de galeries. Pas de nouveau test mGBA ni de compilation : aucun fichier utilisé pour construire le jeu n’a été modifié. Les captures mGBA de Jobard restent celles du lot précédent, sans extension de leur portée.

Reproduire les documents depuis la racine du dépôt :

```sh
python3 tools/yokai/preparer_atelier_personnages.py
```
