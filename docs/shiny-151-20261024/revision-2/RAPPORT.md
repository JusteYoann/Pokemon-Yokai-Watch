# Revue complète des 151 shiny — révision2

**Priorité : chaque shiny doit être lisible seul.** Les10 planches ci-dessous présentent uniquement les formes shiny de face et de dos.

[Voir les151 shiny seuls](PLANCHES.md) · [Galerie individuelle / PNG transparents](GALERIE.md) · [Télécharger la visionneuse et les PNG](apercus-151-shiny-revision-2.zip)

![Shinies seuls — 017 à032](shinies-seuls-02.png)

## Ce qui a été repris

- Revue explicite de toutes les nuances utilisées dans les151 espèces : chaque index est affecté à une zone ou conservé volontairement. Plus d’index oublié par le générateur.
- Ombres et bordures colorées rattachées à la nouvelle gamme de leur matière ; regroupement des teintes très proches pour réduire les points parasites. Les contours profonds, les yeux et les détails nécessaires à la lecture restent contrastés.
- Huit retouches locales, sans déplacer de pixel opaque : **018,051,066,067,120,133,145,150**. Elles séparent les matières qui partageaient un index normal. Robonyan F est bleu/rouge ; Mognyan a un pelage noir et un ventre crème ; les sirènes ont des cheveux gris lavande ; Ronimpec a un casque et une armure distincts ; Terminyanator conserve exactement les couleurs natives de sa moto et de ses vêtements hors de la tête ; Savantard distingue chapeau, peau et blouse ; le visage d’Enma est séparé de sa robe.
- Les dessins normaux, les151 ID, les dimensions, les silhouettes, les cadrages et les matrices d’animation sont conservés. Les masques sont des recolorations du dessin normal, sans lissage ni tramage.
- Les exceptions du dossier restent applicables : échanges limités à la fourrure/peau pour002/003 et055/056, et **yeux seuls** pour137/138.

## Contrôles exécutés

| Contrôle | Publique | Privée |
|---|---:|---:|
| Compilation GBA | Réussie | Réussie |
| Combats natifs mGBA, face et dos |151/151|151/151|
| Pointeurs/palettes natives normal + shiny |302/302|302/302|
| Chargement générique des8 masques, face/dos |8/8|8/8|
| Copies natives vers les fonds d’animation |16/16|16/16|
| Tours réels avec attaque et retour au menu |5/5|5/5|
| Textures en VRAM et palettes conservées après attaque |5/5|5/5|

[Intégrité des151 espèces](TEST_INTEGRITE.json) · [Synthèse des tests](TESTS_SYNTHESE.json) · [Logs](logs/)

Les8 chemins génériques de menus sont vérifiés par appels natifs, pas par un parcours manuel de tous les menus. Les5 tours réels concernent018,066,067,120,145 : équipes/attaques et badge8 sont des fixtures ; l’adversaire emploie Trempette pour éviter les boucles de statut. Aucune modification des PV ni des résultats de combat. Les copies de fonds et les textures sont vérifiées des deux côtés.

Les67 exclusions shiny historiques restent inchangées. Les captures des espèces exclues utilisent explicitement le chargement de leurs palettes et textures comme fixtures de rendu ; elles ne prouvent pas une rencontre shiny naturelle. Les taux, le Charme Chroma, le Safari, le scénario et les ressources overworld sont préservés.

## ROM testées

- public : `065a83e926839e4b5d074a2206221dd5a616a00c61925122564cd0bcaa44fa9c`.
- prive : `63121ecbc74d8d88353a3aafa4fff3fe3e3a24c736b71c94c35df092d6ad1686`.

Mémoire : publique16025700 octets de ROM utilisés ; privée31787063, sur32 Mio. Consommation EWRAM/IWRAM inchangée.

## Inspection et limites

Les302 PNG shiny transparents et les151 comparaisons restent disponibles dans la galerie. La visionneuse HTML permet de masquer le normal, de passer à la taille native et de changer de fond. Les couleurs sont celles de la GBA (RGB555).

La robe de Whisperocrates n’est pas ajoutée au dessin de Whisper : la direction crème/dorée reste adaptée à sa forme existante. Les motifs réguliers absents du normal ne sont pas redessinés. La réduction à15 couleurs opaques des masques peut simplifier certaines nuances. Ces contraintes sont distinctes des oublis de couleurs corrigés dans cette révision.

Les tests techniques ne remplacent pas la validation visuelle. Le jeu complet et toutes les attaques ne sont pas parcourus. Travail conservé sur `feature/shiny-151-refonte-20261024` ; **aucune fusion sur master**.
