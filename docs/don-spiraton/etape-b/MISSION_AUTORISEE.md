# POKÉMON × YO-KAI WATCH — ÉTAPE B : FINALISATION COMPLÈTE DE LA LIGUE ET DE DON SPIRATON

## 1. Contexte et objectif

**Dépôt GitHub :** `JusteYoann/Pokemon-Yokai-Watch`

**Branche de travail :** `feature/boss-final-don-spiraton`

**Dernier commit confirmé :** `4289f076d`

Nous avons progressivement développé le boss final de notre ROM Pokémon Rouge Feu × Yo-kai Watch.

Plusieurs fonctionnalités ont déjà été implémentées et testées dans mGBA :

- Premier combat contre Don Morléone.
- Arrivée de Matt et soin complet de l'équipe.
- Convergence des sbires Mafiamille.
- Flash blanc et entrée en combat.
- Combat spécial contre Don Spiraton.
- Huit transformations adaptatives.
- Huit couches de PV colorées.
- Première forme prédéfinie : Bouh.
- Transformations suivantes en fin de tour.
- Matt comme Champion lors des revanches postgame.
- Maison d'exil de Don Morléone sur l'Île 6.
- Revanche répétable contre Don Morléone dans cette maison.

Cependant, **la première conquête normale de la Ligue n'est pas encore entièrement activée et terminable**.

Les tests précédents reposaient notamment sur des déclenchements diagnostiques et des états de progression préparés.

### Objectif de cette mission

Transformer les fonctionnalités déjà développées en une finale complète et accessible normalement.

Le parcours attendu est :

**Conseil 4 → Don Morléone → Matt soigne l'équipe → Fusion → Don Spiraton → Défaite du boss → Exil de Don → Professeur Chen → Panthéon → Crédits → Postgame.**

Cette mission est autorisée pour l'implémentation.

Ne recommence pas les systèmes existants. Termine leur intégration.

---

## 2. Protection du dépôt

Travaille exclusivement sur :

`feature/boss-final-don-spiraton`

Avant toute modification :

1. Vérifie l'état du dépôt local.
2. Vérifie le dernier commit distant.
3. Identifie les modifications locales éventuellement non publiées.
4. Préserve les travaux existants.
5. Confirme que le prototype de Don Spiraton et la maison d'exil sont présents.

Ne réalise aucune opération Git destructive.

Ne modifie pas directement `master`.

Ne fusionne aucune branche.

Préserve intégralement :

- Les 151 Yo-kai existants.
- Leurs statistiques, types, évolutions et capacités.
- Les trois starters.
- Les huit trophées.
- Les huit Arènes.
- Les rencontres légendaires.
- Les graphismes Mafiamille validés.
- La cinématique d'Argenta.
- Les 31 OST intégrées.
- Les événements des Îles Sevii hors du périmètre demandé.

Ne fusionne pas la branche audio expérimentale.

---

# PARTIE A — INTÉGRATION DÉFINITIVE DU SPRITE DE DON SPIRATON

## 3. Sprite harmonisé validé

Nous avons validé la direction artistique du sprite harmonisé présenté dans l'étape A.

**Commit graphique de référence :** `9bfc27089`

Référence :

`docs/don-spiraton/phase-a/`

Utilise le sprite harmonisé déjà réalisé.

Ne génère pas un nouveau Don Spiraton.

Ne redessine pas arbitrairement son apparence.

### Caractéristiques de référence

- Toile native : 128 × 96 pixels.
- Silhouette opaque : 112 × 76 pixels.
- Palette : 15 couleurs opaques + transparence.
- Format graphique compatible GBA.
- Assemblage actuel : deux objets 64 × 64 et deux objets 64 × 32.
- Position de référence : centre logique `(176,34)`.

L'aperçu réel mGBA de l'étape A constitue notre référence de cadrage.

### Positionnement

Don Spiraton doit apparaître :

- Sur le terrain adverse.
- Avec ses deux bras mécaniques visibles.
- Avec son visage clairement reconnaissable.
- Avec sa grande spirale centrale.
- Dans une position similaire à notre capture validée.
- Sans recouvrir les menus ou les barres de vie.

L'aperçu précédent recadrait quatre lignes au sommet des cornes.

**Vérifie s'il est possible de conserver ces quatre lignes sans réduire sensiblement la taille du boss ni dégrader le cadrage.**

