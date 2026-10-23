# Audit et propositions des 151 palettes

Base : `903281f4982a4b2e5cbe3d6ac8fc6c4cb47dff08`. Palette seule, silhouettes et animations conservées. Aucun merge.

Les 67 exclusions historiques sont conservées : les 151 palettes sont préparées mais seules 84 espèces peuvent actuellement apparaître shiny. Leur activation globale devra être arbitrée après validation visuelle ; ni taux ni rencontres modifiés.

Les zones et les teintes sont des propositions manuelles issues des références, quantifiées en RGB555. Les index peuvent réunir plusieurs zones : la validation porte aussi sur ces approximations locales. Les #008, #018 et #150 présentent des limites détaillées ci-dessous.

## 001 — Jibanyan (`SPECIES_BULBASAUR`)

[ARTWORK_DIRECT — comparaison face/dos](apercus/001-comparaison-x4.png)
Source : `REFERENCES_ORIGINALES/001_Jibanyan.webp`. Reprendre fidèlement TOUTES les zones de couleurs visibles sur l'artwork fourni; adapter ombres, face et dos.

fourrure : index 3,6,7,10 → #e6b633 ; collier : index 4 → #c83b34 ; esprits : index 12,13 → #438bd1.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 002 — Bandinyan (`SPECIES_IVYSAUR`)

[SPECIALE — comparaison face/dos](apercus/002-comparaison-x4.png)
Source : `Sprite normal de l'autre Nyan`. Peau/fourrure du Épinyan NORMAL sur Bandinyan SHINY. Ne pas permuter les vêtements/accessoires.

fourrure : index 4,6,8,11,12 → #a4c54a.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 003 — Épinyan (`SPECIES_VENUSAUR`)

[SPECIALE — comparaison face/dos](apercus/003-comparaison-x4.png)
Source : `Sprite normal de l'autre Nyan`. Peau/fourrure du Bandinyan NORMAL sur Épinyan SHINY. Ne pas permuter les vêtements/accessoires.

fourrure : index 4,6,7,8,9,11 → #a452a4.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 004 — Shogunyan (`SPECIES_CHARMANDER`)

[ARTWORK_DIRECT — comparaison face/dos](apercus/004-comparaison-x4.png)
Source : `REFERENCES_ORIGINALES/004_Shogunyan.webp`. Reprendre fidèlement TOUTES les zones de couleurs visibles sur l'artwork fourni; adapter ombres, face et dos.

armure : index 8,10,11,12,13 → #b62a32 ; casque : index 1,6 → #292a35 ; ornements : index 3,5,7 → #e8c44a.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 005 — Komasan (`SPECIES_CHARMELEON`)

[ARTWORK_DIRECT — comparaison face/dos](apercus/005-comparaison-x4.png)
Source : `REFERENCES_ORIGINALES/005_Komasan.webp`. Reprendre fidèlement TOUTES les zones de couleurs visibles sur l'artwork fourni; adapter ombres, face et dos.

pelage : index 7,8,9,10 → #cda849 ; flammes : index 4,5,6 → #8f5b2e ; habit : index 11,12 → #399eac.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 006 — Komaous (`SPECIES_CHARIZARD`)

[ARTWORK_DIRECT — comparaison face/dos](apercus/006-comparaison-x4.png)
Source : `REFERENCES_ORIGINALES/006_Komaous.webp`. Reprendre fidèlement TOUTES les zones de couleurs visibles sur l'artwork fourni; adapter ombres, face et dos.

pelage : index 6,8,10 → #e8c666 ; flammes : index 3,4,9 → #c3772e ; armure : index 7,11,12 → #398f9b ; details : index 5,13 → #af5d27.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 007 — Komastar (`SPECIES_SQUIRTLE`)

[FAMILLE — comparaison face/dos](apercus/007-comparaison-x4.png)
Source : `REFERENCES_ORIGINALES/006_Komaous.webp`. Adapter les zones homologues (peau, habit, accessoires) aux couleurs de référence de la famille #006; ne PAS copier pixel par pixel.

pelage : index 4,6,7,8 → #e8c666 ; flammes : index 3 → #c3772e ; habit : index 9,12,13 → #398f9b.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 008 — Whisper (`SPECIES_WARTORTLE`)

[SPECIALE — comparaison face/dos](apercus/008-comparaison-x4.png)
Source : `EXTRAS/Whisperocrates_reference.png`. Reproduire les couleurs du visuel Whisperocrates fourni : peau beige crème, robe jaune doré, sombre noir, contour de bouche bleu.

peau : index 3,6,9,10 → #f6e8bb ; bouche : index 4,11 → #3e76b7 ; ombres : index 7,8,12,13 → #ceae69.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.
Le sprite normal ne porte pas de robe : crème et doré adaptés au corps existant, sans inventer de vêtement.

## 009 — Cigalopin (`SPECIES_BLASTOISE`)

[FAMILLE — comparaison face/dos](apercus/009-comparaison-x4.png)
Source : `REFERENCES_ORIGINALES/010_Cigallard.webp`. Adapter les zones homologues (peau, habit, accessoires) aux couleurs de référence de la famille #010; ne PAS copier pixel par pixel.

peau : index 4,8,9,10,11 → #b08539 ; armure : index 3,5,6 → #706449 ; habit : index 1,7 → #ad4b2f.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 010 — Cigallard (`SPECIES_CATERPIE`)

[ARTWORK_DIRECT — comparaison face/dos](apercus/010-comparaison-x4.png)
Source : `REFERENCES_ORIGINALES/010_Cigallard.webp`. Reprendre fidèlement TOUTES les zones de couleurs visibles sur l'artwork fourni; adapter ombres, face et dos.

armure : index 4,5,8,9 → #9c6d39 ; habit : index 10,11,12,13 → #667958 ; details : index 2,7 → #a74735.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 011 — Murhaine (`SPECIES_METAPOD`)

[FAMILLE — comparaison face/dos](apercus/011-comparaison-x4.png)
Source : `REFERENCES_ORIGINALES/012_Saumhonni.webp`. Adapter les zones homologues (peau, habit, accessoires) aux couleurs de référence de la famille #012; ne PAS copier pixel par pixel.

corps : index 8,9,10,11 → #8f3339 ; nageoires : index 2,5,6,7,12,13 → #343039 ; cornes : index 3,4 → #d4b36b.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 012 — Saumhonni (`SPECIES_BUTTERFREE`)

[ARTWORK_DIRECT — comparaison face/dos](apercus/012-comparaison-x4.png)
Source : `REFERENCES_ORIGINALES/012_Saumhonni.webp`. Reprendre fidèlement TOUTES les zones de couleurs visibles sur l'artwork fourni; adapter ombres, face et dos.

corps : index 10,11,13 → #8f3339 ; nageoires : index 1,5,6,7 → #343039 ; cornes : index 4,12 → #d4b36b.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 013 — Dracounet (`SPECIES_WEEDLE`)

[FAMILLE — comparaison face/dos](apercus/013-comparaison-x4.png)
Source : `REFERENCES_ORIGINALES/014_Sir_Dragon.webp`. Adapter les zones homologues (peau, habit, accessoires) aux couleurs de référence de la famille #014; ne PAS copier pixel par pixel.

corps : index 8,9,10,11,12 → #53687d ; cornes : index 1,6 → #bba56b ; nuage : index 4,5 → #c5b2d6.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 014 — Sir Dragon (`SPECIES_KAKUNA`)

[ARTWORK_DIRECT — comparaison face/dos](apercus/014-comparaison-x4.png)
Source : `REFERENCES_ORIGINALES/014_Sir_Dragon.webp`. Reprendre fidèlement TOUTES les zones de couleurs visibles sur l'artwork fourni; adapter ombres, face et dos.

corps : index 2,4,6,7 → #53687d ; cornes : index 9,10,11 → #bba56b ; nuage : index 12,13 → #c5b2d6.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 015 — Octorgone (`SPECIES_BEEDRILL`)

[ARTWORK_DIRECT — comparaison face/dos](apercus/015-comparaison-x4.png)
Source : `REFERENCES_ORIGINALES/015_Octorgone.webp`. Reprendre fidèlement TOUTES les zones de couleurs visibles sur l'artwork fourni; adapter ombres, face et dos.

corps : index 2,3,4,5,6 → #d3c474 ; chevelure : index 7,9 → #ccc06b ; flammes : index 8,10,11,12 → #c4dce5 ; vetement : index 1,13 → #526977.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 016 — Kyubi (`SPECIES_PIDGEY`)

[ARTWORK_DIRECT — comparaison face/dos](apercus/016-comparaison-x4.png)
Source : `REFERENCES_ORIGINALES/016_Kyubi.webp`. Reprendre fidèlement TOUTES les zones de couleurs visibles sur l'artwork fourni; adapter ombres, face et dos.

pelage : index 3,4,5,6,7,8,9,10 → #38373f ; ornements : index 11,12,13 → #507ec7.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 017 — Robonyan (`SPECIES_PIDGEOTTO`)

