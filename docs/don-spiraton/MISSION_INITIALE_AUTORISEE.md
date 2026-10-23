# POKÉMON × YO-KAI WATCH — VALIDATION DE L'AUDIT ET IMPLÉMENTATION DU BOSS FINAL

## 1. Contexte

Dépôt : `JusteYoann/Pokemon-Yokai-Watch`

Dernier commit de référence connu : `d2f590d8b`

Branche de développement précédente : `feature/argenta-morleone-musique`

Nouvelle branche souhaitée : `feature/boss-final-don-spiraton`

Nous avons examiné ton audit de faisabilité concernant le remplacement du Champion final par Don Morléone et le combat spécial contre Don Spiraton.

**J'autorise le démarrage de l'implémentation technique, sous réserve des validations artistiques précisées ci-dessous.**

Vérifie d'abord les commits et les branches actuels. Pars du dernier état validé du projet, en préservant les modifications Mafiamille, Argenta et musicales.

Ne modifie pas directement `master`, `feature/mafiamille-kanto` ou `audio/integration-31-ost`.

Ne fusionne aucune branche.

## 2. Nouvelle structure de la Ligue

### Première conquête

Le joueur traverse les quatre affrontements de la Ligue, puis entre dans la salle du Maître.

Il découvre Don Morléone accompagné de plusieurs sbires Mafiamille.

La finale comprend :

1. Dialogue de Don Morléone.
2. Combat classique contre Don Morléone.
3. Arrivée de Matt et soin complet de l'équipe.
4. Fusion de Don Morléone avec ses sbires.
5. Transformation en Don Spiraton.
6. Combat spécial à huit formes.
7. Défaite définitive de Don Spiraton.
8. Conclusion scénaristique et Panthéon.

Matt ne doit pas être affronté comme Champion pendant cette première conquête.

Ses autres combats de rival restent inchangés.

Ne transforme pas encore les cartes de la Ligue en Temple Céleste.

## 3. Premier combat — Don Morléone

Utilise cette proposition d'équipe issue de l'audit :

| Yo-kai | Niveau |
|---|---|
| Mademoaiselle | 56 |
| Sorcophage | 57 |
| Doyen Doyagari | 56 |
| Fourchelangue | 58 |
| Tristos | 57 |
| Turboss | 60 |

Conserve les capacités légales vérifiées pendant l'audit.

Ce combat utilise :

`vs. The Ghoulfather — Yo-kai Watch 3`

Ne modifie pas les équipes de Don Morléone à Céladopole, à la Sylphe ou à Jadielle.

L'ancien combat bonus de Don Morléone à Sevii doit être retiré proprement, sans supprimer les autres événements postgame ni les ressources réutilisées ailleurs.

## 4. Dialogue d'introduction

Don Morléone attend le joueur dans la salle du Maître.

**DON MORLÉONE :**

« Te voilà enfin... »

« Je savais que tu serais mon dernier obstacle. »

« Depuis notre première rencontre, tu n'as cessé de contrecarrer mes plans. »

« Je dois l'admettre... Tu as gagné mon respect. »

« Mais tu arrives trop tard. »

« Il ne me reste qu'une victoire à remporter pour inscrire mes Yo-kai au Panthéon. »

« Je deviendrai le nouveau Maître de la Ligue. »

« Et Kanto appartiendra à la Mafiamille ! »

Respecte les intentions et le texte. Adapte seulement les coupures nécessaires à l'interface GBA.

## 5. Arrivée de Matt et fusion

Après la première défaite de Don Morléone, Matt entre dans la salle.

**MATT :**

« Hé ! J'ai raté quelque chose ? »

« Attends... Tu l'as vraiment battu ?! »

« Tss... J'aurais préféré m'en charger moi-même. »

« Mais c'est pas encore terminé. »

« Tiens, laisse-moi soigner tes Yo-kai ! »

Matt restaure intégralement les PV, PP et statuts des Yo-kai du joueur.

**DON MORLÉONE :**

« Je vois... »

« Tu ne me laisses donc plus le choix. »

« MAFIAMILLE ! À MOI ! »

Les sbires se précipitent vers lui et fusionnent avec lui.

Don Morléone prend sa véritable apparence de Don Spiraton.

Réutilise les graphismes Mafiamille validés. Ne crée pas d'apparence alternative non autorisée.

## 6. Don Spiraton : un seul boss, huit formes

Don Spiraton n'est pas une équipe de huit Yo-kai.

Il s'agit d'un seul adversaire possédant huit couches de PV, huit transformations et une identité permanente.

Son nom affiché reste toujours :

**DON SPIRATON**

Exemple :

« Don Spiraton utilise Tempête de Sable ! »

Même lorsqu'il emprunte l'apparence de Bouh.

Aucun envoi de Poké Ball entre les formes.

Aucun K.O. traditionnel entre les phases.

Aucun gain d'expérience intermédiaire.

Aucune proposition gratuite de changement de Yo-kai.

La victoire ne se déclenche qu'après la huitième barre épuisée.

## 7. Première transformation — début du tour 1

Le combat commence en affichant le véritable sprite de Don Spiraton.

