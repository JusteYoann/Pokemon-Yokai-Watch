# Chantier après playtest B13 — en cours

Le cahier des charges complet est archivé dans `sources/`. Priorités : ambiance sonore puis présentation des sprites. La B13 privée de référence et ses sauvegardes sont conservées. Aucun nouvel événement de quête n’est créé ; Multi Exp. permanent conservé. **Ce dossier n’atteste pas une bêta terminée.**

- `BASELINE.json` : 24 400 776 octets, SHA B13, 13 OST actives sur 15, marge 9 153 656 octets avant 32 Mio.
- `audio/niveaux-baseline-b13.json` : 375 mesures natives mGBA, fenêtres finies analysées par EBU R128 après rejet du continu à 20 Hz. Ce sont des mesures, pas une écoute humaine ni des valeurs intégrales de chaque composition. Enregistrements conservés hors Git.
- `audio/cartographie_cartes.csv` : inventaire des425 cartes avec affectation actuelle ;128 corrections initiales de continuité, puis attributions approuvées appliquées. Route1 rattachée à Palette, Route11 à Carmin. Tests natifs de six passages réussis, voir bilan ci-dessous.
- `audio/propositions_ambiance.csv` : nouvelles attributions proposées avant arbitrage, puis **validées explicitement par le joueur**. Cinq nouveaux échantillons actifs, deux nouveaux choix encore en repli ; quinze choix imposés conservés.
- `sprites/baseline-b13/` : 151 scènes de combat réelles mGBA (chaque espèce sur les deux côtés), dix planches sur damier avec face/dos/icône. Fixtures de combat, sans parcours de capture. Les icônes sont montrées depuis les fichiers sources ; ce n’est pas encore une vérification des 151 dans le menu.
- `sprites/registre_151.csv` : suivi de chaque espèce. Les dix planches ont été examinées par l’assistant avec vision ; aucune approbation artistique humaine n’est revendiquée. Les sources normales/shiny n’ont pas encore été modifiées.

La calibration du mixeur est issue des mesures, sans modifier les DPCM ni les fichiers musicaux : cible indicative −29 LUFS pour les fenêtres de BGM, −28 pour l’interface répétée, −25 pour les autres effets ; renforcement des pistes privées plafonné à ×3 et composantes du volume bornées pour éviter un débordement. Le volume demandé des cris est ramené à 60 %. Les fondus, la réduction pour cris/aide et les pauses de fanfare restent relatifs au niveau calibré. `data/yokai/mixer_calibration.json` documente chaque coefficient ; valeurs définitives à confirmer par mesures et transitions en jeu après compilation.

Le bilan actualisé et les réserves figurent ci-dessous. Les rapports successifs conservent les SHA de chaque ROM testée ; ne pas confondre la baseline et le dernier jalon.

## Jalon présentation et mesures après correction

Les nouvelles attributions de `audio/propositions_ambiance.csv` ont été **validées explicitement par le joueur**. Leurs activations seront suivies séparément ; cette validation ne prétend pas que les nouveaux échantillons sont déjà intégrés.

