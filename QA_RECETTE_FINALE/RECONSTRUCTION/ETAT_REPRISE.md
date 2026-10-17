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
| Caméos | Ariane/Usapion et Seigneur Enma restaurés ; les cinq autres groupes demandés restent à reconstruire. |
| Dix quêtes | Quête 8 partielle par l'événement Enma partagé ; neuf autres non reconstruites ; aucune annoncée complète. |
| 20 OST DPCM | Direction et références préservées ; intégration active : zéro. Inspection du pilote dans AUDIO_DPCM_PREPARATION.md. |
| Nathan/Katie et autres overworld | Séries originales complètes intégrées : 73 emplacements par protagoniste, tests natifs terrain/combat réussis. Introduction, Surf et écrans secondaires restent à éprouver. Enma/Kyubi et Matt/Ariane présents ; autres overworld à produire. |
| Français complet, animations, aventure | Incomplets ; les tests natifs ciblés ne remplacent pas une traversée réelle complète. |

Les essais Enma utilisent les contrôles du jeu pour refus, défaite, victoire, revanches et capture à la Master Ball. Téléportations, niveaux artificiels et option SET de la fixture sont documentés dans TEST_ENMA_MGBA.json. Les 56 lignes ajoutées Ariane/Enma tiennent dans 208 pixels avec la police native.

## Sauvegarde et reproductibilité

Le clone indépendant récupéré directement depuis GitHub reproduit exactement le jalon Matt/Ariane (`REPRODUCTIBILITE_ARIANE.json`). Les résultats de jalons ultérieurs doivent être lus dans leur propre rapport de clone ; ne pas extrapoler une ancienne empreinte aux changements suivants.

Aucune ROM commerciale, ROM modifiée ou musique protégée n'est publiée. Les graphismes sources, outils et scripts requis pour le build public actuel sont suivis. Une future compilation avec les OST privées nécessitera leur fourniture séparée et ne sera pas musicalement identique sans elles.

La CI est publiée, mais son résultat distant n'a pas pu être consulté (proxy API GitHub : 403). Les preuves locales n'en dépendent pas. Les anciens rapports qui citent des commits/environnements perdus restent des archives ; leur présence ne signifie pas que ces fonctionnalités ont été récupérées.

## Poursuite autorisée

Continuer les caméos manquants, Nathan/Katie et les overworld, les shiny finaux, les quêtes et le pipeline musical DPCM, puis la traduction, l'équilibrage et la recette complète. Préserver les choix validés et publier par jalons testés ; aucun nouveau feu vert n'est requis pour les travaux déjà autorisés dans MANDAT_RECONSTRUCTION.md.

**Verdict global : NON PRÊT.** Aucun parcours intégral ni contrôle exhaustif des 354 animations n'a encore été réalisé.

Jalon protagonistes actif : TEST_PROTAGONISTES_MGBA.json, sources graphics/yokai_characters/{nathan,katie,matt}, découpe et conversions reproductibles dans tools/yokai. Les premiers aperçus GIF peuvent être noirs dans l’interface ; chaque animation possède aussi une planche PNG opaque de vraies captures. Reprise : terminer les tests introduction/Surf/écrans secondaires, puis caméos manquants, sans régénérer les dessins déjà intégrés.
