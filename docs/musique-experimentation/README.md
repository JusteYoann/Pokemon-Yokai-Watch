# Comparaison A / B — Bicycle Theme uniquement

**La lecture échantillonnée fonctionne réellement avec le moteur actuel de Rouge Feu, sans modification de son code.** Une copie privée de la ROM joue une onde PCM ou DPCM issue du morceau fourni, et non une reconstruction des instruments. Les démonstrations sont des captures de mGBA.

Le premier arrangement A1 reste rejeté artistiquement par le créateur. Une révision A2 est livrée, avec ses limites de transcription explicites. La méthode B est la plus sûre pour conserver les notes et les instruments de l’enregistrement ; elle impose un coût ROM bien supérieur et une réduction de bande passante.

## Écouter et récupérer les fichiers privés

```text
/workspace/private-audio/bicycle-ab/DEMO_A_ARRANGEMENT_REVISE.mp3
/workspace/private-audio/bicycle-ab/DEMO_B_DPCM_13379.mp3
/workspace/private-audio/bicycle-ab/COMPARAISON_A_B_PRIVEE.zip
```

Les deux fichiers principaux durent **45 secondes**, avec le même candidat de départ dans le cycle. Leur niveau d’écoute est ramené vers −18 dBFS RMS, avec une limite de crête ; les gains sont documentés dans [LIVRAISON_PRIVEE.json](LIVRAISON_PRIVEE.json). Les WAV bruts sont conservés. Le MP3 de démonstration est un export de la capture de l’émulateur : **la GBA ne lit jamais de MP3**.

Le paquet contient aussi des comparaisons PCM / DPCM, les quatre fréquences, le mixeur à 18 157 Hz, un passage de boucle isolé, la descente du vélo et les enregistrements de cinq retours complets. Les fichiers de travail permettent de reproduire le test ; aucune ROM complète, banque sonore commerciale ou référence MP3 originale n’est jointe.

**Aucun nouvel audio, sample, MIDI ou partition de cette expérience n’est publié sur GitHub.** La méthode B contient bien l’enregistrement converti ; elle reste donc privée conformément à la demande. Les rapports publics et les chemins privés ne rendent pas ces fichiers publiquement accessibles. Si l’interface ne permet pas les téléchargements, récupérer le ZIP dans l’explorateur de l’environnement au chemin indiqué. L’ancien extrait A1 déjà publié à la demande du créateur ne représente pas A2 ni B.

## Résultats principaux mesurés

|Méthode / variante|Ajout ROM du test|PCM actives, seule / avec effets|SoundMain : maximum de lignes VCOUNT, seul / effets|Fidélité attendue|
|---|---:|---:|---:|---|
|A1, ancien arrangement|2 160 octets|4 / 5|38 / 47|Rejeté par le créateur ; partition non fiable|
|A2, arrangement révisé|3 824 octets|5 / 5|38 / 46|Révision fournie ; notes et timbres toujours non certifiés|
|B, PCM 8 bits, 13 379 Hz|1 005 248 octets|1 / 3|10 / 33|Enregistrement conservé en mono, aigu réduit et quantification 8 bits|
|B, DPCM natif, 13 379 Hz|518 392 octets|1 / 3|20 / 43|Même musique, avec une dégradation supplémentaire de compression|
|B, DPCM 16 000 Hz, mixeur 18 157 Hz|619 932 octets|1 / 3|24 / 52|Bande passante supérieure ; coût CPU et réglage global du mixeur plus élevés|

Ces coûts incluent les en-têtes et données du test, pas la taille des fichiers MP3 d’écoute. La banque copiée d’A2 ajoute des paramètres d’instruments mais aucune nouvelle onde. Les autres banques natives restent inchangées. Le plafond reste **cinq voix PCM**, plus les canaux PSG existants ; une absence de saturation n’est pas une certification d’absence de tout vol de queue de note.

La mesure VCOUNT ne couvre que SoundMain au pas d’une ligne écran. Elle ne remplace pas un profilage CPU de toutes les scènes du jeu. La variante à 18 157 Hz passe ces essais, mais doit encore être profilée en scènes chargées ; le banc rétablit le réglage natif en descendant du vélo. Cette gestion du changement de mixeur n’est pas déjà intégrée dans le jeu.

Les résultats par cas sont dans [TESTS_MGBA.csv](TESTS_MGBA.csv) et [PREUVES_MGBA.json](PREUVES_MGBA.json). Le [diagnostic détaillé de A1 et les changements A2](DIAGNOSTIC_A.md) expliquent pourquoi une lecture techniquement valide n’avait pas donné une bonne adaptation musicale.

## Ce qui a réellement été testé

