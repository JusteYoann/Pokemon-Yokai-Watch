# Correction des boucles — résultat partiel explicite

Branche `audio/integration-31-ost`, reprise depuis
`23f611809e842d282ced7d4b50886d54906a2da2`. Commit d'implémentation :
`bb9799a16`. Aucune fusion. **Katies House possède maintenant une boucle mesurée
et testée dans mGBA. Enma Track et Final Battle restent sans boucle : aucune
reprise musicalement suffisamment démontrée n'a été imposée.** L'objectif des
trois boucles n'est donc pas terminé et la branche n'est pas validée comme finale.

## Points actuellement appliqués

Les positions sont des indices d'échantillons à **13 379 Hz**, depuis le début
du fichier source ; la fin est exclusive. La totalité de la portion initiale
précédant le retour est conservée et jouée une fois.

| Morceau | Retour | Fin | Durée du cycle | État |
|---|---|---|---|---|
| Enma Track, slot 5 | Aucun | Source complète : 119,014 s | Aucune | Lecture unique préservée ; boucle non résolue |
| Katies House, slot 8 | **298 726**, soit **22,327977 s** | **1 486 781**, soit **111,127962 s** | **1 188 055 échantillons**, soit **88,799985 s** | Boucle native activée et testée ; écoute humaine à valider |
| Final Battle – Are You Ready?, slot 25 | Aucun | Source complète : 202,057 s | Aucune | Lecture unique préservée ; boucle non résolue |

La portion initiale de 22,328 s de Katies House inclut l'ouverture ; elle ne
prétend pas mesurer une introduction de 22,328 s au sens d'un découpage artistique.
Le retour est choisi dans une portion stable de la reprise, plutôt qu'à zéro.
Un retour à ce point conserve une période musicale entière de 88,8 s. Le fondu
terminal et la répétition supplémentaire du fichier source ne sont pas intégrés.

## Recherche et choix musical

Les trois WAV ont été contrôlés contre leurs empreintes épinglées. La nouvelle
recherche couvre les ancres de six secondes espacées de deux secondes dans
l'ensemble des enregistrements exploitables, avec au moins seize secondes
d'écart. Les meilleures reprises sont ensuite affinées au taux natif ; des
fenêtres de deux secondes comparent le signal, le spectre et le niveau relatif
sur tout le recouvrement disponible. [Analyse reproductible](RECHERCHE.json).

Pour Katies House, plusieurs ancres distinctes retrouvent le même décalage de
88,8 s ; les correspondances s'étendent sur plusieurs dizaines de secondes,
et ne se limitent pas à un petit motif de percussion. Les phases des instruments
et certains niveaux varient entre les passages : ce n'est pas une duplication
exacte de forme d'onde. Le meilleur voisinage de raccord dans le DPCM décodé,
autour de 22,3 s, donne environ 0,84 de corrélation de forme d'onde et 0,95 de
similarité spectrale sur deux secondes. Le point final est aligné à moins de
50 ms de cette ancre, en conservant **exactement le même décalage de 1 188 055
échantillons**.

Au point retenu, le saut PCM8 est nul, la différence des pentes adjacentes est
nulle et l'écart des niveaux RMS des fenêtres précédentes de 20 ms est d'environ
0,10 dB. Aucun fondu croisé, changement de tempo ou réencodage : seuls l'en-tête
WaveData et la longueur conservée changent. Ces mesures et le contexte répété
motivent la boucle expérimentale ; ils ne constituent pas une écoute humaine.

Pour Enma Track, la meilleure correspondance de six secondes de cette recherche
est d'environ 0,566. Des motifs tardifs reviennent vers 84 s et 110,668 s,
mais la comparaison des autres phrases et des niveaux ne démontre pas un cycle
complet. Boucler arbitrairement cette fin ferait surtout répéter une petite
portion tardive après une longue partie jouée une seule fois. **Pas d'activation.**

