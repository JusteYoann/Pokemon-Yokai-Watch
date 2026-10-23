# Intégration expérimentale de 31 OST

**Dernière vérification :** [validation des cinq gains privés](VALIDATION_GAINS_5/README.md).
Cinq corrections approuvées et remesurées dans mGBA, compilation publique
strictement inchangée. Enma reste en lecture unique par décision explicite.
Chantier audio arrêté jusqu'à nouvel ordre ; aucune fusion.
Les bilans suivants sont historiques.

**État actuel :** la [variante C de Final Battle](FINAL_BATTLE_C/README.md) est
activée expérimentalement et testée dans le combat prolongé de Matt, après
validation explicite du raccord. La [correction précédente](CORRECTION_BOUCLES/README.md)
a ajouté la boucle de Katies House. Enma Track reste en lecture unique.
Le catalogue CSV est à jour ; le bilan ci-dessous décrit le premier jalon historique.

Branche **`audio/integration-31-ost`**, créée exactement depuis
`6f143452a026a41c08f1db38f9809959809a31b6`. Premier commit d'intégration :
`a1fb07c86`. Aucune fusion avec une branche principale.

**31 morceaux sont liés et leur lecture a été vérifiée dans mGBA. Le chantier
des boucles reste incomplet : trois nouveaux morceaux jouent une seule fois.**
Cette version sert aux essais ; elle ne constitue pas une version finale.

## Mesures réellement obtenues

| Mesure | Valeur |
|---|---:|
| ROM privée de référence, 26 OST | 31 589 579 octets |
| ROM privée expérimentale, 31 OST | **31 589 579 octets**, environ 30,13 Mio |
| Limite matérielle conservée | 33 554 432 octets, 32 Mio |
| Marge jusqu'à cette limite | 1 964 853 octets |
| Remplissage FF vérifié avant les graphismes | **6 064 420 octets** |
| Section privée ajoutée, données et structures alignées | **4 334 472 octets** |
| Remplissage restant avant les graphismes | **1 729 948 octets** |
| ROM publique, sans ressources privées | 16 777 216 octets |
| RAM privée EWRAM / IWRAM | 261 052 / 29 888 octets, inchangées |

L'espace vérifié va de `0x087376DC` à `0x08D00000`. La nouvelle section finit
à `0x08B59A64`. Les cinq fichiers complets auraient coûté 5 595 065 octets,
plus environ 205 octets de structures/alignement : ils tenaient déjà dans la
zone. Les deux cycles musicaux complets identifiés réduisent ensuite le coût.
Aucune donnée Pokémon n'a été supprimée, ni aucune fréquence réduite.

Le script de liaison place `.yokai_audio_gap` après les données multiboot et
contient une assertion interdisant de dépasser `0x08D00000`. Un essai réel de
liaison avec un objet temporaire volontairement trop grand a échoué avec
**« Private audio overlaps graphics at 0x08D00000 »**. La ROM valide est conservée.
Voir [mesures](MESURES.json) et [protection testée](PROTECTION_CHEVAUCHEMENT.json).

SHA-256 de référence privée :
`6368e2c28cae2eeddf1d6439fcd279693fc67b8270d3f1b1bc5d75e3dd71c65c`.

SHA-256 privé expérimental, fichier `pokefirered_audio.gba` :
`b3000abdffdcfd707cc461165fd1e275f8e0cbc95498fc4d9234a88db3696a09`.

SHA-256 public :
`a00527774542439e1ab0976a45421911c8b067d8bd11730de183c453581b3b3c`.
La ROM publique reste **strictement identique** à la référence publique connue.
Cette empreinte privée expérimentale ne remplace aucune empreinte de la B13.

## Les cinq ajouts

