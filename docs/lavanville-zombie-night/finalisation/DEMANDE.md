# CODEX — FINALISATION DE LAVANVILLE : ZOMBIE NIGHT

## 1. Objectif

Nous travaillons sur le ROM hack **Pokémon Rouge Feu × Yo-kai Watch**, dans le dépôt :

`JusteYoann/Pokemon-Yokai-Watch`

La refonte de Lavanville est déjà en cours. Les sprites d'Alyzon Bie et des zombies ont été réalisés lors d'une précédente session Codex.

**Ta mission est de terminer entièrement le chapitre Lavanville / Tour Pokémon / Alyzon Bie et ses raccordements avec Céladopole.**

Il ne s'agit pas de recommencer le travail existant.

### Branche de travail

Commence par inspecter :

`feature/lavanville-zombie-night`

Retrouve les modifications, sprites, animations et éventuels prototypes déjà créés.

Vérifie l'état du dépôt et les travaux les plus récents avant de modifier quoi que ce soit.

Si certains éléments sont déjà intégrés et fonctionnels, conserve-les.

Ne fusionne rien sur `master`.

Ne supprime aucune modification existante sans justification.

---

# 2. LAVANVILLE — ZOMBIE NIGHT ÉTERNELLE

Lavanville est désormais une ville infestée de zombies.

La ville doit être plongée dans une **nuit permanente**, accompagnée d'une **brume verte translucide et lentement animée**.

Ces effets doivent être présents immédiatement lorsque le joueur entre dans Lavanville.

Il n'y a pas de cinématique d'activation de la nuit.

### Ambiance

- Nuit permanente dans les extérieurs de Lavanville.
- Brume verte translucide animée.
- Visibilité suffisante pour éviter les zombies.
- Musique : **Zombie Night (Town) — Yo-kai Watch 3**.
- Les effets extérieurs disparaissent en quittant Lavanville.
- La ville reste infestée après l'obtention du badge.

La musique existe déjà dans les ressources du projet : retrouve-la et réutilise-la.

Ne modifie pas les autres musiques validées.

### Population

Il ne reste aucun habitant humain ordinaire à Lavanville.

Les rues et les maisons sont occupées par des zombies.

Monsieur Fuji est complètement retiré de l'histoire.

Ses événements et dialogues doivent être remplacés ou supprimés proprement, sans casser la progression.

---

# 3. ZOMBIES ERRANTS DANS LA VILLE

Les zombies errants utilisent les sprites overworld déjà créés.

**Ne redessine pas les sprites.**

Retrouve les assets existants et utilise-les.

Les zombies se déplacent dans les rues et certaines maisons.

Ils possèdent des comportements variés :

- Patrouilles.
- Changements de direction.
- Surveillance de certains passages.
- Déplacements plus ou moins rapides selon leur variante.

Lorsqu'un zombie repère le joueur, il déclenche un combat.

### Règles de combat

Le zombie errant combat directement : il ne possède pas d'équipe de Yo-kai.

- Capture impossible.
- Fuite impossible.
- Victoire par K.O.
- Zombie toujours présent après la victoire.
- Combat répétable indéfiniment.
- Courte immunité après le combat pour éviter les déclenchements immédiats.

### Règle fondamentale

**Tous les zombies errants doivent pouvoir être esquivés.**

Les déplacements doivent être lisibles et les passages rester praticables.

Évite tout softlock, blocage de porte ou enchaînement de combats incontrôlable.

Conserve les quatre variantes de zombies si elles ont déjà été créées. Vérifie leurs statistiques et leur équilibrage.

---

# 4. TOUR POKÉMON — NOUVELLE ARÈNE

La Tour Pokémon devient le véritable défi permettant d'obtenir le quatrième badge.

Le joueur doit atteindre le sommet pour affronter Alyzon Bie.

Conserve la structure générale des sept étages.

## Rencontres aléatoires

**Les rencontres aléatoires de Yo-kai sauvages sont conservées.**

Elles fonctionnent normalement :