Pour Final Battle, des ressemblances locales apparaissent autour de 30–40 s et
180–190 s. Plusieurs décalages concurrents, notamment 150,4 s et 153,6 s, retrouvent
des motifs proches. Le maximum de six secondes atteint environ 0,687 ; le meilleur
voisinage spectral est plus convaincant mais reste court et proche de la fin du
morceau. Cela ne permet pas de choisir automatiquement un cycle complet plutôt
qu'une reprise partielle de motif. **Pas d'activation sans écoute.**

## Tests réellement effectués

| Vérification | Résultat |
|---|---|
| Katies House dans mGBA | **Cinq retours natifs de boucle** ; intro non répétée, cinq raccords du mélangeur comparés au DPCM attendu, corrélation minimale **0,9778** ; [rapport](boucle-katie/TEST_MGBA.json) |
| Bruitage, cri et Flash pendant Katie | Appels natifs SE/cri, fin du cri, sauvegarde Flash native réussie ; même rapport |
| Les trois morceaux | Extraits audio mGBA comparés aux références avant/après SE/cri ; [rapport](lecture/TEST_MGBA.json) |
| Enma | Dialogue original au Mont Braise, thème 5, refus et retour à l'exploration vérifiés ; [rapport événements](evenements/TEST_MGBA.json) |
| Matt prolongé | **30 000 frames, environ 8 min 22 s**, au véritable menu de choix d'action, après apparition des combattants ; aucune action pendant l'attente |
| Résultat musical du test prolongé | **Échec de l'objectif de continuité pour Final Battle** : échantillon terminé, sortie audio finale silencieuse, RMS alternatif mesuré **0** ; champ `requested_continuous_music_goal_met: false` dans le rapport |
| Suite du combat Matt | Reprise du pilotage aux boutons, victoire réelle et thème 26 de conclusion ; aucun résultat forcé |
| Préservation des morceaux | **30 autres échantillons liés identiques octet pour octet**, dont les 26 originaux et les boucles 13/14 ; [preuve](PRESERVATION_30_SAMPLES.json) |
| Liaison et limites | 31 références, en-têtes et empreintes conformes, budget respecté ; [liaison](LIAISON.json) |
| Public et autres ressources | ROM publique inchangée ; seules les données musicales autorisées et leurs relocalisations diffèrent de la référence privée ; [mesures](MESURES.json) |

Le statut `passed` des scripts indique que les vérifications et scénarios
annoncés ont été exécutés comme prévu ; il ne transforme pas le défaut musical
constaté chez Matt en réussite. Ce défaut figure séparément dans le rapport.

Les tests démarrent par une nouvelle partie aux boutons puis utilisent des
fixtures explicites de progression, warp et allié renforcé pour le combat.
L'attente prolongée a été vérifiée au menu natif d'action, avec les deux Yo-kai
affichés, puis la victoire a été jouée au contrôleur. Le premier essai d'attente
restait sur le texte d'entrée du combat ; il a été remplacé par ce test au menu.
Les captures ont été examinées. Pas de partie complète, de test matériel GBA,
de nouvelle écoute humaine ni de reprise intégrale des 28 anciens cycles.

## Taille et intégrité

| Mesure | Avant correction | Après correction |
|---|---:|---:|
| Taille du fichier ROM privé | 31 589 579 octets | **31 589 579 octets** |
| DPCM de Katies House | 978 565 octets | **766 639 octets** |
| Section privée dans le remplissage | 4 334 472 octets | **4 122 544 octets** |
| Remplissage encore libre avant `0x08D00000` | 1 729 948 octets | **1 941 876 octets** |
| Marge avant la limite de 32 Mio | 1 964 853 octets | **1 964 853 octets** |

La différence de remplissage est de 211 928 octets avec l'alignement, contre
211 926 octets dans le DPCM lui-même. Le fichier ROM ne rétrécit pas : les
graphismes restent à leur adresse fixe et la fin de ROM reste identique.
L'assertion de non-chevauchement reste active. Aucun nouveau besoin RAM.

ROM privée `pokefirered_audio.gba`, SHA-256 :
`0d8234bbd5893ef63cfb8caa1d6aa83c34b537e151b0449e848a900ffd86961b`.

