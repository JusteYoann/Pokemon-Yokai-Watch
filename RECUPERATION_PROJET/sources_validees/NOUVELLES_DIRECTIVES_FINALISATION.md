# POKÉMON × YO-KAI WATCH — NOUVELLES DIRECTIVES DE FINALISATION

Je souhaite que tu reprennes le développement de mon ROM hack sur la branche `dev/reconstruction-finalisation` du dépôt `JusteYoann/Pokemon-Yokai-Watch`.

**Ce message actualise nos priorités de développement et apporte plusieurs décisions scénaristiques définitives.**

Il complète les cahiers des charges précédents. En cas de contradiction concernant les priorités ou les éléments scénaristiques décrits ci-dessous, les présentes instructions prévalent.

## 1. OBJECTIF PRINCIPAL : TERMINER LE JEU

Ma priorité absolue est désormais de terminer une version complète, stable et jouable de Pokémon × Yo-kai Watch.

Je souhaite pouvoir parcourir l'intégralité de l'aventure principale, battre la Ligue, explorer le postgame et obtenir les 151 Yo-kai.

Je préfère un jeu terminé et riche musicalement, avec moins de quêtes secondaires supplémentaires, plutôt qu'un projet retardé par l'ajout de contenus facultatifs.

**Nouvel ordre de priorité :**

1. Terminer et stabiliser l'aventure principale, les 151 Yo-kai, les rencontres et le postgame existant.
2. Finaliser les personnages, caméos, combats et événements déjà validés.
3. Intégrer en priorité les 20 OST Yo-kai Watch sélectionnées, avec la méthode DPCM validée.
4. Adapter les dialogues, l'histoire et le vocabulaire pour construire un univers cohérent.
5. Terminer les graphismes indispensables, les rencontres statiques et l'introduction personnalisée.
6. Tester, équilibrer et corriger les problèmes du jeu.
7. Seulement ensuite, ajouter les quêtes secondaires facultatives selon le temps et les ressources disponibles.

La stabilité et la possibilité de terminer le jeu restent prioritaires sur toutes les nouveautés.

Les dix quêtes précédemment conçues ne constituent donc plus une obligation bloquante pour la première version finale.

Ne supprime cependant pas les événements déjà implémentés et fonctionnels.

## 2. NOUVELLE HISTOIRE : LE PROFESSEUR CHEN

Le Professeur Chen conserve sa place au début de l'aventure, mais son rôle scientifique change.

Il est désormais **l'inventeur de la Yo-kai Watch**.

Au cours de ses recherches, il a découvert l'existence des Yo-kai, des créatures normalement invisibles aux humains.

Pour les observer, il a mis au point la Yo-kai Watch, une invention permettant à son détenteur de voir ces êtres mystérieux.

Au cours de précédentes explorations, Chen a également découvert une ancienne relique : **le Médallium des Yo-kai**.

Il cherche à comprendre cet objet et souhaite que le protagoniste l'aide à répertorier les 151 espèces de Yo-kai.

Il confie donc deux grands objectifs au joueur :

- Participer à la **Ligue Yo-kai** et tenter d'en devenir le Champion.
- Compléter progressivement le **Médallium des Yo-kai**.

Ces deux objectifs doivent être présentés naturellement dans les dialogues du début de l'aventure.

La Yo-kai Watch est obtenue très tôt et permet narrativement au joueur de percevoir les Yo-kai.

Il n'est pas nécessaire de programmer un nouveau système complexe d'invisibilité : la montre peut fonctionner passivement, afin de préserver le gameplay de Rouge Feu.

Le choix entre Nathan et Katie, le prénom personnalisable du joueur et Matt comme rival fixe doivent être conservés.

## 3. REMPLACER LE VOCABULAIRE POKÉMON DANS LE JEU

Je souhaite que toutes les mentions de Pokémon disparaissent des textes visibles dans le jeu.

Le joueur doit évoluer dans un univers entièrement centré sur les Yo-kai.

Adapter notamment :

- Pokémon → Yo-kai.
- Pokédex → Médallium.
- Poké Ball → Yo-kai Ball.
- Centre Pokémon → Centre Yo-kai.
- Ligue Pokémon → Ligue Yo-kai.
- Dresseur Pokémon → Dresseur de Yo-kai.
- Pokémon sauvage → Yo-kai sauvage.
- Boîtes Pokémon → Boîtes Yo-kai.
- Système de stockage Pokémon → Système de stockage Yo-kai.

