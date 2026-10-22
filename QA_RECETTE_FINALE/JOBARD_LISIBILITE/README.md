# Dr Jobard — révision à partir des cinq nouvelles références

## Réalisation

Le dessin précédent évoquait surtout un cyclope : il ne donnait pas assez de place au col de blouse, à l’œil saillant au-dessus du visage et aux mèches en zigzag. Le nouveau dessin à quatre orientations reprend ces éléments, le visage cyan/rose, le sourire, le cœur rouge et la blouse crème. Le matériel médical, les tuyaux et les griffes restent supprimés conformément à la consigne précédente.

Le dessin de travail est conservé dans `graphics/yokai_characters/dr_jobard/source/proposition.png`. Ce grand dessin n’est pas la résolution en jeu. Le sprite actif est `overworld.png`, avec sa palette `overworld.pal`. L’ancien dessin et les anciens fichiers natifs sont archivés pour restauration.

La conversion a également été ajustée : le simple échantillonnage ponctuel supprimait des contours noirs fins. La couverture des traits noirs est maintenant prise en compte sur la limite de la silhouette. Les pixels partiellement couverts sont conservés pour éviter de perdre les extrémités du dessin. L’intérieur utilise toujours un échantillonnage sans lissage. Aucune retouche du moteur ni d’un autre personnage.

## Vérifications effectuées

- Compilations publique et privée réussies. Empreintes et tailles dans BUILD.json ; version privée : 31 589 579 octets, sous 32 Mio.
- Ressource indexée : quatre cases de 16 × 32, palette partagée de 16 entrées, index 0 transparent, 1 024 octets de tuiles 4bpp et 32 octets de palette GBA.
- Quatre orientations : bornes visibles identiques à celles de Nathan, soit 12 × 19 pixels (PROPORTIONS.json).
- Dans mGBA, sur la ROM privée : deux parcours depuis une nouvelle partie (Nathan et Katie), quatre orientations, invitation avec refus/acceptation, laboratoire et trois salles, retour sur carte, sauvegarde puis rechargement, sorties, répétition sans récompense supplémentaire. Un troisième scénario vérifie la reprise d’une ancienne sauvegarde de Carmin. Trois scénarios réussis dans apres/TEST_MGBA.json.
- Les captures ont été ouvertes et inspectées. Les données de gameplay, les autres sprites et les sources audio ne sont pas modifiés (PERIMETRE.json).

Commande de reproduction des tests, après compilation privée :

```sh
YOKAI_QA_ROM="$PWD/pokefirered_audio.gba" \
YOKAI_QA_ELF="$PWD/pokefirered_audio.elf" \
YOKAI_MYSTERY_QA_DIR="$PWD/QA_RECETTE_FINALE/JOBARD_LISIBILITE/apres" \
python3 tools/yokai/tester_portes_mysteres_mgba.py
```

## Consulter le résultat et limites

- comparaison-avant-apres.png : montage agrandi des fichiers natifs avec Nathan ; ce n’est pas une capture du moteur.
- cartes-avant-apres-mgba-x2.png : juxtaposition de véritables captures mGBA, agrandies sans lissage.
- apres/nathan-jobard-ville.png et les vues dos/gauche/droite : captures natives du moteur ; Katie est également documentée.

À 12 × 19 pixels, les dents, le petit iris et les doigts ne restent pas aussi détaillés que dans les références ou dans le grand dessin source. La ressemblance est une proposition artistique améliorée, pas une validation du créateur. Les tests prouvent l’intégration et le fonctionnement du prototype des Portes Mystères, pas la recette complète de l’aventure. Pas de nouveau clone propre pour cette retouche ; les compilations ici utilisent l’environnement déjà documenté. Les avertissements de dépréciation Pillow n’ont pas empêché la conversion ou les contrôles.
