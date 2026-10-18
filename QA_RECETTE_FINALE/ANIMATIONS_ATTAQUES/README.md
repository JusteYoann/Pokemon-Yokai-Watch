# Animations des capacités — recette native

Le pilote `tools/yokai/tester_animations_attaques_mgba.py` entre dans une vraie scène de combat mGBA avec deux Yo-kai, puis exécute les scripts/callbacks natifs d’animation. Il n’émule pas une animation en Python et ne remplace aucun script du jeu.

Les conditions sont préparées : douze silhouettes (six paires), niveaux et personnalités choisis ; chaque capacité est isolée par un état instantané. Les 354 scripts sont demandés côté joueur et adversaire, dans un contexte normal et dans un contexte shiny demandé, avec le statut réellement accepté par le moteur enregistré. Les espèces exclues ne doivent pas être forcées shiny. Huit capacités à deux tours reçoivent aussi le second stade.

`TEST_MGBA.json` donne uniquement les résultats réellement terminés ; une interruption ou un dépassement de délai reste un échec, pas une validation. Les images de `preuves/` montrent les effets Métal/masquage/recoloration/déformation choisis, en huit instants d’une animation. Les octets des deux graphismes de combattants en VRAM sont comparés avant/après ; une différence doit être examinée, elle ne suffit pas à prouver une corruption (certaines capacités changent volontairement l’affichage).

**Limites :** ces appels de scripts/callbacks sont des fixtures. Ils ne démontrent pas le calcul des dégâts, les prérequis en combat réel, toutes les météos/combinaisons de statuts, toutes les 151×354 combinaisons, le matériel physique, ni une appréciation humaine de chaque image. Une animation achevée sans plantage n’est pas automatiquement artistiquement validée. Les capacités dont les captures n’ont pas été examinées restent à revoir visuellement. L’état final du rapport prime sur le pilote de 20 cas conservé dans `jalons/`.
