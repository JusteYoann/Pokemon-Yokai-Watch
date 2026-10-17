# Pokémon Rouge Feu × Yo-kai Watch — Protagonistes et rival

**Version : 1.1 — 16 octobre 2026**  
**Projet :** `JusteYoann/Pokemon-Yokai-Watch`  
**Étape :** remplacement graphique des personnages principaux, **après** l'implémentation des équipes et des caméos.  
**Références à transmettre à Codex :** archive `Protagoniste.rar` et, en complément facultatif, la planche de sprites de Pokémon Rouge Feu / Vert Feuille.

## 1. Objectif

Créer et intégrer de **nouveaux sprites originaux en pixel art Rouge Feu** pour les trois personnages suivants :

| Personnage remplacé dans Pokémon Rouge Feu | Nouveau personnage | Condition |
| --- | --- | --- |
| Red, héros masculin | **Nathan Adams** | Joueur : garçon |
| Leaf, héroïne féminine | **Katie Forester** | Joueur : fille |
| Blue, rival | **Matt Descartes** | Toujours, quel que soit le choix du joueur |

Il ne s'agit **pas** d'une simple recoloration des sprites de Red, Leaf et Blue : il faut reproduire les apparences des personnages de Yo-kai Watch en respectant fidèlement l'esthétique de Pokémon Rouge Feu.

L'archive `Protagoniste.rar` contient les références suivantes (noms constatés dans son sommaire) :
- `Protagoniste/Nathan Adams.webp`
- `Protagoniste/Katie Forester.png`
- `Protagoniste/Matt Descartes.webp`

Si l'extraction de RAR n'est pas possible, demander une archive ZIP ou les images séparées : **ne pas prétendre avoir consulté les visuels sans les avoir ouverts**.

## 2. Audit obligatoire des ressources du jeu

Avant toute modification, inspecter **les fichiers réels du dépôt** pour retrouver l'ensemble des sprites, tables et références de Red, Leaf et Blue. Les chemins exacts sont à déduire du projet : ne pas supposer qu'il utilise la même structure qu'un autre dépôt de décompilation.

Inventorier notamment :

- les sprites de dresseurs vus de face et de dos ;
- les sprites overworld et toutes leurs orientations ;
- les animations de marche, course, vélo, surf, pêche et autres actions effectivement utilisées ;
- les éventuelles poses spéciales, frames de transition et animations d'envoi du Pokémon ;
- les portraits et illustrations des menus de choix garçon/fille, de l'introduction, de la carte Dresseur, du Panthéon ou d'autres interfaces qui utilisent les personnages originaux ;
- tous les scripts et événements où le rival apparaît ;
- les formats, dimensions, contraintes de palette, transparence, compression et ordre des frames.

Fournir une liste **ancienne ressource → nouvelle ressource**, avec les références qu'il faut changer.

## 3. Sprites originaux — direction artistique

Coder/dessiner les nouveaux sprites à partir des références de l'archive **et de l'analyse des sprites officiels du jeu** :

- style pixel art GBA / Pokémon Rouge Feu, proportions et poses crédibles ;
- contours lisibles, ombrages par aplats, nombre de teintes et palettes conformes aux contraintes constatées ;
- vêtements, coiffures, accessoires, silhouettes et couleurs reconnaissables pour Nathan, Katie et Matt ;
- animation cohérente dans chaque direction ;
- aucun gradient, flou ou lissage ;
- pas de portraits modernes simplement réduits automatiquement ;
- pas de recolor superficiel d'un personnage existant ;
- nommage et intégration technique conformes au dépôt.

Créer les **vraies séries de sprites nécessaires**, pas uniquement un portrait ou un overworld immobile. Les animations et variantes exactes doivent découler de l'audit initial.

### Nathan — héros masculin

Remplacer toutes les représentations graphiques du joueur masculin : sélection, overworld complet, actions spéciales, dos en combat, éventuels portraits, carte Dresseur et autres représentations réellement employées.

### Katie — héroïne féminine

