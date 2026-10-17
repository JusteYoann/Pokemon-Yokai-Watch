# Direction validée et prototype instrumental Bicycle Theme

Les thèmes personnels demandés sont tous deux dans les 80 MP3. Aucune référence supplémentaire n’est nécessaire pour ces deux combats.

|Combat|Référence retenue obligatoirement|Source exacte|
|---|---|---|
|Domniscian / Hinozall|**Vs. Hinozall (English)**|Blasters, piste **28.5**, lot `yokaiwatch_blasters_part2.rar`|
|Don Morleone / The Ghoulfather|**vs. The Ghoulfather**|Yo-kai Watch 3, piste **57**, lot `yokaiwatch3part2.rar`|

Ces références remplacent **Boss Yo-kai de Sangokushi** et **Soruka de Sangokushi** dans la proposition. Les fichiers sources et SHA figurent dans [THEMES_BOSS_CONFIRMES.csv](THEMES_BOSS_CONFIRMES.csv). La présence de « English » n’est pas une autorisation de reprendre des voix enregistrées : le futur arrangement sera instrumental. La version personnelle fournie est confirmée par son nom et le lexique du créateur, sans prétendre à une authentification musicologique par écoute.

Le [tableau musical actualisé](PROPOSITION_BANDE_SON_V2.csv) conserve les **20 autres références** comme base de travail : **22 références distinctes**, 132 lignes de contextes et de conservation native. La validation de la direction ne signifie pas que 22 arrangements sont produits ou intégrés. `THEME_PERSONNEL_VALIDE` fixe les deux références obligatoires ; les autres arrangements restent à évaluer.

## Premier prototype disponible

Un arrangement de recherche a été réellement produit à partir de la référence **Bicycle Theme — Yo-kai Watch 1**. Il contient des événements de notes et de contrôleurs MIDI, convertis par **mid2agb** et assemblés/liés pour le moteur **M4A** du projet. Le rendu provient de ce moteur sous **mGBA**, avec ses instruments natifs. Aucun MP3, morceau PCM long ou échantillon nouveau n’est inclus dans la séquence.

**Ce prototype est techniquement fonctionnel mais sa fidélité artistique n’est pas validée.** La mélodie et la basse sont estimées automatiquement ; les arpèges et la batterie sont recomposés. Aucune écoute perceptive par l’agent ni correction note par note à partir d’une partition de référence n’est revendiquée. Il faut écouter le résultat avant de décider s’il est suffisamment reconnaissable et musical.

Les fichiers sonores et les partitions dérivées sont **privés, hors Git**, sous :

```text
/workspace/private-audio/bicycle-prototype/
  BICYCLE_PROTOTYPE_GBA.mp3       # rendu complet : deux boucles et début de la suivante
  BICYCLE_EXTRAIT_30S.mp3         # extrait du rendu, de 24 à 54 secondes
  bicycle-prototype-mgba.wav     # capture stéréo brute sans normalisation
  bicycle-prototype.mid          # partition révisable, instruments ciblant voicegroup141
  bicycle-prototype.s            # séquence M4A à relier au futur build
  arrangement.json              # notes, parties, hypothèses d’accords et corrections
  BICYCLE_PROTOTYPE_PRIVE.zip    # livrable privé avec notices, sources de travail et preuves
```

Les MP3 de démonstration sont **encodés depuis la synthèse GBA**, avec un gain d’écoute de +6 dB. Ils ne sont pas une dégradation du MP3 de référence. Le WAV brut est conservé pour comparaison. Le format MIDI utilise les numéros d’instruments du jeu ; une banque General MIDI standard donnera des timbres différents.

Les fichiers ne sont pas publiés sur GitHub. Les liens `sandbox:` éventuellement fournis dans la conversation dépendent de l’interface ; à défaut, récupérer le ZIP depuis l’explorateur du cloud au chemin ci-dessus. Les [empreintes de livraison](LIVRAISON_PRIVEE.json) permettent de vérifier l’identité des fichiers, mais ne donnent pas un accès distant à des fichiers privés. Aucun MP3 original, ROM, BIOS ou banque sonore commerciale n’est joint au ZIP.

## Construction musicale et corrections réelles