| Slot | OST | DPCM lié | Affectation | État |
|---|---|---:|---|---|
| 5 | Enma Track | 821 056 octets | Dialogue existant avec Enma au Mont Braise | Lecture unique de 119,014 s ; boucle à résoudre |
| 8 | Katies House | 978 565 octets | Réservé | Lecture unique de 141,845 s ; boucle à résoudre |
| 13 | Enma Villa | 687 340 octets | Réservé | Intro de 1,001 s puis cycle de 98,630 s |
| 14 | Mount Wildwood in the Past | 453 370 octets | Réservé ; Mystic Grove conservé | Intro de 4,000 s puis cycle de 61,715 s |
| 25 | Final Battle – Are You Ready? | 1 393 936 octets | Combat existant contre Matt Champion | Lecture unique de 202,057 s ; boucle à résoudre |

Les slots 8, 13 et 14 sont disponibles par appel moteur mais n'ont aucune carte
attribuée. Le relevé des 425 cartes le confirme. Aucun dialogue, lieu, personnage,
combat, équipe, statistique, évolution ou sprite n'a été ajouté ou modifié.

Pour 13 et 14, les périodes déjà étudiées ont été vérifiées sur le signal DPCM
décodé : quatre fenêtres successives d'une seconde dépassent 0,98 de corrélation.
Le raccord a été aligné à moins de 50 ms du point d'introduction stable : les
deux échantillons de part et d'autre de la jointure ont la même valeur PCM8.
On conserve l'introduction et un cycle complet ; on retire la répétition et le
fondu terminal de l'enregistrement fourni. Aucun fondu croisé, changement de
tempo ou réencodage des blocs conservés. Les points exacts et les empreintes
MP3/WAV/DPCM sont dans `data/yokai/audio_loops.json`.

Pour 5, 8 et 25, les recherches de récurrence restent insuffisantes pour fixer une
boucle musicale fiable. **Le fichier complet original est donc conservé octet
pour octet, sans activer une fausse boucle.** Après sa fin naturelle, le morceau
reste silencieux jusqu'à une autre demande musicale. C'est notamment une limite
du dialogue Enma laissé ouvert et d'un combat Matt dépassant environ 3 min 22 s.
La branche est expérimentale et ce comportement n'est pas présenté comme abouti.

## Catalogue des 31 OST

Les 26 anciennes vagues DPCM, leurs gains et leurs affectations sont préservés.
Les destinations ci-dessous résument les usages historiques ; elles ne prétendent
pas que les quêtes futures de Coach Antonic ou du scientifique sont terminées.

| Slot | Titre exact du catalogue | Utilisation principale |
|---|---|---|
| 1 | Bicycle Theme | Vélo |
| 2 | Vs. Hinozall (English) | Domniscian |
| 3 | vs. The Ghoulfather | Don Morleone |
| 4 | Infinite Tunnel | Appels dédiés Tour Pokémon ; usages de cartes selon relevé |
| 5 | Enma Track | Dialogue Enma |
| 6 | Vs. Zazelmare | Combat Seigneur Enma |
| 7 | Nates House | Bourg Palette et intérieurs associés |
| 8 | Katies House | Réservé |
| 9 | Blasters Hideout | Dojo de Safrania |
| 10 | Yo-kai Watch Blasters! Theme | Maître Koichi du Dojo |
| 11 | Bada-Bing Tower | Sylphe occupée |
| 12 | Blossom Heights | Jadielle, Argenta et Souterrains |
| 13 | Enma Villa | Réservé |
| 14 | Mount Wildwood in the Past | Réservé |
| 15 | Decisive Battle | Conseil 4 |
| 16 | Harrisville | Île 2 et intérieurs associés |
| 17 | Somewhere A Bit Dodgy (BBQ) | Repaire Rocket |
| 18 | Messenger from the Future ~ Robonyan Arrives | Rencontres de Scientifiques |
| 19 | Vs. Robonyan 3000 | Combats de Scientifiques |
| 20 | Mini Boss Battle | Employés et Mafiamilles |
| 21 | San Fantastico | Carmin sur Mer |
| 22 | Uptown Springdale | Céladopole et usages associés |
| 23 | Mystic Grove | Grottes, forêts, Lavanville et usages conservés |
| 24 | Hoppers Gorge | Mont Sélénite et usages associés |
| 25 | Final Battle – Are You Ready? | Matt Champion |
| 26 | Take Care, Grandpa 1 | Conclusion de la Ligue et victoire associée |
| 27 | Patrol Mission | Routes |
| 28 | vs. Yo-kai ~2~ | Combats courants |
| 29 | vs. Boss Yo-kai | Champions d'arène |
| 30 | The Very Curious Yo-kai Watch | Titre, introduction et événements associés |
| 31 | Usapyon and Hailey Annes Theme (Reused) | Ariane |

