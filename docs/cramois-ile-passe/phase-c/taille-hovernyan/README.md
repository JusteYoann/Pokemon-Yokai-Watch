# Hovernyan à la taille de Nathaniel

Correction demandée après la revue du prototype `b3861163a`, sur `feature/cramois-ile-passe`, sans merge sur master.

Hovernyan mesurait 26 pixels utiles de haut ; Nathaniel en mesure 19. Les deux vues d'Hovernyan sont réduites au plus proche voisin à **18 × 19 pixels**, avec les pieds à la même ligne 30 et le haut à la ligne 12. Les cellules moteur 32 × 32 restent identiques, ainsi que leurs indices de palette, la pose et la cape couvrant le dos. La planche antérieure est conservée dans `graphics/yokai_characters/hovernyan/overworld-reference.png` ; le script de conversion rend la réduction reproductible. Aucun nouveau dessin généré n'est intégré pour cette correction.

- [Comparaison en jeu avec Nathaniel](public/nathaniel-taille-x4.png).
- [Comparaison avec Michael](public/michael-taille-x4.png).
- [Vue de dos dans mGBA](public/compagnon-dos-cape-x4.png).
- [Rencontre Nathaniel avec la taille corrigée](public/rencontre-nathaniel.gif).
- [Rencontre Michael avec la taille corrigée](public/rencontre-michael.gif).
- [Sprite transparent natif](../../../../graphics/yokai_characters/hovernyan/overworld.png).

Versions publique et privée compilées. Les dix contrôles visuels/interactions de phase C sont réexécutés dans chaque version, dans mGBA : orientation dos, collision, interaction, retour du Sac et six questions affichées. Les hauteurs et lignes des pieds sont contrôlées sur les graphismes natifs, et les deux variantes sont filmées dans le moteur. Rapports et empreintes : [public](public/VISUELS_MGBA.json), [privé](prive/VISUELS_MGBA.json), [dimensions publiques](public/TAILLE.json), [dimensions privées](prive/TAILLE.json), [validation](VALIDATION.json).

EWRAM publique/privée : 261368 octets, **776 libres**, variation nulle. IWRAM : 29824 publique, 29888 privée, variation nulle. Les cellules graphiques et leur coût VRAM restent identiques. Aucun script, équipe, donnée de Yo-kai, collision, palette, animation ou système de sauvegarde n'est changé. Les 136 contrôles complets de phase C restent documentés sur leur ROM historique `b3861163a` ; seuls les contrôles pertinents au redimensionnement sont rejoués sur les nouvelles ROM. Les fixtures et limites du rapport de phase C s'appliquent toujours.
