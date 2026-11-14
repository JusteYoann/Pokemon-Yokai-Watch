# YOKAI_CONTENT — personnages et Yo-kai du hack

Données lues dans la ROM (outil `tools/yokai_extract.py`). Les noms anglais sont ceux de la ROM ; les noms
français indiqués entre parenthèses sont ceux de la série Yo-kai Watch en France, **à confirmer** avant traduction.

## Personnages

| Rôle vanilla | Remplacé par (identification visuelle) | Éléments remplacés |
|---|---|---|
| Brendan (garçon) | **Nathan Adams** | illustration de dresseur avant/arrière + palette ; tous les sprites de terrain |
| May (fille) | **Katie Forester** | idem |

Aucun nom de personnage n'est écrit dans le jeu (le joueur saisit son nom). Le rival garde le rôle et les dialogues
de Brendan/May : le rival affiche donc **l'autre** personnage Yo-kai.

## Les six Yo-kai (et non cinq)

Ce sont des espèces **ajoutées** (n° interne 412 à 417, après CHIMECHO) : aucune espèce vanilla n'est remplacée.
Toutes : catégorie Pokédex « YOKAI », croissance Moyenne, cycles d'œuf 10, bonheur 70, taux de capture 190.
**Aucune n'évolue.**

| N° interne / national / Hoenn | Nom ROM | Types | PV/Att/Déf/Vit/AttSp/DéfSp (total) | Talents | Objets tenus | Sexe |
|---|---|---|---|---|---|---|
| 412 / 387 / 203 | JIBANYAN (Jibanyan) | Spectre / Combat | 164/51/61/88/43/61 (468) | Joli Sourire, Cran | Baie Oran, Grelot Zen | mâle |
| 413 / 388 / 204 | KOMASAN (Komasan) | Spectre / Normal | 136/66/58/63/76/58 (457) | Joli Sourire, Benêt | Lait Meumeu, Pierre Plante | mâle |
| 414 / 389 / 205 | KOMAJIRO (Komajiro) | Spectre / Normal | 136/66/62/63/68/62 (457) | Joli Sourire, Benêt | Lait Meumeu, Pierre Plante | mâle |
| 415 / 390 / 206 | BLIZZARIA (Hyperzéro ? à confirmer) | Spectre / Glace | 196/68/73/86/109/73 (605) | Joli Sourire, Attention | Baie Fraive, Glace Éternelle | **femelle** |
| 416 / 391 / 207 | GARGAROS (Ogre rouge ? à confirmer) | Spectre / Acier | 240/118/89/92/67/89 (695) | Tête de Roc, Pression | —, Bandeau | mâle |
| 417 / 392 / 208 | WHISPER (Whisper) | Spectre / **type 255 invalide** | 110/53/78/12/23/78 (354) | Lévitation | Pièce Rune, Bandeau | mâle |

Groupes d'œufs : Jibanyan, Komasan, Komajiro Terrestre/Amorphe ; Blizzaria Fée/Amorphe ; Gargaros Monstre/Amorphe ;
Whisper Amorphe. Rendement d'EXP : 82 (120 pour Gargaros et Whisper).

### Attaques apprises par niveau

| Yo-kai | Liste (niveau : attaque, noms anglais de la ROM) | Remarque |
|---|---|---|
| Jibanyan | 1 Wrap, 6 Growl, 9 Astonish, 14 Confusion, 17 Take Down, 22 Uproar, 25 Yawn, 30 Psywave, 33 Double-Edge, 38 Heal Bell, 41 Safeguard, 46 Psychic | = liste d'Éoko (Chimecho) |
| Komasan | 1 Growl, 4 Will-O-Wisp, 10 Quick Attack, 13 Helping Hand, 19 Fire Spin, 22 Encore, 24 Transform, 28 Fake Tears, 31 Charge, 37 Fire Blast, 40 Baton Pass, 47 Agility, 60 Metronome | base Posipi, version Feu |
| Komajiro | identique à Komasan avec Thunder Wave, Spark, Thunder | base Négapi |
| Blizzaria | 1 Headbutt, Leer, Bite, Double Team ; 10 Ice Ball, 15 Confuse Ray, 25 Fake Tears, 30 Haze, 35 Ice Beam, 36 Hail, 40 Shadow Ball, 45 Will-O-Wisp, 51 Blizzard, 60 Destiny Bond | |
| Gargaros | 1 Pound, Leer, Focus Energy, Bide ; 4 Focus Energy, 8 Bide, 12 Low Kick, 16 Rock Throw, 25 Bulk Up, 30 Metal Sound, 33 Rock Slide, 37 Meteor Mash, 41 Scary Face, 45 Focus Punch, 51 Super Fang | doublons niv. 1/4/8 |
| Whisper | 1 Hypnosis, Lick, Spite ; 8 Spite, 13 Mean Look, 16 Curse, 21 Night Shade, 25 Shadow Punch, 31 Confuse Ray, 39 Dream Eater, 48 Destiny Bond | base Fantominus |

