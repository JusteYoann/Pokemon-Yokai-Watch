# Pokémon Rouge Feu × Yo-kai Watch — Rapport de bêta-test et corrections

Tu travailles sur le dépôt GitHub `JusteYoann/Pokemon-Yokai-Watch`.

J'ai commencé à tester la première ROM jouable sur mGBA et j'ai identifié plusieurs bugs, problèmes visuels et éléments de gameplay à améliorer.

**Mission : corriger les problèmes ci-dessous, sans modifier inutilement les fonctionnalités qui fonctionnent déjà.**

## Règles impératives

- Ne jamais fusionner sur `master` sans mon autorisation explicite.
- Travailler sur une branche dédiée aux corrections.
- Préserver les 151 espèces de Yo-kai, leurs identifiants et le scénario existant.
- Ne pas supprimer de personnages ou d'événements narratifs importants.
- Conserver les sauvegardes compatibles autant que possible.
- Compiler une ROM après les corrections.
- Effectuer des tests mGBA sur les fonctionnalités modifiées.
- Documenter les changements, les tests et les éventuelles limites.

---

## 1. Dialogues et événements

**BUG-001 — Dialogues non traduits**

Certains dialogues sont encore en anglais, notamment :

- Des phrases de Matt.
- Une phrase prononcée par une femme dans un Centre Pokémon.

Effectuer une vérification des dialogues du jeu et traduire les textes restants en français naturel.

**BUG-002 — Dialogue incohérent de Wyatt**

Lorsque Wyatt parle de Don Morléone avant son combat, son nouveau dialogue scénaristique est immédiatement suivi de son ancien dialogue générique.

Il salue donc le joueur une deuxième fois et change brutalement de ton.

Fusionner ces dialogues afin d'obtenir une seule conversation cohérente, suivie du déclenchement du combat.

**BUG-003 — Collision dans la cinématique de Don Morléone**

À la fin de son discours, Don Morléone traverse littéralement l'un de ses sbires.

Corriger les déplacements et vérifier les collisions dans les cinématiques contenant plusieurs personnages.

**BUG-004 — Placement des personnages dans la photographie finale**

Lors de la dernière image des crédits, certains personnages se tiennent sur des cases contenant des arbres ou des obstacles.

Deux solutions possibles :

- Repositionner les personnages.
- Créer un petit décor de plaine verte spécifiquement destiné à cette photographie.

L'objectif est d'obtenir une belle scène de groupe crédible, sans personnages superposés aux éléments du décor.

---

## 2. Sprites et graphismes

**BUG-005 — Icône du Seigneur Enma**

Le Yo-kai n°150 représente désormais le véritable Seigneur Enma, et non l'ancien Enma violet.

Vérifier et remplacer son icône dans les interfaces concernées, notamment le Médallium et l'équipe.

**BUG-013 — Couleurs anormales des montures Surf et Vol**

Les sprites utilisés pendant Surf et Vol présentent des couleurs différentes de celles de Pokémon Rouge Feu original.

Vérifier les palettes graphiques et restaurer les couleurs normales des montures.

Rechercher particulièrement les conflits éventuels avec les palettes personnalisées, le sépia de Cramois'Île et les effets météorologiques.

**BUG-014 — Sprite de combat d'Emperor déformé**

Le sprite d'Emperor semble trop grand et étiré par rapport à son image de référence.

Comparer le sprite actuel avec `101 - Emperor.png`, fourni dans les références.

Corriger les proportions sans dénaturer le pixel art et vérifier également le sprite de dos.

**BUG-015 — Sprites de dos coupés pendant leurs animations**

En combat, les sprites de dos des Yo-kai sont animés.

Cependant, leurs mouvements révèlent parfois une ligne horizontale de découpe, donnant l'impression que le sprite est tronqué.

Identifier l'origine du problème et corriger les limites d'affichage ou le cadrage.

**Conserver les animations de mouvement.**

Effectuer des tests sur plusieurs Yo-kai de tailles différentes.

---

## 3. Lavanville et les zombies

**BUG-006 — Disparition temporaire des effets graphiques**

Lorsque le regard d'un zombie déclenche un combat, Lavanville perd momentanément sa teinte nocturne et son brouillard pendant la transition.

Corriger cette interruption visuelle.

**MOD-007 — Comportement des zombies après la Championne**

Après la victoire contre la Championne associée à Lavanville :

- Les zombies ne doivent plus déclencher automatiquement un combat lorsqu'ils voient le joueur.
- Il faut leur parler volontairement pour les affronter.
- Le joueur doit pouvoir fuir ces combats.

Utiliser le bon indicateur scénaristique pour vérifier la victoire contre la Championne.

**MOD-008 — Petite cinématique avant les combats de zombies**

Avant la victoire contre la Championne, lorsqu'un zombie repère le joueur :

1. Il se tourne vers lui.
2. Il avance lentement dans sa direction.
3. Il prononce une courte phrase, par exemple « Grrr... ».
4. Le combat commence.

Respecter les collisions et éviter que le zombie traverse des obstacles.

**MOD-009 — Vitesse des zombies**

