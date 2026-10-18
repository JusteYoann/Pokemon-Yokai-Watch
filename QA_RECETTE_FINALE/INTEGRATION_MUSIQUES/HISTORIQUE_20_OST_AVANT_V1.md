# Dix OST réellement intégrées dans la ROM musicale privée

Le profil actif contient **10 des20OST sélectionnées**. Elles sont compilées dans le moteur m4a et déclenchées par les cartes, le vélo et les combats existants. Les événements n’utilisent pas un lecteur externe ou une ROM patchée pour simuler cette intégration. **La compilation publique sans sources privées joue des musiques natives de repli : elle n’est pas la bande-son finale.**

Le premier groupe de neuf a été complété par Decisive Battle au Conseil4. Les équipes et l’histoire ne changent pas. Le routage de51combats est contrôlé nativement : les huit versions des combats du Conseil4 utilisent la piste15 ; Matt et les champions d’arène conservent leurs thèmes Pokémon. Hinozall (English) est bien le thème personnel utilisé pour Domniscian. The Ghoulfather est disponible et reste sélectionné pour Don Morleone, mais **son enregistrement n’est pas encore actif**, faute de boucle suffisamment sûre. Aucun thème Sangokushi générique ne le remplace.

## Sélection complète et coûts mesurés

Les tailles ci-dessous sont celles des WaveData réellement encodées, en mono **13 379Hz**, en-tête16octets inclus. Une donnée préparée sans déclencheur en jeu n’est pas comptée comme intégrée. Les versions complètes des20références coûtaient23 248 952octets ; les quinze sections optimisées coûtent8 750 916octets. En gardant encore intégralement les cinq sources aux boucles non verrouillées, le total de données descend à14 024 099octets, soit **9 224 853octets économisés**. Aucun morceau n’a été supprimé.

| N° | Morceau | Destination | Complet, octets | Optimisé, octets | État |
|---:|---|---|---:|---:|---|
| 01 | Bicycle Theme | Vélo (SELECT) | 1069018 | 518314 | Intégrée ; recette native |
| 02 | Vs. Hinozall (English) | Combat Domniscian | 840328 | 397303 | Intégrée ; recette native |
| 03 | vs. The Ghoulfather | Combat Don Morleone | 1702255 | — | Boucle à verrouiller ; repli natif |
| 04 | Infinite Tunnel | Tour de Lavanville,7 étages | 1581541 | 784624 | Intégrée ; recette native |
| 05 | Enma Track | Dialogue Seigneur Enma | 821056 | — | Boucle à verrouiller ; repli natif |
| 06 | Vs. Zazelmare | Combat Seigneur Enma | 1613782 | 794623 | Intégrée ; recette native |
| 07 | Nates House | Maison Nathan,2 étages | 859072 | — | Boucle à verrouiller ; repli natif |
| 08 | Katies House | Maison Katie,2 étages | 978565 | — | Boucle à verrouiller ; repli natif |
| 09 | Blasters Hideout | Base Coach Antonic | 1201480 | 589990 | Préparée ; événement de quête absent |
| 10 | Yo-kai Watch Blasters! Theme | Combat Coach Antonic | 1156963 | 585106 | Préparée ; événement de quête absent |
| 11 | Bada-Bing Tower | Sylphe occupée,11 étages | 1452148 | 677968 | Intégrée ; recette native |
| 12 | Blossom Heights | Céladopole extérieure | 912235 | — | Boucle à verrouiller ; repli natif |
| 13 | Enma Villa | Approche Enma si justifiée | 1455382 | 680938 | Préparée ; scène d’approche non ajoutée |
| 14 | Mount Wildwood in the Past | Bois Baies | 946126 | 446836 | Intégrée ; recette native |
| 15 | Decisive Battle | Conseil4,4 combats et4 revanches | 886825 | 458485 | Intégrée ; recette native |
| 16 | Harrisville | Île2 extérieure | 1296256 | 621307 | Intégrée ; recette native |
| 17 | Somewhere A Bit Dodgy (BBQ) | Repaire Rocket,4 sous-sols et ascenseur | 1572334 | 767530 | Intégrée ; recette native |
| 18 | Messenger from the Future ~ Robonyan Arrives | Dialogue scientifique | 898375 | 409414 | Préparée ; événement de quête absent |
| 19 | Vs. Robonyan 3000 | Combats scientifique | 550555 | 283882 | Préparée ; événement de quête absent |
| 20 | Mini Boss Battle | Employés Domniscian et Mafiamille | 1454656 | 734596 | Intégrée ; recette native |

**ROM musicale actuelle : 21,667,712octets (20.66Mio)** sur32Mio ; marge restante : 11.34Mio. Le build public est paddé à16Mio. La projection des20sources avec les quinze optimisations représente environ28,12Mio de programme et samples, hors petits en-têtes et alignements à confirmer dans le build complet. C’est une perspective de stockage favorable, **pas une preuve de20intégrations**.

Les introductions des combats sont conservées une fois ; les sources répétées et les fins en fondu inutiles sont exclues. Le vélo démarre directement sur sa section principale, vers5,006s de la source. Les points exacts, leurs empreintes et leurs corrélations sont dans `data/yokai/audio_loops.json`. Les raccords sont alignés à l’échantillon dans une portion déjà répétée ; le pipeline ne choisit pas une coupure au hasard lors du build.

## Vérifications réalisées et réserves

