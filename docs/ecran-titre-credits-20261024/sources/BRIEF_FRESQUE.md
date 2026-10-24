# Fresque mythologique défilante — Brief artistique

**Support :** un écran GBA 240 × 160 px, affichant une portion d'une
grande toile horizontale beaucoup plus large.

**Référence de composition :** la capture d'écran d'accueil de
Yo-kai Watch 4++ fournie, pour son inspiration de vieux rouleau peint
et sa superposition logo/fond. **Interdit de reprendre son logo 4++.**

**Identité esthétique :**

- Emakimono japonais ancien, papier doré/beige, texture modérée,
  aplats d'encre et contours traditionnels.
- Nuages tourbillonnants crème/or, montagnes, temples et palais,
  zones de respiration autour du logo fixe.
- Plusieurs scènes d'une même légende reliées par des nuages.
- Yo-kai de tailles variées (grands personnages monumentaux, figures
  moyennes et petites), dimensions dictées par leur rôle mythologique.
- Quelques candidats : Enma, Kyubi, Octorgone, Orqanos, Maître Nyada,
  Shogunyan, Hovernyan, Jibanyan, Komasan, Whisper et Noko. Vérifier
  la liste réelle des espèces et leurs designs contre les assets du dépôt.
- Ne pas disposer les personnages en colonnes de portraits ;
  ne pas aligner toutes les têtes sous le logo ; ne pas sacrifier la lisibilité.

**Animation :**

- Panorama défilant très lentement de gauche à droite, sans zoom,
  sans accélération, sans changement de vitesse.
- Cadence de départ souhaitée : environ 2 à 3 pixels/seconde
  à 60 Hz, ajustable visuellement sur l'émulateur.
- Raccord de boucle invisible. Si la toile ne peut pas boucler sans
  discontinuité visible, proposer un raccord graphique avant validation.
- Animation continue indéfiniment tant que le joueur reste sur
  l'écran-titre, sans consommer inutilement EWRAM.
- Logo original au centre, stable et suffisamment contrasté ;
  « PRESS START » juste sous lui, discret et légèrement clignotant.

**Contrainte :** le budget ROM est serré. Auditer taille des tiles,
palettes, tilemaps et système de BG avant la production finale.
Préférer un format natif efficace et des ressources réutilisables ;
éviter une grande image brute non compressée ou une séquence vidéo.
