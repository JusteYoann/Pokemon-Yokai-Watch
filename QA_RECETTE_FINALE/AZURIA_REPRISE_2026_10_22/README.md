# Azuria — intégration reprise et vérifiée sur notre branche

Référence avant ce lot : `dd46996fc13cb8dfdaa8ef3f7737e74625d7a9a4`, branche `dev/reconstruction-finalisation`. Reprise ciblée des commits `b9c2aae07`/`65b62bd88` de l'autre branche, sans fusion globale ni importation de ses dessins, de son Argenta ou de ses autres choix de casting. `PROVENANCE.json` détaille les fichiers repris.

## Contenu jouable

- Nathan joueur rencontre Katie Championne; Katie joueuse rencontre Nathan Champion. Un seul acteur apparaît, avec nos ressources actuelles de carte et de combat. Aucun dessin de personnage ou Yo-kai n'est remplacé.
- Arène Feu avec trois foyers symboliques: Feulion à gauche, Whisper à droite, Jibanyan au centre. Le guide explique l'ordre. Une erreur permet immédiatement de recommencer. Progression, lumière des pupitres, sortie/rentrée et sauvegarde restent cohérentes.
- Premier trophée exigé; l'épreuve débloque l'accès au Champion. Une interaction directe vérifie aussi les conditions. L'ancien deuxième trophée permet aux anciennes parties d'éviter de refaire cette épreuve.
- Victoire: deuxième trophée, CT03 unique et droits natifs de Coupe conservés. Cadeau récupérable après saturation de la pile CT, sans refaire le combat.
- Les anciens caméos Nathan/Katie de Céladopole sont déplacés ici: leurs équipes postgame historiques à six restent intactes, avec Oui/Non et Pierre Plante unique. Un cadeau gagné mais non récupéré dans une ancienne partie reste disponible. Les nouvelles parties obtiennent cette Pierre après la revanche postgame; les anciens combats optionnels d'avant le postgame à Céladopole ne sont plus actifs.
- Reprise d'une ancienne sauvegarde dans l'arène: recharge unique des tuiles/acteurs et placement à l'entrée sûre. À Céladopole, acteurs désormais masqués et position conservée. Les reprises suivantes conservent la position exacte. Aucun changement du format de sauvegarde.
- Correction supplémentaire par rapport à l'autre branche: le Fame Checker affiche le nom et le portrait du protagoniste opposé, y compris pour un ancien profil d'Ondine. La rencontre et la victoire débloquent réellement le profil et sa fiche de partenaires, conservés au rechargement. Les mentions d'Ondine/Misty et sa biographie Eau sont remplacées dans cette fiche et le journal concerné.

## Équipe active et limites créatives

**Profil d'implémentation provisoire, pas nouvelle approbation définitive du créateur:** Feulion16, Whisper16, Jibanyan18, IV0, sans objet ni soin de dresseur. Deux partenaires Feu et l'exception Spectre respectent la direction du personnage. Données exactes dans `data/yokai/scenario_azuria.json`.

Les tableaux historiques d'Ondine et des caméos restent inchangés dans les sources. Seuls l'ancien emplacement d'Ondine415 et un emplacement factice inutilisé21 sont liés au nouveau profil. Les16autres équipes de boss verrouillées, les équipes de Matt et les revanches historiques sont conservées. Le générateur d'équipes réapplique désormais cet override après génération, ainsi que notre identité de Wyatt: aucun retour silencieux à l'ancien casting.

## Vérifications réellement exécutées

