# Pokémon Rouge Feu × Yo-kai Watch — Synthèse des équipes de boss

> **Version : 1.0 — 16 octobre 2026**  
> **Document de synthèse autonome destiné à préparer le futur script pour Codex.**  
> Source : `REPARTITION_YOKAI_VALIDEE_CODEX.md` v3.15 (registre cumulatif, inchangé).

## 0. Périmètre et règles de lecture

Ce fichier rassemble **toutes les équipes importantes approuvées** (8 champions, 4 membres du Conseil 4, 3 combats de Giovanni — dont son arène —, 2 admins Rocket et Koichi), et rappelle séparément la **composition-cible du rival Champion** et la chronologie imposée de ses huit rencontres.

- **VALIDÉ DÉFINITIVEMENT** = espèces, ordre, niveaux, attaques, talents, objets tenus et sac explicitement retenus **au niveau du game design**, pas preuve de compilation ou d’implémentation dans le jeu.
- **CIBLE FIXÉE, DÉTAILS OUVERTS** = composition et règles narratives du rival à respecter ; niveaux, capacités, talents sélectionnés et objets du Champion restent à définir ou ajuster par Codex selon la progression.
- Le nom de chaque Yo-kai, son **n° fixe** et la **constante `SPECIES_*`** doivent rester liés à `01_POKEDEX_151.csv`. Ne jamais réassigner une constante.
- **Rang*** : reproduit comme information de présentation du registre ; certains rangs étaient explicitement **indicatifs**. Vérifier contre le classement canonique de l’utilisateur, ne pas inférer le rang du BST.
- Les capacités sont des **choix de design validés** pour les boss ; compatibilité d’apprentissage, existence des constantes `MOVE_*`, compétences et comportement Gen III restent à auditer par Codex. Ne jamais changer silencieusement une équipe validée.
- **Aucune modification des cadeaux ni du scénario ici** : une section vide est réservée à la future spécification narrative que nous rédigerons ensemble.

## 1. Vue d’ensemble — adversaires importants

| Catégorie | Dresseur / combat | Nombre | Dernier Yo-kai | Statut |
|---|---|---:|---|---|
| Arène | Pierre — Argenta | 3 | Passpa niv. 12 | **Validé** |
| Arène | Ondine — Azuria | 3 | Sirénité niv. 19 | **Validé** |
| Arène | Major Bob — Carmin-sur-Mer | 4 | Parantonn niv. 23 | **Validé** |
| Arène | Erika — Céladopole | 4 | Misterre niv. 28 | **Validé** |
| Arène | Koga — Parmanie | 5 | Slurpent niv. 40 | **Validé** |
| Arène | Morgane — Safrania | 5 | Savantard niv. 42 | **Validé** |
| Arène | Auguste — Cramois’Île | 5 | Kyubi niv. 45 | **Validé** |
| Arène | Giovanni — Jadielle | 5 | Trytik niv. 49 | **Validé** |
| Conseil 4 | Olga — Conseil 4 n°1 | 5 | Blizzaria niv. 54 | **Validé** |
| Conseil 4 | Aldo — Conseil 4 n°2 | 5 | Turboss niv. 56 | **Validé** |
| Conseil 4 | Agatha — Conseil 4 n°3 | 5 | Potofeu niv. 58 | **Validé** |
| Conseil 4 | Peter — Conseil 4 n°4 | 5 | Octorgone niv. 60 | **Validé** |
| Giovanni hors arène | Repaire de Céladopole | 3 | Crocho niv. 29 | **Validé** |
| Giovanni hors arène | Sylphe SARL | 4 | Crocho niv. 41 | **Validé** |
| Team Rocket | Admin n°1 — Île 5 | 3 | Émousstik niv. 54 | **Validé** |
| Team Rocket | Admin n°2 — Île 5 | 3 | Terminyanator niv. 55 | **Validé** |
| Dojo | Koichi — Safrania | 3 | Coléroptere niv. 37 | **Validé** |
| Ligue | Rival Champion | 6 | Komastar / Appak / Émettor niv. 63 proposé | **Espèces fixées, détails ouverts** |

## 2. Champions d’arène — équipes verrouillées

### Pierre — Argenta — VALIDÉ DÉFINITIVEMENT
**Équipe : 3 Yo-kai.** **Sac du dresseur :** Aucun objet utilisable. **Récompense / suite :** Badge Roche + CT39 Tomberoche.

| Ordre | Yo-kai (n°) | Constante `SPECIES_*` | Niv. | Type | Rang* | Talent | Quatre attaques (ordre fixé) | Objet tenu |
|---:|---|---|---:|---|---|---|---|---|
| 1 | **Felipaix** (137) | `SPECIES_PORYGON` | 8 | Sol | E | Voile Sable (`ABILITY_SAND_VEIL`) | Charge · Jet de Sable · Coud'Boue · — | Aucun |
| 2 | **Bouh** (052) | `SPECIES_MEOWTH` | 10 | Sol | D | Tête de Roc (`ABILITY_ROCK_HEAD`) | Griffe · Jet de Sable · Coud'Boue · — | Aucun |
| 3 | **Passpa** (025) **(dernier)** | `SPECIES_PIKACHU` | 12 | Roche | C | Fermeté (`ABILITY_STURDY`) | Charge · Jet-Pierres · Rugissement · — | Aucun |