Conserver les mécaniques des Balls et leur fonctionnement d'origine. Il s'agit de les adapter au vocabulaire et à l'univers.

La modification doit concerner les menus, dialogues, objets, descriptions, combats, lieux, tutoriels et autres textes réellement visibles par le joueur.

Adapter les phrases naturellement en français.

**Important : ne pas effectuer de remplacement aveugle dans les identifiants techniques du moteur.**

Les constantes, fonctions et fichiers internes peuvent conserver les noms Pokémon nécessaires au fonctionnement du jeu.

Le nom public de mon projet reste Pokémon × Yo-kai Watch ; cette consigne concerne l'univers affiché dans le jeu.

## 4. NOUVEAU RÔLE DE LÉO

Léo reste le scientifique rencontré dans sa maison sur la Route 25.

Dans notre univers, il est **l'inventeur du système PC et des Boîtes Yo-kai**.

Son invention permet de stocker les Yo-kai capturés lorsque l'équipe du joueur est complète.

L'événement original dans lequel Léo s'est accidentellement transformé en Pokémon doit être adapté.

Désormais, son expérience scientifique l'a transformé en **un Yo-kai parmi les 151 espèces intégrées**.

Tu peux choisir librement lequel, en privilégiant un résultat amusant, reconnaissable et adapté au sprite existant.

Évite les Yo-kai légendaires, les boss secrets et les rencontres dont on souhaite préserver la découverte.

Le joueur doit pouvoir aider Léo à retrouver sa forme humaine, comme dans l'événement original.

Adapter les sprites et les dialogues en conséquence.

Ne crée pas inutilement de nouvelles mécaniques : conserve le déroulement fonctionnel de la séquence originale.

## 5. DISTINCTION DÉFINITIVE : SEIGNEUR ENMA ET ENMA

**Attention : il existe deux représentations distinctes d'Enma dans notre jeu. Il ne faut jamais les confondre.**

### Seigneur Enma — Le personnage

Le Seigneur Enma est un personnage spécial que le joueur peut rencontrer et défier au Mont Braise après la Ligue.

Il possède :

- Un sprite de PNJ.
- Un portrait de dresseur.
- Des dialogues personnalisés.
- Une équipe de six Yo-kai.
- Un combat facultatif.
- Des revanches prévues par l'événement existant.

C'est un personnage bienveillant, fier, joueur et très puissant, qui veille à l'équilibre entre les humains et les Yo-kai.

### Enma — Le Yo-kai céleste capturable

Le Yo-kai nommé Enma, présent dans les 151 espèces, possède une origine différente.

**Il s'agit d'un Yo-kai céleste artificiel, créé lors d'une expérience visant à reproduire la puissance du Seigneur Enma à partir d'un Jibanyan.**

Cette expérience a produit une créature d'une puissance exceptionnelle.

Mais Enma s'est échappé du laboratoire dans lequel il avait été créé.

Il a finalement trouvé refuge auprès du véritable Seigneur Enma.

Celui-ci l'a accueilli et pris sous sa protection.

C'est pourquoi **le Seigneur Enma possède le Yo-kai Enma dans son équipe de six**.

Il ne s'agit pas du Seigneur Enma lui-même participant au combat en tant que créature.

Le Yo-kai Enma est une entité distincte.

### Nouveaux dialogues du Seigneur Enma

Lors de sa rencontre au Mont Braise, le Seigneur Enma doit progressivement révéler l'origine de son protégé.

Il explique que des scientifiques ont tenté de reproduire sa puissance et que leur création s'est échappée avant de trouver refuge auprès de lui.

Le dialogue doit conserver sa personnalité : chaleureux, assuré, parfois amusé, mais capable d'être sérieux lorsque la situation l'exige.

Évite d'en faire un monarque froid ou arrogant.

### Après sa défaite

Le Seigneur Enma doit être sincèrement impressionné et fier du protagoniste.

Il félicite le joueur pour sa progression, ses liens avec les Yo-kai et sa victoire.

Il explique ensuite que l'équilibre entre le monde humain et celui des Yo-kai est précieux et parfois fragile.

**Il affirme qu'il compte beaucoup sur le joueur pour contribuer à préserver cet équilibre.**