- Reconstructions du clone GitHub indépendant strictement identiques dans les deux profils: `REPRODUCTIBILITE.json`.
- Compilations publique et privée réussies. `BUILD.json` donne tailles et SHA: privé31589579octets, soit30,13Mio; limite32Mio respectée,26OST conservées. Aucune ROM ni ressource audio privée publiée.
- `CONTROLE_SOURCES.json`: accès aux trois pupitres et aux trois sorties, blocage central, retour possible, capacité d'objets et conservation des tableaux historiques.
- `TEST_CHAPITRE_MGBA.json`: véritables déplacements depuis la porte de la ville, énigme, essais de refus, état visuel après Flash/Continuer et sortie/rentrée, combat gagné, trophée, CT et profil persistant, pour les deux personnages.
- `TEST_MIGRATION_MGBA.json`: six contrôles couvrant défaite réelle et récupération, états partiels/erronés de l'énigme, ancienne sauvegarde simulée après Ondine, cadeau historique en attente, disparition des acteurs déplacés de Céladopole et les deux revanches postgame avec refus et saturation de Pierre Plante.
- `TEST_PROFIL_MGBA.json`: liste et portrait natifs Katie/Nathan selon joueur, profil Wyatt inchangé. Le banc débloque explicitement le livre pour tester l'interface; l'obtention du livre durant l'aventure n'est pas prétendue jouée.
- `LARGEURS_DIALOGUES.json`:135lignes mesurées avec la police native et un prénom de sept W, toutes dans208pixels.
- `TEST_EQUIPES_ACTIVES_MGBA.json`:640équipes et1652créatures construites et contrôlées par les fonctions natives; espèces, niveaux, attaques, talents, objets et chronologie de Matt. Ce n'est pas640combats joués.
- `NON_REGRESSION.json`:6891fichiers de ressources/données préexistants contrôlés inchangés, tous les anciens tableaux de groupes conservés verbatim, seules les deux fiches de nouveaux Champions remplacées; applicateur de profil idempotent.
- Captures d'entrée, foyers, combats Nathan/Katie et deux profils du livre ouvertes et examinées visuellement. Elles proviennent de mGBA.

## Ce que ces tests ne prouvent pas

Pas de traversée continue depuis Bourg Palette ni d'équilibrage avec tous les starters. Les victoires du chapitre utilisent une équipe de fixture aux statistiques ordinaires (Kappacap20, Whisper18, Nihilistik18, IV15; capacités apprises réordonnées). La défaite utilise un partenaire niveau1. Les revanches utilisent Hovernyan100 avec statistiques explicitement augmentées à999: elles valident les événements, pas leur difficulté. Les anciennes parties sont des états construits de façon explicite, pas des fichiers historiques fournis par un joueur.

Le premier contrôle du profil lisait un pas de structure de2octets; l'ABI réelle impose4octets par fiche. Le pilote a été corrigé après lecture de la structure et du code compilé; le jeu n'a pas été modifié pour faire passer ce contrôle.

## Rejouer

Après `source /workspace/.setup/env.sh`, compiler puis sélectionner explicitement ROM/ELF du même profil:

```sh
export YOKAI_QA_ROM="$PWD/pokefirered_audio.gba"
export YOKAI_QA_ELF="$PWD/pokefirered_audio.elf"
python3 tools/yokai/verifier_azuria_sources.py
python3 tools/yokai/tester_azuria_scenario_mgba.py
python3 tools/yokai/tester_azuria_migration_mgba.py
python3 tools/yokai/tester_profil_azuria_mgba.py
python3 tools/yokai/tester_textes_azuria_mgba.py
YOKAI_TEAMS_QA_REPORT="$PWD/QA_RECETTE_FINALE/AZURIA_REPRISE_2026_10_22/TEST_EQUIPES_ACTIVES_MGBA.json" python3 tools/yokai/tester_equipes_mgba.py
```

Suite: Carmin/Ariane et les autres chapitres; le nouveau scénario complet et sa recette finale restent à terminer. `master` n'est pas modifié.

## Textes voisins restant à traiter

L'audit global repère encore deux mentions de MISTY hors du chapitre: `data/maps/CeladonCity_Condominiums_3F/text.inc` et `data/maps/Route20/text.inc`. Elles restent à adapter pendant la prochaine passe de cohérence française. La correction du présent lot porte sur l'arène, son panneau, sa fiche et le journal; elle n'est pas présentée comme une traduction complète du monde.