**Notes :** Première arène : trois Yo-kai ; quatrième attaque vide pour chacun. Les sets Bouh/Passpa nécessitent audit technique.

### Ondine — Azuria — VALIDÉ DÉFINITIVEMENT
**Équipe : 3 Yo-kai.** **Sac du dresseur :** Aucun objet utilisable. **Récompense / suite :** Badge Cascade + CT03 Vibraqua.

| Ordre | Yo-kai (n°) | Constante `SPECIES_*` | Niv. | Type | Rang* | Talent | Quatre attaques (ordre fixé) | Objet tenu |
|---:|---|---|---:|---|---|---|---|---|
| 1 | **Murhaine** (011) | `SPECIES_METAPOD` | 14 | Eau | E | Glissade (`ABILITY_SWIFT_SWIM`) | Charge · Écume · Groz'Yeux · — | Aucun |
| 2 | **Faux Kappa** (020) | `SPECIES_RATICATE` | 16 | Eau | D | Glissade (`ABILITY_SWIFT_SWIM`) | Griffe · Pistolet à O · Mimi-Queue · — | Aucun |
| 3 | **Sirénité** (067) **(dernier)** | `SPECIES_MACHOKE` | 19 | Eau | B | Cuvette (`ABILITY_RAIN_DISH`) | Vibraqua · Charge · Rugissement · Pistolet à O | Aucun |

**Notes :** Sirénité est dernier. Pas de soin de sac.

### Major Bob — Carmin-sur-Mer — VALIDÉ DÉFINITIVEMENT
**Équipe : 4 Yo-kai.** **Sac du dresseur :** 1 Super Potion + 1 Total Soin. **Récompense / suite :** Badge Foudre + CT34 Onde de Choc.

| Ordre | Yo-kai (n°) | Constante `SPECIES_*` | Niv. | Type | Rang* | Talent | Quatre attaques (ordre fixé) | Objet tenu |
|---:|---|---|---:|---|---|---|---|---|
| 1 | **Antonnerre** (074) | `SPECIES_GEODUDE` | 18 | Électrik | D | Statik (`ABILITY_STATIC`) | Éclair · Charge · Cage-Éclair · Rugissement | Aucun |
| 2 | **Usapion** (100) | `SPECIES_VOLTORB` | 19 | Acier | D | Regard Vif (`ABILITY_KEEN_EYE`) | Griffe Acier · Charge · Armure · Groz'Yeux | Aucun |
| 3 | **Tontonnerre** (073) | `SPECIES_TENTACRUEL` | 21 | Vol | C | Matinal (`ABILITY_EARLY_BIRD`) | Picpic · Vive-Attaque · Groz'Yeux · Charge | Aucun |
| 4 | **Parantonn** (075) **(dernier)** | `SPECIES_GRAVELER` | 23 | Électrik / Vol | B | Paratonnerre (`ABILITY_LIGHTNING_ROD`) | Onde de Choc · Picpic · Charge · Groz'Yeux | Aucun |

**Notes :** Un seul Antonnerre ; Usapion conservé.

### Erika — Céladopole — VALIDÉ DÉFINITIVEMENT
**Équipe : 4 Yo-kai.** **Sac du dresseur :** 1 Hyper Potion + 1 Total Soin. **Récompense / suite :** Badge Prisme + CT19 Giga-Sangsue.

| Ordre | Yo-kai (n°) | Constante `SPECIES_*` | Niv. | Type | Rang* | Talent | Quatre attaques (ordre fixé) | Objet tenu |
|---:|---|---|---:|---|---|---|---|---|
| 1 | **Lacanne** (053) | `SPECIES_PERSIAN` | 23 | Plante | E | Chlorophylle (`ABILITY_CHLOROPHYLL`) | Fouet Lianes · Vol-Vie · Charge · Croissance | Aucun |
| 2 | **Potache** (094) | `SPECIES_GENGAR` | 24 | Plante | E | Chlorophylle (`ABILITY_CHLOROPHYLL`) | Tranch'Herbe · Charge · Rugissement · Vol-Vie | Aucun |
| 3 | **Canastelle** (054) | `SPECIES_PSYDUCK` | 26 | Plante | C | Engrais (`ABILITY_OVERGROW`) | Tranch'Herbe · Para-Spore · Vol-Vie · Croissance | Aucun |
| 4 | **Misterre** (033) **(dernier)** | `SPECIES_NIDORINO` | 28 | Sol / Plante | A | Chlorophylle (`ABILITY_CHLOROPHYLL`) | Tranch'Herbe · Tir de Boue · Croissance · Charge | Aucun |

**Notes :** Potache est à la place de Doyaris. Misterre est dernier.

### Koga — Parmanie — VALIDÉ DÉFINITIVEMENT
**Équipe : 5 Yo-kai.** **Sac du dresseur :** 1 Hyper Potion + 1 Total Soin. **Récompense / suite :** Badge Âme + CT06 Toxik.