- Capture autorisée.
- Fuite autorisée.
- Expérience normale.
- Tables de rencontres existantes préservées, sauf nécessité technique justifiée.

Le Scope Sylphe n'est plus nécessaire pour identifier les Yo-kai.

Supprime les blocages de progression liés à cet objet.

## Zombies Dresseurs

Les zombies de la Tour utilisent **exactement les mêmes sprites overworld que les zombies errants de Lavanville**.

Il ne faut pas créer de nouveaux sprites overworld spécifiques aux zombies Dresseurs.

La différence se trouve dans leur fonctionnement :

**Les zombies Dresseurs possèdent des équipes de Yo-kai.**

Ils doivent utiliser le système de combat classique des Dresseurs.

Ils disposent donc d'une équipe et de leurs propres Yo-kai, contrairement aux zombies errants.

### Comportement après la victoire

Les zombies Dresseurs ne peuvent être affrontés **qu'une seule fois**.

Après leur défaite :

- Ils restent visibles.
- Ils ne déclenchent plus de combat.
- Ils peuvent conserver leur animation ou leur patrouille.
- Une interaction peut afficher un court dialogue.
- Leur défaite reste enregistrée après sauvegarde.

Ne rends pas ces combats répétables.

### Difficulté et placement

La majorité des zombies Dresseurs doivent être esquivables.

En revanche, **quelques affrontements doivent être obligatoires** pour progresser jusqu'au sommet.

Proposition de répartition :

- Étages inférieurs : premiers zombies, essentiellement esquivables.
- Étages intermédiaires : premier affrontement obligatoire.
- Étages supérieurs : adversaires plus difficiles, second affrontement obligatoire.
- Sommet : Alyzon Bie.

Ne bloque jamais définitivement le joueur si un zombie change de position.

### Équipes

Les zombies Dresseurs doivent utiliser exclusivement des Yo-kai déjà présents dans notre ROM.

Conserve les équipes existantes si elles ont déjà été validées.

Si aucune équipe n'a été définie, crée des équipes cohérentes avec le quatrième badge, en privilégiant les Yo-kai Spectre et les créatures inquiétantes.

Évite de donner systématiquement les mêmes Yo-kai à tous les zombies.

Vérifie que leurs niveaux restent adaptés à la progression.

### Zone de soin

Conserve la zone de soin existante dans la Tour Pokémon.

Elle doit fonctionner normalement.

Tu peux adapter son ambiance visuelle à la Zombie Night sans modifier son fonctionnement.

---

# 5. ALYZON BIE — CHAMPIONNE DE LAVANVILLE

Alyzon Bie remplace Erika, la Championne de Céladopole.

Elle devient officiellement **Championne de Lavanville**.

Son premier combat se déroule au sommet de la Tour Pokémon.

Ses sprites overworld et son portrait ont déjà été réalisés avec Codex.

**Retrouve et réutilise les assets existants. Ne les remplace pas par des graphismes générés automatiquement.**

## Équipe officielle

Alyzon Bie est spécialisée dans le type **Spectre**.

Son équipe est désormais définie :

| Ordre | Yo-kai | Niveau |
|---|---|---|
| 1 | Potofeu | 27 |
| 2 | Whisper | 28 |
| 3 | Triptic-tac | 29 |
| 4 | Mémogre | 31 |

**Mémogre est son Yo-kai signature et doit être envoyé en dernier.**

Vérifie les identifiants internes, les types et les statistiques réelles de ces quatre Yo-kai dans notre ROM.

Ne confonds pas Triptic-tac avec Télémir : nous avons choisi **Triptic-tac**.

Respecte les quatre niveaux indiqués.

Choisis des attaques légales et cohérentes avec leurs capacités, leur niveau et leur rôle dans l'équipe.

Si un Yo-kai n'est pas de type Spectre dans notre ROM, signale-le avant toute modification de type. Ne modifie pas silencieusement ses données.

## Combat de Championne

Le combat doit être reconnu par le moteur comme un combat de Championne d'Arène.

Après la victoire :

