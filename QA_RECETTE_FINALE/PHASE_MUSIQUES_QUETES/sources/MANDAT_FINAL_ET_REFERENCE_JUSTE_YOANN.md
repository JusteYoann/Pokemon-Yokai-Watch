# POKÉMON × YO-KAI WATCH — DERNIÈRE GRANDE PHASE DE DÉVELOPPEMENT

Je souhaite maintenant lancer la dernière grande phase de développement de mon ROM hack Pokémon Rouge Feu × Yo-kai Watch.

Tu as déjà reçu et lu le fichier **CAHIER_DES_CHARGES_POKEMON_YOKAI_WATCH_MUSIQUES_QUETES.md**, qui constitue le document de référence principal de cette mission.

Je joins également l'image officielle de mon personnage **Juste Yoann**.

**Mon objectif est qu'à l'issue de cette mission, le jeu soit complet en contenu, jouable du début à la fin, avec son postgame, ses quêtes, ses musiques et ses personnages.**

Il ne s'agit plus d'une phase de conception : je souhaite que tu réalises concrètement les modifications nécessaires.

## 1. Préserver tout le travail déjà réalisé

Avant toute modification, effectue un audit du projet et de ses branches.

Nous avons déjà développé de nombreux éléments :

- Les 151 espèces de Yo-kai.
- Leurs statistiques, attaques, évolutions et méthodes d'obtention.
- Les sprites normaux et chromatiques.
- Nathan Adams et Katie Forester comme protagonistes.
- Matt Descartes comme rival.
- Les équipes des champions, du Conseil 4 et des autres adversaires.
- Les rencontres légendaires.
- Les caméos de personnages Yo-kai Watch.
- Les adaptations de dialogues.
- Le système de partage d'expérience.
- Les fonctionnalités spécifiques du postgame.

**Ne repars pas de zéro et ne supprime aucun élément validé.**

Vérifie également les développements présents sur les différentes branches afin de ne pas travailler sur une version incomplète du projet.

Conserve une sauvegarde fiable avant les modifications et travaille sur une branche dédiée.

## 2. Intégrer définitivement les musiques Yo-kai Watch

Je valide la **méthode B en DPCM**, que j'ai personnellement testée à l'écoute.

Les musiques conservent leurs compositions originales tout en possédant un rendu légèrement rétro que je trouve parfaitement adapté à Pokémon Rouge Feu.

Je souhaite intégrer jusqu'à **20 OST**, conformément au cahier des charges.

Cela comprend notamment :

- Bicycle Theme pour le vélo.
- Vs. Hinozall pour Domniscian.
- Vs. The Ghoulfather pour Don Morleone.
- Infinite Tunnel pour la Tour Pokémon.
- Les thèmes d'Enma.
- Les musiques de la base des Blasters et du combat contre Coach Antonic.
- Les thèmes du scientifique et de ses combats contre Robonyan.
- Somewhere A Bit Dodgy pour le Repaire Rocket.
- Mini Boss Battle pour les employés de Domniscian et les Mafiamille.
- Les autres compositions indiquées dans le cahier des charges.

Respecte les associations musicales validées.

Pour les morceaux comportant une introduction importante, notamment les combats de boss, conserve cette introduction avant de répéter la partie principale.

Pour le vélo, privilégie un démarrage immédiat sur la section dynamique lorsque cela correspond à son utilisation en jeu.

Les boucles doivent fonctionner correctement et les musiques doivent revenir naturellement après les combats et les dialogues.

**Si les 20 OST ne rentrent pas**, optimise d'abord les boucles sans dénaturer les compositions, puis retire progressivement les morceaux les moins prioritaires suivant un ordre justifié.

Je préfère moins de musiques parfaitement fonctionnelles à une ROM instable.

Ne recommence pas la transcription automatique MIDI qui avait produit un mauvais résultat.

## 3. Créer et intégrer les dix quêtes secondaires

Implémente les dix quêtes du cahier des charges :