| Ordre | Yo-kai (n°) | Constante `SPECIES_*` | Niv. | Type | Rang* | Talent | Quatre attaques (ordre fixé) | Objet tenu |
|---:|---|---|---:|---|---|---|---|---|
| 1 | **Toumou** (143) | `SPECIES_SNORLAX` | 34 | Poison | E | Point Poison (`ABILITY_POISON_POINT`) | Dard-Venin · Purédpois · Armure · Détritus | Aucun |
| 2 | **Lulugubre** (142) | `SPECIES_AERODACTYL` | 35 | Poison | D | Point Poison (`ABILITY_POISON_POINT`) | Détritus · Crochet Venin · Groz'Yeux · Purédpois | Aucun |
| 3 | **Émousstik** (046) | `SPECIES_PARAS` | 36 | Insecte / Poison | B | Essaim (`ABILITY_SWARM`) | Crochet Venin · Vampirisme · Vive-Attaque · Grincement | Aucun |
| 4 | **Épinyan** (003) | `SPECIES_VENUSAUR` | 38 | Feu / Poison | B | Point Poison (`ABILITY_POISON_POINT`) | Flammèche · Dard-Venin · Vive-Attaque · Morsure | Aucun |
| 5 | **Slurpent** (048) **(dernier)** | `SPECIES_VENONAT` | 40 | Poison | B | Suintement (`ABILITY_LIQUID_OOZE`) | Toxik · Détritus · Plaquage · Groz'Yeux | Aucun |

**Notes :** Toumou/Émousstik/Épinyan sont les choix définitifs ; un seul Émousstik. Slurpent dernier.

### Morgane — Safrania — VALIDÉ DÉFINITIVEMENT
**Équipe : 5 Yo-kai.** **Sac du dresseur :** 1 Hyper Potion + 1 Total Soin. **Récompense / suite :** Badge Marais + CT04 Plénitude.

| Ordre | Yo-kai (n°) | Constante `SPECIES_*` | Niv. | Type | Rang* | Talent | Quatre attaques (ordre fixé) | Objet tenu |
|---:|---|---|---:|---|---|---|---|---|
| 1 | **Baku** (049) | `SPECIES_VENOMOTH` | 36 | Psy | D | Attention (`ABILITY_INNER_FOCUS`) | Choc Mental · Écras'Face · Entrave · Groz'Yeux | Aucun |
| 2 | **Ed Mémoire** (056) | `SPECIES_MANKEY` | 37 | Psy | B | Synchro (`ABILITY_SYNCHRONIZE`) | Rafale Psy · Choc Mental · Entrave · Coup d'Boule | Aucun |
| 3 | **Fourchelang** (136) | `SPECIES_FLAREON` | 38 | Psy | B | Attention (`ABILITY_INNER_FOCUS`) | Rafale Psy · Protection · Coup d'Boule · Méditation | Aucun |
| 4 | **Mognyan** (051) | `SPECIES_DUGTRIO` | 39 | Psy | A | Synchro (`ABILITY_SYNCHRONIZE`) | Rafale Psy · Choc Mental · Entrave · Coup d'Boule | Aucun |
| 5 | **Savantard** (145) **(dernier)** | `SPECIES_ZAPDOS` | 42 | Psy | S | Calque (`ABILITY_TRACE`) | Extrasenseur · Prescience · Entrave · Choc Mental | Aucun |

**Notes :** Mognyan remplace Insomnel. Savantard dernier.

### Auguste — Cramois’Île — VALIDÉ DÉFINITIVEMENT
**Équipe : 5 Yo-kai.** **Sac du dresseur :** 1 Hyper Potion + 1 Total Soin. **Récompense / suite :** Badge Volcan + CT38 Déflagration.

| Ordre | Yo-kai (n°) | Constante `SPECIES_*` | Niv. | Type | Rang* | Talent | Quatre attaques (ordre fixé) | Objet tenu |
|---:|---|---|---:|---|---|---|---|---|
| 1 | **Tête de lard** (093) | `SPECIES_HAUNTER` | 40 | Feu | D | Corps Ardent (`ABILITY_FLAME_BODY`) | Flammèche · Morsure · Hurlement · Brouillard | Aucun |
| 2 | **Sabrille** (135) | `SPECIES_JOLTEON` | 41 | Feu | C | Torche (`ABILITY_FLASH_FIRE`) | Roue de Feu · Feu Follet · Vive-Attaque · Brouillard | Aucun |
| 3 | **Poulpater** (037) | `SPECIES_VULPIX` | 42 | Normal / Feu | B | Ramassage (`ABILITY_PICKUP`) | Flammèche · Coup d’Boule · Griffe · Mimi-Queue | Aucun |
| 4 | **Feulion** (028) | `SPECIES_SANDSLASH` | 43 | Feu | A | Corps Ardent (`ABILITY_FLAME_BODY`) | Lance-Flammes · Morsure · Vive-Attaque · Hurlement | Aucun |
| 5 | **Kyubi** (016) **(dernier)** | `SPECIES_PIDGEY` | 45 | Feu | S | Torche (`ABILITY_FLASH_FIRE`) | Lance-Flammes · Morsure · Vive-Attaque · Groz’Yeux | Aucun |

