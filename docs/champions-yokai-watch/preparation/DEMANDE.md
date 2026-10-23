# CODEX — REFONTE DES CHAMPIONS DE KANTO × YO-KAI WATCH

## 1. Mission

Dépôt : `JusteYoann/Pokemon-Yokai-Watch`

Nous souhaitons remplacer plusieurs Champions de Pokémon Rouge Feu par des personnages emblématiques de Yo-kai Watch, tout en conservant la progression des huit badges.

La branche `feature/lavanville-zombie-night` contient notre chapitre Lavanville terminé, avec Alyzon Bie, les zombies, la Tour Pokémon et les raccordements de Céladopole.

**Commence par auditer les branches et les ressources existantes avant toute modification.**

Crée une branche dédiée à cette refonte à partir de la version validée la plus récente contenant Lavanville et les autres fonctionnalités approuvées.

Nom suggéré :

`feature/champions-yokai-watch`

Ne fusionne rien sur `master`.

Ne modifie pas les 151 espèces de Yo-kai existantes, leurs types, leurs évolutions ou leurs statistiques.

Conserve les événements déjà intégrés, les musiques, les scripts de progression et la finale Don Morléone / Don Spiraton.

---

# 2. NOUVELLE COMPOSITION DES HUIT CHAMPIONS

| Badge | Champion actuel | Nouveau Champion | Spécialité |
|---|---|---|---|
| 1 — Roche | Pierre | Wyatt | Roche |
| 2 — Cascade | Ondine | Katie ou Nathan | Normal |
| 3 — Foudre | Major Bob | Ariane Célestin | Électrik |
| 4 — Prisme | Alyzon Bie | Alyzon Bie | Spectre / Zombies |
| 5 — Âme | Koga | Koga | Poison |
| 6 — Marais | Morgane | Bérénice Bélier | Psy |
| 7 — Volcan | Auguste | Nathaniel ou Michael | Yo-kai du passé |
| 8 — Terre | Don Morléone | Don Morléone | Sol |

Les badges, leurs positions, leurs effets et leurs conditions de progression ne doivent pas changer.

Koga et Don Morléone restent inchangés.

---

# 3. WYATT — PREMIER CHAMPION

Wyatt remplace Pierre à Argenta.

Il devient le Champion spécialisé dans le type Roche.

## Équipe

**Conserve exactement l'équipe actuellement utilisée par Pierre dans notre ROM hack.**

Cela inclut :

- Les Yo-kai.
- Les niveaux.
- Les attaques.
- Les objets éventuels.
- L'ordre d'envoi.

Ne recrée pas une équipe de Pokémon Roche classique.

Ne modifie pas l'équilibrage de cette première Arène.

## Intégration

Remplace :

- Sprite overworld de Pierre.
- Portrait de combat.
- Nom de Champion.
- Dialogues.
- Références au Champion dans les événements concernés.

Adapte les dialogues à Wyatt, sans modifier le fonctionnement de l'Arène.

Conserve le Badge Roche et sa récompense.

---

# 4. KATIE / NATHAN — DEUXIÈME CHAMPION

Ondine est remplacée par un personnage différent selon le sexe du joueur.

### Joueur masculin

La Championne est **Katie**.

### Joueuse féminine

Le Champion est **Nathan**.

Cette règle est obligatoire et doit être appliquée aux sprites, portraits, noms et dialogues.

## Spécialité

L'Arène d'Azuria devient une Arène de type **Normal**.

Le badge reste le Badge Cascade.

L'équipe doit être composée principalement de Yo-kai de type Normal.

### Yo-kai signature

**Jibanyan est obligatoirement le dernier adversaire.**

Il conserve son type réel dans notre ROM, même s'il n'est pas Normal.

Ne modifie pas ses données pour l'adapter à la spécialité de l'Arène.

## Équilibrage

Construis une proposition d'équipe adaptée au deuxième badge.

Utilise exclusivement les Yo-kai déjà présents dans la ROM.

Conserve autant que possible une difficulté comparable à l'équipe actuelle d'Ondine.

Ne valide pas arbitrairement une nouvelle composition sans la présenter dans ton rapport.

---

# 5. ARIANE CÉLESTIN — TROISIÈME CHAMPIONNE

Ariane Célestin remplace Major Bob à Carmin-sur-Mer.

Elle devient la Championne spécialisée dans le type **Électrik**.

## Équipe

Son équipe doit être composée principalement de Yo-kai de type Électrik.

### Yo-kai signature

**Usapion est obligatoirement son dernier Yo-kai.**

Il conserve son type réel dans notre ROM.

Conserve un nombre d'adversaires et une difficulté adaptés au troisième badge.

Tu peux partir de l'équipe actuelle de Major Bob et la modifier si nécessaire.

Ne modifie pas les statistiques ou les types des Yo-kai.

## Intégration

Remplace :

- Sprite overworld.
- Portrait de Championne.
- Nom affiché.
- Dialogues.
- Équipe.

Conserve :

- Badge Foudre.
- Récompense.
- Énigme des interrupteurs.
- Fonctionnement général de l'Arène.

---

