# Traduction française intégrale — chantier en cours

Base avant traduction : `4672b88e19d02acbb068cc3106d24fb2521c9542`, branche `dev/reconstruction-finalisation`. Kanto, les identifiants, les équipes, les correspondances d'espèces, les ressources graphiques et les 26 OST sont conservés. Les noms propres géographiques existants ne sont pas renommés par cette mission.

## Lot 1 effectivement traduit et vérifié

461 messages de combat, puis interfaces principales et messages partagés. Les tables de travail sont dans `data/localisation/fr/` : combats, menus, PC/résumé, connexion/crédits, prix et messages communs. Les traductions nommées conservent exactement les variables et codes entre accolades ; seuls les textes et leur cadrage changent. Les libellés communs utilisent une liste explicite de chaînes complètes, excluant les noms des dresseurs, noms d'espèces et mots contextuels Easy Chat. Les noms d'attaques et talents déjà validés sont préservés.

Les noms des types sont localisés en conservant la limite native de six caractères, avec un point pour les abréviations : INSEC., SPECT., ÉLECT., TÉNÈB. Les modèles de descriptions de statuts et de talents en combat sont traduits ; les menus du Parc Safari aussi. Les crédits conservent les noms des auteurs et organismes et traduisent les fonctions, sans attribuer les créations originales à une autre personne.

Les messages d'obtention, échanges, PC, Pension, boutiques, soins, Surf, contrôles de Badges et évaluations du Médallium sont traduits. L'évaluation de Chen rappelle que le partage d'expérience est permanent : aucun changement de récompense ou de mécanique. La révélation du spectre utilise Castelius Max, conformément au SPECIES_MAROWAK réellement lancé par l'événement.

## Vérifications réalisées

- Compilation privée réussie avec les 26 OST : **31 272 243 octets**, sous 32 Mio. Empreinte et preuve que les modifications des sources sont textuelles : [PRESERVATION_LOT1.json](PRESERVATION_LOT1.json).
- mGBA : textes français réellement liés, encodage des accents, largeur native des libellés contrôlés, ouverture par commandes des écrans Médallium, équipe et Sac. [14 contrôles](interfaces/INTERFACE_FR_MGBA.json).
- mGBA : 14 messages affichés par le moteur de dialogue sur la carte, avec variables préparées. [Rapport](dialogues/TEST_MGBA.json), [captures](dialogues/PLANCHE.png). Ce sont des fixtures de rendu, pas un parcours des PNJ ni une validation de toutes les pages.
- Cadrage de 29 dialogues avec la police native et des bornes prudentes pour les noms et variables. Les menus à coordonnées fixes sont exclus du recadrage automatique. [Détails](CADRAGE_DIALOGUES.json).

Les captures ont été ouvertes et examinées. Une compilation et ces contrôles ciblés ne prouvent pas la traduction ni le bon cadrage de tous les écrans du jeu.

## Couverture et suite

[Inventaire initial](COUVERTURE_AVANT.json) : 11 727 chaînes potentielles, 5 047 candidates anglaises et 457 candidates japonaises. L'analyse inclut aussi des textes hérités inutilisés, des descriptions des espèces hors Médallium et des noms propres. Les nombres ne sont donc ni un pourcentage de traduction ni un compteur de répliques réellement accessibles.

[État courant](COUVERTURE.json) et [inventaire des chaînes](INVENTAIRE.csv) servent au suivi. La détection de langue est une heuristique : une chaîne non signalée n'est pas automatiquement française. Les objets générés depuis JSON et les textes inscrits dans des graphismes nécessitent une vérification distincte.

**La traduction complète n'est pas encore terminée.** Restent notamment la majorité des dialogues de cartes, les aides et tutoriels, les messages de la Salle Union, les notices du Médallium et les mots Easy Chat accessibles. Les textes Yo-kai déjà en français doivent rester cohérents avec les scènes programmées. Les tests de parcours et le contrôle des fenêtres étroites se poursuivent avec les lots suivants.

## Lot 2 — objets et début de l’aventure

298 fiches d’objets traduites (noms et descriptions), neuf fiches personnalisées préservées exactement. Les descriptions respectent les effets de la génération III, notamment Baie Sitrus (30 PV) et Balle Lumière (Attaque Spéciale de Passpa). Les noms occupent au maximum 13 caractères plus la terminaison dans le champ natif de 14 octets ; les abréviations sont explicites et terminées par un point. Les noms complets restent dans les données de localisation. Les noms canoniques sont issus de la liste publique PokéAPI, relus pour Rouge Feu ; les descriptions sont rédigées pour ce moteur, sans importer les effets de générations plus récentes. [Licence](../../../data/localisation/fr/POKEAPI_LICENSE.md).

Les 25 natures, 86 lignes de descriptions de Baies héritées et les modèles du journal de reprise sont traduits. Les paramètres des Baies et le fonctionnement du journal sont inchangés. Les dialogues des cinq cartes de Pallet Town et des sept cartes de Viridian City/Forest sont traduits. Les textes de Chen proposent bien Komasan (Feu), Padrezo (Électrik) et Kappacap (Eau), conformément aux trois scripts existants. Le discours sur le Médallium reste limité à 151 espèces. Les conseils sur les types ne décrivent plus les anciens Pokémon lorsque leurs remplaçants ont un autre type.

Vérifications supplémentaires :

- [298 noms et descriptions d’objets liés, 15 panneaux natifs du Sac dans mGBA](objets/TEST_MGBA.json), [captures](objets/PLANCHE.png). Les panneaux sont des fixtures de rendu : ils ne déplacent pas réellement des objets clés dans la mauvaise poche.
- [Les trois scripts de proposition des starters](starters/TEST_MGBA.json), leurs espèces réellement préparées et leurs textes de choix dans mGBA ; [captures](starters/PLANCHE.png). Le test ne prétend pas avoir terminé les trois combats du rival.
- [26 messages de combat](combats/TEST_MGBA.json) développés avec leurs variables, contrôlés dans le tampon natif de 300 octets et rendus par la fenêtre de combat ; [captures](combats/PLANCHE.png). Il s’agit de fixtures de messages, pas de 26 effets de combat déclenchés. Un long message pédagogique français a été raccourci pour rester dans ce tampon.
- Compilation privée réussie, toujours 31 272 243 octets. [Préservation des sources, effets d’objets, scripts, graphismes et audio](PRESERVATION_LOT2.json). Les rapports d’émulation portent l’empreinte du jalon précis testé ; tous n’ont pas été générés après la dernière modification textuelle.

Le journal de reprise et les dialogues de Viridian restent à parcourir en situation réelle. Le chantier intégral se poursuit ; ces vérifications ciblées ne valident pas toute l’aventure.