- `CONTROLE_ROM_LOT1.json` : compilation privée 24 402 484 octets, 906 ressources liées contrôlées, 151 espèces/attaques/évolutions et 433 libellés vérifiés. SHA propre à ce lot, distinct de la B13 reproductible.
- `sprites/presentation-lot1/` : 151 nouveaux combats natifs, 302 vues, dix planches examinées. 28 profils individuels de présentation, dont 24 face/dos, deux icônes et les objets Léo/Usapyon. Les PNG de combat, palettes et indices sont conservés ; les dérivés 4bpp sont construits par `presentation_4bpp.py`, sans mémoire ou calcul ajouté en jeu. Le recadrage vertical des dos est intentionnel ; aucune coupe horizontale n’est permise. Ce lot ne prétend pas que toutes les retouches artistiques et shiny sont terminées.
- `sprites/icones-menu/` : 26 menus d’équipe ouverts aux boutons après une vraie introduction ; les 151 espèces y figurent. Quatre planches examinées, sans revendication de couverture complète des boîtes PC. Des icônes restent imposantes et l’anglais résiduel du menu à une seule espèce est visible ; finitions à suivre.
- `sprites/MISTERRE_CORRECTION.json` : seuls les yeux verts et la bouche de l’objet de carte sont neutralisés ; masque borné, silhouette, mousse sommitale, transparence et palette originales conservées. La proposition graphique entière n’a pas été substituée à l’original.
- `audio/niveaux-audio-lot1.json` : 375 mesures après calibration ; zéro échantillon saturé sur les fenêtres. Hoppers −35,9 → −29 LUFS, combat sauvage natif −15,7 → −29. Les enregistrements restent privés ; mesure instrumentale, sans écoute humaine revendiquée.
- `audio/CONTINUITE_MGBA.json` : six franchissements réels aux boutons, après introduction puis fixtures de position/progression : Carmin/centre/Route11, Palette/labo/Route1. Même piste, horloge strictement avançante sans remise à zéro et aucune pause. L’échec initial d’une fixture sans véritable introduction est conservé dans `audio/diagnostics/` ; le test vérifie désormais aussi l’état valide du mixeur.

Ces preuves portent sur des ROM distinctes dont les empreintes figurent dans chaque JSON. Elles ne prouvent ni une partie complète ni la recette finale. La B13 et ses contrôles SHA restent inchangés. Aucun enregistrement musical, DPCM ou ROM n’est publié.

## Attributions approuvées — jalon 18 OST

Cinq nouvelles compositions sont désormais **réellement liées et lues par le moteur** : Patrol Mission (routes), vs. Yo-kai ~2~ (sauvages/dresseurs/Matt avant Champion), vs. Boss Yo-kai (champions), The Very Curious Yo-kai Watch (intro/titre/Chen) et thème d’Ariane. Les quinze thèmes imposés restent sélectionnés avec leurs rôles particuliers. Réemploi de San Fantastico, Uptown, Mystic Grove et Hoppers dans les zones approuvées ;178 cartes modifiées dans ce lot après les128 corrections initiales de continuité (ces nombres ne s’additionnent pas en cartes uniques).

**État réel :22 sélections /18 échantillons actifs.** Les reprises de Nate’s House et Blossom Heights sont ambiguës : motifs courts très répétitifs, sans boucle complète fiable établie. Leur attribution est enregistrée, leur repli natif explicite. Enma5 et Final25 restent aussi en attente ; aucune boucle arbitraire ne remplace ces quatre pistes.

ROM privée mesurée : **27 064 355 octets (25,81 Mio)**, SHA `ceee3955c48aaa6b0f49b26dba10cfac855f5b773da2254fd1ed23be72cadd1c`, marge **6 490 077 octets** avant32 Mio. Ce n’est pas une nouvelle B13 ni une version finale distribuée. Le profil reproductible est décrit dans `audio/RECONSTRUCTION_PRIVEE.md`.

Preuves supplémentaires :

