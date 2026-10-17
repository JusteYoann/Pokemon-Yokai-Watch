# Pokémon Rouge Feu × Yo-kai Watch — Cahier des charges Codex pour les caméos

**Version : 1.0 — 16 octobre 2026**  
**Statut : spécification des caméos, à intégrer après audit du dépôt**  
**Référence graphique : archive fournie séparément sous le nom logique `Référence_CAMÉOS_YOKAI_WATCH` (l’archive actuellement jointe s’appelle `CAMEO.rar`).**

**Priorité :** conserver sans changement les équipes de boss déjà validées, le Pokédex 151, la répartition des rencontres, les évolutions et les événements originaux, sauf modification expressément demandée dans ce document. Les noms de Yo-kai doivent être résolus à partir de la table du projet, jamais convertis naïvement à partir des noms des Pokémon d’origine.

Ce document décrit l'intégration de nouveaux dresseurs caméos inspirés de l'univers **Yo-kai Watch** dans le projet **Pokémon Rouge Feu × Yo-kai Watch**.

Le but est d'ajouter plusieurs PNJ spéciaux affrontables, avec sprites inédits, équipes personnalisées, éventuelles revanches postgame et quelques récompenses uniques.

Ce document est destiné à **Codex**.

---

## 1. Règles générales

### 1.1 Nature des combats
- Tous les combats caméos sont **optionnels**.
- Le joueur doit **parler au personnage**, puis une boîte de dialogue doit demander explicitement s'il veut combattre.
- Le combat ne commence que si le joueur sélectionne **« Oui »**.
- Si le joueur répond **« Non »**, le PNJ reste sur place et pourra être réinterrogé plus tard.

### 1.2 Dialogues
- Les dialogues peuvent être **improvisés par Codex**, mais doivent rester **sobres, naturels et dans l'esprit d'un caméo Pokémon**.
- Il ne faut **pas écrire de dialogues très chargés en lore Yo-kai Watch**, ni faire de références trop précises à des événements particuliers de la série.
- Le ton visé est proche d'un caméo Pokémon classique (par exemple un personnage spécial croisé dans une autre version).
- Chaque PNJ doit au minimum avoir :
  - une phrase avant combat,
  - une phrase après défaite,
  - éventuellement une petite phrase après le combat si on lui reparle.

### 1.3 Sprites originaux
- Les nouveaux caméos doivent avoir leurs **propres sprites originaux**, et non de simples recolors.
- Codex doit analyser les fichiers graphiques existants de **Pokémon Rouge Feu** pour comprendre :
  - les dimensions,
  - les proportions,
  - le niveau de détail,
  - le contour,
  - l'ombrage,
  - la palette,
  - les poses,
  - et la logique de construction des sprites de dresseurs.
- À partir de cette analyse, Codex doit créer pour chaque nouveau personnage :
  1. un **sprite de combat** inédit,
  2. un **sprite overworld** cohérent,
  3. les directions, poses, palettes et images d’animation nécessaires aux PNJ sur la carte, suivant ce que le moteur utilise réellement.
- Examiner la structure des sprites source du projet (graphismes de combat des dresseurs, sprites d’overworld, palettes, dimensions, compression, métadonnées et tables d’index). **Ne pas présumer que toutes les ressources font 64×64 ni inventer leurs formats.**
- Les sprites doivent être dessinés à une résolution native du jeu, avec pixels nets, sans flou ou anticrénelage ; conserver une silhouette lisible et une pose inspirée des références officielles fournies.
- Ne jamais réutiliser un sprite de dresseur existant avec une simple recoloration. Ne pas substituer un sprite aléatoire ou générique si un visuel demandé manque : signaler la référence absente.
- Pour les versions alternatives Nathan/Katie et Nathaniel/Michael, **produire des sprites séparés**, conditionnés par la présentation du joueur.
- Les deux employés de Domniscian et les trois Mafiamille doivent également recevoir leurs sprites spécifiques de combat et d’overworld.
- Vérifier les limites et le format des palettes, les dimensions réelles, les encodages/transparences, les registres d’assets et les affichages en jeu après import. Fournir des aperçus PNG exportés à taille lisible dans le compte rendu. Si l’environnement ne permet pas de dessiner proprement les assets, **ne pas prétendre qu’ils ont été créés** : indiquer le blocage et les images nécessaires.
- Les sprites doivent donner l'impression que ces personnages **auraient toujours pu exister dans Rouge Feu**.
- Les sprites doivent être créés en s'appuyant visuellement sur l'archive de référence fournie :
  - **`Référence_CAMÉOS_YOKAI_WATCH`** (voir aussi l’archive jointe **`CAMEO.rar`**, contenant le dossier `CAMEO/` : il s’agit d’une archive RAR et non d’un fichier ZIP).
