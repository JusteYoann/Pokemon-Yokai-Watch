# Audit musical — analyse du corpus reçu et sélection à valider

Le développement est sécurisé par le commit local **`145044ec29f4ad7ee03c1942e8a925d15a9f89e1`** sur `qa/recette-finale`. L’audit se trouve sur **`audio/direction-musicale-audit`**, créée depuis ce point. Aucun merge, push ou PR n’est réalisé. La recette du jeu reste **NON PRÊT** : l’audit musical ne remplace pas les vérifications de parcours encore ouvertes.

## Résultat

- **14 lots RAR extraits**, couvrant les sept jeux. Les envois fractionnés ont résolu les refus initiaux de transfert ; les nouveaux lots sont autonomes.
- **80 MP3 décodés et analysés intégralement**, soit **3 h 33 min 40 s** : YW1(8), YW2(21), YW3(18), YW4(8), Blasters(12), Sangokushi(11), Busters2(2).
- **91 slots musicaux**,425 cartes,711 références littérales et263 sites d’appels audio statiques/dynamiques relevés ;20 équipes de caméos reliées à leurs14 objets de carte et à leurs musiques actuelles.
- **22 références présélectionnées**,58 non retenues comme choix principal,132 lignes de propositions/fallbacks/contextes et des fiches comparatives.
- **Aucun arrangement, MIDI transcrit, MP3 intégré, sample nouveau ou changement du jeu.** La ROM conserve son SHA QA.

**Limite essentielle : aucune écoute perceptive n’est revendiquée.** Les outils ont réellement extrait et décodé tout le signal, mesuré durées, dynamique, spectres, pulsations et répétitions, et produit des diagrammes inspectables. Cela ne certifie ni l’émotion, ni les instruments, ni la présence de voix, ni les meilleurs raccords musicaux. Tous les choix Yo-kai restent **`A_VALIDER`**.

## Présentation de la proposition

1. [Les 22 premiers choix, en une table](CHOIX_PRINCIPAUX.md).
2. [Proposition détaillée par contexte et fallback](PROPOSITION_BANDE_SON.csv).
3. [Cohérence de l’aventure et limites de direction](ANALYSE_COHERENCE.md).
4. [Comparaisons de vrais candidats par contexte](FICHES_COMPARAISON.csv).
5. [Les 58 pistes non retenues et alternatives](MUSIQUES_ECARTEES.csv).

Conserver le socle Pokémon fréquent : titre, début, soins, combats ordinaires, victoires et Champion. Les accents Yo-kai concernent notamment les maisons Nathan/Katie, le vélo, Céladopole, le Manoir, la Sylphe occupée, certains lieux Sevii et les caméos/boss. Les deux concepts natifs pour Matt et le Conseil4 sont des projets de comparaison, pas des arrangements annoncés comme créés.

**Pas de quota par archive.** Busters2 est analysé mais n’a aucun choix principal : Basecamp3 est proposé comme premier prototype de comparaison au Canyon, tandis que la version Busters2 reste une alternative. Un titre célèbre ou un nom de personnage ne garantit pas une bonne affectation.

## Inventaires et preuves

- [Archives, jeux, nombres de pistes et hashes](ARCHIVES_ET_ACCES.csv).
- [Inventaire des 80 MP3](INVENTAIRE_OST.csv), avec chemins internes et noms d’origine conservés ; [application du lexique fourni](LEXIQUE_ET_CONTEXTES.csv).
- [Emplacements moteur](EMPLACEMENTS_MUSICAUX_KANTO.csv), [musique des 425 cartes](MUSIQUES_PAR_CARTE.csv), [références littérales](DECLENCHEURS_AUDIO.csv), [appels paramétrés](APPELS_AUDIO_STATIQUES_ET_DYNAMIQUES.csv), [caméos et cartes réelles](CAMEOS_AUDIO.csv).
- [Analyse numérique détaillée et enveloppes](preuves/ANALYSE_AUDIO.json), [synthèse chiffrée](preuves/SYNTHESE_PHASE1.json).
- [Pré-évaluation GBA](FAISABILITE_GBA.md), [sécurisation du développement](SECURISATION.md), [préservation et contrôles](preuves/PRESERVATION_ET_VALIDATION.json).
- [Cahier des charges fourni, lu intégralement](source-data/DIRECTION_MUSICALE_POKEMON_YOKAI_WATCH_CODEX.md).

