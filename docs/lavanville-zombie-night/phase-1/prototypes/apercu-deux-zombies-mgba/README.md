# Deux zombies — véritable aperçu mGBA

- [Capture jour, agrandissement ×4 sans lissage](mgba-jour-x4.png)
- [Capture nuit et brume, ×4](mgba-nuit-x4.png)
- [GIF de la brume, ×3](mgba-nuit.gif)
- Captures natives 240 × 160 : [jour](mgba-jour-natif.png), [nuit](mgba-nuit-natif.png).

Nathan est au centre, les deux poses de zombies à gauche et à droite, pieds alignés. Les images proviennent du rendu réel mGBA : chargement des tuiles par `LoadSpriteSheet`, palettes par `LoadSpritePalette`, création des deux OBJ par `CreateSprite`. Les zombies utilisent respectivement les banques OBJ 13 et 14, la météo la banque 12 dans ce test. Chaque image occupe 512 octets de tuiles pour une cellule 32 × 32. Alpha d’index 0, au plus 15 couleurs opaques RGB555 ; les deux silhouettes candidates sont 16 × 24 et 18 × 24, flamme comprise.

Le dernier visuel fourni (yeux rouges, bouche ivoire, front vert clair) a servi à une extraction transparente. Préparation technique par échantillonnage sans lissage à l’échelle de test et réduction de palette, avec réservation des couleurs des yeux, des dents et de la flamme pour en préserver la lisibilité. La source générée reste conservée ; la correspondance parfaite de chaque pixel avec la capture envoyée n’est pas certifiée.

**Portée : essai visuel temporaire en RAM/VRAM, positions statiques.** Aucun événement de PNJ, patrouille, collision zombie ou progression n’est ajouté. La nuit et la brume sont également des réglages RAM de test. Aucune ROM n’est modifiée/recompilée, aucune sauvegarde persistante n’est écrite. Les habitants humains restants sont ceux de la carte de base, le chapitre Zombie Night n’est pas encore installé. Le GIF anime la brume, pas une marche zombie.

ROM privée de référence : 31 658 395 octets ; SHA-256 dans [TEST_MGBA.json](TEST_MGBA.json). Scripts de reproduction dans `../../outils/preparer_deux_zombies.py` et `../../outils/apercu_deux_zombies_mgba.py`. Ils utilisent les outils mGBA existants, et requièrent la ROM/ELF de référence ainsi que l’environnement installé.