- Cette archive sert de référence visuelle pour les personnages et leur apparence générale ; ne pas en déduire des équipes ou des événements additionnels.
- Les noms des images peuvent différer légèrement des noms retenus (par exemple `Dominiscian.webp` pour **Domniscian**). Identifier les personnages par leur visuel avant de les attribuer ; les images supplémentaires, non réclamées dans ce cahier des charges, ne créent pas de nouveaux caméos.

### 1.4 Réaffrontements / postgame
- Certains caméos sont affrontables pendant l'aventure, puis **réaffrontables après la fin du jeu** avec une autre équipe.
- D'autres sont **réservés exclusivement au postgame**.
- Il faut respecter exactement les conditions précisées plus bas.

### 1.5 Récompenses
- Les récompenses spéciales doivent être données après victoire, selon les règles précisées pour chaque personnage.
- Si une récompense nécessite un script complémentaire non encore implémenté, Codex doit le signaler clairement.
- Chaque récompense spéciale est **remise une seule fois par sauvegarde** : une revanche ne doit pas dupliquer les pierres, pépites ou autres cadeaux.
- S’assurer que l’inventaire peut recevoir la récompense ; en cas de sac plein, permettre de réessayer le dialogue plutôt que de perdre définitivement l’objet.
- Vérifier les méthodes d’évolution existantes avant de choisir une constante d’objet : les expressions « pierre d’évolution de X » désignent un résultat voulu, **pas forcément un nouvel objet à créer**. Ne jamais inventer une constante d’objet sans contrôle des fichiers.

---

## 2. Caméos rencontrés pendant l'aventure

Ces caméos sont rencontrables avant la fin du jeu. Ils sont également réaffrontables après la Ligue avec une équipe différente. **Si le joueur les rencontre pour la première fois après la Ligue, utiliser leur équipe postgame, sans rendre obligatoire un combat préalable contre l’équipe aventure.** Le niveau exact des membres de chaque équipe postgame peut être choisi par Codex à l’intérieur de la plage proposée, en respectant l’ordre des espèces transmis.

---

## 2.1 Ariane Célestin

### Statut
- Caméo affrontable pendant l'aventure.
- Réaffrontable après la fin du jeu.
- Combat optionnel avec menu Oui / Non.

### Placement conseillé
- Très tôt dans l'aventure.
- Emplacement conseillé : **Route 25 / Cap d'Azuria**.
- Ariane doit être le **premier grand caméo spécial** du jeu.

### Équipe pendant l'aventure
- Usapion (signature)
- Feulion
- Savantard

### Niveaux conseillés pendant l'aventure
- Usapion : 17
- Feulion : 18
- Savantard : 20

### Équipe postgame
- Emperor
- Feulion
- Espreschiot
- Émettor
- Savantard

### Niveaux conseillés postgame
- environ 56 à 60

### Récompense
- Donne une **pierre d'évolution de Usapion**.

### Note importante
- Comme Ariane apparaît tôt et possède Savantard, le combat doit rester **optionnel**.

---

## 2.2 Nathan / Katie

### Condition d'apparition
- Si le joueur est **un garçon** : le caméo affiché est **Katie**.
- Si le joueur est **une fille** : le caméo affiché est **Nathan**.
- Cette logique doit être cohérente avec le futur choix du protagoniste (Nathan ou Katie).

### Statut
- Caméo affrontable pendant l'aventure.
- Réaffrontable après la fin du jeu.
- Combat optionnel avec menu Oui / Non.

### Placement conseillé
- Emplacement conseillé : **Céladopole**.

### Équipe pendant l'aventure
- Jibanyan (signature)
- Whisper
- Komasan
- Kappacap
- Baku

### Niveaux conseillés pendant l'aventure
- Whisper : 28
- Komasan : 28
- Jibanyan : 29
- Kappacap : 29
- Baku : 30

### Équipe postgame
- Shogunyan
- Appak
- Jojojoyeux
- Whisper
- Komaous
- Bakuku

### Niveaux conseillés postgame
- environ 58 à 63

### Récompense
- Donne une **pierre d'évolution de Jibanyan**.

---

## 2.3 Nathaniel / Michael

### Condition d'apparition
- Si le joueur est **un garçon** : le caméo affiché est **Nathaniel**.
- Si le joueur est **une fille** : le caméo affiché est **Michael**.

### Statut
- Caméo affrontable pendant l'aventure.
- Réaffrontable après la fin du jeu.
- Combat optionnel avec menu Oui / Non.