- **18 cas mGBA** : PCM et DPCM à 8 000, 11 025, 13 379 et 16 000 Hz ; cinq cas longs ; cinq cas avec bruitages et cris.
- **Cinq retours de boucle par cas long** pour A1, A2, PCM 13 379, DPCM 13 379 et DPCM 16 000 / mixeur 18 157, soit **25 retours observés**. Chaque cas joue encore environ deux secondes après le cinquième retour.
- Le lecteur d’ondes B est suivi à chaque frame : aucun arrêt ou disparition de sa voix n’est observé. Les positions retournent au début de l’onde ; aucune nouvelle note n’est redéclenchée à chaque retour.
- Les cinq tests d’effets déclenchent chacun dix paires de bruitage et de cri, avec les routines natives. Aucun échantillon saturé n’est détecté. Ce test ne couvre pas toutes les combinaisons de sons et combats du jeu.
- Tous ces tests chargent une vraie carte, **Bourg Palette**, exécutent la transition native du vélo puis restaurent le thème de la zone et l’état à pied. Les cas longs utilisent un appel de fixture RAM à `GetOnOffBike`, sans changer cette fonction.
- **Deux tests supplémentaires par véritable entrée SELECT**, pour A2 et DPCM 13 379 : vélo ajouté et enregistré dans la sauvegarde volatile, pression de SELECT, entrées directionnelles, deuxième pression de SELECT et retour au thème de zone. [Preuve SELECT](SELECT_TESTS.json), [vélo](preuves/B-dpcm4-13379-select-bike.png), [retour à pied](preuves/B-dpcm4-13379-select-off.png).
- Tous les MP3 d’écoute produits sont décodés intégralement par FFmpeg après export. Les fichiers bruts et leurs empreintes restent disponibles.

Le cœur est **mGBA libretro 0.10.5**, BIOS HLE. **Pas de test sur GBA physique**, de parcours complet de la région ou de certification d’écoute humaine par l’agent. Les conditions de tests préparées et les copies de ROM sont privées ; aucune sauvegarde de production n’est utilisée.

## Boucle et entrée directe dans la musique

La référence présente une récurrence mesurée de 144 pulsations, environ **75,13 secondes**. Le candidat d’entrée est déplacé de seize pulsations, vers **8,78 secondes** dans le fichier source, et le cycle complet est tourné autour de ce point. Cela permet d’essayer un départ plus direct sans jouer le début du fichier à chaque montée sur le vélo.

Ce choix est une **rotation de cycle**, pas l’affirmation qu’une introduction formellement identifiée a été supprimée. Un début différent ou une boucle plus courte pourra être choisi après écoute ; aucun découpage semblable n’est présumé valable pour les autres musiques.

La méthode B utilise un `TIE` et une onde native avec début et fin de boucle. Le passage se fait au niveau de l’échantillon, sans réattaquer une note à une limite de mesure MIDI. Une courte transition de 12 ms traite la jonction de forme d’onde ; une garde d’interpolation et l’alignement sur blocs de 64 échantillons sont préparés. La durée n’est pas raccourcie d’une quantité audible à chaque tour : l’ajustement de bloc est de quelques millisecondes, fixe pour chaque variante.

[BOUCLES_CONTROLEES.csv](BOUCLES_CONTROLEES.csv) relève les 25 jonctions : aucun bloc d’environ 10 ms sous −70 dBFS n’y est détecté. Cette vérification et le maintien des voix montrent l’absence de trou technique observé ; **elles ne garantissent pas un raccord musical sans défaut audible**. Le fichier privé `RETOUR_DE_BOUCLE_B.mp3` permet d’écouter la jonction, et les fichiers `*-CINQ_BOUCLES.mp3` permettent de juger la répétition entière.

## PCM, compression et mémoire

Le moteur lit la musique depuis la ROM comme une grande onde mono. Il ne charge pas ses 75 secondes en EWRAM. L’en-tête `WaveData` et les pointeurs de boucle sont ceux du moteur existant.

Le DPCM natif est le format spécifique de Pokémon, **33 octets par bloc de 64 échantillons**, soit **4,125 bits par échantillon** hors en-têtes et garde. Le décodeur et son tampon de **64 octets en IWRAM** sont déjà présents dans le jeu. Un bit de type d’instrument active cette voie. Ce n’est pas du WAV IMA-ADPCM arbitraire et ce n’est pas un nouveau décodeur MP3.

|Encodage|8 kHz|11 025 Hz|13 379 Hz|16 kHz|
|---|---:|---:|---:|---:|
|Onde PCM 8 bits mesurée|601 044 o|828 308 o|1 005 204 o|1 202 132 o|
|Onde DPCM mesurée|309 952 o|427 135 o|518 347 o|619 888 o|
|Bande passante théorique de l’échantillon|4 kHz|5,51 kHz|6,69 kHz|8 kHz|

