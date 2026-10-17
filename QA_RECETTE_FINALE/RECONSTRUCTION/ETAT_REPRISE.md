# État de reprise vérifiable — 17 octobre 2026

Branche active : **dev/reconstruction-finalisation**. `master` reste préservée. Le commit distant a été vérifié avant reprise : `06fb588afaf038ea31235b0f7b605e56153629f3` (Ariane). La seule modification locale restante était le workflow CI, publié séparément dans `b1ad73110`. Aucune reconstruction des étapes déjà présentes n'a été relancée.

## Sources présentes et contrôlées

| Domaine | État et preuve |
|---|---|
| 151 espèces, noms, statistiques, talents, évolutions, CT/CS | Sources actives ; CONTROLE_ROM.json et TESTS_MGBA_MOTEUR.json. |
| Graphismes normaux et 14 redesigns approuvés | 906 ressources liées ; 137 espèces protégées comparées à l'instantané historique. |
| Shiny | 84 éligibles, 67 sans statut ; verrou testé. Les dessins finaux et cornes de Robonyan 28 restent incomplets. |
| Apprentissages et noms français des capacités/talents | 151 listes / 1 977 lignes ; contrôles ROM et natifs. Réserve sur la double relecture humaine de l'OCR. |
| Obtentions | Tables sauvages et cadeaux reconstruits ; couverture de graphe 151. Cela ne prouve pas une partie complète. |
| Légendaires | Kyubi au Mont Braise, Mademoaiselle aux Îles Écume, Octorgone à la Centrale ; Enma verrouillé par son duel caméo. |
| Équipes et rival | 639 équipes contrôlées, 17 boss verrouillés ; Matt nommé et dessiné. |
| Multi Exp. | Actif et testé en combat. Équilibrage du parcours encore à faire. |
| Caméos | Ariane/Usapion et Seigneur Enma restaurés ; Nathan/Katie à Céladopole restaurés ; Nathaniel/Michael à Parmanie et Wyatt à Cramois’Île restaurés ; Domniscian/deux employés et Don Morleone/trois Mafiamille actifs ; thèmes DPCM encore en attente. |
| Dix quêtes | Quête 8 partielle par l'événement Enma partagé ; neuf autres non reconstruites ; aucune annoncée complète. |
| 20 OST DPCM | Direction et références préservées ; intégration active : zéro. Inspection du pilote dans AUDIO_DPCM_PREPARATION.md. |
| Nathan/Katie et autres overworld | Séries originales complètes intégrées : 73 emplacements par protagoniste, tests natifs terrain/combat réussis. Introduction avec prénom personnalisable/Matt fixe, Surf, carte dresseur, Panthéon et crédits testés nativement pour les deux sexes. Enma/Kyubi et Matt/Ariane présents ; autres overworld à produire. |
| Français complet, animations, aventure | Incomplets ; les tests natifs ciblés ne remplacent pas une traversée réelle complète. |

Les essais Enma utilisent les contrôles du jeu pour refus, défaite, victoire, revanches et capture à la Master Ball. Téléportations, niveaux artificiels et option SET de la fixture sont documentés dans TEST_ENMA_MGBA.json. Les 56 lignes ajoutées Ariane/Enma tiennent dans 208 pixels avec la police native.

## Sauvegarde et reproductibilité

Le clone indépendant récupéré directement depuis GitHub reproduit exactement le jalon Matt/Ariane (`REPRODUCTIBILITE_ARIANE.json`). Les résultats de jalons ultérieurs doivent être lus dans leur propre rapport de clone ; ne pas extrapoler une ancienne empreinte aux changements suivants.

Aucune ROM commerciale, ROM modifiée ou musique protégée n'est publiée. Les graphismes sources, outils et scripts requis pour le build public actuel sont suivis. Une future compilation avec les OST privées nécessitera leur fourniture séparée et ne sera pas musicalement identique sans elles.

La CI est publiée, mais son résultat distant n'a pas pu être consulté (proxy API GitHub : 403). Les preuves locales n'en dépendent pas. Les anciens rapports qui citent des commits/environnements perdus restent des archives ; leur présence ne signifie pas que ces fonctionnalités ont été récupérées.

## Poursuite autorisée

