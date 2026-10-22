# Huit arènes — direction artistique et level design délégué

## Règle VALIDÉE : type dominant, pas monotype

Les huit Champions emploient majoritairement des Yo-kai de leur spécialité. **Une ou deux exceptions hors type sont autorisées** lorsque le lore l'exige. Les huit attributions de types ci-dessous ont été élaborées pendant la carte blanche accordée par le créateur et représentent une **direction de référence**, à confirmer lors du jalon d'équilibrage.

Les **espèces/niveaux/objets/attaques proposés** figurent dans `04_CHAMPIONS_ET_EQUIPES.csv` (niveaux encore vides). Ne pas écraser à l'aveugle `data/yokai/equipes_boss_validees.json` : ce fichier contient les anciennes équipes de Pierre/Ondine/etc., travaillées puis validées pour une version antérieure du jeu. Il faut créer une migration explicite depuis cette ancienne version.

## Liberté VALIDÉE pour Codex

Codex doit imaginer **son propre level design** : plans, détours, salles, puzzles, tilesets et mise en scène. Les exemples qui suivent sont des **intentions thématiques** plutôt que des ordres de reproduire un puzzle. Chaque arène doit respecter la personnalité du Champion, la progression de difficulté, les contraintes GBA et les sorties sans pièges. Une capture de prototype et un plan de connections seront présentés au créateur pour validation avant verrouillage.

## Tableau de direction

| Nº | Champion selon joueur | Ville envisagée | Type dominant proposé | Direction visuelle | Exception notable |
|---:|---|---|---|---|---|
| 1 | Wyatt Cardamom | Argenta | Roche | Musée, pierres, fossiles, exploration | Aucune exigée |
| 2 | Katie si Nathan / Nathan si Katie | Azuria | Feu | Lanternes, foyer, énergie des Yo-kai | Whisper, Spectre |
| 3 | Bérénice Bélier | Carmin-sur-Mer | Psy | Laboratoire, Portes Mystères, dimensions | Selon thème de quête |
| 4 | Ariane Célestin | Safrania | Acier | Station spatiale, téléporteurs, machines | Mognyan, Psy |
| 5 | Inspecteur Giraud | Parmanie | Combat | Commissariat, indices, entraînement | Pitou, Normal |
| 6 | Alyzon Bie | Lavanville/Tour Pokémon | Spectre | Zombie Night et Tour Pokémon | Moufpète, Poison |
| 7 | Nathaniel jeune / Michael jeune | Cramois'Île passée | Eau | Arène ancienne, eaux de l'île, souvenirs | Hovernyan Vol, Potofeu Spectre |
| 8 | Don Morleone | Jadielle | Ténèbres | Repaire mafieux, pièges, surveillance | Gorgouille Combat |

### Trophée 1 — Wyatt

Une entrée naturelle dans la course. Ne pas nécessairement conserver le puzzle original de Pierre. Wyatt aime les reliques : fondations du musée et exploration, avec un itinéraire clair pour nouveaux joueurs. Réemployer `data/maps/PewterCity_Gym` et les éventuels tilesets existants si approprié ; créer uniquement les différences nécessaires. **Équipe provisoire :** Nanpart, Passpa.

### Trophée 2 — Nathan/Katie

Décor atypique pour Azuria, volontairement centré sur leur caractère et **Jibanyan**. Ne pas confondre la piscine de l'arène d'Ondine avec une contrainte narrative : Codex peut l'aménager. Un chemin lisible et quelques mécanismes de Feu symbolique sont bienvenus. **Équipe provisoire :** Feulion, Whisper, Jibanyan.

### Trophée 3 — Bérénice

**Les Portes Mystères sont la caractéristique principale**, et non une installation de production électrique. Les joueurs doivent sentir qu'ils changent de dimension. Les portails nécessitent des destinations/retours vérifiés ; ne jamais faire apparaître un état de quête irréversible si un joueur quitte la map. **Équipe provisoire :** Baku, Ed Mémoire, Insomnel.

### Trophée 4 — Ariane

Les technologies spatiales doivent être évidentes ; préserver **Usapion** comme signature. Téléporteurs déjà supportés par le moteur, mais liberté sur l'ordre et le nombre de salles. Ancienne map `SaffronCity_Gym` ; ancien caméo Route 25 à résoudre. **Équipe provisoire :** Navétéran, Robonyan, Mognyan, Usapion.

### Trophée 5 — Giraud

L'expérience idéale est une **enquête jouable** : découvrir un indice, croiser plusieurs témoignages et accéder au Champion. Pas de violence réaliste ; le défi se traduit par des PNJ, scripts et combats Yo-kai. **Équipe provisoire :** Rocky Badboya, Pitou, Samoussrai, Coach Antonic.

### Trophée 6 — Alyzon

Le « donjon » est d'abord l'événement **Zombie Night** dans la ville existante, puis l'accès à la Tour Pokémon. Le **sommet de la Tour** comme salle de combat a été bien accueilli mais n'est pas explicitement figé ; le prévoir comme hypothèse de conception. **Pas de nouvelle géographie à Lavanville**. **Équipe provisoire :** Brumella, Moufpète, Sorcophage, Tristos.

### Trophée 7 — Nathaniel/Michael

Le Champion vit dans l'époque passée de Cramois'Île. La **géographie de l'île reste celle de Rouge Feu** ; Codex peut faire une version intérieure rétro de l'arène pour son puzzle, mais l'extérieur doit rester reconnaissable. **Hovernyan est signature et exception de type**. **Équipe provisoire :** Tukappa, Sirénité, Carpitaine, Potofeu, Hovernyan.

### Trophée 8 — Don Morleone

Décor de quartier général. **Il est le vrai huitième Champion**, pas simplement un combat Rocket scripté au mauvais endroit. Après victoire il remet le dernier trophée à contrecœur, déclare avoir huit trophées lui aussi et part vers le Temple. **Équipe provisoire :** Racaïd, Bonneto, Sabri, Emperor, Gorgouille, Loubarbare.

## Ancienne arène Céladopole — problème à résoudre

Rouge Feu possède huit villes avec arène à l'origine, dont Céladopole et PAS Lavanville. Le déplacement du sixième trophée au scénario de Lavanville entraîne une **ancienne arène surnuméraire**. **PROPOSÉ :** reconvertir l'arène de Céladopole en serre/lieu optionnel sans trophée, et utiliser le Casino et son repaire pour une séquence Mafiamille et Agent X. Ne PAS créer de neuvième trophée ou supprimer Céladopole.

## Recette avant validation des cartes

Une arène est « acceptée » uniquement si : entrée et sortie fonctionnent, le puzzle est réinitialisable / reprenable, les dresseurs ne bloquent pas les tiles de transition, l'équipe de Champion est conforme au fichier approuvé, le trophée est compté exactement une fois, la suite de la campagne est débloquée, et les deux choix de protagoniste sont testés pour les arènes variables.