### Placement conseillé
- Emplacement conseillé : **Parmanie / zone liée au Parc Safari**.

### Équipe pendant l'aventure
- Hovernyan (signature)
- Bouh
- Faux Kappa
- Métaurolog
- Siréné

### Niveaux conseillés pendant l'aventure
- Bouh : 33
- Faux Kappa : 33
- Métaurolog : 34
- Hovernyan : 34
- Siréné : 35

### Équipe postgame
- Hovernyan
- Maître Nyada
- Tauracle
- Sirénité
- Faux Kappa
- Démophage

### Niveaux conseillés postgame
- environ 59 à 64

### Récompense
- Donne une **autre pierre d'évolution**.
- Choix retenu : **pierre d'évolution pour Siréné**.

---

## 2.4 Wyatt

### Statut
- Dernier caméo rencontrable pendant l'aventure.
- Réaffrontable après la fin du jeu.
- Combat optionnel avec menu Oui / Non.

### Placement conseillé
- Emplacement conseillé : **Cramois'Île / zone proche du bord de mer ou du quai**.

### Équipe pendant l'aventure
- Tukappa (signature)
- Raton Glandeur
- Moufpète
- Loupépin
- Tête de lard
- Navétéran

### Niveaux conseillés pendant l'aventure
- Tukappa : 42
- Raton Glandeur : 42
- Moufpète : 43
- Loupépin : 44
- Tête de lard : 44
- Navétéran : 45

### Équipe postgame
- Tukappa
- Mognyan
- Rocky Badboya
- Navigarmateur
- Terminyanator
- Loupépin

### Niveaux conseillés postgame
- environ 61 à 66

### Récompense
- Donne une **pierre d'évolution pour Faux Kappa**.

---

## 3. Caméos réservés au postgame

Ces caméos ne sont affrontables qu'après la fin du jeu.

---

## 3.1 Domniscian

### Statut
- Caméo **réservé au postgame**.
- Combat optionnel avec menu Oui / Non.
- Il est accompagné de **2 employés**.
- Le joueur doit d'abord vaincre les employés, puis peut combattre Domniscian.

### Placement conseillé
- Emplacement conseillé : **Sylphe SARL**, dans un bâtiment / bureau / étage postgame approprié.

### Employé rouge
Chaque employé possède **2 Yo-kai**.

Équipe retenue :
- Jibanyan
- Feulion

### Employé bleu
Équipe retenue :
- Komasan
- Robonyan

### Niveaux conseillés des employés
- environ 58 à 60

### Équipe de Domniscian
- Jibanyan
- Komasan
- Usapion
- Whisper
- Robonyan
- Cigalopin

### Niveaux conseillés de Domniscian
- environ 62 à 66

### Récompense
- Donne la **pierre nécessaire à la lignée de Komasan / Komaous / Komastar**.
- Concrètement : l'objet d'évolution nécessaire pour atteindre **Komastar**.

### Note de design
- Cette équipe composée de formes mignonnes / mascottes est volontaire.
- Il ne faut pas remplacer ces sous-évolutions par leurs formes finales juste pour « renforcer » son équipe.

---

## 3.2 Don Morleone

### Statut
- Caméo **réservé au postgame**.
- Combat optionnel avec menu Oui / Non.
- Il est accompagné de **3 Mafiamille**.
- Le joueur affronte les Mafiamille avant Don Morleone.

### Placement conseillé
- Emplacement conseillé : **une pièce fermée / salle spéciale de l'Entrepôt Rocket de l'Île 5** ou tout autre endroit au fort thème mafieux.

### Composition des 3 Mafiamille
- Un Mafiamille possède **1 Yo-kai**.
- Un Mafiamille possède **2 Yo-kai**.
- Un Mafiamille possède **3 Yo-kai**.

### Équipes retenues
#### Mafiamille 1 (1 Yo-kai)
- Bouh

#### Mafiamille 2 (2 Yo-kai)
- Bonneto
- Castelius II

#### Mafiamille 3 (3 Yo-kai)
- Couchtar
- Volroulo
- Émousstik

### Niveaux conseillés des Mafiamille
- environ 60 à 65

### Équipe de Don Morleone
- Mademoaiselle
- Sorcophage
- Doyen Doyaris
- Fourchelang
- Tristos
- Turboss

### Niveaux conseillés de Don Morleone
- environ 66 à 70

### Récompense
- Donne **3 Pépites**.

---

## 3.3 Seigneur Enma

### Statut
- Caméo **réservé au postgame**.
- Dernier grand caméo / super-boss.
- Combat optionnel avec menu Oui / Non.

