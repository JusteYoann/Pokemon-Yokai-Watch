# Profil audio post-B13 — jalon 18 OST, pas une bêta finale

Les fichiers sonores restent externes au dépôt public. Les sources publiques compilent avec les thèmes natifs de repli ; **elles ne produisent pas une bande-son identique sans les sources privées**. La procédure B13 Windows, ses sources épinglées et son SHA de référence n’ont pas été modifiés par ce chantier.

Pour ce nouveau profil, suivre l’installation documentée dans `INSTALL.md` et le verrouillage de la chaîne B13 (agbcc `da598c1d918402c42c0c0d7128ba14567f3175e9`, binutils2.44, bibliothèques ordonnées/validées). Python3 est nécessaire aux dérivés graphiques ; NumPy, SciPy et FFmpeg sont nécessaires à la préparation audio/QA, Pillow au QA graphique. Le décodeur mesuré est FFmpeg7.1.5 Debian13 ; les SHA des WAV interdisent de substituer silencieusement un autre décodage.

À partir des archives acquises légalement, extraire le manifeste privé via `tools/yokai/extraire_audio_prive.py --help` ; les 22 noms exacts et SHA MP3 sont dans `PROVENANCE_18_OST.json`. Les chemins du manifeste pointent uniquement vers votre dossier privé. Préparer hors du dépôt :

```sh
python3 tools/yokai/preparer_ost_dpcm.py \
  --extracted-manifest /chemin/prive/manifest-private.json \
  --private-output /chemin/prive/full-sources --jobs 2
python3 tools/yokai/generer_audio_prive.py \
  --full-source-dir /chemin/prive/full-sources \
  --output /chemin/prive/post-b13-integration --jobs 2
make -j4 YOKAI_AUDIO_DIR=/chemin/prive/post-b13-integration
```

Le premier outil prépare les références complètes pour l’analyse (aucune intégration de ces enregistrements complets). Le deuxième vérifie les SHA des WAV, découpe aux positions verrouillées dans `data/yokai/audio_loops.json` puis produit les 18 DPCM et la table native **31 emplacements**. Il faut régénérer ce profil : une ancienne table B13 à26 emplacements ne doit pas être réutilisée. Une table sans `gYokaiPrivateSlotCount` échoue au lien plutôt que d’être lue hors limites.

Résultat local : `pokefirered_audio.gba`, jouable dans mGBA, sans publication du fichier. Les contrôles `verifier_liaison_audio.py`, `verifier_attributions_post_b13.py` et `verifier_rom.py` vérifient les échantillons liés, les425 cartes et les données/graphismes. Utiliser leurs variables de rapport `YOKAI_AUDIO_LINK_REPORT` et `YOKAI_VERIFY_REPORT` pour conserver les anciens jalons.

18 pistes actives,22 sélectionnées : Enma5, Nate7, Blossom12 et Final25 restent en repli natif en attente de boucles de sections complètes fiables. Les cinq nouvelles pistes sont27–31. Les treize anciens DPCM restent identiques octet pour octet. Les gains sont reproduits avec `generer_calibration_mixeur.py` à partir des mesures JSON, sans traitement arbitraire des enregistrements.

Contrôle rapide des sources sans reconstruire la ROM :

```sh
python3 tools/yokai/verifier_sources_audio_post_b13.py \
  --extracted-manifest /chemin/prive/manifest-private.json \
  --private-output /chemin/prive/redecodage --jobs 2
```

Cet outil vérifie le SHA des MP3, redécode les18 pistes actives, puis exige les SHA WAV verrouillés. Il échoue en cas d’écart ; ne pas changer les empreintes pour contourner l’échec.
