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