- `audio/boucles-nouvelles/TEST_MGBA.json` : cinq vrais tours pour chacune des cinq nouvelles pistes ;25 coutures contrôlées dans l’audio natif, corrélations minimales0,952 à0,978. Introduction jouée une fois, SFX/cri et sauvegarde Flash natifs. Appels musicaux isolés après vraie introduction ; ce test ne prouve pas tous les déclencheurs de l’aventure. SHA177ca20… avant les seules extensions cartographiques Sevii.
- `audio/niveaux-nouveaux-calibres.json` : cinq mesures natives après calibration, −29,5 à−29 LUFS sur les fenêtres initiales ; aucun échantillon saturé. Pas d’écoute subjective revendiquée.
- `audio/ariane/TEST_ARIANE_MGBA.json` : huit scénarios réels, refus, victoire/sac plein/retrait différé, revanches, première rencontre postgame et défaite ; thème31 en dialogue,28 en combat,27 restauré ensuite. Équipes et récompense Pierre Lune conservées. Fixtures de progression et équipe forte pour les transitions, pas un test d’équilibrage.
- `audio/transition-sauvage/TEST_MGBA.json` : exploration Mont Sélénite→combat sauvage gagné aux boutons→victoire→exploration ; musique24 restaurée, aucune saturation sur les extraits privés ; allié non participant EXP1000→1120, Multi Exp. permanent confirmé dans ce combat. Ennemi/niveau/position préparés explicitement.
- `audio/CONTINUITE_MGBA.json` : six passages réexécutés sur le dernier ROM, aucune coupure ni remise à zéro observée.
- `audio/CARTES_COMPILEES.json` : les425 en-têtes compilés correspondent aux affectations sources, sans prétendre parcourir425 cartes.
- `audio/LIAISON_18_OST.json`, `PROVENANCE_18_OST.json` : limites, repli public, SHA et boucles des18 ressources privées vérifiés ; treize anciens échantillons inchangés.
- `REGRESSION_MOTEUR_MGBA.json` :13 contrôles natifs, dont151 ensembles d’attaques, règles d’évolution/amitié220+Œuf Chance non consommé, persistance Flash et151 éligibilités shiny avec67 exclusions. Ce test ne valide pas les dessins shiny ni toutes les animations d’attaques.
- `sprites/overworld/MISTERRE_LEO_MGBA.json` : deux objets Misterre, deux captures réelles et transformation de Léo pour garçon/fille ; six contrôles réussis, captures examinées.
- `audio/STOCKAGE_ET_CANDIDATS.json` : inventaire conservateur. Les séquences natives restent référencées par la table ; absence d’un nom dans les scripts ne prouve pas qu’une ressource soit supprimable. **Aucune économie de suppression revendiquée :0 octet.**

### Reprise et réserves

P0 restant : quatre boucles, écoute humaine sur parcours, finition des gabarits/icônes encore imposants et audit des autres overworld, validation artistique shiny. P1 restant : traduction résiduelle (dont CANCEL et menu à un seul membre), descriptions,151 propositions d’habitats avec incertitudes à valider, examen Pierre/Passpa/Nanpart. P2 : titre/intro/aide. Pas de nouvelle quête reportée ni modification des villes/Kanto, statistiques, évolutions, rencontres ou équipes. Aucun parcours intégral, profilage matériel ou validation exhaustive des animations n’est revendiqué. **Recette finale NON TERMINÉE.**

### Reconstruction effectivement vérifiée depuis GitHub

`REPRODUCTIBILITE_CLONE_GITHUB.json` porte sur le commit de jeu `1281cf536e4bb23f0c0a6b3c8c1c0e57a1623815` récupéré par un **clone neuf depuis GitHub**. Aucun objet du jeu, dérivé graphique ou ancien DPCM n’a été copié dans ce clone. Seule la chaîne agbcc/bibliothèques épinglée est réutilisée, avec ses empreintes consignées ; dépendances déjà installées sur le même hôte cloud, pas un nouveau PC Windows.

- ROM publique sans fichiers musicaux protégés :16 777 216 octets, SHA `95b52121c36003738827fbf7ba56362fc02bd515f499a293bf610eb92ab78844`, **identique octet pour octet** à celle du checkout de référence.
- Profil privé reconstruit dans un nouveau dossier externe puis compilation :27 064 355 octets, SHA `ceee3955c48aaa6b0f49b26dba10cfac855f5b773da2254fd1ed23be72cadd1c`, **identique octet pour octet** à la référence18 OST.
- `audio/DECODAGE_REPRO.json` :18 MP3 revérifiés par SHA puis redécodés séparément ; les18 WAV retrouvent les empreintes verrouillées utilisées par le générateur. Les médias eux-mêmes restent privés.

Outils rejouables : `verifier_sources_audio_post_b13.py --help` puis `verifier_reproductibilite_post_b13.py --help`. Les commits de preuve/documentation ultérieurs n’altèrent pas ces ROM. Le script de livraison Windows B13 reste épinglé à sa vraie B13 ; ce jalon post-B13 n’est pas encore conditionné comme une nouvelle bêta utilisateur.
