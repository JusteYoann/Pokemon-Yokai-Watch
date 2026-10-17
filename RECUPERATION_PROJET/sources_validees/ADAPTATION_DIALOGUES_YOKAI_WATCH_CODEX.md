# Pokémon Rouge Feu × Yo-kai Watch — Adaptation des dialogues et des textes visibles

**Version : 1.1 — Mission séparée pour Codex (Kanto conservé définitivement)**  
**Portée : textes, dialogues et cohérence narrative ; pas une nouvelle refonte des équipes, graphismes ou mécaniques.**

## 1. Objectif

Parcourir **l'ensemble des textes visibles par le joueur** dans le dépôt du ROM hack et les adapter pour que l'aventure paraisse naturellement se dérouler dans un monde de **Yo-kai Watch**, tout en conservant l'ossature et la progression de Pokémon Rouge Feu. Le résultat ne doit pas ressembler à un simple « rechercher / remplacer » automatique.

Lire les fichiers de référence du projet, notamment `01_POKEDEX_151.csv`, les données réelles d'espèces, les équipes déjà validées, les rencontres et événements spéciaux, ainsi que les cahiers des charges des caméos et protagonistes intégrés. Si ces fichiers sont absents du dépôt, le signaler et ne pas inventer de correspondances.

## 2. Vocabulaire

- Remplacer les mentions textuelles de **« Pokémon »**, sous toutes les casses et graphies pertinentes (`Pokémon`, `POKéMON`, `POKEMON`, pluriels, etc.), par **« Yo-kai »** dans les textes affichés au joueur.
- Adapter la grammaire autour des remplacements : « un Yo-kai », « des Yo-kai », « ton Yo-kai », « les Yo-kai », etc. Reformuler les phrases devenues maladroites plutôt que faire un remplacement mécanique.
- Adapter intelligemment les tournures : « Dresseur de Pokémon » -> « Dresseur de Yo-kai », « Pokémon sauvage » -> « Yo-kai sauvage », « mes Pokémon » -> « mes Yo-kai ».
- Les appellations institutionnelles contenant « Pokémon » (Club des Fans de Pokémon, Tour Pokémon, etc.) peuvent être adaptées à leur équivalent Yo-kai dans le **texte visible**, sans changer les identifiants techniques de cartes ou d'événements.
- Pour les autres noms de mécaniques et objets (`Pokédex`, Poké Balls, Centre Pokémon, etc.), inventorier les occurrences, corriger seulement celles dont l'adaptation est clairement compatible avec les terminologies et mécaniques déjà validées et **signaler les choix terminologiques discutables** avant une modification majeure. Ne pas renommer arbitrairement des objets ou systèmes dont la mécanique et l'interface seraient inchangées.

**Interdiction :** ne pas faire de remplacement global dans les noms de fichiers, les macros, les constantes `SPECIES_*`, les identifiants de scripts, les chemins de ressources ou les commentaires techniques nécessaires au fonctionnement du moteur.

## 3. Noms d'espèces dans les dialogues : vérification contextuelle obligatoire

Lorsqu'un PNJ cite explicitement le nom d'un Pokémon original :

1. Retrouver la scène concernée et identifier à quel Pokémon original elle fait référence.
2. Déterminer si l'espèce est liée à une **constante `SPECIES_*`**, un don, un échange, une rencontre scriptée, un objet, un boss ou une simple préférence exprimée dans un dialogue.
3. Pour les espèces ordinaires, utiliser la correspondance **exacte** présente dans `01_POKEDEX_151.csv` et dans les données de jeu actuelles ; ne pas déduire une équivalence d'après l'apparence ou le type.
4. Pour un événement personnalisé, **prioriser la règle spécifique de l'événement déjà validé** plutôt que la correspondance générique. Vérifier la rencontre réellement implémentée dans le script.
5. Si le dialogue exprime une préférence sans dépendance technique (« Je suis fan de Pikachu ! »), choisir un Yo-kai plus naturel pour la scène, par exemple **Jibanyan**, afin que la référence reste crédible et mémorable.
6. Accorder les articles, les pronoms, la conjugaison et la ponctuation, ainsi que les éventuels changements de genre ou de nombre.
7. Ne jamais laisser le texte annoncer une espèce tandis que la rencontre, l'échange ou le combat en déclenche une autre.

