# Audit en lecture seule — base de la refonte

HEAD exact au démarrage : `903281f4982a4b2e5cbe3d6ac8fc6c4cb47dff08`, branche `feature/juste-yoann-charme-chroma`, arbre propre. Travail sur `feature/shiny-151-refonte-20261024`. Les documents du ZIP, dont l’inventaire complet, ont été lus avant les modifications.

Les 151 ID du CSV sont les constantes natives 001–151 de Rouge Feu. Les noms humains sont parfois tronqués ; les chemins sont sélectionnés par numéro, les constantes par le champ `slug`. Le nº034 est bien `SPECIES_NIDOKING`, Métaureau., un bovin ; aucun glissement vers un autre Yo-kai.

- Sources : `graphics/yokai/NNN/front.png`, `back.png`, `normal.pal`, `shiny.pal`.
- Le sprite normal indexé est partagé avec le shiny. Les anciens dessins de `graphics/yokai_shiny/` sont retirés du chargement : `TryLoadYokaiShinyPicWithPalette` retourne FALSE. Ils ne sont pas utilisés comme références ni modifiés.
- `src/data/graphics/pokemon.h` relie les palettes `shiny.gbapal.lz` aux tables natives. Les menus utilisent les versions `*-display.4bpp`, les combats les `*-battle.4bpp`, à travers `TryLoadYokaiBattlePic`.
- Génération : règles make / gbagfx, profils `data/yokai/sprite_presentation.json` et `presentation_4bpp.py`. Ces profils et les matrices de combat sont conservés.
- GBA : 16 entrées par palette, index 0 transparent, 15 couleurs opaques, RGB555. Les aperçus utilisent les mêmes valeurs quantifiées (canaux par pas de 8) que les couleurs natives.
- Les deux réindexations locales de pupilles #137/#138 utilisent les entrées libres 14/15. Les PNG normaux restent identiques en RGBA ; leurs palettes normales ajoutent les couleurs déjà présentes dans ces cases. Aucun autre dessin normal ni palette normale n’est modifié visuellement.

## Éligibilité préexistante

`IsYokaiShinyAllowed` autorise 84 espèces et en exclut 67. Il intervient dans la création des PID ainsi que dans le choix des palettes. Ce mécanisme reste strictement inchangé : le dossier interdit de modifier la logique de rencontre. Les 151 palettes sont préparées pour validation, mais **67 nouvelles formes ne sont pas encore activées dans les rencontres**. Leur activation devra être décidée explicitement après examen des rendus.

Les tests d’émulateur vérifient d’abord la palette choisie automatiquement par cette règle. Ensuite, pour inspecter les 151 propositions, ils demandent au moteur de charger la palette normale puis la shiny via `LoadCompressedPalette`. Pour les 67 exclusions, cette seconde capture est donc une fixture d’affichage annoncée comme telle, et non une preuve de rencontre shiny naturelle.

## Méthode artistique et limites

Les index sont regroupés manuellement par espèce et par zone. Les familles ont leurs propres groupes, sans copier leurs index. Les teintes sont proposées à partir des artworks ; l’ombrage suit la luminosité d’origine, avec un ancrage médian pondéré sur la face et le dos. Les noirs profonds des contours sont conservés. Les anciennes palettes shiny ne servent pas de source artistique.

Les échanges #002/#003 et #055/#056 prennent leurs couleurs dans les formes normales des donneurs. #137/#138 ne modifient que les pupilles, le dos restant identique. Les 151 fiches et les aperçus permettent de contrôler chaque proposition.

Les palettes normales réunissent parfois plusieurs matières dans une couleur unique. Une palette globale ne permet pas toujours de les dissocier sans un travail de masques supplémentaires ou une réduction d’autres nuances. Les limites repérées sont consignées dans l’audit individuel. Ces résultats restent des **propositions visuelles**, pas une approbation artistique automatique.
