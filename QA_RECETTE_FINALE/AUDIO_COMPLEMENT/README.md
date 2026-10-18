# Complément audio — tous les fonds musicaux vers Yo-kai

Demande : remplacer si possible tous les fonds musicaux Pokémon, réutiliser les OST et commencer/intégrer les morceaux restants. Base préservée : `f4eb55d4f0d0979f992862626a812e4f9168fc0a`. Branche `dev/reconstruction-finalisation`, master inchangée. Aucun changement graphique ou de gameplay.

**Résultat : les 104 identifiants BGM de la compilation privée se résolvent vers des enregistrements Yo-kai actifs. 20 OST distinctes sont intégrées. Les bruitages, cris et jingles fonctionnels restent natifs.** Ce résultat ne signifie donc pas « aucun son ou aucune courte mélodie Pokémon », ni « toutes les versions personnelles des 22 sélections historiques sont terminées ».

## Modifications

- Ajout des neuf derniers alias : introduction de combat historique, ancien soin sur lecteur BGM, Panthéon, victoires dresseur/sauvage/champion, capture, émission et menu TV ABC. Les 64 alias précédents restent conservés. Les musiques du titre et de la présentation étaient déjà réaffectées ; aucun dessin ni déroulement de l'introduction n'est modifié.
- Les anciens identifiants dédiés encore dépourvus de sample propre disposent d'un substitut Yo-kai **uniquement dans la compilation privée**. Leur futur sample personnel reste prioritaire, sans réécrire les scripts. Pas de copie de samples pour chaque affectation.
- Ajout de **Blossom Heights**, pour les 18 cartes déjà affectées à ce thème : 331 237 octets DPCM, 13 379 Hz, introduction 4,809702 s une fois puis phrase de 43,199940 s. Les 19 autres DPCM sont exactement identiques.
- Correction d'une comparaison directe avec le pointeur de l'ancienne victoire Pokémon dans la salle du Maître. Elle utilise désormais la résolution musicale commune, afin de préserver le thème de victoire pendant le retour de combat. Aucun changement de condition de progression.
- Calibration de Blossom sur le cycle complet rendu par mGBA : gain 294/256, résultat **−29,0 LUFS**, pic vrai −17,1 dBFS, aucun échantillon saturé. Les autres gains et toutes les banques de bruitages restent inchangés.

## Limites artistiques et morceaux non terminés

La nouvelle boucle Blossom est un **montage explicite d'une phrase**, pas la prétendue récurrence exacte de tout le MP3. L'analyse antérieure rejetant l'hypothèse d'une répétition complète reste valable. Les nouvelles mesures trouvent un voisinage harmonique compatible au raccord, puis un alignement de phase borné : corrélation d'une seconde 0,862, saut PCM16 de 2 et saut DPCM8 décodé nul. Aucun étirement, fondu croisé ou nouveau dessin instrumental. Les cinq raccords sont fidèlement reproduits par le moteur. **Une écoute humaine reste indispensable pour approuver ce choix de phrase et sa variété**, et la piste est marquée provisoire dans le tableau.

Deux sélections historiques n'ont toujours pas leur boucle personnelle suffisamment établie :

| Sélection | En attendant, lecture privée effective |
|---|---|
| Enma Track, dialogue d'Enma (5) | The Very Curious Yo-kai Watch (30) |
| Final Battle – Are You Ready?, Matt Maître (25) | Decisive Battle (15) |

Ces substitutions sont temporaires et explicites ; ne pas les présenter comme l'intégration des deux enregistrements originaux. Les thèmes de combat personnels de Domniscian, Don Morleone et Enma restent respectivement Hinozall, Ghoulfather et Zazelmare, sans modification de leurs données.

L'inventaire validé après B13 comporte **22 sélections**, alors que le cahier historique fixe **20 pistes distinctes maximum**. Ce jalon respecte 20, ne supprime aucune des 19 pistes existantes, et ne dépasse pas tacitement ce plafond. Intégrer également les deux enregistrements personnels encore en attente nécessitera une boucle fiable et un arbitrage sur ce plafond ou deux pistes à retirer ; aucune suppression arbitraire n'est faite. Les neuf anciens emplacements optionnels non sélectionnés disposent eux aussi d'un substitut actif, sans allouer de nouveau sample.

## Affectations complètes

- [22 sélections : état, taille, intro, boucle, affectation effective](OST_SELECTIONS_ET_ETAT.csv).
- [104 identifiants BGM : demande, lecture effective et substitutions](AFFECTATIONS_BGM_EFFECTIVES.csv).
- [425 cartes compilées : demande et lecture effective](AFFECTATIONS_CARTES_EFFECTIVES.csv) : 423 thèmes privés actifs, deux silences intentionnels.
- [Références dans les sources](REFERENCES_MUSICALES_SOURCES.csv). Une référence source n'est pas une preuve d'accessibilité en partie.
- [Provenance et empreintes des 20 samples](PROVENANCE_20_OST.json), [mesures de la coupe Blossom](BOUCLE_BLOSSOM_MONTAGE.json).

