# Comparaison Agent X / Don Morleone / Mafiamille

Capture réelle mGBA libretro après démarrage d’une nouvelle partie, téléportation de test sur la Route 1 et apparition temporaire de huit PNJ. Nathan est présent pour l’échelle. Don Morleone et les six Mafiamille emploient les ressources de la ROM existante.

La face d’Agent X reprend la disposition approuvée des deux yeux jaunes séparés par le noir, dessinée directement sur la grille 16 × 32 (silhouette 14 × 19). Source dans `docs/atelier-personnages/propositions/agent-x-frlg-abc/agent-x-face-validee-source.json`.

**Limite :** cette nouvelle face est injectée dans les tuiles VRAM du PNJ temporaire, avec une palette isolée chargée par LoadPalette. Ce test vérifie son rendu dans le moteur, pas son intégration compilée. Le callback et l’animation du PNJ de test sont figés pour conserver cette seule face. Aucune ROM ni carte scénaristique modifiée. Les autres orientations et la marche de cette nouvelle version ne sont pas réalisées.

`scene-mgba-native.png` : capture 240 × 160. Les versions ×4 sont agrandies au plus proche voisin ; seule la marge de la version annotée est ajoutée après capture. `CONTROLE.json` conserve les acteurs, l’empreinte de la ROM, les contrôles VRAM et palette.

Reproduction : charger l’environnement de compilation existant, puis `python3 tools/yokai/capturer_agent_x_mafiamille_mgba.py`. Nécessite une ROM et son ELF concordant, mGBA libretro et les dépendances du harnais existant.
