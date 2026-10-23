# POKÉMON × YO-KAI WATCH — FINALISATION DÉFINITIVE DE DON SPIRATON ET DE LA LIGUE

## 1. Contexte du projet

Dépôt GitHub : `JusteYoann/Pokemon-Yokai-Watch`

Branche de travail :
`feature/boss-final-don-spiraton`

Derniers commits confirmés :
- `0b0f99524` — récupération et corrections du prototype.
- `b3396ac9f` — cinématique de fusion et tests mGBA.

Le prototype du boss final Don Spiraton est déjà fonctionnel en environnement de développement.

Il comprend notamment :
- Le premier combat contre Don Morléone.
- L'intervention de Matt et le soin complet.
- La convergence des sbires.
- Le flash blanc.
- L'entrée en combat de Don Spiraton.
- Huit transformations successives.
- La sélection adaptative des contres.
- Les huit couches de vie colorées.
- Les transformations en fin de tour.
- Les trois affectations musicales validées.
- Matt comme Champion lors des revanches postgame.

**Ne reconstruis pas ces fonctionnalités. Réutilise et finalise le travail existant.**

Cette mission vise à rendre la finale accessible et terminable dans une partie normale, sans raccourci QA.

## 2. Protection du projet

Travaille exclusivement sur `feature/boss-final-don-spiraton`.

Vérifie d'abord le dernier commit distant et l'état local.

Préserve les modifications existantes, y compris les éventuels changements non publiés.

Ne fusionne aucune branche.

Ne modifie pas directement `master`, les branches Mafiamille, Argenta ou audio expérimentale.

Ne modifie pas les 151 Yo-kai, leurs statistiques, évolutions, capacités ou sprites déjà validés.

Ne modifie pas les huit trophées, les Champions d'Arène ou les rencontres légendaires.

Les 31 OST doivent rester intactes.

## 3. Intégration du véritable sprite de Don Spiraton

### Références obligatoires

Je fournis deux images.

**Image 1 :** une planche montrant plusieurs sprites de combat déjà utilisés dans notre ROM.

Elle sert de référence pour :
- La densité de pixels.
- Les contours.
- Les ombrages.
- Les palettes.
- La lisibilité.
- La direction artistique générale.

**Image 2 :** notre sprite de Don Spiraton placé dans l'interface de combat Pokémon Rouge Feu.

Elle sert de référence pour :
- L'apparence exacte du personnage.
- Ses proportions.
- Sa taille à l'écran.
- Son orientation.
- Sa position sur le terrain adverse.
- Son intégration visuelle dans l'interface.

**Utilise notre sprite existant comme source principale. Ne crée pas une nouvelle interprétation de Don Spiraton.**

### Harmonisation graphique

Notre sprite est satisfaisant, mais paraît légèrement trop détaillé par rapport aux autres Yo-kai.

Je souhaite une harmonisation modérée avec notre charte graphique.

Conserve impérativement :
- La silhouette.
- Les deux immenses bras mécaniques.
- Les mains noires.
- Le visage violet.
- Les yeux jaunes.
- Les dents.
- Les cornes.
- Les flammes bleues.
- La grande spirale rose centrale.
- Les motifs caractéristiques.
- Les éléments turquoise et roses inférieurs.
- Les couleurs principales.
- L'expression menaçante.

Travaille principalement sur :
- La simplification des détails internes.
- La cohérence des contours.
- La réduction des nuances superflues.
- Les aplats de couleurs.
- La lisibilité des petits motifs.
- La cohérence de l'ombrage.

Le sprite doit rester imposant : c'est notre boss final.

Ne le transforme pas en personnage simpliste ou excessivement cartoon.

### Positionnement

**Reproduis aussi fidèlement que possible le positionnement visible sur la deuxième image.**

Don Spiraton doit :
- Occuper une grande partie du terrain adverse.
- Être visuellement centré sur la zone de combat.
- Conserver ses deux bras visibles.
- Ne pas masquer la barre de vie adverse.
- Ne pas déborder sur les menus.
- Rester lisible à la résolution native GBA.

Ne te contente pas d'importer un sprite 64 × 64 si ce format le rend trop petit ou déforme ses proportions.