Le joueur sélectionne normalement sa première action.

**Au début du premier tour, avant toute attaque**, Don Spiraton utilise automatiquement une métamorphose gratuite.

Elle ne consomme pas son action et ne dépend pas de sa Vitesse.

Réutilise l'animation de Morphing de Pokémon Rouge Feu.

Le message annonce l'espèce empruntée :

« Don Spiraton se transforme en [nom du Yo-kai] ! »

Cette première forme doit être volontairement faible et prédéfinie.

**Son identité n'est pas encore validée : prépare un emplacement configurable, mais ne sélectionne pas définitivement l'espèce sans mon accord.**

La véritable apparence de Don Spiraton ne compte pas comme une neuvième forme.

## 8. Transformations suivantes — FIN DU TOUR

Cette règle corrige et remplace la proposition de transformation immédiate de l'audit.

Lorsqu'une forme atteint zéro PV :

1. La phase est considérée comme vaincue, mais Don Spiraton n'est pas K.O.
2. Aucun message de K.O. traditionnel n'apparaît.
3. Si Don Spiraton n'a pas encore attaqué pendant ce tour, son action restante est annulée.
4. Le moteur termine proprement le tour, sans appliquer de dégâts de fin de tour à la forme épuisée.
5. Le Yo-kai actuellement sur le terrain est identifié.
6. Don Spiraton sélectionne son prochain contre.
7. L'animation de Morphing se déclenche.
8. Le message de transformation apparaît.
9. La nouvelle forme et sa barre de PV sont activées.
10. Le tour suivant commence normalement.

La transformation ne consomme pas de tour supplémentaire.

Le joueur ne peut pas changer gratuitement de Yo-kai entre deux formes.

Les dégâts excédentaires d'une attaque ne traversent jamais plusieurs barres de vie.

Vérifie les attaques à plusieurs coups, les dégâts résiduels, les capacités à effet différé et les changements forcés afin d'éviter tout contournement des huit phases.

## 9. Niveaux et barres de vie

| Forme | Niveau |
|---|---|
| 1 | 56 |
| 2 | 57 |
| 3 | 58 |
| 4 | 59 |
| 5 | 60 |
| 6 | 61 |
| 7 | 62 |
| 8 | 63 |

Chaque forme possède ses propres PV, statistiques, types et capacités.

Les barres de vie doivent représenter huit couches colorées superposées.

La première est verte, la deuxième orange. Propose une palette lisible pour les six suivantes.

Lorsqu'une barre est épuisée, elle disparaît et révèle la suivante.

Ne modifie pas globalement l'interface de combat des autres adversaires.

## 10. Sélection du meilleur contre

À partir de la deuxième forme, Don Spiraton sélectionne une espèce parmi les 151 Yo-kai disponibles.

**La sélection doit dépendre uniquement du Yo-kai actuellement sur le terrain.**

Elle ne doit pas analyser les autres membres de l'équipe du joueur.

Prends en compte les types, les statistiques, les résistances, la Vitesse et les attaques légalement accessibles à la forme candidate.

Une forme déjà vaincue ne peut pas être réutilisée.

L'algorithme doit être testable et ne doit pas provoquer de ralentissement perceptible.

## 11. Capacités légales

Don Spiraton peut utiliser les attaques naturellement accessibles à chaque espèce et les CT compatibles.

Il peut optimiser ses quatre attaques selon son adversaire.

Il ne peut jamais utiliser une attaque que l'espèce empruntée ne peut pas apprendre.

N'altère pas les données permanentes des 151 Yo-kai.

Le nom du combattant reste Don Spiraton, indépendamment de sa forme.

## 12. Statuts et effets temporaires

Chaque transformation supprime les altérations de statut de Don Spiraton.

Affiche un message correspondant au statut supprimé :

- « Don Spiraton n'est plus brûlé ! »
- « Don Spiraton n'est plus empoisonné ! »
- « Don Spiraton n'est plus paralysé ! »
- « Don Spiraton s'est réveillé ! »
- « Don Spiraton n'est plus gelé ! »

Si aucun statut n'était présent, n'affiche aucun message.

Examine aussi les modifications temporaires de statistiques, la confusion et les autres effets propres à l'ancienne forme.

Ne réinitialise pas arbitrairement les effets de terrain ni les états du Yo-kai du joueur.

## 13. Musiques validées

| Situation | OST |
|---|---|
| Conseil 4 | Decisive Battle |
| Don Morléone — premier combat | vs. The Ghoulfather |
| Don Spiraton — boss final | **Vs. Zazelmare** |
| Matt — Champion postgame | **Decisive Battle** |

Ces choix sont définitifs pour cette mission.

Ne remplace pas *Vs. Zazelmare* dans ses autres utilisations existantes.

Ne supprime pas *Final Battle – Are You Ready?* de la bibliothèque audio : elle peut rester disponible pour une future affectation.

## 14. Revanche postgame : Matt devient Maître

Après la victoire contre Don Spiraton, le joueur est reconnu comme Maître de la Ligue et inscrit ses Yo-kai au Panthéon.

