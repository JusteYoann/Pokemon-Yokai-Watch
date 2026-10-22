# Portraits de combat — archive PORTRAIT COMBAT

27 images de référence ont été examinées : 24 personnages ou formes distincts. Les doublons sont les deux poses de Michael, les deux références de Nathaniel âgé et les vues de groupe complémentaires des Mafiamille. Le trio est couvert par trois portraits distincts. Les fichiers originaux restent hors du dépôt public. Leurs noms et empreintes sont conservés dans REFERENCES_27.json.

## Production réelle

15 nouveaux portraits : Agent X, Alyzon Bie, Bérénice Bélier, Inspecteur Giraud, Lady Perpétua, Laure, Marge, McKraken, Steve Jaws, Whisper en costume, Nathaniel âgé, Enma humain, Zazel, Yopple-bot et Enma ancien.

9 PNG existants conservés byte pour byte : Ariane, Wyatt, Don Morleone, Michael, Nathaniel jeune, Enma royal et les trois Mafiamille. Aucune nouvelle pose de course de Michael n’a été substituée à son portrait précédent.

Les nouvelles images sont dessinées directement sur des canevas indexés 64 × 64, avec Pillow et des cellules entières : aucun outil du plugin graphique, aucune illustration réduite automatiquement, aucune image générée utilisée dans les ressources. Une tentative de l’outil intégré de génération a échoué avant de produire une image (erreur HTTP 400 « Unknown parameter: reasoning ») ; elle n’est pas la source des sprites. Les matrices de pixels et palettes sont conservées dans les dossiers source. L’exportation est reproductible sans service de génération.

Reproduction depuis la racine : `python3 tools/yokai/exporter_portraits_archive.py`. Pillow est nécessaire. Les 14 portraits supplémentaires peuvent être redessinés depuis leurs primitives avec creer_portraits_archive.py ; Agent X garde sa source distincte. L’export des matrices est la voie de reprise des retouches manuelles.

## Intégration et tests

Les portraits sont déclarés dans les tables natives : Agent X ID160 et les 14 autres IDs161 à174. Images compressées 4bpp, palettes 16 entrées, transparence d’indice0, animation statique native. Aucun adversaire, équipe, ville de Champion, dialogue ou carte n’est inventé pour leur donner un emploi. Leurs futurs événements doivent sélectionner ces nouveaux IDs lorsqu’ils seront validés : l’enregistrement dans les tables ne constitue pas une rencontre scénaristique.

24 portraits ont été chargés par CreateTrainerPicSprite dans mGBA, depuis les ressources de ROM compilées. Les tuiles et palettes matérielles ont été comparées exactement aux fichiers convertis. Les captures utilisent un décor de combat de test basé sur Don Morleone : le texte résiduel de cette rencontre n’est pas une attribution du personnage affiché. Les graphismes ne sont pas injectés en VRAM par le test ; seul le chargeur natif de portraits est appelé. Ce n’est pas un test de 24 combats complets.

Les compilations publique et musicale privée passent : 16 Mio et 31 602 147 octets (30,138 Mio), sous 32 Mio. Les deux variantes ont passé les 24 tests de chargement mGBA. Voir QA_RECETTE_FINALE/PERSONNAGES_PRODUCTION/PORTRAITS_ARCHIVE et PORTRAITS_ARCHIVE_AUDIO. Les ROM et ressources audio ne sont pas publiées.

Le travail Agent X précédemment local est aussi sauvegardé : face approuvée intacte, dos/profils et marche, quatre orientations testées dans mGBA, quatre répétitions des cycles, déplacement horizontal et coexistence de sa palette avec Don Morleone/Mafiamille. Ces essais n’ajoutent aucun événement permanent. Les effets de terrain et reflets dans toutes les situations ne sont pas une validation revendiquée.

## Réserves artistiques explicites

Les nouveaux portraits sont des propositions créées et testées techniquement, **pas des dessins approuvés par le créateur**. Les ornements de Perpétua, les tentacules/mécanismes de McKraken, les détails du manteau de Zazel et la tenue cérémonielle d’Enma ancien sont simplifiés pour 64 × 64 et 15 couleurs opaques. Le bas du corps de Giraud est extrapolé car sa référence est un buste. Le pantalon et les chaussures d’Enma humain sont une adaptation du haut de sa tenue montré dans l’image. Ces variantes ne remplacent ni Enma royal ni Nathaniel jeune dans l’histoire.

La provenance des références est l’archive fournie par le créateur ; aucune licence générale de redistribution de ces artworks n’est affirmée. Les sprites sont des adaptations graphiques pour le projet ; les personnages appartiennent à leurs ayants droit.

Les deux grandes planches sont des aperçus des PNG sources ; les images portant mgba dans le dossier QA sont des captures réelles du moteur. Le ZIP contient les 24 PNG natifs, palettes et sources des nouveautés, sans artworks ni musique.
