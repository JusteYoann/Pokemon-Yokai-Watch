# Production et intégration des personnages — en cours

Branche dédiée : `art/personnages-production`, créée depuis `dev/reconstruction-finalisation` au commit c182067ed.

Premier jalon fonctionnel : Ariane, Nathaniel et Michael possèdent chacun six nouvelles images de pas, soit neuf images de carte avec les trois poses fixes conservées. Le moteur utilise leurs neuf images via sa table d’animation standard ; leurs événements existants chargent ces ressources. Les portraits de combat et équipes sont conservés.

Les dessins sont créés sur une grille native 16 × 32 affichée à un zoom entier 16. Le convertisseur lit chaque cellule logique de 16 × 16 pixels et ne réduit pas une illustration. Seules les cellules des jambes/chaussures y26..31 sont prises dans les nouvelles sources ; têtes, torses, identités, palettes et trois images fixes restent inchangés. Les trois paires de pas doivent être distinctes. Les sources et poses initiales sont archivées dans le sous-dossier source/ de chaque personnage.

## Vérifications réellement effectuées

- Protagonistes existants : deux parcours natifs de rendu (Nathan/Katie), quatre résultats dans PROTAGONISTES_AVANT/TEST_PROTAGONISTES_MGBA.json. Marche/course/vélo, actions terrain et Cherche VS, pêche dans quatre directions avec retour à la normale, rendu surf dans une fixture et entrée en combat de Dresseur. Ces résultats montrent que les roues et cannes existent ; le constat précédent de fichiers apparemment sans accessoires était erroné.
- Nouveau lot : compilations publique et privée réussies ; trois personnages testés dans leurs cartes réelles. Quatre orientations, quatre répétitions de pas par direction, correspondance exacte entre les images natives et les octets réellement chargés en VRAM, puis entrée en combat avec portrait existant. Captures et GIF dans MARCHE/ ; aucune victoire ou progression de scénario annoncée par ces tests.
- Le premier test sur une seule action de marche ne demandait qu’un pied au moteur. La fixture a été corrigée pour répéter les actions et contrôler effectivement les deux pieds. Aucun contrôle de contenu n’a été supprimé.
- Les sources graphiques de Wyatt sont encore en contrôle : un premier dessin a été refusé par la vérification de sa grille. Il n’est pas intégré à ce jalon.

## Provenance et périmètre

Les références d’identité proviennent des archives Protagoniste.rar et Référence_CAMÉOS_YOKAI_WATCH.rar fournies par le créateur ; elles restent privées. Les personnages officiels sont protégés, ces références ne sont pas présentées comme libres de droits. Aucun nouveau sprite tiers extrait d’un autre fangame n’est importé. Les nouvelles images de pas sont produites depuis les sprites déjà présents et leurs références, avec leurs propres sources conservées. Aucune licence générale de redistribution des personnages n’est déduite de ces fichiers.

Le pack ZIP de transmission local a été retrouvé : il contient des spécifications et des documents, pas une image pour chaque personnage. Les références manquantes doivent être retrouvées avant d’inventer une identité. Le réseau disponible ne permet pas actuellement de vérifier le wiki externe (refus HTTP403 du tunnel), ce qui n’empêche pas la production depuis les références déjà présentes.

Les tableaux dans docs/atelier-personnages/production recensent toutes les entrées d’objets des cartes, les entrées de dresseurs et les créations/changements d’acteurs par script : ils ne se limitent pas aux Champions. Une entrée peut être un objet ou réutiliser un figurant ; aucun rôle ni aucune ville n’en est déduit automatiquement.

## Reste de la mission

Mission globale NON TERMINÉE. Restent les autres personnages, les références à retrouver, leurs poses réellement requises et les chapitres non encore présents. Bérénice et l’Inspecteur Giraud sont bien demandés dans la nouvelle mission ; ne pas réattribuer les arènes pour simplifier les graphismes. Ariane reste Ariane à Carmin. Les rôles contradictoires entre les anciennes listes et le casting consolidé (Steve/Whisper notamment) restent à expliciter sans modifier l’histoire pendant ce lot.

Jobard reste en pause. Les anciens designs choisis d’Enma et Domniscian, les Mafiamilles communes sur la carte et distinctes en combat, les protagonistes validés et le retrait antérieur de l’Usapyon décoratif ne sont pas annulés par une simple ligne d’inventaire. L’apparence d’Usapyon peut être préparée pour un usage explicitement retenu sans réintroduire automatiquement son événement supprimé.