1. **Le Médallium du Professeur Chen** : obtenir les 151 Yo-kai.
2. **La fan de Jibanyan** : obtenir toutes les variantes demandées et recevoir un Shogunyan shiny.
3. **Le grand-père disparu** : retrouver un grand-père sur une île et le combattre.
4. **Le scientifique obstiné** : quatre rencontres successives, de Robonyan jusqu'à Robonyan 28 shiny.
5. **Le spécialiste des chromatiques** : présenter un véritable Yo-kai shiny, notamment celui obtenu via la quête 2.
6. **Les deux légendaires** : présenter Octorgone et Kyubi.
7. **Le mystérieux Red** : découvrir et affronter Red avec une véritable équipe de Pokémon.
8. **Les épreuves du Seigneur Enma** : enrichir son événement et son affrontement existants.
9. **Juste Yoann** : un premier combat humoristique, puis des revanches avec une véritable équipe stratégique.
10. **Coach Antonic et les Blasters** : une quête d'entraînement avec son équipe et ses compagnons.

Chaque quête doit disposer de véritables conditions de progression, de dialogues adaptés, de combats lorsque nécessaire et d'une conclusion.

Prévois des récompenses cohérentes sans créer de nouvelles espèces ni rendre le 100 % impossible.

Les dix quêtes doivent pouvoir être terminées sur une même sauvegarde.

## 4. Créer les personnages et leurs sprites

Utilise les sprites déjà présents lorsqu'ils sont satisfaisants.

Crée les nouveaux sprites nécessaires en respectant le style visuel de Pokémon Rouge Feu.

### Apparence officielle de Juste Yoann

**L'image jointe représente mon avatar et constitue la référence officielle de Juste Yoann.**

Conserve notamment :

- Ses cheveux gris foncé, volumineux et bouclés.
- Son visage clair.
- Ses caractéristiques faciales reconnaissables.
- Son style expressif et cartoon.

En revanche, pour sa tenue, **il doit porter les vêtements emblématiques de Nathan Adams dans Yo-kai Watch 1**, ainsi qu'une **Yo-kai Watch visible à son poignet**.

Crée un sprite overworld et un sprite de dresseur reconnaissables, compatibles avec Pokémon Rouge Feu.

L'image sert de référence pour son identité visuelle : tu peux adapter la pose et l'expression.

### Coach Antonic et les Blasters

Coach Antonic doit être visible avec trois compagnons :

- Jibanyan.
- Komasan.
- Whisper.

Ils doivent apparaître physiquement sur la carte, avec des interactions et des dialogues individuels.

Whisper doit conserver son caractère de chef autoproclamé des Blasters, tandis que Coach Antonic dirige désormais leur entraînement.

**Usapyon doit être placé auprès d'Ariane Célestin**, et non auprès de Coach Antonic.

Crée également les sprites nécessaires pour le scientifique, Red et les autres nouveaux personnages.

## 5. Donner une véritable personnalité aux dialogues

Je souhaite que les dialogues soient l'un des points forts du jeu.

Ne te limite pas à quelques phrases génériques avant les combats.

Les personnages importants doivent bénéficier de véritables scènes, avec des échanges parfois longs et construits, lorsque cela améliore la mise en scène.

**Les réactions après les combats sont particulièrement importantes.**

Chaque personnage doit réagir selon sa personnalité :

- Enma : puissant, joueur, curieux et enthousiaste face à un adversaire intéressant.
- Coach Antonic : énergique, exigeant et toujours obsédé par l'entraînement.
- Domniscian : arrogant, théâtral et fier de ses créations.
- Don Morleone : autoritaire, fier et fidèle à son rôle de chef mafieux.
- Le scientifique : prétentieux, de plus en plus frustré par ses défaites.
- Juste Yoann : humoristique, excessif et obsédé par l'idée de rester le favori du joueur face à Nyleco.
- Red : extrêmement sobre et mystérieux.

Respecte également les personnalités officielles de Nathan, Katie, Ariane, Whisper, Jibanyan, Komasan et des autres personnages présents.

Tu peux effectuer des recherches sur leurs personnalités dans les jeux Yo-kai Watch et tenir compte du contexte narratif déjà fourni.

Écris des dialogues originaux, adaptés à Kanto.

Prévois aussi des conversations lorsqu'on revient parler aux personnages après avoir terminé leurs quêtes, ainsi que des dialogues spécifiques aux revanches.

Respecte les contraintes techniques des boîtes de dialogue GBA.

## 6. Intégrer correctement tous les événements

Les personnages doivent apparaître aux bons endroits et au bon moment.

Fais attention aux conditions de déblocage, à la progression du joueur, aux badges, à la Ligue et au postgame.

Les quêtes ne doivent jamais bloquer l'aventure principale.

La quête de Red mérite une attention particulière : il doit combattre avec de véritables Pokémon possédant leurs propres statistiques, types, attaques et graphismes.