**Notes :** Cinq Yo-kai seulement ; Jibanyan a été RETIRÉ. Kyubi dernier.

### Giovanni — Jadielle — VALIDÉ DÉFINITIVEMENT
**Équipe : 5 Yo-kai.** **Sac du dresseur :** 1 Hyper Potion + 1 Total Soin. **Récompense / suite :** Badge Terre + CT26 Séisme.

| Ordre | Yo-kai (n°) | Constante `SPECIES_*` | Niv. | Type | Rang* | Talent | Quatre attaques (ordre fixé) | Objet tenu |
|---:|---|---|---:|---|---|---|---|---|
| 1 | **Pachycool** (129) | `SPECIES_MAGIKARP` | 41 | Sol | D | Tête de Roc (`ABILITY_ROCK_HEAD`) | Charge · Tir de Boue · Tomberoche · Armure | Aucun |
| 2 | **M. Felipaix** (138) | `SPECIES_OMANYTE` | 42 | Sol | C | Tête de Roc (`ABILITY_ROCK_HEAD`) | Tir de Boue · Tomberoche · Bélier · Hâte | Aucun |
| 3 | **Crocho** (031) | `SPECIES_NIDOQUEEN` | 44 | Normal | C | Cran (`ABILITY_GUTS`) | Plaquage · Tranche · Tomberoche · Groz'Yeux | Aucun |
| 4 | **Pachypipi** (130) | `SPECIES_GYARADOS` | 45 | Sol | B | Tête de Roc (`ABILITY_ROCK_HEAD`) | Tunnel · Éboulement · Grincement · Charge | Aucun |
| 5 | **Trytik** (084) **(dernier)** | `SPECIES_DODUO` | 49 | Feu / Sol | A | Intimidation (`ABILITY_INTIMIDATE`) | Lance-Flammes · Séisme · Tomberoche · Groz'Yeux | Aucun |

**Notes :** Cinq Yo-kai. Crocho à la place de Racaïd ; Démophage RETIRÉ. Trytik premier dévoilement et dernier.

## 3. Conseil 4 — équipes verrouillées

### Olga — Conseil 4 n°1 — VALIDÉ DÉFINITIVEMENT
**Équipe : 5 Yo-kai.** **Sac du dresseur :** 1 Guérison. **Récompense / suite :** Passage vers Aldo.

| Ordre | Yo-kai (n°) | Constante `SPECIES_*` | Niv. | Type | Rang* | Talent | Quatre attaques (ordre fixé) | Objet tenu |
|---:|---|---|---:|---|---|---|---|---|
| 1 | **Angelik** (026) | `SPECIES_RAICHU` | 50 | Glace | D | Isograisse (`ABILITY_THICK_FAT`) | Vent Glace · Poudreuse · Mur Lumière · Vive-Attaque | Aucun |
| 2 | **Espreschiot** (110) | `SPECIES_WEEZING` | 51 | Normal / Glace | C | Attention (`ABILITY_INNER_FOCUS`) | Laser Glace · Météores · Vent Glace · Mimi-Queue | Aucun |
| 3 | **Sabruine** (134) | `SPECIES_VAPOREON` | 52 | Eau | C | Absorb Eau (`ABILITY_WATER_ABSORB`) | Surf · Tranche · Danse Pluie · Aéropique | Aucun |
| 4 | **Frohuahua** (064) | `SPECIES_KADABRA` | 53 | Glace | B | Isograisse (`ABILITY_THICK_FAT`) | Laser Glace · Psyko · Hâte · Météores | Aucun |
| 5 | **Blizzaria** (027) **(dernier)** | `SPECIES_SANDSHREW` | 54 | Glace | B | Isograisse (`ABILITY_THICK_FAT`) | Laser Glace · Vibraqua · Vent Glace · Protection | Baie Sitrus |

**Notes :** Baie Sitrus exclusivement sur Blizzaria, son dernier Yo-kai.

### Aldo — Conseil 4 n°2 — VALIDÉ DÉFINITIVEMENT
**Équipe : 5 Yo-kai.** **Sac du dresseur :** 1 Guérison. **Récompense / suite :** Passage vers Agatha.

| Ordre | Yo-kai (n°) | Constante `SPECIES_*` | Niv. | Type | Rang* | Talent | Quatre attaques (ordre fixé) | Objet tenu |
|---:|---|---|---:|---|---|---|---|---|
| 1 | **Coach Antonic** (099) | `SPECIES_KINGLER` | 51 | Combat | C | Cran (`ABILITY_GUTS`) | Casse-Brique · Tomberoche · Gonflette · Coup d’Boule | Aucun |
| 2 | **Scatcheur** (080) | `SPECIES_SLOWBRO` | 52 | Insecte | B | Essaim (`ABILITY_SWARM`) | Taillade · Casse-Brique · Vive-Attaque · Hâte | Aucun |
| 3 | **Sabri** (039) | `SPECIES_JIGGLYPUFF` | 53 | Ténèbres / Combat | B | Intimidation (`ABILITY_INTIMIDATE`) | Casse-Brique · Feinte · Tomberoche · Grincement | Aucun |
| 4 | **Rocky Badboya** (116) | `SPECIES_HORSEA` | 54 | Combat | B | Cran (`ABILITY_GUTS`) | Casse-Brique · Vendetta · Tomberoche · Groz’Yeux | Aucun |
| 5 | **Turboss** (086) **(dernier)** | `SPECIES_SEEL` | 56 | Eau / Combat | A (BST 540 ; rang d’origine S à confirmer si pertinent) | Intimidation (`ABILITY_INTIMIDATE`) | Casse-Brique · Surf · Tomberoche · Gonflette | Baie Sitrus |

