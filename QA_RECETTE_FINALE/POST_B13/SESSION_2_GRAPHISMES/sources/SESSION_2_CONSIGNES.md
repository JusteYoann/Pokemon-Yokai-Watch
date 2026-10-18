# SESSION 2/4 — FINALISATION GRAPHIQUE COMPLÈTE

## Contexte

Nous poursuivons la finalisation de mon ROM hack Pokémon Rouge Feu × Yo-kai Watch.

Travaille sur la branche `dev/reconstruction-finalisation` du dépôt `JusteYoann/Pokemon-Yokai-Watch`.

Cette session est exclusivement consacrée à **l'amélioration graphique et à l'harmonisation des sprites**.

Je veux que tu reprennes les travaux déjà réalisés lors du chantier POST-B13, sans repartir de zéro et sans écraser les éventuelles modifications de la session 1 consacrée à l'audio.

Consulte notamment les rapports, registres, planches comparatives et captures déjà présents dans `QA_RECETTE_FINALE/POST_B13/`.

**Objectif principal : tous les Yo-kai doivent être correctement dimensionnés, positionnés et visuellement cohérents avec le style GBA de Pokémon Rouge Feu.**

La compilation réussie ne suffit pas. Je veux un contrôle du rendu réel dans le jeu.

---

## PRIORITÉ 1 — LES 151 SPRITES DE COMBAT

C'est le chantier graphique le plus important.

Je souhaite un contrôle individuel des 151 espèces, pour leurs sprites de face et de dos.

### A. Sprites de face

Pour chaque Yo-kai :

- Vérifier la taille apparente dans un combat.
- Vérifier son centrage horizontal.
- Vérifier sa hauteur par rapport à la plateforme.
- Vérifier les éventuelles zones transparentes excessives.
- Vérifier que les pieds, les pattes ou la base du corps reposent correctement sur la plateforme lorsque cela correspond à sa morphologie.
- Harmoniser la taille des espèces selon leur véritable gabarit.
- Respecter les différences naturelles entre les petits Yo-kai, les grands Yo-kai et les boss.
- Vérifier la progression visuelle entre les évolutions.

**Exemples problématiques observés dans la B13 :**

**Pitou :** trop grand pour son gabarit. Réduire sa taille apparente et ajuster son centrage.

**Baku :** trop petit et mal centré. Ajuster son échelle et sa position.

**Cigalopin :** légèrement trop imposant pour une petite espèce du début du jeu.

Ces exemples ne sont pas une liste exhaustive.

### B. Sprites de dos

C'est un point particulièrement important.

Lors de mon premier test, beaucoup de sprites alliés étaient cadrés trop haut ou montraient une proportion excessive du bas du corps.

Je veux que les back sprites reprennent la logique visuelle des combats de Pokémon Rouge Feu.

**Pour les Yo-kai dont la morphologie le permet, le cadrage doit privilégier le haut du corps, approximativement à partir de la taille ou du bassin.**

Je ne souhaite pas voir systématiquement le personnage entier jusqu'aux pieds.

Attention cependant :

- Ne pas couper les personnages arbitrairement.
- Adapter le cadrage aux créatures quadrupèdes, volantes ou possédant une morphologie particulière.
- Éviter les décalages identiques appliqués à tous les sprites.
- Conserver les détails caractéristiques importants.
- Ne pas déformer les pixels.
- Ne pas agrandir artificiellement des images de mauvaise résolution.

**Cas à réexaminer en priorité :**

- Komasan : bas du corps trop visible.
- Komaous : cadrage de dos peu homogène, corps presque entièrement visible.
- Cigalopin : taille et cadrage.
- Nihilistik : position verticale.
- Les autres espèces présentant des anomalies comparables.

Les corrections déjà effectuées dans les derniers commits doivent être contrôlées, pas automatiquement refaites.

### C. Méthode de vérification

Je veux une approche systématique.

