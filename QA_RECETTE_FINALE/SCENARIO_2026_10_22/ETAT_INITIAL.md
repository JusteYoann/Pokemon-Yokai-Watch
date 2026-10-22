# État initial vérifié — 22 octobre 2026

Branche : `dev/reconstruction-finalisation`. Référence avant scénario : `6f143452a026a41c08f1db38f9809959809a31b6`. Aucun changement sur master. Les seuls ajouts locaux sont le pack reçu et ce dossier d'audit.

## Faits constatés dans les fichiers

- 151 espèces personnalisées, rencontres, attaques et évolutions déjà intégrées. Les trois starters sont Komasan005, Padrézo029 et Kappacap087. Komaous évolue avec une Pierre Foudre et Faux Kappa avec une Pierre Eau : aucune restauration des anciens starters ni modification de ces tables n'est nécessaire.
- Multi Exp. permanent dans `src/battle_script_commands.c`. Son code ne constitue pas une validation de la courbe 60–70 sur une aventure entière.
- Nathan/Katie, Matt fixe, caméos conditionnels et certains événements existent. Leur présence ne signifie pas que leurs nouveaux rôles scénaristiques sont intégrés.
- Géométrie de combat étendue : 302 vues à deux pixels maximum des contours des références, 151 captures réelles, 354 scripts d'animation / 1448 cas exécutés, tests de masques et combats spéciaux dans `../COMBATS_ETENDUS/`. Les figures représentent des fixtures natives, pas une traversée de l'aventure.
- 84 espèces éligibles au shiny ; 67 sans statut shiny. Les cinq dessins dédiés retirés restent retirés. Les variantes de couleur sont conservées.
- 26 OST configurées dans la compilation privée actuelle. Les mentions 13/15 OST du pack décrivent un ancien jalon. Aucun fichier audio privé ou ROM n'est inclus dans cette sauvegarde.
- Kyubi : `MtEmber_Summit`; Mademoaiselle : `SeafoamIslands_B4F`; Octorgone : `PowerPlant`; Enma : `CeruleanCave_B1F`. La confirmation explicite du créateur prime sur l'inversion dans le pack.
- Huit arènes et Ligue encore structurées par Rouge Feu : pas d'arène à Lavanville, Céladopole possède toujours sa quatrième arène. Le Temple Céleste et le nouveau climax ne sont pas présents.
- Les nouveaux chapitres Yopple HQ, Zombie Night, passé de Cramois, Zazel et Soranaki ne sont pas implémentés. Les caméos actuels ne les remplacent pas.
- Moteur des types de génération III, sans type Fée et sans séparation physique/spéciale par capacité. L'audit de ces choix n'autorise pas à inventer un nouveau système.

## Preuves renouvelées

`ETAT_INITIAL.json` donne les tailles et SHA-256 des deux ROM existantes. La compilation publique et `TEST_MOTEUR_PUBLIC.json` ont été renouvelés : 151 listes initiales, règles shiny, évolution Noko et opérations natives de sauvegarde/rechargement. Un clone indépendant récupéré directement depuis GitHub sert au contrôle de reproductibilité (résultat séparé).

`DEFAITE_ARGENTA_AVANT.json` reproduit le débordement du tampon de texte de défaite par le chemin natif d'expansion. Cette reproduction isolée ne remplace pas un combat gagné par contrôleur.

## Écarts historiques et limites

Les spécifications reçues sont conservées intégralement dans `docs/mission-codex/2026-10-22/`, avec leurs empreintes et les confirmations de conversation. Les anciens castings Bérénice/Giraud, starters, règles shiny et listes musicales ne doivent pas écraser les choix actuels. Le document DOCX historique ne contient pas de média graphique intégré : les références des nouveaux personnages ne sont donc pas fournies par ce pack.

Aucune preuve de parcours complet Nathan/Katie ni de collection des 151 sur une seule sauvegarde n'a été produite pendant cet audit. Le nouveau scénario n'est pas une v1 prête.