Si une correction mineure est possible, applique-la.

Si elle nécessite une réduction importante, conserve le cadrage validé et signale cette limite.

### Direction artistique

Conserve :

- Les contours sombres.
- Les ombrages par aplats.
- Les pixels nets.
- Les couleurs caractéristiques.
- Le visage violet.
- Les flammes bleues.
- Les bras mécaniques.
- Les mains noires.
- Les motifs dorés.
- La spirale magenta.
- Les éléments turquoise et roses.

Ne modifie aucun autre sprite de Yo-kai.

---

## 4. Intégration du grand sprite dans le moteur

L'aperçu mGBA utilisait une composition de quatre objets graphiques.

Cette composition doit désormais devenir la véritable représentation initiale de Don Spiraton pendant le combat.

Vérifie notamment :

- Le chargement des quatre objets.
- Leur synchronisation.
- Leurs palettes.
- Leur priorité d'affichage.
- Leur positionnement.
- Leur libération en mémoire.
- Leur compatibilité avec les animations.
- Leur comportement lors d'une défaite.
- Leur disparition pendant Morphing.
- L'absence de résidus graphiques après le combat.

Le sprite ne doit pas être seulement un élément décoratif superposé au véritable adversaire.

Il doit fonctionner comme la représentation initiale du boss.

### Attention à la mémoire

Le dernier rapport indiquait :

- EWRAM statique : 261 124 / 262 144 octets.
- IWRAM privée : 29 888 / 32 768 octets.
- ROM privée : 31 658 511 octets.

La marge EWRAM est particulièrement faible.

Évite les nouveaux buffers statiques importants.

Privilégie la réutilisation des ressources existantes lorsque c'est possible.

Documente toute augmentation de mémoire.

---

# PARTIE B — MORPHING ET COMBAT FINAL

## 5. Première transformation

Le combat commence avec le véritable sprite de Don Spiraton.

L'interface affiche :

**D. SPIRATION**

Cette abréviation est volontaire et validée par le créateur afin d'éviter que le nom soit coupé dans l'interface GBA.

Ne cherche pas à remplacer ce nom par une version trop longue.

### Déroulement

1. Le sprite de Don Spiraton apparaît.
2. La musique Vs. Zazelmare joue.
3. Le message d'apparition est affiché.
4. Le joueur choisit sa première action.
5. Au début du tour 1, avant les attaques, Don Spiraton se transforme en Bouh.
6. L'animation native de Morphing se déclenche.
7. Bouh apparaît à la place de Don Spiraton.
8. Le combat continue normalement.

La transformation ne consomme pas son action.

Elle ne dépend pas de la Vitesse.

Elle ne constitue pas une neuvième forme.

## 6. Effet sonore original de Morphing

**Nouvelle précision définitive : conserve le son original de l'attaque Morphing de Pokémon Rouge Feu.**

Ce son doit accompagner :

- La première transformation en Bouh.
- Les sept transformations suivantes.

Réutilise l'effet sonore natif et sa synchronisation avec l'animation.

N'ajoute pas de nouveau son personnalisé.

Ne joue pas systématiquement le cri de l'espèce empruntée.

La musique Vs. Zazelmare doit continuer en arrière-plan.

Vérifie dans mGBA que le son est effectivement audible et qu'il ne se déclenche pas deux fois.

Ne considère pas une simple vérification du code comme une écoute humaine.

## 7. Conservation des huit phases

Les règles validées restent inchangées.

| Forme | Niveau |
|---|---:|
| 1 — Bouh | 56 |
| 2 | 57 |
| 3 | 58 |
| 4 | 59 |
| 5 | 60 |
| 6 | 61 |
| 7 | 62 |
| 8 | 63 |

À partir de la deuxième forme, Don Spiraton choisit automatiquement le meilleur contre parmi les 151 Yo-kai.

Il analyse **uniquement le Yo-kai actuellement sur le terrain**.

Il ne consulte jamais les autres membres de l'équipe du joueur.

Une espèce déjà utilisée ne peut pas être réutilisée.

Ses attaques doivent être légalement accessibles par apprentissage naturel ou CT compatible.

Le nom affiché reste D. SPIRATION, quelle que soit sa forme.

### Transformations de fin de tour

Lorsqu'une barre atteint zéro :

