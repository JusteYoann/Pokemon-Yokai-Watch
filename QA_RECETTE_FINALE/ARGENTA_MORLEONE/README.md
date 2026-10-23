# Argenta : cinématique et affectations musicales

Branche : `feature/argenta-morleone-musique`. Base Mafiamille `1bf5774d8` ; récupération sélective des ressources techniques audio depuis `837bd1757`, sans fusion. Premier jalon publié : `b75d2f42a`. Les ressources audio protégées, ROM et sauvegardes ne sont pas publiées.

## Résultat

La première arrivée depuis la Route 2 déclenche une seule fois la scène : appel de Matt, rassemblement des habitants, discours exact de Don Morléone, départ des quatre gardes et de Don, dispersion puis explication de Matt. Aucun combat ajouté. Les textes validés figurent dans `DIALOGUES_VALIDES.json` ; seuls les retours de ligne sont adaptés à la boîte du jeu.

Le conflit entre Matt et Don est corrigé localement : Matt utilise la palette existante dans la banque 6, Don et les gardes conservent la banque 10. Aucun dessin, palette source ou animation n'est modifié. Les déplacements ne traversent aucun obstacle ; le maximum observé est de 12 objets actifs, sous la limite de 16.

| Musique | Affectation effective |
| --- | --- |
| Bada-Bing Tower | Discours de Don ; utilisation existante à la Sylphe conservée |
| Katies House | Maison de Matt à Bourg Palette |
| Mystic Grove | Extérieur de Lavanville conservé, conformément à la dernière décision |
| Enma Villa | Disponible, non affectée ; aucune modification de la Ligue |
| Zombie Night (Town) | Disponible dans l'emplacement 360, non affectée ; remplace Mount Wildwood dans la bibliothèque |

La bibliothèque privée contient 31 pistes liées, dont Enma Villa et Zombie Night laissées en réserve. Les données encodées, en-têtes de boucle et gains des 30 autres pistes sont identiques à ceux de la référence audio. Final Battle conserve la variante C. Enma Track conserve sa lecture unique originale.

Zombie Night reste en lecture unique originale : aucun raccord approximatif, redémarrage ou fondu ajouté. La décision de la laisser sans affectation évite d'introduire un silence en exploration. Une affectation future demandera une nouvelle décision, ainsi qu'une écoute humaine pour toute boucle proposée. Son gain privé seul passe de 256 à 370 (Q8). Mesures dans le mélangeur mGBA : −32,0 → −28,9 LUFS ; pic vrai −16,7 → −13,6 dBTP ; aucun échantillon écrêté. Analyse EBU R128 avec filtre de mesure à 20 Hz ; aucun filtre ajouté au jeu. Ces mesures ne constituent pas une validation musicale à l'écoute.

## Vérifications réellement effectuées

Compilation publique et privée réussies. Les rapports ci-dessous correspondent aux empreintes finales, sauf `ZOMBIE_NIVEAUX_AVANT.json`, mesure historique avant correction du gain.

- `public`, `prive`, `katie-public`, `katie-prive` : 16 parcours complets dans le moteur mGBA libretro, par la connexion réelle Route 2 → Argenta, sur les quatre cases d'arrivée. Interactions par manette, progression jusqu'à la libération du joueur ; aucune modification de la ROM de test. Les fixtures initialisent une nouvelle partie et sa position sans rejouer tout le début de l'aventure.
- Palettes simultanées : vérification des banques et des 32 octets des palettes de Matt et Don par rapport aux ressources de la ROM ; captures natives 240×160 publiées. `CAPTURES_MGBA.png` assemble quatre captures privées agrandies ×2 par nearest-neighbor. Les GIF montrent le déroulement, à une cadence de prélèvement de test.
- `sauvegarde-public`, `sauvegarde-prive` : sauvegarde Flash réelle et rechargement avant et après la scène ; reprise de la scène en attente ; absence de déclenchement lors d'une revisite ; ancienne progression conservée. Les anciennes sauvegardes ayant déjà visité Argenta ne reçoivent pas la scène rétroactivement.
- `rejeu-developpement`, `rejeu-fichier-sav` : rejeu isolé puis restauration exacte des deux blocs de sauvegarde. Le fichier fourni reste intact. L'essai avec fichier utilise une sauvegarde de contrôle, pas une sauvegarde personnelle du joueur.
- `musiques` : entrée par la porte de la maison de Matt ; trois retours de boucle Katie ; reprise après fanfare d'objet ; bruitage et cri sans perte de musique ; Lavanville, Tour Pokémon, Ligue et Sylphe contrôlés ; lecture isolée de Zombie jusqu'à sa fin, sans redémarrage.
- Transitions de la scène, pour les 16 parcours : musique de Route 2 → Argenta → Bada-Bing → musique d'Argenta. Les en-têtes audio sont suivis pendant le parcours. La compilation publique conserve ses musiques de secours, sans échantillons Yo-kai.
- `AUDIO_INTEGRITE.json` : comparaison binaire des 30 autres pistes avec la référence audio ; 31 pointeurs valides ; gains des 377 autres identifiants identiques ; limites de ROM vérifiées.
- `verifier_scene_argenta.py` : dialogues approuvés, scripts et textes préexistants, équipes, cartes hors modifications autorisées et ressources protégées contrôlés. Aucun changement de statistiques, évolutions ou sprites.