Il révèle enfin que son protégé, le Yo-kai Enma, se trouve désormais dans les profondeurs de la Caverne Azurée.

La victoire contre le Seigneur Enma débloque donc sa rencontre statique.

Le joueur doit ensuite se rendre dans la Caverne Azurée pour rencontrer et capturer le Yo-kai Enma.

**La victoire contre le Seigneur Enma ne doit pas automatiquement donner Enma au joueur ni enregistrer sa capture dans le Médallium.**

Conserve les scripts existants de déblocage, de sauvegarde, de combat et de capture unique, en les adaptant à cette nouvelle histoire.

Ne crée pas une seconde rencontre capturable.

Enfin, le PNJ Seigneur Enma et la créature Enma doivent utiliser leurs représentations graphiques appropriées, sans confusion.

## 6. GRAPHISMES DES YO-KAI STATIQUES

Vérifie les graphismes overworld des cinq espèces concernées par les rencontres statiques principales :

- Misterre, qui remplace Ronflex sur les Routes 12 et 16.
- Mademoaiselle, qui remplace Artikodin aux Îles Écume.
- Octorgone, qui remplace Électhor à la Centrale.
- Kyubi, qui remplace Sulfura au Mont Braise.
- Enma, le Yo-kai capturable dans la Caverne Azurée.

Chacune doit apparaître sous sa véritable apparence Yo-kai directement sur la carte.

Il ne doit plus rester de représentation de Ronflex, Artikodin, Électhor, Sulfura ou Mewtwo à ces emplacements.

Les sprites doivent respecter les limites graphiques GBA et rester reconnaissables.

Si Kyubi possède déjà son sprite spécifique, conserve-le s'il fonctionne.

Attention à bien distinguer le sprite du Seigneur Enma, personnage au Mont Braise, et le sprite de l'espèce Enma dans la Caverne Azurée.

## 7. NOUVELLE INTRODUCTION DU JEU

Je souhaite également personnaliser davantage l'introduction de Pokémon Rouge Feu.

Tu as deux directions artistiques possibles.

### Option A — Combat entre deux Yo-kai

Conserver la structure de l'introduction originale avec son affrontement entre Nidoran et Ectoplasma, mais remplacer ces deux créatures par deux Yo-kai.

Choisis deux Yo-kai visuellement impressionnants, reconnaissables et complémentaires.

**Ne choisis pas Enma, Kyubi, Octorgone ou une grande rencontre légendaire que le joueur doit découvrir plus tard.**

Il faut préserver le mystère autour des créatures exceptionnelles.

Privilégie des Yo-kai rencontrables normalement pendant l'aventure.

Adapter les sprites et, si possible, les mouvements de la séquence pour que l'affrontement paraisse naturel.

### Option B — Introduction originale inspirée de Yo-kai Watch : Le Film

Si tu te sens inspiré et si les contraintes techniques le permettent, je préférerais une introduction totalement différente.

Je souhaite retrouver l'ambiance d'une scène de Yo-kai Watch : Le Film, dans laquelle des Yo-kai normalement invisibles sont suggérés dans l'obscurité.

L'idée serait de montrer :

- Une atmosphère mystérieuse.
- Des décors sombres ou une forêt.
- Des silhouettes cachées.
- Plusieurs paires d'yeux très brillants.
- Quelques apparitions furtives de Yo-kai.
- Une présentation de leur présence invisible dans le monde des humains.
- Une transition vers la Yo-kai Watch ou le titre du jeu.

**Cette mise en scène doit susciter la curiosité sans révéler les Yo-kai les plus rares.**

La référence musicale est :

**« 0. The Very Curious Yo-kai Watch » — Yo-kai Watch 2 OST.**

Si le morceau est disponible dans les fichiers audio privés retrouvés, étudie son intégration pour cette séquence avec la méthode musicale validée.

La narration doit expliquer, avec une formulation originale, que les Yo-kai vivent autour des humains mais qu'une Yo-kai Watch permet de les voir.

Le texte peut être intégré à l'écran si une véritable voix off est techniquement disproportionnée.

Je te laisse une réelle liberté artistique pour imaginer une introduction agréable et marquante.

**Toutefois, ne laisse pas cette cinématique bloquer la finalisation du jeu.**