[ARTWORK_DIRECT — comparaison face/dos](apercus/017-comparaison-x4.png)
Source : `REFERENCES_ORIGINALES/017_Robonyan.webp`. Reprendre fidèlement TOUTES les zones de couleurs visibles sur l'artwork fourni; adapter ombres, face et dos.

metal : index 3,4,5,8,10,11,12 → #d9af32 ; flammes : index 7,13 → #4d9bd5 ; visage : index 6,9 → #eee2b6.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 018 — Robonyan F (`SPECIES_PIDGEOT`)

[ARTWORK_DIRECT — comparaison face/dos](apercus/018-comparaison-x4.png)
Source : `REFERENCES_ORIGINALES/018_Robonyan_F.webp`. Reprendre fidèlement TOUTES les zones de couleurs visibles sur l'artwork fourni; adapter ombres, face et dos.

carrosserie : index 10,11,12 → #3183d4 ; flammes : index 9,13 → #fff1ab ; details : index 2 → #c23c4b.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.
La carrosserie bleue partage ses index : le bicolore rouge/bleu de la référence reste approximatif.

## 019 — Robony.28. (`SPECIES_RATTATA`)

[ARTWORK_DIRECT — comparaison face/dos](apercus/019-comparaison-x4.png)
Source : `REFERENCES_ORIGINALES/019_Robonyan_28.webp`. Reprendre fidèlement TOUTES les zones de couleurs visibles sur l'artwork fourni; adapter ombres, face et dos.

carrosserie : index 2,4,5,8,10,11,12 → #d8ae32 ; coeur : index 6,7 → #c64639.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 020 — Faux Kappa (`SPECIES_RATICATE`)

[ARTWORK_DIRECT — comparaison face/dos](apercus/020-comparaison-x4.png)
Source : `REFERENCES_ORIGINALES/020_Faux_Kappa.webp`. Reprendre fidèlement TOUTES les zones de couleurs visibles sur l'artwork fourni; adapter ombres, face et dos.

peau : index 4,5,8,9,10 → #66aaa6 ; habit : index 6,7,11,12 → #98c8c9 ; cheveux : index 3 → #343943.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 021 — Tukappa (`SPECIES_SPEAROW`)

[FAMILLE — comparaison face/dos](apercus/021-comparaison-x4.png)
Source : `REFERENCES_ORIGINALES/020_Faux_Kappa.webp`. Adapter les zones homologues (peau, habit, accessoires) aux couleurs de référence de la famille #020; ne PAS copier pixel par pixel.

peau : index 7,8,9,10,11 → #66aaa6 ; habit : index 4,5,6 → #98c8c9 ; cheveux : index 12 → #343943.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 022 — Granpapéti (`SPECIES_FEAROW`)

[ARTWORK_DIRECT — comparaison face/dos](apercus/022-comparaison-x4.png)
Source : `REFERENCES_ORIGINALES/022_Granpapeti.webp`. Reprendre fidèlement TOUTES les zones de couleurs visibles sur l'artwork fourni; adapter ombres, face et dos.

peau : index 4,5,6,7 → #e8dfbb ; habit : index 3,8,9 → #d5bb70.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 023 — Puissanfon (`SPECIES_EKANS`)

[FAMILLE — comparaison face/dos](apercus/023-comparaison-x4.png)
Source : `REFERENCES_ORIGINALES/022_Granpapeti.webp`. Adapter les zones homologues (peau, habit, accessoires) aux couleurs de référence de la famille #022; ne PAS copier pixel par pixel.

peau : index 2,4,5,6 → #e8dfbb ; habit : index 7,8,9 → #d5bb70.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 024 — Nanpart (`SPECIES_ARBOK`)

[FAMILLE — comparaison face/dos](apercus/024-comparaison-x4.png)
Source : `REFERENCES_ORIGINALES/025_Passpa.webp`. Adapter les zones homologues (peau, habit, accessoires) aux couleurs de référence de la famille #025; ne PAS copier pixel par pixel.

peau : index 8,9,10,11 → #e9dbc0 ; toiture : index 5,6,7 → #6d5b3b ; habit : index 2,3,4 → #638481.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 025 — Passpa (`SPECIES_PIKACHU`)

[ARTWORK_DIRECT — comparaison face/dos](apercus/025-comparaison-x4.png)
Source : `REFERENCES_ORIGINALES/025_Passpa.webp`. Reprendre fidèlement TOUTES les zones de couleurs visibles sur l'artwork fourni; adapter ombres, face et dos.

peau : index 3,4,7,8 → #e9dbc0 ; toiture : index 2,5,6 → #6d5b3b ; habit : index 9,10,11,12 → #638481.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 026 — Angélik (`SPECIES_RAICHU`)

[FAMILLE — comparaison face/dos](apercus/026-comparaison-x4.png)
Source : `REFERENCES_ORIGINALES/027_Blizzaria.webp`. Adapter les zones homologues (peau, habit, accessoires) aux couleurs de référence de la famille #027; ne PAS copier pixel par pixel.

cheveux : index 3,4,5,6,7 → #c6484c ; habit : index 8,13 → #d22e35.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 027 — Blizzaria (`SPECIES_SANDSHREW`)

[ARTWORK_DIRECT — comparaison face/dos](apercus/027-comparaison-x4.png)
Source : `REFERENCES_ORIGINALES/027_Blizzaria.webp`. Reprendre fidèlement TOUTES les zones de couleurs visibles sur l'artwork fourni; adapter ombres, face et dos.

cheveux : index 1,4,5,6,11 → #c6484c ; habit : index 8,9 → #d22e35.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 028 — Feulion (`SPECIES_SANDSLASH`)

[ARTWORK_DIRECT — comparaison face/dos](apercus/028-comparaison-x4.png)
Source : `REFERENCES_ORIGINALES/028_Feulion.webp`. Reprendre fidèlement TOUTES les zones de couleurs visibles sur l'artwork fourni; adapter ombres, face et dos.

flammes : index 2,7,8,9,10,11,12 → #382b30 ; corps : index 4,5,6 → #a6382a.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 029 — Padrézo (`SPECIES_NIDORAN_F`)

[FAMILLE — comparaison face/dos](apercus/029-comparaison-x4.png)
Source : `REFERENCES_ORIGINALES/030_Emettor.webp`. Adapter les zones homologues (peau, habit, accessoires) aux couleurs de référence de la famille #030; ne PAS copier pixel par pixel.

peau : index 4,5,8,9,10,11,12 → #afd3ce ; habit : index 1,6,7,13 → #534956.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 030 — Émettor (`SPECIES_NIDORINA`)

[ARTWORK_DIRECT — comparaison face/dos](apercus/030-comparaison-x4.png)
Source : `REFERENCES_ORIGINALES/030_Emettor.webp`. Reprendre fidèlement TOUTES les zones de couleurs visibles sur l'artwork fourni; adapter ombres, face et dos.

peau : index 4,5,6,7,8,9,11,12 → #afd3ce ; habit : index 2,10,13 → #534956.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 031 — Crocho (`SPECIES_NIDOQUEEN`)

[ARTWORK_DIRECT — comparaison face/dos](apercus/031-comparaison-x4.png)
Source : `REFERENCES_ORIGINALES/031_Crocho.webp`. Reprendre fidèlement TOUTES les zones de couleurs visibles sur l'artwork fourni; adapter ombres, face et dos.

peau : index 2,4,5,7,9,11,12 → #52505a ; gants : index 8,10 → #4d4654 ; ceinture : index 6,13 → #be4381 ; ornements : index 3 → #b79345.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 032 — Potofeu (`SPECIES_NIDORAN_M`)

[ARTWORK_DIRECT — comparaison face/dos](apercus/032-comparaison-x4.png)
Source : `REFERENCES_ORIGINALES/032_Potofeu.png`. Reprendre fidèlement TOUTES les zones de couleurs visibles sur l'artwork fourni; adapter ombres, face et dos.

marmite : index 4,5,6,7,9,10,11 → #514367 ; marques : index 3,8 → #973dbe ; yeux : index 12,13 → #e6376c.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 033 — Misterre (`SPECIES_NIDORINO`)

[ARTWORK_DIRECT — comparaison face/dos](apercus/033-comparaison-x4.png)
Source : `REFERENCES_ORIGINALES/033_Misterre.webp`. Reprendre fidèlement TOUTES les zones de couleurs visibles sur l'artwork fourni; adapter ombres, face et dos.

terre : index 4,5,6,8,9,10,11,12 → #426982 ; herbe : index 7,13 → #95c7d1.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 034 — Métaureau. (`SPECIES_NIDOKING`)

[PERSONNALISE — comparaison face/dos](apercus/034-comparaison-x4.png)
Source : ``. Peau gris ardoise, cornes dorées, détails rouge sombre (Métaureau).

peau : index 4,6,7,8,9 → #7e8f9e ; cornes : index 10 → #e0b64e ; details : index 1,13 → #8f323d.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.
Mapping confirmé SPECIES_NIDOKING / Métaureau., sprite bovin. Aucun remplacement par Métaurolog.