**Notes :** Baie Sitrus exclusivement sur Turboss, son dernier Yo-kai.

### Agatha — Conseil 4 n°3 — VALIDÉ DÉFINITIVEMENT
**Équipe : 5 Yo-kai.** **Sac du dresseur :** 1 Guérison. **Récompense / suite :** Passage vers Peter.

| Ordre | Yo-kai (n°) | Constante `SPECIES_*` | Niv. | Type | Rang* | Talent | Quatre attaques (ordre fixé) | Objet tenu |
|---:|---|---|---:|---|---|---|---|---|
| 1 | **Brumella** (042) | `SPECIES_GOLBAT` | 53 | Spectre | C | Lévitation (`ABILITY_LEVITATE`) | Ball'Ombre · Onde Folie · Dépit · Feinte | Aucun |
| 2 | **Sorcophage** (070) | `SPECIES_WEEPINBELL` | 54 | Spectre | À confirmer auprès du classement utilisateur | Insomnia (`ABILITY_INSOMNIA`) | Ball'Ombre · Tomberoche · Coup d'Boule · Groz'Yeux | Aucun |
| 3 | **Triptic-tac** (044) | `SPECIES_GLOOM` | 55 | Spectre | B | Insomnia (`ABILITY_INSOMNIA`) | Ball'Ombre · Psyko · Protection · Entrave | Aucun |
| 4 | **Mémogre** (125) | `SPECIES_ELECTABUZZ` | 56 | Spectre | B | Pression (`ABILITY_PRESSURE`) | Ball'Ombre · Coup d'Boule · Grincement · Vive-Attaque | Aucun |
| 5 | **Potofeu** (032) **(dernier)** | `SPECIES_NIDORAN_M` | 58 | Spectre | A | Lévitation (`ABILITY_LEVITATE`) | Ball'Ombre · Psyko · Feu Follet · Coup d'Boule | Baie Sitrus |

**Notes :** Sorcophage remplace Moufpète. Baie Sitrus exclusivement sur Potofeu.

### Peter — Conseil 4 n°4 — VALIDÉ DÉFINITIVEMENT
**Équipe : 5 Yo-kai.** **Sac du dresseur :** 1 Guérison. **Récompense / suite :** Accès au combat du Champion.

| Ordre | Yo-kai (n°) | Constante `SPECIES_*` | Niv. | Type | Rang* | Talent | Quatre attaques (ordre fixé) | Objet tenu |
|---:|---|---|---:|---|---|---|---|---|
| 1 | **Dracounet** (013) | `SPECIES_WEEDLE` | 54 | Dragon | D | Attention (`ABILITY_INNER_FOCUS`) | Dracogriffe · Morsure · Charge · Hâte | Aucun |
| 2 | **Chauvkipeut** (127) | `SPECIES_PINSIR` | 55 | Vol / Ténèbres | B | Regard Vif (`ABILITY_KEEN_EYE`) | Aéropique · Feinte · Mur Lumière · Groz'Yeux | Aucun |
| 3 | **Noctambill** (058) | `SPECIES_GROWLITHE` | 56 | Ténèbres / Vol | A | Intimidation (`ABILITY_INTIMIDATE`) | Mâchouille · Aéropique · Vive-Attaque · Hurlement | Aucun |
| 4 | **Sir Dragon** (014) | `SPECIES_KAKUNA` | 58 | Dragon / Vol | A | Attention (`ABILITY_INNER_FOCUS`) | Dracogriffe · Aéropique · Danse Draco · Tomberoche | Aucun |
| 5 | **Octorgone** (015) **(dernier)** | `SPECIES_BEEDRILL` | 60 | Ténèbres | S | Pression (`ABILITY_PRESSURE`) | Mâchouille · Casse-Brique · Dracogriffe · Ultralaser | Baie Sitrus |

**Notes :** Octorgone de type Ténèbres pur, Baie Sitrus exclusivement sur lui.

## 4. Giovanni — deux autres confrontations

### Giovanni — Repaire Rocket, Céladopole — VALIDÉ DÉFINITIVEMENT
**Équipe : 3 Yo-kai.** **Sac du dresseur :** Aucun objet utilisable. **Récompense / suite :** Scope Sylphe (événement scénaristique).