[Catalogue CSV complet](CATALOGUE_31_OST.csv) : provenance par jeu, tailles,
durées, nombre et noms des cartes, identifiants BGM effectifs. Les
[425 affectations de cartes compilées](routage/AFFECTATIONS_CARTES_EFFECTIVES.csv)
et les [104 appels BGM](routage/AFFECTATIONS_BGM_EFFECTIVES.csv) font foi sur les
destinations effectives, plutôt que les anciennes propositions de scénario.
Les bruitages, cris et fanfares Pokémon sont conservés.

## Vérifications effectuées

| Test | Résultat et portée |
|---|---|
| Compilation privée de référence | Réussie, taille et SHA-256 historiques retrouvés exactement |
| Compilation privée 31 OST | Réussie, masque `0x7FFFFFFF`, 31 pointeurs et échantillons vérifiés ; [liaison](LIAISON.json) |
| Préservation binaire | Tous les octets préexistants conservés hors cinq pointeurs, masque et relocalisations équivalentes de liaison ; [mesures](MESURES.json) |
| Lecture effective des 31 OST | Audio du callback mGBA comparé aux échantillons attendus avant/après appels SE et cri, corrélations > 0,85 ; [lecture](lecture/TEST_MGBA.json) |
| Fin des trois lectures uniques | Morceaux joués jusqu'à leur fin native sans réécriture du curseur ; absence de redémarrage confirmée ; même rapport |
| Boucles nouvelles 13 / 14 | Cinq / six retours natifs, au moins cinq raccords audio conformes par morceau ; intro non répétée, sauvegarde Flash native réussie ; [boucles](boucles/TEST_MGBA.json) |
| Routage | 104 appels BGM, 425 en-têtes compilés et 273 pointeurs SE/fanfares vérifiés ; [rapport](routage/ROUTAGE_MGBA.json) |
| Enma | Interaction originale au Mont Braise, slot 5, refus aux boutons et restauration du thème de carte ; [événements](evenements/TEST_MGBA.json) |
| Matt | Scène originale, combat au slot 25, victoire aux boutons et conclusion au slot 26 ; même rapport |
| Fanfare d'objet | Appel natif pendant Enma Track, fin de fanfare et reprise de l'échantillon sans redémarrage ; rapport lecture |
| Compilation publique | Réussie et ROM entièrement identique à la référence ; nouvelle partie et 31 replis natifs lancés dans mGBA ; [rapport](PUBLIC_MGBA.json) |
| Régénération privée | Nouveau dossier de sortie, assemblages régénérés depuis les entrées épinglées, même SHA-256 ROM ; [rapport](REGENERATION.json) |
| Protection de placement | Liaison trop grande effectivement refusée ; [rapport](PROTECTION_CHEVAUCHEMENT.json) |

Les 56 octets différents hors zone de remplissage comprennent les cinq pointeurs,
le masque et le réordonnancement de sept petits relais Thumb produits par GNU ld.
Chaque relais conserve exactement son code et sa destination ; 17 appels BL ont
été décodés pour vérifier qu'ils visent le même relais nommé. Aucune autre
différence n'est acceptée par `verifier_preservation_audio31.py`.

Les tests partent d'une vraie nouvelle partie. Ils utilisent ensuite des fixtures
explicites : warps, progression, allié renforcé pour Matt et appels isolés pour le
catalogue audio. Ce n'est pas une partie complète ; les 425 cartes ne sont pas
parcourues une par une. Les deux captures Enma/Matt ont été ouvertes et examinées.
Les anciens cycles des 26 morceaux n'ont pas tous été rejoués intégralement : leur
contenu est identique et leur lecture a fait l'objet de cette nouvelle régression.
Les 273 effets n'ont pas tous fait l'objet d'une écoute.