- Décodage de toute la référence et séparation harmonique/percussive pour l’analyse, sans modification du MP3 fourni.
- Pulsation ajustée sur les horodatages : **115,005 BPM** environ, contre l’estimation initiale grossière de 117,5. Une récurrence de **144 pulsations**, environ **75,13 s**, obtient une similarité moyenne de chroma de 0,956. Cela suggère un cycle de 36 mesures **si** l’on retient le 4/4 ; ce n’est pas une preuve auditive du premier temps ou d’une structure formelle exacte.
- Transcription polyphonique **Basic Pitch / ONNX** : 1 073 événements bruts estimés sur le fichier complet. Une fusion des deux occurrences du cycle limite certains événements instables. Les probabilités du modèle ne sont pas des probabilités calibrées d’exactitude musicale.
- Mélodie et basse ramenées à des lignes monophoniques ; quantification à la double croche ; chevauchements, notes trop brèves et sauts isolés filtrés. Le premier registre de mélodie était trop haut et omettait les passages graves ; il a été élargi à MIDI 48–84. Les activations continues ont été réexaminées lorsque le seuil des événements bruts créait des vides. Quatre changements isolés ont été filtrés dans la version livrée. Les silences ne sont pas tous présumés être des erreurs.
- Accompagnement harmonique **inféré**, rendu en arpèges courts ; rythme simple recomposé. Les renversements, accords enrichis, syncopes, ornements et contrechants de l’original ne sont pas certifiés et ne sont pas reproduits intégralement.
- Tempo de séquence nominal **116 BPM**, adapté à la résolution de commande du moteur. Boucle rendue d’environ **74,82 s** ; petit écart par rapport à la référence accepté pour ce prototype.

### Parties et timbres

|Partie|Instrument natif, banque 141|Rôle et limite|
|---|---|---|
|Mélodie|21, accordéon PCM|Ligne estimée ; identité mélodique à vérifier|
|Basse|85, onde programmable PSG|Ligne estimée, sans longue queue PCM|
|Accompagnement|24, guitare nylon PCM|Arpèges d’accords inférés, sans accords massifs simultanés|
|Kick / caisse claire|0, banque rythmique native ; notes 36 / 38|Rythme recomposé et allégé|
|Charleston|127, bruit PSG|Impulsions courtes, pas d’échantillon additionnel|

La partition d’arrangement contient **1 118 notes**, dont 124 pour la ligne mélodique et 274 pour la basse. Ce nombre inclut la batterie et les arpèges recomposés et ne représente pas 1 118 notes de l’original transcrites avec certitude.

## Vérifications réellement effectuées

Les valeurs de mesure sont dans [VALIDATION_TECHNIQUE.json](VALIDATION_TECHNIQUE.json) ; la préservation et les contrôles du livrable figurent dans [PRESERVATION_ET_CONTROLES.json](PRESERVATION_ET_CONTROLES.json).

|Contrôle|Résultat|
|---|---|
|Conversion MIDI → M4A et assemblage ARM|Réussis ; séquence liée **2 160 octets**|
|Nouveaux échantillons|**0 octet**, banque 141 du jeu réutilisée|
|Pistes|5, compatibles avec les 10 pistes BGM déjà allouées|
|Rendu normal mGBA|**9 258 images**, 155,004 s de son stéréo à 32 768 Hz|
|Boucle technique|Les cinq pistes restent actives ; pointeurs valides ; deux passages de boucle dépassés, 7 159 ticks observés pour une boucle de 3 456 ticks|
|Voix PCM actives, musique seule|Maximum **4**, plafond moteur inchangé à **5**|
|Saturation numérique, rendu brut|**0** échantillon saturé ; crête d’environ −16,0 dBFS|
|Test avec effets|25 déclenchements alternés de bruitage et de cri, sur plus de deux cycles ; cinq pistes maintenues actives, zéro saturation|
|PCM avec effets|Maximum **5**, plafond respecté ; pas de garantie exhaustive d’absence de vol de toutes les queues de notes|
|Coût SoundMain, mesure grossière VCOUNT|Maximum **37 lignes** musique seule, **49** avec effets ; vélo natif mesuré séparément à 44 lignes sur un essai plus court|
|Intégration vélo en exploration / matériel réel|**Non effectuée** ; aucun routage du vélo modifié|
|ROM et anciennes sources|Contrôlées séparément contre le point de départ ; aucune modification de production|

La durée de calcul hôte n’est pas une mesure CPU GBA. La mesure VCOUNT est de résolution grossière et ne remplace pas le profilage d’une scène de jeu chargée. La comparaison native couvre seulement dix secondes ; elle n’établit pas une supériorité générale de performance.

La présence de GOTO et la lecture de plusieurs cycles prouvent une boucle **technique**, pas un raccord **musicalement naturel**. Il faut encore écouter le point de retour. La phase des oscillateurs, le bruit PSG et le mixage rendent une comparaison échantillon par échantillon inadaptée ; la corrélation brute des cycles n’est pas utilisée comme critère de qualité artistique. Le rendu d’effets comporte en outre des interruptions sonores intentionnelles.