| Ordre | Yo-kai (n°) | Constante `SPECIES_*` | Niv. | Type | Rang* | Talent | Quatre attaques (ordre fixé) | Objet tenu |
|---:|---|---|---:|---|---|---|---|---|
| 1 | **Felipaix** (137) | `SPECIES_PORYGON` | 24 | Sol | E | Voile Sable | Charge · Tir de Boue · Ampleur · Tomberoche | Aucun |
| 2 | **Pachycool** (129) | `SPECIES_MAGIKARP` | 25 | Sol | D | Tête de Roc | Charge · Jet de Sable · Coud'Boue · Tir de Boue | Aucun |
| 3 | **Crocho** (031) **(dernier)** | `SPECIES_NIDOQUEEN` | 29 | Normal | C | Cran | Plaquage · Griffe · Groz'Yeux · Morsure | Aucun |

**Notes :** Felipaix → M. Felipaix ensuite ; Pachycool → Pachypipi ensuite ; Crocho est le partenaire récurrent. Ne pas altérer le script du Scope Sylphe.

### Giovanni — Sylphe SARL, Safrania — VALIDÉ DÉFINITIVEMENT
**Équipe : 4 Yo-kai.** **Sac du dresseur :** Aucun objet utilisable. **Récompense / suite :** Master Ball remise par le président de la Sylphe après la victoire.

| Ordre | Yo-kai (n°) | Constante `SPECIES_*` | Niv. | Type | Rang* | Talent | Quatre attaques (ordre fixé) | Objet tenu |
|---:|---|---|---:|---|---|---|---|---|
| 1 | **Bouh** (052) | `SPECIES_MEOWTH` | 35 | Sol | D | Voile Sable | Griffe · Jet de Sable · Coud'Boue · Tir de Boue | Aucun |
| 2 | **M. Felipaix** (138) | `SPECIES_OMANYTE` | 37 | Sol | C | Tête de Roc | Tir de Boue · Tomberoche · Tunnel · Bélier | Aucun |
| 3 | **Pachypipi** (130) | `SPECIES_GYARADOS` | 37 | Sol | B | Tête de Roc | Bélier · Tunnel · Tomberoche · Grincement | Aucun |
| 4 | **Crocho** (031) **(dernier)** | `SPECIES_NIDOQUEEN` | 41 | Normal | C | Cran | Plaquage · Tranche · Tomberoche · Groz'Yeux | Aucun |

**Notes :** Pachypipi est issu du Pachycool du repaire. Le Pachycool présent plus tard à Jadielle est un second individu. Bouh n’est présent que dans ce combat ; Trytik est réservé à l’arène.

## 5. Deux admins Rocket — Entrepôt de l’Île 5

### Admin Rocket n°1 — premier cadre — VALIDÉ DÉFINITIVEMENT
**Équipe : 3 Yo-kai.** **Sac du dresseur :** Aucun objet utilisable. **Récompense / suite :** Progrès dans les dalles de l’entrepôt ; argent indicatif 1 728 ₽.

| Ordre | Yo-kai (n°) | Constante `SPECIES_*` | Niv. | Type | Rang* | Talent | Quatre attaques (ordre fixé) | Objet tenu |
|---:|---|---|---:|---|---|---|---|---|
| 1 | **Sal de bain** (113) | `SPECIES_CHANSEY` | 52 | Ténèbres | D | Insomnia | Feinte · Provoc · Grincement · Onde Folie | Aucun |
| 2 | **Lamlam'mou** (144) | `SPECIES_ARTICUNO` | 53 | Normal | C | Immunité | Plaquage · Vive-Attaque · Danse-Lames · Damoclès | Aucun |
| 3 | **Émousstik** (046) **(dernier)** | `SPECIES_PARAS` | 54 | Insecte / Poison | B | Essaim | Crochet Venin · Vampirisme · Vive-Attaque · Grincement | Aucun |

**Notes :** Sal de bain remplace l’ancienne proposition Lulugubre, et n’est pas une espèce à distribuer systématiquement aux sbires.

### Admin Rocket n°2 — second cadre — VALIDÉ DÉFINITIVEMENT
**Équipe : 3 Yo-kai.** **Sac du dresseur :** Aucun objet utilisable. **Récompense / suite :** Fin de la branche Rocket Sevii ; argent indicatif 1 760 ₽.

| Ordre | Yo-kai (n°) | Constante `SPECIES_*` | Niv. | Type | Rang* | Talent | Quatre attaques (ordre fixé) | Objet tenu |
|---:|---|---|---:|---|---|---|---|---|
| 1 | **Racaïd** (132) | `SPECIES_DITTO` | 53 | Ténèbres | B | Intimidation | Mâchouille · Gonflette · Plaquage · Éboulement | Aucun |
| 2 | **Humainequin** (047) | `SPECIES_PARASECT` | 54 | Normal | B | Calque | Plaquage · Tranche · Casse-Brique · Grincement | Aucun |
| 3 | **Terminyanator** (133) **(dernier)** | `SPECIES_EEVEE` | 55 | Acier / Ténèbres | A | Armurbaston | Griffe Acier · Casse-Brique · Mâchouille · Grincement | Aucun |

**Notes :** Humainequin remplace l’ancienne proposition Sabrille. Le Saphir lié à Gédéon est un événement distinct ; ne pas réécrire les scripts.

## 6. Maître du Dojo de Safrania