- Alyzon Bie reconnaît la valeur du joueur.
- Elle remet le quatrième badge, correspondant à celui d'Erika.
- Le compteur de badges est mis à jour.
- Les capacités et conditions associées au badge sont préservées.
- Le joueur peut poursuivre normalement son aventure.
- Le repaire Mafiamille de Céladopole devient accessible.

Conserve le fonctionnement global des huit badges.

La musique du combat doit être cohérente avec les autres combats de Champions. Si aucune musique spécifique n'a été validée, conserve une musique existante appropriée plutôt que d'en importer une nouvelle.

---

# 6. PREMIÈRE ARRIVÉE À LAVANVILLE

Crée ou finalise la cinématique d'introduction.

Elle se déclenche une seule fois, lors de la première entrée du joueur dans la ville.

### Déroulement

1. Le joueur entre dans Lavanville.
2. La Zombie Night est déjà active.
3. Un zombie s'approche du joueur.
4. Alyzon Bie intervient et se place entre eux.
5. Le zombie recule puis repart.
6. Alyzon Bie explique que la ville est prisonnière d'une Zombie Night éternelle.
7. Elle révèle qu'elle vit volontairement ici, car elle adore les zombies et les trouve mignons.
8. Elle se présente comme Championne de Lavanville.
9. Elle comprend que le joueur est venu pour obtenir son badge.
10. Elle plaisante sur le fait qu'un futur grand Dresseur ne devrait pas avoir peur des zombies.
11. Elle évoque un précédent visiteur, très discret mais particulièrement efficace.
12. Elle précise que ce visiteur fait partie des rares Dresseurs à l'avoir battue en plus de cinq ans.
13. Elle souhaite bonne chance au joueur.
14. Elle se dirige vers la Tour Pokémon.

Le visiteur mystérieux est implicitement **Matt**, le rival.

Ne révèle pas directement son nom.

### Dialogues

Écris des dialogues naturels en français.

Respecte les limites des boîtes de texte GBA.

Alyzon Bie doit être excentrique, passionnée, amusante et compétente.

Elle ne doit pas paraître malveillante.

---

# 7. DIALOGUES AU SOMMET

Avant le combat, Alyzon Bie accueille le joueur avec enthousiasme.

Elle est heureuse qu'il ait réussi à traverser la Tour.

Elle lui rappelle que les zombies ne sont pas forcément méchants, mais qu'ils peuvent être particulièrement coriaces.

Elle explique que le dernier obstacle pour obtenir le badge sera de la vaincre.

Après sa défaite, elle doit reconnaître le talent du joueur, tout en conservant son humour et sa passion pour les zombies.

Crée les dialogues nécessaires :

- Avant-combat.
- Défaite d'Alyzon Bie.
- Remise du badge.
- Dialogue après le combat.
- Interaction ultérieure si le joueur revient au sommet.

---

# 8. ARÈNE DE CÉLADOPOLE

Le bâtiment de l'Arène de Céladopole est conservé.

Il devient la **seconde résidence d'Alyzon Bie**.

## Avant la victoire contre Alyzon Bie

Matt se trouve à l'intérieur.

Il explique au joueur que l'Arène semble abandonnée et qu'il n'y a personne à affronter ici.

Il ne déclenche pas de combat.

## Après la victoire contre Alyzon Bie

Matt n'est plus présent dans l'Arène.

Alyzon Bie peut désormais être rencontrée ici.

Elle explique que cet endroit est sa deuxième maison.

Elle ne peut pas encore être réaffrontée.

## Après la Ligue

Une revanche contre Alyzon Bie devient disponible après la première victoire à la Ligue et l'entrée au Panthéon.

**N'invente pas encore son équipe de revanche.**

Prépare la condition d'accès et, si nécessaire, un dialogue temporaire indiquant qu'elle souhaite affronter le joueur plus tard.

---

# 9. REPAIRE MAFIAMILLE DE CÉLADOPOLE

Le repaire Mafiamille de Céladopole doit être accessible uniquement après la victoire contre Alyzon Bie.

Il remplace toujours le repaire de la Team Rocket.