1. Inventorier les 151 espèces et leurs sprites face/dos.
2. Générer des captures de combat réelles dans mGBA pour chacune.
3. Construire des planches comparatives lisibles.
4. Identifier les problèmes restants de taille et de cadrage.
5. Appliquer des corrections individuelles.
6. Reconstruire la ROM.
7. Regénérer les captures après correction.
8. Comparer les résultats avant/après.

Ne considère pas un sprite comme correct uniquement parce que son fichier possède les dimensions attendues.

**Préserver autant que possible les dessins originaux des Yo-kai.** Je demande surtout une harmonisation des proportions et de la présentation, pas une refonte complète de tous les personnages.

---

## PRIORITÉ 2 — LES 151 ICÔNES D'ÉQUIPE ET DE PC

Les icônes de la première B13 présentaient de grandes différences de taille apparente.

Je sais qu'une première harmonisation a déjà été effectuée.

Je veux maintenant vérifier le résultat final sur les 151 espèces.

Contrôler :

- Les dimensions visibles.
- Le centrage.
- La cohérence des proportions.
- La lisibilité des petits personnages.
- Les éventuels débordements.
- Les animations des icônes si elles existent.
- L'affichage dans le menu d'équipe.
- L'affichage dans les boîtes PC.
- Les autres interfaces qui réutilisent ces images.

Il ne faut pas nécessairement donner la même taille à toutes les espèces : un petit Yo-kai doit conserver son identité.

Mais aucun personnage ne doit sembler démesurément grand ou minuscule à cause d'un mauvais traitement graphique.

Je veux des planches comparatives et des vérifications directement dans les interfaces du jeu.

---

## PRIORITÉ 3 — SPRITES OVERWORLD HUMAINS

Je souhaite une passe artistique complète sur tous les nouveaux personnages actuellement implémentés.

Pendant mon test, j'ai trouvé plusieurs personnages personnalisés moins réussis que les PNJ originaux de Rouge Feu.

**La référence stylistique doit être le véritable overworld de Pokémon Rouge Feu.**

À contrôler :

- Taille du personnage.
- Proportions tête/corps.
- Largeur de la silhouette.
- Densité et cohérence des pixels.
- Contours.
- Ombres.
- Palette.
- Lisibilité du visage et des vêtements.
- Animations de marche.
- Orientations avant, arrière, gauche et droite.
- Position sur les cases et cohérence avec les décors.

Examiner notamment les personnages déjà intégrés :

- Nathan.
- Katie.
- Matt.
- Ariane.
- Domniscian et ses employés.
- Don Morleone et la Mafiamille.
- Nathaniel.
- Michael.
- Wyatt.
- Lord Enma.
- Les autres personnages personnalisés effectivement présents dans le jeu.

Ne pas inventer de nouveaux personnages ni intégrer les quêtes supplémentaires reportées.

Pour les personnages disposant d'animations particulières, vérifier également les poses concernées.

---

## PRIORITÉ 4 — YO-KAI OVERWORLD

Certains Yo-kai présents directement sur la carte paraissent trop grands par rapport au joueur et aux décors.

Je veux une vérification globale.

### Léo transformé en Jibanyan

Dans le bâtiment où se déroule sa transformation, Jibanyan était beaucoup trop grand.

Réduire son gabarit apparent pour qu'il corresponde davantage à l'échelle du joueur et du décor.

Il doit rester parfaitement identifiable.

### Usapyon avec Ariane

Vérifier la taille de son sprite et ses proportions par rapport à Ariane.

Conserver sa silhouette et ses caractéristiques visuelles.

### Misterre

**Le sprite overworld de Misterre est déjà très réussi : ne pas le refaire entièrement.**

Je demande seulement de confirmer les corrections suivantes :

- Retirer les deux éléments verts ressemblant à des yeux.
- Utiliser les couleurs marron/bois appropriées à cet endroit.
- Supprimer la bouche ajoutée sur son tronc.
- Ne pas modifier inutilement sa silhouette, ses branches ni son apparence générale.

Vérifier les deux emplacements où Misterre remplace Ronflex.

### Autres Yo-kai sur la carte

