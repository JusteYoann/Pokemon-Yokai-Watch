# Liaison Carmin / Océane — progression et Coupe

## Correction réelle

Dans la version `292bd4fb0`, remplir les 30 emplacements d’objets rares sans Boîte CT, puis parler au capitaine, produit le résultat natif suivant : `FLAG_GOT_HM01=true`, scène de départ=1, mais aucune CS01 dans le sac. Le capitaine annonçait donc une récompense qui n’avait pas été remise. Reproduction mGBA conservée dans `DEFAUT_AVANT.json`.

Le script contrôle maintenant le résultat réel de `additem` avant la fanfare, le drapeau de récompense et le départ. En cas de refus, le joueur peut libérer une place et revenir. La branche « pas de place » autrefois inutilisée est réactivée. Aucune nouvelle mécanique de combat ni aucun objet supplémentaire.

## Cohérence textuelle

Matt reste un rival technophile amical : ses dialogues n’affirment plus arbitrairement qu’il possède déjà 40 espèces et ne dénigrent plus le capitaine malade. Il indique la cabine, Coupe, le trophée d’Azuria et l’accès à Ariane. Ses trois équipes, son portrait, ses déplacements et son combat obligatoire restent identiques.

Le capitaine cite Carmin-sur-Mer et le trophée d’Azuria. Les messages de l’arbre et d’utilisation des capacités de terrain passent en français; variables et identifiants techniques conservés. Le message commun nom/capacité occupe deux lignes pour préserver la place des variables.

## Tests réellement effectués

Le script `tools/yokai/tester_oceane_progression_mgba.py` démarre de nouvelles parties dans mGBA, puis utilise des fixtures déclarées de carte, inventaire et équipe. Il ne simule pas une traversée depuis Bourg Palette.

- **6 cas capitaine** : Nathan et Katie, chacun avec inventaire normal, poche d’objets rares pleine sans Boîte CT, puis pile de CS01 saturée à 999. Refus sans départ, sauvegarde/rechargement, libération de place, récupération, récompense unique, vraie cinématique de départ et retour à Carmin, nouvelle sauvegarde/reprise.
- **6 combats de Matt gagnés par manette** : les trois choix de starter avec les deux protagonistes, déclenchés sur les trois cases d’approche natives. Lecture de chaque équipe générée, scène terminée persistante après rechargement. Équipe de test Komasan40 avec statistiques générées et Lance-Flammes assigné : test des événements, **pas** de l’équilibrage au niveau attendu.
- **2 cas Coupe** : refus sans deuxième trophée, retrait natif de l’arbre avec le trophée et Coupe, animation de terrain, passage sur sa case.
- **70 lignes** mesurées avec la police du moteur, limite 208px; nom joueur remplacé par 7W, surnom par 10W et nom de capacité par 12W pour le test. Largeur maximale constatée 203px.
- Compilations publique et privée. Version privée **31 589 579 octets**, donc moins de 32 Mio, 26 OST préservées. Empreintes dans `BUILD_NON_REGRESSION.json`.
- Seuls quatre fichiers actifs de scripts/textes changent. Aucune modification des équipes, espèces, rencontres, sprites, palettes, animations de combat, Multi Exp. ou sources musicales.

Les captures sont des sorties natives mGBA, pas des compositions. Images de retour au port, arbre retiré et introduction du combat ouvertes et examinées.

## Piège du pilote corrigé pendant la recette

Un premier essai de reprise montrait de l’eau à la place du port. Le pilote appelait `TrySavingData` sans `SaveMapView`, contrairement au véritable menu (`StartMenu_PrepareForSave`). Cela réinjectait une ancienne vue de carte au rechargement : anomalie de la fixture, pas preuve d’un défaut de la cinématique. Le pilote prépare désormais la vue et compare les 25 cases autour du joueur avant/après chaque reprise; toutes les captures publiées de la version corrigée proviennent de cette séquence. Aucune correction arbitraire du moteur de carte.

## Limites et prochaine reprise

- Le capitaine reste **provisoire** comme donneur de Coupe. La future attribution à Bérénice, les Portes Mystères et le Dr Jobard ne sont pas annoncés comme intégrés : rôles précis, ressources et chapitre complet restent à traiter conformément au pack.
- Pas de nouvelle traversée complète, pas de test d’équilibrage de Matt, pas de nouvelle campagne de défaites dans ce lot.
- La correction empêche de nouvelles remises fictives. Elle ne répare pas automatiquement une ancienne sauvegarde où le bateau serait déjà parti sans la CS. Aucun fichier utilisateur présentant ce cas n’a été fourni.
- Suite prévue : cadrer le chapitre Portes Mystères/Dr Jobard et la transition vers Yopple/Safrania, en préservant les ressources artistiques approuvées. Les autres anomalies du scénario global restent ouvertes.

```sh
source /workspace/.setup/env.sh
YOKAI_QA_ROM=$PWD/pokefirered_audio.gba YOKAI_QA_ELF=$PWD/pokefirered_audio.elf python3 tools/yokai/tester_oceane_progression_mgba.py
```

Pour reproduire le défaut historique, utiliser **la ROM et l’ELF de 292bd4fb0** avec `--reproduce-before`. Le mode attend volontairement l’ancien échec; il ne doit pas passer sur la version corrigée.