Ne restaure aucun sprite, dialogue ou nom de Team Rocket.

Conserve les éléments déjà réalisés :

- Sbires Mafiamille.
- Don Morléone.
- Équipes.
- Cartes.
- Musiques.
- Événements validés.

## Flûte Yo-kai

Le joueur récupère désormais la **Flûte Yo-kai dans le repaire Mafiamille**, à la place du Scope Sylphe.

Cette flûte permet de réveiller les Misterre qui bloquent les routes.

Elle ne doit plus être obtenue auprès de Monsieur Fuji.

Vérifie que les scripts de réveil fonctionnent toujours.

Le joueur doit pouvoir progresser vers les routes suivantes sans blocage.

---

# 10. SUPPRESSION DES ANCIENS ÉVÉNEMENTS

Audite les scripts et flags de :

- Monsieur Fuji.
- Scope Sylphe.
- Erika.
- Arène de Céladopole.
- Tour Pokémon.
- Repaire de Céladopole.
- Flûte Yo-kai.
- Misterre bloquant les routes.

Supprime ou adapte les anciens événements devenus incompatibles avec notre scénario.

Ne supprime pas un flag global s'il est utilisé ailleurs.

Préserve les sauvegardes et les mécanismes de progression autant que possible.

---

# 11. TESTS OBLIGATOIRES

Après intégration, compile les versions publique et privée de la ROM.

Teste dans mGBA :

### Lavanville

- Entrée dans la ville.
- Nuit immédiatement active.
- Brume verte animée.
- Musique Zombie Night.
- Cinématique d'Alyzon Bie.
- Absence de répétition de la cinématique.
- Zombies errants.
- Patrouilles et esquives.
- Combats répétables.
- Interdiction de fuite et de capture.
- Entrée et sortie des maisons.

### Tour Pokémon

- Accès sans Scope Sylphe.
- Rencontres aléatoires conservées.
- Captures de Yo-kai sauvages.
- Combats contre les zombies Dresseurs.
- Quelques combats obligatoires.
- Zombies Dresseurs non réaffrontables.
- Sauvegarde des défaites.
- Zone de soin.
- Accès au sommet.

### Alyzon Bie

- Affichage correct du portrait.
- Équipe exacte : Potofeu 27, Whisper 28, Triptic-tac 29, Mémogre 31.
- Combat de Championne.
- Remise du quatrième badge.
- Dialogue après victoire.
- Absence de second badge en cas de retour.

### Céladopole

- Matt présent avant le badge.
- Alyzon Bie présente après le badge.
- Repaire Mafiamille verrouillé avant le badge.
- Repaire accessible après le badge.
- Flûte Yo-kai récupérable.
- Misterre réveillables.
- Aucun blocage de progression.

### Compatibilité générale

- Huit badges toujours disponibles.
- Finale Don Morléone / Don Spiraton préservée.
- 151 Yo-kai préservés.
- 31 OST préservées.
- Aucune régression des autres villes.
- Taille de ROM compatible.
- Mémoire EWRAM/IWRAM/VRAM surveillée.

---

# 12. LIVRABLES

Je souhaite à la fin :

1. Un résumé précis des modifications effectuées.
2. Les fichiers modifiés.
3. Les sprites existants réutilisés.
4. Les nouveaux scripts et événements.
5. Les équipes des zombies Dresseurs.
6. Les dialogues définitifs.
7. Les résultats des compilations.
8. Les résultats des tests mGBA.
9. Les captures des principaux événements.
10. Les éventuelles limitations restantes.
11. Le nom de la branche et les commits réalisés.

Ne présente pas une fonctionnalité comme testée si elle n'a pas réellement été vérifiée.

Si un problème bloque l'intégration, explique-le précisément plutôt que de le contourner en supprimant des fonctionnalités.

**Priorité absolue : terminer Lavanville en réutilisant les sprites déjà réalisés, sans casser le reste de notre ROM hack.**

Tu peux coder, compiler et tester sur la branche dédiée, mais ne fusionne rien sur `master` sans mon autorisation.