# 6. ALYZON BIE — MODIFICATION DE SON ÉQUIPE

Alyzon Bie est déjà intégrée dans notre chapitre Lavanville.

**Ne recommence pas son intégration.**

Conserve :

- Ses sprites validés.
- Son portrait.
- Ses dialogues.
- La cinématique de Lavanville.
- La Tour Pokémon.
- Les zombies errants.
- Les zombies Dresseurs.
- La nuit et la brume.
- Le Badge Prisme.
- Les raccordements avec Céladopole.

Nous souhaitons uniquement modifier son dernier adversaire.

## Ancienne équipe

| Ordre | Yo-kai | Niveau |
|---|---|---|
| 1 | Potofeu | 27 |
| 2 | Whisper | 28 |
| 3 | Triptic-tac | 29 |
| 4 | Mémogre | 31 |

## Nouvelle équipe définitive

| Ordre | Adversaire | Niveau |
|---|---|---|
| 1 | Potofeu | 27 |
| 2 | Whisper | 28 |
| 3 | Triptic-tac | 29 |
| 4 | **Zombie Colosse** | **31** |

Le Zombie Colosse devient le nouvel adversaire signature d'Alyzon Bie.

Mémogre est retiré de son équipe de Championne.

## Intégration du Zombie Colosse

Le Zombie Colosse existe déjà dans les combats spéciaux de Lavanville.

Réutilise son sprite de combat validé et son identité visuelle.

Il ne doit pas être ajouté aux 151 espèces capturables.

Le combat contre Alyzon doit continuer à fonctionner comme un combat de Championne classique.

Le Zombie Colosse doit :

- Être envoyé en quatrième position.
- Être de niveau 31.
- Posséder des statistiques et des attaques adaptées au combat.
- Ne pas pouvoir être capturé.
- Donner lieu à une victoire normale lorsqu'il est vaincu.
- Ne pas casser la remise du badge.

**Attention : le système des zombies errants utilise actuellement des combats spéciaux distincts des combats de Dresseurs.**

Audite cette architecture avant de modifier l'équipe d'Alyzon.

Ne remplace pas silencieusement l'un des 151 Yo-kai dans les données globales.

Ne modifie pas les combats des zombies errants.

Si le moteur nécessite une représentation spéciale du Zombie Colosse au sein d'une équipe de Dresseur, implémente une solution propre, isolée et compatible avec les sauvegardes.

## Dialogue spécial

Lorsque le Zombie Colosse entre en combat, Alyzon Bie peut prononcer :

« Et maintenant, je vais te présenter mon petit préféré ! Hihi ! »

Ce dialogue doit être adapté à la largeur des boîtes de texte GBA.

Il ne doit apparaître qu'une seule fois pendant le combat, au moment de l'envoi du Zombie Colosse.

---

# 7. BÉRÉNICE BÉLIER — SIXIÈME CHAMPIONNE

Bérénice Bélier remplace Morgane à Safrania.

Elle devient la Championne spécialisée dans le type **Psy**.

## Équipe

Conserve une équipe composée de Yo-kai de type Psy.

Pour cette première intégration, privilégie la conservation de l'équipe actuellement attribuée à Morgane dans notre ROM, sauf si un problème de cohérence ou de type est détecté.

Présente les membres et les niveaux réels de l'équipe.

Ne change pas les types des Yo-kai.

## Intégration

Remplace :

- Sprite overworld.
- Portrait.
- Nom de Championne.
- Dialogues.

Conserve :

- Badge Marais.
- Récompense.
- Téléporteurs de l'Arène.
- Événements existants.
- Conditions de progression.

---

# 8. NATHANIEL / MICHAEL — SEPTIÈME CHAMPION

Auguste est remplacé par un personnage différent selon le sexe du joueur.

### Joueur masculin

Le Champion est **Nathaniel**.

### Joueuse féminine

Le Champion est **Michael**.

Les deux personnages partagent la même équipe.

## Nouvelle spécialité

L'Arène de Cramois'Île n'est plus spécialisée dans le type Feu.

Elle devient une Arène consacrée aux **Yo-kai du passé**.

C'est une équipe thématique, pas une équipe monotype.

Les types réels des Yo-kai sont conservés.

## Équipe obligatoire

| Ordre | Yo-kai |
|---|---|
| 1 | Métaurolog |
| 2 | Sirénité |
| 3 | Sal de bain |
| 4 | Brumella |
| 5 | Faux Kappa |
| 6 | **Hovernyan** |

**Hovernyan est le Yo-kai signature et doit être envoyé en dernier.**

Conserve les six membres exactement.

Ne remplace aucun Yo-kai par une évolution sans validation.

## Niveaux

Propose des niveaux adaptés au septième badge et à la difficulté actuelle de notre ROM.

Vérifie leurs statistiques réelles, leurs attaques légales et leurs types.

Le dernier Hovernyan doit constituer le principal défi du combat.

## Intégration

Remplace :

- Sprite overworld.
- Portrait.
- Nom de Champion.
- Dialogues.
- Équipe.

Conserve :

