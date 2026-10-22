# Portes Mystères — premier prototype jouable

## Intégré dans les sources

Un nouveau Dr Jobard attend à Carmin en **(28,9)**. Après le trophée d’Ariane, il propose une visite Oui/Non. Refuser laisse le joueur en ville; accepter mène à son laboratoire. Le passage reste facultatif et ne verrouille aucune progression existante.

Le laboratoire contient un ordinateur proposant trois destinations : **Stabilité, Orientation, Retour**, plus Annuler/B. Chaque salle permet de consulter sa console, puis de retourner au laboratoire par l’un des trois passages sud. La sortie sud du laboratoire ramène à Carmin en (28,10). Le médecin reconnaît les trois relevés et évoque ses recherches chez Yopple. Les salles restent revisitables après leur achèvement; aucun objet, trophée, expérience ou combat supplémentaire.

Les quatre cartes utilisent le décor de laboratoire natif `LAYOUT_ROUTE25_SEA_COTTAGE`. Elles sont ajoutées au **groupe43**, sans déplacer les identifiants des cartes existantes. Leur décor commun est volontairement réutilisé pour ce premier prototype; il ne s’agit pas de trois salles finales inédites.

## Sprite adapté à la référence du créateur

Le créateur a fourni l’artwork officiel en cours de travail et demandé la même taille et les mêmes proportions générales que Nathan. La première proposition humaine aux cheveux blancs a été écartée avant publication du jeu.

- `graphics/yokai_characters/dr_jobard/source/proposition.png` : nouvelle planche générée d’après la référence fournie. Œil unique jaune, visage vert/violet, blouse et cœur rouge conservés. Appareil externe, poche médicale, tuyaux reliés au cœur et griffes supprimés; mains et mèches simplifiées.
- `overworld.png`, `overworld.pal` : feuille indexée **64×32**, quatre poses natives **16×32**. Les limites visibles correspondent exactement à celles de Nathan : **12×19pixels**, y12..30 pour toutes les poses. Alignement horizontal identique : face/dos x2..13, gauche x1..12, droite x3..14.
- Face, dos, gauche et **droite distincte**; le profil droit n’est pas un simple miroir du gauche, afin de préserver les moitiés de peau. La répartition des couleurs est inversée dans la vue de dos. Le PNJ reste immobile : aucune animation de marche supplémentaire n’est annoncée.
- Indice0 transparent, palette commune16couleurs, **1024octets4bpp +32octets de palette**. Identifiant graphique173, tagpalette0x112B, table d’animations statiques propre au personnage.
- `preview-x8.png` et `comparaison-nathan-jobard-x8.png` montrent les pixels natifs agrandis. La comparaison est une composition technique, pas une capture du moteur. Les quatre captures d’orientation en ville sont, elles, issues de mGBA.
- `production.json`, `PROPORTIONS.json` et `tools/yokai/convertir_dr_jobard.py` documentent la provenance et la conversion reproductible. Le contrôle compare les limites opaques réelles des deux sprites, pas seulement leurs cases de16×32.

Le dessin est produit par image_gen à partir de la référence utilisateur. La conversion technique recadre, réduit au plus proche voisin et quantifie la palette GBA. Les images `archive-human-not-retained.png` et `three-poses-draft.png` conservent les essais écartés; elles ne sont pas liées à la ROM. Les sprites de Nathan et des autres personnages restent inchangés.

## Sauvegardes et stabilité

Six bits jusque-là inutilisés : révision de Carmin0x32E, trois relevés0x32F–0x331, rencontre0x332, calibrage0x333. Aucun ancien drapeau de trophée/récompense réaffecté, aucun format de sauvegarde modifié.

Une ancienne sauvegarde chargée directement dans Carmin recharge une seule fois ses modèles de PNJ pour ajouter le Dr Jobard et place le joueur en (28,10). Les reprises suivantes gardent la position. Les progrès et les relevés restent enregistrés. Dans les nouvelles salles, les vérifications natives de Corde Sortie, Tunnel, Téléport et Vol refusent l’évasion; les sorties normales sont toujours libres.

## Vérifications réellement effectuées

Pour **chacun des profils public et privé**, nouvelles parties lancées par manette avec Nathan et Katie, puis fixtures explicites d’équipe, de trophée et de déplacement :

- Refus avant trophée3 et affichage des quatre orientations du PNJ par interaction native.
- Invitation refusée puis acceptée, annulation par B à l’ordinateur sans téléportation.
- Retour d’une salle sans lire sa console : pas de relevé offert.
- Visite effective des trois salles dans l’ordre3,1,2; lecture des consoles, sauvegarde Flash et Continuer dans chacune, relevé conservé.
- Tous les trois passages de retour et tous les trois passages de sortie du laboratoire, avec réentrées et achèvement persistant.
- Appels des fonctions de garde natives Corde Sortie/Tunnel/Téléport/Vol dans les salles : refus. Ce ne sont pas des essais de sélection de chaque capacité dans le menu de l’équipe.
- Validation du calibrage et interactions répétées : aucun ajout au sac, à l’expérience ou aux autres trophées.
- Fixture d’ancienne sauvegarde de Carmin avec huit modèles de PNJ en cache : neuvième acteur rafraîchi, trophée conservé, seconde reprise stable.
- **38lignes** mesurées avec la police native, maximum192px sur208. Une ligne de221px a été reformulée avant validation.

Les PNG de ce dossier et de `public/` sont des captures du moteur mGBA. Les captures du personnage en ville, du laboratoire et des salles ont été ouvertes et examinées. Le dessin source haute résolution et l’aperçu×8 ne sont pas des captures du jeu.

Ces tests ne sont **pas** un parcours complet depuis Argenta ni une recette du chapitre Yopple. Les fichiers `TEST_MGBA.json` des deux profils détaillent les scénarios et les empreintes. Les anciens PNG de diagnostic éventuels sont nommés explicitement; ils ne constituent pas des validations.

## Limites et suite

Il s’agit du premier chapitre facultatif de rencontre et de manipulation des portes, **pas du scénario complet définitif**. Aucune équipe du Dr Jobard n’est inventée. Sa trahison, le siège de Yopple, Mark Orckerberg, Steve et le changement de donneur de Coupe vers Bérénice restent à intégrer. Le capitaine conserve provisoirement sa fonction actuelle, avec les corrections déjà validées. Le calibrage n’est pas encore une condition imposée au siège de Yopple.

Le créateur a autorisé la création des ressources, puis fourni la référence du Dr Jobard et imposé les dimensions de Nathan. Les textes d’observation et le décor réutilisé restent des choix de prototype, distincts du futur chapitre complet de Yopple.

## Reproduire

```sh
source /workspace/.setup/env.sh
make -j4 YOKAI_AUDIO_DIR=/chemin/vers/les/ressources/privees
YOKAI_QA_ROM=$PWD/pokefirered_audio.gba YOKAI_QA_ELF=$PWD/pokefirered_audio.elf python3 tools/yokai/tester_portes_mysteres_mgba.py
```

Pour le profil public, compiler avec `make -j4`, sélectionner `pokefirered.gba` et son ELF, et définir `YOKAI_MYSTERY_QA_DIR` vers le sous-dossier `public` pour isoler les preuves.
