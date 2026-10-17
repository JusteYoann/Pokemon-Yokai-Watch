# Pokémon × Yo-kai Watch — Direction musicale et audit des 7 OST (v1.0)

## Mission et ordre des opérations

Tu travailles sur le ROM hack `JusteYoann/Pokemon-Yokai-Watch`. Je fournis **7 archives ZIP**, chacune représentant la bande-son d'un jeu Yo-kai Watch distinct. Les MP3 ont déjà des noms structurés contenant numéro de piste, titre anglais et jeu d'origine. **Conserve les noms et les associations aux jeux** lors de l'inventaire.

**Étape 0 : sécuriser le travail existant.** Le dernier rapport de recette annonce une branche **locale** `qa/recette-finale`, non publiée sur GitHub. Avant tout changement musical, identifier l'état des branches, commits, changements non enregistrés et tests. Préserver ce travail sans l'écraser. Ne pas supposer qu'un rapport de tests équivaut à une validation finale du jeu. Coordonner la publication de cette branche avec l'utilisateur avant toute fusion. Ne pas lancer une refonte musicale sur une branche non sécurisée.

**Étape 1 : analyser les OST, inventorier et proposer, sans remplacer encore les musiques.** Décompresser les sept archives, repérer chaque fichier, doublon, variante, durée, boucle potentielle, tempo et ambiance lorsque les outils permettent effectivement de l'établir. S'aider des noms et du lexique ci-dessous, sans déduire une ambiance musicale uniquement du titre. Analyser la musique réellement, avec les moyens disponibles; signaler honnêtement lorsqu'une écoute ou une analyse perceptive n'a pas été possible.

**Étape 2 : inventorier TOUTES les situations musicales de Pokémon Rouge Feu.** Villes, routes, grottes, bâtiments, Team Rocket, combat sauvage, dresseurs, champions, Conseil 4, Matt, légendaires, Enma, caméos, événements, postgame, menus, génériques, etc. Vérifier les déclencheurs audio réels dans les scripts, y compris les événements ajoutés au hack.

**Étape 3 : préparer une proposition globale d'affectation.** Pour chaque emplacement, comparer le thème Pokémon Rouge Feu original et les candidats Yo-kai Watch. Choisir la musique qui rend **la scène et l'ensemble du jeu meilleurs**, même si cela signifie conserver la musique Pokémon. Liberté d'écarter des MP3, de réaffecter une musique à un contexte très différent de son usage d'origine, et d'exploiter les musiques moins célèbres. Aucun quota Pokémon/Yo-kai Watch. S'assurer d'une cohérence sonore et émotionnelle sur l'aventure complète, d'une progression dans la tension des combats, de transitions harmonieuses et de thèmes suffisamment variés pour éviter la fatigue auditive. Les thèmes importants (Matt, Enma, Giovani, Conseil 4) doivent se distinguer lorsque cela est pertinent; identifier les leitmotivs et variations plutôt que faire doublon involontaire.

**Étape 4 : faire valider la proposition par l'utilisateur AVANT toute intégration musicale définitive.** Ne pas commencer par convertir 230 Mo de MP3 en masse. Présenter les choix, leurs justifications et les morceaux écartés. Produire si possible de courts aperçus techniques seulement à partir de ressources autorisées, en expliquant clairement les limites.

**Étape 5, seulement après validation : faisabilité GBA, arrangement, intégration et tests.** Examiner le moteur m4a/Sappy et les outils du dépôt. Ne pas confondre MP3 rééchantillonné, conversion MIDI automatique approximative et véritable arrangement séquencé pour GBA. Un MP3 polyphonique seul ne garantit pas une transcription fidèle. Étudier les limites ROM, RAM, nombre de voix, banques de sons, fréquence, boucles et charge CPU. Conserver une palette instrumentale homogène entre morceaux issus de jeux différents. Tester sur émulateur le volume, les entrées/sorties de zones, les transitions, les boucles, les reprises après combat, la sauvegarde et les éventuels conflits de pistes. Ne déclarer aucun succès sans preuve.

## Lexique EN → FR et contexte narratif (fourni par le créateur)