Lors d'une visite ultérieure à la Ligue, **Matt est désormais le Champion à affronter**.

La justification scénaristique est qu'il a finalement conquis la Ligue après le départ du joueur et lui a pris sa place.

Il conserve sa personnalité compétitive et arrogante.

Dialogue proposé :

**MATT :**

« Alors, surpris de me retrouver ici ? »

« Pendant que tu te reposais sur tes lauriers, j'ai conquis la Ligue ! »

« Cette fois, c'est moi le Maître ! »

« Allez, montre-moi si tu mérites encore ton titre ! »

Utilise pour ce combat :

**Decisive Battle — Yo-kai Watch**

Préserve les équipes de revanche existantes de Matt et leurs variantes selon le starter.

Ne répète pas le combat contre Don Spiraton pendant les revanches.

Vérifie soigneusement les flags et conditions de progression pour distinguer la première conquête des visites suivantes.

## 15. Panthéon et conclusion

Après la huitième forme, Don Spiraton est vaincu définitivement.

La progression vers le Panthéon, l'enregistrement de l'équipe, les crédits, la sauvegarde et le déblocage du postgame doivent fonctionner.

Les dialogues originaux dans lesquels le Professeur Chen réprimande Matt pour avoir perdu son titre doivent être adaptés, car Matt n'est plus le Champion vaincu lors de la première conquête.

**N'invente pas encore une conclusion scénaristique complète.**

Prépare une transition technique et propose les dialogues nécessaires à une validation séparée.

## 16. Graphismes de Don Spiraton

Le visuel officiel de Don Spiraton a été fourni comme référence.

Vérifie si les contraintes de la GBA permettent une représentation fidèle et suffisamment imposante.

Prépare une proposition de sprite et d'animation de fusion.

**Ne valide pas automatiquement un sprite approximatif.**

Présente le rendu pour approbation avant son intégration définitive.

Préserve les sprites et animations existants.

## 17. Suppression de l'ancien caméo Sevii

L'ancien combat bonus contre Don Morléone n'est plus souhaité.

Retire son déclenchement et ses dialogues spécifiques après avoir vérifié leurs dépendances.

Ne supprime pas les autres événements de Sevii.

Ne supprime pas les ressources utilisées par Don Morléone dans l'aventure principale.

## 18. Méthode d'implémentation

Procède par étapes contrôlées.

### Étape A — Infrastructure

- Créer la branche dédiée.
- Préparer le système de huit phases.
- Préparer la sélection adaptative.
- Préparer les transformations de fin de tour.
- Préparer les données de combat.
- Ajouter des tests automatisés.

### Étape B — Intégration de la Ligue

- Remplacer le combat final contre Matt.
- Ajouter Don Morléone et ses sbires.
- Ajouter le premier combat.
- Ajouter l'arrivée et le soin de Matt.
- Préparer la fusion.
- Brancher le combat spécial.

### Étape C — Postgame

- Faire de Matt le Champion des revanches.
- Affecter Decisive Battle à son combat.
- Préserver ses équipes existantes.
- Adapter les conditions de progression.
- Retirer l'ancien caméo de Don Morléone.

### Étape D — Validation

- Compiler les ROM publique et privée.
- Vérifier la limite de 32 Mio.
- Tester les huit phases.
- Tester les choix de contres.
- Tester les capacités CT.
- Tester les altérations.
- Tester les transitions musicales.
- Tester la première conquête.
- Tester la revanche postgame.
- Tester les sauvegardes et le Panthéon.
- Fournir des captures réelles mGBA et un rapport détaillé.

## 19. Points soumis à validation artistique

Les éléments suivants ne sont pas encore décidés :

1. L'identité de la première forme faible.
2. Le sprite final de Don Spiraton.
3. L'animation définitive de fusion.
4. Les dialogues complets après sa défaite.
5. Les six dernières couleurs des barres de vie.

Prépare des propositions ou des prototypes isolés pour ces éléments.

Ne prends aucune décision créative définitive à ma place.

Si un élément bloque la progression, arrête uniquement la partie concernée et demande mon accord.

## 20. Contraintes absolues

- Aucun changement aux statistiques ou évolutions des 151 Yo-kai.
- Aucun changement aux trois starters.
- Aucun changement aux huit trophées.
- Aucun changement aux équipes des Champions d'Arène.
- Aucun changement aux rencontres légendaires.
- Aucun changement aux graphismes Mafiamille validés.
- Aucun changement aux OST sans rapport avec cette mission.
- Aucune fusion de branches.
- Aucun changement direct sur `master`.
- Aucun remplacement silencieux d'une mécanique demandée par une approximation.

## 21. Livrables

À chaque étape, fournis :

- Le commit et la branche.
- Les fichiers modifiés.
- Les tests réalisés.
- Les résultats des compilations.
- Les problèmes rencontrés.
- Les éléments restant à valider.

Ne présente pas un test automatisé comme une recette complète en conditions réelles.

Si une fonctionnalité n'est que partiellement opérationnelle, indique-le explicitement.

**Tu peux commencer l'implémentation technique. Respecte les validations artistiques restantes et ne fusionne aucune branche sans mon autorisation.**