Étudie la meilleure solution technique compatible avec le moteur GBA, ses contraintes de tuiles, de palettes et de mémoire.

Le rendu final doit être comparé directement à la capture fournie.

### Validation artistique

Prépare :
1. Le sprite source inchangé.
2. La version harmonisée.
3. Une comparaison côte à côte.
4. Une capture réelle mGBA du rendu.
5. Une capture à la résolution native GBA.

**Présente le rendu avant de remplacer définitivement la ressource du prototype.**

N'ajoute aucun sprite overworld de Don Spiraton.

N'ajoute aucun sprite de fusion.

## 4. Activation de la finale normale

Actuellement, la scène fonctionne en diagnostic, mais le déclencheur de production utilise encore Matt.

Il faut désormais raccorder le scénario complet à la première conquête normale de la Ligue.

Déroulement obligatoire :

1. Le joueur vainc les quatre adversaires de la Ligue.
2. Il entre dans la salle du Maître.
3. Don Morléone l'attend avec plusieurs sbires.
4. Don Morléone prononce son discours.
5. Premier combat classique contre Don Morléone.
6. Matt entre dans la salle.
7. Matt soigne intégralement l'équipe.
8. Don Morléone appelle ses sbires.
9. Les sbires convergent vers lui.
10. Flash blanc.
11. Disparition des personnages pendant le flash.
12. Début du combat contre Don Spiraton.
13. Apparition de son véritable sprite.
14. Première transformation au début du premier tour, après le choix du joueur.
15. Sept transformations suivantes à la fin des tours.
16. Défaite de la huitième forme.
17. Scène de conclusion.
18. Départ de Don Morléone.
19. Intervention du Professeur Chen.
20. Inscription du joueur au Panthéon.
21. Crédits et sauvegarde.
22. Déblocage normal du postgame.

Aucun saut QA ne doit être nécessaire pour terminer ce parcours.

Conserve les outils de diagnostic isolés si utiles, mais ils ne doivent pas être accessibles au joueur dans une partie normale.

## 5. Rappel du combat contre Don Spiraton

Ne modifie pas les règles validées.

- Un seul boss.
- Huit formes différentes.
- Bouh comme première forme.
- Niveaux 56 à 63.
- Première métamorphose au début du tour 1.
- Transformations suivantes à la fin du tour.
- Sélection du meilleur contre uniquement selon le Yo-kai actuellement sur le terrain.
- Aucun accès aux autres membres de l'équipe du joueur.
- Capacités naturelles et CT compatibles uniquement.
- Nom affiché toujours DON SPIRATON.
- Huit barres : vert, orange, cyan, bleu, violet, magenta, rouge, ivoire.
- Disparition des altérations de statut à chaque transformation.
- Pas de K.O. traditionnel entre les phases.
- Pas d'expérience intermédiaire.
- Pas de changement gratuit de Yo-kai.
- Pas de capture.
- Pas de fuite.
- Pas de dégâts traversant plusieurs barres.
- Aucune neuvième forme.

Musique : **Vs. Zazelmare**.

## 6. Conclusion après la défaite de Don Spiraton

### Intention scénaristique

Après la destruction de sa huitième barre de vie, Don Spiraton est définitivement vaincu.

Le combat prend fin.

Le joueur revient dans la salle du Maître.

Don Morléone a retrouvé son apparence humaine habituelle.

Les sbires qui avaient fusionné avec lui ne constituent plus une menace immédiate.

Don Morléone comprend qu'il ne peut pas vaincre le joueur.

**Il reconnaît sa défaite, renonce à conquérir la Ligue et décide de prendre la fuite pour s'exiler hors de Kanto.**

Il ne meurt pas.

Il n'est pas arrêté.

Il ne reste pas dans la salle du Maître.

Il ne devient pas le Champion postgame.

### Proposition de dialogue

**DON MORLÉONE :**

« Alors... même ce pouvoir n'aura pas suffi... »

« Je pensais pouvoir soumettre toute cette région. »

« Mais tu as réussi à me vaincre... deux fois. »

« Je dois reconnaître ma défaite. »

« La Ligue est à toi. »

« Quant à moi... il est temps de quitter Kanto. »

« Nous nous reverrons peut-être un jour... »

