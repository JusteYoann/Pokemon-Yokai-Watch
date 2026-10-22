# Carmin-sur-Mer — Bérénice et le troisième trophée

## Contenu jouable intégré

La porte existante de l'arène de Carmin-sur-Mer mène au laboratoire de Bérénice. La ville conserve sa géographie, son accès par Coupe et ses autres événements. Bérénice utilise ses sprites existants, sa blouse et ses lunettes, avec une équipe dominante Psy. Le panneau extérieur est réécrit et ne débloque plus une ancienne fiche du Major Bob.

Trois terminaux liés aux Portes Mystères donnent accès à des cartes nouvelles de 15×15, dans un ordre libre :

- **Songes** : parcours végétal avec trois bandes d'obstacles et un signal au bout du chemin.
- **Mémoire** : grotte, indice lisible et choix entre trois stèles ; une mauvaise réponse permet de réessayer immédiatement.
- **Veille** : deux chambres physiquement séparées, reliées par une paire de téléporteurs natifs réciproques. Chacune possède son retour au laboratoire.

Ces dimensions, leurs noms et leurs petites épreuves sont des choix de level design dans la liberté accordée par le dossier. Chaque dimension possède un retour fixe disponible avant sa réussite ; la calibration réussie renvoie au laboratoire et conserve un indicateur indépendant. Aucun retour ne dépend d'une destination dynamique perdue après sauvegarde. Les nouvelles cartes et dispositions sont originales, avec des tilesets natifs différents. Leurs identifiants sont ajoutés après les cartes existantes, sans renumérotation.

Le deuxième trophée autorise les expériences. Le passage vers Bérénice et l'interaction directe avec elle exigent les trois calibrations. Un assistant propose un soin facultatif avant la suite. La victoire donne le troisième trophée et la CT34, en préservant les fonctions natives de progression, notamment Vol et l'apparition de l'assistant de Chen liée à Flash. Un Sac plein laisse la CT en attente ; une interaction ultérieure la remet sans nouveau combat ni duplication.

## Équipe et textes

Baku niveau22, Ed Mémoire niveau22 et Insomnelle niveau24 ; IV0, Synchro, aucun objet tenu ni soin de Dresseur. Les espèces correspondent à la proposition du scénario. Le nom « Insomnel » du dossier désigne ici `SPECIES_VICTREEBEL`, déjà affiché « Insomnelle » dans le Pokédex actif ; aucun identifiant ni nom global n'a été modifié. L'ancienne équipe verrouillée du Major Bob reste dans `sYokaiParty_LEADER_LT_SURGE` et dans sa spécification historique.

Niveaux et attaques restent des choix provisoires de gameplay. Les textes français suivent l'enthousiasme de chercheuse décrit dans le dossier et restent disponibles pour relecture créative. Le profil actif, les lieux et les indicateurs figurent dans `data/yokai/scenario_carmin.json`. Après une régénération intentionnelle des anciennes équipes globales, réappliquer les profils Argenta, Azuria puis Carmin avant compilation.

## Graphismes : correction et élément restant

L'habillage définitif des **portes à œil et serrure reste à produire**. Les motifs roses natifs des terminaux sont provisoires. Les références, dimensions, fichiers attendus et points d'intégration exacts sont documentés dans `ASSETS_PORTES_A_FINALISER.md`. Cet asset n'est pas déclaré terminé.

La recette a révélé deux défauts dans l'enregistrement antérieur des nouveaux sprites : l'export des feuilles de carte utilisait des rangées de tuiles au lieu de frames complètes ; les nouveaux portraits de combat n'avaient pas leurs pointeurs d'animation, ce qui bloquait l'entrée en combat de Bérénice. Les règles de découpage des 18 ressources et les 15 entrées de portraits sont corrigées. La validation précédente de simple présence/palette ne suffisait pas : les nouveaux contrôles comparent désormais les pixels sources, les frames liées et la VRAM réellement utilisée par le moteur. Argenta a été rejoué ; les captures d'Enma sont actualisées.

## Recette et limites