Contrôler les créatures spéciales, les rencontres fixes et les Yo-kai utilisés dans les événements.

Les grandes créatures peuvent conserver une taille imposante lorsqu'elle est intentionnelle.

Il faut distinguer un personnage naturellement gigantesque d'un sprite incorrectement agrandi.

---

## PRIORITÉ 5 — LES VARIANTES SHINY

Je souhaite également terminer les finitions graphiques liées aux shiny.

Vérifier les espèces réellement autorisées à être shiny dans notre système.

**Conserver les exclusions déjà validées pour les 67 espèces non éligibles.**

Pour les espèces éligibles :

- Vérifier l'existence de leurs variantes graphiques.
- Vérifier les couleurs et palettes.
- Vérifier les sprites de face et de dos.
- Vérifier les icônes lorsque nécessaire.
- Contrôler les éventuelles différences visuelles prévues.
- Vérifier les évolutions shiny.
- Vérifier les familles de Yo-kai.
- Finaliser les éléments encore manquants de Robonyan 28, notamment ses détails spécifiques.

Ne pas inventer une variante shiny arbitraire lorsque son apparence n'est pas définie.

Si certaines références visuelles sont indispensables, identifier précisément les espèces concernées afin que je puisse fournir les images nécessaires.

---

## PRIORITÉ 6 — CONTRÔLES TECHNIQUES

Toutes les modifications graphiques doivent rester compatibles avec les contraintes de la GBA.

**Limite absolue de la ROM : 33 554 432 octets.**

Contrôler :

- Taille des ressources graphiques.
- Palettes et index des couleurs.
- Transparence.
- Dimensions et alignements.
- Pointeurs et tables graphiques.
- Mémoire vidéo et mémoire de travail.
- Compatibilité des animations.
- Absence de corruption graphique pendant les combats et dans les menus.

Ne pas remplacer les ressources d'origine par des images beaucoup plus lourdes sans justification.

Préserver les données et le fonctionnement des 151 Yo-kai, leurs statistiques, attaques, évolutions, rencontres, captures et événements.

---

## ORGANISATION DU TRAVAIL

Je veux que tu travailles de manière autonome sur tout ce chantier graphique, avec des commits intermédiaires.

Commence par auditer les corrections graphiques déjà publiées, puis concentre-toi sur ce qui reste réellement incomplet.

L'ordre de priorité est :

1. Sprites de combat des 151 Yo-kai.
2. Icônes d'équipe et PC.
3. Sprites overworld humains.
4. Sprites overworld des Yo-kai.
5. Variantes shiny et finitions particulières.
6. Tests de non-régression.

**Ne t'arrête pas après une simple inspection : effectue effectivement les corrections nécessaires.**

Quand une décision demande une validation artistique de ma part, présente des captures avant/après et signale clairement ce qui attend mon accord.

---

## LIVRABLES ATTENDUS

À la fin de la session, je veux :

- Une ROM privée reconstruite et testée, ou une procédure exacte pour la reconstruire avec mes ressources locales.
- Les commits GitHub publiés sur la branche de développement.
- Un inventaire des 151 sprites face/dos vérifiés.
- Des planches comparatives avant/après.
- Un bilan des 151 icônes.
- Des captures des personnages et Yo-kai overworld corrigés.
- Un état précis des variantes shiny.
- Le détail des tests réellement effectués dans mGBA.
- La taille finale mesurée de la ROM.
- Une liste honnête des corrections restantes.

Documente le tout dans `QA_RECETTE_FINALE/POST_B13/` et mets à jour le tableau de suivi existant.

**Important :** cette session concerne les graphismes uniquement.

Ne relance pas la refonte musicale, ne remplace aucun bruitage et ne commence pas encore la nouvelle introduction ni l'écran titre. Ces sujets appartiennent à d'autres sessions.

Ne modifie pas inutilement le gameplay, la traduction ou les événements scénaristiques.

**Je veux avant tout une cohérence graphique digne d'un jeu GBA abouti, et non une collection de sprites aux tailles et aux cadrages disparates.**