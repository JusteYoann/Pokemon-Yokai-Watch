# Bande-son — sélection définitive v1.0

La mission finale remplace la sélection antérieure de20pistes. **13/15 sont réellement activées**. Les deux pistes restantes sont présentes dans les références privées mais attendent une boucle musicale fiable : Enma Track et Final Battle – Are You Ready?. Le repli natif reste explicite ; aucun autre morceau n’est présenté comme leur équivalent.

| Choix | Titre / version fournie | Emplacement | État |
|---|---|---|---|
| 01 | Bicycle Theme (YW1) | Vélo | DPCM actif |
| 02 | Vs. Hinozall (English) (BLASTERS) | Domniscian | DPCM actif |
| 03 | Infinite Tunnel (YW2) | Tour de Lavanville (7 étages) | DPCM actif |
| 04 | Vs. Zazelmare (BLASTERS) | Seigneur Enma, combat | DPCM actif |
| 05 | Bada-Bing Tower (YW3) | Sylphe occupée (11 étages) | DPCM actif |
| 06 | Decisive Battle (SANGOKUSHI) | Conseil4 et revanches | DPCM actif |
| 07 | Somewhere A Bit Dodgy (BBQ) (YW3) | Repaire Rocket | DPCM actif |
| 08 | San Fantastico (YW2) | Carmin sur Mer | DPCM actif |
| 09 | Uptown Springdale (YW2) | Céladopole extérieur | DPCM actif |
| 10 | vs. The Ghoulfather (YW3) | Don Morleone | DPCM actif |
| 11 | Enma Track (BLASTERS) | Seigneur Enma, dialogues | Boucle à terminer, repli natif |
| 12 | Mystic Grove (YW4) | Caverne Azurée (3 étages) | DPCM actif |
| 13 | Hoppers Gorge (YW3) | Mont Sélénite (3 étages) | DPCM actif |
| 14 | Final Battle – Are You Ready? (YW1) | Matt Champion uniquement | Boucle à terminer, repli natif |
| 15 | Take Care, Grandpa 1 (YW2) | Conclusion après Matt | DPCM actif |

Mount Wildwood, Harrisville et Mini Boss ne sont plus compilées dans le profil privé : retour natif au Bois Baies, à l’Île2 et pour les employés/Mafiamille. Maisons, Enma Villa et quêtes reportées restent sans ces enregistrements. Les identifiants historiques sont conservés pour compatibilité ; leur présence dans le catalogue ne signifie pas une musique active.

Pipeline13379Hz mono, codec natif33octets/64échantillons ; aucune transcription MIDI. Les sources restent extérieures au dépôt. Génération optionnelle : `preparer_ost_dpcm.py`, puis `generer_audio_prive.py`, puis `make YOKAI_AUDIO_DIR=/chemin/prive/integration`. Les WAV épinglés sont vérifiés parSHA256. Tous les outils, configurations et sources du jeu sont sur la branche ; MP3/WAV/DPCM/ROM restent privés.

## Preuves

- `TEST_MGBA.json` : douze déclencheurs (cartes, vélo enregistré, vrais combats PNJ) et60raccords audio propres ; `CONCLUSION_LIGUE_V1.json` ajoute la treizième piste et5raccords. Audio réellement enregistré du cœur mGBA, comparaison avec les DPCM liés. Chaque rapport porte l’empreinte exacte de la ROM testée. Les changements de vocabulaire intervenus après la campagne musicale sont vérifiés par la liaison et les tests ciblés récents ; les anciennes empreintes ne sont pas réétiquetées.
- `TEST_INTERRUPTIONS_MGBA.json` : reprise de voix après fanfares, pauses/fondus, legacy vélo et Flash. `ROUTAGE_COMBATS_MGBA.json` :51routes, Matt rival conservé et Champion réservé à la nouvelle piste (repli natif tant qu’elle est inactive).
- `CONCLUSION_LIGUE_V1.json` : combat réel Matt, conclusion, Panthéon, crédits et Continuer au postgame ; préparation explicite d’une arrivée à la Ligue avec équipe forte, pas une traversée complète.
- `VERIFICATION_LIAISON.json` : tous les samples actifs et leur compression sont vérifiés octet par octet dans la ROM finale de développement.
- `../VERSION_1_DEVELOPPEMENT/REPRODUCTIBILITE.json` : reconstructions depuis GitHub, avec/out audio privé régénéré, comparées aux ROM locales. Même machine cloud et outils indépendants, pas une nouvelleVM.

## Limites

Pas d’écoute perceptive humaine complète, pas de profilage sur console physique. Les transitions musicales sont des scénarios ciblés ; cela ne prouve pas toute l’aventure. Les deux raccords manquants interdisent de déclarer la sélection15 terminée. Les anciens rapports20/10pistes restent historiques, notamment `HISTORIQUE_20_OST_AVANT_V1.md` et `ETAT_20_OST.csv` ; ils ne définissent plus la version courante.

La ROM publique utilise les thèmes natifs de repli et compile sans ressources privées. Elle est volontairement différente musicalement. Instructions détaillées : `../VERSION_1_DEVELOPPEMENT/README.md`.
