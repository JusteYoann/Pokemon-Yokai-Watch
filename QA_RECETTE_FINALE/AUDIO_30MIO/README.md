# Extension musicale vers 30 Mio

**26 OST actives, contre20 au jalon précédent. ROM privée : 31 272 243 octets, soit29,82 Mio.** Les six nouvelles pistes sont effectivement déclenchées par des lieux et combats existants. Le nouveau budget de30 Mio remplace le plafond historique de20 morceaux ; la limite matérielle de32 Mio reste respectée. Branche `dev/reconstruction-finalisation`, base préservée `79e0a0282e5d1048697bfc79ab47e90b308e0d50`.

## Morceaux intégrés et déclencheurs réels

| OST | Affectation active |
|---|---|
| Blasters Hideout | Ambiance du Dojo de Safrania |
| Yo-kai Watch Blasters! Theme | Combat contre le maître Koichi du Dojo |
| Harrisville | Île2 : extérieur, port, maison, salle de jeux et les deux étages du centre de soins |
| Messenger from the Future ~ Robonyan Arrives | Rencontre des dresseurs de classe Scientifique |
| Vs. Robonyan 3000 | Combats des dresseurs de classe Scientifique |
| Mini Boss Battle | Deux employés de Domniscian et trois Mafiamilles |

Ces affectations enrichissent les événements **présents dans les sources**. Elles ne prétendent pas créer ou restaurer les quatre rencontres de la quête du scientifique ni la scène de Coach Antonic : aucune quête, équipe, récompense, condition ou représentation de personnage n'est ajoutée dans ce lot. Les scènes futures pourront réutiliser ces mêmes identifiants et samples. La musique du maître du Dojo n'est pas présentée comme un combat Coach déjà implémenté.

Les thèmes personnels Domniscian/Hinozall, Don Morleone/Ghoulfather, Enma/Zazelmare et les thèmes validés de la Ligue restent inchangés. Les 20 anciens samples et leurs gains sont conservés. Les employés/Mafiamilles utilisent désormais le thème de subordonnés qui leur était prévu, distinct de celui de leurs boss.

## Boucles et volumes

[Table des six nouvelles pistes](SIX_NOUVELLES_OST.csv) : tailles exactes, durées d'introduction et de boucle, SHA-256, volumes et destinations. Sources MP3 vérifiées contre le manifeste privé, redécodage FFmpeg, WAV identiques aux analyses antérieures. [Provenance](PROVENANCE_SOURCES.json), [analyse des boucles](ANALYSE_SIX_BOUCLES.json), [empreintes des26 samples](PROVENANCE_26_OST.json).

Les périodes complètes sont83,48 /76,80 /86,00 /58,25 /33,11 /94,43 secondes selon les pistes. Les introductions sont conservées une fois. Le raccord est aligné à moins de20ms autour des limites déjà trouvées, sans fondu croisé ni changement de tempo. Dix fenêtres successives de3 secondes ont été comparées à la reprise pour chaque piste ; toutes dépassent0,93 de corrélation. Il ne s'agit pas d'un court motif choisi seulement pour réduire la taille.

Mesure mGBA sur **l'introduction et un cycle complets**, puis correction du gain entier : de−29,1 à−28,9 LUFS, aucun écrêtage. [Avant](LUFS_AVANT.json), [après](LUFS_FINAL.json). Les vagues DPCM ne sont pas réencodées pour modifier le volume. Aucun bruitage ou cri n'est remplacé.

## Essais effectués sur la ROM finale de ce jalon

| Contrôle | Résultat |
|---|---|
| Six nouvelles musiques | **30 retours natifs de boucle** au total, cinq par piste ; intro non répétée, audio comparé au sample décodé ; [rapport](boucles/TEST_MGBA.json) |
| Bruitage, cri et Flash | Bruitage de sélection, cri terminé, sauvegarde native pendant chacune des six lectures ; même rapport |
| Routage complet |104 BGM résolus vers des OST privées,425 en-têtes de cartes compilés conformes,273 pointeurs de bruitages/jingles conservés ; [rapport](ROUTAGE_MGBA.json) |
| Thèmes spéciaux |Sélection native vérifiée pour les5 subordonnés, les3 grands caméos, Lorelei, le scientifique et Koichi ; pas11 nouveaux combats complets |
| Combat scientifique |Interaction originale avec Ted au Manoir, thème19, victoire aux boutons, retour au thème de carte. Le hook de rencontre18 est aussi testé par appel natif isolé |
| Dojo |Thème9 en exploration, interaction originale Koichi, thème10 au combat, victoire aux boutons, retour au9 |
| Employé rouge |Interaction originale, thème20 au combat, victoire aux boutons, retour à l'ambiance de la Sylphe ; [trois événements](evenements/TEST_MGBA.json) et captures |
| Fanfares |40 scénarios :14 fanfares sur Patrol Mission, puis une réception d'objet sur chacune des26 OST ; pause/reprise au curseur sans redémarrage ; [rapport](FANFARES_MGBA.json) |
| Continuité Île2/centre |Deux passages réels entrée/sortie aux boutons, même thème Harrisville, horloge avançante sans pause/redémarrage ; [rapport](portes/TEST_MGBA.json) |
| Sources privées → ROM |26 échantillons liés identiques au manifeste, compression et limites vérifiées, replis publics conformes ; [liaison](LIAISON_26_OST.json) |

