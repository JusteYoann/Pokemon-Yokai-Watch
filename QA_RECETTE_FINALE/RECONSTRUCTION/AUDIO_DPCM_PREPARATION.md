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