## 035 — Tauracle (`SPECIES_CLEFAIRY`)

[PERSONNALISE — comparaison face/dos](apercus/035-comparaison-x4.png)
Source : ``. Peau gris anthracite, cornes dorées, ornements pourpres; parenté visuelle avec Métaureau.

peau : index 1,6,10,11,12,13 → #60616d ; cornes : index 7,8,9 → #ddba57 ; ornements : index 3,4 → #8c57ab.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 036 — Poulpatou. (`SPECIES_CLEFABLE`)

[PERSONNALISE — comparaison face/dos](apercus/036-comparaison-x4.png)
Source : ``. Peau rose corail et tentacules violets; adapter les volumes au sprite.

peau : index 5,6,8,10,11,12 → #fa9c91 ; tentacules : index 3,9,13 → #984ea4.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 037 — Poulpater (`SPECIES_VULPIX`)

[PERSONNALISE — comparaison face/dos](apercus/037-comparaison-x4.png)
Source : ``. Même identité rose corail / tentacules violets que Poulpatou, avec ses propres détails.

peau : index 2,3,4,7,11,12 → #fa9c91 ; tentacules : index 1,5,6,8,9,10 → #984ea4.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 038 — Bonneto (`SPECIES_NINETALES`)

[ARTWORK_DIRECT — comparaison face/dos](apercus/038-comparaison-x4.png)
Source : `REFERENCES_ORIGINALES/038_Bonneto.webp`. Reprendre fidèlement TOUTES les zones de couleurs visibles sur l'artwork fourni; adapter ombres, face et dos.

chapeau : index 11,12,13 → #d1c69c ; corps : index 6 → #3f969b ; costume : index 4,5,9,10 → #2b3036.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 039 — Sabri (`SPECIES_JIGGLYPUFF`)

[ARTWORK_DIRECT — comparaison face/dos](apercus/039-comparaison-x4.png)
Source : `REFERENCES_ORIGINALES/039_Sabri.webp`. Reprendre fidèlement TOUTES les zones de couleurs visibles sur l'artwork fourni; adapter ombres, face et dos.

chapeau : index 7,8,9 → #e6b948 ; cape : index 10,11,12,13 → #bd352d ; costume : index 4,6 → #dca534.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 040 — Démophage (`SPECIES_WIGGLYTUFF`)

[ARTWORK_DIRECT — comparaison face/dos](apercus/040-comparaison-x4.png)
Source : `REFERENCES_ORIGINALES/040_Demophage.webp`. Reprendre fidèlement TOUTES les zones de couleurs visibles sur l'artwork fourni; adapter ombres, face et dos.

peau : index 2,3,5,7,8,9,10,12 → #c6b3de ; habit : index 4,6 → #493259 ; perles : index 13 → #be315c.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 041 — Brumette (`SPECIES_ZUBAT`)

[ARTWORK_DIRECT — comparaison face/dos](apercus/041-comparaison-x4.png)
Source : `REFERENCES_ORIGINALES/041_Brumette.webp`. Reprendre fidèlement TOUTES les zones de couleurs visibles sur l'artwork fourni; adapter ombres, face et dos.

nuage : index 2,4,6,7,8,9,10,11 → #e9ba2e ; volutes : index 3 → #f8ecc0.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 042 — Brumella (`SPECIES_GOLBAT`)

[FAMILLE — comparaison face/dos](apercus/042-comparaison-x4.png)
Source : `REFERENCES_ORIGINALES/041_Brumette.webp`. Adapter les zones homologues (peau, habit, accessoires) aux couleurs de référence de la famille #041; ne PAS copier pixel par pixel.

nuage : index 2,3,5,9,10,11,12 → #e9ba2e ; volutes : index 6,7,13 → #f8ecc0.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 043 — Télémir (`SPECIES_ODDISH`)

[ARTWORK_DIRECT — comparaison face/dos](apercus/043-comparaison-x4.png)
Source : `REFERENCES_ORIGINALES/043_Telemir.webp`. Reprendre fidèlement TOUTES les zones de couleurs visibles sur l'artwork fourni; adapter ombres, face et dos.

cadre : index 1,2,3,5,6 → #555467 ; miroir : index 4,7 → #c6b8e8.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 044 — Triptic-t. (`SPECIES_GLOOM`)

[FAMILLE — comparaison face/dos](apercus/044-comparaison-x4.png)
Source : `REFERENCES_ORIGINALES/043_Telemir.webp`. Adapter les zones homologues (peau, habit, accessoires) aux couleurs de référence de la famille #043; ne PAS copier pixel par pixel.

cadre : index 1,3,4,8,9,11,12 → #555467 ; miroir : index 5,6,7,10 → #c6b8e8.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 045 — Nihilistik (`SPECIES_VILEPLUME`)

[FAMILLE — comparaison face/dos](apercus/045-comparaison-x4.png)
Source : `REFERENCES_ORIGINALES/046_Emousstik.webp`. Adapter les zones homologues (peau, habit, accessoires) aux couleurs de référence de la famille #046; ne PAS copier pixel par pixel.

corps : index 2,5,6,7,10,11,12 → #72607f ; ailes : index 3,4,8,9 → #9985a2.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 046 — Émousstik (`SPECIES_PARAS`)

[ARTWORK_DIRECT — comparaison face/dos](apercus/046-comparaison-x4.png)
Source : `REFERENCES_ORIGINALES/046_Emousstik.webp`. Reprendre fidèlement TOUTES les zones de couleurs visibles sur l'artwork fourni; adapter ombres, face et dos.

corps : index 1,2,3,6,7,8,9,10 → #72607f ; ailes : index 4,5 → #9985a2 ; pattes : index 11,12,13 → #b99346.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 047 — Humainequ. (`SPECIES_PARASECT`)

[ARTWORK_DIRECT — comparaison face/dos](apercus/047-comparaison-x4.png)
Source : `REFERENCES_ORIGINALES/047_Humainequin.webp`. Reprendre fidèlement TOUTES les zones de couleurs visibles sur l'artwork fourni; adapter ombres, face et dos.

peau : index 3,6,7,8,9,10,12 → #d7edef ; ceinture : index 13 → #688fa9.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 048 — Slurpent (`SPECIES_VENONAT`)

[PERSONNALISE — comparaison face/dos](apercus/048-comparaison-x4.png)
Source : ``. Serpent bleu clair et blanc; préserver les motifs, les yeux et les contrastes.

serpent : index 2,3,4,5,6,7,9,10,11,12 → #c6e9f5 ; ventre : index 8,13 → #fcfcf1.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 049 — Baku (`SPECIES_VENOMOTH`)

[ARTWORK_DIRECT — comparaison face/dos](apercus/049-comparaison-x4.png)
Source : `REFERENCES_ORIGINALES/049_Baku.webp`. Reprendre fidèlement TOUTES les zones de couleurs visibles sur l'artwork fourni; adapter ombres, face et dos.

corps : index 4,5,6,7,8,9,10,13 → #f1ede2 ; trompe : index 11,12 → #c8b1b0.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 050 — Bakuku (`SPECIES_DIGLETT`)

[FAMILLE — comparaison face/dos](apercus/050-comparaison-x4.png)
Source : `REFERENCES_ORIGINALES/049_Baku.webp`. Adapter les zones homologues (peau, habit, accessoires) aux couleurs de référence de la famille #049; ne PAS copier pixel par pixel.

corps : index 4,6,9,10,11 → #f1ede2 ; couronne : index 3 → #d5b66c.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 051 — Mognyan (`SPECIES_DUGTRIO`)

[PERSONNALISE — comparaison face/dos](apercus/051-comparaison-x4.png)
Source : ``. Fourrure noire, ventre crème et détails turquoise.