Les captures ont été ouvertes et examinées. Les tests démarrent par une vraie nouvelle partie. Warps, drapeaux de progression, objets et allié de niveau100 sont des fixtures explicites. Aucun adversaire, PP ou résultat de combat n'est modifié pendant les combats. Le banc utilise un allié Eau contre l'employé pour éviter d'alimenter Torche avec un allié Feu. Les premiers réglages de fixture qui lançaient une scène de détection avant la capture ou bloquaient le pilote en sélection d'équipe ont été corrigés ; ils ne sont pas présentés comme des bugs du jeu.

La campagne de64 portes du précédent jalon n'est pas annoncée comme rejouée ici. Les425 cartes ne sont pas toutes parcourues. Pas de partie complète, d'écoute humaine ni de profilage sur une GBA physique dans ce lot. Les mesures et corrélations ne remplacent pas la validation artistique à l'écoute.

## Budget et préservation

[Bilan mesuré](BILAN_COMPILATION.json) :

- Avant :28 049 679 octets,26,75 Mio,20 OST.
- Après :**31 272 243 octets,29,823535 Mio,26 OST**.
- Ajout :3 222 315 octets de DPCM, plus les petits changements de code/alignment.
- Réserve jusqu'à30 Mio :**185 037 octets**, soit0,18 Mio.
- Réserve jusqu'à32 Mio :**2 282 189 octets**, soit2,18 Mio.
- EWRAM261052 et IWRAM29888 octets, inchangées ; un sample BGM actif à la fois, pas26 morceaux chargés en RAM.
- SHA-256 privé : `586ee6b7934b4825291934f5fcbbe1c4f9a3a1fc83a642fb9ab7a75b8e56bd58`.

La prochaine piste complète dont la récurrence est déjà établie dépasserait30 Mio : Mount Wildwood coûte environ446ko, contre185ko disponibles. Enma Track et Final Battle nécessitent toujours une boucle propre, plus d'espace que cette réserve et leurs substituts restent explicites. Ne pas remplir artificiellement les185ko par du silence, une seconde copie de boucle ou des octets inutiles pour afficher exactement30,00 Mio. Les 20 anciennes pistes, dont le montage provisoire de Blossom Heights, conservent leur état artistique précédent.

Les sept cartes modifiées ne changent que leur champ `music`. Aucun sprite, donnée d'espèce, évolution, rencontre, équipe, récompense, texte, carte géométrique ou Multi Exp. n'est modifié. Seules les sélections musicales des deux fonctions de dresseur ont changé. [Préservation](PERIMETRE_PRESERVE.json).

## Reconstruction privée

Les sources publiques compilent avec leurs replis audio natifs et ne contiennent aucun MP3, WAV, DPCM ou ROM. Pour retrouver **cette** bande-son, fournir les fichiers personnels légalement acquis ; utiliser FFmpeg7.1.5 Debian13 et les dépendances épinglées documentées dans [la procédure précédente](../POST_B13/audio/RECONSTRUCTION_PRIVEE.md). Les nouvelles empreintes WAV/MP3 sont dans les tableaux de provenance, sans désactivation des contrôles.

Les outils sélectionnent maintenant28 candidats historiques et encodent26 samples actifs ; les deux autres restent en attente. Tous les noms source attendus se trouvent dans `data/yokai/audio_candidates.json`.

```sh
python3 tools/yokai/preparer_ost_dpcm.py --extracted-manifest /chemin/prive/manifest-private.json --private-output /chemin/prive/audio30-full-sources --jobs 2
python3 tools/yokai/generer_audio_prive.py --full-source-dir /chemin/prive/audio30-full-sources --output /chemin/prive/audio30-integration --jobs 2
make -j4 YOKAI_AUDIO_DIR=/chemin/prive/audio30-integration
YOKAI_AUDIO_DIR=/chemin/prive/audio30-integration python3 tools/yokai/verifier_liaison_audio.py
```

Le dépôt contient déjà les PNG, palettes, configurations et affectations actives ; la compilation n'exige aucun nouveau dessin caché. Les sorties privées restent hors du checkout. La compilation publique et la compilation avec26 OST ont réussi ; aucun nouveau profil B13 Windows ni empreinte B13 n'est falsifié. Ce jalon musical ne constitue pas une version finale du jeu.