Faire exactement la même couverture pour le joueur féminin, avec ses propres dessins, animations et palettes. **Aucune ressource de Nathan ne doit apparaître par erreur** quand Katie est sélectionnée, ni l'inverse.

### Matt — rival

Créer le sprite de dresseur en combat, ses éventuelles poses, son overworld et toutes les apparitions scénaristiques du rival. **Matt remplace visuellement Blue partout**, y compris au Plateau Indigo et dans les combats secondaires déjà existants.

## 4. Choix du personnage, noms et conditions

### Choix garçon/fille

Le choix initial doit rester fonctionnel :
- **Garçon = Nathan**.
- **Fille = Katie**.

Conserver le fonctionnement original du nom personnalisable du joueur : le joueur incarne visuellement Nathan ou Katie, mais ne pas supprimer sans accord l'écran permettant de saisir son prénom.

### Rival : prénom « Matt » obligatoire, non modifiable

**Décision explicite et définitive du créateur : le rival porte le prénom « Matt » dans toutes les parties. Le joueur NE PEUT PAS le renommer.**

- Retirer proprement ou court-circuiter **l'écran de choix/saisie du nom du rival** lors de l'introduction du professeur Chen, sans rompre la suite de l'introduction ni la progression du jeu.
- Initialiser le nom du rival à **Matt** dans les données de sauvegarde / variables réellement utilisées par le moteur ; vérifier et adapter les fonctions qui le lisent si nécessaire.
- Vérifier que le nom visible **Matt** est identique dans les dialogues, les annonces de combat, les équipes de dresseur, les apparitions sur les cartes, les scripts, la Ligue et toute autre interface concernée.
- Matt est le rival **pour les deux choix** du joueur (Nathan ou Katie).
- Conserver les équipes, rencontres et événements du rival déjà validés. **Ne pas modifier son rôle scénaristique** en profitant du changement de nom.
- Ne pas supprimer la possibilité pour le joueur de **choisir son propre prénom**, car cette règle ne concerne que le rival.
- Tester également le comportement sur les nouvelles parties et, autant que techniquement raisonnable, les anciennes sauvegardes : signaler les limitations de compatibilité sans corrompre une sauvegarde.

Le nom complet **Matt Descartes** sert à identifier la référence visuelle, mais l'affichage en jeu doit utiliser exactement **Matt**.

## 5. Compatibilité impérative avec les caméos

Le cahier des charges `CAMEOS_YOKAI_WATCH_CODEX.md` prévoit un caméo du protagoniste **non choisi**. Cette condition doit rester exacte :

| Joueur | Personnage incarné | Caméo Nathan/Katie | Autre caméo conditionnel |
| --- | --- | --- | --- |
| Garçon | Nathan | **Katie** | **Nathaniel** |
| Fille | Katie | **Nathan** | **Michael** |

Les sprites de héros jouable et de caméo dresseur peuvent avoir des formats différents. Prévoir les ressources nécessaires aux deux usages sans collision d'identifiants, de palettes ni de tables.

**Ne jamais faire apparaître le protagoniste choisi comme son propre caméo.** Les combats de caméos restent entièrement **facultatifs**, déclenchés uniquement quand le joueur parle au PNJ et confirme **Oui** ; le refus **Non** ne doit pas lancer de combat.

## 6. Éléments à ne pas modifier

Cette étape ne doit toucher à aucun autre contenu hors des ajustements d'affichage et de scripts indispensables à l'intégration des personnages :

- les 151 Yo-kai, leur correspondance `SPECIES_*`, leurs statistiques, talents et évolutions ;
- les équipes des champions, du Conseil 4, des admins Rocket, de Giovanni et du Dojo ;
- les équipes du rival et sa chronologie : Cigalopin → Cigallard → disparition, Jibanyan → Shogunyan seulement à la Ligue, Navétéran → Navigarmateur seulement à la Ligue, arrivée de Camaueil seulement au Champion ;
- les trois variantes de starter du rival : Komastar contre Padrezo, Appak contre Komasan, Émettor contre Kappacap ;
- les lieux, dialogues simples, combats optionnels, récompenses et scripts des caméos déjà conçus ;
- le déblocage de l'apparition d'Enma dans la Caverne Azurée après la victoire contre Seigneur Enma ;
- les cadeaux, fossiles, rencontres sauvages, objets, échanges et progression scénaristique hors de cette demande.

