# FRENCH_TRANSLATION — stratégie de traduction

Objectif : jouer **entièrement en français** en gardant Nathan, Katie, les six Yo-kai, leurs données, animations,
évènements et la progression, **et** rester compatible Archipelago.

## Méthode A — Traduire directement la ROM (Hex Maniac Advance CE)

`jmynes/HexManiacAdvance-CE` (MIT, dernier commit 2026-06-23, .NET 6, Windows) :

| Constat | Preuve |
|---|---|
| HMA reconnaît une ROM par son **code d'en-tête** (`BPEE0`), pas par son hash : il traitera ce hack comme l'Émeraude officielle | `docs/SUPPORTED-ROMS.md` |
| Ses références pour Émeraude sont des **emplacements de pointeurs** fixés sur la ROM officielle (`tableReference.txt`) | colonne `BPEE0` |
| **Mesure** : 370/377 de ces pointeurs sont valides sur l'Émeraude officielle, **27/377 sur ce hack** (8 vers les bonnes données) | script de ROM_ANALYSIS (tableau de référence HMA relu contre les deux ROM) |
| Tables cassées, exemples : noms des types, des classes de dresseurs, descriptions d'attaques, multichoix, écran de nom, noms des natures | idem |

Verdict : **non viable**. Dans ce hack, construit depuis la décompilation, toutes les tables ont bougé : HMA
pointerait à côté. Même un HMA fonctionnel imposerait de retraduire ~14 000 chaînes à la main, de les repointer
(le français est plus long), et ne résoudrait pas Archipelago. HMA n'a pas été lancé ici (application Windows/.NET) ;
le verdict repose sur sa propre table de référence.

## Méthode B — Reconstruire sur une Émeraude française

Une Émeraude française officielle (`BPEF`, No-Intro SHA-1 `ca666651374d89ca439007bed54d839eb7bd14d0`) a tous les
textes officiels. Mais transférer en binaire 6 nouvelles espèces (tableaux dimensionnés par `NUM_SPECIES`, Pokédex,
sauvegarde) dans une ROM compilée est un travail d'assembleur fragile. **Non viable en binaire.**

Viable **en source** : la décompilation **`qigast/pokeemeraude`** (fork maintenu de la décompilation française de
DizzyEgg, synchronisé avec pret le 2026-08-20, `GAME_LANGUAGE = LANGUAGE_FRENCH`) annonce reconstruire **à l'octet**
l'Émeraude française officielle (`rom.sha1` = `ca666651…`). C'est la méthode C appliquée à une base française.

> La compilation de cette décompilation a été **bloquée par une règle de permission** dans cet environnement : la
> reproduction à l'octet **n'est pas vérifiée ici**. Test à faire sur votre PC (BUILD_GUIDE.md, étape 2).

## Méthode C — Reconstruire depuis une décompilation (recommandée)

| Base | Langue | Intérêt | Limite |
|---|---|---|---|
| `pret/pokeemerald` | anglais | base du hack **et** des patchs Archipelago | tout le texte serait à traduire nous-mêmes |
| **`qigast/pokeemeraude`** | **français officiel** | textes, menus, police, noms français **d'origine** | portage du code Archipelago (écrit pour l'anglais) |
| `pokeemeraude-expansion` (qigast / RHH, traduction de pokeemerald-expansion) | français | moderne | moteur très différent : incompatible avec les patchs AP existants |
| `kleeenexfeu/pokeemerald-french` | français | — | arrêté en 2023 |

**Recommandation : `qigast/pokeemeraude`**, avec trois couches de modifications en source :
1. **Yo-kai** : les 6 espèces, les graphismes de Nathan/Katie, le panneau de crédits, les rencontres. Produits par
   `tools/yokai_extract.py` à partir de **votre** ROM du hack (avec l'autorisation du créateur).
2. **Archipelago** : le code C du patch de base (voir ARCHIPELAGO_COMPATIBILITY.md).
3. **Textes ajoutés en français** : seulement ce qui n'existe pas dans le jeu officiel, à écrire nous-mêmes :

| Texte | Volume | Source |
|---|---|---|
| 6 noms d'espèces (10 caractères max) | 6 | noms officiels français de la série Yo-kai Watch, à vérifier un par un |
| catégorie « YO-KAI » | 1 | |
| 6 descriptions Pokédex | 6 | **traduction** des textes du créateur (son travail : à demander) |
| panneau de crédits | 1 | à traduire en gardant les noms Ludo, SonGoku, Nicowico |
| textes ajoutés par le patch Archipelago (messages « objet reçu », options, menu) | ~100-300 | à traduire depuis le code AP choisi |

Points techniques à vérifier pendant le portage :
- Les noms français d'objets et d'attaques sont plus longs ; les messages Archipelago incrustent des noms d'objets
  d'**autres jeux** (fournis par le serveur, souvent en anglais) : prévoir la longueur et les caractères (`é`, `è`,
  `à`, `ç`, `œ` existent dans la table de caractères FR de la décompilation).
- La police et la `charmap.txt` françaises de la décompilation sont celles du jeu officiel : aucun outil de police à créer.

## Droits et conditions

- Le texte officiel français vient de **la cartouche du joueur** : notre patch est un différentiel depuis sa ROM
  française, il ne contient pas le texte officiel.
- pret/pokeemerald, qigast/pokeemeraude et le fork AP de Flit **n'ont aucun fichier de licence** : usage
  communautaire courant, mais pas de droit écrit. Créditer (pret, DizzyEgg, Qigast) et demander en cas de diffusion.
- Les descriptions des Yo-kai et les sprites appartiennent au créateur et aux dessinateurs : **demander avant de
  traduire et de redistribuer** (PERMISSION_REQUEST.md).
- Le nom « Yo-kai Watch » et ses personnages appartiennent à Level-5 : projet non commercial, sans assets officiels
  extraits des jeux Yo-kai Watch.