- Badge Volcan.
- Récompense.
- Conditions de progression.
- Fonctionnement général de l'Arène.

Les dialogues doivent être adaptés à la personnalité de Nathaniel ou Michael.

---

# 9. SPRITES ET PORTRAITS

Avant de créer de nouveaux sprites, recherche dans toutes les branches du dépôt les ressources existantes des personnages suivants :

- Wyatt.
- Katie.
- Nathan.
- Ariane Célestin.
- Bérénice Bélier.
- Nathaniel.
- Michael.

Recherche également les variantes orthographiques et les noms de fichiers abrégés.

Certains personnages peuvent déjà posséder des sprites overworld ou des portraits créés dans des travaux précédents.

**Réutilise les sprites déjà validés lorsqu'ils existent.**

Ne remplace pas un sprite existant par une nouvelle génération automatique.

Si un personnage ne possède aucun sprite :

1. Identifie les ressources manquantes.
2. Prépare un emplacement d'intégration.
3. Signale les références nécessaires.
4. Ne substitue pas un personnage sans rapport.
5. Demande une validation artistique avant l'intégration définitive.

Les nouveaux sprites devront respecter le style graphique de Pokémon Rouge Feu / Vert Feuille.

---

# 10. CONDITIONS LIÉES AU SEXE DU JOUEUR

Deux Arènes disposent de variantes.

| Arène | Joueur garçon | Joueuse fille |
|---|---|---|
| Azuria | Katie | Nathan |
| Cramois'Île | Nathaniel | Michael |

Le moteur doit choisir automatiquement le bon personnage.

Le choix doit être cohérent dans :

- Les sprites overworld.
- Les portraits de combat.
- Les noms.
- Les dialogues.
- Les références aux Champions.

Les équipes et les récompenses sont identiques entre les deux variantes d'une même Arène.

Vérifie également les sauvegardes, les retours dans l'Arène et les éventuelles scènes utilisant les Champions.

---

# 11. PRÉSERVATION DES AUTRES CHAMPIONS

## Koga

Ne modifie pas Koga.

Il conserve :

- Son sprite.
- Son portrait.
- Ses dialogues.
- Son équipe Poison.
- Son badge.
- Son Arène.

## Don Morléone

Ne modifie pas Don Morléone.

Il conserve son rôle de huitième Champion, son équipe Sol, ses dialogues et ses événements.

La finale Don Morléone / Don Spiraton doit rester intacte.

---

# 12. AUDIT ET TESTS

Avant l'intégration, réalise un audit des cinq Arènes concernées et de l'équipe actuelle d'Alyzon.

Après les modifications, compile les versions publique et privée.

Teste dans mGBA :

- Wyatt avec l'équipe exacte de Pierre.
- Katie avec un joueur garçon.
- Nathan avec une joueuse fille.
- Ariane Célestin et son Usapion final.
- Alyzon Bie et son Zombie Colosse final.
- Bérénice Bélier.
- Nathaniel avec un joueur garçon.
- Michael avec une joueuse fille.
- Hovernyan envoyé en dernier.
- Les huit badges et leurs effets.
- Les récompenses.
- Les sauvegardes après chaque victoire.
- Les Arènes déjà terminées.
- Lavanville et la Tour Pokémon.
- La Flûte Yo-kai.
- Le repaire Mafiamille.
- Koga et Don Morléone inchangés.
- La finale Don Spiraton jusqu'au Panthéon.

Contrôle également :

- Les portraits et palettes.
- Les noms affichés.
- Les textes GBA.
- Les statistiques et attaques.
- La taille des ROM.
- Les limites EWRAM, IWRAM et VRAM.
- La préservation des 151 Yo-kai.
- La préservation des OST existantes.

---

# 13. MÉTHODE DE TRAVAIL ET LIVRABLES

Procède en deux étapes.

### Étape 1 — Audit et préparation

Présente :

1. Les sprites existants retrouvés.
2. Les sprites manquants.
3. Les équipes actuelles des Champions.
4. Les nouvelles équipes proposées pour Katie/Nathan et Ariane.
5. Les niveaux proposés pour Nathaniel/Michael.
6. La solution technique envisagée pour le Zombie Colosse d'Alyzon.
7. Les impacts éventuels sur les sauvegardes.
8. Les modifications nécessaires aux scripts.

**Attends mon accord sur les équipes proposées et sur les éventuels sprites manquants.**

### Étape 2 — Intégration et validation

Une fois les choix validés :

- Implémente les nouveaux Champions.
- Intègre les variantes garçon/fille.
- Modifie l'équipe d'Alyzon.
- Compile les deux ROM.
- Exécute les tests.
- Fournis les captures mGBA.
- Documente les modifications.
- Publie les commits sur la branche dédiée.

Ne fusionne rien sur `master`.

## Consigne finale

Je veux que les Arènes de Kanto ressemblent désormais à une véritable Ligue Yo-kai Watch.

Chaque Champion doit avoir une identité reconnaissable, des dialogues adaptés et une équipe cohérente avec son personnage.

**Ne recommence aucun travail déjà terminé et ne sacrifie aucune fonctionnalité existante pour intégrer ces changements.**