Les 80 diagrammes de signal sont dans `preuves/<id>.png`, avec le même identifiant stable que le CSV. Par exemple : [Vélo](preuves/YW1-6b2ae63e.png), [Nocturne Hospital](preuves/YW1-3fb46a59.png), [Enma Track](preuves/BL-50568e39.png), [Soruka](preuves/SG-634d3b4c.png).

`CONSERVER` décrit le comportement natif, notamment les usages non ciblés d’un slot partagé. `A_VALIDER` décrit un choix proposé. `REMPLACER` n’est jamais présenté comme une décision définitive avant l’accord du créateur. Certains choix sont locaux : changer globalement `MUS_PALLET`, `MUS_SEVII_ROUTE` ou `MUS_VS_TRAINER` modifierait des lieux et combats non visés.

## Corpus et limites

L’inventaire porte sur les 14 lots effectivement reçus et accessibles. Il ne prétend pas que chaque OST commerciale est exhaustive, ni que les nouveaux lots reproduisent bit à bit les premières archives trop grosses, dont le contenu n’a pas été transféré. Les numéros manquants ne deviennent pas des pistes inventées. Les suffixes `(1)`, `(4)`, `Reused`, `X` et le numéro `28.5` sont conservés et ne prouvent pas une variante ou une provenance compositionnelle.

Aucun doublon de fichier ou de PCM mono11025 Hz exact n’est retrouvé. Les reprises, variantes de mix, transpositions et arrangements d’une même composition restent à vérifier : deux titres proches ne suffisent pas à conclure.

Les mesures utilisent une copie mono11025 Hz du MP3, sans modifier le fichier original. Elles ne décrivent donc pas toute la spatialisation ni les hautes fréquences. BPM a une ambiguïté demi/double ; RMS n’est pas LUFS ; centroïde n’est pas identification d’instrument ; similitude de chroma n’est pas frontière de boucle. Les limites figurent dans chaque ligne d’inventaire.

## Reproduire

Les références restent hors Git, sous `/workspace/attachments/` et `/workspace/scratch/music-analysis/extracted/`. Les preuves versionnées contiennent des métadonnées, valeurs et graphiques, aucun MP3, extrait audio, ROM ou MIDI dérivé.

```sh
cd /workspace/Pokemon-Yokai-Watch
. /workspace/.setup/env.sh
export PYTHONPATH=/workspace/.setup/music-python
export MPLCONFIGDIR=/workspace/.setup/music-cache
export XDG_CACHE_HOME=/workspace/.setup/font-cache
export OPENBLAS_NUM_THREADS=1
export NUMBA_NUM_THREADS=1
python3 docs/musique-audit/scripts/extract_rar.py
python3 docs/musique-audit/scripts/analyse_audio.py
python3 docs/musique-audit/scripts/inventorier_jeu.py
python3 docs/musique-audit/scripts/preparer_proposition.py
python3 docs/musique-audit/scripts/lexique_contextes.py
python3 docs/musique-audit/scripts/verifier_audit.py
```

Les chemins du script d’extraction sont ceux des pièces jointes de cette session ; ajuster ses entrées si les fichiers sont récupérés ailleurs. Les chemins internes et SHA256 permettent de retrouver les bons fichiers. L’analyse ne recalcule que les références dont le contenu a changé. Les scripts sont des outils d’audit, pas un pipeline d’intégration dans la ROM.

FFmpeg, ffprobe, libarchive, librosa, NumPy, SciPy, SoundFile et Matplotlib ont été réellement utilisés ; versions dans `preuves/OUTILS.json`. Les consignes d’environnement sont sauvegardées en **brouillon** : les revoir/enregistrer dans les paramètres puis publier l’environnement si leur réutilisation est souhaitée. Cette publication est distincte de GitHub ; aucune restauration sur une autre machine n’est certifiée.

## Validation attendue

Consulter les choix, écouter les candidats et amender les affectations. **Après validation explicite seulement**, sélectionner un prototype GBA, examiner sa transcription, sa banque, ses boucles et son coût, puis tester le rendu. Aucun arrangement de masse ou remplacement définitif n’est commencé ici. Les autorisations sur les compositions restent à vérifier avant une diffusion publique ; les MP3 de référence ne sont pas publiés.