Continuer les caméos manquants, Nathan/Katie et les overworld, les shiny finaux, les quêtes et le pipeline musical DPCM, puis la traduction, l'équilibrage et la recette complète. Préserver les choix validés et publier par jalons testés ; aucun nouveau feu vert n'est requis pour les travaux déjà autorisés dans MANDAT_RECONSTRUCTION.md.

**Verdict global : NON PRÊT.** Aucun parcours intégral ni contrôle exhaustif des 354 animations n'a encore été réalisé.

Jalon protagonistes actif : TEST_PROTAGONISTES_MGBA.json, sources graphics/yokai_characters/{nathan,katie,matt}, découpe et conversions reproductibles dans tools/yokai. Les premiers aperçus GIF peuvent être noirs dans l’interface ; chaque animation possède aussi une planche PNG opaque de vraies captures. Reprise : continuer les caméos manquants, sans régénérer les dessins déjà intégrés.

Caméo Nathan/Katie de Céladopole : actif, testé avec les deux sexes en aventure et postgame, récompense unique/retry sac plein/revanches/Flash/défaite. Données data/yokai/cameo_protagonistes.json ; preuve TEST_CAMEO_PROTAGONISTES_MGBA.json. Prochaine étape : Nathaniel/Michael et Wyatt (références visuelles consultées ; nouveaux dessins en préparation), puis deux groupes de boss restants.

Nathaniel/Michael/Wyatt : intégration active et22 contrôles natifs réussis, TEST_CAMEOS_AVENTURE_MGBA.json ; quatre directions et combats visibles dans preuves/. Source originale de ces dessins, conversion et intégration ponctuelle suivies. Prochaine étape : Domniscian/employés puis Don Morleone/Mafiamille, avant shiny finaux/quêtes/DPCM. Références de ces deux groupes ouvertes, nouvelles sources artistiques en préparation.

Sources artistiques Domniscian/deux employés et Don Morleone/trois Mafiamille créées et converties, aperçus PNG vérifiés ; elles ne sont PAS ENCORE ACTIVES à ce point de sauvegarde. Source dans graphics/yokai_characters/cameos_boss/source/, convertisseur convertir_cameos_boss.py. Palette commune par groupe prévue pour éviter les conflits entre PNJ simultanés ; Domniscian overworld32×32, autres16×32, trois directions plus miroir. Reprise concrète : intégrer les deux groupes postgame avec employés/prérequis, récompenses uniques (Pierre Foudre /3 Pépites), puis tests natifs et publication. Le clone GitHub du jalon aventure3abcd3586 produit la même ROM3d041e20… (REPRODUCTIBILITE_CAMEOS_AVENTURE.json).

Jalon caméos complet côté graphismes/scripts/équipes/récompenses : les 7 groupes sont actifs. Domniscian/Sylphe 11F et Don Morleone/Entrepôt Île 5 : TEST_CAMEOS_BOSS_MGBA.json(18 contrôles) et TEST_AFFICHAGE_GROUPES_BOSS_MGBA.json. Leurs sources artistiques auparavant inactives sont maintenant liées et vérifiées. Reste : thèmes privés DPCM, trajets réels, difficulté, puis shiny finaux(84 éligibles / 67 sans statut), quêtes et recette. Prochaine reprise : architecture des graphismes shiny spécifiques pour les modifications de silhouette approuvées, dont cornes Robonyan28 ; les normales protégées restent intouchées.

## Directives actualisées — prioritaires

Voir `RECUPERATION_PROJET/sources_validees/NOUVELLES_DIRECTIVES_FINALISATION.md`, lu intégralement. L’aventure et les 151 obtentions restent prioritaires, puis personnages/caméos, **20 OST DPCM avant quêtes facultatives**, français, graphismes essentiels et recette. Les dix quêtes ne bloquent plus la première version ; conserver les événements fonctionnels. Chen invente la Watch passive et étudie le Médallium ; Léo invente le PC. Seigneur Enma et l’espèce Enma sont distincts ; victoire = déblocage, jamais cadeau/capture automatique. Kanto et légendaires inchangés. L’introduction propre et stable prime sur une nouvelle cinématique risquée. Somewhere A Bit Dodgy reste réservé au Repaire Rocket.

