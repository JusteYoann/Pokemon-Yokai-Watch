# Bérénice Bélier — ressources réutilisées

Ensemble approuvé pour réutilisation par le créateur le 23 octobre 2026, sous réserve de contrôle mGBA et de captures.

Source : `codex/reprise-scenario-2026-10-22`, commit `2647bc1627050f193cc9606f8c0f5f1151986047`, dossier homonyme `graphics/yokai_characters/berenice/`.

Les deux PNG et les deux palettes sont repris sans redessin. `conversion.json` conserve les métadonnées historiques de la source ; son statut ancien de conversion ne décrit pas la validation actuelle.

- Overworld : neuf cellules 16×32, conversion par cellules dans `spritesheet_rules.mk` ; ID175, palette0x112D, banque7.
- Portrait : 64×64 ; ID162.
- L’objet de Safrania conserve son ID graphique historique dans la carte et les sauvegardes ; le moteur résout son apparence lors de chaque chargement.

Les captures et les comparaisons PNG/VRAM des quatre orientations, du portrait et du retour de sauvegarde sont dans [la validation des Champions](../../../docs/champions-yokai-watch/validation/README.md). Aucun ancien événement de la branche scénario n’est repris.