Ces dialogues sont une proposition de base.

Respecte le ton d'un chef mafieux orgueilleux qui reconnaît la supériorité de son adversaire sans devenir soudainement gentil.

Il ne doit pas supplier le joueur, ni se transformer en personnage comique.

Adapte les coupures aux contraintes GBA sans changer le sens.

### Départ

Don Morléone quitte la salle du Maître.

Les sbires survivants se retirent également.

Utilise leurs sprites overworld existants.

Prévois des déplacements compatibles avec la carte, sans collision ni blocage.

Ne crée pas de nouvelle animation graphique.

## 7. Intervention du Professeur Chen

Après le départ de Don Morléone, le Professeur Chen intervient pour féliciter le joueur.

Dans Pokémon Rouge Feu, il réprimande normalement Matt après sa défaite.

Cette situation n'a plus de sens dans notre scénario.

Il faut donc adapter la scène.

### Dialogue proposé

**PROFESSEUR CHEN :**

« Incroyable... »

« Tu as non seulement remporté la Ligue... »

« Mais tu as aussi mis fin aux ambitions de Don Morléone ! »

« Tu as prouvé que tu méritais ta place parmi les plus grands Dresseurs. »

« Viens avec moi. »

« Il est temps d'inscrire tes Yo-kai au Panthéon ! »

Matt peut réagir brièvement à la victoire du joueur, en conservant sa personnalité compétitive.

Ne transforme pas cette conclusion en longue cinématique.

### Panthéon

Conserve les mécanismes existants :
- Enregistrement des six Yo-kai.
- Reconnaissance du joueur comme Champion.
- Crédits.
- Sauvegarde.
- Passage au postgame.

Supprime toute référence incohérente à Matt comme Champion vaincu lors de cette première conquête.

## 8. Exil de Don Morléone et rencontre postgame

Je souhaite désormais que Don Morléone soit retrouvable après sa défaite.

### Principe

Après avoir fui Kanto, Don Morléone s'est installé dans **une petite maison située hors de Kanto**.

Le joueur pourra le retrouver pendant le postgame.

Il ne dirige plus ouvertement la Mafiamille dans la région.

Il a reconnu sa défaite, mais conserve sa personnalité et son esprit de compétition.

### Emplacement

**L'emplacement exact de cette maison reste à définir.**

Étudie les cartes postgame existantes, notamment les Îles Sevii, pour proposer un emplacement cohérent avec son exil.

Ne construis pas une nouvelle maison et ne modifie pas une carte existante sans mon accord.

Présente deux ou trois possibilités, avec leurs avantages techniques et scénaristiques.

### Combat revanche

Lorsque le joueur lui parle, Don Morléone peut proposer une revanche.

Cette revanche reprend **uniquement son premier combat classique de la Ligue**, jamais le combat contre Don Spiraton.

Équipe :

| Yo-kai | Niveau |
|---|---|
| Mademoaiselle | 56 |
| Sorcophage | 57 |
| Doyen Doyagari | 56 |
| Fourchelangue | 58 |
| Tristos | 57 |
| Turboss | 60 |

Conserve les attaques et les paramètres validés pour ce premier combat.

Ne crée pas de nouvelle équipe plus puissante sans autorisation.

Musique : **vs. The Ghoulfather**.

### Répétabilité

Le joueur doit pouvoir refaire ce combat plusieurs fois.

Après chaque victoire, Don Morléone reste disponible dans la maison.

Il ne disparaît pas définitivement.

Il ne se transforme plus en Don Spiraton.

Il n'appelle aucun sbire.

Il ne déclenche aucun événement de Ligue.

La revanche ne doit pas modifier les flags du Panthéon ou du postgame.

Prévois un dialogue court permettant d'accepter ou de refuser le combat.

Ne rédige pas définitivement ce dialogue avant validation.

## 9. Matt devient le Champion postgame

Après la première victoire du joueur, Matt finit par conquérir la Ligue et prend sa place.

Lors des revanches postgame, c'est Matt qui attend le joueur dans la dernière salle.

Conserve ses trois variantes d'équipe selon le starter.

Conserve les niveaux de revanche existants.

Musique : **Decisive Battle**.

Ne réactive pas Don Spiraton lors des revanches.