- Pas de K.O. classique.
- Pas d'expérience intermédiaire.
- Pas de Poké Ball.
- Pas de changement gratuit pour le joueur.
- Pas d'attaque supplémentaire injustifiée.
- Transformation à la fin du tour.
- Nouvelle espèce, nouveaux types, statistiques et attaques.
- Nouvelle barre de vie complète.
- Suppression des altérations de statut de l'ancienne forme.

Les huit couleurs validées sont :

**Vert → Orange → Cyan → Bleu → Violet → Magenta → Rouge → Ivoire.**

La victoire définitive intervient uniquement après la huitième barre.

---

# PARTIE C — ACTIVATION DE LA PREMIÈRE FINALE NORMALE

## 8. Remplacement de Matt par Don Morléone

Lors de la première conquête de la Ligue, le joueur doit rencontrer Don Morléone dans la dernière salle.

Matt ne doit pas être le Champion à affronter lors de cette première visite.

Il conserve ses autres apparitions dans l'aventure.

### Mise en scène

Don Morléone attend le joueur, accompagné de plusieurs sbires Mafiamille.

Il reconnaît sa valeur et explique qu'il compte devenir Maître de la Ligue pour contrôler Kanto.

Conserve les dialogues déjà approuvés et préparés dans le projet.

Ne les remplace pas par de nouvelles répliques inventées.

### Premier combat

Utilise l'équipe existante :

| Yo-kai | Niveau |
|---|---:|
| Mademoaiselle | 56 |
| Sorcophage | 57 |
| Doyen Doyagari | 56 |
| Fourchelangue | 58 |
| Tristos | 57 |
| Turboss | 60 |

Musique :

**vs. The Ghoulfather — Yo-kai Watch 3**

Ne modifie pas cette équipe.

## 9. Intervention de Matt

Après la victoire contre Don Morléone :

1. Le premier combat se termine.
2. Matt entre dans la salle.
3. Il réagit à la victoire du joueur.
4. Il soigne intégralement les six Yo-kai de l'équipe.
5. Don Morléone reprend la parole.

Le soin doit restaurer :

- Les PV.
- Les PP.
- Les altérations de statut.

Conserve les dialogues déjà définis.

## 10. Fusion de la Mafiamille

Don Morléone s'écrie :

**« MAFIAMILLE ! À MOI ! »**

Les sbires convergent vers lui.

Un flash blanc recouvre l'écran.

Le flash masque leur disparition.

Le jeu passe directement au combat contre Don Spiraton.

### Contraintes

- Aucun sprite overworld de Don Spiraton.
- Aucun sprite de fusion.
- Aucun envoi adverse par Poké Ball.
- Capture interdite.
- Fuite interdite.
- Apparition de son véritable sprite de combat.
- Musique Vs. Zazelmare.

Réutilise la cinématique déjà testée.

Ne reconstruis pas une seconde version indépendante.

---

# PARTIE D — CONCLUSION APRÈS DON SPIRATON

## 11. Défaite définitive

Lorsque la huitième barre atteint zéro :

1. Don Spiraton est vaincu.
2. Le combat prend fin normalement.
3. Le joueur revient dans la salle du Maître.
4. Don Morléone apparaît sous son apparence overworld habituelle.
5. Matt est toujours présent.
6. Les sbires ne constituent plus une menace.

Ne déclenche pas un deuxième combat.

Ne bloque pas la progression.

Ne rejoue pas l'animation de fusion.

## 12. Don Morléone reconnaît sa défaite

Il reste fier et orgueilleux, mais reconnaît que le joueur est plus fort que lui.

Utilise le dialogue suivant, avec seulement les adaptations de coupures nécessaires aux boîtes GBA.

**DON MORLÉONE :**

« Alors... même ce pouvoir n'aura pas suffi... »

« Je pensais pouvoir soumettre toute cette région. »

« Mais tu as réussi à me vaincre... deux fois. »

« Je dois reconnaître ma défaite. »

« La Ligue est à toi. »

« Quant à moi... il est temps de quitter Kanto. »

« Nous nous reverrons peut-être un jour... »

### Départ

Après son discours :

- Don Morléone quitte la salle.
- Les sbires quittent également les lieux.
- Matt reste présent pour la transition suivante.
- Aucun personnage ne bloque les déplacements.
- Aucun sprite ne reste affiché par erreur.

Don Morléone n'est ni arrêté ni tué.

