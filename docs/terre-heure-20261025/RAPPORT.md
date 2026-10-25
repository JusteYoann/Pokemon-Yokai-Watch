# Terr’heure et quête des trois Oni — 25 octobre 2026

> Une correction ultérieure remplace le voile fixe par un décor gris avec des nuages jaunes mobiles, et déclenche le combat à zéro : [nouvelle version et tests](../terre-heure-corrections-20261025/RAPPORT.md).

Branche dédiée : `feature/terre-heure-quete-oni-20261025`. Aucune fusion sur `master`.

[**Télécharger la ROM de test avec les OST**](Pokemon_Yokai_Watch_Beta_0.1_Terre_Heure.gba) · [Informations et SHA-256](LIVRAISON.json)

**33 489 991 octets**, soit environ 31,94 Mio. Les musiques existantes sont conservées, sans nouvelle conversion.

## Décisions appliquées

- Les récompenses utilisent exactement le sprite de Poké Ball déjà présent pour les objets au sol : `OBJ_EVENT_GFX_ITEM_BALL`. Aucun sprite de coffre ajouté.
- Le voile doré discret, choisi dans le chat, affecte uniquement le décor. Nathan, les Oni, les patrouilles et la porte gardent leurs couleurs.
- Gorgouille nº65, niveau 80, remplace la rencontre de Maître Nyada au Mont Braise, en **(9, 6)**. Alizon Bie l’accompagne en **(7, 6)**.
- Maître Nyada conserve son rôle de dernier adversaire de la Ligue. Sa rencontre existante au Canyon Sesor, hors du Mont Braise, est également préservée : le nº148 reste obtenable.

## Captures mGBA

| Situation | Preuve |
| --- | --- |
| Transformation et disparition progressive des PNJ | [GIF de la transition](prive/transparence-pnj-mgba-x3.gif) |
| Patrouille et poursuite réelle de Gargaros | [GIF en jeu](prive/patrouille-poursuite-mgba-x3.gif) |
| Porte coulissante, blanc complet et sortie | [GIF en jeu](prive/porte-sortie-mgba-x3.gif) |
| Gorgouille et Alizon au Mont Braise | [Capture](prive/gorgouille-alizon-mont-braise-x3.png) |
| Combat réel contre Gorgouille niveau 80 | [Capture](prive/combat-gorgouille-80-x3.png) |
| Gorgouille capturé | [Capture](prive/gorgouille-capture-x3.png) |
| Partie rechargée avec Continuer | [Capture](prive/quete-apres-continuer-x3.png) |
| Visibilité pendant la Terr’heure / obscurité restaurée | [Pendant](prive/grotte-sombre-eclairee-x3.png) · [Après](prive/obscurite-restauree-x3.png) |
| OST Infinite Tunnel, sortie audio directe mGBA | [Extrait WAV](prive/infinite-tunnel-mgba.wav) |

Les GIF sont constitués d’images réellement rendues par mGBA. Les équipes, positions et états initiaux des fixtures sont préparés avec les fonctions natives du jeu ; les attaques, captures, déplacements, animations et retours terrain sont exécutés par le moteur.

## Fonctionnement intégré

**Déclenchement.** Le premier rendez-vous obligatoire est choisi entre le Mont Sélénite et la Grotte Sombre, puis mémorisé dans une variable existante de sauvegarde. Un déclenchement aléatoire peut le précéder ailleurs. La Route Victoire sert de garantie supplémentaire si la grotte choisie a été contournée. La première apparition satisfait l’obligation même si le joueur échoue.

Après cette première apparition, un contrôle a lieu tous les 16 pas admissibles : chance de 1/16, ou 1/4 si au moins un membre de l’équipe tient le Short Oni. Deux porteurs ne cumulent pas le bonus. Un répit de 256 pas suit la fin d’un événement, y compris en cas de défaite.

**Grottes.** [L’audit reproductible](AUDIT_GROTTES.json) couvre 27 cartes et 43 liaisons réciproques entre composantes accessibles. Seize étages permettent des poursuivants. Les secteurs trop étroits servent de passages ; la Grotte Bakuku, l’extérieur et le sommet du Mont Braise sont exclus des déclenchements. La rencontre de Gorgouille ne peut donc pas être interrompue par une nouvelle Terr’heure.

Les emplacements évitent l’eau, les corniches, les rochers initiaux, les échelles et les cases qui couperaient un passage. Le choix de la porte utilise les connexions accessibles et une borne conservatrice de 450 pas, soit environ deux minutes de marche normale, pour laisser une marge sur les trois minutes.

**Transition.** La musique baisse, un cri existant retentit, puis les PNJ deviennent progressivement transparents pendant 120 images. Le joueur reste opaque. La grotte devient entièrement visible sans activer définitivement Flash. Le décor passe au monochrome avec un voile doré. Infinite Tunnel remplace la musique de la grotte.

**Chronomètre.** Trois minutes au rythme matériel de la GBA ; blanc, jaune à partir de 60 secondes, rouge sous 30 secondes. Le temps continue dans le menu et le SAC. Il est suspendu pendant les combats et les transitions imposées. Sauvegarder, Vol, Téléport, Tunnel, Corde Sortie et les rencontres sauvages ordinaires ou provoquées sont neutralisés pendant l’événement. Les escaliers internes fonctionnent, les sorties ordinaires sont bloquées.

