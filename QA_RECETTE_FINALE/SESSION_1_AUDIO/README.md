# Session 1/4 — ambiance sonore

**Verdict : chantier audio avancé, non entièrement terminé.** Branche `dev/reconstruction-finalisation`. Aucun nouveau travail graphique, d’introduction, de titre, de traduction ou de gameplay dans cette session. Le point de sauvegarde préalable `11ae692cb` conserve les changements commencés avant cette nouvelle consigne. `master` est resté à `037335f4c725d7c9aecdac87066f2002b4bd7e14`.

## Résultat intégré

- **19 OST actives**, contre 18 au début de session. Nate’s House utilise un cycle long de86,4 secondes, précédé de son introduction jouée une fois. Le motif récurrent de19,2 secondes a été rejeté comme boucle complète. Les 18 anciens DPCM n’ont pas changé.
- **405 cartes** utilisent des OST privées actives ; 18 attendent encore Blossom Heights et utilisent son repli natif ; 2 gardent leur silence prévu. Les 425 en-têtes compilés ont été comparés aux sources. Cela ne signifie pas que 425 cartes ont été parcourues.
- **187 fichiers de cartes** réaffectés : uniquement le champ musical. Réutilisation des pistes existantes aux Îles Sevii, sur l’Océane, dans les arènes, le Manoir, la Centrale, les forêts, les ruines et les bâtiments de route. Les centres et boutiques ordinaires partagent leur thème extérieur ; les exceptions de scénario restent distinctes.
- **64 anciens appels musicaux** du moteur ou des scripts redirigés vers les OST partagées, sans recopier les échantillons. Les identifiants dédiés à Domniscian, Don Morleone, Enma et aux autres thèmes spéciaux restent conservés.
- Calibration des 19 pistes sur **une introduction et un cycle complets rendus dans mGBA** : de −29,2 à −28,9 LUFS, zéro échantillon saturé. Les premières mesures de 12 secondes étaient insuffisantes : Infinite Tunnel et Take Care commencent doucement puis deviennent plus forts. La correction conserve cette dynamique plutôt que d’amplifier leurs seules introductions. Aucun réencodage supplémentaire des18 pistes existantes.

## Bruitages : règle définitive appliquée

Les 255 bruitages Pokémon, les cris et les fanfares fonctionnelles restent présents. L’ancienne demande de nouveaux bruitages Yo-kai est annulée. Les réglages d’atténuation précédemment mesurés sont conservés ; aucune banque sonore originale n’est modifiée. Le résolveur natif a vérifié 273 identifiants de bruitages/fanfares sans remplacement de leur pointeur.

Les jingles de récompense, capture et victoire restent natifs. Les autres exceptions inventoriées sont la célébration du Panthéon, la présentation de la TV ABC, son bruit d’accordage et les anciennes séquences d’introduction/soin inutilisées. Les dernières restent dans les sources ; une référence source ne prouve pas qu’elle soit encore exécutée. Voir la table complète plutôt que d’affirmer la disparition de toute musique Pokémon.

## Tableaux

- [Toutes les 425 cartes](AFFECTATIONS_425_CARTES.csv) : identifiant, nom de l’OST, disponibilité effective ou repli.
- [Moteur, jingles et replis](AFFECTATIONS_MOTEUR_ET_JINGLES.csv) : toute la table musicale, y compris les séquences natives conservées.
- [Personnages, combats et événements](AFFECTATIONS_EVENEMENTS.csv).
- [Références dans les sources](REFERENCES_MUSICALES_SOURCES.csv) : localisation et résolution ; accessibilité réelle non déduite automatiquement.
- [Modifications des cartes](MODIFICATIONS_CARTES.json), [périmètre préservé](PERIMETRE_PRESERVE.json), [provenance des 19 DPCM](PROVENANCE_19_OST.json).

## Essais réellement effectués

Les campagnes finales ci-dessous utilisent la même ROM privée, identifiée plus bas. Nouvelle partie initialisée aux boutons ; positions, drapeaux, équipes ou appels musicaux isolés sont des fixtures explicitement documentées. Aucune partie complète n’est revendiquée.

| Contrôle | Résultat | Preuve |
|---|---|---|
|19 pistes, cinq boucles chacune | **95 retours validés**, introductions non rejouées ; corrélation audio native/référence minimale 0,952 | `boucles-finales/TEST_MGBA.json` |
| Bruitage de sélection, cri et sauvegarde Flash pendant les lectures |19 pistes testées ; audio reconnu après les effets | même rapport |
|19 cycles complets, volumes |−29,2 à −28,9 LUFS ; aucune saturation | `CYCLES_19_OST_FINAUX.json` |
| Portes réelles aux boutons | **64 franchissements**, même thème et horloge avançante, sans pause/redémarrage | `portes/TEST_MGBA.json` + captures |
| Connexions ville/route et laboratoire |6 franchissements, dont Palette/Route1 et Carmin/Route11 | `connexions/CONTINUITE_MGBA.json` |
| Fanfares |33 scénarios : les 14 fanfares sur Patrol Mission, puis une récompense sur chacune des 19 pistes ; pause puis reprise du curseur sans remise à zéro | `FANFARES_MGBA.json` |
| Exploration→combat sauvage→victoire→exploration | Combat gagné aux boutons ; musique restaurée ; aucun écrêtage sur les extraits ; allié non participant reçoit de l’EXP | `transition-sauvage-finale/TEST_MGBA.json` + captures |
| Routage |64 alias démarrent réellement ; alias→thème explicite sans redémarrage ; cinq grands combats sélectionnent leur thème prévu | `ROUTAGE_MGBA.json` |
| Sources→ROM |425 affectations compilées conformes ;19 échantillons privés identiques au manifeste | `CARTES_COMPILEES.json`, `LIAISON_19_OST.json` |