Certains zombies se déplacent actuellement beaucoup trop rapidement.

Nouvelle vitesse souhaitée :

- Zombies rapides : environ un pas par seconde.
- Zombies classiques : plus lents encore, avec une proposition d'environ un pas toutes les deux secondes.

Conserver une différence de vitesse perceptible entre les deux catégories.

---

## 4. Apparitions des personnages

**MOD-010 — Suppression des anciens caméos devenus inutiles**

Plusieurs personnages qui avaient initialement été intégrés comme caméos sont désormais des Champions d'Arène.

Leurs anciennes apparitions secondaires devenues redondantes doivent être supprimées.

Attention : conserver impérativement leurs rôles de Champions, leurs dialogues importants et leurs événements scénaristiques indispensables.

Effectuer d'abord un inventaire précis des caméos concernés avant toute suppression.

---

## 5. Cramois'Île, Route 21 et brume temporelle

**BUG-011 — Disparition brutale du sépia sur la Route 21**

Cramois'Île se situe 60 ans dans le passé et utilise une teinte sépia.

Pourtant, lorsqu'on rejoint le petit secteur de la Route 21 adjacent à l'île, le sépia disparaît immédiatement.

Le sépia doit également être présent dans cette portion de la Route 21.

Il doit ensuite disparaître progressivement à mesure que le joueur approche et traverse la brume temporelle.

Le comportement doit être cohérent dans les deux sens.

**BUG-012 — Surf extrêmement lent près de la brume**

L'animation de Surf est devenue anormalement lente dans les zones concernées par la brume temporelle.

Vérifier si le problème provient :

- Du rendu de la brume.
- Des mises à jour graphiques.
- De l'animation du personnage.
- Du déplacement sur la carte.
- D'un éventuel problème de performances.

Si la brume est trop coûteuse, envisager de réduire sa densité tout en conservant un effet atmosphérique convaincant.

**Priorité : retrouver une vitesse de déplacement et une fluidité normales.**

---

## 6. Équilibrage de la Ligue

**ÉQUILIBRAGE-016 — Ligue excessivement difficile**

Pendant les premiers tests, les Yo-kai de la Ligue semblent beaucoup trop puissants.

L'objectif est de permettre à un joueur disposant d'une équipe normalement constituée de six Yo-kai autour du niveau 60 de terminer la Ligue avec une bonne stratégie.

Tester les quatre adversaires, dans cet ordre :

1. Zazel.
2. Enma l'Ancien.
3. Orqanos.
4. Maître Nyada.

Objectifs :

- Équipe niveau 55 : victoire possible, mais très difficile.
- Équipe niveau 60 : difficulté élevée, mais raisonnablement gagnable.
- Équipe niveau 65 : combat accessible avec une stratégie adaptée.

Analyser les statistiques, attaques, talents, objets tenus, types et éventuelles combinaisons déséquilibrées.

Rééquilibrer les paramètres nécessaires sans retirer de membres aux équipes.

Conserver les six Yo-kai de chaque Dresseur, leurs identités stratégiques et leurs Yo-kai emblématiques.

Si possible, conserver Maître Nyada au niveau 65 en tant que dernier adversaire.

Éviter qu'une équipe adverse puisse éliminer systématiquement les six Yo-kai du joueur sans réelle possibilité de riposte.

Ne pas se contenter d'une comparaison théorique des niveaux : effectuer des tests de combat représentatifs.

---

## 7. Problème audio majeur

**AUDIO-001 — Grésillement constant de type radio**

Toutes les musiques semblent fonctionner, mais un bruit parasite permanent ressemblant à des interférences radio est audible dans la ROM jouée sur mGBA.

Information particulièrement importante :

**L'avant-dernière ROM produite ne présentait pas ce problème. Il est apparu dans la dernière version.**

Il faut donc rechercher une régression récente.

Consignes :

1. Comparer la dernière ROM problématique avec la version précédente qui fonctionnait.
2. Examiner les changements apportés au moteur audio, aux musiques, aux banques de sons et aux conversions.
3. Vérifier si le problème touche les effets sonores, les musiques ou les deux.
4. Identifier précisément la cause avant de modifier les ressources.
5. Corriger le bruit parasite sans supprimer les OST personnalisées.
6. Vérifier le résultat directement dans une ROM exécutée sur mGBA.

---

## 8. Validation finale

Après les corrections :

1. Compiler une nouvelle ROM `.gba`.
2. Vérifier qu'elle démarre correctement.
3. Tester les événements et animations concernés.
4. Vérifier qu'aucune correction ne provoque une nouvelle régression.
5. Effectuer une vérification des performances à Cramois'Île et sur les routes maritimes.
6. Produire un rapport détaillé indiquant, pour chaque problème, s'il est corrigé, partiellement corrigé ou toujours présent.
7. Fournir un lien vers la nouvelle ROM de test.

**Ne pas fusionner sur `master` sans mon accord explicite.**

Le but est d'obtenir une version bêta plus stable, plus fluide et mieux équilibrée, tout en conservant l'identité et l'ambition du projet.