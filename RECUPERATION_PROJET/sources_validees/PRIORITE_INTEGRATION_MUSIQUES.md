# POKÉMON × YO-KAI WATCH — PRIORITÉ ABSOLUE À L'INTÉGRATION DES MUSIQUES

Reprends immédiatement le développement de Pokémon × Yo-kai Watch sur la branche `dev/reconstruction-finalisation`.

Ton dernier rapport indique le commit `c6ef8f46b`, avec le scénario de Chen et du Seigneur Enma adapté, le sprite distinct d'Enma capturable intégré et un pipeline DPCM préparé.

Je valide ces progrès.

**Je souhaite maintenant que tu consacres cette session principalement à l'intégration effective des musiques Yo-kai Watch dans le jeu.**

## 1. Reprendre sans recommencer

Vérifie le dernier commit GitHub, les modifications locales éventuelles et les documents de direction musicale.

Ne refais pas les audits déjà terminés.

Conserve les dernières décisions scénaristiques et graphiques, notamment la distinction entre le Seigneur Enma et le Yo-kai Enma capturable.

## 2. Optimiser les 20 OST avant toute suppression

Tu as indiqué que les morceaux complets porteraient la ROM à 36,92 Mio, au-delà de la limite de 32 Mio.

**Ne supprime aucune musique sans avoir d'abord étudié et appliqué les optimisations possibles.**

Pour chaque morceau :

- Identifie une introduction éventuelle à jouer une seule fois.
- Identifie la section musicale qui doit tourner en boucle.
- Évite d'encoder plusieurs répétitions identiques.
- Réduis les silences inutiles.
- Optimise la taille des données audio sans dégrader excessivement leur qualité.
- Conserve une fréquence d'échantillonnage adaptée à la GBA.
- Mesure précisément le poids obtenu après optimisation.

Utilise le pipeline DPCM déjà développé, en privilégiant la méthode B précédemment validée.

Le morceau de vélo doit démarrer directement sur son thème principal.

Les musiques de combat doivent respecter leur introduction puis boucler correctement.

Vérifie également si les morceaux de grande taille disposent d'autres optimisations pertinentes, sans provoquer de bugs audio.

Ne modifie pas la durée ou la structure musicale au hasard : les boucles doivent rester naturelles.

## 3. Intégrer réellement les musiques dans la ROM

**Je ne veux pas seulement un rapport d'optimisation ou de nouveaux fichiers audio préparés.**

Je souhaite que tu commences effectivement à relier les morceaux aux événements et aux lieux prévus dans le jeu.

Reprends les affectations des 20 OST validées dans le cahier des charges musical.

Commence par un premier groupe de morceaux prioritaires permettant de valider complètement la chaîne d'intégration.

Pour chaque musique intégrée :

1. Prépare ses données audio optimisées.
2. Intègre-les dans le moteur sonore.
3. Associe-les au bon lieu, personnage ou combat.
4. Compile la ROM.
5. Teste leur lecture dans mGBA.
6. Vérifie les boucles et les transitions.
7. Contrôle la taille de la ROM et l'absence de régression.

Une fois le premier groupe fonctionnel, poursuis avec les autres OST, tant que les contraintes techniques le permettent.

## 4. Préserver les 20 choix musicaux

Je souhaite toujours conserver les 20 OST prévues.

Ne remplace pas arbitrairement leur sélection ni leurs emplacements.

Je tiens notamment à conserver « Somewhere A Bit Dodgy » pour le Repaire Rocket.

La musique « The Very Curious Yo-kai Watch » envisagée pour la nouvelle introduction est une référence supplémentaire facultative. Elle ne doit pas retarder l'intégration des vingt morceaux principaux.

Si les 20 OST ne peuvent pas tenir correctement malgré les optimisations, donne-moi un bilan précis des morceaux intégrés, de ceux qui restent et de leur poids respectif.

Ne retire aucun morceau définitivement sans me consulter.

## 5. Respecter les limites de la ROM

Le jeu doit rester dans la limite ROM compatible avec notre cible GBA et fonctionner correctement dans mGBA.

Les données audio ne doivent pas écraser d'autres ressources.

Contrôle :

- La taille finale de la ROM.
- L'espace disponible pour les fonctionnalités restantes.
- La lecture des bruitages pendant les musiques.
- Les changements de musique entre cartes et combats.
- Le retour à la musique d'exploration après un combat.
- Les sauvegardes et le chargement.
- L'absence de ralentissements ou de plantages.

Évite les modifications invasives du moteur lorsque des solutions plus simples sont possibles.

## 6. Attention aux ressources musicales privées

Les enregistrements Yo-kai Watch doivent rester privés.

Ne publie pas les MP3, les échantillons DPCM dérivés des enregistrements protégés ni une ROM contenant ces musiques dans le dépôt GitHub public.

Publie uniquement les outils, les scripts, la configuration, les modifications du moteur et les instructions nécessaires pour reconstruire localement une ROM avec les sources audio privées.

Prévois un fonctionnement reproductible :

- Compilation publique sans les enregistrements privés.
- Compilation locale avec intégration des musiques lorsque les sources privées sont disponibles.
- Documentation des fichiers attendus et de leurs empreintes.
- Vérification explicite de la version réellement testée.

La version publique sans musique ne doit pas être présentée comme la version musicale finale.

## 7. Ne pas se disperser

Pour cette session, évite de développer de nouvelles quêtes secondaires.

Les quêtes sont désormais la dernière priorité du projet.

N'ajoute pas de nouveaux personnages ou de nouvelles mécaniques indépendantes.

Concentre-toi sur la musique, la stabilité et la progression vers une version finalisée.

Si l'intégration musicale révèle un problème bloquant, corrige-le avant de poursuivre.

## 8. Sauvegarder régulièrement

Publie régulièrement tes modifications fonctionnelles sur `dev/reconstruction-finalisation`.

Ne laisse pas les changements importants uniquement dans ton environnement local.

Conserve `master` intact.

Avant la fin de la session, réalise une sauvegarde GitHub et une vérification de reproductibilité depuis un clone propre, dans la mesure où les ressources privées disponibles permettent cette vérification.

## 9. Résultat attendu

À la fin de cette session, je souhaite un résultat concret :

- Plusieurs musiques réellement intégrées et audibles dans mGBA, si techniquement possible.
- Des boucles fonctionnelles.
- Des mesures précises de taille avant et après optimisation.
- Une ROM qui reste stable et compatible avec la cible.
- Des modifications de code sauvegardées sur GitHub.
- Un rapport indiquant clairement quelles musiques sont fonctionnelles et lesquelles restent à intégrer.

Ne déclare pas une OST « intégrée » si elle est seulement convertie, préparée ou simulée.

Tu peux avancer de façon autonome, sans me demander de validation intermédiaire pour les décisions techniques secondaires.

**Mon objectif est que cette session fasse progresser concrètement la bande-son de Pokémon × Yo-kai Watch, et pas uniquement sa préparation.**

Commence immédiatement par optimiser et intégrer un premier groupe d'OST, puis poursuis aussi loin que possible pendant cette session.