**Ne pas recréer les combats ni rééquilibrer les dresseurs pour ce travail graphique.**

## 7. Méthode de réalisation demandée à Codex

1. **Audit.** Localiser les ressources de Red, Leaf et Blue, leurs animations, leurs palettes, leurs références dans les scripts et les écrans de l'interface.
2. **Création graphique.** Dessiner les ressources originales de Nathan, Katie et Matt en suivant l'archive et les contraintes graphiques GBA vérifiées.
3. **Intégration.** Ajouter les fichiers, palettes, tables, scripts ou déclarations nécessaires. Éviter toute collision avec les sprites de caméos.
4. **Contrôle des conditions.** Vérifier le choix garçon/fille, la substitution de Matt, les caméos conditionnels et le fonctionnement de l'introduction.
5. **Contrôle du nom fixe.** Vérifier que l’introduction ne propose plus de renommer le rival, que celui-ci est initialisé à « Matt » et que ce prénom s’affiche correctement dans tous les scripts/combats, pour les deux sexes de personnage.
6. **Compilation.** Compiler le projet avec le système disponible et relever les erreurs éventuelles.
7. **Contrôle visuel.** Produire des planches des frames/sprites créés et, si possible, des captures en jeu des personnages et animations. Ne pas déclarer « testé en jeu » si seule la compilation a été effectuée.
8. **Compte rendu.** Détailler les fichiers touchés, les ressources générées, les tests effectivement réalisés, les incohérences et ce qui reste à valider.

Si l'environnement ne permet pas de produire de vrais sprites utilisables, **le dire honnêtement**, fournir un audit concret et une liste des ressources manquantes, mais ne pas prétendre que le remplacement graphique est terminé.

## 8. Checklist finale

- [ ] Nathan affiché avec ses animations lorsqu'on choisit un garçon.
- [ ] Katie affichée avec ses animations lorsqu'on choisit une fille.
- [ ] Matt affiché dans toutes les apparitions du rival.
- [ ] Aucun choix de nom du rival pendant l’introduction ; le prénom **Matt** est imposé dans tous les textes, combats et menus concernés, quel que soit le personnage choisi.
- [ ] Le joueur peut toujours personnaliser son propre prénom.
- [ ] Aucune image erronée de Red, Leaf ou Blue dans les écrans et animations répertoriés.
- [ ] Les vues de dos et animations de combat correspondent aux personnages choisis.
- [ ] Les caméos Nathan/Katie et Nathaniel/Michael dépendent bien du choix du joueur.
- [ ] Les ressources caméos existantes ne sont pas écrasées.
- [ ] Aucun changement non autorisé des équipes, récompenses, évolutions ou scripts de scénario.
- [ ] Compilation exécutée et statut réel communiqué.
- [ ] Fichiers graphiques et aperçus livrés ou limitations signalées.

## 9. Livrable et priorité

Cet ensemble d'instructions sera envoyé à Codex **après la fin du chantier équipes + caméos**. Le travail demandé ici est uniquement de **remplacer l'identité graphique du protagoniste masculin, du protagoniste féminin et du rival**, tout en maintenant le comportement du jeu, les événements validés et la logique des caméos.

## 10. Résumé explicite des décisions de noms (prioritaire)

| Élément | Règle |
| --- | --- |
| Joueur masculin | Apparence de Nathan Adams ; son prénom reste personnalisable |
| Joueuse | Apparence de Katie Forester ; son prénom reste personnalisable |
| Rival | Apparence de Matt Descartes ; nom affiché **Matt**, fixe et non modifiable |
| Caméo si Nathan joué | Katie |
| Caméo si Katie jouée | Nathan |
| Autre caméo selon sexe | Nathaniel si garçon / Michael si fille |

En cas d'instruction antérieure contradictoire sur la possibilité de renommer le rival, **la présente version 1.1 a priorité**.