### Exemples à vérifier

| Ancien contexte | Traitement attendu |
|---|---|
| PNJ admirateur de Pikachu | Peut devenir admirateur de **Jibanyan** pour la cohérence du caméo ; choix narratif assumé |
| Mention générique directement liée à `SPECIES_PIKACHU` | Le fichier de correspondance associe cette constante à **Passpa** ; vérifier le contexte avant de modifier |
| Ronflex qui bloque la route | Respecter la rencontre scriptée déjà fixée avec **Misterre** sur les routes concernées, plutôt qu'une simple équivalence de constante |
| Rencontre dans la Caverne Azurée | Utiliser **Enma** et respecter son verrou de déblocage après Seigneur Enma |
| Cadeau, fossile, échange spécial ou starter | Utiliser **la variante et l'espèce réellement programmées**, pas une correspondance présumée du jeu original |

Le but est de rendre **la scène vraie**, pas seulement de remplacer un nom.

## 4. Cohérence de l'univers et des personnages

- Adapter les références à l'univers Pokémon qui n'ont plus de sens dans notre hack : anecdotes de collection, légendes sur des espèces, spécialités de PNJ, clubs de fans, descriptions de lieux, dialogues liés aux combats ou à des événements.
- Préserver la personnalité générale des PNJ et la fonction des événements originaux : conseils utiles, indications de chemin, tutoriels et indices nécessaires pour progresser.
- Les PNJ peuvent adorer **Jibanyan, Komasan, Usapion, Whisper** ou d'autres Yo-kai cohérents avec leur environnement, sans être forcément restreints à la correspondance technique d'une espèce.
- Prendre en compte **Nathan/Katie** comme héros ou héroïne, **Matt** comme rival au nom fixe, et les caméos selon le sexe du joueur. Ne jamais réintroduire les prénoms Red, Leaf ou Blue dans les dialogues joueurs si les remplacements sont achevés.
- Pour les caméos Yo-kai Watch, conserver le ton sobre déjà demandé : phrases de rencontre et de combat naturelles, sans grands rappels de l'intrigue de Yo-kai Watch.
- Respecter les scénarios déjà validés : disparition non expliquée de Cigallard du rival ; surprise de Shogunyan, Navigarmateur et Camaueil au Champion ; conditions de présence d'Enma ; récompenses et événements des caméos.

## 5. Nom de la région : décision définitive — conserver Kanto

**DÉCISION VALIDÉE : la région doit continuer à s'appeler « Kanto ».** La proposition antérieure de la renommer « Granval-sur-Mer » est **abandonnée et ne doit pas être appliquée**.

- Conserver **Kanto** dans tous les textes, dialogues, écrans, cartes et interfaces où il désigne la région.
- Conserver les noms existants des **villes, routes, îles, bâtiments et lieux** de Rouge Feu.
- Ne modifier **aucun identifiant technique** de cartes, de zones, d'événements ou de scripts à des fins de renommage.
- Adapter uniquement les références aux créatures et à l'univers Pokémon quand cela améliore la cohérence avec **Yo-kai Watch**, sans changer la géographie du jeu.
- Ne pas faire d'audit ou de proposition de changement de nom de région : **ce choix est tranché**.
- Si un texte présente une contradiction narrative liée à la région, le reformuler en préservant le nom « Kanto » et le sens de la scène, sans inventer de nouveaux lieux.

**Priorité en cas de contradiction documentaire :** cette version 1.1 fait autorité sur toute suggestion antérieure de renommer Kanto en « Granval-sur-Mer ».

## 6. Surfaces textuelles à auditer

Recenser les textes du dépôt selon l'organisation réelle du projet :

