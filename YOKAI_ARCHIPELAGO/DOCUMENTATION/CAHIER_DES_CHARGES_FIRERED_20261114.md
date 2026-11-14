# CODEX — POKÉMON ROUGE FEU × YO-KAI WATCH
## Développement du mode Archipelago — Cahier des charges complet

### CONTEXTE DU PROJET

Nous développons un Multiworld Archipelago réunissant cinq créateurs, chacun jouant à un jeu différent :

1. **Yo-kai Watch 1 (3DS européen)** — Yochix.
2. **Yo-kai Watch 2 : Spectres Psychiques (3DS)** — Juste Yoann.
3. **Pokémon Rouge Feu × Yo-kai Watch (GBA)** — Kammy64 ou Petit Shiny.
4. **Mario Kart Wii × Yo-kai Watch (Wii)** — Krackonyx.
5. **Pokémon Yo-kai Emerald (GBA)** — Dejais.

Le but est de terminer collectivement les cinq objectifs principaux grâce à des objets et déblocages répartis entre les jeux.

Nous avons défini une difficulté **équilibrée, avec autonomie maximale et attente limitée**.

Je souhaite maintenant que tu poursuives en priorité l'intégration Archipelago de mon fangame Pokémon Rouge Feu × Yo-kai Watch.

---

# PHASE 1 — CONSERVER ET SÉCURISER LES AVANCÉES EXISTANTES

Tu as précédemment annoncé avoir réussi les premiers tests suivants :

- Compilation et démarrage dans mGBA.
- Connexion à un véritable serveur Archipelago.
- Réception d'une Potion dans le sac.
- Absence de doublon après reconnexion.
- Persistance des données après sauvegarde et redémarrage.
- Détection du premier badge après un combat contre Wyatt et transmission du check au serveur.

Commence par vérifier que ces fonctionnalités sont toujours opérationnelles sur la branche de développement actuelle.

### Sécurité des sauvegardes

Mon fangame comporte de nombreuses fonctionnalités personnalisées, notamment Aspirateur, Blasters, des événements scénaristiques et des systèmes spécifiques aux Yo-kai.

Tu as identifié des zones de sauvegarde déjà utilisées par certaines de ces fonctionnalités.

Je veux donc que tu :

1. Audites précisément les données de sauvegarde existantes.
2. Réserves un espace sûr aux données Archipelago.
3. Vérifies l'absence de chevauchement avec les systèmes personnalisés.
4. Garantisses la persistance des checks envoyés et des objets reçus.
5. Empêches la duplication des récompenses après reconnexion.
6. Prévoies une gestion sûre des objets reçus lorsque le sac est plein.
7. Vérifies les sauvegardes après fermeture et redémarrage de l'émulateur.

Ne considère aucune protection comme validée sans test correspondant.

### Protection du fangame original

Le mode Archipelago doit être développé séparément.

- Ne modifie pas la branche originale.
- Ne supprime aucune fonctionnalité.
- Ne réécris pas le scénario.
- Ne modifie pas les statistiques, talents, types ou évolutions des Yo-kai sans nécessité technique.
- Conserve les cinématiques, cartes, dialogues et événements personnalisés.

Travaille sur une branche dédiée à Archipelago, créée depuis la véritable branche contenant mon fangame complet, et non depuis une base Pokémon Rouge Feu vanilla.

---

# PHASE 2 — DÉFINIR LA CONDITION DE VICTOIRE

### Objectif du joueur Rouge Feu

**Vaincre le dernier adversaire de la Ligue et entrer au Panthéon.**

La victoire doit être détectée automatiquement et envoyée au serveur Archipelago sous forme de condition `Goal`.

### Le postgame est exclu

Notre vidéo ne consiste pas à terminer les jeux à 100 %.

Pour Pokémon Rouge Feu × Yo-kai Watch :

- Pas besoin de compléter le Médallium.
- Pas besoin d'explorer les Limbes Éternelles.
- Pas besoin de vaincre Soranaki.
- Pas besoin de terminer les quêtes postgame.
- Pas besoin de capturer tous les Yo-kai.

Ces contenus doivent rester présents et fonctionnels dans le fangame original.

En revanche, **ils ne doivent pas faire partie des checks de notre première version Archipelago**.

