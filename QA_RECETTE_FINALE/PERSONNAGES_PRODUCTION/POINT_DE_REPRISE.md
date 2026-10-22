# Reprise après le lot de marche

## Ne pas recommencer ce qui est fait

- Branche art/personnages-production, issue de dev/reconstruction-finalisation au commitc182067ed. Ne pas travailler sur master.
- Commits fonctionnels b493680ac puis740c257b2 : neuf personnages, 54 nouvelles images de pas, quatre directions via le miroir natif pour l’est ; neuf images indexées par personnage. Six sources dessinées et trois variantes partagées.
- Ariane, Nathaniel, Michael, Don Morleone, Mafiamilles1/2/3, employés rouge/bleu : sources, poses fixes archivées, PNG actifs, GIF natifs éditables, tables moteur et tests mGBA publics/privés sont présents.
- Protagonistes : les équipements existent ; ne pas refaire vélo/pêche à cause de la mauvaise lecture de la première galerie. Animations de carte et entrée de combat contrôlées avant les modifications des PNJ, ressources préservées.
- Palettes du jeu, portraits, équipes, scripts, cartes, rencontres, 151espèces, MultiExp et audio inchangés. Les palettes embarquées des neuf PNG sont alignées sur la banque du moteur pour des aperçus fidèles.
- Recompilations GitHub depuis sources nettoyées : SHA identiques. Une vérification mGBA supplémentaire d’Ariane a été exécutée sur le binaire public du clone.

## Suite réelle

1. Consulter docs/atelier-personnages/production/ETAT_PAR_PERSONNAGE.csv et la réponse éventuelle à la question d’archive de références. Ce sont51entrées de travail, pas une affirmation que le casting narratif est définitivement exhaustif. Les1 678objets de cartes et743entrées de dresseurs sont recensés séparément, y compris figurants/objets.
2. Retrouver les références identifiées de Bérénice, Inspecteur Giraud, Alyzon, Steve Jaws, Mark, Zazel et antagonistes du Temple avant de dessiner leurs identités. Le ZIP de transmission contient des documents ; les images officielles retrouvées concernent surtout les personnages déjà présents. Ne pas inventer de tenue ou de personnage sur la seule base d’un nom.
3. Wyatt, Coach Antonic et complément d’Enma : propositions sous docs/atelier-personnages/propositions/non-integrees. Elles ne passent pas le contrôle de la grille ; elles sont hors moteur. Reprendre dans un éditeur à résolution native si les générations ne peuvent pas être suffisamment précises. Ne pas abaisser le seuil pour faire passer un dessin.
4. Enma et Domniscian : anciens designs choisis conservés. Domniscian possède son appareil dans la silhouette ; ne pas le transformer en jambes pour créer un pas. Jobard reste en pause. Usapyon : ne pas réactiver automatiquement l’événement décoratif retiré.
5. Personnages spéciaux et formes de Soranaki : vérifier les variantes réellement spécifiées. Ne pas créer des tenues/formes arbitraires ni réattribuer les arènes pour faciliter l’intégration.
6. Créer les prochaines ressources à taille native, intégrer lorsque leur usage est défini, compiler et tester les ressources réellement changées, puis pousser des jalons fonctionnels sur la branche dédiée. Les tests actuels ne sont pas une traversée de l’aventure complète.

## Outils et ressources

- tools/yokai/convertir_marche_personnages.py : extraction des cellules natives, préservation des poses originales, conversion à la palette réelle et variantes communes.
- tools/yokai/tester_marche_personnages_mgba.py : acteurs des cartes réelles, quatre directions, vérification VRAM et palettes, entrées en combat. YOKAI_WALK_REPORT_DIR permet un autre dossier de preuve ; YOKAI_WALK_ACTORS sélectionne un lot.
- tools/yokai/preparer_atelier_personnages.py et suivre_production_personnages.py : galeries et suivi ; ne pas confondre ces outils avec de la création artistique.
- Les GIF source/marche-*-native.gif s’ouvrent dans Aseprite/LibreSprite à16×32 ; les PNG indexés sont les ressources de compilation. Après une retouche manuelle, conserver le fichier de travail et son export natif ; ne pas écraser cette retouche par une ancienne génération.
- Le générateur historique Red réapplique désormais les sources de marche présentes en dernier. Sa régénération complète des autres personnages n’a pas été exécutée dans cette mission.

Ne publier aucune ROM ni ressource audio protégée. La branche dev et master n’ont pas été modifiées par cette mission.

## Nouveau jalon : décalques Nathan

Laure, Marge et Agent X disposent de PNG natifs neuf poses, déclarations moteur et tests mGBA des deux profils sous DECALQUES_NATHAN et DECALQUES_NATHAN_AUDIO. Corps/mains/pieds copiés des masques de Nathan ; coiffures propres. Source imagegen commune sous graphics/yokai_characters/nathan_trace/source, conversion reproductible avec tools/yokai/decalquer_personnages_nathan.py. Leur palette de groupe est volontairement partagée pour affichage simultané. Scène de comparaison temporaire Route 1 : aucun placement narratif ajouté. Portraits, événements du Temple et approbation artistique restent à faire. Ne pas utiliser les anciens aperçus par injection RAM comme preuve de ces nouveaux fichiers ; le nouveau test utilise leurs ressources réellement compilées. Perpétua/McKraken restent des propositions non intégrées.

## Changement demandé : dessin natif direct

Les versions par conversion imagegen de Laure/Marge/Agent X sont remplacées par des matrices explicitement dessinées de 16x32 cases : chaque acteur possède source/overworld-grille.json. Export direct via exporter_grilles_personnages.py ; ancien convertisseur transformé en point d’entrée de compatibilité, sans lecture d’illustration. Tests des deux profils sous GRILLES_NATIVES_DIRECTES et GRILLES_NATIVES_DIRECTES_AUDIO. Aucun changement de Nathan/Katie/Ariane ni du gameplay. Ne plus reprendre les images générées pour recréer ces trois PNG : éditer leurs cases natives.
