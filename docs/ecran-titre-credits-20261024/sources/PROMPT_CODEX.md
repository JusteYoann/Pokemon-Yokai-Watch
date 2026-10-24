# PROMPT INTÉGRAL POUR CODEX — ÉCRAN-TITRE + CRÉDITS

Projet : `JusteYoann/Pokemon-Yokai-Watch` (Pokémon Rouge Feu × Yo-kai Watch).
Ce dossier contient le logo ORIGINAL retenu par Yoann, les références visuelles
et l'audio des crédits. Lire tous les documents avant toute modification.
**NE JAMAIS MERGER SUR MASTER SANS AUTORISATION EXPLICITE.**

## 0. Méthode de travail

1. Vérifier HEAD, branche active, changements non commités, allocations ROM,
   moteur audio, écrans intro/titre, séquence crédits et déclencheurs existants.
2. Faire d'abord un rapport d'audit sur les assets/capacités GBA et proposer
   découpage des tâches. Créer/utiliser une branche dédiée.
3. Implémenter par étapes testables, avec captures mGBA et commits atomiques.
4. **Ne pas casser** les scènes existantes de Carmin-sur-Mer, Cramois'Île
   (phases A/B/C selon état réel), Yopple, Don Morléone/Don Spiraton,
   ni les drapeaux/save/load/postgame.
5. Aucun ajout de nouvelle OST pour l'écran-titre ; aucun merge master.

## A. Nouvelle entrée en jeu

### Écran noir de signature

- Au lancement, retirer/sauter la cinématique d'ouverture habituelle
  pour aboutir à une page NOIRE, sobre, avec uniquement le texte blanc exact
  `by Juste Yoann` centré.
- Durée indicative ~2 secondes, léger fondu à l'entrée/sortie si le matériel
  le permet ; **silence total** pendant ce carton.
- Ne pas supprimer par erreur le tutoriel de nouvelle partie du professeur
  Chen lorsque l'utilisateur sélectionne « Nouvelle partie ».

### Écran-titre principal

- À la sortie du carton, démarrer une piste musicale et faire apparaître
  la fresque mythologique en fond.
- Le LOGO fourni dans `REFERENCES/Logo_Yo-kai_Watch_original.png` doit être
  utilisé, correctement adapté à la résolution/palette de la GBA.
- Ne jamais utiliser le logo Yo-kai Watch 4++, une modification « GBA »,
  un logo artificiellement redessiné ou un sous-titre.
- Le logo doit se révéler progressivement en **~5 secondes** :
  fade-in doux (ou effet techniquement équivalent) sans clignotement.
- Dès la fin de son apparition, montrer `PRESS START` sous le logo ;
  légère pulsation/clignotement lisible.
- Fresque **PANORAMIQUE ET ANIMÉE** sur le fond derrière :
  grand rouleau illustré façon peintures mythologiques japonaises,
  personnages Yo-kai de tailles très variées, nuages, temples, montagnes.
  Style ancien, papier doré et encres douces (voir `BRIEF_FRESQUE.md`).
- Fresque se déplaçant **très lentement de gauche vers la droite**
  (point de départ ~2–3 pixels/s), de façon fluide à ~60 images/s,
  boucle transparente/continue; PAS un fond immobile, PAS du scrolling
  rapide; logo et PRESS START ne bougent PAS.
- Tant que le joueur ne presse pas START : animation et musique continuent.

### Choix de l'OST titre — délégué à Codex

- **Choisir UNIQUEMENT parmi les pistes déjà intégrées** et disponibles
  sur la configuration audio active de la ROM. Aucune nouvelle musique,
  instrument, copie WAV, ni sample ajouté sans approbation.
- Audit des `MUS_YOKAI_*` dans le dépôt, avec écoute effective ou
  aperçu mGBA des candidats; privilégier une intro musicale PROGRESSIVE,
  douce, compatible avec les cinq secondes de révélation du logo.
- **Mystic Grove est rejetée** par Yoann pour cette fonction : elle
  commence trop brutalement. `Take Care` était une proposition, **pas
  une validation**. Il faut comparer les autres titres, pas imposer
  une piste sans écoute.
- Donner à Yoann piste choisie, motif, point de départ et preuve sonore/
  vidéo avant validation finale.

### START : exigence audio cruciale

- Quand le joueur appuie sur START : arrêter la BGM de l'écran-titre,
  sans laisser la piste continuer derrière le menu.
- Ouvrir le MENU DE SÉLECTION DE SAUVEGARDE STANDARD de Pokémon Rouge Feu
  (Continuer/Nouvelle partie/Options selon état de sauvegarde).
- **AUCUNE MUSIQUE DE FOND dans ce menu de sauvegarde.**
  Les petits SFX de navigation et de validation peuvent rester normaux.
- La musique du titre ne doit pas repartir pendant la consultation du menu,
  ni en sortie/retour involontaire : tester les chemins retour, Start,
  sauvegarde absente/présente, Nouvelle partie, Continuer, Options.
- Lors du lancement effectif d'une partie, les musiques de la scène/du jeu
  reprennent selon la logique habituelle.

## B. Crédits — évocation de l'aventure

### Identité globale

- Référence : mise en page des crédits de **Super Mario 64**, PAS une
  vidéo plein écran. Fond NOIR, photos/souvenirs petit format et
  textes indépendants.