## Enma et cohérence générale

La [comparaison Enma](COMPARAISON_ENMA.csv) confronte six références effectivement présentes : Final Battle / Are You Ready, Zazelmare, Whismellowman, Enma Track, World et Enma Villa. Les mesures de niveau RMS ne sont pas une mesure d’intensité dramatique et ne classent pas leur qualité.

Je maintiens **provisoirement** Final Battle / Are You Ready pour le combat du Seigneur Enma et Enma Track pour son dialogue. Zazelmare demande un développement plus long ; Whismellowman est une alternative plus courte. World est une option de dialogue bref ; Enma Villa ne doit pas transformer le lieu existant en villa. Sans audition comparative, je ne confirme pas définitivement le meilleur thème du combat. Le combat sauvage d’Enma reste distinct et conserve le thème natif de Mewtwo dans la proposition.

Conserver les thèmes Pokémon du début, des combats ordinaires, des victoires et du Champion Matt reste pertinent pour éviter une succession de super-boss musicaux. Les deux thèmes personnels obligatoires remplacent les deux comparatifs Sangokushi, sans changer les autres rôles. Aucun changement des équipes, événements, récompenses ou conditions n’est effectué.

## Faisabilité des autres compositions et suite

La chaîne technique **MIDI → séquence M4A → instruments natifs → capture sous mGBA** est démontrée sur une composition. Cela ne prouve pas la qualité de transcription des 21 autres, particulièrement des pièces denses, avec chœurs, guitares saturées, changements de tempo ou arrangements orchestraux.

Les thèmes simples de lieu peuvent être adaptés avec peu de pistes ; les boss nécessiteront davantage de réduction, de choix de registres et de correction manuelle. Les voix éventuelles devront être transposées en lignes instrumentales, pas échantillonnées depuis l’OST. Chaque titre demandera une vérification de sa partition, de sa banque, de sa boucle et de sa concurrence avec les bruitages. Aucun chiffrage fiable de durée de production complète n’est possible avant l’évaluation de ce premier essai.

**Verdict du prototype : jouable par le moteur, à retravailler et à valider musicalement.** Ne pas lancer les 21 autres arrangements ni intégrer définitivement le vélo avant l’écoute et la validation du créateur.

## Reproduction dans le cloud d’origine

Les scripts génériques sont dans `tools/yokai_music/` sur la branche locale **`audio/prototype-bicycle-gba`**. Le projet complet reste issu du point de sauvegarde QA, sans fusion ni publication de cette branche. Le paquet privé contient également les scripts.

```sh
cd /workspace/Pokemon-Yokai-Watch
. /workspace/.setup/env.sh
export PYTHONPATH=/workspace/.setup/prototype-python:/workspace/.setup/music-python
export MPLCONFIGDIR=/workspace/.setup/music-cache
export XDG_CACHE_HOME=/workspace/.setup/font-cache
export OPENBLAS_NUM_THREADS=1
export NUMBA_NUM_THREADS=1
python3 tools/yokai_music/actualiser_direction.py
python3 tools/yokai_music/analyse_bicycle.py
python3 tools/yokai_music/transcrire.py
python3 tools/yokai_music/arranger.py
tools/mid2agb/mid2agb /workspace/private-audio/bicycle-prototype/bicycle-prototype.mid /workspace/private-audio/bicycle-prototype/bicycle-prototype.s -Lbicycle_prototype -G141 -V090 -R30 -E
python3 tools/yokai_music/rendre_mgba.py
python3 tools/yokai_music/rendre_mgba.py --stress
python3 tools/yokai_music/livrer.py
```

Les modèles et dépendances sont isolés hors dépôt ; versions complémentaires dans `tools/yokai_music/requirements-prototype.txt`. Le contexte audio précédent utilise aussi `docs/musique-audit/scripts/requirements-audio.txt`. L’absence de TensorFlow/CoreML n’est pas bloquante : le modèle ONNX a réellement été exécuté. Les adresses du binaire de test sont propres à l’allocation RAM de cet essai ; pour une future intégration, **recompiler et relier le `.s`** avec le build visé. Le `.bin` expérimental n’est pas une ressource ROM prête à copier.

Les consignes de démarrage et d’activation audio sont également sauvegardées en brouillon dans les paramètres de l’environnement. Les revoir et les enregistrer, puis publier l’environnement si leur réutilisation est souhaitée. Cela ne publie pas les fichiers privés sur GitHub et ne prouve pas une restauration dans une autre session.