**Aucune écoute humaine n'est revendiquée.** Les corrélations, valeurs au raccord
et sorties mGBA sont des contrôles automatisés ; ils ne prouvent pas à eux seuls
l'absence de tout clic perceptible ni la qualité artistique. Les deux nouvelles
boucles, les niveaux perçus des cinq ajouts et le montage historique de Blossom
Heights demandent encore une validation à l'écoute. Pas de test matériel GBA.

## Reconstruction privée, notamment sous Windows/WSL

Toutes les commandes suivantes se lancent dans Debian/WSL, depuis le dépôt sur
cette branche, avec les dépendances et le compilateur agbcc documentés par le
projet. La configuration testée est indiquée dans [OUTILS.json](OUTILS.json).
La disposition de liaison expérimentale exige `MODERN=0`, sans révision 10.

Les sources audio légalement obtenues restent **hors du dépôt**. Le manifeste
privé d'extraction doit fournir les noms `source_stem` du catalogue
`data/yokai/audio_candidates.json`. FFmpeg 7.1.5 Debian 13 est celui utilisé pour
les WAV épinglés. Les empreintes attendues ne doivent jamais être modifiées pour
contourner une divergence de source ou de décodeur.

Préparer uniquement les cinq nouveaux encodages complets, si on ne les possède
pas déjà. Exemple avec des chemins personnels à adapter :

```sh
python3 tools/yokai/preparer_ost_dpcm.py \
  --extracted-manifest /chemin/prive/manifest-private.json \
  --private-output /chemin/prive/cinq-complets \
  --numbers 5,8,13,14,25 --jobs 2
```

Les cinq MP3 et WAV sont contrôlés avant encodage ; les cinq DPCM complets sont
à nouveau contrôlés lors de la génération. Aucun morceau absent n'est remplacé
automatiquement par un autre fichier. Cette session n'a pas répété ce décodage
MP3 complet : elle a vérifié les sources existantes et utilisé les DPCM complets
déjà disponibles, conformément à la consigne.

Avec un dossier des **26 encodages originaux** déjà préparé et vérifié :

```sh
python3 tools/yokai/generer_audio_prive.py \
  --reuse-26-dir /chemin/prive/anciens-26 \
  --gap-source-dir /chemin/prive/cinq-complets \
  --output /chemin/prive/integration-31
make -j4 YOKAI_AUDIO_DIR=/chemin/prive/integration-31
YOKAI_AUDIO_DIR=/chemin/prive/integration-31 \
  python3 tools/yokai/verifier_liaison_audio.py
sha256sum pokefirered_audio.gba
```

Les 26 fichiers réutilisés sont comparés aux empreintes de
`AUDIO_30MIO/PROVENANCE_26_OST.json` : ce ne sont pas des fichiers locaux acceptés
sans contrôle. Pour les reconstruire depuis les sources personnelles, reprendre
la [procédure audio précédente](../AUDIO_30MIO/README.md#reconstruction-privée)
et son décodage épinglé. Sur cette branche, l'appel au générateur doit recevoir
en plus `--gap-source-dir`. Il est aussi possible de fournir directement
`--full-source-dir /chemin/prive/wav-26` au lieu de `--reuse-26-dir` ; chaque WAV
des 26 est alors vérifié avant réencodage.

Le résultat est `pokefirered_audio.gba`, ouvrable directement dans mGBA. Le dépôt
public ne contient ni ce fichier, ni les MP3/WAV/DPCM, ni les extraits de tests.
Une compilation publique par `make -j4` utilise ses replis Pokémon et ne peut pas
être identique musicalement à la compilation privée.

## État à reprendre

L'intégration de placement et les tests techniques sont réalisés. **Il reste à
établir des boucles musicales fiables pour Enma Track, Katies House et Final
Battle, puis à valider l'écoute des cinq ajouts avant fusion.** Ne pas forcer une
boucle sur la fin complète et son fondu. Aucun changement de scénario ou
d'affectation des 26 anciennes OST n'est nécessaire pour reprendre ce travail.
