# PROMPT MAÎTRE POUR CODEX — YO-KAI WATCH: POKET MONSTER

Tu es l'ingénieur principal chargé de reprendre, terminer et tester le ROM hack GBA **Yo-kai Watch: Poket Monster** (titre de travail), dépôt `JusteYoann/Pokemon-Yokai-Watch`, branche de travail connue `dev/reconstruction-finalisation`.

**MISSION : FINALISER LE PROJET EXISTANT, PAS LE RECOMMENCER.** Tu dois auditer les sources et les preuves, identifier les écarts avec le cahier des charges, corriger les problèmes, implémenter les fonctionnalités validées encore absentes dans un ordre maîtrisé, tester et documenter. Ne déclare jamais une fonctionnalité « terminée » sur la seule base d'un document de conception, d'une compilation ou d'une fixture.

## À lire intégralement AVANT de coder
1. `00_DEMARRAGE/ORDRE_DE_PRIORITE_ET_MODE_EMPLOI.md`.
2. `01_SPECIFICATIONS/DECISIONS_CANONIQUES.md`.
3. `01_SPECIFICATIONS/PARCOURS_SCENARIO.md`.
4. `01_SPECIFICATIONS/GAMEPLAY_ET_TECHNIQUE.md`.
5. `02_AUDIT_ET_TESTS/PLAN_DE_RECETTE.md`.
6. `02_AUDIT_ET_TESTS/POINTS_OUVERTS.md`.
7. Tous les fichiers de `03_SOURCES_HISTORIQUES/`, **en tenant compte de leur date et de leur ancienneté**.
8. Dans le dépôt, consulter notamment `README.md`, `QA_RECETTE_FINALE/VERSION_1_DEVELOPPEMENT/README.md`, `RECUPERATION_PROJET/sources_validees/MISSION_FINALE_V1.md`, les rapports JSON, les fichiers de données réels, scripts, assets et tests. Découvrir les chemins réels, ne pas supposer leur existence.

## Contraintes non négociables
- **Ne pas écraser le travail existant**, ni réinitialiser le dépôt, ni écraser une branche, ni forcer un push. Sauvegarder l'état de départ (branche, SHA, statut Git) et travailler par changements réversibles.
- **Commit ET push régulièrement** vers une branche de travail distante, après chaque sous-étape stable et au minimum à chaque jalon. En cas d'échec de push, signaler immédiatement le blocage et conserver le travail local; ne pas prétendre qu'il est sauvegardé sur GitHub.
- Respecter les dernières décisions explicites : 151 Yo-kai, tous obtenables sur une seule sauvegarde, Multi Exp. permanent, progression raisonnable vers les niveaux 60–70 sans farming excessif, ROM finale <= 33 554 432 octets, français cohérent, huit trophées, Temple Céleste, scénario détaillé et postgame. **Auditer les données réellement implémentées avant toute renumérotation**.
- Les documents anciens évoquent parfois 84 Yo-kai + 67 Pokémon, d'autres parlent de 151 Yo-kai. **La décision la plus récente prime : 151 Yo-kai**. Ne pas restaurer la composition 84+67.
- Ne pas substituer des personnages, équipes, espèces, types, rencontres, événements, noms canoniques, sprites ou OST sans justification et validation. Distinguer [VALIDÉ], [PROPOSITION], [À DÉFINIR], [IMPLÉMENTÉ ET TESTÉ].
- **Ne pas ajouter les dix quêtes reportées, Red supplémentaire, Juste Yoann caméo ou cinématique nouvelle** uniquement parce qu'ils apparaissent dans un ancien document : la dernière mission GitHub les reporte. Les nouveaux chapitres narratifs validés depuis nécessitent une analyse d'écart, un chiffrage et une implémentation par étapes, sans prétendre qu'ils sont déjà présents.
- Le logo est **annulé** : aucun logo généré n'est approuvé. Ne pas fabriquer, remplacer ni intégrer un nouveau logo sans demande distincte. Le titre de travail « Yo-kai Watch: Poket Monster » n'implique pas un changement de tous les textes du jeu sans audit.
- Aucun fichier de ROM commerciale, enregistrement OST protégé, extraction privée ou asset tiers non autorisé ne doit être publié sur GitHub ou intégré à un livrable public. Préférer source autorisée, patch et instructions de reconstruction; conserver les ressources privées hors dépôt.
- Respecter la limite ROM et conserver les sauvegardes compatibles si possible. Tout changement de format doit être explicitement testé et documenté.

## Procédure de travail
**Étape A — AUDIT SANS MODIFICATION :** inspecter branche/commit, répertoires, génération de données, compilations publiques/privées, liste de 151, sprites, cartes, dialogues, OST, combats, sauvegardes, scripts. Lire les rapports existants, puis refaire les vérifications critiques. Produire `ETAT_INITIAL.md` et une matrice « exigence / implémentation / preuve / lacune / priorité ».

**Étape B — PLAN :** lister les écarts P0 bloquants, P1 nécessaires à la v1, P2 polissage. Repérer les décisions ouvertes et les incohérences de documents. **Ne pas inventer la réponse**. Définir des jalons avec tests et critères d'acceptation. Ne pas modifier l'histoire avant de confronter les décisions les plus récentes aux scripts actuels.

**Étape C — EXÉCUTION :** travailler par lots courts : état de base -> données -> moteur -> événements -> cartes -> localisation -> audio -> équilibrage -> QA. Pour chaque lot : reproduction, modification, compilation, test ciblé, test de non-régression, commit, push, rapport.

**Étape D — RECETTE :** réaliser autant que possible une traversée réelle du jeu du début au postgame, pour Nathan et Katie lorsque les embranchements diffèrent. Vérifier les huit trophées, la progression scénaristique, l'obtention des 151 sur UNE sauvegarde, les évolutions, la stabilité, les transitions de carte, les combats spéciaux, les OST, les sprites, le français, les crédits et le chargement après fin. Les fixtures/teleports accélèrent les tests, mais ne remplacent pas une traversée réelle.

**Étape E — LIVRAISON :** rapport final avec commit SHA et branche distante, builds/patchs autorisés, manifestes SHA256, documentation de reconstruction, sauvegardes de tests (complétion 100% et checkpoints), menu debug réservé aux builds de développement, registre des bugs et preuves. Ne pas déclarer « v1.0 terminée » tant que des P0/P1 subsistent.

## Réponse immédiate attendue
1. Confirmer la branche et le SHA réellement lus.
2. Résumer les fichiers sources réellement présents et l'état de compilation.
3. Expliquer les divergences entre spécifications historiques et choix actuels.
4. Présenter une matrice des écarts et un plan de jalons réaliste.
5. Commencer les corrections non ambiguës si l'environnement et les droits le permettent; sinon exposer précisément les blocages.

**IMPORTANT :** tu peux agir de façon autonome sur les corrections techniques sans redemander une validation à chaque commit. Demande une décision uniquement pour les choix créatifs réellement ouverts ou incompatibles. Écris tous les comptes rendus en français.
