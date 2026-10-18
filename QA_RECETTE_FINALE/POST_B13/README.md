# Chantier après playtest B13 — en cours

Le cahier des charges complet est archivé dans `sources/`. Priorités : ambiance sonore puis présentation des sprites. La B13 privée de référence et ses sauvegardes sont conservées. Aucun nouvel événement de quête n’est créé ; Multi Exp. permanent conservé. **Ce dossier n’atteste pas une bêta terminée.**

- `BASELINE.json` : 24 400 776 octets, SHA B13, 13 OST actives sur 15, marge 9 153 656 octets avant 32 Mio.
- `audio/niveaux-baseline-b13.json` : 375 mesures natives mGBA, fenêtres finies analysées par EBU R128 après rejet du continu à 20 Hz. Ce sont des mesures, pas une écoute humaine ni des valeurs intégrales de chaque composition. Enregistrements conservés hors Git.
- `audio/cartographie_cartes.csv` : inventaire des 425 cartes ; 128 corrections de continuité vers le thème déjà utilisé par leur ville, centres de soins et labos compris. Route 1 rattachée à Palette, Route 11 à Carmin. Arènes/dojos et donjons scénaristiques explicitement séparés. Tests de portes et connexions à produire.
- `audio/propositions_ambiance.csv` : nouvelles attributions artistiques proposées **avant validation**, non activées. Les 15 choix imposés sont conservés ; aucune nouvelle composition ajoutée pour l’instant.
- `sprites/baseline-b13/` : 151 scènes de combat réelles mGBA (chaque espèce sur les deux côtés), dix planches sur damier avec face/dos/icône. Fixtures de combat, sans parcours de capture. Les icônes sont montrées depuis les fichiers sources ; ce n’est pas encore une vérification des 151 dans le menu.
- `sprites/registre_151.csv` : suivi de chaque espèce. Les dix planches ont été examinées par l’assistant avec vision ; aucune approbation artistique humaine n’est revendiquée. Les sources normales/shiny n’ont pas encore été modifiées.

La calibration du mixeur est issue des mesures, sans modifier les DPCM ni les fichiers musicaux : cible indicative −29 LUFS pour les fenêtres de BGM, −28 pour l’interface répétée, −25 pour les autres effets ; renforcement des pistes privées plafonné à ×3 et composantes du volume bornées pour éviter un débordement. Le volume demandé des cris est ramené à 60 %. Les fondus, la réduction pour cris/aide et les pauses de fanfare restent relatifs au niveau calibré. `data/yokai/mixer_calibration.json` documente chaque coefficient ; valeurs définitives à confirmer par mesures et transitions en jeu après compilation.

Restent notamment : vérifier le résultat sonore, appliquer les corrections individuelles de sprites et comparer en jeu, obtenir la validation des nouvelles attributions musicales, finir les deux boucles, inventaire SFX dédiés, traduction complète, habitats, examen Pierre/Passpa/Nanpart, puis les finitions titre/intro. Aucun bilan final de ces points n’est annoncé à ce stade.

## Jalon présentation et mesures après correction

Les nouvelles attributions de `audio/propositions_ambiance.csv` ont été **validées explicitement par le joueur**. Leurs activations seront suivies séparément ; cette validation ne prétend pas que les nouveaux échantillons sont déjà intégrés.

- `CONTROLE_ROM_LOT1.json` : compilation privée 24 402 484 octets, 906 ressources liées contrôlées, 151 espèces/attaques/évolutions et 433 libellés vérifiés. SHA propre à ce lot, distinct de la B13 reproductible.
- `sprites/presentation-lot1/` : 151 nouveaux combats natifs, 302 vues, dix planches examinées. 28 profils individuels de présentation, dont 24 face/dos, deux icônes et les objets Léo/Usapyon. Les PNG de combat, palettes et indices sont conservés ; les dérivés 4bpp sont construits par `presentation_4bpp.py`, sans mémoire ou calcul ajouté en jeu. Le recadrage vertical des dos est intentionnel ; aucune coupe horizontale n’est permise. Ce lot ne prétend pas que toutes les retouches artistiques et shiny sont terminées.
- `sprites/icones-menu/` : 26 menus d’équipe ouverts aux boutons après une vraie introduction ; les 151 espèces y figurent. Quatre planches examinées, sans revendication de couverture complète des boîtes PC. Des icônes restent imposantes et l’anglais résiduel du menu à une seule espèce est visible ; finitions à suivre.
- `sprites/MISTERRE_CORRECTION.json` : seuls les yeux verts et la bouche de l’objet de carte sont neutralisés ; masque borné, silhouette, mousse sommitale, transparence et palette originales conservées. La proposition graphique entière n’a pas été substituée à l’original.
- `audio/niveaux-audio-lot1.json` : 375 mesures après calibration ; zéro échantillon saturé sur les fenêtres. Hoppers −35,9 → −29 LUFS, combat sauvage natif −15,7 → −29. Les enregistrements restent privés ; mesure instrumentale, sans écoute humaine revendiquée.
- `audio/CONTINUITE_MGBA.json` : six franchissements réels aux boutons, après introduction puis fixtures de position/progression : Carmin/centre/Route11, Palette/labo/Route1. Même piste, horloge strictement avançante sans remise à zéro et aucune pause. L’échec initial d’une fixture sans véritable introduction est conservé dans `audio/diagnostics/` ; le test vérifie désormais aussi l’état valide du mixeur.

Ces preuves portent sur des ROM distinctes dont les empreintes figurent dans chaque JSON. Elles ne prouvent ni une partie complète ni la recette finale. La B13 et ses contrôles SHA restent inchangés. Aucun enregistrement musical, DPCM ou ROM n’est publié.