Ajouter quelques dizaines d’octets aux ondes pour la banque, la piste et l’en-tête du morceau. [FORMATS_MESURES.csv](FORMATS_MESURES.csv) contient les tailles exactes, la durée et le SNR de quantification/compression. Le SNR est comparé à l’entrée **déjà mono et rééchantillonnée à la même fréquence** ; il ne mesure donc pas la perte des aigus du disque original. À 13 379 Hz, il est d’environ 31,8 dB pour PCM et 24,7 dB pour DPCM.

Le mixeur reste à 13 379 Hz dans les variantes usuelles : stocker à 16 kHz n’augmente pas automatiquement la bande passante de sortie et peut introduire de l’aliasing lors du rééchantillonnage natif. La variante mixée à 18 157 Hz teste une voie qui peut conserver davantage d’aigu. La démo mono ne préserve pas la spatialisation stéréo ; deux flux doubleraient à peu près le stockage et utiliseraient deux voix.

Un contrôle supplémentaire compare la sortie DPCM réelle et la conversion d’entrée dans la bande jusqu’à 2 kHz : corrélation alignée **0,991** sur deux secondes. Cela confirme que le signal issu de l’enregistrement traverse effectivement le moteur ; ce n’est ni une note de qualité d’écoute ni un SNR pleine bande. Voir [IDENTITE_SIGNAL_B.json](IDENTITE_SIGNAL_B.json).

La RAM statique du build existant est déjà proche des limites : **261 044 octets d’EWRAM et 29 824 d’IWRAM**. Aucune allocation du morceau complet ou nouveau tampon de streaming n’est ajoutée ici. Un décodeur IMA-ADPCM externe nécessiterait une autre intégration ; LZ77 seul demanderait soit une décompression complète trop grande pour la RAM, soit un lecteur par blocs à développer. Ces solutions et un décodeur MP3 embarqué ne sont **pas implémentés ni validés** par cette expérience.

## Conséquences sur la ROM et nombre de morceaux

La cartouche cible reste plafonnée à **32 Mio = 33 554 432 octets**. Le fichier de travail est rembourré à **16 Mio**, ce qui laisse **16 Mio** pour les ajouts sans toucher un seul de ses octets. Le dernier octet lié utile est à **15 480 620** : un futur rebuild pourrait récupérer les **1 296 596 octets** de rembourrage final, soit une marge de **18 073 812 octets**. Cette récupération n’a pas été faite dans la ROM de production. Le grand intervalle réservé avant les graphismes n’est pas compté comme espace libre.

Les durées des 22 références validées totalisent **3 814,191 s**. Sans convertir un autre titre, on projette leur coût à partir de ces durées. Ce scénario conserve les fichiers fournis complets, y compris leurs répétitions et fades ; une future définition de boucles uniques pourrait réduire le coût, mais n’est pas inventée pour les autres titres.

|Format des enregistrements|Coût estimé des 22 fichiers complets|Nombre qui tient dans les 16 Mio libres, selon l’ordre des durées*|
|---|---:|---:|
|PCM 8 bits, 8 kHz|30 515 072 o|9 à 14|
|PCM 8 bits, 13 379 Hz|51 031 488 o|5 à 9|
|DPCM, 8 kHz|15 735 688 o|22, marge résiduelle faible|
|DPCM, 11 025 Hz|21 684 896 o|15 à 18|
|DPCM, 13 379 Hz|26 314 468 o|11 à 16|
|DPCM, 16 kHz|31 469 200 o|9 à 14|

\* Préfixes du corpus trié du plus long au plus court, ou inversement ; ce ne sont pas des garanties de production de ces arrangements. Les budgets n’incluent pas une réserve pour d’autres ajouts au jeu.

Pour **le cycle de vélo et vingt autres fichiers complets** parmi les 21 références restantes, le DPCM à 13 379 Hz demanderait environ **23,95 à 25,04 Mo** supplémentaires : cela dépasse même la marge après récupération du rembourrage. Le DPCM à 8 kHz demanderait environ **14,32 à 14,97 Mo** : possible théoriquement, au prix du son mono limité à 4 kHz et d’une faible marge. On ne peut donc pas annoncer vingt longs enregistrements de bonne qualité dans la ROM actuelle sans sélection, boucles plus courtes ou compromis de fréquence.

