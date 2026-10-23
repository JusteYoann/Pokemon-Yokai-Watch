# Quatre sprites de combat des zombies errants

[Planche annotée des quatre variantes](planche-quatre-zombies.png) · [Planche native transparente](quatre-zombies-natif.png) · [Comparaison avec six sprites des 151](comparaison-151-x4.png).

| Variante | PNG transparent 64 × 64 | Silhouette | Couleurs opaques |
|---|---|---|---:|
| Errant | [PNG](../../../../../graphics/yokai_zombies/errant/battle-front.png) | 44 × 54 | 13 |
| Sprinteur | [PNG](../../../../../graphics/yokai_zombies/sprinteur/battle-front.png) | 51 × 50 | 13 |
| Colosse | [PNG](../../../../../graphics/yokai_zombies/colosse/battle-front.png) | 58 × 54 | 14 |
| Spectral | [PNG](../../../../../graphics/yokai_zombies/spectral/battle-front.png) | 39 × 56 | 13 |

Les mesures effectives sont dans [RESSOURCES.json](RESSOURCES.json). Les colonnes reposent sur les silhouettes complètes ; les fragments d'une variante voisine ne sont pas conservés.

## Captures réelles de combat

[Les quatre affichages mGBA](quatre-combats-mgba-x2.png).

Captures individuelles : [errant](mgba-errant-x3.png), [sprinteur](mgba-sprinteur-x3.png), [colosse](mgba-colosse-x3.png), [spectral](mgba-spectral-x3.png). Captures natives 240 × 160 également disponibles dans ce dossier. [Résultat du test](TEST_MGBA.json).

Chaque capture provient d'un combat réel de la ROM de base inchangée, avec chargement de la nouvelle image et de sa palette dans un OBJ de test. Un adversaire RAM de gabarit `species=9`, renommé pour le contrôle visuel, est utilisé explicitement : ces images ne prouvent pas l'intégration d'une nouvelle espèce ni ses statistiques ou règles de fuite/capture. Pas d'affectation de rencontre, d'équipe ou d'attaque effectuée. Validation artistique du créateur en attente.

Les nouveaux fichiers sont préparés à partir de concepts générés guidés par les sprites existants et les références du créateur ; la source et la méthode sont conservées. Pas de revendication d'une création initialement dessinée à la main sur une grille native.
