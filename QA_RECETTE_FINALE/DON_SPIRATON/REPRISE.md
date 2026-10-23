# Don Spiraton — étape A, noyau technique

Branche `feature/boss-final-don-spiraton`, créée depuis `d2f590d8b`. Aucune fusion.

Bouh (SPECIES_MEOWTH, 52) a été explicitement validé dans la conversation.
Les niveaux 56–63, transitions à la fin du tour et musiques figurent dans `data/yokai/spiraton/mission.json`.

## Réalisé à ce jalon

- Noyau C déterministe, sans accès à une équipe, un objet ou une action cachée du joueur.
- Huit réserves distinctes ; surplus perdu ; état épuisé en attente jusqu'à EndTurn ; huitième réserve seule terminale.
- Catalogue ROM reproductible des 151 espèces et 3 929 entrées d'apprentissage/CT. Pointeurs actifs Yo-kai utilisés, CS/tuteurs exclus de l'ajout des machines.
- Sélection avec types, statistiques neutres, vitesse, précision, puissance et attaques révélées. Modèle explicite approximatif : pas encore de simulation exhaustive des talents, météos et effets spéciaux.
- Tests hôte sous ASan/UBSan : 1 208 cas de phase, 151 adversaires, quatre attaques légales et distinctes, absence de répétition, déterminisme.
- Compilation publique réussie ; trois séquences complètes du noyau compilé ARM exécutées dans mGBA. Voir CORE_MGBA.json.

## Limites importantes

Ces tests mGBA appellent les fonctions ARM du noyau dans une instance temporaire. Ils NE montrent PAS un combat rendu à huit phases. Le noyau n'est pas encore branché sur les routines de K.O., l'interface ou la salle du Maître. La finale actuellement jouable reste donc inchangée à ce jalon.

Les IV du modèle sont 24, sans EV, nature neutre ; aucun bonus de statistiques. Le modèle estime les statistiques de l'adversaire d'après son espèce/niveau, sans lire ses valeurs cachées.

## Reproduction

```sh
python3 tools/yokai/generer_spiraton_catalogue.py --check
cc -std=c99 -Wall -Wextra -Werror -fsanitize=address,undefined -g \
  -Itests/spiraton/shims -Iinclude -Isrc \
  tests/spiraton/test_core.c src/spiraton_core.c -o /tmp/spiraton-core-test
/tmp/spiraton-core-test
source /workspace/.setup/env.sh
make -j6
python3 tools/yokai/tester_spiraton_core_mgba.py
```

Le compilateur agbcc et le compilateur hôte ne remplissent pas les structures de la même manière : les diagnostics natifs utilisent des accesseurs scalaires, sans supposer les offsets hôte. Les sources des 151 Yo-kai ne sont pas modifiées.

Prochain travail : adaptation des routines de combat et intégration des données de Ligue, puis branchement de la scène lorsque les éléments artistiques auront été validés. Ne pas présenter cette étape A comme un boss déjà jouable.
