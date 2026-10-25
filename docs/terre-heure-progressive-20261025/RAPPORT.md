# Terr’heure : déclenchement différé, transition et sortie

[Vidéo mGBA avec le son](declenchement-porte-sortie-mgba.mp4) · [ROM de test](Pokemon_Yokai_Watch_Beta_0.1_Terre_Heure_6min_Entrees.gba)

Branche dédiée : `fix/terre-heure-apparition-progressive-20261025`. Aucune fusion sur `master`.

## Déclenchement

Un seul tirage par visite de grotte éligible :

| Situation | Sans Short Oni | Avec Short Oni |
|---|---:|---:|
| Aventure | 5 % | 15 % |
| Postgame | 10 % | 30 % |

Le bonus dépend d’un Short Oni tenu dans l’équipe au moment du tirage. Plusieurs porteurs ne cumulent pas leurs bonus. Les tirages utilisent un échantillonnage uniforme sans biais de modulo.

Un succès programme secrètement un délai aléatoire de **30 à 150 pas inclus**. Attendre immobile ne le réduit pas. Un échec reste consommé pendant toute la visite. Le tirage et le compteur survivent aux changements d’étage, aux menus et à une sauvegarde suivie de « Continuer ». Sortir entièrement du massif annule le compteur et autorise un nouveau tirage à la prochaine visite. Une Terr’heure déjà rencontrée ne peut pas se relancer pendant cette même visite.

La première rencontre est garantie tardivement par un tirage favorable à la **Route Victoire**, si aucune Terr’heure n’a encore été rencontrée. Les grottes précédentes appliquent les taux ordinaires : la première grotte n’impose pas systématiquement l’événement. La première rencontre est enregistrée au déclenchement, même si le joueur échoue ensuite.

Un compteur arrivé à échéance attend un contexte sûr : contrôle du joueur, absence de dialogue/combat/fondu, carte et composante compatibles. Sur une case d’escalier ou de sortie, il attend la transition ; une sortie complète annule cet événement en attente. Les petits étages incompatibles et la Grotte Bakuku restent exclus.

## Priorité sur les Dresseurs

Le pas est compté avant la détection des Dresseurs. Le moteur natif vérifiant aussi leur regard pendant l’animation d’un déplacement, leur détection est suspendue pendant le dernier pas programmé, jusqu’à sa fin. La Terr’heure peut ainsi commencer avant la création d’une tâche d’approche ou d’un dialogue de Dresseur.

Les cinématiques de carte gardent leur priorité et un déclenchement déjà dû reste en attente. Après la Terr’heure, les Dresseurs reviennent sans perdre leur disponibilité ni leurs drapeaux de victoire. Une protection de position empêche une détection automatique tant que le joueur reste à sa position de retour ; une rencontre ultérieure normale peut démarrer leur combat.

Le format des sauvegardes est conservé. Trois variables existantes inutilisées portent l’état de visite (`0x40FA`), le compteur/attente (`0x40FB`) et la protection du retour (`0x40FC`).

## Autres corrections demandées

- **Transition simultanée** : noir et blanc, apparition des nuages jaunes et dissolution progressive des habitants pendant 300 VBlanks, soit au moins 5 secondes. Le texte attend la fin des trois effets. Nathan conserve ses couleurs. La disparition des habitants utilise une dissolution de pixels pour permettre une brume indépendante sur le matériel GBA.
- **Six minutes** : le chrono commence à `6:00`, après l’introduction. La conversion évite le débordement arithmétique à cette durée. À zéro, le combat reste imposé ; si le menu est ouvert, il débute au retour au terrain.
- **Patrouilles** : jusqu’à huit, avec renfort de présence près de la caméra. Les patrouilles lointaines sont recyclées hors écran ; les nouveaux placements évitent les cases occupées, les escaliers et les passages étroits. L’Oni tient compte des autres objets dans sa recherche de chemin. Toutes les patrouilles disparaissent après sa défaite.
- **Chrono et trous de texture** : les caractères étaient stockés à `0x0600F000`, également occupé par une carte de tuiles du décor. Les deux usages s’écrasaient mutuellement. Les douze tuiles du chrono occupent désormais une zone libre à `0x0600D000`, séparée des cartes du décor. L’enregistrement final ne reproduit plus les motifs parasites ni les trous signalés.

Les OST, les équipes des Oni, la porte et ses effets, les récompenses et la progression de quête sont conservés.