Aucun objet indispensable à la progression d'un des cinq joueurs ne doit être placé après la condition de victoire d'un autre joueur.

La victoire doit correspondre au véritable événement de fin de la Ligue de mon fangame, et pas à une hypothèse fondée uniquement sur Pokémon Rouge Feu vanilla.

---

# PHASE 3 — INVENTORIER LES CHECKS ARCHIPELAGO

Je souhaite un inventaire aussi complet que raisonnable des emplacements accessibles avant la fin de l'histoire principale.

### A. Objets ordinaires

Inclure notamment :

- Poké Balls contenant des objets au sol.
- Objets cachés, si leur détection est fiable.
- Objets offerts par les PNJ.
- Récompenses ordinaires.
- Objets récupérables dans les bâtiments et donjons.

Une simple Poké Ball ramassée sur la Route 2 doit pouvoir constituer un check Archipelago.

### B. Événements importants

Étudier :

- Les huit badges.
- Les récompenses des Champions.
- Les événements majeurs du scénario.
- Les objets clés.
- Les récompenses de certaines quêtes.
- Les événements personnalisés du fangame.

### C. Contenu secondaire avant la Ligue

Autoriser les checks facultatifs accessibles avant la victoire :

- Quêtes secondaires.
- Exploration facultative.
- Récompenses de PNJ.
- Zones annexes accessibles avant la Ligue.

Attention : un emplacement facultatif peut contenir un objet indispensable à un autre joueur.

### D. Exclusions

Exclure :

- Les checks accessibles uniquement après la victoire.
- Les événements impossibles à détecter de manière fiable.
- Les récompenses dont la modification provoquerait un blocage scénaristique.
- Les éléments techniques internes au fangame.

### Pour chaque check

Documente :

1. Son identifiant Archipelago unique.
2. Son nom français.
3. Sa localisation.
4. Sa condition de validation.
5. Son emplacement dans le code source.
6. Les prérequis nécessaires pour l'atteindre.
7. Son caractère obligatoire ou facultatif.
8. Les risques techniques éventuels.

Ne te limite surtout pas aux badges et aux grands événements.

---

# PHASE 4 — RANDOMISATION DES RÉCOMPENSES

C'est une priorité majeure.

Je veux retrouver le fonctionnement d'un véritable Archipelago.

### Principe fondamental

**N'importe quel check éligible peut contenir une récompense importante ou secondaire, sous réserve de la logique de progression.**

Par exemple :

- Une Poké Ball sur une route peut envoyer une CS indispensable à Dejais.
- Un Champion peut envoyer une Potion à Yochix.
- Une quête secondaire peut débloquer une coupe pour Krackonyx.
- Un objet ordinaire peut envoyer un objet clé à Juste Yoann.

Ces exemples illustrent le comportement souhaité, sans imposer de placements fixes.

Ne réserve pas les objets importants aux événements importants.

### Classification des récompenses

Distingue :

**Objets de progression**
- CS indispensables.
- Objets clés nécessaires à l'aventure.
- Déblocages de zones.
- Autres éléments indispensables à la condition de victoire.

**Objets utiles**
- CT.
- Objets de soin.
- Objets de combat.
- Récompenses facultatives.

**Objets secondaires**
- Consommables ordinaires.
- Récompenses de faible importance.

**Objets exclus**
- Données techniques.
- Objets nécessaires au fonctionnement interne des scripts.
- Éléments dont la randomisation casserait le scénario.

### Règle importante

La randomisation ne doit pas simplement ajouter des récompenses Archipelago en plus des récompenses originales lorsque cela rendrait le système incohérent.

Pour chaque emplacement, détermine si la récompense originale doit être remplacée, conservée ou gérée séparément.

En particulier, évite qu'un objet de progression randomisé soit également obtenu gratuitement à son emplacement original.

Si un objet clé est indispensable à une cinématique, étudie comment préserver cette cinématique sans créer de blocage.

---

# PHASE 5 — DIFFICULTÉ ÉQUILIBRÉE ET AUTONOMIE MAXIMALE

Nous avons validé les règles suivantes.

### 1. Chaque joueur doit pouvoir commencer à jouer

Pour Rouge Feu, vise environ **10 checks accessibles dès le départ**, lorsque la structure du jeu le permet.