- Utiliser des **captures réelles mGBA du jeu** comme souvenirs,
  en pixel art FRLG (pas d'illustration IA pour les souvenirs).
- Alterner positions et dimensions : image à gauche, droite,
  haut/bas/centre selon séquence, en laissant respirer le fond noir.
- Les textes de crédits apparaissent/disparaissent également en FONDU,
  dans l'espace noir libre, sans jamais cacher un sujet de la photo.
- Chaque souvenir classique dure **entre 7 et 8 secondes tout compris** :
  fondu d'entrée, pose visible, fondu de sortie, sans allonger la durée
  par inadvertance. Une valeur moyenne ~7,26 s est compatible avec
  31 scènes sur 225 s.
- Les images ne remplissent PAS tout l'écran. Dimensions de référence
  indicatives ~80×60 à 120×80 px selon composition, à tester en 240×160.
- Favoriser des transitions douces. Prévoir contrôles contre flicker,
  palettes saturées, texte illisible, coupures audio et dépassement VRAM.

### Musique crédits

- Audio fourni par Yoann : `AUDIO_ORIGINAL/Credits_OST_fourni_par_Yoann.rar`,
  qui contient « Yo-kai Watch 1 for Nintendo Switch - Credits (Nate).mp3 »,
  durée mesurée ~255,14 s, source MP3 stéréo 44,1 kHz, environ 6,12 Mo.
- La musique est la **préférence de Yoann**, mais l'espace ROM est limité.
  Étudier une conversion GBA réaliste (séquence M4A instrumentale si
  possible, échantillons/streaming seulement si qualité et espace le
  permettent). Auditer précisément le budget réel du ROM, pas EWRAM.
- Ne pas supprimer des fichiers de musique encore utilisés; ne pas
  remplacer aveuglément l'OST actuelle `MUS_YOKAI_TAKE_CARE` avant
  comparaison et accord. Si l'audio ne tient pas, proposer un scénario
  alternatif sans casser le build.
- Synchroniser le dernier souvenir sur les ~30 dernières secondes
  de cette OST si elle est retenue.

### Storyboard

Lire `STORYBOARD_CREDITS_32.csv` : 32 scènes dans l'ordre prévisionnel
de l'aventure, dont **31 souvenirs classiques + 1 final**.
Le storyboard peut être réordonné UNIQUEMENT pour corriger un écart
avec les événements réellement implémentés, et ces corrections
doivent être soumises à Yoann.
Ne pas montrer dans les crédits des événements non présents dans le jeu
sans accord; signaler les scènes pas encore capturables.

### Souvenir final — exception de 30 secondes

- La 32e scène dure **environ 30 secondes**, contre 7–8 pour les autres.
- Image entièrement CENTRÉE, fixe, plus généreuse que les mini-captures
  précédentes, toujours sur fond noir.
- Il s'agit d'une **capture réalisée dans mGBA**, d'une scène de groupe
  utilisant les VRAIS sprites overworld du jeu. Pas d'illustration
  dessinée/IA. Préparer un décor de réunion/photo de groupe adapté.
- Tous les personnages PRINCIPAUX doivent être proches du protagoniste,
  avec les Yo-kai emblématiques. Liste de composition indicative :
  protagoniste, rival, Ariane, Usapion, Nathan ou Katie selon choix,
  Nathaniel/Michael, Hovernyan, Matt, Domniscian, Don Morléone,
  Don Spiraton, Zazel, Enma l'Ancien, Orqanos, Maître Nyada,
  Jibanyan, Whisper et Komasan.
- **EXCLURE Léo et le professeur Chen de ce dernier groupe**, selon
  décision explicite de Yoann.
- Si 18 entités ne sont pas lisibles en 240×160, proposer agencement
  à 2–3 rangées et photo cadrée avant de retirer arbitrairement un
  personnage; les postures peuvent être statiques.
- Texte blanc exact SOUS l'image : `MERCI D'AVOIR JOUÉ !`.
- Timing suggéré sur 30 s : image 0–3 s en fondu;
  texte 3–7 s en fondu; pose 7–25 s; fondu image/texte 25–30 s.
  Terminer sur un NOIR silencieux / comportement de fin standard à
  vérifier. Ne pas ajouter d'autre slogan ou image.

## C. Audit GBA/ROM et validation

- Budget par média en octets avant/après; vérifier le ROM final et
  ses contraintes d'exécution, RAM/VRAM, vblank, chargements et
  performances scrolling/fondu.
- Tester construction de chaque variante applicable, boot et traversée
  titre → START → menu silencieux → partie, présence/absence de sauvegarde,
  transitions retour, crédits complets 4:15, scène finale 30 s.
- Fournir une capture GIF ou vidéo de l'écran-titre (au moins 15 s pour
  voir la fresque) et un extrait représentatif des crédits (incluant
  dernière image) ainsi qu'une planche des 32 captures.
- **Arrêter pour approbation visuelle et sonore de Yoann avant toute fusion**
  ou suppression de contenu utilisé. Aucun merge sur master.

## Point d'attention copyright

Les références et OST fournies servent au travail personnel de ROM hack.
Si diffusion publique envisagée, soumettre au propriétaire la question
des droits des morceaux/enregistrements et des logos.