Les huit scénarios d’Ariane ont aussi été rejoués : refus, victoire, sac plein, retrait différé, revanches, sauvegarde et défaite (`ariane/TEST_ARIANE_MGBA.json`). Ils portent sur le jalon musical intermédiaire `cd36cffe…`, avant le dernier ajustement des gains, et ne sont pas présentés comme huit nouveaux combats sur la ROM finale.

Les premières fixtures de portes ont rencontré des scènes de première visite : Matt aux Îles 4/6, Léo/Ciléo à l’Île 1, colis de Chen à Jadielle. La progression est désormais préparée explicitement. Aucun script du jeu n’a été modifié pour les contourner. Le premier essai exécutant zéro porte a été rejeté et archivé dans `diagnostics/`. La campagne finale exige au moins 40 franchissements et en réussit 64.

## Compilation et stockage

Compilations publique et privée réussies. ROM privée de cette session :

- Nom local : `session1-final.gba`, conservée hors du dépôt public.
- Taille : **27 712 771 octets**, soit **26,43 Mio**.
- Marge avant 32 Mio : **5 841 661 octets**, soit **5,57 Mio**.
- SHA-256 : `5d6151756916f9e28ad0e1c8a0527d9174a52cdf7b6381680a77ebc10b9aefc2`.

[Bilan machine et limites](BILAN_SESSION.json). La ROM, les sauvegardes et les enregistrements audio ne sont pas publiés. Les captures PNG et mesures JSON sont publiques. Les statistiques, équipes, évolutions, scripts de progression, ressources graphiques et Multi Exp. sont préservés ; celui-ci est aussi vérifié dans le combat natif. Aucun nouveau profil de livraison Windows B13 n’est créé ou falsifié.

## Reconstruction privée

Reprendre l’installation et la préparation des WAV documentées dans `../POST_B13/audio/RECONSTRUCTION_PRIVEE.md`. Les empreintes des sources restent verrouillées ; utiliser le générateur actuel et un nouveau dossier privé :

```sh
python3 tools/yokai/generer_audio_prive.py --full-source-dir /chemin/prive/full-sources --output /chemin/prive/session1-integration --jobs 2
make -j4 YOKAI_AUDIO_DIR=/chemin/prive/session1-integration
```

Le générateur produit19 pistes actives, sans choix automatique de boucle à la compilation. Sans ressources privées, la compilation publique utilise ses replis natifs et produit une bande-son différente. Aucune ressource protégée supplémentaire n’est nécessaire aux seules réaffectations.

Les outils `tester_session1_*_mgba.py` rejouent les campagnes. Définir `YOKAI_QA_ROM` vers la ROM privée, son ELF de même nom, et `YOKAI_AUDIO_DIR` vers le dossier de DPCM pour les comparaisons. `mesurer_cycles_session1_mgba.py --numbers 1,2,3,4,6,7,11,15,17,21,22,23,24,26,27,28,29,30,31` mesure tous les cycles. Les médias restent externes.

## Travail audio restant

**Une poursuite du chantier audio est nécessaire pour les trois sélections suivantes :**

1. Enma Track 5, dialogue : aucune reprise longue stable suffisamment établie. Le combat d’Enma utilise déjà Vs. Zazelmare 6, actif et testé.
2. Blossom Heights 12 : la ressemblance au début de 43,2 secondes s’effondre ensuite ; le prétendu cycle de86,4 secondes n’est pas confirmé. Dix-huit cartes conservent donc son repli natif.
3. Final Battle 25, Matt Champion : reprise candidate de 153,6 secondes trop locale ; repli natif du Champion conservé.

Les sources sont présentes : il ne s’agit pas de fichiers perdus. Les mesures détaillées sont dans `BOUCLES_NON_VALIDEES.json`. Un montage musical validé ou une meilleure référence de boucle est nécessaire avant d’activer ces morceaux ; aucune répétition arbitraire d’un court motif n’est intégrée.

**Limites restantes :** absence d’écoute humaine de la bande-son, absence de profilage sur une vraie GBA et absence de parcours intégral de l’aventure. Les mesures, captures et essais mGBA ne remplacent pas ces validations. Les 64 portes et 6 connexions ne couvrent pas toutes les maisons, toutes les transitions surf/vélo, tous les téléporteurs ni tous les événements. Le jeu n’est pas déclaré prêt pour une version finale.

## Complément ultérieur : 20e OST et routage intégral des BGM

La demande ultérieure de remplacer tous les fonds musicaux est documentée dans [AUDIO_COMPLEMENT](../AUDIO_COMPLEMENT/README.md). Ce nouveau jalon intègre Blossom Heights sous forme de montage explicite de phrase, à écouter humainement ; il atteint20 OST, route les104 identifiants BGM vers des samples Yo-kai privés et conserve les bruitages/jingles fonctionnels. Les résultats de cette ancienne session restent historiques : consulter le nouveau rapport pour les substitutions temporaires Enma Track/Final Battle, les mesures et la dernière empreinte de ROM.
