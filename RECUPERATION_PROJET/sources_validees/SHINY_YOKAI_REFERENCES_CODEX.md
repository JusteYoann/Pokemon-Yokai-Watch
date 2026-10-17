# Pokémon Rouge Feu × Yo-kai Watch — Consignes Codex pour les shiny (v1.1)

Ce document définit la direction artistique à utiliser pour les **sprites shiny** du projet.

Je fournis un dossier / une archive de références shiny réalisé en amont. Même si certains noms de fichiers ou références internes peuvent provenir de Yo-kai officiels hors du roster final du hack, ce dossier constitue la **base visuelle principale** pour concevoir les shiny du projet.

## 1. Objectif général

Je veux que **seules les familles de Yo-kai représentées dans l’archive de références shiny retenue possèdent un shiny visuellement distinct**. Les autres familles n’ont **aucun redesign shiny** : même apparence et mêmes couleurs que la forme normale. La règle s’applique aux 151 espèces du hack, sans exiger une variante unique pour chacune.

Le but n'est pas de faire des recolors aléatoires :
- il faut reprendre les **couleurs, motifs ou idées de design** des références ;
- il faut conserver une bonne lisibilité en sprite GBA / Pokémon Rouge Feu ;
- il faut garder une cohérence au sein des lignes d'évolution.

## 2. Règle principale

Quand une référence shiny existe dans l'archive fournie, **utilise-la comme base prioritaire**.

Dans de nombreux cas, la référence peut être transposée quasiment telle quelle.
Dans d'autres, il faudra l'**adapter intelligemment** au sprite final du hack.

Si la référence correspond à une seule forme d’une famille, étends son identité colorimétrique à ses pré-évolutions et évolutions de la même famille. **N’étends jamais cette identité à une famille entièrement absente de l’archive retenue.**


### 2.1 Règle prioritaire de sélection des familles — NOUVELLE DÉCISION

**C’est une condition obligatoire, prioritaire sur les formulations antérieures de ce document :**

1. Codex dresse la liste exacte des références présentes dans **la version définitive de l’archive shiny jointe à la mission**. Ne pas prendre une archive de caméos ou de protagonistes à sa place.
2. Il rattache chaque référence à une espèce canonique du projet puis à sa **famille évolutive**, en vérifiant les évolutions réelles du hack.
3. **Au moins un membre de la famille référencé et retenu dans l’archive** → produire un shiny distinct et cohérent pour l’ensemble de cette famille, même si certains membres ne figurent pas individuellement dans le ZIP.
4. **Aucun membre de la famille référencé dans l’archive retenue** → **aucun shiny différent visuellement pour cette famille**. Pas de nouvelle palette créative, pas de recoloration aléatoire, pas de motif supplémentaire. Le sprite et la palette shiny doivent présenter exactement les mêmes couleurs et détails que la forme normale.
5. Les éventuelles données shiny déjà présentes dans le dépôt pour une famille non retenue doivent être neutralisées **sur le plan visuel seulement**, pour que le jeu ne montre pas une ancienne version shiny non approuvée.
6. Ne pas modifier par défaut les probabilités, le calcul interne du statut shiny, la capture, les statistiques ni les autres mécaniques : « pas de shiny » signifie ici **pas d’apparence alternative**, pas la suppression technique du statut shiny. Si une exclusion du statut lui-même s’avère nécessaire, la signaler pour décision.
7. **Kappacap et Noko :** leurs références sont retirées de la sélection. Ignorer ces références si elles restent accidentellement dans un ancien ZIP ; leur famille ne peut recevoir un shiny distinct **que si une autre forme de la famille possède une référence retenue**. Ne rien inventer à partir de leur référence exclue.

Dans le rapport final, fournir deux inventaires : **familles avec shiny distinct** et **familles sans shiny distinct**, avec la référence utilisée pour chaque famille retenue.

## 3. Ce qu'il faut produire

Je veux que cette direction shiny soit appliquée aux ressources shiny du jeu, selon ce que le projet utilise réellement, notamment :
- sprite de face shiny,
- sprite de dos shiny,
- palettes shiny,
- et toute autre ressource shiny réellement utilisée.

Si le projet utilise aussi des icônes / mini-icônes avec palette shiny distincte, applique la cohérence nécessaire.

## 4. Consignes générales de design

- Préserver la silhouette et la lisibilité du Yo-kai de base.
- Garder un rendu fidèle au style GBA / Rouge Feu.
- Éviter les détails trop fins ou trop complexes lorsqu'ils ne passeront pas bien en sprite.
- Quand le redesign complet est trop complexe, privilégier une **adaptation colorimétrique simple**.
- Toujours respecter la hiérarchie visuelle du sprite : visage, éléments forts, accessoires, motifs principaux.

## 5. Cas particuliers explicitement validés

### 5.1 Robonyan / Robonyan F / Robonyan 28
- **Robonyan** et **Robonyan F** : faire des shiny **dorés**.
- **Robonyan 28** : le rendre **noir**, avec malgré tout des **éléments dorés**, afin qu'il paraisse plus impressionnant et plus puissant.
- Pour Robonyan 28, il est validé d'ajouter un petit bonus de design : **des cornes sur la tête**.

