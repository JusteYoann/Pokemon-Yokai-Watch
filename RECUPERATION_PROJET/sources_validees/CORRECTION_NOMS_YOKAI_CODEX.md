# Pokémon Rouge Feu × Yo-kai Watch — Noms canoniques des 151 Yo-kai

**Version 1.1 — 16 octobre 2026**

## Décision définitive

La liste transmise par le créateur fait foi pour l’orthographe des 151 Yo-kai. Le fichier joint `NOMS_CANONIQUES_151_YOKAI_CODEX.csv` fournit la liste complète et **les correspondances `SPECIES_*` inchangées**.

**Correction de numérotation explicite du créateur :** le n°090 est **Glapie** ; **Sergent Rampant est n°098**, et non n°090. Il y a exactement 151 entrées distinctes, de 001 à 151.

**Attention :** le n°062 **Chauvekipeut** et le n°127 **Chauvkipeut** sont deux entrées distinctes. Ne pas les confondre ni fusionner leurs espèces. Cette modification du n°062 remplace l’ancien nom « Charivari » et doit être traitée comme un renommage volontaire, pas comme une correction mineure de typographie.

**Précision validée :** le Yo-kai n°012 s’écrit **Saumhonni**, et non « Saumonni ». Il s’agit bien de l’orthographe déjà présente dans le Pokédex d’origine ; aucune modification de sa constante `SPECIES_BUTTERFREE` n’est nécessaire.

## Corrections constatées par rapport à `01_POKEDEX_151.csv`

| Numéro | Ancien nom | Nouveau nom officiel |
|---:|---|---|
| 026 | Angelik | **Angélik** |
| 029 | Padrezo | **Padrézo** |
| 034 | Métaurolog | **Métaureaulog** |
| 059 | Fouetar | **Fouétar** |
| 060 | Superfouetar | **Superfouétar** |
| 062 | Charivari | **Chauvekipeut** |
| 064 | Frohuahua | **Froahuahua** |
| 066 | Siréné | **Sirénée** |
| 067 | Sirénité | **Sirènité** |
| 071 | Insomnel | **Insomnelle** |
| 078 | Coléroptere | **Coléroptère** |
| 084 | Trytik | **Tryptik** |
| 089 | Camaueil | **Camaïeul** |
| 100 | Usapion | **Usapyon** |
| 111 | Duc DeLaFeuille | **Duc Delafeuille** |
| 112 | FeuildeChou | **Feuildechou** |
| 119 | Samoussrai | **Samoussraï** |
| 129 | Pachycool | **Pachycoul** |
| 136 | Fourchelang | **Fourchelangue** |
| 139 | Doyaris | **Doyagari** |
| 140 | Doyen Doyaris | **Doyen Doyagari** |

Au total, **21 noms** diffèrent du fichier précédent. Les autres noms du CSV joint sont conservés à l’identique.

## Consignes à Codex

1. **Auditer l'état actuel du dépôt GitHub avant toute modification.** Retrouver la table des noms d'espèces affichés et les autres lieux où des libellés Yo-kai ont été saisis en dur. Prendre `NOMS_CANONIQUES_151_YOKAI_CODEX.csv` comme **source de vérité pour les 151 noms et leur numéro**.
2. **Ne pas modifier les identités des espèces** : ne changer ni l’ordre du Pokédex, ni les `species_id`, ni les `SPECIES_*`, ni les statistiques, types, talents, évolutions, équipes, rencontres, cartes, événements, récompenses ou sprites. Les changements demandés sont des **renommages affichés et corrections documentaires**, pas des remplacements d'espèces.
3. Corriger les **noms visibles** dans le Pokédex, les écrans de combats, les menus, les interfaces, les noms éventuellement codés en dur dans les dialogues et tutoriels, les textes des caméos et les éventuels crédits/documentations. Ne pas modifier les chaînes techniques servant d'identifiants à l'aveugle.
4. Dans les dialogues, **respecter le sens du contexte**, pas un simple remplacement global : certaines phrases n'ont pas vocation à changer si le nom est une partie d'un identifiant, d'une constante ou d'une autre expression. Prendre en compte la décision déjà validée : la région conserve son nom **Kanto**.
5. Vérifier les **limites techniques du moteur GBA** : encodage des accents, caractères spéciaux, espaces et apostrophes ; longueur maximum des noms et affichage des textes dans les différentes interfaces. Plusieurs noms canoniques dépassent les limites habituelles d'un nom d'espèce en troisième génération. **Ne jamais tronquer silencieusement** un nom canonique ; exposer les limites et proposer une solution technique ou une abréviation à faire approuver avant usage.
6. Actualiser les **documents de spécifications** et synthèses qui contiennent des fautes, tout en évitant de modifier ou d'effacer les contenus validés sous prétexte de correction orthographique. Un nom ancien peut subsister dans un historique explicitement étiqueté « ancien » ; le rendu final du jeu doit utiliser exclusivement la forme canonique.
7. Effectuer les modifications, compiler et contrôler les éventuelles erreurs, puis fournir un **rapport de correspondance** : numéro, ancienne orthographe, nouvelle orthographe, fichiers modifiés, problèmes de longueur/encodage, et vérifications réelles.