### Placement conseillé
- Emplacement conseillé : **sommet le plus élevé d'une zone des îles postgame**.
- Proposition retenue : **sommet ultime du Mont Braise**.

### Équipe de Seigneur Enma
- Enma (signature)
- Superfouetar
- Démophage
- Castelius Max
- Camaueil
- Gorgouille

### Niveaux conseillés
- environ 70 à 75

### Particularité de script
- Si le joueur bat Seigneur Enma, alors **Enma apparaît dans la Caverne Azurée**.
- Tant que Seigneur Enma n'a pas été battu, **Enma ne doit pas apparaître dans la Caverne Azurée**.
- Le combat contre Seigneur Enma sert donc de **déclencheur scénaristique / script** pour débloquer l'apparition du Yo-kai capturable Enma.

### Récompense
- Pas de récompense supplémentaire obligatoire.
- Le véritable gain est le **déblocage de l'apparition d'Enma** dans la Caverne Azurée.

---

## 4. Points de script importants

### 4.1 Système de menu avant combat
Pour **chaque caméo, chaque employé et chaque Mafiamille** :
- interaction avec le PNJ ; jamais de combat automatique lorsque le joueur franchit une dalle ou entre dans une pièce ;
- texte court de proposition de combat, suivi du choix **Oui / Non** ;
- **Oui** : lancer le combat voulu (équipe aventure, postgame ou groupe selon le flag approprié) ;
- **Non** : fermer le dialogue sans combat, sans bloquer la progression ni consommer une tentative ;
- après victoire : sauvegarder un flag distinct, proposer les dialogues de victoire et les récompenses prévues ;
- après défaite du joueur : pas de récompense, aucune victoire fictive enregistrée ; le défi reste disponible.

Pour un groupe d’employés/Mafiamille, chacun garde son propre choix Oui/Non et son flag de victoire. Le boss devient **proposable** seulement après les victoires contre tous les membres du groupe. Le boss final garde lui aussi le menu Oui/Non.

### 4.2 Réaffrontements postgame
Pour Ariane, Nathan/Katie, Nathaniel/Michael et Wyatt :
- un premier combat existe pendant l'aventure,
- une équipe de revanche existe après la fin du jeu ;
- il faut prévoir des flags/conditions adaptés pour la version postgame, indépendamment des flags des récompenses uniques ;
- les revanches sont demandées volontairement en reparlant au personnage ; ne pas les transformer en rencontres automatiques.
- Ne pas revenir à l’équipe aventure une fois le postgame déverrouillé.

### 4.3 Variantes selon le sexe du joueur
Codex devra vérifier le système utilisé par le projet pour identifier le sexe / personnage du joueur, puis afficher :
- **Nathan ou Katie** selon le cas,
- **Nathaniel ou Michael** selon le cas.

### 4.4 Déblocage d'Enma
- **Avant** la victoire contre Seigneur Enma : la rencontre statique d’**Enma** à la Caverne Azurée est absente/inaccessible.
- **Après** la victoire : rendre cette rencontre visible et accessible à l’endroit déjà prévu par la répartition validée (remplacement de la rencontre Mewtwo).
- Utiliser un flag fiable de **victoire** contre Seigneur Enma ; parler, refuser le duel ou le perdre ne doit jamais débloquer Enma.
- Conserver les conditions de progression normales vers la Caverne Azurée et la logique de capture/rencontre unique. Ne pas permettre d’obtenir plusieurs Enma via ce déblocage.
- Le Seigneur Enma peut néanmoins utiliser un Enma dans son équipe de dresseur : cela n’accorde pas le Yo-kai au joueur.
- Tester le comportement des scripts avec le flag absent puis présent.

---

## 5. Ce que Codex doit faire

**Traiter ce document comme une spécification, pas comme une preuve que les fichiers sont déjà implémentés.** Les lieux et niveaux marqués « conseillés » sont des propositions approuvées comme direction générale, mais Codex doit signaler toute contrainte de map ou d’équilibrage avant d’imposer un déplacement important.

1. Identifier les bons fichiers de scripts, de maps, de dresseurs et de graphismes pour intégrer ces nouveaux caméos.
2. Créer les **sprites originaux** nécessaires en respectant le style de Rouge Feu.
3. Utiliser l'archive **`Référence_CAMÉOS_YOKAI_WATCH`** comme base visuelle des personnages.
4. Intégrer les combats, équipes, niveaux et récompenses décrits ici.
5. Implémenter les conditions Oui / Non avant chaque combat.
6. Gérer les variantes de PNJ selon le sexe du joueur pour Nathan/Katie et Nathaniel/Michael.
7. Gérer les rematches postgame des quatre caméos principaux.
8. Implémenter le déblocage d'Enma après la victoire contre Seigneur Enma.
9. Signaler clairement toute contrainte technique, toute limite du moteur ou toute donnée manquante.

