# Alyzon Bie — ressources retenues et enregistrées

Source : branche `codex/reprise-scenario-2026-10-22`, commit `2647bc1627050f193cc9606f8c0f5f1151986047`. Les deux PNG, les deux palettes, `preview.png` et le fichier historique `conversion.json` sont copiés sans modification ; leurs empreintes sont dans `PROVENANCE.json`.

- `overworld.png` : neuf cases natives 16 × 32, face/dos/profil et deux pas par orientation. Le moteur produit le profil droit par miroir, comme dans la version retrouvée. Aucun redessin ou rééchantillonnage.
- `overworld.pal` : palette dédiée, indépendante de celle du joueur et du groupe Don Morléone.
- `battle.png` : portrait de combat 64 × 64, avec `normal.pal`.
- Identifiant de carte : `OBJ_EVENT_GFX_YOKAI_ALYZON` = **173**.
- Identifiant du portrait : `TRAINER_PIC_YOKAI_ALYZON` = **160**.

La règle de conversion `-mwidth 2 -mheight 4` conserve les neuf images dans l'ordre attendu par les animations FRLG. Les données compilées sont vérifiées dans les deux ROM avec `tools/yokai/verifier_alyzon_integration_mgba.py`.

`conversion.json` est la provenance historique de l'ancienne conversion, dont le statut ancien n'a pas été réécrit. L'état de validation actuel est dans `docs/lavanville-zombie-night/integration-alyzon/`.

Ces ressources remplacent les propositions artistiques comme choix pour les prochains scripts. Aucun ancien scénario, trophée, équipe, identifiant de sauvegarde ou carte de la branche source n'est importé. Le PNJ est enregistré dans le moteur et prêt à être placé par la future cinématique ; aucun placement permanent ou combat scénarisé d'Alyzon n'est encore ajouté.