| Terme anglais dans les OST | Correspondance / contexte |
|---|---|
| Springdale | **Granval-sur-Mer**, ville de départ de Yo-kai Watch et ville de Nathan. **Ne pas renommer la région Kanto dans le ROM hack.** |
| Nate / Nate's | **Nathan**, protagoniste Yo-kai Watch. |
| Katie / Katie's | **Katie**, protagoniste alternative. |
| Natsume / Natsume's | **Natsume**, fille de Nathan venant du futur, protagoniste de Yo-kai Watch 4. |
| Hailey Anne / Hailey Anne's | **Ariane Célestin**, personnage de Yo-kai Watch. |
| Dukeville | Ville western des canyons dans Yo-kai Watch 3. |
| Zombie Night | Événement nocturne de Pistachburg dans Yo-kai Watch 3 : zombies, survie et cloche à activer. |
| New Yorkai | Capitale du monde des Yo-kai. |
| Bada Bing Tower | Haute tour de la Mafiamille dans Yo-kai Watch 3, ascension d'environ 50 étages avant le combat contre Don Morleone. |
| The Ghoulfather | **Don Morleone**, antagoniste de Yo-kai Watch 3. |
| Blasters | Équipe de chasseurs de fantômes inspirée de Ghostbusters ; Jibanyan, Whisper, Komasan, Coach Antonic, Usapyon, avec Felipaix, Nanpart et Chauvekipeut dans le premier jeu. |
| Blasters T / Blasters Basecamp | Équipe de chasseurs de trésors à l'ambiance aventure/Indiana Jones et leur camp dans Yo-kai Watch 3. |
| Club Koma | Boîte de nuit où Komajiro (frère de Komasan) joue souvent. |
| Time For Horse | Thème de la chevauchée à travers les canyons de Dukeville. |
| San Fantastico | Ville portuaire de Yo-kai Watch 2. |
| Harrisville | Campagne et village de la grand-mère de Nathan. |
| Old / Past (dans YW2) | Contexte de voyage dans le temps environ 60 ans en arrière, avec Hovernyan et Nathaniel ou Michael, grands-pères respectifs des protagonistes. |
| Venoct | **Octorgone**. |
| Master Nyada | **Maître Nyada**. |
| Wildwood | Forêt de Granval. |
| Infinite Tunnel | Tunnel mystérieux pouvant s'étendre sur des distances immenses selon les interactions. |
| Terror Time | Événement : ville grisâtre et poursuite par un Oni dont le joueur doit s'échapper. |
| Robonyan 3000 | Référence au shiny noir et doré de Robonyan 28, avec cornes. |
| Captain Thunder | Boss inspiré d'Usapyon. |
| Hinozall | **Domniscian**. |
| Whismellowman | Boss final de Yo-kai Watch Blasters, inspiré de Whisper et du méchant final de Ghostbusters. |
| Zazel / Zazelmare | Zazel est le second du Seigneur Enma au palais. Zazelmare est sa forme antagoniste temporaire dans Blasters. Enma l'arrête. |

**Attention** : Le contexte d'origine renseigne la signification du nom, **pas une affectation obligatoire**. Le titre « Time For Horse » peut parfaitement devenir un thème de route si son arrangement fonctionne ; un thème de boss peut être écarté. Il faut écouter/analyser plutôt que se fier aux seules étiquettes.

## Direction artistique irrévocable

- Le jeu reste **Pokémon Rouge Feu dans sa structure**, avec 151 Yo-kai, Nathan, Katie, Matt, les caméos et les scripts spécifiques. La musique doit renforcer la double identité, pas éliminer toute identité Pokémon.
- **Ne pas remplacer pour remplacer.** Si un thème Pokémon est meilleur, le conserver.
- **La célébrité d'une musique n'est pas un critère de préférence.** Les thèmes d'ambiance secondaires peuvent être plus adaptés qu'un thème culte.
- **Ne pas forcer l'usage des 7 archives en entier.** Les morceaux non retenus restent dans l'inventaire, pas dans la ROM.
- Évaluer chaque affectation en **contexte global** : rythme narratif, transition entre lieux, répétition, variété, intensité et style GBA cohérent.
- **Ne pas modifier les événements, combats, stats, sprites ou noms** dans le cadre de cette tâche audio.
- Les fichiers MP3 sont des **références de travail** ; ne pas incorporer sans nécessité tous les MP3 volumineux dans le GitHub du jeu ni dans la ROM.

## Livrables de la première phase : audit, PAS intégration

Créer un dossier de documentation `docs/musique-audit/` sur une branche de travail sécurisée, avec au minimum :

1. `INVENTAIRE_OST.csv` : archive, jeu, piste, titre, chemin, durée, éventuels doublons, remarques, éléments audibles et niveau de confiance.
2. `EMPLACEMENTS_MUSICAUX_KANTO.csv` : identifiant de musique du moteur, maps/scripts/événements utilisateurs, morceau Pokémon original, contraintes et rôle narratif.
3. `PROPOSITION_BANDE_SON.csv` : emplacement, morceau Pokémon de base, candidat Yo-kai Watch et jeu, décision **CONSERVER / REMPLACER / A_VALIDER**, justification et alternative.
4. `MUSIQUES_ECARTEES.csv` : fichier d'origine, raison de non-utilisation et alternatives plausibles éventuelles.
5. `ANALYSE_COHERENCE.md` : vue de l'ensemble du parcours, contrastes, répétitions, transitions, lieux importants, thème rival/boss, et limites de l'analyse.
6. `FAISABILITE_GBA.md` : moteur, formats, coût/qualité de la conversion, risques, limites, évaluation honnête de ce qui peut être arrangé à partir du MP3 seul.

**Stopper à la fin de l'étape de sélection pour validation explicite par le créateur.** Ne pas prétendre avoir écouté les pistes si les outils ne le permettent pas, et ne pas déclarer la compilation ou le jeu validés sans vérification.

## Droits musicaux

Les musiques de Yo-kai Watch sont protégées. Les archives MP3 ne sont pas à redistribuer publiquement dans le dépôt. Une adaptation instrumentale ou GBA peut aussi relever des droits sur les compositions. Pour une distribution publique du hack avec ces morceaux, vérifier les autorisations nécessaires ; à défaut, privilégier des compositions originales autorisées ou des ressources légalement utilisables. Conserver le dépôt du jeu séparé des MP3 fournis en référence lorsque leur redistribution n'est pas autorisée.
