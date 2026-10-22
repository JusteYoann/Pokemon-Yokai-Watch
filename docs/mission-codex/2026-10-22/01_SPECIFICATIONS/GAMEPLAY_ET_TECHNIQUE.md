# Gameplay, intégration et ressources

## Base technique
- Décompilation FireRed, scripts et assets générés; suivre l'organisation du dépôt existant et ne pas migrer de moteur.
- Compilation publique documentée : `source /workspace/.setup/env.sh && make -j4` **uniquement si ces chemins existent dans l'environnement Codex**. Sinon suivre `INSTALL.md` et `RECUPERATION_PROJET/scripts/configurer_outils_debian.sh`.
- Deux variantes audio selon les sources disponibles : repli natif reproductible et intégration privée externe au dépôt. Le README du dépôt signale 13/15 OST actives; vérifier à nouveau.
- Ne pas inclure des enregistrements de musique ou ROM propriétaires dans des commits, patches publics contenant des données protégées, ou archives distribuées.

## Espèces, graphismes et données
- 151 Yo-kai capturables sur une sauvegarde; aucune espèce fantôme impossible, aucune évolution inaccessible.
- Tables cohérentes : species ID / Médallium / icônes / noms FR / sprites face-dos / shinies / palettes / cries / rencontres / évolutions / talents officiels Pokémon / attaques / dresseurs.
- Sprites GBA natifs avec transparence correcte et palettes vérifiées; éviter images IA à faux pixel art. Ne pas changer les shinies approuvés sans décision.
- Équilibrage starters et boss, progression EXP sans farming forcé; Multi Exp. permanent, y compris cas de captures et switches.
- Compatibilité des mécaniques réellement implémentées (types Fée/Acier/Ténèbres, split physique/spécial) à auditer; ne pas inventer un nouveau moteur.

## Maps, événements, interface
- Huit trophées et portes d'accès; test des flags, rematches, transitions, Cut/Surf/vol et progression.
- Portes Mystères, Zombie Night, Yopple HQ, Terr'heure, Triptic-tac, Temple Céleste : tester chaque entrée, sortie, blocage et retour.
- Médallium FR, équipes, sauvegarde/chargement, combat, crédits et postgame.
- OST : respecter la sélection des 15 de la mission finale du dépôt, pas une ancienne liste de 20; conserver les SFX Pokémon si c'est le choix de la dernière mission, avec niveaux équilibrés.

## Outillage QA et livraison
- Créer des sauvegardes de test : départ, après chaque trophée, avant/après chaque événement majeur, avant les quatre adversaires du Temple, avant boss final, après crédits, postgame, **151/151 et 100%**.
- Menu développeur **uniquement dans build debug**, avec téléportation contrôlée, flags, relecture d'événements, génération de rencontres et reset des variables QA; jamais visible par accident en version publique.
- Produire patch légalement distribuable quand possible, sources, docs, tests, empreintes, rapport d'anomalies et matrice de traçabilité. Une ROM privée reconstruite peut être un artefact local mais ne doit pas être distribuée sans droits appropriés.