Limites : tests automatisés du moteur, sans écoute humaine ni parcours intégral de l'aventure. Les tests de cette mission ne remplacent pas une recette complète du jeu. Aucun problème bloquant détecté dans le périmètre testé.

## ROM finales privées à l'environnement

| Profil | Fichier | Octets | SHA-256 |
| --- | --- | ---: | --- |
| Public, musiques de secours | `pokefirered.gba` | 16 777 216 | `1f2f5daa51b0f46b5e68ccd2eeff431b4d98d76adf790aa3af0fc2b22353b439` |
| Privé, 31 OST | `pokefirered_audio.gba` | 31 589 579 | `a8211bafc29ab8e750c412dc921b5989b8e443548095b9b66f179c78efdf18bb` |

La ROM privée occupe 30,13 Mio ; marge avant 32 Mio : 1 964 853 octets. Les ROM ne sont pas incluses dans Git.

## Reconstruction et rejeu

Même environnement de compilation que le projet, GCC ARM/agbcc et mGBA libretro ; FFmpeg utilisé pour la conversion reproductible : `7.1.5-0+deb13u1`. `ZOMBIE_PROVENANCE.json` fournit les empreintes source et PCM. Une seconde conversion vérifiée produit les mêmes 680 146 octets DPCM. Les chemins suivants désignent les ressources privées locales, non fournies par Git :

```sh
source /workspace/.setup/env.sh
python3 tools/yokai/preparer_ost_dpcm.py \
  --extracted-manifest /workspace/private-audio/extracted/manifest-private.json \
  --private-output /workspace/private-audio/argenta-repro-zombie \
  --numbers 14 --jobs 1
python3 tools/yokai/generer_audio_prive.py \
  --reuse-26-dir /workspace/private-audio/audio30-integration \
  --gap-source-dir /workspace/private-audio/argenta31-full-inputs \
  --output /workspace/private-audio/argenta-integration
make -j6
make -j6 YOKAI_AUDIO_DIR=/workspace/private-audio/argenta-integration
python3 tools/yokai/verifier_scene_argenta.py
```

Le dossier privé `argenta31-full-inputs` contient les cinq sources complètes encodées 05/08/13/14/25, et non des extraits de prévisualisation. L'outil conserve les points approuvés et la lecture unique des pistes 05/14.

Rejeu réservé au développement, sans option ajoutée au jeu :

```sh
python3 tools/yokai/rejouer_scene_argenta_mgba.py \
  --save-file /chemin/vers/une-copie.sav \
  --output /tmp/rejeu-argenta
```

Utiliser une sauvegarde brute compatible de 131 072 octets. Le test charge ses données dans une instance temporaire, rejoue la scène en mémoire et restaure les blocs de progression ; il n'écrit jamais dans le fichier donné. Les outils utilisent `mgba_rpc.py` et l'environnement mGBA du projet. Aucun menu de triche ni mécanisme de rejeu persistant n'est livré dans la ROM.

## Clôture du périmètre

La mission Argenta et les affectations autorisées sont vérifiées dans les limites ci-dessus. Mystic Grove reste à Lavanville ; Zombie Night et Enma Villa attendent une utilisation future. Aucun autre chantier commencé et aucune branche fusionnée.