### Ne pas confondre

- n°029 : **Padrézo** ;
- n°084 : **Tryptik** ;
- n°100 : **Usapyon** ;
- n°062 : **Chauvekipeut** vs n°127 : **Chauvkipeut** ;
- n°139 : **Doyagari** et n°140 : **Doyen Doyagari** ;
- n°098 : **Sergent Rampant**.

## Table canonique complète

| N° | Nom officiel | Constante d'espèce à conserver |
|---:|---|---|
| 001 | Jibanyan | `SPECIES_BULBASAUR` |
| 002 | Bandinyan | `SPECIES_IVYSAUR` |
| 003 | Épinyan | `SPECIES_VENUSAUR` |
| 004 | Shogunyan | `SPECIES_CHARMANDER` |
| 005 | Komasan | `SPECIES_CHARMELEON` |
| 006 | Komaous | `SPECIES_CHARIZARD` |
| 007 | Komastar | `SPECIES_SQUIRTLE` |
| 008 | Whisper | `SPECIES_WARTORTLE` |
| 009 | Cigalopin | `SPECIES_BLASTOISE` |
| 010 | Cigallard | `SPECIES_CATERPIE` |
| 011 | Murhaine | `SPECIES_METAPOD` |
| 012 | Saumhonni | `SPECIES_BUTTERFREE` |
| 013 | Dracounet | `SPECIES_WEEDLE` |
| 014 | Sir Dragon | `SPECIES_KAKUNA` |
| 015 | Octorgone | `SPECIES_BEEDRILL` |
| 016 | Kyubi | `SPECIES_PIDGEY` |
| 017 | Robonyan | `SPECIES_PIDGEOTTO` |
| 018 | Robonyan F | `SPECIES_PIDGEOT` |
| 019 | Robonyan 28 | `SPECIES_RATTATA` |
| 020 | Faux Kappa | `SPECIES_RATICATE` |
| 021 | Tukappa | `SPECIES_SPEAROW` |
| 022 | Granpapéti | `SPECIES_FEAROW` |
| 023 | Puissanfon | `SPECIES_EKANS` |
| 024 | Nanpart | `SPECIES_ARBOK` |
| 025 | Passpa | `SPECIES_PIKACHU` |
| 026 | Angélik | `SPECIES_RAICHU` |
| 027 | Blizzaria | `SPECIES_SANDSHREW` |
| 028 | Feulion | `SPECIES_SANDSLASH` |
| 029 | Padrézo | `SPECIES_NIDORAN_F` |
| 030 | Émettor | `SPECIES_NIDORINA` |
| 031 | Crocho | `SPECIES_NIDOQUEEN` |
| 032 | Potofeu | `SPECIES_NIDORAN_M` |
| 033 | Misterre | `SPECIES_NIDORINO` |
| 034 | Métaureaulog | `SPECIES_NIDOKING` |
| 035 | Tauracle | `SPECIES_CLEFAIRY` |
| 036 | Poulpatouch | `SPECIES_CLEFABLE` |
| 037 | Poulpater | `SPECIES_VULPIX` |
| 038 | Bonneto | `SPECIES_NINETALES` |
| 039 | Sabri | `SPECIES_JIGGLYPUFF` |
| 040 | Démophage | `SPECIES_WIGGLYTUFF` |
| 041 | Brumette | `SPECIES_ZUBAT` |
| 042 | Brumella | `SPECIES_GOLBAT` |
| 043 | Télémir | `SPECIES_ODDISH` |
| 044 | Triptic-tac | `SPECIES_GLOOM` |
| 045 | Nihilistik | `SPECIES_VILEPLUME` |
| 046 | Émousstik | `SPECIES_PARAS` |
| 047 | Humainequin | `SPECIES_PARASECT` |
| 048 | Slurpent | `SPECIES_VENONAT` |
| 049 | Baku | `SPECIES_VENOMOTH` |
| 050 | Bakuku | `SPECIES_DIGLETT` |
| 051 | Mognyan | `SPECIES_DUGTRIO` |
| 052 | Bouh | `SPECIES_MEOWTH` |
| 053 | Lacanne | `SPECIES_PERSIAN` |
| 054 | Canastelle | `SPECIES_PSYDUCK` |
| 055 | Yvantouse | `SPECIES_GOLDUCK` |
| 056 | Ed Mémoire | `SPECIES_MANKEY` |
| 057 | Couchtar | `SPECIES_PRIMEAPE` |
| 058 | Noctambill | `SPECIES_GROWLITHE` |
| 059 | Fouétar | `SPECIES_ARCANINE` |
| 060 | Superfouétar | `SPECIES_POLIWAG` |
| 061 | Égare-dare | `SPECIES_POLIWHIRL` |
| 062 | Chauvekipeut | `SPECIES_POLIWRATH` |
| 063 | Chihuaglagla | `SPECIES_ABRA` |
| 064 | Froahuahua | `SPECIES_KADABRA` |
| 065 | Gorgouille | `SPECIES_ALAKAZAM` |
| 066 | Sirénée | `SPECIES_MACHOP` |
| 067 | Sirènité | `SPECIES_MACHOKE` |
| 068 | Papa Ress | `SPECIES_MACHAMP` |
| 069 | Ralbouc | `SPECIES_BELLSPROUT` |
| 070 | Sorcophage | `SPECIES_WEEPINBELL` |
| 071 | Insomnelle | `SPECIES_VICTREEBEL` |
| 072 | Tata Aura | `SPECIES_TENTACOOL` |
| 073 | Tontonnerre | `SPECIES_TENTACRUEL` |
| 074 | Antonnerre | `SPECIES_GEODUDE` |
| 075 | Parantonn | `SPECIES_GRAVELER` |
| 076 | Scoltine | `SPECIES_GOLEM` |
| 077 | Scolérique | `SPECIES_PONYTA` |
| 078 | Coléroptère | `SPECIES_RAPIDASH` |
| 079 | Rhinolimit | `SPECIES_SLOWPOKE` |
| 080 | Scatcheur | `SPECIES_SLOWBRO` |
| 081 | Scarmouche | `SPECIES_MAGNEMITE` |
| 082 | Noko | `SPECIES_MAGNETON` |
| 083 | Nénunoko | `SPECIES_FARFETCHD` |
| 084 | Tryptik | `SPECIES_DODUO` |
| 085 | Carpitaine | `SPECIES_DODRIO` |
| 086 | Turboss | `SPECIES_SEEL` |
| 087 | Kappacap | `SPECIES_DEWGONG` |
| 088 | Appak | `SPECIES_GRIMER` |
| 089 | Camaïeul | `SPECIES_MUK` |
| 090 | Glapie | `SPECIES_SHELLDER` |
| 091 | Chiperpiou | `SPECIES_CLOYSTER` |
| 092 | Rapiaf | `SPECIES_GASTLY` |
| 093 | Tête de lard | `SPECIES_HAUNTER` |
| 094 | Potache | `SPECIES_GENGAR` |
| 095 | Dépotache | `SPECIES_ONIX` |
| 096 | Navétéran | `SPECIES_DROWZEE` |
| 097 | Navigarmateur | `SPECIES_HYPNO` |
| 098 | Sergent Rampant | `SPECIES_KRABBY` |
| 099 | Coach Antonic | `SPECIES_KINGLER` |
| 100 | Usapyon | `SPECIES_VOLTORB` |
| 101 | Emperor | `SPECIES_ELECTRODE` |
| 102 | Castelius III | `SPECIES_EXEGGCUTE` |
| 103 | Castelius II | `SPECIES_EXEGGUTOR` |
| 104 | Castelius I | `SPECIES_CUBONE` |
| 105 | Castelius Max | `SPECIES_MAROWAK` |
| 106 | Pitou | `SPECIES_HITMONLEE` |
| 107 | Choubidou | `SPECIES_HITMONCHAN` |
| 108 | Arbrézo | `SPECIES_LICKITUNG` |
| 109 | Abrézo Social | `SPECIES_KOFFING` |
| 110 | Espreschiot | `SPECIES_WEEZING` |
| 111 | Duc Delafeuille | `SPECIES_RHYHORN` |
| 112 | Feuildechou | `SPECIES_RHYDON` |
| 113 | Sal de bain | `SPECIES_CHANSEY` |
| 114 | XXL de bain | `SPECIES_TANGELA` |
| 115 | Tristos | `SPECIES_KANGASKHAN` |
| 116 | Rocky Badboya | `SPECIES_HORSEA` |
| 117 | Raton Glandeur | `SPECIES_SEADRA` |
| 118 | Vertipiou | `SPECIES_GOLDEEN` |
| 119 | Samoussraï | `SPECIES_SEAKING` |
| 120 | Ronimpec | `SPECIES_STARYU` |
| 121 | Moufpète | `SPECIES_STARMIE` |
| 122 | Gloups | `SPECIES_MR_MIME` |
| 123 | Chip-Chop | `SPECIES_SCYTHER` |
| 124 | Chaipo | `SPECIES_JYNX` |
| 125 | Mémogre | `SPECIES_ELECTABUZZ` |
| 126 | Jojojoyeux | `SPECIES_MAGMAR` |
| 127 | Chauvkipeut | `SPECIES_PINSIR` |
| 128 | Chauv'coucou | `SPECIES_TAUROS` |
| 129 | Pachycoul | `SPECIES_MAGIKARP` |
| 130 | Pachypipi | `SPECIES_GYARADOS` |
| 131 | Loubarbare | `SPECIES_LAPRAS` |
| 132 | Racaïd | `SPECIES_DITTO` |
| 133 | Terminyanator | `SPECIES_EEVEE` |
| 134 | Sabruine | `SPECIES_VAPOREON` |
| 135 | Sabrille | `SPECIES_JOLTEON` |
| 136 | Fourchelangue | `SPECIES_FLAREON` |
| 137 | Felipaix | `SPECIES_PORYGON` |
| 138 | M. Felipaix | `SPECIES_OMANYTE` |
| 139 | Doyagari | `SPECIES_OMASTAR` |
| 140 | Doyen Doyagari | `SPECIES_KABUTO` |
| 141 | Volroulo | `SPECIES_KABUTOPS` |
| 142 | Lulugubre | `SPECIES_AERODACTYL` |
| 143 | Toumou | `SPECIES_SNORLAX` |
| 144 | Lamlam'mou | `SPECIES_ARTICUNO` |
| 145 | Savantard | `SPECIES_ZAPDOS` |
| 146 | Loupépin | `SPECIES_MOLTRES` |
| 147 | Mademoaiselle | `SPECIES_DRATINI` |
| 148 | Maître Nyada | `SPECIES_DRAGONAIR` |
| 149 | Hovernyan | `SPECIES_DRAGONITE` |
| 150 | Enma | `SPECIES_MEWTWO` |
| 151 | Raltesse | `SPECIES_MEW` |

**Statut :** noms validés par le créateur. Ne pas redemander une validation orthographique générale ; signaler uniquement les conflits techniques avérés.