ROM publique, SHA-256 toujours inchangé :
`a00527774542439e1ab0976a45421911c8b067d8bd11730de183c453581b3b3c`.
Les mêmes fichiers publics compilés sont conservés et vérifiés ; aucune nouvelle
compilation publique complète n'était nécessaire pour ces seuls changements de
configuration privée et de tests. Aucun script, dialogue, équipe, sprite,
évolution, effet sonore ou affectation des autres OST n'a changé.

## Validation à l'écoute des deux morceaux non résolus

Des extraits A/B ont réellement été générés dans le dossier privé
`/workspace/private-audio/audio31-loop-research/ecoute/`, hors Git. Les extraits
sont calculés depuis le DPCM original : **ce ne sont pas des captures mGBA**.
Les cinq extraits natifs des raccords de Katie, eux, proviennent du test mGBA et
restent également privés. Aucun WAV, MP3, DPCM ou ROM n'est publié sur GitHub.

Les [propositions d'écoute](PROPOSITIONS_ECOUTE.json) pour 5 et 25 sont des
**hypothèses rejetées pour l'activation automatique**, pas des points approuvés :

- Enma : contexte de 84 s, comparé à environ 110,668 s ; il faut notamment juger
  si répéter cette portion tardive est musicalement acceptable ou trop restrictif.
- Final Battle : contexte de 33 s, comparé à environ 183,400 s ; il faut notamment
  juger la fin de phrase, le retour harmonique et la différence d'orchestration.

Pour reproduire ces extraits sur son ordinateur, depuis WSL avec ses cinq DPCM
complets déjà préparés par la procédure précédente :

```sh
python3 tools/yokai/previsualiser_raccord_audio31.py \
  --number 5 --full-dpcm-dir /chemin/prive/cinq-complets \
  --loop-start 1123830 --loop-end 1480619 \
  --private-output /chemin/prive/ecoute-boucles

python3 tools/yokai/previsualiser_raccord_audio31.py \
  --number 25 --full-dpcm-dir /chemin/prive/cinq-complets \
  --loop-start 441507 --loop-end 2453709 \
  --private-output /chemin/prive/ecoute-boucles
```

Le générateur contrôle les empreintes, produit un fichier A avec la continuation
originale, un B avec la tentative de raccord et un C avec le contexte du retour.
Dans B, écouter les raccords à **4, 12 et 20 secondes** : l'extrait de huit secondes
est répété trois fois pour comparer ; les séparations à 8 et 16 secondes ne sont
pas les retours d'une boucle musicale entière. Il n'y a ni fondu masquant un
défaut, ni normalisation modifiant les niveaux, ni activation dans la ROM.

Écouter au casque puis sur les haut-parleurs utilisés pour le jeu ; comparer A/B
à volume égal et juger séparément rythme, harmonie, mélodie, orchestration,
rupture de niveau, blanc et clic. Si ces deux propositions ne conviennent pas,
il faudra placer manuellement des marqueurs de phrases dans un éditeur audio,
ou retrouver une source comportant une reprise complète ou des marqueurs fiables.
Un fondu seul ne suffit pas à valider une phrase musicalement incorrecte.
Après un choix à l'écoute, appliquer les indices retenus et refaire plusieurs
cycles mGBA, dont le combat prolongé de Matt. Jusqu'à cette étape, les deux
originaux restent complets, inchangés, avec leur limite de lecture unique.

## Reprise et reconstruction

La [procédure privée du jalon précédent](../README.md#reconstruction-privée-notamment-sous-windowswsl)
reste applicable : mêmes fichiers personnels et mêmes outils, nouvelle
configuration de Katie. Aucun ajout audio n'est requis pour cette correction.
Le générateur conserve les 26 fichiers épinglés et contrôle les cinq originaux.

La recherche peut être répétée sans compiler la ROM :

```sh
python3 tools/yokai/rechercher_boucles_audio31.py \
  --private-sources /chemin/prive/wav-complets \
  --report /chemin/prive/recherche-boucles.json
```

Le travail restant est **musical**, pour les slots 5 et 25, puis la validation
perceptive de Katie. Aucun point non validé n'est dissimulé derrière une boucle
de silence ou un redémarrage à zéro. Ne pas fusionner comme une correction des
trois morceaux terminée.
