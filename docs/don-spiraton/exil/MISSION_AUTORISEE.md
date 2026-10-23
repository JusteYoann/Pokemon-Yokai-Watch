# POKÉMON × YO-KAI WATCH — MAISON D'EXIL DE DON MORLÉONE

## 1. Validation de l'emplacement

Je valide officiellement la maison du **Chemin d'O, Île 6**, comme lieu d'exil de Don Morléone après sa défaite contre le joueur.

Carte concernée : `SixIsland_WaterPath_House2`.

Cette maison possède actuellement un habitant avec lequel le joueur peut discuter.

**Je souhaite que Don Morléone remplace cet habitant après la conclusion de la première Ligue.**

Il ne doit pas y avoir deux PNJ dans la maison.

## 2. Comportement avant et après la Ligue

### Avant la défaite de Don Spiraton

- La maison conserve son habitant d'origine.
- Son dialogue et son comportement restent inchangés.
- Don Morléone n'est pas présent.
- Aucun événement supplémentaire n'est déclenché.

### Après la défaite de Don Spiraton

- L'habitant d'origine disparaît de la maison.
- Don Morléone apparaît à sa place.
- Il utilise son sprite overworld Mafiamille déjà intégré.
- Il reste présent lors des visites suivantes.
- Il ne disparaît pas après une revanche.
- Il ne peut pas apparaître avant la victoire définitive contre Don Spiraton.

Utilise les flags de progression existants lorsque cela est possible.

**La seule victoire contre la première équipe de Don Morléone ne doit pas suffire à débloquer sa présence dans la maison.**

## 3. Placement et déplacements

Réutilise l'intérieur existant :

`SixIsland_WaterPath_House2`

Position de référence de l'habitant : `(7,4)`.

Place Don Morléone à cet emplacement, ou à une case adjacente si cela améliore son orientation et la conversation.

Ne modifie pas :
- Les murs.
- Le mobilier.
- Les portes.
- Les collisions.
- Les warps.
- L'extérieur de la maison.

Aucune nouvelle carte ne doit être créée.

Vérifie que le joueur peut entrer, parler à Don Morléone et ressortir sans blocage.

## 4. Dialogue et revanche

Don Morléone a reconnu sa défaite et s'est exilé hors de Kanto.

Il conserve sa personnalité de chef mafieux orgueilleux, mais ne cherche plus à conquérir la Ligue.

Je souhaite qu'il propose un combat revanche lorsque le joueur lui parle.

### Dialogue proposé

**DON MORLÉONE :**

« Tiens, tiens... »

« Je ne pensais pas te revoir ici. »

« Depuis notre affrontement, j'ai eu le temps de réfléchir. »

« Kanto ne m'appartient plus... »

« Mais je n'ai pas perdu le goût du combat ! »

« Que dirais-tu d'une revanche ? »

**Choix : OUI / NON**

Si NON :

« Une autre fois, peut-être... »

Si OUI :

« Parfait ! Voyons si tu es toujours à la hauteur ! »

Ces dialogues peuvent être adaptés aux contraintes d'affichage de Pokémon Rouge Feu, sans en modifier le sens.

## 5. Combat revanche

La revanche doit réutiliser **exactement le premier combat classique contre Don Morléone à la Ligue**.

| Yo-kai | Niveau |
|---|---:|
| Mademoaiselle | 56 |
| Sorcophage | 57 |
| Doyen Doyagari | 56 |
| Fourchelangue | 58 |
| Tristos | 57 |
| Turboss | 60 |

Réutilise les attaques, objets et paramètres du combat validé.

Musique : **vs. The Ghoulfather — Yo-kai Watch 3**.

Interdictions :
- Aucun combat contre Don Spiraton.
- Aucune fusion.
- Aucun sbire.
- Aucun système de huit barres.
- Aucune nouvelle équipe inventée.
- Aucune modification de son équipe de la Ligue.

## 6. Combat répétable

Le joueur doit pouvoir accepter une nouvelle revanche après chaque victoire.

Le combat ne doit pas être définitivement désactivé par un flag de victoire de Dresseur.

Après le combat :
- Le joueur revient dans la maison.
- Don Morléone reste à sa place.
- Il est possible de lui reparler.
- Il peut proposer une nouvelle revanche.
- Les flags de Ligue restent inchangés.

Si le joueur perd, applique les règles normales de défaite, sans corrompre la progression.

## 7. Contraintes de progression

L'apparition de Don Morléone doit dépendre de la victoire complète contre Don Spiraton et de la progression postgame appropriée.

Ne débloque pas prématurément l'accès à l'Île 6.

Ne modifie pas les conditions normales de navigation vers les Îles Sevii.

Préserve les autres événements de l'île.

## 8. Tests mGBA

Teste au minimum :

1. Maison avant la première conquête : habitant original présent.
2. Maison après la victoire contre le premier Don Morléone, mais avant Don Spiraton : habitant original toujours présent.
3. Maison après la victoire finale : Don Morléone présent, habitant original absent.
4. Entrée et sortie de la maison.
5. Dialogue OUI / NON.
6. Première revanche.
7. Deuxième revanche consécutive.
8. Sauvegarde et rechargement.
9. Défaite contre Don Morléone.
10. Absence d'impact sur les revanches de Matt à la Ligue.

Teste les versions publique et privée.

Vérifie que la ROM privée reste sous 32 Mio.

## 9. Branche et sécurité

Travaille sur :

`feature/boss-final-don-spiraton`

Pars du dernier commit distant confirmé, en préservant les modifications déjà réalisées.

Ne modifie pas `master`.

Ne fusionne aucune branche.

Ne remplace aucun graphisme validé.

Ne modifie aucune OST en dehors de l'affectation prévue pour ce combat.

## 10. Livrables

Fournis :
- Le commit publié.
- Les fichiers modifiés.
- Une capture réelle mGBA de la maison avant la Ligue.
- Une capture réelle mGBA avec Don Morléone après la Ligue.
- Le résultat des tests de répétabilité.
- Le bilan des flags utilisés.
- Les tailles des ROM.
- Les éventuelles limitations.

**Tu peux implémenter cette modification.**

Il s'agit d'une validation définitive de l'emplacement et du remplacement conditionnel de l'habitant.

Ne considère pas pour autant l'ensemble de la finale comme terminé : l'intégration définitive du sprite de Don Spiraton, la conclusion et la validation complète de la Ligue restent des étapes distinctes.