Pour A, seuls **2 160 et 3 824 octets** sont mesurés sur ce thème. Avec les banques existantes, le stockage de 22 arrangements de taille comparable n’est pas le facteur bloquant. Une enveloppe de travail **2 à 20 Kio par arrangement**, hypothèse non mesurée sur les autres titres, donnerait environ 44 à 440 Kio pour 22. De nouvelles banques augmenteraient ce budget. Le problème principal reste le travail nécessaire pour une bonne partition, pas la capacité ROM. Aucun nombre garanti d’arrangements complets n’est déduit d’un unique morceau.

Les détails, hypothèses et coûts par référence sont dans [STOCKAGE_SCENARIOS.csv](STOCKAGE_SCENARIOS.csv), [COUTS_22_REFERENCES_ESTIMES.csv](COUTS_22_REFERENCES_ESTIMES.csv) et [STOCKAGE.json](STOCKAGE.json). **Aucun autre morceau n’a été adapté ou converti.**

Il faut distinguer une composition complète d’un fichier qui la joue deux fois. Pour Bicycle Theme, conserver un cycle de 75 s au lieu du fichier de 155 s retire une répétition, sans supprimer la seconde moitié de la composition. Les autres pistes n’ont pas encore cette définition validée. À titre de seuil, le cycle du vélo plus vingt cycles uniques d’une durée moyenne d’environ **118 s maximum** pourraient tenir en DPCM 13 379 Hz dans les 16 Mio libres, sans réserve. Un scénario hypothétique de vingt cycles de **90 s** et du vélo coûte environ **12,94 Mo** et tiendrait. Cela ne prouve ni que ces durées sont celles des autres compositions ni que les 22 thèmes sont intégrables ; l’audit des boucles uniques doit précéder un verdict global de stockage.

## Recommandation

Écouter d’abord **B DPCM à 13 379 Hz**, puis son équivalent PCM pour décider si la différence de compression est acceptable. Cette méthode garde la musique source et s’insère dans le moteur existant avec une voix PCM. Le PCM est plus fidèle au signal rééchantillonné mais presque deux fois plus coûteux ; le DPCM est le meilleur candidat de stockage à comparer.

Pour l’ensemble du jeu, je recommande de préparer un **budget hybride** : conserver les thèmes Pokémon efficaces, réserver certains enregistrements à des thèmes choisis, définir leurs boucles individuellement et utiliser des arrangements vérifiés pour les autres besoins. Ne pas lancer la transcription automatique A en série. Si l’objectif devient de conserver tous les longs enregistrements, le 8 kHz DPCM serait un compromis de place à juger à l’écoute, et non une promesse de qualité équivalente aux OST.

**Verdict de l’expérience : B est techniquement viable ; A2 reste une proposition de reconstruction non certifiée. La bande-son complète n’est pas encore autorisée à l’intégration.** Le raccord définitif, la fréquence et les affectations attendent la comparaison du créateur. Aucune affirmation d’écoute humaine par l’agent n’est faite.

## Préservation et reproduction

Branche expérimentale locale : **`audio/experimentation-pcm-bicycle`**. Les sources et la ROM de travail sont comparées au manifeste initial ; les copies modifiées vivent uniquement dans `/workspace/private-audio/bicycle-ab/`. Les ROM de test ajoutent les données et remplacent seulement le pointeur de `MUS_CYCLING`, sans modifier le code du moteur ou les données de gameplay. Les [contrôles finaux](CONTROLES_FINAUX.json) vérifient aussi que tous les autres octets de chaque copie ROM correspondent à la ROM d’origine et que les sources précédentes sont intactes. `make -j4` ne reconstruit rien et réussit ; la compilation n’est pas utilisée comme preuve de qualité musicale.

```sh
cd /workspace/Pokemon-Yokai-Watch
. /workspace/.setup/env.sh
export PYTHONPATH=/workspace/.setup/prototype-python:/workspace/.setup/music-python
export OPENBLAS_NUM_THREADS=1
make -C tools/wav2agb -j2
python3 tools/yokai_music/experience_assets.py
python3 tools/yokai_music/experience_arrangement.py
python3 tools/yokai_music/experience_suite.py
python3 tools/yokai_music/experience_select.py
python3 tools/yokai_music/experience_rapport.py
python3 tools/yokai_music/experience_livrer.py
python3 tools/yokai_music/experience_verifier.py
```

Les scripts s’appuient sur l’ELF et les outils préparés du projet, ainsi que sur les mesures privées du prototype précédent. Les dépendances utilisées sont déjà présentes ; aucune nouvelle activation d’environnement n’est requise. Les consignes cloud d’activation existantes restent applicables. Pour d’autres machines, retrouver les références légitimes et recompiler le projet ; ne pas copier les adresses ou une ROM complète depuis ce rapport.