- TEST_MGBA.json : dix déclencheurs réels en ROM, au moins cinq retours de boucle par piste et cinq fenêtres audio de raccord comparées à la référence encodée. Le Bois Baies effectue six cycles : un raccord est superposé à un cri ambiant natif, les cinq autres restent contrôlés ; les cris ne sont pas désactivés.
- Sélection du vélo par l’objet enregistré et SELECT, second SELECT pour revenir à pied et à la musique de zone ; véritables combats Domniscian, Seigneur Enma, employé et Lorelei, puis retour à la musique d’exploration.
- TEST_INTERRUPTIONS_MGBA.json : fanfares objet/niveau/soin, pause/reprise répétée, fondus temporaires, volume restauré, ancienne musique de vélo et lecture/écriture Flash. La perte de voix du sample après fanfare a été reproduite puis corrigée.
- TEST_LIBERATION_SYLPHE_MGBA.json : véritable déclencheur de Giovanni2, combat et libération ; la musique normale revient grâce au script, sans appel musical manuel du test.
- VERIFICATION_LIAISON.json et CONTROLE_ROM_PRIVEE.json : octets des samples réellement liés, masques actifs, bons replis publics, limite32Mio,151espèces/apprentissages/évolutions et ressources graphiques protégées.
- REPRODUCTIBILITE.json : source GitHub, builds public/privé avec outils indépendants et empreintes comparées ; les ressources privées sont fournies séparément.

Les fixtures utilisent des téléportations et flags de progression pour isoler les événements, ainsi qu’une équipe artificiellement forte pour terminer les combats. Elles ne prouvent pas un parcours complet ni l’équilibrage. Les essais conservent les vrais contrôleurs de combat, scripts, équipes adverses, sons et animations. Aucun nouveau PNJ, aucune quête ni aucune modification de gameplay n’est ajouté pour installer les morceaux.

**L’écoute perceptive humaine n’a pas été effectuée dans cet environnement.** Les corrélations et raccords numériques valident le signal produit, sans certifier que chaque arrangement, chant ou transition est artistiquement optimal. Les performances sur console physique n’ont pas été mesurées ; mGBA et la cadence native des boucles ont été vérifiés. Les autres dix pistes restent à intégrer : cinq nécessitent une étude musicale de boucle ; quatre attendent les événements Coach/scientifique, non créés durant cette mission ; Enma Villa reste facultatif tant qu’une scène cohérente ne le justifie pas. The Very Curious Yo-kai Watch reste supplémentaire, non intégré et n’a remplacé aucun des20choix.

## Reproduction publique et privée

Prérequis de compilation : outils Debian/agbcc épinglés documentés dans RECUPERATION_PROJET. Le jeu public ne nécessite pas Python audio ni MP3. Pour la préparation privée : FFmpeg7.1.5, libarchive, Python avec `tools/yokai/requirements-audio.txt`. Utiliser des chemins sans espaces, comme pour agbcc.

```sh
# Activer la chaîne publique installée
source /workspace/.setup/env.sh
make -j4

# Fournir séparément les archives légitimement disponibles
export YOKAI_AUDIO_DIR=/chemin/prive/audio
python3 tools/yokai/extraire_audio_prive.py --output "$YOKAI_AUDIO_DIR/extracted" "$YOKAI_AUDIO_DIR/archives/"*.rar
python3 tools/yokai/preparer_ost_dpcm.py --extracted-manifest "$YOKAI_AUDIO_DIR/extracted/manifest-private.json" --private-output "$YOKAI_AUDIO_DIR/full" --jobs 4
python3 tools/yokai/generer_audio_prive.py --full-source-dir "$YOKAI_AUDIO_DIR/full" --output "$YOKAI_AUDIO_DIR/integration" --jobs 4
make -j4 YOKAI_AUDIO_DIR="$YOKAI_AUDIO_DIR/integration"

# Le nom de ROM détermine aussi le bon ELF pour les tests
YOKAI_AUDIO_DIR="$YOKAI_AUDIO_DIR/integration" YOKAI_QA_ROM="$PWD/pokefirered_audio.gba" python3 tools/yokai/tester_musiques_integrees_mgba.py
YOKAI_AUDIO_DIR="$YOKAI_AUDIO_DIR/integration" YOKAI_QA_ROM="$PWD/pokefirered_audio.gba" python3 tools/yokai/tester_interruptions_musique_mgba.py
```

Le générateur vérifie les WAV attendus par leurs empreintes. Les20MP3 sont identifiés dans TAILLES_ET_ETAT.json ; les enregistrements, WAV, DPCM et ROM musicaux ne sont **jamais publiés** sur GitHub. Le dépôt contient le code, les paramètres, les scripts et les preuves non musicales. Les modes public et privé ont des noms/objets distincts (`pokefirered.gba`, `pokefirered_audio.gba`), avec repli explicite pour les pistes inactives. Un masque natif permet de vérifier le profil réellement chargé.

Dans cette session, les démonstrations8s et fenêtres de raccord réellement enregistrées par mGBA sont conservées en privé dans `/workspace/private-audio/integration-v2/previews/` (`01-mgba-8s.wav`, `02-mgba-8s.wav`, etc. et fichiers `NN-loop-K.wav`). Elles restent distinctes des MP3 sources. Sans les ressources externes, une reconstruction ne sera pas musicalement identique à la version privée.

Prochain point de reprise : terminer les boucles des pistes3/5/7/8/12, en conservant leurs introductions et sans coupe arbitraire. Ne pas reconstruire le pipeline ni les dix intégrations validées. Les événements de quête ne deviennent pas prioritaires pour augmenter artificiellement le compteur musical.
