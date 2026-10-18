# SESSION 3/4 — REFONTE DE L'INTRODUCTION ET DE L'ÉCRAN TITRE

## CONTEXTE

Nous poursuivons la finalisation de mon ROM hack Pokémon Rouge Feu × Yo-kai Watch.

Dépôt : `JusteYoann/Pokemon-Yokai-Watch`

Branche : `dev/reconstruction-finalisation`

Cette session est consacrée à deux éléments essentiels :

1. Une véritable introduction cinématographique inspirée de Yo-kai Watch.
2. Un écran titre visuellement proche de l'identité des jeux Yo-kai Watch.

Une première version de ces éléments existe déjà dans le projet, mais je souhaite maintenant un résultat beaucoup plus travaillé et fidèle à ma direction artistique.

**IMPORTANT : les images jointes sont des références artistiques, pas nécessairement des ressources à intégrer telles quelles dans la ROM.**

Je fournirai un ZIP contenant les références visuelles de l'introduction et de l'écran titre.

Si le ZIP n'est pas encore joint, prépare d'abord les éléments techniques et le plan d'intégration, mais ne finalise pas de choix artistiques qui nécessitent ces références.

---

# PARTIE 1 — NOUVELLE INTRODUCTION CINÉMATOGRAPHIQUE

## 1. Direction artistique

Je souhaite une introduction inspirée de l'ambiance mystérieuse de l'ouverture du film Yo-kai Watch.

Mes références montrent notamment :

- Une forêt plongée dans l'obscurité.
- Des arbres et de la végétation.
- Des créatures dissimulées dans l'environnement.
- Des yeux lumineux apparaissant dans le noir.
- Des Yo-kai dont on devine la présence avant de découvrir leur apparence.
- Une atmosphère nocturne, mystérieuse et légèrement inquiétante.

**Ce sont les éléments que je souhaite retrouver.**

Le but n'est pas de reproduire directement une séquence du film, mais de créer une introduction originale utilisant cette même logique de mise en scène.

Le spectateur doit ressentir qu'un monde invisible existe autour des humains.

## 2. Déroulement souhaité

Je propose la structure suivante.

### Séquence A — Le silence et l'obscurité

L'écran commence dans une ambiance sombre.

Un décor forestier nocturne apparaît progressivement.

On doit distinguer des silhouettes d'arbres, des buissons et éventuellement une rivière.

La scène doit installer le mystère.

### Séquence B — Les yeux dans l'obscurité

Des yeux lumineux commencent à apparaître.

D'abord une paire, puis plusieurs autres à différents endroits du décor.

Ils peuvent apparaître :

- Derrière un arbre.
- Entre deux buissons.
- Dans l'ombre des branches.
- À proximité de l'eau.
- Dans un coin du décor.

Je veux que ces yeux attirent l'attention du joueur.

Les Yo-kai doivent être principalement dissimulés.

### Séquence C — La présence des Yo-kai

On comprend progressivement que plusieurs créatures observent la scène.

De légers mouvements ou changements de lumière peuvent suggérer leur présence.

Il n'est pas nécessaire de révéler entièrement chaque personnage.

Au contraire, je souhaite conserver cette impression de mystère.

### Séquence D — La Yo-kai Watch

La cinématique introduit ensuite le concept de la Yo-kai Watch.

La montre permet de révéler les créatures invisibles aux humains.

On peut utiliser une apparition lumineuse, un fondu ou un changement d'ambiance.

Éviter de transformer la scène en succession de longs dialogues.

### Séquence E — Transition vers le titre

La cinématique se termine par une transition fluide vers l'écran titre.

La musique doit accompagner cette transition.

Le résultat doit donner l'impression de regarder le début d'un véritable jeu Yo-kai Watch.

## 3. Contraintes artistiques