fourrure : index 6,8,9,10 → #38333e ; ventre : index 11 → #f1e4c3 ; details : index 5,13 → #40b9ba.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.
Index partagés entre zones : pelage/ventre (#051), cheveux/contours (#066/#067), visage/contours (#121), fourrure/pièces mécaniques (#133), yeux/ornements (#151). Recoloration globale approchée à arbitrer visuellement pour cette espèce.

## 052 — Bouh (`SPECIES_MEOWTH`)

[ARTWORK_DIRECT — comparaison face/dos](apercus/052-comparaison-x4.png)
Source : `REFERENCES_ORIGINALES/052_Bouh.webp`. Reprendre fidèlement TOUTES les zones de couleurs visibles sur l'artwork fourni; adapter ombres, face et dos.

boue : index 5,6,7,8,9,10,12 → #574a50 ; masque : index 4,11 → #516b9f.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 053 — Lacanne (`SPECIES_PERSIAN`)

[PERSONNALISE — comparaison face/dos](apercus/053-comparaison-x4.png)
Source : ``. Aspect canne à sucre rouge rayée de blanc; conserver l'identité propre du sprite.

canne : index 8,9,10,11,12,13 → #f5eee1 ; feuilles : index 4,5,6,7 → #b92c3a.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.
Le sprite ne possède pas de bandes régulières : identité rouge/blanc adaptée aux zones existantes, sans dessiner de rayures nouvelles.

## 054 — Canastelle (`SPECIES_PSYDUCK`)

[PERSONNALISE — comparaison face/dos](apercus/054-comparaison-x4.png)
Source : ``. Aspect canne à sucre rouge rayée de blanc, coordonné à Lacanne.

canne : index 9,10,11,12,13 → #f5eee1 ; feuilles : index 2,6,7,8 → #b92c3a.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.
Le sprite ne possède pas de bandes régulières : identité rouge/blanc adaptée aux zones existantes, sans dessiner de rayures nouvelles.

## 055 — Yvantouse (`SPECIES_GOLDUCK`)

[PERSONNALISE — comparaison face/dos](apercus/055-comparaison-x4.png)
Source : ``. Remplacer uniquement la couleur de peau par celle d'Ed Mémoire NORMAL; autres zones inchangées.

peau : index 6,7,10 → #eee6ac.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 056 — Ed Mémoire (`SPECIES_MANKEY`)

[PERSONNALISE — comparaison face/dos](apercus/056-comparaison-x4.png)
Source : ``. Remplacer uniquement la couleur de peau par celle du Yvantouse normal; autres zones inchangées.

peau : index 6,8,13 → #8bcda4.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 057 — Couchtar (`SPECIES_PRIMEAPE`)

[PERSONNALISE — comparaison face/dos](apercus/057-comparaison-x4.png)
Source : ``. Symboliser le jour/l'aube : jaune crème et orange pastel (pas de transformation de forme).

peau : index 10 → #f6e7b4 ; nuage : index 6,7,8,9 → #ffceb3.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 058 — Noctambill (`SPECIES_GROWLITHE`)

[PERSONNALISE — comparaison face/dos](apercus/058-comparaison-x4.png)
Source : ``. Plumage blanc argenté, ailes gris clair, yeux rouge rubis; allure lunaire.

plumage : index 7,9,10,11,12 → #f0f1f5 ; ailes : index 4,5 → #bdc3cd ; yeux : index 1 → #b72748.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 059 — Fouétar (`SPECIES_ARCANINE`)

[ARTWORK_DIRECT — comparaison face/dos](apercus/059-comparaison-x4.png)
Source : `REFERENCES_ORIGINALES/059_Fouetar.webp`. Reprendre fidèlement TOUTES les zones de couleurs visibles sur l'artwork fourni; adapter ombres, face et dos.

fourrure : index 4,8,9,10,11,12 → #684534 ; visage : index 3,5,6,7,13 → #b4424b.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 060 — Superfoué. (`SPECIES_POLIWAG`)

[FAMILLE — comparaison face/dos](apercus/060-comparaison-x4.png)
Source : `REFERENCES_ORIGINALES/059_Fouetar.webp`. Adapter les zones homologues (peau, habit, accessoires) aux couleurs de référence de la famille #059; ne PAS copier pixel par pixel.

fourrure : index 5,7,9,11,12,13 → #684534 ; visage : index 2,3 → #b4424b.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 061 — Égare-dare (`SPECIES_POLIWHIRL`)

[PERSONNALISE — comparaison face/dos](apercus/061-comparaison-x4.png)
Source : ``. Version sombre « dark » : noir bleuté, détails violet profond; zones lisibles.

carrosserie : index 7,8,9,10,11,12 → #343550 ; accessoires : index 4,5,6 → #273459.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 062 — Chauvekip. (`SPECIES_POLIWRATH`)

[PERSONNALISE — comparaison face/dos](apercus/062-comparaison-x4.png)
Source : ``. Corps violet lavande, ailes bleu nuit, yeux dorés.

corps : index 5,6,7,10,11,12 → #b9a4d6 ; ailes : index 4,9 → #343b69 ; yeux : index 8 → #e5c64d.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 063 — Chihuagla. (`SPECIES_ABRA`)

[FAMILLE — comparaison face/dos](apercus/063-comparaison-x4.png)
Source : `REFERENCES_ORIGINALES/064_Frohuahua.webp`. Adapter les zones homologues (peau, habit, accessoires) aux couleurs de référence de la famille #064; ne PAS copier pixel par pixel.

pelage : index 5,6,7,8,9,10 → #c66550 ; oreilles : index 2 → #b63637 ; details : index 11,12 → #e8c36e.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 064 — Froahuahua (`SPECIES_KADABRA`)

[ARTWORK_DIRECT — comparaison face/dos](apercus/064-comparaison-x4.png)
Source : `REFERENCES_ORIGINALES/064_Frohuahua.webp`. Reprendre fidèlement TOUTES les zones de couleurs visibles sur l'artwork fourni; adapter ombres, face et dos.

pelage : index 5,7,8,9,11,12,13 → #c66550 ; oreilles : index 3,10 → #b63637 ; details : index 4 → #e8c36e.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 065 — Gorgouille (`SPECIES_ALAKAZAM`)

[ARTWORK_DIRECT — comparaison face/dos](apercus/065-comparaison-x4.png)
Source : `REFERENCES_ORIGINALES/065_Gorgouille.webp`. Reprendre fidèlement TOUTES les zones de couleurs visibles sur l'artwork fourni; adapter ombres, face et dos.

peau : index 2,3,7,9,10,11,12 → #a9bac9 ; armure : index 4,5,6,8 → #555960.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 066 — Sirénée (`SPECIES_MACHOP`)

[PERSONNALISE — comparaison face/dos](apercus/066-comparaison-x4.png)
Source : `EXTRAS/Sirenee_Sirenite_reference.webp`. REFERENCE PHOTO NOUVELLE : cheveux bleu-gris lavande, peau ivoire, yeux bleu azur, queue bleu marine, rubans rose corail, ornements anthracite, vêtements crème.

cheveux : index 4,5,7,12 → #9ca7bb ; peau : index 10,11 → #f5e9d8 ; queue : index 1,2,3 → #24436c ; rubans : index 8 → #c66970 ; ornements : index 9,13 → #45454b.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.
Index partagés entre zones : pelage/ventre (#051), cheveux/contours (#066/#067), visage/contours (#121), fourrure/pièces mécaniques (#133), yeux/ornements (#151). Recoloration globale approchée à arbitrer visuellement pour cette espèce.

## 067 — Sirènité (`SPECIES_MACHOKE`)

[PERSONNALISE — comparaison face/dos](apercus/067-comparaison-x4.png)
Source : `EXTRAS/Sirenee_Sirenite_reference.webp`. Même palette que l'image Sirénée/Sirénité : cheveux bleu-gris lavande, peau ivoire, yeux bleus, queue marine, rubans rose corail, ornements anthracite, vêtements crème.

cheveux : index 4,7 → #9ca7bb ; peau : index 8 → #f5e9d8 ; queue : index 9,10,11,12,13 → #24436c ; rubans : index 1,5 → #c66970 ; ornements : index 6 → #45454b.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.
Index partagés entre zones : pelage/ventre (#051), cheveux/contours (#066/#067), visage/contours (#121), fourrure/pièces mécaniques (#133), yeux/ornements (#151). Recoloration globale approchée à arbitrer visuellement pour cette espèce.

## 068 — Papa Ress (`SPECIES_MACHAMP`)

[FAMILLE — comparaison face/dos](apercus/068-comparaison-x4.png)
Source : `REFERENCES_ORIGINALES/069_Ralbouc.jpg`. Adapter les zones homologues (peau, habit, accessoires) aux couleurs de référence de la famille #069; ne PAS copier pixel par pixel.

cheveux : index 7,8,9,10,12 → #8a3f31 ; habit : index 6,11,13 → #dacb97 ; accessoires : index 3 → #bba34c.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 069 — Ralbouc (`SPECIES_BELLSPROUT`)

[ARTWORK_DIRECT — comparaison face/dos](apercus/069-comparaison-x4.png)
Source : `REFERENCES_ORIGINALES/069_Ralbouc.jpg`. Reprendre fidèlement TOUTES les zones de couleurs visibles sur l'artwork fourni; adapter ombres, face et dos.

cheveux : index 8,10,11,12 → #8a3f31 ; habit : index 3,4,7 → #dacb97 ; accessoires : index 13 → #bba34c.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 070 — Sorcophage (`SPECIES_WEEPINBELL`)

[PERSONNALISE — comparaison face/dos](apercus/070-comparaison-x4.png)
Source : ``. Palette argent métallique (Sorcophage); conserver les ombrages et inscriptions.

or : index 2,3,6,7,8,10,11 → #cbd5dc.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 071 — Insomnelle (`SPECIES_VICTREEBEL`)

[ARTWORK_DIRECT — comparaison face/dos](apercus/071-comparaison-x4.png)
Source : `REFERENCES_ORIGINALES/071_Insomnel.webp`. Reprendre fidèlement TOUTES les zones de couleurs visibles sur l'artwork fourni; adapter ombres, face et dos.

corps : index 4,5,6,7,8,9,10,11 → #d26888 ; rayures : index 2,3 → #9d3859 ; ornements : index 12,13 → #e7b75f.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 072 — Tata Aura (`SPECIES_TENTACOOL`)

[ARTWORK_DIRECT — comparaison face/dos](apercus/072-comparaison-x4.png)
Source : `REFERENCES_ORIGINALES/072_Tata_Aura.webp`. Reprendre fidèlement TOUTES les zones de couleurs visibles sur l'artwork fourni; adapter ombres, face et dos.

corps : index 1,2,3,6,7,9,10,11 → #62616f ; fleur : index 5,8 → #e2b753 ; ruban : index 4,12,13 → #704d80.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 073 — Tontonner. (`SPECIES_TENTACRUEL`)

[ARTWORK_DIRECT — comparaison face/dos](apercus/073-comparaison-x4.png)
Source : `REFERENCES_ORIGINALES/073_Tontonnerre.webp`. Reprendre fidèlement TOUTES les zones de couleurs visibles sur l'artwork fourni; adapter ombres, face et dos.

nuage : index 11,12,13 → #696b62 ; armure : index 5,6,7 → #e4ad3d ; fourrure : index 3,4 → #f2e6c8 ; details : index 9 → #6d5a85.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 074 — Antonnerre (`SPECIES_GEODUDE`)

[PERSONNALISE — comparaison face/dos](apercus/074-comparaison-x4.png)
Source : ``. Nuage gris orageux, éclairs bleu électrique; identité cohérente avec Parantonn.

nuage : index 3,4,5,6,8,9,10,11 → #8c99a7 ; eclairs : index 12,13 → #329ef1.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 075 — Parantonn (`SPECIES_GRAVELER`)

[PERSONNALISE — comparaison face/dos](apercus/075-comparaison-x4.png)
Source : ``. Nuage gris orageux, éclairs bleu glacier; identité cohérente avec Antonnerre.

nuage : index 4,5,6,7,8,9,10,11 → #b2bdcb ; eclairs : index 12,13 → #95e6ff.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 076 — Scoltine (`SPECIES_GOLEM`)

[PERSONNALISE — comparaison face/dos](apercus/076-comparaison-x4.png)
Source : ``. Carapace noire et motifs vert émeraude; préserver le volume et les contrastes.

carapace : index 9,10,11,12 → #282e37 ; motifs : index 4,5,6,7,8 → #38aa80.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 077 — Scolérique (`SPECIES_PONYTA`)

[PERSONNALISE — comparaison face/dos](apercus/077-comparaison-x4.png)
Source : ``. Carapace noire et motifs vert émeraude; même famille chromatique que Scoltine.

carapace : index 3,8,9,10,11,12 → #282e37 ; motifs : index 2,4,5,6,7,13 → #38aa80.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 078 — Coléroptè. (`SPECIES_RAPIDASH`)

[FAMILLE — comparaison face/dos](apercus/078-comparaison-x4.png)
Source : `REFERENCES_ORIGINALES/079_Rhinolimit.webp`. Adapter les zones homologues (peau, habit, accessoires) aux couleurs de référence de la famille #079; ne PAS copier pixel par pixel.

armure : index 2,3,4,5,6,7,10,11,12 → #745271 ; ornements : index 8,9 → #e1bc5e.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 079 — Rhinolimit (`SPECIES_SLOWPOKE`)

[ARTWORK_DIRECT — comparaison face/dos](apercus/079-comparaison-x4.png)
Source : `REFERENCES_ORIGINALES/079_Rhinolimit.webp`. Reprendre fidèlement TOUTES les zones de couleurs visibles sur l'artwork fourni; adapter ombres, face et dos.

armure : index 1,2,3,4,5,6,7,8,9 → #745271 ; ornements : index 10,11,12,13 → #e1bc5e.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 080 — Scatcheur (`SPECIES_SLOWBRO`)

[FAMILLE — comparaison face/dos](apercus/080-comparaison-x4.png)
Source : `REFERENCES_ORIGINALES/081_Scarmouche.webp`. Adapter les zones homologues (peau, habit, accessoires) aux couleurs de référence de la famille #081; ne PAS copier pixel par pixel.

corps : index 5,8,9,10,11,12 → #9f443a ; armure : index 3,4,6,7 → #d4bb62.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 081 — Scarmouche (`SPECIES_MAGNEMITE`)

[ARTWORK_DIRECT — comparaison face/dos](apercus/081-comparaison-x4.png)
Source : `REFERENCES_ORIGINALES/081_Scarmouche.webp`. Reprendre fidèlement TOUTES les zones de couleurs visibles sur l'artwork fourni; adapter ombres, face et dos.

corps : index 1,7,8,9,10,11 → #9f443a ; armure : index 3,4,5,6,12,13 → #d4bb62.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 082 — Noko (`SPECIES_MAGNETON`)

[ARTWORK_DIRECT — comparaison face/dos](apercus/082-comparaison-x4.png)
Source : `REFERENCES_ORIGINALES/082_Noko.webp`. Reprendre fidèlement TOUTES les zones de couleurs visibles sur l'artwork fourni; adapter ombres, face et dos.

peau : index 6,7,10,11,12 → #438f93 ; ventre : index 4,5 → #c4d7cd ; ornements : index 3,9,13 → #e8cd69.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 083 — Nénunoko (`SPECIES_FARFETCHD`)

[FAMILLE — comparaison face/dos](apercus/083-comparaison-x4.png)
Source : `REFERENCES_ORIGINALES/082_Noko.webp`. Adapter les zones homologues (peau, habit, accessoires) aux couleurs de référence de la famille #082; ne PAS copier pixel par pixel.

peau : index 3,4,5,6,7,8,9,12,13 → #438f93 ; ventre : index 10 → #c4d7cd ; ornements : index 11 → #e8cd69.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 084 — Tryptik (`SPECIES_DODUO`)

[ARTWORK_DIRECT — comparaison face/dos](apercus/084-comparaison-x4.png)
Source : `REFERENCES_ORIGINALES/084_Trytik.webp`. Reprendre fidèlement TOUTES les zones de couleurs visibles sur l'artwork fourni; adapter ombres, face et dos.

corps : index 1,3,4,8,9,10 → #575363 ; ornements : index 5,6,7 → #879495 ; oeil : index 11,12,13 → #bd486d.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 085 — Carpitaine (`SPECIES_DODRIO`)

[ARTWORK_DIRECT — comparaison face/dos](apercus/085-comparaison-x4.png)
Source : `REFERENCES_ORIGINALES/085 - Carpitaine.webp`. Reprendre fidèlement TOUTES les zones de couleurs visibles sur l'artwork fourni; adapter ombres, face et dos.

peau : index 5,7,8,9,12 → #667c7d ; habit : index 10,11,13 → #313b45 ; ceinture : index 4 → #e9c751.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 086 — Turboss (`SPECIES_SEEL`)

[PERSONNALISE — comparaison face/dos](apercus/086-comparaison-x4.png)
Source : ``. Rose clair, reliefs de peau et accessoires préservés.

peau : index 4,5,6,9,13 → #f0b1c2.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 087 — Kappacap (`SPECIES_DEWGONG`)

[FAMILLE — comparaison face/dos](apercus/087-comparaison-x4.png)
Source : `REFERENCES_ORIGINALES/088 - Appak.webp`. Adapter les zones homologues (peau, habit, accessoires) aux couleurs de référence de la famille #088; ne PAS copier pixel par pixel.

peau : index 9,10,11,12 → #437b83 ; habit : index 2,3,4 → #bed8d9 ; details : index 8,13 → #8498af ; yeux : index 7 → #b1c257.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 088 — Appak (`SPECIES_GRIMER`)

[ARTWORK_DIRECT — comparaison face/dos](apercus/088-comparaison-x4.png)
Source : `REFERENCES_ORIGINALES/088 - Appak.webp`. Reprendre fidèlement TOUTES les zones de couleurs visibles sur l'artwork fourni; adapter ombres, face et dos.

peau : index 4 → #437b83 ; chapeau : index 3,5,6,9,10 → #bed8d9 ; habit : index 7 → #40657b.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 089 — Camaïeul (`SPECIES_MUK`)

[PERSONNALISE — comparaison face/dos](apercus/089-comparaison-x4.png)
Source : ``. Corps blanc cassé, motifs bleu cobalt, petits détails dorés.

corps : index 2,3,6,7,8,9,10,11,12 → #f0eee6 ; motifs : index 4,5 → #3565b4 ; details : index 13 → #d8b94b.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 090 — Glapie (`SPECIES_SHELLDER`)

[PERSONNALISE — comparaison face/dos](apercus/090-comparaison-x4.png)
Source : ``. Corps bleu glacier très pâle, détails rose givré.

corps : index 4,5,6,7,8 → #bce7f2 ; details : index 9,10,11,12,13 → #f3cfdf.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 091 — Chiperpiou (`SPECIES_CLOYSTER`)

[ARTWORK_DIRECT — comparaison face/dos](apercus/091-comparaison-x4.png)
Source : `REFERENCES_ORIGINALES/091 - Chiperpiou.webp`. Reprendre fidèlement TOUTES les zones de couleurs visibles sur l'artwork fourni; adapter ombres, face et dos.

corps : index 4,5,6,7,9,10,12 → #c2714b ; visage : index 3,8,13 → #e0c598.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 092 — Rapiaf (`SPECIES_GASTLY`)

[FAMILLE — comparaison face/dos](apercus/092-comparaison-x4.png)
Source : `REFERENCES_ORIGINALES/091 - Chiperpiou.webp`. Adapter les zones homologues (peau, habit, accessoires) aux couleurs de référence de la famille #091; ne PAS copier pixel par pixel.

corps : index 1,2,4,5,8,9,10,11,12,13 → #c2714b ; visage : index 3,6 → #e0c598.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 093 — Tête de l. (`SPECIES_HAUNTER`)

[PERSONNALISE — comparaison face/dos](apercus/093-comparaison-x4.png)
Source : ``. Teint sensiblement plus pâle; accessoires inchangés.

peau : index 2,4,5,7,8,9,10,11,12 → #f6bdae.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 094 — Potache (`SPECIES_GENGAR`)

[PERSONNALISE — comparaison face/dos](apercus/094-comparaison-x4.png)
Source : ``. Bois de sakura : rose pâle, beige rosé et brun clair; ne pas confondre avec feuillage.

bois : index 4,5,6,7,8,9,10,11,12,13 → #dcaaa6.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 095 — Dépotache (`SPECIES_ONIX`)

[PERSONNALISE — comparaison face/dos](apercus/095-comparaison-x4.png)
Source : ``. Bois de sakura : rose pâle, beige rosé et brun clair; accord avec Potache.

bois : index 3,4,5,7,8,9,10,11,12 → #dcaaa6.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 096 — Navétéran (`SPECIES_DROWZEE`)

[PERSONNALISE — comparaison face/dos](apercus/096-comparaison-x4.png)
Source : ``. Coque de navire dorée avec reliefs métal/or; parties organiques et accessoires préservés.

coque : index 3,5,7,9,10,12 → #d2ad42.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 097 — Navigarma. (`SPECIES_HYPNO`)

[PERSONNALISE — comparaison face/dos](apercus/097-comparaison-x4.png)
Source : ``. Coque de navire dorée avec reliefs métal/or; cohérence avec Navétéran.

coque : index 3,9,10,11,12 → #d2ad42.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 098 — Serg.Ramp. (`SPECIES_KRABBY`)

[PERSONNALISE — comparaison face/dos](apercus/098-comparaison-x4.png)
Source : ``. Autre variante d'escargot connu, inspirée de l'escargot de Bourgogne : coquille brun miel, corps beige; adapter au design exact.

coquille : index 5,6,9,10 → #97662f ; corps : index 8,11,12,13 → #f0dfb5.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 099 — C.Antonic. (`SPECIES_KINGLER`)

[ARTWORK_DIRECT — comparaison face/dos](apercus/099-comparaison-x4.png)
Source : `REFERENCES_ORIGINALES/099 - Coach Antonic.webp`. Reprendre fidèlement TOUTES les zones de couleurs visibles sur l'artwork fourni; adapter ombres, face et dos.

peau : index 7,8,9,10,11 → #b64545 ; habit : index 2,6 → #783a55 ; ornements : index 12 → #d6ad49.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 100 — Usapyon (`SPECIES_VOLTORB`)

[ARTWORK_DIRECT — comparaison face/dos](apercus/100-comparaison-x4.png)
Source : `REFERENCES_ORIGINALES/100 - Usapion.webp`. Reprendre fidèlement TOUTES les zones de couleurs visibles sur l'artwork fourni; adapter ombres, face et dos.

costume : index 9,10,11,12,13 → #e8792c ; visage : index 4,6,7,8 → #75bde3.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 101 — Emperor (`SPECIES_ELECTRODE`)

[FAMILLE — comparaison face/dos](apercus/101-comparaison-x4.png)
Source : `REFERENCES_ORIGINALES/100 - Usapion.webp`. Adapter les zones homologues (peau, habit, accessoires) aux couleurs de référence de la famille #100; ne PAS copier pixel par pixel.

costume : index 5,7,8,9,10 → #e8792c ; visage : index 6,11,12,13 → #75bde3.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 102 — Cast. III. (`SPECIES_EXEGGCUTE`)

[PERSONNALISE — comparaison face/dos](apercus/102-comparaison-x4.png)
Source : ``. Castelius III : BRONZE patiné (étape la moins précieuse des quatre).

metal : index 3,4,5,6,7,8,9,10,11,12,13 → #c58953.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 103 — Cast. II. (`SPECIES_EXEGGUTOR`)

[PERSONNALISE — comparaison face/dos](apercus/103-comparaison-x4.png)
Source : ``. Castelius II : ARGENT gris clair métallique.

metal : index 2,3,4,5,6,7,8,9,10,11,12,13 → #d1d9e2.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 104 — Cast. I. (`SPECIES_CUBONE`)

[PERSONNALISE — comparaison face/dos](apercus/104-comparaison-x4.png)
Source : ``. Castelius I : OR jaune métallique.

metal : index 2,3,4,5,6,7,8,9,10,11,12,13 → #e6be4b.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 105 — Cast. Max. (`SPECIES_MAROWAK`)

[PERSONNALISE — comparaison face/dos](apercus/105-comparaison-x4.png)
Source : ``. Castelius MAX : PLATINE blanc argenté éclatant, plus prestigieux dans la progression retenue.

metal : index 2,3,4,5,6,7,8,9,10,11,12,13 → #f0f4ff.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 106 — Pitou (`SPECIES_HITMONLEE`)

[FAMILLE — comparaison face/dos](apercus/106-comparaison-x4.png)
Source : `REFERENCES_ORIGINALES/107 - Choubidou.webp`. Adapter les zones homologues (peau, habit, accessoires) aux couleurs de référence de la famille #107; ne PAS copier pixel par pixel.

fourrure : index 6,7,8,9 → #a6a2b8 ; accessoires : index 3,4,10,11,12,13 → #62527d.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 107 — Choubidou (`SPECIES_HITMONCHAN`)

[ARTWORK_DIRECT — comparaison face/dos](apercus/107-comparaison-x4.png)
Source : `REFERENCES_ORIGINALES/107 - Choubidou.webp`. Reprendre fidèlement TOUTES les zones de couleurs visibles sur l'artwork fourni; adapter ombres, face et dos.

fourrure : index 4,5,6,7,10,13 → #a6a2b8 ; accessoires : index 1,8,9,11,12 → #62527d.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 108 — Arbrézo (`SPECIES_LICKITUNG`)

[PERSONNALISE — comparaison face/dos](apercus/108-comparaison-x4.png)
Source : ``. Arbre/feuillage sur la tête orange automnal; reste de la silhouette inchangé sauf harmonisation légère.

feuillage : index 4,5 → #ce8437.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 109 — Abrézo So. (`SPECIES_KOFFING`)

[PERSONNALISE — comparaison face/dos](apercus/109-comparaison-x4.png)
Source : ``. Arbre/feuillage sur la tête orange automnal, même règle qu'Arbrézo.

feuillage : index 4,5,6 → #c47e35.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 110 — Espreschi. (`SPECIES_WEEZING`)

[ARTWORK_DIRECT — comparaison face/dos](apercus/110-comparaison-x4.png)
Source : `REFERENCES_ORIGINALES/110 - Espreschiot.webp`. Reprendre fidèlement TOUTES les zones de couleurs visibles sur l'artwork fourni; adapter ombres, face et dos.

peau : index 6,8,9,10,12,13 → #f2c8af ; cheveux : index 1,7 → #bc393e ; habit : index 2,3,4,5 → #3f9a95.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 111 — Duc Delaf. (`SPECIES_RHYHORN`)

[ARTWORK_DIRECT — comparaison face/dos](apercus/111-comparaison-x4.png)
Source : `REFERENCES_ORIGINALES/111 - Duc DeLaFeuille.webp`. Reprendre fidèlement TOUTES les zones de couleurs visibles sur l'artwork fourni; adapter ombres, face et dos.

pelage : index 3,4,5,7,8,9 → #f3dfad ; habit : index 10,11,12,13 → #d74841 ; ailes : index 2 → #f5eee2.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 112 — Feuildech. (`SPECIES_RHYDON`)

[FAMILLE — comparaison face/dos](apercus/112-comparaison-x4.png)
Source : `REFERENCES_ORIGINALES/111 - Duc DeLaFeuille.webp`. Adapter les zones homologues (peau, habit, accessoires) aux couleurs de référence de la famille #111; ne PAS copier pixel par pixel.

pelage : index 4,5,6,7,8,9,10,11 → #f3dfad ; habit : index 2,3 → #d74841 ; ailes : index 12,13 → #f5eee2.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 113 — Sal de ba. (`SPECIES_CHANSEY`)

[PERSONNALISE — comparaison face/dos](apercus/113-comparaison-x4.png)
Source : ``. Peau bleu glacier, vêtements vert menthe.

peau : index 4,11 → #b5e8f4 ; habit : index 5,6,7,8,9,10,12,13 → #9ed5bb.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 114 — XXL de ba. (`SPECIES_TANGELA`)

[PERSONNALISE — comparaison face/dos](apercus/114-comparaison-x4.png)
Source : ``. Peau bleu glacier, vêtements vert menthe, détails turquoise plus marqués.

peau : index 7,9,10,11 → #b5e8f4 ; habit : index 2,3,4,5 → #58c0b7.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 115 — Tristos (`SPECIES_KANGASKHAN`)

[PERSONNALISE — comparaison face/dos](apercus/115-comparaison-x4.png)
Source : ``. Os gris acier métalliques avec reflets discrets; zones non osseuses préservées.

os : index 2,3,5,8,12 → #b1beca.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 116 — Rocky Bad. (`SPECIES_HORSEA`)

[PERSONNALISE — comparaison face/dos](apercus/116-comparaison-x4.png)
Source : ``. Visage et corps vert olive désaturé, reliefs plus sombres.

peau : index 8 → #9a9b76.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 117 — Raton Gla. (`SPECIES_SEADRA`)

[ARTWORK_DIRECT — comparaison face/dos](apercus/117-comparaison-x4.png)
Source : `REFERENCES_ORIGINALES/117 - Raton Glandeur.webp`. Reprendre fidèlement TOUTES les zones de couleurs visibles sur l'artwork fourni; adapter ombres, face et dos.

peau : index 2,3,8,9,10,11 → #b19866 ; habit : index 4,12,13 → #72517b ; ornements : index 5,6,7 → #c77e70.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 118 — Vertipiou (`SPECIES_GOLDEEN`)

[PERSONNALISE — comparaison face/dos](apercus/118-comparaison-x4.png)
Source : ``. Poussin violet assorti à la couleur NORMALE de Chiperpiou; autres détails reconnaissables.

poussin : index 6,7,8,10,11,12,13 → #9b74cf.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 119 — Samoussraï (`SPECIES_SEAKING`)

[ARTWORK_DIRECT — comparaison face/dos](apercus/119-comparaison-x4.png)
Source : `REFERENCES_ORIGINALES/119 - Samoussrai.webp`. Reprendre fidèlement TOUTES les zones de couleurs visibles sur l'artwork fourni; adapter ombres, face et dos.

chapeau : index 3,4,5,7,8,9 → #c94f2d ; habit : index 10,11,12,13 → #6c7748 ; details : index 2 → #e6ca8d.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 120 — Ronimpec (`SPECIES_STARYU`)

[FAMILLE — comparaison face/dos](apercus/120-comparaison-x4.png)
Source : `REFERENCES_ORIGINALES/119 - Samoussrai.webp`. Adapter les zones homologues (peau, habit, accessoires) aux couleurs de référence de la famille #119; ne PAS copier pixel par pixel.

chapeau : index 1,2,5,7,9,10 → #c94f2d ; habit : index 6,8,11,12,13 → #6c7748 ; details : index 4 → #e6ca8d.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 121 — Moufpète (`SPECIES_STARMIE`)

[PERSONNALISE — comparaison face/dos](apercus/121-comparaison-x4.png)
Source : ``. Fourrure gris argenté, marques bleu nuit, museau rose pâle.

fourrure : index 9,11,12 → #c9d0d8 ; rayures : index 3,4,5,8 → #334367 ; nez : index 7 → #e7b8c9.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.
Index partagés entre zones : pelage/ventre (#051), cheveux/contours (#066/#067), visage/contours (#121), fourrure/pièces mécaniques (#133), yeux/ornements (#151). Recoloration globale approchée à arbitrer visuellement pour cette espèce.

## 122 — Gloups (`SPECIES_MR_MIME`)

[PERSONNALISE — comparaison face/dos](apercus/122-comparaison-x4.png)
Source : ``. Corps turquoise et bouche violet foncé, adaptée à la silhouette de Gloups.

corps : index 1,4,5,6,7,10,11,12 → #4dc0ba ; bouche : index 2,3,8,9 → #44345e.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 123 — Chip-Chop (`SPECIES_SCYTHER`)

[PERSONNALISE — comparaison face/dos](apercus/123-comparaison-x4.png)
Source : ``. Corps turquoise foncé, détails violets, coordonné à Gloups.

corps : index 3,4,5,6,8,9,10,11,12,13 → #348e92 ; details : index 1,2,7 → #84519b.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 124 — Chaipo (`SPECIES_JYNX`)

[ARTWORK_DIRECT — comparaison face/dos](apercus/124-comparaison-x4.png)
Source : `REFERENCES_ORIGINALES/124 - Chaipo.webp`. Reprendre fidèlement TOUTES les zones de couleurs visibles sur l'artwork fourni; adapter ombres, face et dos.

corps : index 2,4,5,6,8,9,11,12,13 → #d29237 ; details : index 3,7,10 → #45576d.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 125 — Mémogre (`SPECIES_ELECTABUZZ`)

[FAMILLE — comparaison face/dos](apercus/125-comparaison-x4.png)
Source : `REFERENCES_ORIGINALES/124 - Chaipo.webp`. Adapter les zones homologues (peau, habit, accessoires) aux couleurs de référence de la famille #124; ne PAS copier pixel par pixel.

corps : index 3,4,5,6,7,8,9,10,12 → #d29237 ; details : index 2,11,13 → #45576d.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 126 — Jojojoyeux (`SPECIES_MAGMAR`)

[PERSONNALISE — comparaison face/dos](apercus/126-comparaison-x4.png)
Source : ``. Corps jaune pastel, détails roses et accessoires bleu ciel.

corps : index 3,4,7,9,10,11,12,13 → #f9e59c ; details : index 6 → #c990ae ; accessoires : index 1 → #a4d9ef.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 127 — Chauvkipe. (`SPECIES_PINSIR`)

[FAMILLE — comparaison face/dos](apercus/127-comparaison-x4.png)
Source : `REFERENCES_ORIGINALES/128 - Chauv'coucou.webp`. Adapter les zones homologues (peau, habit, accessoires) aux couleurs de référence de la famille #128; ne PAS copier pixel par pixel.

ailes : index 1,2,3,8,9,11,12 → #414b5b ; toit : index 4,5,6,10 → #9b4b45 ; maison : index 7,13 → #b59d82.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 128 — Chauv'cou. (`SPECIES_TAUROS`)

[ARTWORK_DIRECT — comparaison face/dos](apercus/128-comparaison-x4.png)
Source : `REFERENCES_ORIGINALES/128 - Chauv'coucou.webp`. Reprendre fidèlement TOUTES les zones de couleurs visibles sur l'artwork fourni; adapter ombres, face et dos.

ailes : index 1,2,5,6,7,8 → #414b5b ; toit : index 3,4,9,10 → #9b4b45 ; maison : index 11,12,13 → #b59d82.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 129 — Pachycoul (`SPECIES_MAGIKARP`)

[ARTWORK_DIRECT — comparaison face/dos](apercus/129-comparaison-x4.png)
Source : `REFERENCES_ORIGINALES/129 - Pachycool.webp`. Reprendre fidèlement TOUTES les zones de couleurs visibles sur l'artwork fourni; adapter ombres, face et dos.

corps : index 4,5,6,10,11,12,13 → #5a6f99 ; oreilles : index 8,9 → #a3614f ; ventre : index 7 → #e7dcc4.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 130 — Pachypipi (`SPECIES_GYARADOS`)

[FAMILLE — comparaison face/dos](apercus/130-comparaison-x4.png)
Source : `REFERENCES_ORIGINALES/129 - Pachycool.webp`. Adapter les zones homologues (peau, habit, accessoires) aux couleurs de référence de la famille #129; ne PAS copier pixel par pixel.

corps : index 2,3,4,5,6,7,8,9,10,11,12 → #5a6f99 ; oreilles : index 13 → #a3614f.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 131 — Loubarbare (`SPECIES_LAPRAS`)

[ARTWORK_DIRECT — comparaison face/dos](apercus/131-comparaison-x4.png)
Source : `REFERENCES_ORIGINALES/131 - Loubarbare.webp`. Reprendre fidèlement TOUTES les zones de couleurs visibles sur l'artwork fourni; adapter ombres, face et dos.

corps : index 2,9,10,11 → #59607c ; chapeau : index 4,5,6,7,8 → #d9c15c ; details : index 3,12,13 → #d75a5f.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 132 — Racaïd (`SPECIES_DITTO`)

[ARTWORK_DIRECT — comparaison face/dos](apercus/132-comparaison-x4.png)
Source : `REFERENCES_ORIGINALES/132 - Racaïd.webp`. Reprendre fidèlement TOUTES les zones de couleurs visibles sur l'artwork fourni; adapter ombres, face et dos.

corps : index 4,8,9,10,11,12 → #8b7052 ; chapeau : index 5,6,7,13 → #d3b45f ; habit : index 2,3 → #6b9996.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 133 — Terminyan. (`SPECIES_EEVEE`)

[PERSONNALISE — comparaison face/dos](apercus/133-comparaison-x4.png)
Source : ``. Peau rouge rubis désaturée, plutôt sombre; conserver vêtements, mécanique et accessoires.

peau : index 3,6,7,9 → #b35b6b.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.
Index partagés entre zones : pelage/ventre (#051), cheveux/contours (#066/#067), visage/contours (#121), fourrure/pièces mécaniques (#133), yeux/ornements (#151). Recoloration globale approchée à arbitrer visuellement pour cette espèce.

## 134 — Sabruine (`SPECIES_VAPOREON`)

[ARTWORK_DIRECT — comparaison face/dos](apercus/134-comparaison-x4.png)
Source : `REFERENCES_ORIGINALES/134 - Sabruine.webp`. Reprendre fidèlement TOUTES les zones de couleurs visibles sur l'artwork fourni; adapter ombres, face et dos.

cheveux : index 1,6,9,12 → #4aa7a8 ; habit : index 5,7,8,13 → #dac55a ; parapluie : index 2,3,4,11 → #c64b50.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 135 — Sabrille (`SPECIES_JOLTEON`)

[ARTWORK_DIRECT — comparaison face/dos](apercus/135-comparaison-x4.png)
Source : `REFERENCES_ORIGINALES/135 - Sabrille.webp`. Reprendre fidèlement TOUTES les zones de couleurs visibles sur l'artwork fourni; adapter ombres, face et dos.

peau : index 2,4,5,6,7,8,9 → #e4c2b1 ; habit : index 3,10,11,12,13 → #a7cdbf.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 136 — Fourchela. (`SPECIES_FLAREON`)

[PERSONNALISE — comparaison face/dos](apercus/136-comparaison-x4.png)
Source : ``. Corps noir violacé, langue rouge écarlate, yeux jaune vif.

corps : index 2,4,5,7,8,9,10,11,12 → #3f2e52 ; langue : index 3,6 → #d72e3f ; yeux : index 13 → #f4dc46.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 137 — Felipaix (`SPECIES_PORYGON`)

[PERSONNALISE — comparaison face/dos](apercus/137-comparaison-x4.png)
Source : ``. Une seule modification : son œil devient ORANGE; tout le reste exactement normal.

oeil : index 14 → #f49a29.

Pupilles seules : réindexation locale vers deux cases libres, couleurs normales strictement conservées. Dos strictement identique.

## 138 — M. Felipa. (`SPECIES_OMANYTE`)

[PERSONNALISE — comparaison face/dos](apercus/138-comparaison-x4.png)
Source : ``. Une seule modification : son œil devient ORANGE; tout le reste exactement normal.

oeil : index 14 → #f49a29.

Pupilles seules : réindexation locale vers deux cases libres, couleurs normales strictement conservées. Dos strictement identique.

## 139 — Doyagari (`SPECIES_OMASTAR`)

[PERSONNALISE — comparaison face/dos](apercus/139-comparaison-x4.png)
Source : ``. Vêtements bleu nuit, ornements dorés, silhouette et détails propres préservés.

vetements : index 9,10 → #334e7c ; ornements : index 8 → #dfb855.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 140 — Doyen Doy. (`SPECIES_KABUTO`)

[PERSONNALISE — comparaison face/dos](apercus/140-comparaison-x4.png)
Source : ``. Vêtements bleu nuit, ornements dorés, même famille chromatique que Doyagari.

vetements : index 4,8,9,10,12 → #334e7c ; ornements : index 11 → #dfb855.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 141 — Volroulo (`SPECIES_KABUTOPS`)

[PERSONNALISE — comparaison face/dos](apercus/141-comparaison-x4.png)
Source : ``. Corps bleu turquoise, ailes vert émeraude, détails jaunes.

corps : index 2,3,7,8,9,10,11,12 → #4db8b7 ; ailes : index 4,6,13 → #3e976c ; details : index 5 → #edd356.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 142 — Lulugubre (`SPECIES_AERODACTYL`)

[ARTWORK_DIRECT — comparaison face/dos](apercus/142-comparaison-x4.png)
Source : `REFERENCES_ORIGINALES/142 - Lulugubre.webp`. Reprendre fidèlement TOUTES les zones de couleurs visibles sur l'artwork fourni; adapter ombres, face et dos.

corps : index 1,2,3,4,5,6,7,8,9,10,11,12,13 → #559b9b.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 143 — Toumou (`SPECIES_SNORLAX`)

[FAMILLE — comparaison face/dos](apercus/143-comparaison-x4.png)
Source : `REFERENCES_ORIGINALES/144 - Lamlam'mou.webp`. Adapter les zones homologues (peau, habit, accessoires) aux couleurs de référence de la famille #144; ne PAS copier pixel par pixel.

cheveux : index 2,3,4,5,8,9 → #a1d1dc ; habit : index 6,7,10,11,12,13 → #cdad40.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 144 — Lamlam'mou (`SPECIES_ARTICUNO`)

[ARTWORK_DIRECT — comparaison face/dos](apercus/144-comparaison-x4.png)
Source : `REFERENCES_ORIGINALES/144 - Lamlam'mou.webp`. Reprendre fidèlement TOUTES les zones de couleurs visibles sur l'artwork fourni; adapter ombres, face et dos.

cheveux : index 3,4,5,6,7,8,9,10,11,12,13 → #a1d1dc ; habit : index 1,2 → #cdad40.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 145 — Savantard (`SPECIES_ZAPDOS`)

[ARTWORK_DIRECT — comparaison face/dos](apercus/145-comparaison-x4.png)
Source : `REFERENCES_ORIGINALES/145 - Savantard.webp`. Reprendre fidèlement TOUTES les zones de couleurs visibles sur l'artwork fourni; adapter ombres, face et dos.

peau : index 5,8,13 → #53acc3 ; details : index 6,9,10 → #b93d43 ; ornements : index 12 → #dab64c.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.
Le noir du vêtement partage les index du chapeau et des contours : vêtement conservé sombre au lieu de la blouse blanche de la référence, à arbitrer.

## 146 — Loupépin (`SPECIES_MOLTRES`)

[PERSONNALISE — comparaison face/dos](apercus/146-comparaison-x4.png)
Source : ``. Pomme / peau vert pomme clair, conserver les détails.

pomme : index 11,12,13 → #a8cd62.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 147 — Mademoais. (`SPECIES_DRATINI`)

[PERSONNALISE — comparaison face/dos](apercus/147-comparaison-x4.png)
Source : ``. Aspect pierre d'améthyste, violet minéral; pierre alternative à la version normale.

pierre : index 5,8,11,12,13 → #9971b5.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 148 — Maître Ny. (`SPECIES_DRAGONAIR`)

[PERSONNALISE — comparaison face/dos](apercus/148-comparaison-x4.png)
Source : ``. Évocation de Dark Sidious : noir, violet sombre, peau grisâtre; préserver visage, bâton, identité Maître Nyada, pas de copie du personnage.

peau : index 3,4,10 → #bdada9 ; vetements : index 5,6,11,12,13 → #423447.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 149 — Hovernyan (`SPECIES_DRAGONITE`)

[ARTWORK_DIRECT — comparaison face/dos](apercus/149-comparaison-x4.png)
Source : `REFERENCES_ORIGINALES/149 - Hovernyan.webp`. Reprendre fidèlement TOUTES les zones de couleurs visibles sur l'artwork fourni; adapter ombres, face et dos.

fourrure : index 4,6,7 → #363d40 ; cape : index 9,11,12,13 → #3963ac.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.

## 150 — Enma (`SPECIES_MEWTWO`)

[ARTWORK_DIRECT — comparaison face/dos](apercus/150-comparaison-x4.png)
Source : `REFERENCES_ORIGINALES/150 - Enma.webp`. Reprendre fidèlement TOUTES les zones de couleurs visibles sur l'artwork fourni; adapter ombres, face et dos.

cheveux : index 2,3,4 → #c7d6d4 ; robe : index 6,7,9,10,11,12,13 → #554488 ; ornements : index 5 → #3e9ca5.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.
Référence : autre présentation d’Enma (cheveux clairs, robe violette). Le dessin humain à épée existant est conservé ; seules ses zones sont recolorées.

## 151 — Raltesse (`SPECIES_MEW`)

[PERSONNALISE — comparaison face/dos](apercus/151-comparaison-x4.png)
Source : ``. Variante blanche/grise avec yeux rouges.

corps : index 2,3,4,6,7,9,12,13 → #e3e6eb ; yeux : index 11 → #b82c49.

Palette de 16 entrées, index 0 transparent ; ombres modulées suivant la luminosité des couleurs normales, ancrage médian pondéré face/dos.
Les zones partageant un index suivent la même couleur ; fidélité locale à contrôler sur les aperçus.
Index partagés entre zones : pelage/ventre (#051), cheveux/contours (#066/#067), visage/contours (#121), fourrure/pièces mécaniques (#133), yeux/ornements (#151). Recoloration globale approchée à arbitrer visuellement pour cette espèce.

