# Préparation privée des vingt OST — tailles réellement mesurées

Les 80 fichiers sont récupérés et les vingt références du cahier sont toutes identifiées sans ambiguïté. Hinozall (English) et The Ghoulfather sont bien leurs thèmes personnels. Somewhere A Bit Dodgy reste affecté au Repaire Rocket. The Very Curious Yo-kai Watch est aussi présent ; il reste supplémentaire et n’a remplacé aucune des vingt références.

Les vingt enregistrements **complets, non coupés**, ont réellement été encodés en DPCM mono 13 379 Hz, sans intégration ni boucle certifiée. Coût des WaveData : **23 248 952 octets (22,17 Mio)**. Sources actuellement liées : **15 465 136 octets (14,75 Mio)**, ROM publique paddée à16 Mio. Leur somme minimale atteint **38 714 088 octets (36,92 Mio)** : dépassement de **5 159 656 octets (4,92 Mio)** de la limite32 Mio, avant même les petits en-têtes de chansons et alignements. **Les vingt sources intégrales ne tiennent donc pas telles quelles.**

La prochaine étape consiste à conserver les introductions utiles et une seule partie principale bouclable, en retirant les répétitions déjà présentes dans les enregistrements et les fins en fondu. Aucune piste n’est sacrifiée ni classée automatiquement pour suppression. Le gain réellement obtenu sera mesuré après sélection et contrôle des raccords. Une éventuelle réduction de la sélection nécessitera l’arbitrage prévu au cahier ; elle n’est pas décidée par ce tableau.

| N° | Référence | Destination prévue | DPCM complet, octets | Durée complète |
|---:|---|---|---:|---:|
| 01 | Bicycle Theme | velo | 1069018 | 154.96 s |
| 02 | Vs. Hinozall (English) | combat_domniscian | 840328 | 121.81 s |
| 03 | vs. The Ghoulfather | combat_don_morleone | 1702255 | 246.75 s |
| 04 | Infinite Tunnel | tour_pokemon | 1581541 | 229.25 s |
| 05 | Enma Track | dialogue_seigneur_enma | 821056 | 119.01 s |
| 06 | Vs. Zazelmare | combat_seigneur_enma | 1613782 | 233.93 s |
| 07 | Nates House | maison_nathan | 859072 | 124.53 s |
| 08 | Katies House | maison_katie | 978565 | 141.84 s |
| 09 | Blasters Hideout | base_coach | 1201480 | 174.16 s |
| 10 | Yo-kai Watch Blasters! Theme | combat_coach | 1156963 | 167.71 s |
| 11 | Bada-Bing Tower | sylphe_occupee | 1452148 | 210.49 s |
| 12 | Blossom Heights | celadopole | 912235 | 132.23 s |
| 13 | Enma Villa | approche_enma_si_justifiee | 1455382 | 210.96 s |
| 14 | Mount Wildwood in the Past | bois_baies | 946126 | 137.14 s |
| 15 | Decisive Battle | moment_ligue_si_pertinent | 886825 | 128.55 s |
| 16 | Harrisville | ile_deux | 1296256 | 187.90 s |
| 17 | Somewhere A Bit Dodgy (BBQ) | repaire_rocket | 1572334 | 227.92 s |
| 18 | Messenger from the Future ~ Robonyan Arrives | dialogue_scientifique | 898375 | 130.22 s |
| 19 | Vs. Robonyan 3000 | combat_scientifique | 550555 | 79.80 s |
| 20 | Mini Boss Battle | employes_mafiamille | 1454656 | 210.86 s |

## Reproduction sans publier les enregistrements

Dépendances de préparation : FFmpeg (version mesurée ci-dessus), libarchive et Python3. Le test spectral optionnel utilise `tools/yokai/requirements-audio.txt` (Pillow12.3.0, NumPy2.3.5), ainsi que les outils mGBA documentés. Ces dépendances audio ne sont pas nécessaires pour compiler le jeu public actuel.

```sh
python3 tools/yokai/extraire_audio_prive.py --output "$YOKAI_AUDIO_DIR/extracted" "$YOKAI_AUDIO_DIR/archives/"*.rar
python3 tools/yokai/preparer_ost_dpcm.py --extracted-manifest "$YOKAI_AUDIO_DIR/extracted/manifest-private.json" --private-output "$YOKAI_AUDIO_DIR/dpcm-full" --jobs 4
```

Les archives doivent être les lots fournis par le créateur. Le manifeste des références, les scripts et les tailles/empreintes sont publics ; les MP3, WAV et DPCM contenant les enregistrements restent **hors du dépôt**. Les chemins privés de cette session sont documentés dans ETAT_REPRISE.md pour la continuation ; ils ne sont pas des dépendances de compilation cachées. Aucun des vingt morceaux n’est actif dans la ROM publique : elle compile avec sa bande-son de repli. Une future version avec musique privée sera nécessairement différente musicalement sans la fourniture de ces ressources.

État de validation : décodage et lecture du format vérifiés sur signaux synthétiques dans mGBA ; conversion complète des vingt fichiers effectuée ; écoute perceptive, points de boucle musicaux, cinq répétitions de chaque véritable morceau, déclencheurs en jeu et coût ROM final **non validés**. Aucun essai de format ne vaut recette de la bande-son complète.
