# POKÉMON × YO-KAI WATCH — FINALISATION DÉFINITIVE DE LA MAFIAMILLE

## 1. AUTORISATION

Je valide officiellement les animations de marche de Don Morléone et des sbires Mafiamille.

Je valide également le nouvel emblème représentant le chapeau de Don Morléone, présenté dans les aperçus du commit :

`cee38fa5f22f95b65d63d995848c5ee94578b12c`

Tu es maintenant autorisé à procéder à l'intégration définitive des ressources graphiques, sous réserve des instructions ci-dessous.

Travaille exclusivement sur :

`feature/mafiamille-kanto`

Conserve les commits `ddcb53b10` et `cee38fa5f` comme références.

## 2. ANIMATIONS DE MARCHE — VALIDATION DÉFINITIVE

J'ai personnellement examiné les animations de marche.

**Je valide définitivement les huit animations :**

- Don Morléone : nord, sud, est, ouest.
- Sbire Mafiamille : nord, sud, est, ouest.

Aucune modification supplémentaire n'est nécessaire.

Conserve exactement les animations actuellement intégrées.

## 3. EMBLÈME OFFICIEL DE LA MAFIAMILLE

Le symbole officiel est désormais **le chapeau gris de Don Morléone avec sa bande sombre**.

Je valide le dessin proposé.

Ne le remplace pas par une tête de sbire, une lettre M ou un autre symbole.

### Casino — VALIDÉ

Intègre le chapeau sur :

- Les rouleaux des machines à sous.
- Le tableau des gains.

Les aperçus actuels sont approuvés.

Respecte les palettes et dimensions natives.

Ne modifie pas les autres symboles, les probabilités ou les gains.

### Repaire de Céladopole — VALIDÉ

Conserve le chapeau à l'emplacement de l'ancien symbole Rocket.

Le logo doit rester discret et cohérent avec le décor.

Je valide le principe de son intégration dans l'illustration d'entrée.

Ne redessine pas le bâtiment et ne modifie aucun élément sans rapport avec le symbole.

### Entrepôt des îles Sevii — NOUVELLE DÉCISION

**Je ne souhaite finalement aucun emblème sur l'entrepôt.**

Supprime complètement le « R » de la Team Rocket dans l'illustration d'entrée.

Ne le remplace ni par le chapeau, ni par une lettre, ni par un autre dessin.

Reconstitue simplement le mur ou le panneau d'origine de manière naturelle, en respectant :

- Les couleurs existantes.
- La texture du décor.
- Les contours et les ombres.
- Le style graphique de Pokémon Rouge Feu.

L'objectif est que l'emplacement ne présente aucune trace visible d'un ancien logo.

Ne retire pas d'autres éléments du décor.

Cette décision remplace les précédentes instructions concernant le symbole de l'entrepôt.

## 4. INTÉGRATION TECHNIQUE

Applique les modifications aux quatre ressources graphiques identifiées dans le rapport Mafiamille :

1. Rouleaux du Casino : remplacement du R par le chapeau.
2. Tableau des gains : remplacement du R par le chapeau.
3. Illustration du repaire : remplacement du R par le chapeau.
4. Illustration de l'entrepôt : suppression du R sans remplacement.

Utilise les ressources natives appropriées, et non de simples captures de simulation.

Vérifie les palettes, tilemaps, dimensions, compressions et contraintes GBA.

Préserve tous les éléments graphiques voisins.

## 5. TESTS FINAUX OBLIGATOIRES

Après intégration, compile les versions publique et privée.

Teste réellement les modifications dans mGBA.

Je souhaite notamment vérifier :

- Le chapeau sur les rouleaux du Casino.
- Le chapeau sur le tableau des gains.
- Le chapeau à l'entrée du repaire.
- L'absence totale de symbole à l'entrée de l'entrepôt.
- Le bon affichage des palettes.
- L'absence de corruption graphique.
- Le fonctionnement inchangé des machines à sous.
- Les animations de marche validées.
- Les rencontres avec Don Morléone et les sbires.
- La sauvegarde et le rechargement.

Fournis des captures réelles de mGBA après intégration, et pas uniquement des simulations.

Vérifie également que les anciens symboles Rocket ne subsistent plus dans les ressources concernées.

## 6. PROTECTION ABSOLUE DU RESTE DU PROJET

Ne modifie pas :

- Les 151 Yo-kai.
- Les statistiques, types et évolutions.
- Les équipes de Don Morléone.
- Les équipes des sbires.
- Les dialogues déjà validés.
- Les événements et la progression.
- Les Champions et la Ligue.
- Les musiques et ressources audio.
- Les mécaniques personnalisées.
- Les animations de marche désormais validées.

Ne touche pas à la branche audio `audio/integration-31-ost`.

Ne fusionne pas avec `master`.

Ne crée aucun nouvel élément scénaristique.

## 7. RAPPORT FINAL

Une fois le travail terminé, publie un nouveau commit sur `feature/mafiamille-kanto`.

Fournis :

- Le hash du commit final.
- La liste exacte des ressources modifiées.
- Les captures mGBA avant/après.
- Les résultats des compilations.
- Les résultats des tests.
- Les éventuelles limites ou anomalies.
- La confirmation que les animations de marche sont définitivement validées.
- La confirmation que les quatre anciens symboles R ont été traités selon mes décisions.

Mets à jour le rapport Mafiamille pour distinguer les validations artistiques terminées des tests de gameplay qui restent éventuellement à effectuer.

**Ne déclare pas qu'une traversée complète de l'aventure a été effectuée si seuls des tests ciblés ont été réalisés.**

## 8. OBJECTIF

Cette mission doit clôturer la transformation graphique de la Team Rocket en Mafiamille.

Le résultat final doit être :

- Une Mafiamille présente partout où se trouvait la Team Rocket.
- Don Morléone à la place de Giovanni.
- Des sbires et des animations définitivement validés.
- Un emblème officiel représentant le chapeau de Don Morléone.
- Un Casino et un repaire utilisant cet emblème.
- Un entrepôt discret, sans emblème.
- Aucune modification des autres éléments du jeu.

**Tu es autorisé à intégrer ces modifications, effectuer les tests et publier le résultat final sur la branche dédiée. Aucune fusion n'est autorisée.**