- Atmosphère mystérieuse plutôt que comique.
- Palette nocturne avec des bleus, verts sombres et touches lumineuses.
- Yeux lumineux clairement visibles.
- Composition lisible malgré la résolution GBA.
- Pas de révélations sur les grands boss ou les rencontres légendaires.
- Pas de texte inutilement long.
- Pas de séquence copiée directement du film.
- Pas de simples images statiques enchaînées sans mise en scène.

Je préfère une cinématique relativement courte, mais soigneusement réalisée.

## 4. Animations possibles

Étudier les techniques compatibles avec le moteur GBA :

- Fondus progressifs.
- Apparitions successives d'yeux.
- Petits déplacements de sprites.
- Changements de palettes.
- Effets lumineux simples.
- Défilement léger du décor.
- Transitions entre arrière-plans.

L'animation doit fonctionner correctement sur le matériel GBA, sans surcharge de mémoire ni ralentissements importants.

**Je souhaite une véritable impression de mise en scène, pas seulement un écran sombre avec quelques phrases.**

---

# PARTIE 2 — REFONTE DE L'ÉCRAN TITRE

## 1. Référence principale

Je souhaite un écran titre inspiré de l'image de référence de Yo-kai Watch 4 que je fournirai.

Cette image sert de référence pour :

- La composition générale.
- L'organisation visuelle.
- Le style du fond.
- La présence de plusieurs Yo-kai.
- La position du logo.
- L'ambiance et les couleurs.

**Je ne veux PAS un écran titre affichant Yo-kai Watch 4.**

Le logo doit indiquer uniquement :

**YO-KAI WATCH**

Aucun numéro 4.

Aucun logo Pokémon Rouge Feu.

## 2. Composition attendue

### En haut

Un grand logo YO-KAI WATCH bien visible et correctement centré.

Il doit être immédiatement identifiable.

Le logo ne doit pas être trop petit ni déformé.

### Au centre

Un fond illustré avec plusieurs Yo-kai.

Je souhaite une composition riche, inspirée des jeux Yo-kai Watch.

On peut notamment envisager :

- Jibanyan.
- Whisper.
- Komasan.
- D'autres Yo-kai représentatifs de notre sélection de 151 espèces.

Les personnages doivent être intégrés harmonieusement à la scène.

Ils ne doivent pas ressembler à des sprites simplement collés au hasard.

### En arrière-plan

Un décor inspiré du folklore japonais ou de l'esthétique des jeux Yo-kai Watch.

La référence possède notamment un aspect illustré et une ambiance de papier traditionnel.

Je souhaite reprendre cette direction artistique, adaptée à la palette et aux contraintes de la GBA.

### En bas

Les indications nécessaires pour démarrer le jeu.

Le texte doit être discret, lisible et cohérent avec le reste de l'écran.

Ne pas laisser d'éléments graphiques Pokémon Rouge Feu inutiles.

## 3. Contraintes visuelles

L'écran GBA possède une résolution de 240 × 160 pixels.

Il faut donc adapter intelligemment la composition.

Priorités :

1. Lisibilité du logo.
2. Qualité de la composition.
3. Reconnaissance des Yo-kai.
4. Lisibilité des commandes.
5. Cohérence des couleurs.

Je préfère un écran titre présentant trois ou quatre Yo-kai très bien intégrés plutôt qu'une multitude de personnages minuscules et illisibles.

Il faut préserver une identité visuelle forte malgré les limitations techniques.

## 4. Animation du titre

Si possible, ajouter quelques animations légères :

- Apparition progressive du logo.
- Mouvement subtil d'un élément du décor.
- Effet lumineux.
- Animation discrète des personnages.
- Clignotement de l'invitation à démarrer.

Ces animations doivent rester secondaires par rapport à la qualité de l'illustration.

---

# PARTIE 3 — IDENTITÉ SONORE DE L'INTRO ET DU TITRE

Les musiques utilisées doivent provenir de l'univers Yo-kai Watch.

