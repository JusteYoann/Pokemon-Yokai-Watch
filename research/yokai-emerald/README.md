# Pokémon Yo-kai Emerald × Archipelago — audit et stratégie

Audit du 2026-11-14 du hack fourni et de l'intégration Archipelago de Pokémon Émeraude.

| Document | Contenu |
|---|---|
| [ROM_ANALYSIS.md](ROM_ANALYSIS.md) | identité de la ROM (Émeraude US construite avec `make modern`), toutes les modifications mesurées, bugs |
| [YOKAI_CONTENT.md](YOKAI_CONTENT.md) | Nathan, Katie et les **six** Yo-kai : statistiques, attaques, Pokédex, 106 rencontres |
| [FRENCH_TRANSLATION.md](FRENCH_TRANSLATION.md) | HMA (inutilisable sur cette ROM), base française `qigast/pokeemeraude` |
| [ARCHIPELAGO_COMPATIBILITY.md](ARCHIPELAGO_COMPATIBILITY.md) | monde officiel et fork de Flit ; le patch existant refuse le hack (testé) |
| [IMPLEMENTATION_STRATEGY.md](IMPLEMENTATION_STRATEGY.md) | stratégies A/B/C ; recommandation : C en deux jalons |
| [PROTOTYPE_RESULTS.md](PROTOTYPE_RESULTS.md) | tests en jeu dans mGBA, tests Archipelago réels, ce qui reste à faire |
| [BUILD_GUIDE.md](BUILD_GUIDE.md) | reproduire l'audit, compiler, tester |
| [ROADMAP.md](ROADMAP.md) | étapes restantes et crédits |
| [PERMISSION_REQUEST.md](PERMISSION_REQUEST.md) | messages au créateur et aux auteurs du code AP |

Outils : `tools/yokai_extract.py`, `tools/analysis/*`, `poc/ap_patch_check.py`, `poc/mgba_drive.sh`.

Ce dossier ne contient **aucune ROM, aucun asset du créateur et aucune capture de jeu** (`.gitignore`).