- `TEST_CHAPITRE_MGBA.json` : Nathan et Katie, vraie porte de la ville, refus avant deuxième trophée, accès aux trois dimensions par interaction, mauvaise stèle, retour anticipé, sauvegarde/reprise dans chaque dimension, téléporteurs dans les deux sens, combat natif, troisième trophée, CT, Sac plein, non-duplication et sortie.
- `TEST_MIGRATION_MGBA.json` : défaite réelle sans trophée, conservation des calibrations, refus avec une/deux calibrations, tous les portails avant le deuxième trophée, retours sans réussite depuis Mémoire et les deux chambres de Veille, soin facultatif Oui/Non, ancienne sauvegarde construite explicitement puis sauvegardée/reprise nativement.
- `TEST_SPRITES_LIES_MGBA.json` et `SPRITES_SCENARIO_NATIFS.png` : 18 objets instanciés dans mGBA ; toutes leurs frames comparées à un encodage indépendant des PNG ; rendu VRAM et palette contrôlés. Vérification des bornes/pointeurs des 15 portraits, avec combat réel de Bérénice dans la recette du chapitre. Les combats des 14 autres futurs boss ne sont pas joués par ce test.
- `TEST_EQUIPES_ACTIVES_MGBA.json` : construction native des 640 équipes actives, espèces, niveaux, attaques, talents et objets ; aucun parcours de 640 combats revendiqué.
- `CONTROLE_SOURCES.json` : accès aux objectifs et sorties, fermeture du passage vers Bérénice, nécessité de la paire de téléporteurs, restrictions de sortie et stabilité des identifiants des anciennes cartes/layouts.
- `LARGEURS_DIALOGUES.json` : 99 lignes contrôlées avec la police native et un nom du joueur de sept W.
- `REGRESSION_CHAPITRE_ARGENTA_MGBA.json` et `REGRESSION_CONTINUE_ARGENTA_MGBA.json` : chapitre et migration d'Argenta rejoués après les corrections communes.

La fixture de victoire est Kappacap26, Whisper25 et Cigallard25, IV15 et statistiques ordinaires. Cigallard provient de l'évolution au niveau18 du Cigalopin capturable en Forêt de Jade. Le pilote utilise les attaques déjà apprises, réordonnées depuis l'équivalent du résumé : Vibraqua, Ombre Nocturne et Rayon Signal sont privilégiés selon le partenaire. Il sélectionne un partenaire vivant après une mise K.O. par les boutons du menu. Aucun résultat de combat ni statistique de victoire n'est forcé. Une première fixture avec Nihilistik, faible au Psy, a notamment perdu : ses diagnostics sont conservés ; ils ne constituent pas une validation d'équilibrage global.

Les sauvegardes de recette appellent `SaveMapView`, comme le menu Sauvegarder natif, puis l'écriture Flash, la lecture et le callback Continuer. Un premier pilote omettait la vue courante, ce qui réinjectait des tuiles d'une carte précédente et faussait le test des téléporteurs. Les tests actuels reproduisent cette préparation native. Les essais restent des fixtures explicites, sans partie continue depuis Bourg Palette ni fichier archivé d'un joueur.

Reproduire depuis la racine, après `source /workspace/.setup/env.sh` et `make -j4` :

```sh
python3 tools/yokai/verifier_carmin_sources.py
python3 tools/yokai/tester_textes_carmin_mgba.py
python3 tools/yokai/tester_carmin_scenario_mgba.py
python3 tools/yokai/tester_carmin_migration_mgba.py
python3 tools/yokai/tester_sprites_scenario_lies_mgba.py
python3 tools/yokai/tester_equipes_mgba.py
python3 tools/yokai/tester_argenta_scenario_mgba.py
python3 tools/yokai/tester_argenta_continue_mgba.py
```

Les trois derniers outils écrivent dans leurs dossiers historiques ; leurs résultats actuels sont copiés ici, et les captures d'Enma corrigées restent aussi dans Argenta. Les anciens diagnostics ont un préfixe Argenta hérité du pilote commun ; ils concernent bien les essais de Carmin.

L'équilibrage de tous les starters, le parcours continu, les sauvegardes historiques réelles et l'habillage final des portes restent à valider ou terminer. Le vérificateur général historique des sprites conserve son incompatibilité connue avec les nouvelles présentations ; aucune validation globale du jeu n'est revendiquée. Le prochain ensemble scénaristique est Ariane Célestin à Safrania. ROM locale de recette uniquement ; aucun binaire ROM publié.
