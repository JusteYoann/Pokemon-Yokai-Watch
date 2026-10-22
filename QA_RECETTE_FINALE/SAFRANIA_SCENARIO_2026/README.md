# Safrania — Ariane et le quatrième trophée

La porte existante de l'arène donne accès à une station orbitale explorable : hall, compartiment énergie, navigation et passerelle. Trois paires de téléporteurs natifs sont réciproques. Les consoles se réactivent dans l'ordre énergie, navigation, communication ; chaque état est sauvegardé. Le troisième trophée est nécessaire, et le passage comme l'interaction directe avec Ariane refusent une préparation incomplète. Chaque compartiment conserve son retour vers la sortie.

La disposition, les petites manipulations et les dialogues sont des choix de réalisation à relire créativement. La station utilise un tileset secondaire dédié composé de graphismes natifs du Musée : technologie, maquette lunaire et vaisseau. Aucun nouvel artwork de tiers n'est ajouté. Les sprites existants d'Ariane et d'Usapion sont réutilisés et leur présence simultanée a été examinée dans les captures mGBA. Aucun nouveau sprite n'est revendiqué par ce lot.

Le Sbire qui bloquait cette porte disparaît après le troisième trophée ; les autres événements de la Sylphe et de la ville sont conservés. Les anciens caméos d'Ariane et d'Usapion sur la Route25 sont masqués, sans supprimer leurs scripts historiques. Leur revanche originale à cinq partenaires est disponible dans la station au postgame. La Pierre Lune reste unique ; une récompense historiquement gagnée mais non reçue reste récupérable.

## Combat et progression

Ariane utilise Navétéran28, Robonyan28, Mognyan29 et Usapion30, sans objet tenu ni soin de Dresseur. Le Pokédex actif affiche « Usapyon » pour la même espèce ; aucun identifiant n'est changé. Niveaux et attaques restent provisoires. Le profil actif est dans `data/yokai/scenario_safrania.json` ; les anciennes équipes verrouillées sont conservées. Après une réimportation intentionnelle des équipes historiques, réappliquer les profils Argenta, Azuria, Carmin puis Safrania avant compilation.

La victoire donne le quatrième trophée, son flag natif et la CT04 ; elle ne donne pas le sixième. La serre de Céladopole reste un combat facultatif avec sa CT19, sans trophée. Un Sac plein conserve chaque récompense en attente, sans exiger de revanche ni permettre de duplication.

`FLAG_SCENARIO_ARIANE_TROPHY` distingue le nouveau quatrième trophée d'un ancien badge gagné à Céladopole. Le Temple exige cette preuve en plus des huit flags natifs. Une ancienne victoire de Morgane avec son ancien sixième badge est reconnue comme réussite d'Ariane ; les badges historiques restent conservés. Les anciennes sauvegardes construites pour la recette sont rechargées par Continuer : position sûre et nouveaux objets dans l'arène, retrait des caméos Route25 et actualisation du garde de Safrania. Le format de sauvegarde ne change pas.

## Vérifications et limites

- `TEST_CHAPITRE_MGBA.json` : Nathan et Katie, vraie porte de ville, consoles, refus, téléporteurs, retours, sauvegarde/reprise, combat natif, quatrième trophée, CT et sortie. Fixture explicite Komaous33, Whisper32, Cigallard32, IV15 et statistiques ordinaires ; attaques apprises réordonnées, aucune victoire forcée.
- `TEST_MIGRATION_MGBA.json` : défaite réelle, sept combinaisons incomplètes des systèmes, absence du troisième trophée, sauvegardes anciennes préparées puis écrites/relues en Flash, caméos, CT/Pierre Lune en attente, combat réel de la serre sans trophée et revanche postgame. La serre utilise la même équipe ordinaire. La revanche utilise explicitement Hovernyan100 avec statistiques999 : contrôle du déroulement et des récompenses, aucune validation de son équilibrage.
- `TEST_ACCES_TEMPLE_MGBA.json` : 256 combinaisons de trophées, huit refus de passage, entrée réelle, persistance et distinction entre ancien badge de Céladopole et ancienne victoire de Morgane.
- `TEST_EQUIPES_ACTIVES_MGBA.json` : construction native des 640 équipes, sans prétendre jouer 640 combats.
- `CONTROLE_SOURCES.json` : graphe des déplacements et retours, passage fermé, téléporteurs indispensables, collisions, trois sorties et stabilité de tous les identifiants de cartes/layouts.
- `LARGEURS_DIALOGUES.json` : 125 lignes avec police native et prénom de sept W.
- `REGRESSION_CONTINUE_ARGENTA_MGBA.json` : reprise native d'anciennes positions d'Argenta après modification du callback partagé.

Les SHA des ROM testées figurent dans les rapports. Compilation publique avec audio de remplacement ; ROM locale ignorée, non publiée. Ces essais sont des fixtures déclarées, sans partie continue depuis Bourg Palette ni sauvegarde historique fournie par un joueur. L'équilibrage de tous les starters, l'habillage final des Portes Mystères de Carmin et le reste du scénario demeurent à réaliser/valider. Le nouveau Temple n'est pas intégré par ce contrôle d'accès. Les dialogues ordinaires historiques de la serre ne sont pas tous traduits.

Reproduire après `source /workspace/.setup/env.sh` et `make -j4` :

```sh
python3 tools/yokai/verifier_safrania_sources.py
python3 tools/yokai/tester_safrania_scenario_mgba.py
python3 tools/yokai/tester_safrania_migration_mgba.py
python3 tools/yokai/tester_textes_safrania_mgba.py
python3 tools/yokai/tester_acces_temple_mgba.py
python3 tools/yokai/tester_equipes_mgba.py
python3 tools/yokai/tester_argenta_continue_mgba.py
```

Les trois derniers outils écrivent dans leurs dossiers historiques : les résultats de cette compilation ont été copiés ici, puis les preuves historiques d'équipes et d'Argenta restaurées.