Ce nombre est une cible d'équilibrage, pas une obligation absolue.

Ne crée pas artificiellement des événements inutiles pour atteindre ce chiffre.

### 2. Favoriser plusieurs chemins de progression

Je souhaite éviter qu'un joueur dépende systématiquement d'un seul objet pour accomplir quoi que ce soit.

Lorsque c'est possible, privilégie :

- Plusieurs zones accessibles.
- Plusieurs checks disponibles simultanément.
- Des quêtes secondaires réalisables.
- Des possibilités d'exploration avant les prochains déblocages majeurs.

### 3. Les blocages temporaires sont autorisés

Un joueur peut être bloqué parce qu'il attend un objet provenant d'un autre jeu.

C'est normal et même souhaitable dans Archipelago.

En revanche, nous voulons limiter au maximum les situations où un joueur ne peut plus effectuer aucun check pendant une longue période.

### 4. Aucun blocage définitif

Une seed correctement générée doit permettre d'atteindre les cinq conditions de victoire.

Exemples interdits :

- Surf placé derrière une zone nécessitant Surf.
- Un objet indispensable au début d'Émeraude placé dans le postgame de Yo-kai Watch 2.
- Deux objets indispensables placés derrière des accès nécessitant réciproquement ces mêmes objets.
- Une progression nécessitant un check impossible à déclencher.

Utilise les mécanismes de logique et de génération d'Archipelago pour empêcher ces situations.

---

# PHASE 6 — ANALYSE DES SPHÈRES DE PROGRESSION

Je souhaite que tu exploites les sphères de progression d'Archipelago pour évaluer les seeds.

Pour chaque seed testée, analyse notamment :

- Le nombre de checks accessibles initialement dans chaque jeu.
- Les nouvelles possibilités ouvertes après réception des objets importants.
- Les dépendances entre les cinq jeux.
- Les joueurs qui restent plusieurs sphères sans nouvelle possibilité de progression.
- Les objets de progression concentrés très tardivement.
- Les dépendances excessives envers un seul joueur.

Si possible, produis un rapport d'équilibrage.

Ne confonds pas le nombre de sphères avec une durée réelle de jeu : une sphère peut prendre quelques minutes ou plusieurs heures.

### Paramètres recommandés

- `progression_balancing` : cible initiale de 65 %, à adapter aux valeurs et fonctionnalités réellement prises en charge.
- `accessibility` : `full`, si compatible.
- Aucun piège pour la première version.
- Placement libre des récompenses sous contraintes de logique.
- Aucun check postgame.
- Priorité à l'autonomie des joueurs.

Ne considère pas ces paramètres comme suffisants à eux seuls pour garantir une seed équilibrée.

---

# PHASE 7 — SYSTÈME D'INDICES ET ATTENTE LIMITÉE

Nous avons validé une règle supplémentaire pour la vidéo.

**Après 20 minutes de blocage réel, un joueur peut demander un indice Archipelago.**

Un blocage réel signifie que le joueur ne peut plus poursuivre son objectif principal et n'a plus de checks raisonnablement accessibles à effectuer, ou a épuisé les pistes connues.

### Fonctionnement souhaité

1. Le joueur constate son blocage.
2. Après 20 minutes, il peut demander un indice sur un objet de progression.
3. L'indice aide à identifier l'emplacement de cet objet.
4. Les autres joueurs peuvent coopérer pour le récupérer.

Utilise prioritairement le système d'indices natif d'Archipelago.

Ce délai est une règle d'organisation du tournage, pas nécessairement une fonctionnalité à programmer dans la ROM.

### Procédure de secours

Si le blocage persiste :

- Après environ 30 minutes, les joueurs peuvent faire un point collectif sur leurs checks et objectifs.
- Après environ 45 minutes, un organisateur peut consulter le spoiler log pour fournir une indication ciblée.

L'organisateur ne doit pas dévoiler toute la seed.

Cette procédure est une protection contre les longues périodes d'inactivité, pas un moyen de supprimer la difficulté.

---

# PHASE 8 — TESTS DE GÉNÉRATION ET DE PROGRESSION

Je veux une validation rigoureuse, mais pas de longues sessions automatisées destinées à terminer le jeu.

### Tests demandés

