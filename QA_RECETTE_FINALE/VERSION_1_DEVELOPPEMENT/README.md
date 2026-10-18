# Version de développement — mission finale v1.0

La consigne exhaustive est conservée dans `RECUPERATION_PROJET/sources_validees/MISSION_FINALE_V1.md`. Elle remplace les priorités précédentes : 15 OST, aucune nouvelle quête. Les anciens 20 choix et leurs tests restent dans l’historique Git ; ils ne définissent plus la sélection.

## Ce jalon

- Sources exactes des 15 titres retrouvées dans les archives privées : `../INTEGRATION_MUSIQUES/SOURCES_V1.json`.
- 13 pistes activées dans le profil privé ; deux sont encore en attente d’un raccord musical fiable : Enma Track (dialogues) et Final Battle – Are You Ready? (Matt Champion). Leurs identifiants sont préparés, avec repli natif explicite. Ce jalon ne prétend donc pas intégrer les 15 OST.
- Mount Wildwood, Harrisville et Mini Boss sont retirés du profil ; Bois Baies, Île 2, employés et Mafiamille retrouvent leurs thèmes natifs. Maisons et quêtes reportées sans enregistrements privés. Les anciens identifiants restent réservés pour éviter une renumérotation.
- San Fantastico : Carmin sur Mer ; Uptown : Céladopole ; Mystic Grove : trois étages de la Caverne Azurée ; Hoppers Gorge : trois étages du Mont Sélénite. Les sept thèmes demandés sont conservés. Ghoulfather utilise son propre enregistrement, pas Sangokushi.
- Take Care, Grandpa 1 commence après la victoire contre Matt, dans la scène originale avec Chen, puis laisse place au Panthéon et aux crédits natifs.
- Trois nouveaux sprites de carte 32×32 : Misterre (Routes 12 et 16), Octorgone (Centrale), Mademoaiselle (Îles Écume). Kyubi et Enma capturable conservés, Seigneur Enma distinct. Aucun sprite normal/shiny de combat remplacé.
- Léo devient Jibanyan avec neuf images directionnelles et sa propre palette. Son dialogue français explique le PC et les Boîtes Yo-kai. Les scripts de séparation/restitution humaine sont conservés.
-1850chaînes affichées harmonisées, puis menus principaux/aide/sauvegarde et34messages de combat traduits. Médallium50px : menu agrandi de7à8tuiles. Six classements et compteurs bornés à151 après déblocage national, sans supprimer les flags existants.30contrôles natifs de libellés et interfaces. Deux en-têtes générés corrigés via leurs JSON sources après comparaison de clone propre.
- Dialogues français de Matt/Chen dans la salle du Champion et le Panthéon. Les autres textes du jeu ne sont pas tous traduits : aucune revendication de français intégral.

## Preuves et limites

`STATIQUES_LEO_MGBA.json` et `preuves/` : quatre interactions/captures réelles, espèces vérifiées dans le groupe et le Médallium ; palettes et nouveaux objets vérifiés ; téléporteur original de Léo pour les deux sexes. Fixtures explicites de téléportation, progression et objets : cela ne prouve pas les trajets de l’aventure.

`../INTEGRATION_MUSIQUES/CONCLUSION_LIGUE_V1.json` : entrée et combat réel contre Matt, cinq boucles enregistrées de la conclusion, Panthéon, crédits complets et retour par le menu Continuer. Équipe de test forte et arrivée directe à la Ligue, sans modification de son équipe. Cela ne constitue pas une partie du début à la fin.

Les anciens échecs d’instrumentation sont conservés dans `../INTEGRATION_MUSIQUES/diagnostics-v1/` : arrivée de fixture dans l’eau à Carmin (Surf joue correctement), tentative de RPC durant le reset des crédits, et vérification trop précoce pendant le récapitulatif de sauvegarde. Hoppers : un premier raccord dans un silence inférieur au pas PCM8 n’atteignait pas la corrélation audio requise ; le raccord est déplacé au sein de la même période musicale complète vers une section audible, sans abaisser le seuil.

Restent obligatoires : deux raccords/activations musicaux, direction artistique des 84 shiny (dont les cornes actives de Robonyan 28), français/vocabulaire complet, équilibrage et vraie traversée principale/postgame, recette des animations et des 151 obtentions. **NON PRÊT pour une déclaration v1.0 finale.** La version de développement compile ; les contrôles ciblés ne suffisent pas à lever ces réserves.

## Reconstruction

La compilation publique reste `source /workspace/.setup/env.sh` puis `make -j4` avec les musiques natives de repli. Installation portable : `RECUPERATION_PROJET/scripts/configurer_outils_debian.sh`, documentation du dépôt. Aucun besoin d’enregistrement externe pour cette variante.

Pour la variante privée, installer les dépendances de `tools/yokai/requirements-audio.txt`, extraire ses propres archives avec `extraire_audio_prive.py`, puis :

```bash
python tools/yokai/preparer_ost_dpcm.py --extracted-manifest /chemin/prive/manifest-private.json --private-output /chemin/prive/sources --jobs 4
python tools/yokai/generer_audio_prive.py --full-source-dir /chemin/prive/sources --output /chemin/prive/integration --jobs 4
make -j4 YOKAI_AUDIO_DIR=/chemin/prive/integration
```

Les répertoires privés doivent être extérieurs au checkout. Le générateur vérifie les WAV épinglés avant toute liaison ; son masque indique les 13 pistes réellement compilées. Les enregistrements, WAV, DPCM et ROM restent privés ; aucun de ces fichiers n’est envoyé sur GitHub. Sans les sources externes, le résultat musical est volontairement différent. Ne pas appeler cette ROM v1.0 finale tant que les critères manquants ne sont pas remplis.