Sauvegarde artistique Robonyan28 : paire noire/or à cornes et sources dans `graphics/yokai_shiny_artwork/019/`, conversion reproductible ; **inactive** à ce jalon. Ne pas annoncer ses cornes visibles en jeu. Le contrôle indépendant des caméos a révélé les limites du pilote A seul ; diagnostic et reprise du test en cours, équipes inchangées.

### Dernier jalon réellement terminé

Nouvelles directives enregistrées ; Chen/Watch passive/Médallium/Ligue et origine distincte d’Enma intégrés dans les premiers dialogues. Compilation, intro réelle garçon/fille, Enma victoire-déblocage-capture unique, largeurs natives réussies. Nouveau clone GitHub ce6359ba0 : ROM identique f0fc873c…, tests natifs introduction, boss et décodeur réussis avec outils indépendants ; voir REPRODUCTIBILITE_DIRECTIVES.json. Ancien défaut du pilote A seul corrigé et échecs conservés, aucun changement aux équipes pour faire passer les tests.

Pipeline DPCM : encodeur restauré, comparaison exacte des 710 échantillons synthétiques au décodeur ARM ; essai réel du mixer avec introduction unique, plus de onze boucles, bruitage/cri et retour API à MUS_PALLET. Cela ne constitue pas l’intégration des 20 OST. Prochaine étape musicale : extraction privée des références, points de boucle par morceau, système optionnel de ressources privées et affectations validées ; tests réels vélo/carte/combat, coûts ROM et écoute. Voix DPCM : bit 0x20 obligatoire (0x28 testé en fréquence fixe).

Les dix quêtes deviennent facultatives et ne doivent pas passer avant les musiques et la stabilisation. Protagonistes et sept groupes caméos sont présents ; ne pas les refaire. Léo, overworld statiques manquants, 84 dessins shiny finaux (dessin Rob28 à cornes sauvegardé mais inactif), français intégral et recette d’aventure restent incomplets. **NON PRÊT**, aucune traversée complète annoncée.

Préparation audio complétée : quatre scripts DPCM/test, extracteur libarchive et préparation batch ; vingt sources intégrales effectivement encodées, 23 248 952octets, trop volumineuses telles quelles (base + samples=36,92Mio >32Mio). Tous les thèmes requis sont disponibles. Rapports PREPARATION_20_OST_DPCM.md /MESURES_20_OST_DPCM.json ; aucune suppression décidée. Privé : `/workspace/private-audio/recovery/*.rar`, `/workspace/private-audio/extracted/manifest-private.json`, `/workspace/private-audio/dpcm-full-sources/encoding-metadata.json` et01..20.wav/.dpcm. Ne pas publier ces enregistrements. Prochaine tâche : choisir des sections intro/boucle, gagner les répétitions enregistrées, mesurer raccords et coûts, puis intégrer optionnellement sans ressources privées obligatoires pour le build public.

Correction graphique Enma terminée : l’objet de Caverne Azurée partageait à tort le sprite du Seigneur Enma. Nouvelle ressource féline originale32×32 d’après le front validé150, ID168/palette1126, source et conversion suivies ; Seigneur Enma humain inchangé154 au Mont Braise. Build et tests natifs refus/défaite/victoire/revanches/Flash/vraie capture réussis ; le Médallium n’enregistre pas de capture lors de la victoire contre le dresseur. Capture carte examinée. Rapport DISTINCTION_GRAPHIQUE_ENMA.md ; ROM locale c8cea690… . Les anciennes preuves de clones portent leurs propres empreintes et ne valident pas automatiquement cette nouvelle ressource.

Jalon graphique Enma reproduit depuis GitHub772d41cb4 avec la chaîne indépendante : ROM c8cea690… identique, huit cas natifs réussis dont palette/objet distincts, absence de capture automatique, capture réelle et Flash. Voir REPRODUCTIBILITE_ENMA_CREATURE.json. La compilation publique actuelle n’utilise aucune ressource audio privée ; les20sources intégrales encodées sont seulement une préparation de taille. Le prochain chantier reste la préparation des vrais points de boucle et l’intégration DPCM optionnelle, puis français/Léo, graphismes statiques restants et recette principale. Ne pas lancer les quêtes facultatives avant ces priorités.