1. Compiler le jeu.
2. Vérifier son démarrage dans mGBA.
3. Générer plusieurs seeds Archipelago.
4. Vérifier les conditions de victoire.
5. Tester les dépendances d'objets.
6. Analyser les sphères de progression.
7. Vérifier que les objets importants ne peuvent pas être placés dans le postgame.
8. Tester les objets ordinaires comme checks.
9. Tester les badges et les événements importants.
10. Tester l'envoi et la réception d'objets avec un véritable serveur.
11. Tester la sauvegarde et la reconnexion.
12. Tester les situations de sac plein et de réception différée.
13. Vérifier qu'aucun check ne peut être envoyé plusieurs fois de manière incorrecte.

### Tests de robustesse

Effectue des générations répétées de seeds avec des paramètres variés.

Si une seed échoue, identifie la cause et corrige la logique plutôt que de masquer le problème.

Les tests statiques ne remplacent pas les tests réels dans l'émulateur.

N'affirme pas que toutes les parties sont garanties sans bug uniquement parce que plusieurs seeds ont été générées avec succès.

---

# PHASE 9 — INTÉGRATION AU MULTIWORLD À CINQ JEUX

Notre objectif final est de réunir les cinq jeux dans une même session Archipelago.

Pour Rouge Feu :

- Respecte les conventions APWorld.
- Utilise des identifiants d'objets et de locations stables.
- Assure la compatibilité avec les mécanismes de génération Multiworld.
- Prévois les objets envoyés depuis les autres jeux.
- Vérifie la gestion des objets reçus lorsque le jeu n'est pas dans un état permettant leur distribution immédiate.

Ne suppose pas que les quatre autres intégrations sont déjà entièrement fonctionnelles.

Pokémon Yo-kai Emerald reste dépendant des fichiers privés nécessaires à la reprise de son développement.

---

# PHASE 10 — DOCUMENTATION ET LIVRABLES

Je veux pouvoir suivre précisément l'avancement.

Documente :

- La branche GitHub utilisée.
- Les commits réalisés.
- Les fichiers modifiés.
- La liste des checks.
- La liste des objets Archipelago.
- Les règles de progression.
- La condition de victoire.
- Les tests effectués et leurs résultats.
- Les bugs connus.
- Les fonctionnalités encore manquantes.

Prépare également les instructions permettant de lancer la version Archipelago dans mGBA et de la connecter à un serveur.

Ne publie pas de ROM commerciale, de BIOS ou de fichiers propriétaires non autorisés.

---

# PRIORITÉS IMMÉDIATES

Travaille dans cet ordre :

**Priorité 1 :** sécuriser les sauvegardes et confirmer les premiers échanges réseau.

**Priorité 2 :** inventorier les checks accessibles avant la Ligue.

**Priorité 3 :** définir précisément les objets de progression et leurs conditions d'utilisation.

**Priorité 4 :** implémenter une première randomisation réelle, incluant les objets ordinaires.

**Priorité 5 :** vérifier les conditions de victoire et les dépendances.

**Priorité 6 :** analyser et améliorer l'autonomie du joueur.

**Priorité 7 :** tester les échanges avec un serveur Archipelago et préparer l'intégration Multiworld.

Tu peux avancer de manière autonome sur les décisions purement techniques.

En revanche, demande mon avis avant toute modification importante du scénario, des règles de progression originales ou de l'équilibrage du fangame.

## OBJECTIF FINAL

Je veux que Pokémon Rouge Feu × Yo-kai Watch soit une véritable aventure Archipelago :

- Où une simple Poké Ball peut contenir un objet indispensable.
- Où les cinq joueurs dépendent les uns des autres.
- Où chacun conserve un maximum d'autonomie.
- Où les blocages temporaires créent des interactions.
- Où les blocages définitifs sont empêchés par une logique correcte.
- Où aucun joueur n'est obligé de terminer le postgame.
- Où la victoire correspond à la fin de l'histoire principale.
- Où le fangame original reste intact.

**Commence dès maintenant par les priorités 1 à 4, puis poursuis les autres phases selon les résultats. Ne te limite pas à rédiger de la documentation : implémente et teste réellement ce qui est possible dans ton environnement.**

À la fin, fournis un compte rendu clair distinguant les fonctionnalités implémentées, celles testées en conditions réelles et celles restant à développer.