## Vidéo demandée

Enregistrement continu de **50,28 secondes**, à vitesse normale, avec sortie audio directe de mGBA :

- vers 00:02 : déclenchement ;
- vers 00:08–00:14 : transformation et disparition des habitants ;
- vers 00:22 : exploration et patrouilles ;
- vers 00:32 : interaction avec la porte et ouverture ;
- vers 00:40 : retour à la grotte normale et commandes rendues ;
- fin vers 00:50 : plus de dix secondes après ce retour.

L’équipe, la position, les chaussures de course et une visite réussie juste avant son dernier pas sont préparées avant l’enregistrement. Une graine native reproductible choisit une porte sur le même étage. **Pendant la capture : uniquement des commandes de manette, aucune téléportation, aucun déplacement forcé de porte/Oni, aucune modification du chrono, aucune coupe ni accélération.** La porte est atteinte et ouverte par déplacement et interaction réels. Les détails et empreintes sont dans [ENREGISTREMENT_SORTIE.json](ENREGISTREMENT_SORTIE.json).

## Vérifications

**65 contrôles réussis sur la même ROM** :

| Série | Contrôles | Résultats |
|---|---:|---|
| Déclenchement et priorité | 17 | [TESTS_DECLENCHEMENT.json](TESTS_DECLENCHEMENT.json) |
| Transition, patrouilles, chrono, six minutes écoulées | 7 | [TESTS.json](TESTS.json) |
| Cartes, collisions, porte, menus, Flash et expiration | 41 | [TESTS_CARTES_PORTE.json](cartes/TESTS_CARTES_PORTE.json) |

Les tests incluent les seuils natifs exacts de 30 et 150 pas, réussite/échec, étages, sortie, nouveau tirage, bonus sans cumul, attente sous verrouillage, attente sur un escalier, sauvegarde native puis « Continuer », ainsi qu’un **véritable déplacement à la manette dans le regard d’Iris au pas déclencheur**. Après retour, 180 frames sans entrée vérifient l’absence de rencontre fantôme, puis un déplacement ultérieur déclenche réellement son combat.

Les autres vérifications comprennent 48 comparaisons des tuiles du chrono en VRAM pendant les déplacements, les six minutes réellement écoulées dans mGBA, et le retrait de l’Oni et des huit patrouilles après le résultat de victoire. Les paramètres déterministes appartiennent aux scripts de test ; aucun mode de triche n’est compilé dans la ROM.

## Fichiers concernés

- `src/terre_heure.c`, `src/terre_heure_fog.c`, `src/overworld.c` : transition, densité, durée, affichage et état de visite.
- `src/field_control_avatar.c`, `src/trainer_see.c` : comptage et priorité des événements.
- `include/terre_heure.h`, `include/constants/vars.h` : interfaces et variables persistantes.
- `tools/yokai/tester_terreur_declenchement_mgba.py`, `tester_terreur_progressive_mgba.py`, `tester_terreur_cartes_mgba.py` : fixtures ciblées.
- `tools/yokai/enregistrer_terreur_sortie_mgba.py` et `enregistrer_terreur_complete_mgba.py` : enregistrements reproductibles.

## ROM et limites

ROM : **33 493 107 octets**. SHA-256 :

```text
6fa4668ae1c5cfb3562ae769044e03d69b6473375dce326f20ad65cb6450e4bc
```

Les deux compilations, standard et avec les OST privées intégrées, réussissent. La ROM fournie est celle avec les OST, utilisée par tous les tests et par la vidéo. EWRAM : 261 620 octets ; IWRAM : 30 912 octets, sans augmentation des réservations fixes de RAM.

La limite native de seize objets et la géométrie du terrain peuvent réduire le nombre de patrouilles sur certaines cartes ; leur visibilité permanente dans chaque case d’un couloir n’est pas garantie.

La quête dédiée Nyada/Démophage n’existe pas encore sur cette branche : son drapeau est explicitement réservé et n’est jamais posé par le scénario actuel. La protection de la Grotte Azurée est vérifiée avec ce marqueur ; la présence d’un acteur Nyada visible protège également sa carte. Cela ne constitue pas un test d’une cinématique Nyada/Démophage absente du dépôt, et cette quête n’a pas été reconstruite.

Ces fixtures ciblées et cette vidéo ne constituent pas une nouvelle campagne complète de l’aventure à 100 %.