Ne réintroduis pas l'ancien dialogue du Professeur Chen réprimandant Matt.

## 10. Musiques à conserver

| Situation | Musique |
|---|---|
| Premier combat Don Morléone | vs. The Ghoulfather |
| Don Spiraton | Vs. Zazelmare |
| Matt Champion postgame | Decisive Battle |
| Revanche Don Morléone dans sa maison | vs. The Ghoulfather |

Ne modifie pas les autres affectations musicales.

Préserve les 31 OST et leurs données audio.

## 11. Tests obligatoires

### Graphismes

- Comparaison du sprite original et harmonisé.
- Respect de la charte graphique des autres Yo-kai.
- Positionnement fidèle à l'image fournie.
- Absence de débordement sur l'interface.
- Animation de Morphing depuis le véritable sprite.
- Vérification des palettes et de la mémoire vidéo.

### Première conquête

- Accès normal à la salle du Maître.
- Premier combat Don Morléone.
- Arrivée et soin de Matt.
- Convergence des sbires.
- Flash blanc.
- Entrée sans Poké Ball adverse.
- Huit formes de Don Spiraton.
- Victoire finale.
- Retour à la carte.
- Conclusion.
- Fuite de Don Morléone.
- Intervention de Chen.
- Panthéon.
- Crédits.
- Sauvegarde et rechargement.

### Postgame

- Matt présent comme Champion.
- Trois variantes de son équipe.
- Musique Decisive Battle.
- Don Morléone accessible uniquement après sa défaite.
- Maison postgame sans blocage.
- Combat revanche classique.
- Répétabilité du combat.
- Aucun retour de Don Spiraton.
- Aucun impact indésirable sur les autres événements de Sevii.

### Stabilité

- Compilation publique et privée.
- ROM privée sous 32 Mio.
- Contrôle EWRAM et IWRAM.
- Contrôle des palettes.
- Absence de corruption des sauvegardes.
- Tests de défaite et de reprise.
- Tests avec une équipe normale, pas seulement des équipes QA renforcées.
- Régression des événements Mafiamille et d'Argenta.

## 12. Méthode de travail

Procède en trois étapes.

### Étape A — Graphismes et préparation

Prépare la version harmonisée du sprite et son aperçu mGBA.

Audite les emplacements possibles de la maison postgame.

Présente les deux éléments pour validation avant leur intégration définitive.

### Étape B — Finalisation de la Ligue

Après validation du sprite :

- Intègre le véritable sprite de Don Spiraton.
- Raccorde la finale à la progression normale.
- Implémente la conclusion.
- Adapte Chen et Matt.
- Raccorde le Panthéon.
- Vérifie les crédits et la sauvegarde.

### Étape C — Postgame

Après validation de l'emplacement :

- Installe Don Morléone dans la maison.
- Ajoute son dialogue de revanche.
- Réutilise son équipe classique.
- Vérifie la répétabilité.
- Confirme Matt comme Champion postgame.

## 13. Livrables

Fournis :

1. Le commit et la branche de travail.
2. Les fichiers modifiés.
3. Le sprite original et la version harmonisée.
4. Une capture mGBA du sprite en combat.
5. Une comparaison avec les autres Yo-kai.
6. Les propositions d'emplacement pour la maison.
7. Le rapport des tests.
8. Les tailles des ROM.
9. Les éventuelles régressions.
10. Les éléments restant à valider.

**Ne déclare pas la finale terminée tant que la première conquête complète ne fonctionne pas dans une partie normale, sans saut QA.**

Ne fusionne aucune branche.

## 14. Objectif final

Je souhaite que Don Morléone constitue le véritable antagoniste principal de notre aventure.

Son combat final doit être mémorable grâce à la révélation de Don Spiraton et à ses huit transformations adaptatives.

Après sa défaite, il reconnaît la victoire du joueur et s'exile hors de Kanto.

Le joueur devient Maître de la Ligue.

Matt prend ensuite sa place lors des revanches postgame.

Enfin, Don Morléone reste accessible dans une petite maison pour des combats classiques répétés.

**Tu peux commencer par l'étape A. Présente les propositions artistiques et géographiques avant de poursuivre les parties qui en dépendent.**