---

## 6. Règle de prudence

- Ne pas inventer de modification lourde du scénario en dehors de ce qui est demandé.
- Ne pas faire de références trop appuyées à des arcs narratifs de Yo-kai Watch.
- Ne pas remplacer les équipes validées par des versions « plus fortes » sans demande explicite.
- Si certaines attaques, palettes, sprites ou scripts demandent un travail complémentaire, le signaler explicitement.


---

## 7. Contrôles techniques et critères d'acceptation

### 7.1 Audit préalable
- Inspecter le dépôt et les ressources de référence avant de modifier les maps.
- Cartographier les tables de dresseurs, les classes, leurs noms, les sprites de combat, les sprites overworld, les scripts d’événements, les conditions de postgame et les nouveaux flags disponibles.
- Retrouver chaque Yo-kai par la table **151 espèces** et vérifier ses constantes `SPECIES_*`, ses talents et ses attaques. Les noms et les accents affichés ne remplacent pas la vérification des identifiants techniques.
- Si une équipe ou un sprite fait référence à une espèce absente, s’arrêter pour ce point et signaler précisément ce qui manque.
- Conserver les équipes de boss et le rival déjà verrouillés par les autres documents ; aucun écrasement des tables déjà validées.

### 7.2 Références de l’archive
L’archive actuellement fournie contient notamment les références suivantes (noms internes observés sans analyse de leur contenu) :
- `CAMEO/Ariane Celestin.webp`
- `CAMEO/Nathan Adams.webp`, `CAMEO/Katie Forester.png`
- `CAMEO/Nathaniel Adams.webp`, `CAMEO/Michael Forester.webp`
- `CAMEO/Wyatt Cardamom.webp`
- `CAMEO/Dominiscian.webp`
- `CAMEO/Don Morleone.webp`
- `CAMEO/Seigneur Enma.webp`
- `CAMEO/Employé 1.png`, `CAMEO/Employé 2.png`, `CAMEO/Employé 3.jpg`
- `CAMEO/Mafiamille 1.webp`, `CAMEO/Mafiamille 2.png`, `CAMEO/Mafiamille 3.webp`, `CAMEO/Mafiamille 4.webp`

Il peut exister plus d'images que de PNJ demandés : ne créer que **deux employés** (rouge et bleu) et **trois Mafiamille**, en sélectionnant les images appropriées parmi les références. Les images d'autres personnages ne constituent **pas** une autorisation à ajouter davantage de caméos.

### 7.3 États de jeu à tester
1. Avant postgame : seuls les quatre caméos aventure prévus sont accessibles ; les postgame-only restent bloqués.
2. Chaque interaction ouvre une proposition **Oui/Non** ; **Non** ne déclenche aucun combat.
3. Le choix du personnage joueur donne la bonne variante : garçon → Katie et Nathaniel ; fille → Nathan et Michael.
4. Les équipes du premier combat et des revanches sont les bonnes selon la progression de la sauvegarde.
5. Les deux employés sont battus avant Domniscian ; les trois Mafiamille avant Don Morleone. Aucune victoire ne s’enregistre sur refus ou défaite.
6. Les récompenses uniques ne sont jamais dupliquées lors des réaffrontements ; gérer le sac plein.
7. Avant victoire contre Seigneur Enma, **Enma capturable** est absent de la Caverne Azurée ; après victoire, il apparaît dans la rencontre statique prévue, une seule fois.
8. Vérifier que tous les sprites nouveaux s’affichent sans palette incorrecte, transparence cassée ou corruption d’animation.
9. Compiler avec les outils du dépôt et fournir le résultat exact. Une compilation réussie ne remplace pas un test en jeu.

### 7.4 Compte rendu final attendu
- Liste des caméos, PNJ d’entourage, cartes, scripts, flags, équipes et objets implémentés.
- Liste des sprites réellement dessinés et intégrés, avec leurs dimensions, palettes et fichiers sources/exportés.
- Captures ou previews des sprites de combat et overworld lorsqu’elles existent réellement.
- Résultat exact du build et des contrôles joués/simulés.
- Points non implémentés ou bloqués et décisions explicitement laissées à l’utilisateur.

**Ne pas créer un événement ou un objet nouveau non demandé simplement parce qu’il paraît intéressant. Le joueur doit découvrir les caméos de façon naturelle, sans qu’ils remplacent des événements majeurs de Rouge Feu.**
