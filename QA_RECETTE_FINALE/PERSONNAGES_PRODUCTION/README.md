# Production et intégration des personnages — en cours

Branche dédiée : `art/personnages-production`, créée depuis `dev/reconstruction-finalisation` au commit c182067ed.

Jalons fonctionnels : Ariane, Nathaniel, Michael, Don Morleone, Mafiamilles 1/2/3 et employés rouge/bleu possèdent chacun six nouvelles images de pas, soit neuf images de carte avec les trois poses fixes conservées. Total : 54 images de pas attribuées à neuf personnages, issues de six dessins sources distincts et de trois variantes partagées conformément aux choix du créateur. Le moteur utilise leurs neuf images via sa table d’animation standard ; leurs événements existants chargent ces ressources. Les portraits de combat et équipes sont conservés.

Les dessins sont créés sur une grille native 16 × 32 affichée à un zoom entier 16. Le convertisseur lit chaque cellule logique de 16 × 16 pixels et ne réduit pas une illustration. Seules les cellules des jambes/chaussures y26..31 sont prises dans les nouvelles sources ; têtes, torses, identités, palettes et trois images fixes restent inchangés. Les trois paires de pas doivent être distinctes. Les sources et poses initiales sont archivées dans le sous-dossier source/ de chaque personnage.

## Vérifications réellement effectuées

- Protagonistes existants : deux parcours natifs de rendu (Nathan/Katie), quatre résultats dans PROTAGONISTES_AVANT/TEST_PROTAGONISTES_MGBA.json. Marche/course/vélo, actions terrain et Cherche VS, pêche dans quatre directions avec retour à la normale, rendu surf dans une fixture et entrée en combat de Dresseur. Ces résultats montrent que les roues et cannes existent ; le constat précédent de fichiers apparemment sans accessoires était erroné.
- Nouveau lot : compilations publique et privée réussies ; neuf personnages testés dans leurs cartes réelles, sur les profils public ET privé. Quatre orientations, quatre répétitions de pas par direction, correspondance exacte entre les images natives et les octets réellement chargés en VRAM, puis entrée en combat avec portrait existant. Captures et GIF dans MARCHE/ ; aucune victoire ou progression de scénario annoncée par ces tests.
- Le premier test sur une seule action de marche ne demandait qu’un pied au moteur. La fixture a été corrigée pour répéter les actions et contrôler effectivement les deux pieds. Aucun contrôle de contenu n’a été supprimé.
- Wyatt et Coach Antonic : les propositions non conformes sont conservées dans docs/atelier-personnages/propositions/non-integrees, avec les limites et une méthode de retouche native. Aucun de ces essais n’est intégré. Le dernier appel supplémentaire pour Wyatt a été refusé par l’outil de génération ; son dessin actif est conservé.

## Provenance et périmètre

Les références d’identité proviennent des archives Protagoniste.rar et Référence_CAMÉOS_YOKAI_WATCH.rar fournies par le créateur ; elles restent privées. Les personnages officiels sont protégés, ces références ne sont pas présentées comme libres de droits. Aucun nouveau sprite tiers extrait d’un autre fangame n’est importé. Les nouvelles images de pas sont produites depuis les sprites déjà présents et leurs références, avec leurs propres sources conservées. Aucune licence générale de redistribution des personnages n’est déduite de ces fichiers.

Le pack ZIP de transmission local a été retrouvé : il contient des spécifications et des documents, pas une image pour chaque personnage. Les références manquantes doivent être retrouvées avant d’inventer une identité. Le réseau disponible ne permet pas actuellement de vérifier le wiki externe (refus HTTP403 du tunnel), ce qui n’empêche pas la production depuis les références déjà présentes.

Les tableaux dans docs/atelier-personnages/production recensent toutes les entrées d’objets des cartes, les entrées de dresseurs et les créations/changements d’acteurs par script : ils ne se limitent pas aux Champions. Une entrée peut être un objet ou réutiliser un figurant ; aucun rôle ni aucune ville n’en est déduit automatiquement.

## Reste de la mission