Cette fonctionnalité ne doit pas remplacer ou perturber les 151 espèces de Yo-kai.

Pour les caméos déjà existants, enrichis les dialogues et les événements sans créer de doublons.

## 7. Finaliser l'ensemble du jeu

Une fois les nouvelles fonctionnalités intégrées, ne considère pas immédiatement la mission comme terminée.

Vérifie également les éléments déjà développés.

Je souhaite que l'ensemble du jeu soit cohérent et complet :

- Aventure principale terminable.
- Huit badges accessibles.
- Team Rocket et Giovanni fonctionnels.
- Conseil 4 et combat final contre Matt.
- Progression et équilibrage satisfaisants.
- Évolutions et méthodes d'obtention fonctionnelles.
- Les 151 Yo-kai obtenables sur une seule sauvegarde.
- Sprites et animations correctement affichés.
- Système de partage d'expérience fonctionnel.
- Îles Sevii et postgame accessibles.
- Rencontres légendaires.
- Caméos et combats facultatifs.
- Dix quêtes secondaires.
- Musiques intégrées et correctement déclenchées.
- Sauvegarde et chargement fiables.

Corrige les bugs identifiés pendant les tests.

Ne modifie pas arbitrairement les choix artistiques et les données déjà validés.

## 8. Effectuer une véritable recette finale

Compile le jeu et vérifie son fonctionnement dans mGBA.

Ne te contente pas de vérifier que le projet compile.

Je veux des tests couvrant les différents événements importants, notamment :

- Les combats spéciaux.
- Les quêtes et leurs différentes étapes.
- Les dialogues conditionnels.
- Les revanches.
- Les récompenses.
- Les captures et évolutions.
- Les sauvegardes.
- Les interactions entre les musiques DPCM et les effets sonores.
- Les collisions et les déplacements des nouveaux sprites.
- L'obtention de tous les Yo-kai.
- La progression jusqu'à la fin de l'aventure et du postgame.

Si possible, effectue une véritable partie de validation de l'aventure principale et du 100 %, plutôt que de simples tests isolés.

Si certains éléments ne peuvent pas être testés automatiquement, signale-les explicitement.

## 9. Gestion des fichiers et GitHub

Conserve tous les fichiers sources nécessaires au développement.

N'efface pas les branches ou les travaux existants sans vérification.

Prépare le projet pour qu'il puisse être recompilé correctement.

Ne publie pas les MP3 originaux, les conversions audio protégées ou une ROM commerciale dans le dépôt GitHub public.

Préserve une méthode locale de compilation et de vérification.

## 10. Résultat final attendu

À la fin de cette mission, je veux :

1. Une version du jeu compilable et jouable.
2. Les vingt OST intégrées, ou le nombre maximal réellement compatible.
3. Les dix quêtes fonctionnelles.
4. Tous les nouveaux sprites nécessaires.
5. Les dialogues finalisés.
6. Les combats et événements correctement déclenchés.
7. Un rapport de tests détaillé.
8. Une liste des bugs corrigés.
9. Une liste précise des éventuels problèmes encore présents.
10. Des instructions claires pour récupérer et tester la version du jeu.

Classe honnêtement le résultat :

- **PRÊT** : toutes les fonctionnalités essentielles sont intégrées et correctement vérifiées.
- **PRÊT AVEC RÉSERVES** : le jeu est jouable et complet, mais quelques défauts mineurs subsistent.
- **NON PRÊT** : il reste des fonctionnalités essentielles incomplètes ou des bugs bloquants.

**MON OBJECTIF FINAL :**

Après cette mission, je souhaite que Pokémon × Yo-kai Watch soit terminé en contenu et suffisamment stable pour préparer mes tournages YouTube de décembre.

Je ne prévois pas d'ajouter de nouvelles grandes fonctionnalités après cette étape.

Je veux que tu concentres tes efforts sur la finition, la cohérence et la stabilité.

Prends le temps nécessaire pour réaliser un travail rigoureux. Si un problème technique empêche d'atteindre cet objectif, explique-le précisément et indique ce qu'il reste à corriger.

**Ne considère pas le jeu comme terminé tant que l'aventure principale, le postgame, les 151 Yo-kai et les dix quêtes ne sont pas réellement fonctionnels.**

Tu peux maintenant commencer le développement en suivant le cahier des charges joint et l'image de référence.