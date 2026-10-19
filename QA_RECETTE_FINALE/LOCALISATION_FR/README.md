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

## Lot 3 — Médallium, TV ABC et trajet jusqu’à Cerulean

Les 151 notices actives n’emploient plus les biographies anglaises des Pokémon remplacés. Elles donnent des faits vérifiables dans les sources validées : types, statistique de combat la plus élevée (hors PV) et premier talent. Il ne s’agit pas de biographies officielles Yo-kai Watch inventées. Les catégories deviennent « Yo-kai » ; un espace terminal conserve la compatibilité du lecteur de catégories de Rouge Feu révision 0. Le suffixe qui répétait « Yo-kai » est retiré. Les tailles, poids et échelles hérités sont conservés et ne sont pas certifiés par cette tâche textuelle.

[151 notices et 15 pages rendues dans mGBA](medallium/TEST_MGBA.json), [captures vérifiées](medallium/PLANCHE.png). Les drapeaux de capture sont préparés par le test ; les pages sont redessinées par les fonctions natives. L’en-tête d’habitat reste celui de la liste ouverte par la fixture : la planche n’est pas une reclassification des habitats.

Traduction de tous les textes des neuf cartes de Pewter, des routes 1 à 4 et de leurs bâtiments, de MT. MOON, des rencontres avec Matt sur la Route 22 et des dix cartes de Cerulean (310 entrées de dialogue au total dans les tables 12, 14 et 15). Les noms propres géographiques préexistants ne sont pas renommés. Les combats, gains et scripts sont inchangés. La vente de la Route 4 annonce Castelius III, l’espèce réellement donnée par le script (`SPECIES_EXEGGCUTE`), sans appliquer aveuglément la correspondance de Magicarpe.

Les 42 textes de la TV ABC et de son démonstrateur sont traduits. Les explications respectent les types réellement intégrés de Télémir, Superfouet et Saumhonni, et le Multi Exp. permanent. [13 contrôles mGBA](tv_abc/TEST_MGBA.json) : sept libellés et sélection des six émissions, avec Boîte CT accordée par la fixture pour ouvrir les deux dernières leçons. [Captures examinées](tv_abc/PLANCHE.png). Les combats pédagogiques complets ne sont pas validés ici.

Compilation privée réussie avec les 26 OST : toujours **31 272 243 octets**. [Preuve des seules modifications textuelles](PRESERVATION_LOT3.json). Restent de nombreux dialogues ultérieurs, les aides, revanches, salles de connexion et certains écrans spécifiques : aucune déclaration de traduction intégrale terminée.

## Lot 4 — aide intégrée et revanches

238 textes du Cherch’Combat et des revanches sont traduits, sans changer les équipes ni les conditions d’activation. Les conseils et allusions aux anciennes espèces sont reformulés lorsque leur remplacement n’a plus les mêmes types ou la même apparence.

Les 369 entrées de l’aide intégrée sont localisées : rubriques, questions, réponses, commandes des menus, statistiques, CT/CS et tableaux d’affinités de la génération III. L’aide explique le Multi Exp. permanent. Les contrôles numérotés et les glyphes des tableaux sont conservés. Le cadrage propre à l’aide tient compte de sa fenêtre fixe de 208 × 104 pixels, avec sept lignes au maximum ; il ne suppose pas qu’un dialogue défilant compensera un dépassement.

[Contrôles de cadrage](AIDE_CADRAGE.json), [369 textes liés et largeurs vérifiés dans mGBA](aide/TEST_MGBA.json), [onze captures examinées](aide/PLANCHE.png). L’aide s’ouvre réellement avec R ; le test autorise cette interface en mémoire dans la chambre de début de partie. Dix couples question/réponse sont ensuite affichés avec le moteur natif, sans prétendre avoir parcouru tous les menus conditionnels. Les sept lignes de l’explication des statuts restent visibles.

Compilation réussie avec les 26 OST, toujours sous 32 Mio. [Préservation du code et des scripts](PRESERVATION_LOT4.json). Les dialogues restants, liaisons, mots Easy Chat et inscriptions graphiques nécessitent encore du travail ; la traduction totale reste en cours.
