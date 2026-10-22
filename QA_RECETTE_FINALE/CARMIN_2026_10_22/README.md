# Carmin — Ariane et le troisième trophée

Branche: `dev/reconstruction-finalisation`. Référence avant ce lot: `260edd121`. L'arène devient celle d'Ariane selon le pack actuel. Aucun import des nouveaux dessins de l'autre branche, aucun changement de géographie de Carmin ni de sprite de combat/carte. **Ce lot finalise l'arène; il n'intègre pas encore les Portes Mystères, le Dr Jobard ou la nouvelle remise de Coupe.**

## Intégration

- Portrait et sprite d'Ariane déjà présents réutilisés; Usapyon placé à côté sur une case praticable. Leurs deux anciens acteurs de Route25 sont masqués sans supprimer leurs identifiants ni les scripts historiques.
- Double verrou, interrupteurs aléatoires et grille de l'arène d'origine conservés. Le deuxième trophée est également contrôlé avant le combat, même si l'on arrive directement devant Ariane.
- Troisième trophée, droits de Vol, CT34, apparition de l'assistant de Chen et indicateurs historiques conservés. Une ancienne victoire de Major Bob compte toujours comme troisième trophée.
- Pierre Lune historique unique après la victoire de l'arène. Saturation du Sac/pile: cadeau et CT différés, récupérables sans refaire le combat. Les cadeaux gagnés sur une ancienne partie ne sont pas dupliqués.
- Revanches facultatives après la fin, avec Oui/Non et l'équipe historique de cinq membres. Les anciens flags de victoire et de cadeau restent utilisés, y compris la victoire Ariane générale après une revanche.
- Anciennes sauvegardes dans l'arène: rechargement unique des acteurs et placement sûr à l'entrée; Route25: rechargement des acteurs masqués, position conservée. Les reprises suivantes gardent la position exacte. Pas de nouveau format de sauvegarde.
- Texte de l'arène, panneau, profil et journal adaptés à Ariane/Acier; portrait et nom du Fame Checker corrigés. Les deux mentions restantes de Misty à Route20 et dans les Condominiums de Céladopole sont également corrigées en français, sans changer leurs scripts.
- La sélection de musique de combat reconnaît maintenant Ariane aux emplacements416,1et2. Le thème personnel existant `MUS_YOKAI_ARIANE` est observé dans le mixeur natif; son échantillon privé est bien disponible. Les26OST et bruitages sont réutilisés, sans nouveau fichier audio.

## Profil d'équipe provisoire

Navétéran18, Robonyan19, Mognyan21, Usapyon23. Trois Acier et l'exception Psy; Usapyon reste la signature. Espèces issues de la proposition historique d'Ariane, déplacée au troisième trophée conformément au pack actuel. Niveaux/IV0/sets sans objets sont des choix d'implémentation **provisoires**, pas une nouvelle approbation définitive du créateur. Toutes les attaques sont apprises dans les tables validées aux niveaux concernés.

Les anciens tableaux Major Bob et Ariane/caméos restent verbatim dans les sources. Seule la fiche active416 est remplacée. Un applicateur idempotent et le générateur global conservent le nouveau profil lors d'une reconstruction volontaire des équipes historiques. Les15autres équipes verrouillées encore actives et les équipes de Matt sont préservées.

## Tests réellement effectués

