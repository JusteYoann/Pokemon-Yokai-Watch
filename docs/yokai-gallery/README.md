# Galerie Pokémon × Yo-kai Watch — 151 espèces

Galerie de contrôle des ressources réellement intégrées : aucune image de référence WebP ni nouveau dessin. Les sprites de combat gardent le canevas complet 64 × 64 et une échelle uniforme **×3**, sans recadrage ; face et dos sont côte à côte. Les icônes sont affichées **×4**, première frame sur deux. Les damiers sont des pixels opaques des PNG RGB 8 bits.

Les couleurs proviennent des palettes **RGB555 de la ROM**, développées vers RGB 8 bits sans recoloration. Les shinies utilisent leurs palettes existantes : ils ne sont pas de nouveaux sprites.

Les marges du canevas sont conservées. Ces planches ne simulent pas le terrain de combat ni les offsets appliqués par le moteur ; les coordonnées actuelles sont consignées dans [le manifeste](source-manifest.json).

## 1. Sprites de combat normaux

### 001–025
[Ouvrir en pleine résolution](normal/001-025.png)

![Sprites de combat normaux 001–025](normal/001-025.png)

### 026–050
[Ouvrir en pleine résolution](normal/026-050.png)

![Sprites de combat normaux 026–050](normal/026-050.png)

### 051–075
[Ouvrir en pleine résolution](normal/051-075.png)

![Sprites de combat normaux 051–075](normal/051-075.png)

### 076–100
[Ouvrir en pleine résolution](normal/076-100.png)

![Sprites de combat normaux 076–100](normal/076-100.png)

### 101–125
[Ouvrir en pleine résolution](normal/101-125.png)

![Sprites de combat normaux 101–125](normal/101-125.png)

### 126–150
[Ouvrir en pleine résolution](normal/126-150.png)

![Sprites de combat normaux 126–150](normal/126-150.png)

### 151–151
[Ouvrir en pleine résolution](normal/151-151.png)

![Sprites de combat normaux 151–151](normal/151-151.png)

## 2. Sprites shiny

### 001–025
[Ouvrir en pleine résolution](shiny/001-025.png)

![Sprites shiny 001–025](shiny/001-025.png)

### 026–050
[Ouvrir en pleine résolution](shiny/026-050.png)

![Sprites shiny 026–050](shiny/026-050.png)

### 051–075
[Ouvrir en pleine résolution](shiny/051-075.png)

![Sprites shiny 051–075](shiny/051-075.png)

### 076–100
[Ouvrir en pleine résolution](shiny/076-100.png)

![Sprites shiny 076–100](shiny/076-100.png)

### 101–125
[Ouvrir en pleine résolution](shiny/101-125.png)

![Sprites shiny 101–125](shiny/101-125.png)

### 126–150
[Ouvrir en pleine résolution](shiny/126-150.png)

![Sprites shiny 126–150](shiny/126-150.png)

### 151–151
[Ouvrir en pleine résolution](shiny/151-151.png)

![Sprites shiny 151–151](shiny/151-151.png)

## 3. Icônes

Image fixe : frame 0 de l’animation existante. Palette d’icône sélectionnée par la table du jeu ; pas de variante shiny d’icône inventée.

### 001–025
[Ouvrir en pleine résolution](icons/001-025.png)

![Icônes 001–025](icons/001-025.png)

### 026–050
[Ouvrir en pleine résolution](icons/026-050.png)

![Icônes 026–050](icons/026-050.png)

### 051–075
[Ouvrir en pleine résolution](icons/051-075.png)

![Icônes 051–075](icons/051-075.png)

### 076–100
[Ouvrir en pleine résolution](icons/076-100.png)

![Icônes 076–100](icons/076-100.png)

### 101–125
[Ouvrir en pleine résolution](icons/101-125.png)

![Icônes 101–125](icons/101-125.png)

### 126–150
[Ouvrir en pleine résolution](icons/126-150.png)

![Icônes 126–150](icons/126-150.png)

### 151–151
[Ouvrir en pleine résolution](icons/151-151.png)

![Icônes 151–151](icons/151-151.png)

## Données et vérifications

Les **906 ressources** sont : 302 sprites de combat (151 faces + 151 dos), 151 icônes à deux frames, 151 empreintes et 302 palettes de combat (151 normales + 151 shiny). Les trois palettes d’icônes partagées sont supplémentaires. Les empreintes sont présentes dans l’instantané mais ne constituent pas une quatrième galerie demandée.

Les 906 ressources ont été retrouvées byte pour byte dans la ROM compilée au moment de l’export ; indices des PNG sources et palettes RGB555 vérifiés. Enma est bien **150 / SPECIES_MEWTWO**. Les 151 numéros apparaissent exactement une fois dans chaque section, soit **755 vues** affichées (302 normales, 302 shiny, 151 icônes).

Les PNG sont opaques, non entrelacés et sans profil de couleur. Les sprites/palettes du jeu et la ROM sont inchangés. Cette galerie permet une revue hors jeu ; elle ne remplace pas un test en émulateur.

## Régénérer la galerie

La branche galerie est autonome : l’[instantané compact](sources/gba-graphics.zip) conserve les données indexées nécessaires. Aucun fichier ROM n’est distribué.

Avec Python et Pillow, depuis la racine du dépôt :

```sh
python3 docs/yokai-gallery/scripts/gallery.py
```

Pour rafraîchir cet instantané depuis le checkout de développement complet et sa ROM compilée (modifications du jeu non incluses dans cette branche) :

```sh
python3 docs/yokai-gallery/scripts/gallery.py --refresh
```

[Manifeste des sources](source-manifest.json) · [Rapport de validation](validation.json)