Il décide de s'exiler hors de Kanto.

Son exil est déjà représenté par sa présence conditionnelle dans la maison du Chemin d'O, sur l'Île 6.

Ne modifie pas cette maison.

---

## 13. Intervention de Matt

Après le départ de Don Morléone, Matt peut réagir brièvement.

Il doit reconnaître l'exploit du joueur tout en conservant sa rivalité.

Dialogue proposé :

**MATT :**

« Tss... Tu l'as vraiment fait. »

« Tu as battu Don Morléone... et ce monstre ! »

« Mais ne prends pas trop la grosse tête ! »

« La prochaine fois, c'est moi qui serai le Maître ! »

Cette intervention doit rester courte.

Elle prépare son retour comme Champion postgame.

## 14. Arrivée du Professeur Chen

Le Professeur Chen arrive ensuite pour féliciter le joueur.

Il ne doit plus réprimander Matt comme dans Pokémon Rouge Feu.

**PROFESSEUR CHEN :**

« Incroyable... »

« Tu as non seulement remporté la Ligue... »

« Mais tu as aussi mis fin aux ambitions de Don Morléone ! »

« Tu as prouvé que tu méritais ta place parmi les plus grands Dresseurs. »

« Viens avec moi. »

« Il est temps d'inscrire tes Yo-kai au Panthéon ! »

Conserve les intentions de ces dialogues.

Adapte uniquement leur présentation aux contraintes du moteur.

Ne crée pas de scène supplémentaire non demandée.

---

# PARTIE E — PANTHÉON ET POSTGAME

## 15. Panthéon

Après l'intervention du Professeur Chen :

- Le joueur accède au Panthéon.
- Ses Yo-kai sont enregistrés.
- Le jeu reconnaît sa première victoire.
- Les crédits se lancent.
- La sauvegarde fonctionne.
- Le postgame est débloqué.

**Ce parcours doit fonctionner sans saut QA ni manipulation artificielle des flags.**

Préserve le fonctionnement natif du Panthéon autant que possible.

Vérifie les flags de victoire du combat classique contre Don Morléone et du combat contre Don Spiraton.

La progression ne doit pas considérer la première victoire contre Don Morléone comme une victoire finale.

## 16. Matt Champion postgame

Après la première conquête, Matt finit par prendre la place du joueur comme Maître de la Ligue.

Lors des revanches :

- Matt attend le joueur dans la dernière salle.
- Ses variantes d'équipe selon le starter sont conservées.
- Ses niveaux de revanche restent inchangés.
- Sa musique est **Decisive Battle**.
- Don Spiraton ne réapparaît pas.

Préserve les tests déjà réalisés sur ses trois variantes.

## 17. Maison d'exil

La maison du Chemin d'O, Île 6, est déjà implémentée.

Commit de référence :

`4289f076d`

Ne modifie pas son fonctionnement.

Vérifie simplement qu'après une véritable première victoire :

- Don Morléone remplace l'habitant original.
- Son dialogue OUI/NON fonctionne.
- Son premier combat classique est répétable.
- Sa musique est vs. The Ghoulfather.
- Il ne se transforme jamais en Don Spiraton.
- Le joueur peut sauvegarder et recharger normalement.

Le déblocage doit toujours dépendre de la victoire contre Don Spiraton et du Panthéon.

---

# PARTIE F — VALIDATION TECHNIQUE

## 18. Tests mGBA obligatoires

Je veux une recette complète dans mGBA, pour les ROM publique et privée.

### Parcours de la première conquête

1. Vaincre le quatrième adversaire de la Ligue.
2. Entrer normalement dans la dernière salle.
3. Déclencher le dialogue de Don Morléone.
4. L'affronter.
5. Le vaincre.
6. Voir Matt arriver.
7. Recevoir le soin complet.
8. Voir les sbires converger.
9. Voir le flash blanc.
10. Entrer dans le combat contre Don Spiraton.
11. Voir son véritable sprite.
12. Sélectionner la première action.
13. Voir la transformation en Bouh.
14. Vérifier l'animation et le son de Morphing.
15. Vaincre les huit formes.
16. Voir la conclusion.
17. Voir Don Morléone quitter la salle.
18. Voir le Professeur Chen.
19. Accéder au Panthéon.
20. Déclencher les crédits.
21. Sauvegarder.
22. Recharger la partie.
23. Accéder au postgame.