Si une introduction entièrement originale demande trop de modifications risquées ou de temps, choisis l'option A et livre une séquence propre et fonctionnelle.

Ne remplace pas un système stable par une cinématique expérimentale non vérifiée.

## 8. PRIORITÉ AUX MUSIQUES YO-KAI WATCH

Les musiques sont désormais prioritaires sur les nouvelles quêtes secondaires.

Je souhaite conserver l'objectif des 20 OST précédemment sélectionnées et leurs affectations validées.

Utilise la méthode B en DPCM, déjà choisie pour obtenir une restitution proche des enregistrements d'origine avec une sonorité GBA.

Prête une attention particulière :

- Aux boucles musicales.
- Aux introductions qui ne doivent jouer qu'une seule fois.
- Aux transitions entre exploration et combat.
- Aux bruitages du jeu.
- À l'espace disponible dans la ROM.
- À la fluidité dans mGBA.
- À la fidélité des morceaux.
- À l'absence de bugs audio ou de plantages.

La nouvelle référence musicale de l'introduction, « The Very Curious Yo-kai Watch », est une proposition supplémentaire. Elle ne doit pas remplacer arbitrairement une des vingt musiques déjà validées.

Si l'espace ou le temps ne permet pas de toutes les intégrer correctement, privilégie les musiques les plus importantes pour l'aventure, puis documente les morceaux restants.

Ne supprime pas arbitrairement « Somewhere A Bit Dodgy », que je souhaite conserver pour le Repaire Rocket.

Les enregistrements protégés doivent rester privés : ne les publie pas sur le dépôt GitHub public et ne distribue aucune ROM.

## 9. QUÊTES SECONDAIRES : DERNIÈRE PRIORITÉ

Les dix quêtes imaginées précédemment deviennent facultatives pour la première version finalisée.

Ne consacre pas les prochaines sessions à leur implémentation tant que l'aventure principale, les musiques, les graphismes essentiels et les contrôles de stabilité ne sont pas suffisamment avancés.

Les événements déjà développés, comme le combat contre Seigneur Enma, doivent être conservés.

Une fois le jeu stable, tu pourras intégrer progressivement certaines quêtes si le temps le permet.

Évite particulièrement de bloquer la sortie du jeu sur des fonctionnalités complexes et indépendantes, comme le combat contre Red avec de véritables Pokémon supplémentaires.

## 10. SAUVEGARDES, TESTS ET AUTONOMIE

Continue de travailler sur `dev/reconstruction-finalisation`.

Avant toute modification, vérifie le dernier commit et les éventuels changements locaux pour éviter une régression.

Sauvegarde régulièrement sur GitHub les fonctionnalités terminées et testées.

Préserve `master` et les branches de récupération.

Compile après les modifications importantes, exécute les tests mGBA et vérifie la reproductibilité depuis un clone GitHub propre.

Teste particulièrement :

- La progression jusqu'à la Ligue.
- Les personnages et événements obligatoires.
- Les rencontres statiques.
- L'obtention des 151 Yo-kai.
- La sauvegarde et le rechargement.
- Les musiques et les transitions sonores.
- Le vocabulaire français.
- L'introduction et les sprites.
- L'accès au postgame.

Les tests automatisés ciblés ne remplacent pas une vérification de l'aventure complète.

**Ne me demande pas une validation après chaque étape.**

Tu peux prendre des décisions techniques secondaires cohérentes avec les choix ci-dessus.

En cas de difficulté, privilégie une solution simple, stable et reproductible plutôt qu'une fonctionnalité spectaculaire qui retarderait tout le jeu.

Si tu atteins une limite de session, sauvegarde les modifications fonctionnelles et fournis un résumé honnête des éléments terminés, restants et testés.

## OBJECTIF FINAL

Je veux désormais que tu consacres tes efforts à **terminer réellement Pokémon × Yo-kai Watch**.

Je souhaite une aventure qui donne l'impression d'appartenir à l'univers Yo-kai Watch grâce à ses personnages, son histoire, son vocabulaire, ses musiques et ses créatures.

Le but n'est pas de multiplier indéfiniment les nouveautés.

**Le but est d'obtenir un jeu complet, cohérent, jouable, stable et prêt pour mes tournages.**

Reprends le développement immédiatement, en commençant par vérifier l'état actuel du dépôt et en poursuivant les tâches prioritaires encore incomplètes.