Mission globale NON TERMINÉE. Restent les autres personnages, les références à retrouver, leurs poses réellement requises et les chapitres non encore présents. Bérénice et l’Inspecteur Giraud sont bien demandés dans la nouvelle mission ; ne pas réattribuer les arènes pour simplifier les graphismes. Ariane reste Ariane à Carmin. Les rôles contradictoires entre les anciennes listes et le casting consolidé (Steve/Whisper notamment) restent à expliciter sans modifier l’histoire pendant ce lot.

Jobard reste en pause. Les anciens designs choisis d’Enma et Domniscian, les Mafiamilles communes sur la carte et distinctes en combat, les protagonistes validés et le retrait antérieur de l’Usapyon décoratif ne sont pas annulés par une simple ligne d’inventaire. L’apparence d’Usapyon peut être préparée pour un usage explicitement retenu sans réintroduire automatiquement son événement supprimé.

## Résultat visuel et ressources éditables

- [Nouveaux pas natifs agrandis](NOUVEAUX_PAS_NATIFS_X6.png) : montage des fichiers indexés, pas des captures du moteur.
- [Portraits existants dans mGBA](PORTRAITS_EXISTANTS_MGBA.png) : extraits de véritables captures d’entrée en combat. Les portraits sont conservés, pas nouvellement dessinés dans ce lot.
- [Contrôles mGBA privés](MARCHE/TEST_MGBA.json) et [publics](MARCHE_PUBLIC/TEST_MGBA.json), avec PNG/GIF des quatre orientations.
- [Tailles, empreintes et préservation](BUILD_ET_PERIMETRE.json). Les trois premières images compilées de chaque personnage sont identiques à la compilation des poses originales archivées ; cela a été vérifié en4bpp, pas seulement sur les PNG.
- Le PNG overworld.png de chaque personnage est le fichier utilisé par la compilation. Les GIF marche-*-native.gif dans son dossier source/ sont des cycles éditables 16×32 à quatre images, pas des captures mGBA. Le PNG peut être importé dans Aseprite en neuf cases16×32.

Les neuf sprites ont désormais une palette embarquée PNG alignée sur la banque réelle du moteur. Certains anciens PNG conservaient une couleur d’outline plus douce que le noir utilisé en jeu. Cette correction porte sur la représentation PNG : aucun fichier .pal actif, aucune couleur de combat, aucun portrait, aucune statistique et aucun événement n’ont été modifiés.

Les images de marche représentent13 824 octets supplémentaires de données4bpp non compressées. La taille de la ROM privée reste31 589 579octets (30,13Mio), sous32Mio ; le fichier public reste16Mio. Les allocations par image et les banques de palettes restent celles des personnages existants.

### Reproduire

```sh
python3 tools/yokai/convertir_marche_personnages.py ariane nathaniel michael don_morleone mafiamille_1 employe_rouge --variants
python3 tools/yokai/preparer_atelier_personnages.py
python3 tools/yokai/suivre_production_personnages.py
source /workspace/.setup/env.sh
make -j4
make -j4 YOKAI_AUDIO_DIR=/chemin/vers/les/ressources/audio/privees
YOKAI_QA_ROM="$PWD/pokefirered_audio.gba" YOKAI_QA_ELF="$PWD/pokefirered_audio.elf" python3 tools/yokai/tester_marche_personnages_mgba.py
```

Le script de conversion native a été relancé : PNG et métadonnées identiques. L’ancien générateur Red applique désormais les sources de marche natives en dernier pour ne pas écraser ces nouvelles séries ; le générateur historique complet n’a pas été relancé sur les autres personnages de ce lot. Les builds n’ont pas besoin de régénérer les dessins : les PNG et palettes nécessaires sont suivis dans Git.

[Suivi par personnage](../../docs/atelier-personnages/production/ETAT_PAR_PERSONNAGE.csv) : états, ressources présentes/manquantes et références. Le recensement mécanique couvre1 678objets de cartes et743entrées de dresseurs ; il inclut des objets et des figurants génériques, pas1 678identités nouvelles à dessiner.