### Koichi — Maître du Dojo — VALIDÉ DÉFINITIVEMENT
**Équipe : 3 Yo-kai.** **Sac du dresseur :** Aucun objet utilisable. **Récompense / suite :** Deux cadeaux identifiés ci-dessous ; aucun badge ni CT ; argent 888 ₽ indicatif.

| Ordre | Yo-kai (n°) | Constante `SPECIES_*` | Niv. | Type | Rang* | Talent | Quatre attaques (ordre fixé) | Objet tenu |
|---:|---|---|---:|---|---|---|---|---|
| 1 | **Coach Antonic** (099) | `SPECIES_KINGLER` | 35 | Combat | C | Cran | Casse-Brique · Gonflette · Coup d'Boule · Tomberoche | Aucun |
| 2 | **Scatcheur** (080) | `SPECIES_SLOWBRO` | 37 | Insecte | B | Essaim | Taillade · Casse-Brique · Vive-Attaque · Hâte | Ceinture Noire |
| 3 | **Coléroptere** (078) **(dernier)** | `SPECIES_RAPIDASH` | 37 | Insecte | B | Essaim | Casse-Brique · Taillade · Tomberoche · Puissance | Ceinture Noire |

**Notes :** Scatcheur et Coléroptere portent chacun une Ceinture Noire. Les autres karatékas du Dojo ne sont pas inclus dans cette équipe verrouillée.

**Récompenses déjà décidées (sans script supplémentaire ici)** : Scatcheur n°080 (`SPECIES_SLOWBRO`) **niveau 25** et Coléroptere n°078 (`SPECIES_RAPIDASH`) **niveau 25**, sans objet tenu. Le joueur doit pouvoir recevoir **les deux dans une même sauvegarde** ; les modalités exactes seront décrites plus tard dans le script de scénario. Ne pas implémenter de nouveau mécanisme de cadeau à partir de cette seule synthèse.

## 7. Rival — Champion de la Ligue (composition cible fixée, détails ouverts)

**Attention : l’ancienne proposition Rapiaf / Mognyan / Rhinolimit / Feulion / Carpitaine est OBSOLÈTE et ne doit pas être utilisée.** Le rival a **six Yo-kai exactement**, dont **les cinq partenaires fixes ci-dessous**, plus son starter final dans la sixième position. Les **niveaux suggérés sont indicatifs**, et **aucun moveset/objet final n’a été validé** pour cette nouvelle composition.

| Ordre | Yo-kai final (n°) | Constante technique | Type | BST | Niveau indicatif (à ajuster) | Rôle / contrainte |
|---:|---|---|---|---:|---:|---|
| 1 | **Robonyan 28 (019)** | `SPECIES_RATTATA` | Acier | 550 | 58 | Évolution de Robonyan F ; **28 fait partie du nom de l’espèce** |
| 2 | **Glapie (090)** | `SPECIES_SHELLDER` | Vol / Spectre | 530 | 59 | Partenaire déjà vu à la Tour Pokémon |
| 3 | **Shogunyan (004)** | `SPECIES_CHARMANDER` | Feu / Acier | 550 | 60 | Première apparition de cette évolution UNIQUEMENT au Champion |
| 4 | **Camaueil (089)** | `SPECIES_MUK` | Plante | 530 | 60 | Première apparition ABSOLUE chez le rival, UNIQUEMENT au Champion |
| 5 | **Navigarmateur (097)** | `SPECIES_HYPNO` | Acier | 530 | 61 | Première apparition de cette évolution UNIQUEMENT au Champion |
| 6 | **Komastar 007 / Appak 088 / Émettor 030** | Selon la variante ci-dessous | Feu/Électrik, Eau ou Électrik | 560 / 520 / 520 | 63 | **Dernier Yo-kai, déterminé par le starter du joueur** |

### Choix du starter du rival (règle fixe)

| Starter choisi par le joueur | Starter du rival au laboratoire | Évolutions pendant l’aventure | Dernier Yo-kai du Champion | Constante technique |
|---|---|---|---|---|
| **Padrezo** | Komasan | Komasan → Komaous → Komastar (Pierre Foudre) | **Komastar n°007** | `SPECIES_SQUIRTLE` |
| **Komasan** | Kappacap | Kappacap → Appak (niveau 36) | **Appak n°088** | `SPECIES_GRIMER` |
| **Kappacap** | Padrezo | Padrezo → Émettor (niveau 34) | **Émettor n°030** | `SPECIES_NIDORINA` |

**Sac et objets tenus du rival Champion : à définir**, comme ses quatre attaques, talents de combat et niveaux exacts (les niveaux 58, 59, 60, 60, 61, 63 sont des bases de travail et non des validations). Conserver l’entrée au Panthéon et les mécaniques de fin de Ligue existantes ; aucune nouvelle récompense scénaristique n’est fixée par ce fichier.

### Chronologie obligatoire des huit combats du rival (équipes à composer techniquement)

