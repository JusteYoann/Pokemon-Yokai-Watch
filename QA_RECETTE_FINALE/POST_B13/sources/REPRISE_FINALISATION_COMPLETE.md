# REPRISE DU CHANTIER — FINALISATION COMPLÈTE DU ROM HACK

Tu viens de terminer une première session de travail sur `dev/reconstruction-finalisation`, au commit `9c550849e`.

Cependant, **je ne considère absolument pas le cahier des charges B13 comme terminé**.

Je veux que tu reprennes maintenant l'intégralité du cahier des charges transmis et que tu travailles sur **TOUTES les tâches restantes**, et pas seulement sur les problèmes musicaux.

## 1. Priorités absolues : son et graphismes

**Ambiance sonore :**
- Remplacer presque toutes les musiques Pokémon par des OST Yo-kai Watch.
- Réutiliser intelligemment les morceaux pour respecter les 32 Mio.
- Assurer une continuité musicale entre les villes, leurs bâtiments ordinaires (y compris centres de soins, boutiques et laboratoire de Chen) et certaines routes voisines.
- Réduire les écarts de volume entre musiques Pokémon et Yo-kai Watch.
- Réduire les bruitages de menu trop forts.
- Revoir les cris et les effets sonores de combat.
- Résoudre les problèmes de boucles musicales encore signalés.
- Vérifier les anciennes musiques inutilisées qui pourraient être retirées.

**Graphismes :**
- Finaliser la vérification visuelle des 151 sprites front et back.
- Corriger les tailles et cadrages incohérents, notamment Pitou, Baku, Cigalopin, Komasan, Komaous et Nihilistik.
- Harmoniser toutes les icônes d'équipe.
- Retravailler les nouveaux sprites overworld pour qu'ils correspondent au style de Rouge Feu.
- Corriger la taille de Léo/Jibanyan et vérifier celle d'Usapyon.
- Corriger Misterre : retirer ses éléments verts ressemblant à des yeux et supprimer sa bouche, sans refaire le reste du sprite.

## 2. Introduction et présentation du jeu

Je veux que tu travailles également sur les éléments du début du jeu qui n'ont pas encore été finalisés :

- **Nouvelle introduction cinématique** inspirée de l'ambiance mystérieuse de Yo-kai Watch, courte, réussie et adaptée à la GBA.
- **Nouvel écran titre**, sans le logo Pokémon Rouge Feu ni Dracaufeu, avec une véritable identité Pokémon × Yo-kai Watch.
- **Remplacement de Pikachu par Jibanyan** sur l'écran d'aide initial.
- Habillage et musiques de démarrage cohérents avec l'univers Yo-kai Watch.

Ne dévoile pas les grandes surprises scénaristiques, les boss et les Yo-kai légendaires dans l'introduction.

## 3. Traduction française intégrale

Termine la traduction de tous les textes visibles :

- Dialogues et événements.
- Menus et interfaces.
- Messages de combat.
- Noms et descriptions des attaques.
- Objets et CT/CS.
- Médallium.
- Évolutions.
- Fin du jeu et postgame.

Corrige également « Usapion » en « Usapyon » dans les dialogues concernés.

Il ne doit quasiment plus rester de texte Pokémon ni de texte anglais destiné au joueur.

## 4. Médallium

- Corriger le classement des 151 Yo-kai par habitat.
- Kappa parmi les Yo-kai des rivières.
- Poissons et créatures marines parmi les Yo-kai de la mer.
- Réserver la catégorie des Yo-kai rares aux espèces réellement exceptionnelles.
- Traduire les noms des catégories et les commandes encore en anglais.
- Vérifier toutes les entrées sans modifier accidentellement leur numérotation.

## 5. Gameplay et événements

- **Conserver le Multi Exp. permanent.**
- Examiner l'équilibrage de Pierre et la possibilité de remplacer Passpa par Nanpart.
- Vérifier les événements personnalisés déjà implémentés.
- Préserver les combats spéciaux, les rencontres légendaires, les évolutions et le scénario.
- Ne pas lancer les quêtes supplémentaires précédemment reportées.

## 6. Optimisation et stabilité

- Ne jamais dépasser **33 554 432 octets**.
- Auditer les anciennes musiques et ressources graphiques Pokémon réellement inutilisées.
- Éliminer les ressources inutiles uniquement si cela ne crée aucune régression.
- Conserver une marge mémoire pour les dernières finitions.
- Effectuer des tests réels dans mGBA, en complément des vérifications automatiques.
- Préserver la compatibilité des sauvegardes autant que possible.

## 7. Organisation attendue

Je souhaite que tu :

1. Relises le cahier des charges B13 complet.
2. Vérifies ce qui est réellement terminé et ce qui reste à faire.
3. Établisses une liste de suivi exhaustive.
4. Reprennes les corrections immédiatement.
5. Traites les tâches par lots cohérents avec des commits intermédiaires.
6. Continues au-delà de la seule partie musicale et des sprites de combat.
7. Prépares une nouvelle bêta privée reconstruisible sur mon Windows.
8. Fournisses un rapport indiquant précisément les modifications réalisées, les preuves de test et les éléments encore incomplets.

**Ne marque pas une tâche comme terminée simplement parce que le code compile ou qu'un script passe : je veux une vérification du résultat visible ou audible en jeu lorsque c'est pertinent.**

Mon objectif est de terminer ce ROM hack dans son ensemble, pas de multiplier les petites sessions limitées à quelques corrections.

**N'interromps pas volontairement le chantier après avoir traité seulement une partie des demandes.** Si une limite de session t'oblige à t'arrêter, sauvegarde et publie proprement ton avancement, puis fournis un état précis permettant de reprendre immédiatement.

La priorité reste très clairement :

**1. Ambiance sonore  
2. Qualité et cohérence des sprites  
3. Introduction et présentation  
4. Traduction et Médallium  
5. Gameplay, optimisation et validation finale**

Je veux maintenant que tu avances sur l'ensemble de ces points.