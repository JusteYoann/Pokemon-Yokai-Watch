# Lavanville — phase 1, à examiner

La direction **FRLG uniquement** et la base de corpulence zombie ont été confirmées par le créateur pendant cette phase. Aucune autorisation d’intégration définitive n’est déduite de ces choix.

- [Nouvelle comparaison : Red et quatre zombies compacts, agrandissement ×6](prototypes/FRLG-comparaison-red-x6.png)
- [Même comparaison à la taille native](prototypes/FRLG-comparaison-red-natif.png)
- [Montage sur carte : illustration de placement, pas une capture d’intégration](prototypes/MONTAGE-zombies-sur-carte-x4.png)
- [Brume animée : véritable essai RAM mGBA, ROM de base inchangée](prototypes/mgba-brume-ram.gif)
- [Galerie complète avec avertissements de statut](galerie.html)
- [Audit, solutions proposées, budget, risques, plan de tests](RAPPORT.md)
- [Équipes candidates](EQUIPES.md)
- [Dialogue de première arrivée proposé](DIALOGUES.md)
- [Sources et lignes vérifiables](PREUVES-SOURCES.md)

Les fichiers natifs sont des **candidats de mise à l’échelle/palette** issus de planches générées. Ils ne sont pas annoncés comme des sprites finaux dessinés au pixel. Les quatre dernières faces prennent le gabarit FRLG ; les anciennes vues plus hautes restent archivées comme études dépassées. Aucun sprite validé n’est remplacé.

## Reproduction

Depuis la racine de ce worktree :

```sh
python docs/lavanville-zombie-night/phase-1/outils/auditer.py
python docs/lavanville-zombie-night/phase-1/outils/etudier_patrouilles.py
```

Le premier audit s’appuie sur les neuf artworks présents localement dans `/workspace/artifacts/lavanville-phase1/references` pour leur manifeste ; ils ne sont pas redistribués. Pour les captures, il faut l’environnement mGBA et les ROM/ELF de référence déjà construits :

```sh
source /workspace/.setup/env.sh
YOKAI_QA_ROM=/workspace/Pokemon-Yokai-Watch-spiraton/pokefirered_audio.gba python docs/lavanville-zombie-night/phase-1/outils/prototype_mgba.py
python docs/lavanville-zombie-night/phase-1/outils/preparer_planches.py
```

Les planches générées sources sont conservées dans `prototypes/sources/`, les images indexées candidates dans `prototypes/natifs/`. Aucun audio protégé ni ROM dans ce dossier. Les outils n’écrivent que dans ce dossier documentaire et dans la RAM temporaire de l’émulateur, pas dans les sources du jeu ou une sauvegarde persistante.
