# Final Battle — variante C intégrée expérimentalement

Branche **`audio/integration-31-ost`**, référence précédente
`100c22e9f6c46831820c3140f0138589f9df0b11`. Commit d'implémentation :
`76766d0e4`. Aucune fusion et aucune modification d'une autre branche.

**La variante C choisie par l'utilisateur est activée et fonctionne pendant le
combat de Matt. Cinq cycles ont été vérifiés dans mGBA, puis le combat a été
gagné aux boutons et le thème de conclusion s'est déclenché.** Ce résultat valide
le fonctionnement technique expérimental, pas la qualité musicale définitive.

## Points appliqués, sans estimation au moment de compiler

| Paramètre | Valeur exacte |
|---|---|
| Morceau / identifiant existant | Final Battle – Are You Ready? / slot 25, `MUS_YOKAI_FINAL_BATTLE` |
| Fréquence | 13 379 Hz |
| Retour natif | **462 424 échantillons**, soit **34,5634202855 s** |
| Fin exclusive | **2 474 626 échantillons**, soit **184,9634501831 s** |
| Cycle | **2 012 202 échantillons**, soit **150,4000298976 s** |
| Introduction conservée une seule fois | Échantillons 0 à 462 423 inclus |
| Source après la fin choisie | Exclue du WaveData lié ; original privé complet conservé |
| En-tête natif | Compression DPCM type 1, drapeau de boucle `0x4000` |

Le générateur utilise ces indices épinglés dans `data/yokai/audio_loops.json`.
Il conserve le début original et les blocs DPCM existants ; il ajuste seulement
le drapeau, le point de retour et le nombre d'échantillons, puis retire les blocs
de fin inutilisés. Aucun réencodage, fondu croisé, changement de fréquence,
modification du volume ou nouveau routage musical. Les bornes sont celles de la
variante C, sans nouveau recalage automatique à la compilation.

La validation utilisateur porte explicitement sur le choix expérimental du
raccord. Le champ `perceptual_listening_validated` reste `false` ; il ne doit pas
être confondu avec cette autorisation d'intégration.

## Test réel dans le combat de Matt

[Rapport du combat prolongé](evenements/TEST_MGBA.json).

Le test démarre une vraie nouvelle partie aux boutons, prépare explicitement
les drapeaux de progression, un warp et un allié renforcé, puis suit la scène
originale du Champion. **La musique est déclenchée par le combat existant**,
sans appel direct à `m4aSongNumStart` pour remplacer ce déclenchement.

Après apparition des deux combattants, le pilote laisse le jeu au menu natif
de choix d'action pendant **46 029 frames**, environ **770,65 s**, soit
**12 min 50,65 s**. Le jeu continue de tourner ; seule l'entrée du contrôleur
reste au repos. Le test surveille le canal et l'en-tête BGM à chaque frame.

| Retour | Frame relative du test | Position observée juste après retour | Corrélation de l'audio mGBA avec le raccord DPCM attendu |
|---|---:|---:|---:|
| 1 | 10 057 | 462 550 | 0,957290 |
| 2 | 19 040 | 462 540 | 0,957637 |
| 3 | 28 023 | 462 530 | 0,957758 |
| 4 | 37 006 | 462 520 | 0,957584 |
| 5 | 45 989 | 462 510 | 0,956861 |

Les positions sont échantillonnées une fois par frame : le curseur a déjà
avancé de quelques échantillons après le retour exact à 462 424. Les retours
espacent chacun environ **8 983,045 frames**. Aucun retour à zéro, aucune reprise
de l'introduction, aucune perte du canal ni substitution de l'en-tête musical
n'a été détecté pendant ces 46 029 frames.

Les cinq raccords ont été capturés depuis le callback audio réel mGBA puis
comparés au DPCM attendu. Le minimum de corrélation est **0,956861**. L'identité
du morceau est également vérifiée avant/après les appels natifs de bruitage de
sélection et de cri ; le cri se termine. Aucune sauvegarde n'est provoquée dans
le combat. Les extraits WAV natifs restent hors Git, dans le dossier privé
`final-battle-c-integration/previews`.

Le pilote reprend ensuite le combat aux boutons : victoire réelle, drapeau du
Champion enregistré, puis musique **26 — Take Care, Grandpa 1** dans le script
original de conclusion. Aucun adversaire, résultat ou drapeau de victoire n'est
forcé pendant le combat.

Un [test complémentaire de victoire](victoire/TEST_MGBA.json), sans répéter
l'attente prolongée, observe également le thème de victoire natif redirigé vers
**22 — Uptown Springdale**, avant le passage au thème 26. Les captures du menu
pendant le combat prolongé et de la victoire ont été ouvertes et examinées.

Ces tests vérifient le déclenchement, la lecture continue, les retours, les
sorties audio et les transitions. Ils ne constituent ni une écoute humaine
définitive, ni un test matériel GBA, ni une partie complète de l'aventure.
L'appréciation d'une éventuelle rupture de phrase, d'un clic perceptible ou du
maintien des notes reste à confirmer musicalement avant toute fusion.

