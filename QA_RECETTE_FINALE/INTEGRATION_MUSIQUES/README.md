# Intégration musicale optionnelle — état du premier jalon

Le vélo joue réellement Bicycle Theme dans la ROM musicale compilée, via SELECT et l’objet enregistré. Cinq boucles natives complètes, bruitage, cri, sauvegarde et seconde pression SELECT pour revenir à pied/au thème de zone ont été testés dans mGBA. La sortie audio correspond au sample encodé (corrélation dans la bande1kHz). Cela dépasse une simulation du mixer ou une simple conversion. L’écoute perceptive reste à distinguer de ces mesures ; la démo réelle8s est privée.

Le jeu dispose de20identifiants musicaux dédiés avec repli natif public. La version privée utilise une table de pointeurs générée, sans remplacer globalement les thèmes natifs partagés. Les deux modes ont des noms/objets distincts (`pokefirered.gba` / `pokefirered_audio.gba`, build/firered /build/firered_audio), empêchant de réutiliser les mauvais flags. Les starts, pauses/reprises et arrêts m4a résolvent tous le même en-tête. Aucune modification du décodeur ou du mixer n’est nécessaire. Aucune donnée de gameplay ne change.

Premier groupe câblé : vélo1 ; Domniscian2 ; Tour4 ; combat Seigneur Enma6 ; Sylphe occupée11 ; Bois Baies14 ; Île2 16 ; Repaire Rocket17 ; employés et Mafiamille20. Les résultats de recette sont détaillés par musique dans TEST_MGBA.json, **ne pas assimiler câblage à validation**. Les autres titres sont conservés, sans suppression. Les affectations Nathan/Katie et Céladopole sont prêtes avec repli tant que leurs boucles ne sont pas suffisamment établies. La Sylphe libérée reprend sa musique native. Matt n’est pas ciblé.

Quinze sources présentent des répétitions exploitables, affinées à l’échantillon ; ces points sont explicitement enregistrés dans data/yokai/audio_loops.json, pas redéduits aléatoirement à chaque build. L’introduction est conservée une fois, puis l’échantillon boucle ; le vélo commence directement sur le passage répété. L’alignement local de phase déplace le point de moins de100ms au sein d’une section déjà périodique. Cela préserve la durée du cycle musical et évite de raccourcir arbitrairement une phrase.

Les cinq autres sources (3/5/7/8/12) ne sont pas éliminées : leurs formes ou arrangements ne donnent pas encore une répétition suffisamment sûre avec la comparaison de forme d’onde. Les pistes9/10/13/15/18/19 préparées ne sont pas annoncées intégrées à des événements inexistants ou non encore retenus. Aucune nouvelle quête n’est développée dans ce jalon.

## Reconstruction publique et privée

Compilation publique habituelle : `source <installation>/env.sh` puis `make -j4`. Aucune ressource protégée requise ; la version publique joue les thèmes de repli et **n’est pas la bande-son finale**.

Prérequis audio : FFmpeg7.1.5, libarchive, Python avec `pip install -r tools/yokai/requirements-audio.txt`. Extraire les lots fournis et recréer les WAV mono13379Hz avec les scripts publics documentés dans PREPARATION_20_OST_DPCM.md. Les empreintes attendues sont dans data/yokai/audio_loops.json (WAV) et TAILLES_ET_ETAT.json (MP3). Puis :

```sh
python3 tools/yokai/generer_audio_prive.py --full-source-dir "$YOKAI_AUDIO_DIR/dpcm-full" --output "$YOKAI_AUDIO_DIR/integration" --jobs 4
make -j4 YOKAI_AUDIO_DIR="$YOKAI_AUDIO_DIR/integration"
YOKAI_AUDIO_DIR="$YOKAI_AUDIO_DIR/integration" YOKAI_QA_ROM="$PWD/pokefirered_audio.gba" python3 tools/yokai/tester_musiques_integrees_mgba.py
```

Ne jamais ajouter les WAV/DPCM générés, les MP3 ni une ROM au dépôt public. Le générateur exige un dossier de sortie hors du checkout et vérifie les empreintes des sources. Les morceaux manquants ne sont pas remplacés par une autre OST : la table utilise le repli Pokémon explicite. Le masque natif `YokaiGetPrivateAudioMask()` indique les données réellement présentes. Les preuves portent les empreintes de la version musicale testée.