Ne considère pas des flags injectés comme une validation de ce parcours complet.

### Tests complémentaires

Vérifie :

- Les huit barres de vie.
- Les changements de formes.
- La sélection adaptative.
- Les attaques CT.
- Les dégâts excédentaires.
- Les coups multiples.
- Les dégâts résiduels.
- Les statuts.
- Les K.O. simultanés.
- Les défaites du joueur.
- Les sauvegardes.
- Les transitions musicales.
- La libération des sprites et palettes.
- Les trois variantes de Matt.
- La maison d'exil.
- Les combats ordinaires après Don Spiraton.

## 19. Équilibrage

Les tests précédents utilisaient parfois des équipes QA de niveau 100.

Ces tests sont utiles pour vérifier le fonctionnement technique, mais ils ne prouvent pas que le combat est équilibré.

Effectue également des essais avec des équipes représentatives d'une fin d'aventure normale.

Évalue :

- La difficulté du premier Don Morléone.
- L'intérêt du soin de Matt.
- La durée du combat contre Don Spiraton.
- L'efficacité des contres adaptatifs.
- Le risque de blocage stratégique.
- La difficulté de la huitième forme.

Ne modifie pas les statistiques des 151 Yo-kai pour équilibrer le boss.

Présente les résultats et propose des ajustements séparément si nécessaire.

## 20. Compilations et mémoire

Compile :

- La ROM publique.
- La ROM privée avec les 31 OST.

Vérifie :

- La limite de 32 Mio.
- L'EWRAM.
- L'IWRAM.
- La mémoire vidéo.
- Les palettes.
- Les ressources audio.
- La sauvegarde Flash.
- Les éventuels dépassements de mémoire.

Les 31 OST doivent être préservées.

Ne supprime pas des ressources validées pour libérer de l'espace sans mon accord.

---

# PARTIE G — PUBLICATION ET LIVRABLES

## 21. Méthode de développement

Procède par jalons contrôlés :

**Jalon 1 — Sprite et Morphing**

Intègre le véritable sprite, l'animation et le son natif.

Teste leur fonctionnement réel.

**Jalon 2 — Première conquête**

Active le scénario normal et raccorde les deux combats.

Teste l'ensemble de la cinématique.

**Jalon 3 — Conclusion et Panthéon**

Intègre la défaite de Don Morléone, son départ, Matt, Chen, le Panthéon et les crédits.

**Jalon 4 — Recette complète**

Teste le parcours normal, les revanches, la maison d'exil et les sauvegardes.

À chaque jalon :

- Crée un commit identifiable.
- Publie-le sur la branche dédiée.
- Vérifie sa présence sur GitHub.
- Fournis les résultats des tests.
- Signale les problèmes restants.

## 22. Livrables finaux

Je souhaite recevoir :

1. Les commits publiés.
2. La liste des fichiers modifiés.
3. Des captures réelles mGBA.
4. Une animation ou vidéo du Morphing depuis le grand sprite.
5. Une capture de la conclusion.
6. Une capture du Panthéon.
7. Les rapports de tests publics et privés.
8. Les tailles des ROM.
9. Les bilans EWRAM/IWRAM.
10. La liste des éventuelles limitations.
11. Une confirmation explicite que la première conquête normale est jouable sans raccourci QA.

Ne présente jamais un test isolé comme une validation complète de l'aventure.

## 23. Contraintes finales

- Aucun changement de branche non autorisé.
- Aucune fusion.
- Aucun changement direct sur `master`.
- Aucun changement aux 151 Yo-kai.
- Aucun changement aux huit Arènes.
- Aucun changement aux rencontres légendaires.
- Aucun changement aux graphismes Mafiamille.
- Aucun changement à la maison d'exil validée.
- Aucun changement non demandé aux 31 OST.
- Aucun nouveau sprite overworld de Don Spiraton.
- Aucun nouveau système de combat alternatif.
- Aucune simplification silencieuse des huit formes.
- Aucun raccourci QA dans le parcours normal.
- Aucune modification scénaristique arbitraire.

Si une contrainte technique empêche de respecter une fonctionnalité, explique précisément le problème et propose une solution avant de remplacer le comportement demandé.

## 24. Objectif final

**Cette mission doit transformer Don Spiraton d'un prototype technique en véritable boss final jou