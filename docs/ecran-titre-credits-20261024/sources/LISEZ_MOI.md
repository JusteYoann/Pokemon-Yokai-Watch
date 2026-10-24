# Pokémon Rouge Feu × Yo-kai Watch — Écran-titre et crédits

Livrable de conception à remettre à Codex.

## Fichiers

- `PROMPT_CODEX.md` — cahier des charges technique et artistique complet.
- `STORYBOARD_CREDITS_32.csv` — 31 souvenirs + plan final de 30 secondes.
- `BRIEF_FRESQUE.md` — direction artistique de la toile mythologique animée.
- `REFERENCES/Logo_Yo-kai_Watch_original.png` — logo retenu par Yoann.
- `REFERENCES/Ecran_titre_Yokai_Watch_4_inspiration.jpg` — référence d'ambiance ; **ne pas utiliser son logo 4++**.
- `REFERENCES/Credits_Super_Mario_64_disposition.png` — référence de mise en page variable.
- `REFERENCES/Credits_Yokai_Watch_1_OST_capture.png` — référence historique de la musique choisie.
- `AUDIO_ORIGINAL/Credits_OST_fourni_par_Yoann.rar` — audio transmis par Yoann.

## Décisions impératives

1. Le logo original fourni est le seul logo accepté. Ne pas utiliser les variantes
   expérimentales « GBA », ni les essais de logo redessiné, ni le 4++.
2. Défilement très lent de la fresque de gauche vers la droite, en boucle invisible ;
   logo et « PRESS START » fixes.
3. Codex choisit **une OST déjà présente dans la ROM** pour l'écran-titre après
   écoute/comparaison, en privilégiant une entrée progressive.
4. START **arrête immédiatement la musique de l'écran-titre** et ouvre le menu de
   sélection de sauvegarde existant. Le menu doit demeurer **sans BGM**.
   Les sons de navigation du menu peuvent rester.
5. Crédits : 31 souvenirs de 7 à 8 s, dernier souvenir de ~30 s centré avec
   tous les personnages principaux et « MERCI D'AVOIR JOUÉ ! » dessous.
6. Aucun merge sur `master` sans accord explicite de Yoann.

Les 31 souvenirs du storyboard sont des intentions de capture mGBA. Il ne
s'agit **pas de 31 captures déjà fournies**. Les états de jeu nécessaires
devront être préparés/obtenus puis contrôlés visuellement.