- Compilations publique et privée réussies. `BUILD.json`: privé31589579octets, environ30,13Mio, limite32Mio respectée. ROM et enregistrements privés non publiés.
- `TEST_CHAPITRE_MGBA.json`: cinq contrôles natifs complets. Pour Nathan et Katie: entrée réelle par la porte de Carmin après téléportation de fixture, refus sans deuxième trophée, vraie erreur d'interrupteur puis résolution, passage, combat gagné avec statistiques ordinaires, troisième trophée, CT34/Pierre Lune différées selon la pile saturée, absence de doublon, Flash/Continuer, sortie et retour à la musique de la carte.
- Défaite réelle avec un partenaire niveau1: aucun trophée, CT ou cadeau accordé. La nouvelle tentative reste possible.
- Anciennes parties simulées après Major Bob et sur Route25: Continuer recharge les objets appropriés, garde le trophée, permet de récupérer les cadeaux sans refaire le combat et conserve ensuite la position.
- Revanche postgame: refus accepté; vrai combat contre les cinq anciens membres, thème personnel, flags persistants et aucun deuxième cadeau.
- `TEST_EQUIPES_MGBA.json`:640équipes/1652créatures construites par le moteur; espèces, niveaux, capacités, talents, objets et chronologie de Matt contrôlés. Il ne s'agit pas de640combats joués.
- `TEXTES_MGBA.json`:144lignes, police native, prénom de sept W, maximum208pixels respecté.
- `TEST_PROFIL_MGBA.json`: identité416/portrait148 et nom dans la liste native du Fame Checker; livre explicitement débloqué pour ce banc.
- `TEST_MENU_COMBAT_MGBA.json`: capture native après stabilisation du menu de combat, véritable interaction avec Ariane, Navétéran premier adversaire, thème377 et échantillon privé disponibles. Ce banc prépare explicitement le deuxième trophée et le verrou résolu; il ne remplace pas le test complet de l'énigme.
- `NON_REGRESSION.json`:6894fichiers de ressources/données préexistants contrôlés inchangés, anciens tableaux préservés verbatim, seul bloc de Champion416 remplacé et générateur idempotent. Statistiques/types/évolutions/rencontres, Multi Exp., sprites et politique shiny restent intacts.
- Captures de carte avec Ariane/Usapyon, portrait de profil et menu de combat natif ouvertes et examinées. `*-combat.png` peut montrer la transition d'envoi; `combat-menu-natif.png` montre le rendu stabilisé.

## Fixtures et limites

Les deux victoires utilisent Jibanyan24/Komasan24/Kappacap23, IV15, statistiques ordinaires et attaques déjà apprises réordonnées. Les autres Dresseurs de l'arène sont marqués battus dans le banc pour isoler l'énigme et Ariane. La revanche utilise Hovernyan100 avec statistiques explicitement augmentées à999: contrôle d'événement, pas équilibrage. Les anciennes sauvegardes sont des états construits, pas des fichiers historiques fournis par le créateur.

Le pilote initial répétait une capacité légale mais inadaptée après Entrave; il a perdu. Sa sélection actuelle choisit une attaque offensive utilisable en tenant compte des types et évite de répéter Bluff. Il ne modifie ni PP, ni curseur en RAM, ni équipe adverse, ni résultat: uniquement des touches de manette. Les diagnostics de cet essai sont conservés dans `diagnostics/` (préfixe historique du helper partagé). Le premier placement d'Usapyon sur une tuile bloquée a été corrigé avant validation. Le pilote de sortie a aussi été ajusté pour traverser la flèche de porte jusqu'au changement de carte.

Pas de preuve de parcours continu depuis Bourg Palette ni d'équilibrage avec tous les starters. L'arène est intégrée; l'ensemble du nouveau scénario et les événements du S.S.Anne restent à développer/tester. `master` n'est pas modifié.

## Rejouer

Après compilation et activation de l'environnement:

```sh
export YOKAI_QA_ROM="$PWD/pokefirered_audio.gba"
export YOKAI_QA_ELF="$PWD/pokefirered_audio.elf"
python3 tools/yokai/tester_carmin_mgba.py
python3 tools/yokai/tester_textes_carmin_mgba.py
python3 tools/yokai/tester_profil_carmin_mgba.py
python3 tools/yokai/capturer_carmin_menu_mgba.py
YOKAI_TEAMS_QA_REPORT="$PWD/QA_RECETTE_FINALE/CARMIN_2026_10_22/TEST_EQUIPES_MGBA.json" python3 tools/yokai/tester_equipes_mgba.py
```
