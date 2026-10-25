# Terr’heure — patrouilles stables à l’écran

Le remplacement des patrouilles pouvait apparaître au bord visible de l’écran. De plus, les identifiants supplémentaires 236 à 241 n’étaient pas protégés de la suppression native hors champ.

Les huit identifiants de patrouille sont désormais conservés par le moteur. Une patrouille visible ne peut pas être recyclée ; une marge plus large protège les arrivées hors champ. Les remplacements sont placés au-delà de la zone visible, avec une marge pour la taille des sprites, puis peuvent entrer à pied dans l’écran.

Cinq [contrôles ciblés dans mGBA](TESTS.json) passent : maintien des huit identifiants hors champ, maintien d’une patrouille proche sur 90 vérifications, créations hors de la zone visible, ancrages stables et plafond de difficulté conservé. Vérifications par situations préparées, sans nouvelle vidéo.

Le chrono reste à cinq minutes et le texte annonce toujours 5 MINUTES. Les fondus d’introduction et de victoire sont conservés.

[Télécharger la ROM](Pokemon_Yokai_Watch_Beta_0.1_Patrouilles_Stables.gba)

Taille : 33517639 octets. SHA-256 : `85fbf1ea4324abf81e17f870225bd95dac5960c8618e2cf47ed88691554279b9`. Format des sauvegardes conservé.

Branche dédiée : `fix/terre-heure-regard-oni-20261025`. Aucune fusion sur `master`.