- Dialogues des PNJ de villes, routes, maisons et bâtiments ;
- Instructions, conseils et panneaux ;
- Dialogues des dresseurs avant et après les combats et à la revanche ;
- Textes des champions, Ligue, rival Matt, Team Rocket et caméos ;
- Introduction du professeur, choix du protagoniste, scènes de début et de fin ;
- Textes liés aux cadeaux, échanges, légendaires, fossiles, Centre/Club, événements scriptés ;
- Messages de tutoriels, menus et interfaces où le terme « Pokémon » apparaît ;
- Bibliothèques de textes partagées et textes générés dynamiquement à partir des noms d'espèces.

**Attention :** les noms d'espèces affichés dynamiquement peuvent provenir des tables d'espèces déjà modifiées ; ne pas remplacer à la main des placeholders tels que noms dynamiques, variables, marqueurs de texte ou séquences de contrôle.

## 7. Contraintes techniques GBA

- Conserver tous les tokens de contrôle, variables, placeholders, macros, codes couleur, pauses, sauts de ligne et séquences d'affichage exigés par le moteur de texte réel du dépôt.
- Respecter la taille des boîtes de dialogue, la largeur des lignes, le nombre de lignes et les retours à la ligne.
- Vérifier les accents, caractères spéciaux et le rendu de « Yo-kai » et des noms de lieux existants avec l'encodage et la police effectivement disponibles.
- Corriger les phrases qui débordent ; ne pas tronquer des informations indispensables.
- Vérifier les variantes dépendantes du sexe du joueur et les noms de joueur variables.
- Modifier les *chaînes de texte affichées* et, si nécessaire, leurs références appropriées, **sans casser les flags, les conditions de scripts, les batailles ou les téléportations**.
- Travailler dans la langue effectivement utilisée par le jeu. S'il reste des textes anglais ou un mélange de langues, inventorier cette situation et proposer une solution cohérente au lieu de laisser un résultat moitié français, moitié anglais.

## 8. Procédure de travail

**Phase A — Audit :** localiser tous les dialogues et textes visibles ; dresser une liste des occurrences de « Pokémon », des noms d'espèces originales et des références à Kanto. Identifier les sources de noms dynamiques et les correspondances scriptées.

**Phase B — Corrections sûres :** remplacer et reformuler les dialogues liés aux Yo-kai ; adapter les mentions d'espèces en respectant le Pokédex et les événements effectivement programmés ; rendre les textes grammaticalement naturels. Ne jamais renommer la région : **Kanto doit rester Kanto**.

**Phase C — Contrôle de cohérence :** vérifier les scènes de cadeaux, les clubs de fans, les rencontres spéciales, les variantes du protagoniste, Matt, le rival, la Ligue et les caméos. Contrôler que l'information communiquée au joueur reste exacte.

**Phase D — Vérifications techniques :** compiler si le projet le permet ; examiner les erreurs et avertissements ; tester en jeu les scènes accessibles quand c'est possible ; distinguer clairement vérification statique, compilation et test réel.

**Phase E — Compte rendu :** indiquer les fichiers modifiés, le nombre et la catégorie des textes modifiés, les exceptions contextuelles, les noms non résolus, les limites d'affichage et les éventuels problèmes techniques. Confirmer explicitement dans le compte rendu que **Kanto et les noms des lieux ont été conservés**.

## 9. Protections et priorités

1. **Ne pas altérer** les 151 correspondances d'espèces, les statistiques, attaques, évolutions, équipes de boss et de dresseurs, les sprites ou les cartes déjà conçues.
2. **Ne pas annuler** les modifications de caméos, de scénario ou les conditions de déblocage existantes.
3. **Ne pas inventer** de nouvelles mécaniques, objets, dialogues de quête obligatoires ou changements de progression.
4. Si une incohérence est impossible à résoudre par une simple correction textuelle, **la signaler**, avec une proposition minimale, plutôt que modifier le scénario de sa propre initiative.
5. Conserver le dépôt compilable et ne jamais annoncer un test non effectué.

**Résultat attendu :** un jeu dans lequel on parle naturellement de Yo-kai, où les espèces citées correspondent à ce que le joueur voit et obtient réellement, sans références incohérentes à l'ancien univers ni modifications de gameplay non autorisées.