| N° | Rencontre | Membres et continuité imposés | Statut détaillé |
|---:|---|---|---|
| 1 | Laboratoire du Professeur Chen | Starter seul, niv. 5 | Composition fixée |
| 2 | Route 22 (début, facultatif) | Starter + **Cigalopin**. Aucun Chiperpiou/Rapiaf. | Niveaux/moves libres sous la courbe |
| 3 | Azuria, Pont Pépite | Starter + **Cigalopin non évolué** + **Jibanyan**. | Niveaux/moves libres |
| 4 | L’Océane | Starter + **Cigallard** (évolution de Cigalopin au niv.18) + **Jibanyan** + **Navétéran**. **Dernière apparition de Cigallard.** | Niveaux/moves libres |
| 5 | Tour Pokémon | Starter + **Jibanyan** + **Navétéran** + **Glapie**. Cigallard a disparu, sans explication. | Niveaux/moves libres |
| 6 | Sylphe SARL | Starter + **Jibanyan non évolué** + **Navétéran non évolué** + **Glapie** + **Robonyan**. | Niveaux/moves libres ; Robonyan F doit arriver plus tard |
| 7 | Route 22 avant la Ligue | **Exactement cinq** : Robonyan F + Glapie + Jibanyan **non évolué** + Navétéran **non évolué** + starter évolué. **Jamais Camaueil**. | Niveaux/moves à composer |
| 8 | Plateau Indigo, Champion | **Exactement six** : Robonyan 28 + Glapie + Shogunyan + Camaueil + Navigarmateur + starter final (dernier). | Espèces fixées ; détails techniques ouverts |

**Règles narratives impératives :** Cigalopin → Cigallard est le **SEUL compagnon que le rival recrute puis perd** ; ne pas ajouter Rapiaf/Chiperpiou ni de partenaire jetable. La disparition de Cigallard doit rester **mystérieuse et inexpliquée**, sans écrire qu’il est mort. Jibanyan et Navétéran sont maintenus sans évoluer tout au long des duels pré-Ligue, même au-dessus de leur niveau d’évolution habituel. Ils évoluent seulement avant le Champion. Camaueil n’apparaît jamais avant le Champion. Un membre qui rejoint l’équipe (hors Cigallard) doit rester présent dans les affrontements ultérieurs, dans sa forme ou son évolution.

## 8. Autres dresseurs — cadrage rapide pour la suite

**Dresseurs ordinaires :** Codex sélectionnera librement les Yo-kai en fonction du type de dresseur, des lieux, du stade de progression, des classes et des niveaux habituels de Rouge Feu. Ne pas modifier les boss verrouillés ci-dessus et préserver scripts, flags, combats doubles et revanches. Les évolutions dans les équipes des PNJ sont permises ; cela ne change pas les rencontres sauvages.

**Palette prioritaire des sbires Rocket :** Lulugubre ; Toumou → Lamlam’mou ; Raltesse ; Loubarbare → Racaïd ; Bouh ; Nihilistik → Émousstik. Les deux admins ont leurs équipes particulières et ne doivent pas être traités comme des sbires ordinaires. Varier les combinaisons par lieu (repaire, Sylphe, Sevii), éviter les clones.

## 9. Contrôles techniques obligatoires avant tout codage

1. Lire `01_POKEDEX_151.csv` pour les 151 noms et constantes, `02_STATS_TYPES_TALENTS.csv` pour types/talents, `03_EVOLUTIONS.xlsx` et le code source des évolutions, ainsi que `04_ATTAQUES_NIVEAU.csv` et les vraies tables du dépôt pour les attaques. Ne jamais utiliser l’ancien Pokémon comme substitut textuel de l’espèce Yo-kai.
2. Vérifier toutes les constantes d’attaques (`MOVE_*`), talents (`ABILITY_*`), objets (`ITEM_*`) et l’existence des movesets personnalisés. Certaines espèces de numéros 001–130 n’ont pas de learnset exhaustif dans les documents fournis ; une décision validée de design ne prouve pas que la capacité est intégrée.
3. Respecter les catégories physique/spécial de la Génération III (définies **par type**) lors des vérifications d’équilibrage.
4. Ne **jamais corriger silencieusement** une attaque, un niveau, un talent, un objet ou une espèce déjà validés : signaler toute impossibilité et proposer une adaptation à approuver.
5. Aucun changement de script, rencontre sauvage, cadeau, fossile, événement de scénario ou boutique n’est autorisé par la création de cette synthèse. Ne pas présenter les équipes comme intégrées ou testées tant qu’une compilation et des essais n’ont pas eu lieu.

## 10. Réservé à notre futur script de scénario — À COMPLÉTER ENSEMBLE

**Statut : volontairement vide.** Les idées de cadeaux supplémentaires, déclencheurs d’événements, dialogues, conditions d’obtention et séquences scénaristiques feront l’objet de décisions ultérieures de l’utilisateur. Aucune mécanique nouvelle n’est déduite de ce document.

<!-- BLOC À COMPLÉTER PLUS TARD : description événement, localisation, préconditions/flags, dialogues, conséquences, récompenses, pseudo-code ou instructions d’implémentation Codex. -->

---

*Fin de la synthèse. Le document cumulatif original v3.15 conserve l’historique des décisions et reste disponible en cas de doute. La présente synthèse privilégie uniquement les choix courants, et exclut les compositions annulées.*