## Préservation des 30 autres OST et du jeu

[Preuve binaire](PRESERVATION_30_OST.json) : les **30 autres échantillons liés**
sont identiques octet pour octet à la ROM du commit `100c22e9f`, y compris
Katies House et les deux autres nouvelles boucles. Leurs empreintes figurent
individuellement dans ce rapport.

Plus fortement, **tous les octets de la ROM situés hors de l'ancien WaveData 25
sont identiques à la référence**. Le changement est limité à cet en-tête, aux
blocs conservés et à son ancien suffixe remplacé par du remplissage FF. Les
blocs DPCM conservés sont eux-mêmes identiques à l'original.

Aucun sprite, équipe, statistique, évolution, attaque, carte, dialogue, script,
effet sonore, gain de mixage ou mécanisme de gameplay ne change. Le Multi Exp.
et toutes les affectations des autres morceaux sont donc préservés. Les seules
autres modifications du dépôt sont la configuration documentaire, le catalogue,
les rapports et les outils de prévisualisation/test de ce chantier audio.

## Compilation et budget

| Mesure | Avant | Après |
|---|---:|---:|
| ROM privée | 31 589 579 octets | **31 589 579 octets** |
| Limite conservée | 33 554 432 octets | **33 554 432 octets** |
| Marge jusqu'à 32 Mio | 1 964 853 octets | **1 964 853 octets** |
| WaveData DPCM 25 | 1 393 936 octets | **1 276 027 octets** |
| Section audio dans le remplissage | 4 122 544 octets | **4 004 635 octets** |
| Remplissage restant avant les graphismes | 1 941 876 octets | **2 059 785 octets** |

Le fichier ROM ne rétrécit pas : les adresses fixes des graphismes et la fin de
ROM sont conservées. Le suffixe retiré libère **117 909 octets** dans la zone
privée existante. Aucune donnée partagée n'est supprimée. L'assertion de
non-chevauchement à `0x08D00000` reste active. EWRAM 261 052 et IWRAM 29 888
octets, inchangées.

Compilation privée réussie ; [liaison et empreintes des 31 morceaux](LIAISON.json)
conformes. La compilation publique a également été vérifiée par `make -j6` : sa
ROM reste strictement identique à sa référence, **16 777 216 octets**.
Voir les [mesures](MESURES.json).

ROM privée actuelle `pokefirered_audio.gba`, SHA-256 :
`0e7ff7f6096e5b52932e1e1cf090eaee3c53ee7ebe182ebbd5302feee2a2bfce`.

ROM publique inchangée, SHA-256 :
`a00527774542439e1ab0976a45421911c8b067d8bd11730de183c453581b3b3c`.

Cette nouvelle empreinte décrit la nouvelle version expérimentale ; elle ne
remplace aucune empreinte attendue pour une ancienne bêta ou un autre commit.

## Reconstruction et reprise

La [procédure privée existante](../README.md#reconstruction-privée-notamment-sous-windowswsl)
reste applicable, avec les mêmes ressources personnelles légalement obtenues.
Le générateur prend automatiquement les nouveaux points approuvés :

```sh
python3 tools/yokai/generer_audio_prive.py \
  --reuse-26-dir /chemin/prive/anciens-26 \
  --gap-source-dir /chemin/prive/cinq-complets \
  --output /chemin/prive/final-battle-c
make -j4 YOKAI_AUDIO_DIR=/chemin/prive/final-battle-c
YOKAI_AUDIO_DIR=/chemin/prive/final-battle-c \
  python3 tools/yokai/verifier_liaison_audio.py
```

Pour répéter le scénario complet testé, avec mGBA/libretro et les dépendances
QA déjà documentés :

```sh
export YOKAI_AUDIO_DIR=/chemin/prive/final-battle-c
export YOKAI_QA_ROM="$PWD/pokefirered_audio.gba"
export YOKAI_QA_ELF="$PWD/pokefirered_audio.elf"
YOKAI_AUDIO31_MATT_VERIFY_LOOPS=1 \
YOKAI_AUDIO31_EVENTS_DIR=QA_RECETTE_FINALE/AUDIO_31_OST/FINAL_BATTLE_C/evenements \
  python3 tools/yokai/tester_audio31_evenements_mgba.py
```

Le mode `YOKAI_AUDIO31_MATT_VERIFY_LOOPS=1` exige cinq retours, la continuité
contrôlée à chaque frame, au moins dix minutes et la victoire ; il ne peut pas
réussir simplement parce que les pointeurs sont corrects.

Aucun MP3, WAV, DPCM ou fichier ROM n'est envoyé sur GitHub. Seules les sources,
les réglages, les outils, les captures et les preuves numériques sont publiés.
**La prochaine validation est une écoute humaine de la variante C en jeu.**
Enma Track reste dans son état antérieur ; aucune correction de ce morceau n'a
été entreprise ici. Aucun merge n'est effectué.
