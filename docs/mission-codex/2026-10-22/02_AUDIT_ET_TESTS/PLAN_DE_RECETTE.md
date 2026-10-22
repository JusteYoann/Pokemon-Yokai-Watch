# Plan de recette obligatoire

## P0 — sécurité / compilation
- Vérifier HEAD, branche, modifications locales; créer branche dédiée sans perte de travail; commits + pushes à chaque jalon.
- Build reproductible, aucun crash au lancement, ROM <= 33 554 432 octets, sauvegarde/reprise intactes, aucune ressource privée poussée.
- Établir différence entre build public et privé (audio), avec provenance de chaque source.

## P1 — jeu complet
- Vérifier 151 species IDs et 151 entrées Médallium, toutes obtenables en **une sauvegarde**, rencontres/évolutions/cadeaux/échanges vérifiés par tests et parcours.
- Tester 3 starters, équilibrage stats, évolutions (notamment Pierre Foudre et Pierre Eau), distribution d'EXP et progression niveaux 60–70.
- Tester les deux protagonistes et Matt, huit trophées, accès Temple avec 7 refusé / 8 autorisé, Zazel, quatre boss sans doublon, Matt soigne au bon moment, Morleone et climax, Panthéon.
- Tester chapitres Carmin/S.S. Anne, Yopple HQ, Parmanie, Zombie Night, Terr'heure et Cramois passé/présent.
- Tester rencontres légendaires fixes, postgame Limbes Éternelles et Sanctuaire Divin, retour libre et absence de softlock.
- Vérifier texte FR, noms, accents, collisions, palettes shiny, sprites, SFX/OST et animations de capacités.

## P2 — finitions
- Cohérence dialogues, densité de rencontres, lisibilité des interfaces, qualité des transitions, rééquilibrage des boss, QA visuelle des maps.

## Preuves attendues
Pour chaque critère : commande ou procédure, capture/log, résultat, SHA de la build, état « PASS / FAIL / NON TESTÉ / BLOQUÉ ». Différencier analyse statique, test automatisé, émulateur avec fixture, traversée réelle et contrôle visuel humain.

## Livrables
`ETAT_INITIAL.md`, `MATRICE_ECARTS.csv`, `PLAN_JALONS.md`, `RAPPORT_TESTS.md`, `BUGS_OUVERTS.md`, `LIVRAISON.md`, `MANIFEST_SHA256.txt`, sauvegardes de test et checkpoints, menu debug isolé, patch/source autorisés, notes de reconstruction. Pas de déclaration v1.0 si des critères majeurs manquent.
