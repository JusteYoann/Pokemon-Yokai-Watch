# Écran titre Jibanyan

Logo GBA et fond issus des PNG fournis dans `Nouveau dossier (4).rar`, conservés dans `graphics/yokai_title/source_20261025`. Conversion native RGB555 en couches distinctes, sans tramage : dégradé fixe, silhouette de Jibanyan mobile, logo et texte. Le logo et les caractères PRESS START proviennent des fichiers fournis.

La silhouette monte continûment de 96 pixels pendant **419 images, soit 7,015 secondes** au rythme GBA. A et START sont ignorés avant la fin ; PRESS START apparaît alors et clignote. Le retour au titre par B relance cette introduction.

La brume blanche utilise les motifs de nuages natifs, avec une couverture épaisse en mouvement. Son mélange est identique à la Terr’heure : **3/16 de brume et 13/16 de fond**. Elle passe devant le dégradé et la silhouette ; le logo et le texte restent au premier plan. Aucune musique n’est ajoutée ou reconvertie.

[Contrôles mGBA](TESTS_MGBA.json) : démarrage réel, A/START précoces bloqués, montée monotone jusqu’à sa position finale, 15 nuages effectivement affichés et mouvement visible, menu, retour B et seconde introduction, nouvelles parties Nathan/Katie, sauvegarde native puis Continuer avec nom, sexe et carte conservés. Aucune sauvegarde utilisateur n’a été ouverte ou modifiée. Aucun changement du format de sauvegarde.

[Écran à la fin de la montée](titre-419.png) · [Brume en mouvement](titre-brume.png) · [ROM](Pokemon_Yokai_Watch_Beta_0.1_Titre_Jibanyan.gba).

Branche `feature/titre-jibanyan-brume-20261025`, sans fusion sur master. Les corrections précédentes de la quête Nyada/Démophage, de Domniscian et des souvenirs des crédits sont incluses. Les enregistrements de démonstration restent séparés de la ROM.