Ne pas réintroduire les musiques Pokémon d'origine.

Réutiliser si possible les OST Yo-kai Watch déjà présentes dans le projet, afin de préserver l'espace disponible.

La transition entre la cinématique et l'écran titre doit être agréable à l'oreille.

Éviter les changements de volume brutaux.

**Concernant les bruitages : conserver les effets sonores existants et ajuster leur volume si nécessaire. Il ne faut pas lancer de refonte générale des bruitages pendant cette session.**

---

# PARTIE 4 — INTÉGRATION DES RÉFÉRENCES

Je vais fournir un ZIP contenant les images de référence.

Organisation suggérée :

- `01_INTRO/` : références de forêt nocturne, yeux lumineux et Yo-kai cachés.
- `02_ECRAN_TITRE/` : référence principale inspirée de Yo-kai Watch 4.

Je veux que tu examines ces références avant de finaliser les éléments graphiques.

Ne les considère pas comme des images à coller directement dans le jeu.

Étudie les compositions, les palettes, l'ambiance et les éléments visuels à reproduire avec des ressources originales.

Si une référence est incompatible avec la résolution GBA, propose une adaptation cohérente plutôt qu'une reproduction dégradée.

Les illustrations définitives doivent correspondre à l'identité des Yo-kai de notre ROM hack.

---

# PARTIE 5 — TESTS OBLIGATOIRES

Je veux une vérification du démarrage réel du jeu dans mGBA.

Tester notamment :

- Lancement de la ROM depuis le premier écran.
- Lecture complète de l'introduction.
- Fluidité des transitions.
- Affichage des yeux lumineux.
- Qualité des palettes.
- Apparition du logo.
- Lisibilité des textes.
- Affichage du nouvel écran titre.
- Fonctionnement du bouton START.
- Possibilité de passer l'introduction avec les commandes prévues.
- Passage au menu principal.
- Démarrage d'une nouvelle partie.
- Chargement d'une sauvegarde.
- Musiques et transitions sonores.
- Absence de corruption graphique.

Produire des captures réelles de l'émulateur à plusieurs étapes de l'introduction et de l'écran titre.

---

# PARTIE 6 — CONTRAINTES TECHNIQUES

- Conserver la compatibilité avec le moteur Pokémon Rouge Feu.
- Respecter la résolution 240 × 160.
- Préserver les systèmes de sauvegarde.
- Éviter les problèmes de palettes et de mémoire vidéo.
- Préserver les musiques et corrections réalisées dans les sessions précédentes.
- Ne pas casser les événements existants.
- Ne jamais dépasser **33 554 432 octets (32 Mio)** pour la ROM.
- Ne pas publier de fichiers audio protégés ni de ROM commerciale complète sur GitHub.

Ne pas entreprendre de réécriture générale du moteur si des solutions graphiques simples permettent d'obtenir le rendu souhaité.

---

# LIVRABLES ATTENDUS

À la fin de cette session, je souhaite :

1. Une nouvelle introduction fonctionnelle.
2. Un nouvel écran titre conforme aux références.
3. Des captures mGBA montrant les principales étapes de l'introduction.
4. Une capture complète de l'écran titre.
5. Un bilan des animations réalisées.
6. Un contrôle des performances et de la mémoire.
7. La taille finale exacte de la ROM.
8. Les modifications publiées sur GitHub.
9. Une liste des éventuelles limitations restantes.

**Je veux que tu privilégies la qualité artistique.**

Si tu hésites entre plusieurs compositions, propose des aperçus comparatifs avant de retenir une version définitive.

La priorité n'est pas de terminer le plus rapidement possible, mais de produire une introduction et un écran titre qui donnent immédiatement l'impression de jouer à Yo-kai Watch.

Cette session ne doit pas relancer le chantier global des sprites de combat, la traduction complète ni les autres quêtes.

Ces sujets sont réservés aux autres sessions.