CT/CS : Jibanyan, Komasan et Komajiro partagent la même liste (24, dont Psychic, Shadow Ball, Calm Mind) ;
Blizzaria et Gargaros une autre (23, dont Ice Beam, Blizzard, Earthquake, Hyper Beam) ; Whisper 28 (dont
Thunderbolt, Brick Break, Sludge Bomb, Strength, Rock Smash). Chacun a une liste d'attaques par œuf.

### Pokédex

| N° | Taille / poids | Description (anglais, ROM) |
|---|---|---|
| 387 Jibanyan | 0,7 m / 5,4 kg | « After being run over by a truck, he inspirits an intersection and seeks to get his revenge on passing trucks. » |
| 388 Komasan | 0,7 m / 5,4 kg | « Komasan is a guardian lion-dog that got bored with guarding his shrine. Now he's looking for a new one. » |
| 389 Komajiro | 0,7 m / 2,4 kg | **bug** : affiche le texte de Whisper ; le sien (« Komasan's younger twin… ») n'est pas référencé |
| 390 Blizzaria | 1,1 m / 7,4 kg | « Now she can fully control her chilling power… » |
| 391 Gargaros | 2,2 m / 110 kg | « A giant red Oni that appears in children's nightmares… » |
| 392 Whisper | **0 / 0** | **bug** : entrée vide, pointeur de description nul |

## Où les obtenir : 106 emplacements sauvages, aucun don ni dresseur

| Yo-kai | Emplacements | Exemples (niveaux) |
|---|---|---|
| Jibanyan | 18 | Route 101 (3), 103 (2), 104 (4), 112, 114 (×2), 116, 119, 123, Mont Mémoria 1F-6F, Caverne Granite (salle de Pierre), Pilier Céleste 3F |
| Komasan | 15 | Routes 103, 104, 110, 112, 117, 121 ; Mont Mémoria ; Pilier Céleste 5F ; Caverne Granite |
| Komajiro | 16 | Routes 101, 103, 104, 110, 112, 117, 123 ; Mont Mémoria ; Pilier Céleste 5F |
| Blizzaria | 20 | Routes 102, 103, 115 (×2), 120, 121, 123 ; Grotte Tréfonds (5, dont **niv. 1-100**) ; Mont Mémoria ; Pilier Céleste 3F |
| Gargaros | 19 | Routes 102, 103, 111, 113, 118 (×2), 120 ; Caverne Granite 1F ; Chemin Ardu ; Météorite ; Mont Mémoria ; Pilier Céleste 1F |
| Whisper | 18 | Routes 102, 103, 104, 111, 116, 118, 119, 120 ; Mont Mémoria ; Pilier Céleste 1F ; Météorite |

Dès la Route 101 (niv. 3), donc dans les toutes premières minutes de jeu. Liste complète et reproductible :
`python3 tools/yokai_extract.py <rom> <sortie>` → `species.json`, champ `wild_encounters`.

## Graphismes extraits (non versionnés)

Pour chaque Yo-kai : `front.png`, `back.png` (64×64, PNG indexé 16 couleurs), `normal.pal`, `shiny.pal` (JASC),
`icon.png` + id de palette d'icône ; pour les personnages : `BRENDAN_front.png`, `MAY_front.png` + palettes.
Ces fichiers sont **le travail du créateur et des dessinateurs** (Ludo pour Jibanyan, SonGoku et Nicowico pour les
autres, selon les crédits de la ROM) : ils ne sont **pas** versionnés tant qu'une autorisation n'est pas obtenue
(voir PERMISSION_REQUEST.md).