**Poursuite.** Les Oni cherchent sans connaître initialement la position du joueur. Les patrouilles restent immobiles, tournent leur regard et signalent le joueur avec le point d’exclamation natif et un son. Une alerte persiste sur l’étage, y compris après un aller-retour dans le SAC ; changer d’étage l’annule. Les déplacements respectent les collisions. Ogralos se déplace un peu plus vite que Gargaros ; Orqanos conserve cette vitesse et examine les intersections avant de choisir une direction de recherche.

| Palier | Équipe |
| --- | --- |
| Gargaros | Fouétar 75 |
| Ogralos | Carpitaine 75, Turboss 75 |
| Orqanos | Quatre Superfouétar 80 |

Les portraits de Gargaros et Ogralos sont reliés aux tables de portraits, palettes et animations. Orqanos réutilise son portrait existant. Les combats jouent l’OST de Boss déjà intégrée. Aucun Oni ne possède Gorgouille.

**Fin d’événement.** Une victoire enregistre le palier, retire tous les poursuivants et supprime la limite de temps. Le décor et les restrictions restent actifs jusqu’à la porte. Une défaite termine l’événement et ramène le joueur dans la grotte normale. Les règles de mort définitive et de Game Over du Nuzlocke restent applicables.

Les Poké Balls de récompense utilisent une réserve temporaire : leurs objets sont versés après une sortie réussie, perdus en cas d’échec. Les changements d’étage ne les dupliquent pas. Si le SAC se remplit entre-temps, le PC reçoit les objets ; en dernier recours, une réserve persistante attend qu’une place se libère.

## Alizon Bie et Gorgouille

La conversation postgame au sommet de la Tour Pokémon propose l’enquête. Refuser permet de revenir. Accepter remet le Short Oni, qui peut être équipé et retiré normalement. Les victoires contre les Oni obtenues avant cette conversation comptent aussi.

Après les trois victoires, reparler à Alizon débloque le rendez-vous au Mont Braise. Sa présence et celle de Gorgouille nécessitent le postgame, les trois victoires et cette progression de quête.

- **K.O. :** Gorgouille disparaît pour la visite courante, Alizon réagit, puis il revient après une sortie et un retour.
- **Fuite ou défaite :** aucune disparition définitive n’est enregistrée.
- **Capture :** Gorgouille et Alizon quittent définitivement la zone, la quête se termine et le Médallium enregistre le nº65.

Les douze anciennes cases de rencontre sauvage ordinaire de Gorgouille ont été remplacées par Fouétar, aux mêmes niveaux. [Détail des cases](anciennes-rencontres-gorgouille.json). Son indice natif de capture est **45/255**, avec les effets habituels des PV, statuts et Balls. [Exception documentée dans la politique de capture](CAPTURE_GORGOUILLE.json).

La numérotation des 151 espèces est inchangée. Les Gorgouille déjà présents dans d’anciennes sauvegardes sont conservés.

## Vérifications

**78 contrôles ciblés réussis sur la ROM téléchargeable**, dont des combats et une capture réellement exécutés, avec le même SHA-256 dans chacun des rapports :

| Groupe | Contrôles | Résultats |
| --- | ---: | --- |
| Cartes, palettes, porte, menu, minuterie et Flash | 41 | [JSON](prive/TESTS_CARTES_PORTE.json) |
| Conditions de la rencontre statique | 9 | [JSON](prive/TESTS_QUETE.json) |
| Trois combats Oni, défaite, K.O., capture et sauvegarde/Continuer | 11 | [JSON](prive/TESTS_COMBATS_REELS.json) |
| IA, Short Oni, récompenses et dialogues de quête | 13 | [JSON](prive/TESTS_PROGRESSION.json) |
| Transparence et garanties de première apparition | 4 | [JSON](prive/TESTS_TRANSITION.json) |

Le blanc complet de la porte est vérifié jusque dans les 512 entrées de palette matérielle. La minuterie reste arrêtée pendant un vrai combat. Sur la séquence de poursuite mesurée avec les OST, les 120 images observées reçoivent 120 mises à jour du terrain.

Une régression Nuzlocke vérifie également la capture du premier adversaire, le refus du suivant, le secours par un survivant du PC et les Game Over après de vraies attaques : [résultats](../nuzlocke-20261024/regression-terreur-20261025/COMBATS.json).

Ces contrôles sont des fixtures ciblées. Ils ne constituent pas une partie naturelle complète ni une validation à 100% de toute l’aventure. L’équilibrage de la recherche de porte et de la difficulté de chasse reste à apprécier en jouant.

## Mémoire et sauvegardes

| Ressource | Utilisée | Libre |
| --- | ---: | ---: |
| ROM, limite de 32 Mio | 33 489 991 octets | 64 441 octets |
| EWRAM fixe | 261 612 octets | 532 octets |
| IWRAM | 30 912 octets | 1 856 octets |

La session ajoute 192 octets fixes. La recherche de chemin utilise temporairement le tas déjà réservé par le jeu, au maximum 5 880 octets de travail pour les cartes retenues, puis les libère. Aucun pointeur de session ne dépend d’un bloc du tas réinitialisé par un chargement de carte ou de menu.

La taille et les offsets des SaveBlocks ne changent pas : les états permanents utilisent des drapeaux et variables existants auparavant inutilisés. Les PNJ temporaires de la Terr’heure ne sont pas enregistrés dans les souvenirs du journal.

Pour reprendre une partie, copie ta sauvegarde `.sav` sous le même nom que la nouvelle ROM, puis utilise **Continuer**. La ROM précédente et sa sauvegarde peuvent être conservées séparément.