Les fichiers `AFFECTATIONS_MOTEUR_ET_JINGLES.csv` et `AFFECTATIONS_425_CARTES.csv` décrivent les identifiants déclarés. Pour les substitutions privées, consulter les tableaux **EFFECTIVES** issus du résolveur compilé.

## Vérifications réellement effectuées sur ce jalon

| Test | Résultat et preuve |
|---|---|
| Résolution et démarrage natifs de tous les BGM | **104/104**, passage alias → thème effectif sans redémarrage ; [rapport mGBA](ROUTAGE_MGBA.json) |
| En-têtes compilés des cartes | **425/425** conformes et résolus ; il ne s'agit pas de 425 cartes parcourues |
| Bruitages/fanfares | **273 pointeurs inchangés** : 255 identifiants d'effets et 18 jingles/fonctions musicales |
| Blossom, retours de boucle | **5/5** natifs ; corrélation audio au raccord ≥0,987 ; intro non rejouée, bruitage, cri terminé et sauvegarde Flash ; [preuve](boucles-blossom/TEST_MGBA.json) |
| Volume Blossom | [Cycle complet avant](BLOSSOM_LUFS_AVANT.json), [après calibration](BLOSSOM_LUFS_FINAL.json) |
| Portes ville/soins/boutique/laboratoire | **64 franchissements aux boutons**, horloge avançante, même thème, sans pause/redémarrage ; [rapport](portes/TEST_MGBA.json) |
| Fanfares sur OST | **34 scénarios** : 14 fanfares sur Patrol Mission, puis objet sur chacune des 20 pistes ; pause et reprise au curseur conservé ; [rapport](FANFARES_MGBA.json) |
| Combat sauvage | Victoire aux boutons puis retour au thème d'exploration, Multi Exp. confirmé pour l'allié non participant ; [rapport/captures](transition-sauvage/TEST_MGBA.json) |
| Capture | Master Ball utilisée via le sac natif, musique de capture Yo-kai observée, espèce reçue en équipe, retour au thème de carte ; [rapport](capture/TEST_MGBA.json) |
| Salle du Maître après victoire | Branche musicale native vérifiée sur sa vraie carte, thème et horloge préservés ; test isolé, pas un nouveau combat complet de Matt |
| Sources → ROM | 20 samples privés identiques au manifeste, pointeurs et limites vérifiés ; [liaison](LIAISON_20_OST.json) |

Les tests commencent par une vraie nouvelle partie. Les warps, progression, objets et adversaires préparés sont des fixtures RAM. Aucun résultat de combat ou de capture n'est forcé. La fixture capture a été corrigée avant validation : tous les homonymes natifs de la fonction de menu sont reconnus et le Yo-kai sauvage utilise le D.O. joueur comme dans les rencontres normales. Les premiers essais erronés du banc ne sont pas présentés comme des défauts du jeu.

Les 95 retours des 19 anciennes pistes restent documentés dans la session1 ; ils ne sont pas annoncés comme 95 nouveaux essais sur cette ROM. Leur source DPCM n'a pas changé. Pas de nouvelle aventure complète, d'écoute humaine ni de profilage matériel GBA dans ce lot.

## Compilation et reconstruction

[Bilan exact](BILAN_COMPILATION.json) : **28 049 679 octets**, soit **26,75 Mio**, réserve **5 504 753 octets** avant 32 Mio. Hausse de 331 420 octets par rapport au jalon graphique. EWRAM et IWRAM inchangées. SHA-256 privé : `e63f84dc175b902b6783d8ffcd78c330e6e55b066c00fd3908d891f9bb68cb1e`.

Compilation publique et privée réussies. Sans ressources audio externes, le dépôt garde ses replis musicaux natifs légaux et ne produit **pas** la même bande-son. La promesse de remplacement des BGM concerne la compilation privée avec ses 20 samples, pas le clone sans musique externe. Les séquences originales restent dans les sources pour les replis et le fonctionnement du moteur ; elles n'ont pas été supprimées au hasard pour économiser de la place.

Après préparation des WAV privés suivant [la procédure existante](../POST_B13/audio/RECONSTRUCTION_PRIVEE.md), utiliser un nouveau dossier privé :

```sh
python3 tools/yokai/generer_audio_prive.py --full-source-dir /chemin/prive/full-sources --output /chemin/prive/audio-completion --jobs 2
make -j4 YOKAI_AUDIO_DIR=/chemin/prive/audio-completion
YOKAI_AUDIO_DIR=/chemin/prive/audio-completion python3 tools/yokai/verifier_liaison_audio.py
```

Ne pas réutiliser sans régénération un ancien dossier de 19 samples : ses replis restent jouables mais ce n'est pas ce jalon de 20 pistes. Les MP3, WAV, DPCM, démos audio, sauvegardes et ROM restent hors du dépôt public. Les correctifs, tables et preuves non audio sont publiés sur la branche de développement. **L'ambiance est largement couverte ; la validation artistique de Blossom et les deux sélections personnelles restantes empêchent de déclarer toute la bande-son définitive.**