### 5.2 Usapion
- Usapion shiny ne change pas principalement de couleurs.
- Il prend surtout le **regard / les yeux d'Emperor**.
- Il faut donc un shiny reconnaissable mais subtil.

### 5.3 Coach Antonic
- Le shiny de Coach Antonic peut récupérer un **style “vêtements de plage”**.
- Il ne faut pas juste recolorer bêtement : l'idée est d'assumer ce petit changement de tenue, tout en gardant le sprite lisible et cohérent avec le style du jeu.

### 5.4 Jojojoyeux
- Le shiny de Jojojoyeux ne change pas forcément beaucoup de couleurs.
- Il peut surtout récupérer un **costard** / une tenue plus habillée.
- **Ne pas reprendre les confettis** visibles sur l'artwork de référence.

### 5.5 Télémir et Triptic-tac
- Pour **Télémir** et **Triptic-tac**, ne cherche pas à reproduire tout le redesign de la référence si celui-ci est trop complexe.
- Il vaut mieux se contenter **des couleurs**.
- Objectif : éviter un rendu embrouillé ou illisible.

### 5.6 Brumella
- Brumella doit devenir **noir et blanc** comme dans l'artwork de référence.
- En revanche, **ne pas lui ajouter la robe** ou tout autre ajout complexe qui pourrait compliquer le sprite.
- Ici aussi, priorité à la lisibilité.

### 5.7 Référence “Platinos”
- Si l'archive de référence contient **Platinos** comme base visuelle à transposer, l'idée validée est la suivante :
  - couleurs **argentées brillantes**,
  - conserver les éléments intéressants comme **la touffe** et **la corne** si le Yo-kai concerné du hack possède déjà des équivalents visuels pertinents.
- Applique cela intelligemment au Yo-kai concerné dans le projet.

### 5.8 Couchtar
- Pour Couchtar shiny :
  - changer les **couleurs**,
  - ajouter **un sourire**,
  - sans modifier lourdement le design général.

## 6. Références à ignorer / retirer

Le dossier de référence contient actuellement des cas qui seront retirés ou qui ne doivent pas être utilisés tels quels :
- **Kappacap**
- **Noko**

Si leurs références shiny restent dans une ancienne archive, **ignore-les : elles ne sont pas retenues**. Ne déduis pas un shiny inédit de ces deux références exclues. Une autre forme de leur famille peut justifier un shiny familial uniquement si elle possède sa propre référence conservée.

## 7. Adaptation par ligne d'évolution

Quand une référence est surtout donnée pour une seule forme, tu dois **propager intelligemment l'idée** aux autres formes de la même ligne.

### Exemple validé : Loubarbare / Racaïd
Pour **Loubarbare** et **Racaïd**, si une référence existe dans le dossier, il faut garder la logique des zones colorées au même endroit.
Exemple validé :
- cheveux **jaunes**,
- peau **violette**,
- partie basse / bas du corps **verte**.

Cette logique doit être conservée d'une forme à l'autre.

### Exemple validé : Komasan
Exemple de direction shiny à respecter pour **Komasan** :
- peau **blanche**,
- baluchon / éléments principaux en **bleu foncé**,
- flammes conservées dans la logique validée,
- intérieur des oreilles et petits éléments de peau en **rose**.

Cette logique doit ensuite être adaptée avec cohérence à **Komaous** et **Komastar**.

### Exemple validé : lignes évolutives en général
Si une forme d’une famille dispose d’une référence **retenue**, adapte le shiny aux autres formes de cette famille pour conserver une **famille visuelle**. **Si la famille entière n’est pas représentée, toutes ses formes gardent les couleurs et le design normaux.**

## 8. Cas où il faut simplifier

Quand la référence officielle est trop complexe pour un sprite GBA :
- simplifier les motifs,
- garder les couleurs principales,
- conserver seulement 1 ou 2 idées visuelles fortes,
- éviter tout ajout qui casserait la lisibilité du sprite en combat.

Ceci est particulièrement important pour :
- Télémir,
- Triptic-tac,
- Brumella,
- et tout autre cas où l'artwork est trop chargé.

## 9. Compatibilité avec le projet

Les shiny doivent être intégrés sans modifier :
- les espèces,
- les statistiques,
- les noms,
- les évolutions,
- les teams,
- ou d'autres éléments de gameplay.

Cette mission concerne la **direction visuelle des shiny**.

## 10. Vérifications attendues

À la fin, je veux que tu me fournisses :
1. la liste des fichiers shiny modifiés ;
2. les lignes d'évolution pour lesquelles tu as dû extrapoler une référence ;
3. les cas particuliers traités manuellement ;
4. les références que tu as volontairement simplifiées ;
5. les références ignorées (notamment Kappacap et Noko si encore présentes) ;
6. les éventuelles limites techniques de palette ou de lisibilité rencontrées ;
7. la liste exhaustive des familles avec shiny distinct et leur référence source ;
8. la liste exhaustive des familles sans shiny distinct, conservant leur apparence normale.

## 11. Priorité

Priorité absolue : créer un shiny distinct **uniquement pour les familles représentées dans les références retenues**, avec des adaptations **belles, cohérentes, lisibles et fidèles aux sources**. Les autres familles gardent leur apparence normale.
