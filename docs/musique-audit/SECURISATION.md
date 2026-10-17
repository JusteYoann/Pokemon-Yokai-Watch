# Préservation du développement avant l’audit musical

L’état initial a été vérifié avant toute écriture de documentation musicale : branche locale `qa/recette-finale`, HEAD `2f8b5b3911b75480ae447e027c9624300e57dae9`, nombreuses modifications non commitées et ressources non suivies. Il ne suffisait donc pas de noter le nom de la branche.

## Points de restauration

1. Instantané hors dépôt : **`/workspace/scratch/music-before/sources-and-derived.tar.gz`**, avec 28775 fichiers et manifeste SHA256 `manifest.json`. Les sources et dérivés préexistants sont conservés, dont la ROM locale ; les dossiers Git, build, caches Python et la dépendance compilateur agbcc ne sont pas inclus dans ce tar. Aucun de ces dossiers n’est supprimé ou déplacé.
2. Bundle des références Git avant sauvegarde : **`/workspace/scratch/music-before/branches-before.bundle`**. Il conserve les branches/commits d’avant l’intervention, sans fichiers d’authentification Git. Les diffs index/worktree et l’état complet des fichiers non suivis sont également sauvegardés à côté.
3. Commit local **`145044ec29f4ad7ee03c1942e8a925d15a9f89e1`** sur `qa/recette-finale` :5637 fichiers, regroupant les missions préexistantes de données, graphismes, personnages, dialogues, shiny et recette. Il sauvegarde les fichiers de projet non ignorés ; les dérivés ignorés restent sur disque et dans le tar lorsqu’ils étaient concernés. Les caches Python préexistants restent non suivis et intacts.
4. Branche **`audio/direction-musicale-audit`** créée depuis ce commit, sans merge ni reset. Les modifications de cette phase sont limitées à `docs/musique-audit/`.

Les autres branches existantes ne sont ni fusionnées ni écrasées. Le commit local de sauvegarde ne représente pas une nouvelle validation de jeu : `QA_RECETTE_FINALE/VERDICT_FINAL.md` demeure un rapport historique intact, avec son verdict NON PRÊT et ses limites. Ses phrases d’état Git précèdent cette sécurisation ; le présent document décrit la situation actuelle.

## Vérifications

Le manifeste initial est recomparé après l’audit. Les ressources de gameplay, cartes, scripts, sprites, noms, équipes et audio existants doivent rester identiques octet par octet. La ROM conserve son SHA256 `84d3bffbb7e74322aa69d5df211f774576d00b1e3e16eec3794c5b74fc66e186`. La relance normale `make -j4` ne reconstruit rien et réussit. Les erreurs d’un essai `make -q` concernent le mode requête propagé aux sous-makes des outils ; elles ne sont pas présentées comme une compilation échouée du jeu. Le journal de contrôle est dans `preuves/PRESERVATION_ET_VALIDATION.json`.

Le tar a été créé avant l’arrivée des MP3 et avant les fichiers de l’audit. Les références musicales téléchargées restent sous `/workspace/attachments/` et le scratch d’analyse, hors du dépôt du jeu. Aucun MP3 ni archive OST n’entre dans un commit.

## Publication

**Aucun push, PR ou merge n’est effectué.** La demande impose de coordonner toute publication/fusion de la recette avec le créateur ; sauvegarder des commits locaux n’autorise pas à prétendre qu’ils sont visibles sur GitHub. Le point de restauration n’est pas une garantie de récupération après destruction de l’environnement : conserver le dépôt local et les archives, puis convenir séparément de la publication du travail complet.
