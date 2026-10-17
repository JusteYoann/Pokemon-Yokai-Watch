# Reprise de la méthode B : état technique, sans intégration annoncée

La direction validée reste l'audio échantillonné **DPCM mono à 13 379 Hz**. Les 80 références MP3 récupérées restent hors du dépôt public. Aucun arrangement MIDI n'est substitué à cette décision. Les anciens rapports musicaux sont des archives de sessions, pas une preuve que leurs outils ou données sont présents dans les sources actives.

## Ce que les sources actuelles permettent de vérifier

- `src/m4a_1.s`, `SoundMainRAM_Unk1` et `SoundMainRAM_Unk2`, contiennent déjà le chemin de décompression DPCM du pilote m4a. Le format comporte **33 octets pour 64 échantillons**, après l'en-tête WaveData de 16 octets. Ce n'est pas de l'IMA ADPCM.
- Le bloc démarre par un échantillon 8 bits. Le premier delta est dans le demi-octet bas de l'octet suivant ; viennent ensuite les deltas hauts/bas. La table signée est `0,1,4,9,16,25,36,49,-64,-49,-36,-25,-16,-9,-4,-1` (`src/m4a_tables.c`). L'accumulation se replie sur 8 bits.
- Le cache de décodage existant est de 64 octets. Son indice est invalidé au début du traitement de chaque canal ; la présence d'un tampon commun n'établit donc pas, à elle seule, une incompatibilité avec les cris. La coexistence réelle BGM/cris/effets doit encore être mesurée.
- Le pilote démarre déjà au mode `SOUND_MODE_FREQ_13379`. Cela évite de présumer qu'une réécriture complète du moteur audio serait nécessaire. Cela ne prouve ni la qualité des boucles ni la charge CPU de vingt morceaux.

## Reprise nécessaire

1. Reconstruire un encodeur local reproductible, vérifier son résultat contre le décodeur natif avec un signal de test libre, puis le valider sur les références privées.
2. Relever les points d'introduction et de boucle de chaque piste, écouter les raccords et tester au moins cinq répétitions dans mGBA avec effets sonores.
3. Mesurer les tailles exactes, l'activité du moteur et les transitions de carte, vélo, dialogue et combat. Préserver les thèmes Pokémon des utilisateurs non ciblés d'un identifiant partagé.
4. Documenter le build avec `YOKAI_AUDIO_DIR` ou équivalent. Les sources publiques doivent compiler avec une solution de repli explicite ; une ROM sans ressources musicales privées ne sera pas musicalement identique à la version complète.

**État actuel : aucun des 20 morceaux n'est encore intégré dans cette reconstruction.** Ce document est une inspection des sources, pas un essai de lecture en émulateur. La bande-son originale reste active pour les caméos reconstruits. Aucun MP3, enregistrement adapté ou fichier ROM n'est publié.

## Encodeur reconstruit et comparaison au décodeur natif

`tools/yokai/dpcm_m4a.py` convertit un WAV mono PCM16 dans le format WaveData natif, avec en-tête, fréquence, taille, éventuel début de boucle et blocs de 33 octets. Les notes/instruments ne sont pas reconstruits. Préparation privée, par exemple :

```sh
ffmpeg -i "$YOKAI_AUDIO_DIR/source.mp3" -ac 1 -ar 13379 -c:a pcm_s16le "$YOKAI_AUDIO_DIR/source-13379.wav"
python3 tools/yokai/dpcm_m4a.py "$YOKAI_AUDIO_DIR/source-13379.wav" "$YOKAI_AUDIO_DIR/source.dpcm" --loop-start POINT_EN_ECHANTILLONS
```

Le début de boucle doit être mesuré par morceau ; ne pas employer un point arbitraire en production. Une boucle d’échantillon permet une introduction unique puis le retour au début de boucle, mais la séquence m4a et ses transitions ne sont pas encore restaurées. Ne pas ajouter les fichiers de sortie protégés à Git.

`tester_dpcm_decodeur_mgba.py` appelle la véritable routine ARM SoundMainRAM_Unk2 du jeu, via une passerelle temporaire en RAM, sur silence, extrêmes signés, sinusoïde et rampe. Les 710 échantillons correspondent exactement au décodeur Python, y compris les limites de blocs et le repli signé. La preuve est TEST_DPCM_DECODEUR_MGBA.json. Les sources de tests sont libres et synthétiques ; aucun enregistrement original n’est publié.

L’encodeur est glouton : la fidélité musicale et l’erreur sur les attaques complexes devront être écoutées et mesurées sur les références. Ces essais ne valident pas encore la lecture BGM, les boucles, les bruitages, la charge CPU ou les transitions. Aucun des 20 morceaux n’est encore intégré ; le système public continue de compiler avec la bande-son de repli.

## Premier essai réel dans le mixer m4a restauré

`tester_dpcm_lecture_mgba.py` ajoute uniquement à une copie temporaire de la ROM un son synthétique libre : introduction 440 Hz de 0,4 s, boucle 660 Hz de 0,6 s, voix m4a, piste TIE et WaveData DPCM. La ROM de production et sa table musicale ne changent pas. Le test observe la véritable sortie audio libretro, mesure les fréquences, déclenche SE_SELECT et un cri, laisse passer plus de onze périodes et demande le retour à MUS_PALLET par PlayBGM. Rapport TEST_DPCM_LECTURE_MGBA.json. La ROM temporaire est supprimée et n’est jamais publiée.

Point technique confirmé pendant la restauration : l’en-tête WaveData de type 1 ne suffit pas. Le **type de voix doit aussi contenir le bit de compression 0x20** ; la voix testée vaut **0x28** (DPCM + fréquence fixe, à la fréquence native du mixer). Sans ce bit, les données compressées sont lues comme du PCM et le son est incorrect. Le taux source 13 379 Hz est cohérent avec le mixer ; le taux de sortie du cœur mGBA, interrogé réellement ici, vaut 65 536 Hz. Ne pas les confondre lors de l’analyse et de l’export.

L’introduction ne réapparaît pas dans les fenêtres spectrales tardives. Cela ne démontre pas encore un raccord agréable pour une musique. Les appels bruitage/cri et le maintien de la lecture sont testés ; leur équilibre perceptif reste à écouter. La reprise musicale est demandée par l’API native, pas par un véritable trajet vélo. La charge matérielle et les 20 affectations attendent leurs tests dédiés.
