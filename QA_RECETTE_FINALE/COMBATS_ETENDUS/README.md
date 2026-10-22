# Combats agrandis — moteur GBA

Point de restauration : `af64e4032`. Branche `dev/reconstruction-finalisation` ; master inchangé.

## Rendu

Les302 vues utilisent une géométrie individuelle tirée des151 maquettes. Les dessins récents et leurs indices de palette sont conservés. Des textures de combat centrées sont dérivées des originaux, sans redimensionnement. Le moteur utilise les matrices affines GBA et une fenêtre OBJ double de128×128 pour obtenir les largeurs et hauteurs demandées, au lieu de plafonner à64px.

Les facteurs horizontal et vertical sont indépendants : ils suivent les proportions de chaque maquette. Aucune inversion d'axe. Les dos gardent leur orientation récente et leur bas de corps est masqué par le premier plan natif. La transformation de présentation est composée avec les matrices d'animation, dans le tampon OAM final ; elle ne remplace pas l'état logique des animations.

Les réservations de matrices sont temporaires et restaurées en fin de rendu ; aucun tableau RAM persistant supplémentaire. En cas de manque de matrices, le code reste borné et revient au rendu natif plutôt que d'accéder hors tableau. Les silhouettes utilisées sur BG1/BG2 sont recalculées avec les mêmes pixels et les mêmes facteurs, dans les4096octets existants (maximum actuel3840octets par vue).

Les textures des menus/PC/résumé et les profils overworld antérieurs restent distincts et inchangés. Les cinq dessins shiny dédiés retirés ne sont pas réactivés. Les shiny autorisés utilisent le même dessin que la forme normale, avec leur palette.

## Preuves disponibles

- `apres/001.png` à `151.png` :151 captures réelles mGBA ; action de combat atteinte,302 tampons graphiques et palettes normales vérifiés.
- `comparaisons/comparatif-01.png` à `19.png` : maquette utilisateur / ancien moteur64px / nouveau moteur, tous les rendus du jeu provenant de mGBA.
- `GEOMETRIE_302.json` : dimensions demandées, transformations effectives et ancrages par vue. La quantification des matrices peut laisser un écart d'un pixel.
- `masques/` :36 comparaisons avant OBJ / après BG / différence RGB, sur neuf espèces dont Padrézo, Émettor et Robonyan28, deux côtés et deux BG. Les36 comparaisons sont identiques pixel pour pixel.
- `prototype/` : premier essai intermédiaire avant séparation des textures de menus ; son empreinte ROM est différente du jalon courant. Ces captures restent historiques.

La compilation privée conserve les26 OST et fait31589579octets (30,126Mio), sous32Mio. EWRAM261052octets, IWRAM29888octets, identiques au jalon précédent.

## Bilan final vérifié

-302 vues mesurées sur les captures natives : **302/302 à2pixels maximum** des bords de cadrage demandés (`MESURES_CAPTURES.csv/json`). C'est une mesure du contour visible, pas une égalité des dessins ou poses anciennes.
-26 dos ont reçu une découpe technique individuelle du bas du corps, car le point le plus large du dessin complet passait sous la boîte de dialogue et faussait le zoom du premier plan. Les PNG originaux restent intacts ; `battle_geometry_overrides.json` conserve les limites. La mesure exclut la bordure de dialogue native ày112, alors que la maquette laisse une ligne de plus visible.
-354 scripts d'attaque,1448 cas normaux/shiny et deux côtés, avec variantes de deuxième tour : **PASS**. Fin des scripts, restauration des tuiles/palettes et mode OAM double observé pendant les images actives. Les matrices logiques ne sont pas réécrites. Ce succès technique n'est pas une revue visuelle humaine exhaustive des1448 cas.
-151 demandes shiny en combat : **PASS**,84 acceptées/67 refusées, mêmes tuiles que la forme normale et palettes natives vérifiées.
-36 comparaisons OBJ/BG : **PASS**,0pixel différent, y compris les dos recadrés114,119,149.
-20 captures PC/résumé et20 chargements génériques des cinq anciens shiny spécifiques :30 contrôles **PASS**. Les profils génériques et palettes sont inchangés par rapport à`af64e4032`.
-Métamorph et Clonage : **deux tours réellement joués avec le contrôleur**, retour au menu, espèce/tuiles transformées ou PV/statut du clone vérifiés. Combat double avec quatre acteurs : **PASS**, bornes horizontales visibles contrôlées ; la position est bornée en doubles pour éviter le rognage à gauche. Les tests d'action utilisent des Yo-kai appartenant au joueur et un adversaire limité àTrempette.
-Les19 planches ont été examinées ; les cinq shiny dédiés ne sont pas réactivés, aucune donnée de gameplay ni source audio modifiée.

ROM privée testée :SHA-256 `6368e2c28cae2eeddf1d6439fcd279693fc67b8270d3f1b1bc5d75e3dd71c65c`. Manifestes et résultats : `BILAN_TESTS.json` et `sources/BUILD_SOURCE_MANIFEST.json`.

Les premières tentatives du test de tours étaient incorrectes : B au lieu deA, puis des Yo-kai de niveau50 avec un OT étranger sans trophées déclenchaient la désobéissance et choisissaient une autre attaque. La fixture a été corrigée (OT du joueur, adversaire inoffensif) ; aucun correctif de gameplay n'a été introduit pour forcer le succès.

`CONTROLE_OBSOLETE_BITMAP.json` conserve un premier échec du contrôleur de test : il comparait l'allocation logique de matrices au tampon matériel d'une image précédente. Une matrice matérielle temporaire peut être réallouée logiquement avant le rendu suivant, sans collision. Ce contrôle a été corrigé pour observer le mode OAM réellement produit, sans imposer une synchronisation inexistante. Il ne constitue pas une anomalie démontrée du moteur.

## Limites

Les dessins récents peuvent avoir une pose ou une silhouette différente de l'ancien dessin présent dans une maquette. Égaliser leurs boîtes de cadrage ne transforme pas ces dessins en copies de l'ancien artwork. Les références comportent aussi des halos blancs de détourage, volontairement ignorés. L'identité pixel pour pixel avec chaque maquette n'est donc pas promise.

Les essais sont des scènes natives mGBA après initialisation de nouvelle partie, avec fixtures d'équipe ; ils ne sont pas une aventure complète ni des mesures de performances sur console physique.

## Reconstruction

```sh
python3 tools/yokai/generer_geometrie_combat_etendue.py
make -j4 YOKAI_AUDIO_DIR=/chemin/audio-prive
YOKAI_QA_ROM=$PWD/pokefirered_audio.gba YOKAI_QA_ELF=$PWD/pokefirered_audio.elf python3 tools/yokai/capturer_combats_etendus.py
```

La configuration cloud existante fournit agbcc, devkitARM et mGBA. Les ressources musicales sont privées ; aucune ROM ni ressource audio n'est publiée.
