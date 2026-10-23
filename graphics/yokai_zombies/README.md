# Zombies — ressources validées et intégrées

Le chapitre actif est documenté dans [la finalisation de Lavanville](../../docs/lavanville-zombie-night/finalisation/README.md). Les anciens prototypes restent archivés dans `docs/lavanville-zombie-night/phase-1/`.

## Carte

`errant/overworld.png` est la planche de marche existante validée : neuf cellules 32 × 32, silhouette de 14 × 20 pixels, contours noirs conservés. Les trois poses droites sont produites par le miroir natif des trois poses gauches. La face, le dos et leurs deux pas sont présents.

Aucun PNG n'est redessiné, redimensionné ou recolorié pendant l'intégration. `overworld.pal` transcrit seulement les seize entrées de la palette existante. Identifiant `OBJ_EVENT_GFX_LAVENDER_ZOMBIE` = **174**, palette **0x112C**, banque OBJ **8** (ancienne banque de reflet du troisième PNJ). Alyzon reste en banque 7 ; Nathan0, Matt6 et Don10 ne sont pas modifiés. Les scènes du chapitre réservent ces banques de reflet ; une future scène avec des reflets d'eau concurrents devra prévoir sa propre répartition.

Tous les zombies de la Tour utilisent exactement cette même planche, sans nouvelle variante graphique de carte. Les membres calmes des services utilisent aussi ce graphisme, en conservant leurs fonctions de soin, boutique et changement de surnom.

## Combat

Les quatre `battle-front.png` existants sont conservés octet par octet : errant, sprinteur, colosse et spectral. Ils sont indexés, transparents et de 64 × 64 pixels. Leur présentation reprend les centres et échelles de `battle-presentation.json` à travers les transformations matérielles déjà utilisées pour les Yo-kai ; les images sources ne sont pas rééchantillonnées.

Les errants sont des adversaires directs, sans Dresseur ni équipe : un seul combattant est créé par rencontre. Le moteur utilise un gabarit interne existant, avec nom, statistiques et capacités propres à l'instance, et remplace uniquement son apparence pendant ce combat. Aucun des 151 Yo-kai ne change de données, de graphisme ou de table de rencontre. Le gabarit n'est pas enregistré au Médallium par ces combats ; la capture et toutes les sorties de combat prévues par fuite, capacité d'évasion ou objet d'évasion sont interdites.

Les zombies Dresseurs de la Tour gardent le système de Dresseurs et de flags de victoire natif. Leur portrait réutilise l'image de combat de l'errant (identifiant **161**) ; leurs équipes contiennent des Yo-kai ordinaires capturables ailleurs.

Les sources artistiques antérieures restent dans `sources/`. L'historique initial de préparation des images est conservé dans Git ; les vérifications actuelles et les empreintes d'intégrité sont dans `finalisation/AUDIT_STATIQUE.json`.
