# Argenta — reprise du 22 octobre 2026

Chapitre intégré : entrée naturelle depuis la Route 2, discours de Morleone et de la Mafiamille devant les habitants, rencontre avec Enma sous forme humaine sans révélation de son identité, puis arène de Wyatt. Les personnages successifs partagent la banque de palette spéciale sans se superposer. Les deux protagonistes sont testés.

L'arène conserve son bâtiment et ses sorties, avec une nouvelle disposition de fouilles : deux stèles interactives, obstacles et accès central conditionné par leur lecture et la scène d'Argenta. Wyatt remet le premier trophée et la CT39. Nanpart niveau9 et Passpa niveau11 remplacent son équipe active du premier passage ; IV0, Fermeté, aucun objet. Ces niveaux sont des choix techniques provisoires, pas une décision scénaristique validée ni un équilibrage global achevé.

L'ancienne équipe verrouillée reste dans sa source historique. Le caméo optionnel de Wyatt après le Panthéon est déplacé de Cramois'Île vers son arène ; ses six combattants et ses indicateurs existants sont conservés. La Pierre Eau existante se récupère désormais après cette revanche. Un sac plein laisse les cadeaux en attente, sans duplication ni combat supplémentaire imposé.

## Vérification

- `TEST_CHAPITRE_MGBA.json` : véritables déplacements, transitions, dialogues, palettes, fouilles, combat natif, trophée, CT, sortie et Chaussures de Sport ; Nathan et Katie. Équipe déclarée de test : Kappacap13, Whisper11, Nihilistik10, IV15, statistiques ordinaires et attaques déjà apprises réordonnées. L'aventure précédente n'est pas jouée intégralement pour préparer cette équipe.
- `TEST_MIGRATION_MGBA.json` : défaite réelle avec starter niveau1, conservation des stèles, reprise de progression, sauvegardes Flash, récompenses et revanche optionnelle. Pour cette seule revanche, Hovernyan100 possède explicitement des statistiques augmentées à999 : validation des événements, aucune preuve d'équilibrage du postgame.
- `TEST_CONTINUE_MGBA.json` : états d'anciennes sauvegardes construits explicitement, puis sauvegarde Flash et véritable callback Continuer. Une première reprise en ville ou dans l'arène recharge les nouveaux objets/cartes et utilise une position sûre. Les reprises suivantes conservent la position exacte. Aucun fichier d'une partie historique de joueur n'a été fourni pour cette recette.
- `CONTROLE_SOURCES.json` : accessibilité et collisions, accès au Champion, sorties, quatre colonnes d'entrée, capacité maximale des objets et conservation de l'équipe historique.
- `LARGEURS_DIALOGUES.json` :98 lignes contrôlées avec les largeurs de la police native.
- `TEST_EQUIPES_ACTIVES_MGBA.json` :639 équipes actives vérifiées, dont le nouveau profil de Wyatt et ses talents.

Reproduire après `source /workspace/.setup/env.sh` et `make -j4` :

```sh
python3 tools/yokai/verifier_argenta_sources.py
python3 tools/yokai/tester_textes_argenta_mgba.py
python3 tools/yokai/tester_argenta_scenario_mgba.py
python3 tools/yokai/tester_argenta_migration_mgba.py
python3 tools/yokai/tester_argenta_continue_mgba.py
python3 tools/yokai/tester_equipes_mgba.py
```

Le dernier outil historique écrit dans `RECONSTRUCTION` ; son résultat actuel est copié ici afin de conserver les preuves historiques. Les diagnostics conservés montrent aussi les erreurs initiales du pilote de test et la défaite d'une première fixture postgame. Ils ne constituent pas des validations réussies.

Le profil actif est `data/yokai/scenario_argenta.json`. Si une régénération intentionnelle réapplique les anciennes équipes globales, exécuter ensuite `python3 tools/yokai/appliquer_equipe_argenta.py` avant compilation ; le script conserve l'ancienne équipe source et rétablit le profil actif, les talents et le manifeste.

## Limites et suite

Ce chapitre n'est pas le scénario intégral. L'équilibrage des trois starters, une partie complète, la suite des Champions, Lavanville, les voyages temporels, le nouveau Temple et le postgame scénarisé restent à développer ou valider. Les tests emploient des fixtures déclarées, pas une sauvegarde ayant parcouru toute l'aventure. Le vérificateur général historique des sprites signale toujours son incompatibilité connue avec les nouvelles présentations ; aucune validation globale n'est revendiquée. ROM locale de recette uniquement, aucun binaire ROM publié.
