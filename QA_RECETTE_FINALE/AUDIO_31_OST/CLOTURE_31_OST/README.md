# Clôture des vérifications audio — réserve Enma et propositions de mixage

Branche **`audio/integration-31-ost`**, référence audio
`c86f86ae0d4ae1eb4d6cc68c87b176714647fe92`. Aucun merge.

**31 OST sont intégrées et lisibles ; 30 possèdent une boucle native. Les quatre
nouvelles boucles et les transitions testées fonctionnent. Enma Track reste en
lecture unique et s'arrête lors d'un dialogue prolongé : cette réserve empêche
de déclarer l'intégration entièrement terminée.** Les vérifications de cette
phase sont closes ; aucun autre chantier n'est commencé.

Les cinq nouveaux morceaux sont aussi nettement plus faibles que le groupe
initial. Leur cause et des corrections ciblées sont documentées ci-dessous,
**sans changement de gain**, conformément à la demande d'approbation préalable.
Les trois morceaux réservés restent disponibles sans nouvelles affectations.

## 1. Enma Track : recherche terminée, pas de boucle forcée

[Source vérifiée](ENMA_SOURCE.json) et [nouvelle recherche](ENMA_RECHERCHE.json).
Le manifeste privé disponible contient une seule source correspondante, de
119,014 s. Les empreintes MP3/WAV/DPCM sont contrôlées. Les tags inspectés ne
contiennent pas de marqueurs fiables de boucle.

La recherche couvre des fenêtres de signal de six secondes sur l'enregistrement,
puis des comparaisons spectrales de hauteur sur huit et seize secondes. Les
meilleures correspondances de signal restent locales : environ 84 s et 110,668 s,
corrélation 0,566. Une ressemblance tardive de période voisine de 20 s atteint
0,882 sur huit secondes mais 0,829 sur seize secondes. Ces valeurs ne sont pas
des pourcentages de qualité et ne démontrent pas une reprise de phrase complète.
Répéter cette seule fin après une très longue partie jouée une fois serait un
choix d'arrangement, pas une boucle naturelle suffisamment établie.

**Aucun point n'est activé ni inventé.** Le fichier complet original reste
identique, avec son introduction. Il n'est remplacé par aucune autre OST.

[Test réel du dialogue prolongé](enma-prolonge/TEST_MGBA.json) : nouvelle partie,
progression et warp explicites, interaction originale avec Enma au Mont Braise,
puis attente de **9 000 frames, environ 150,68 s**, texte laissé ouvert. À la fin,
le canal du sample a terminé et le RMS alternatif de sortie vaut zéro : silence
confirmé. Le test marque `requested_continuous_music_goal_met: false`.
Le refus aux boutons restaure ensuite normalement le thème de la carte.
La capture du dialogue a été ouverte et examinée.

### Secours proposé — approbation requise, non appliqué et non testé comme solution

**Relancer le même enregistrement intégral à sa fin naturelle**, seulement si
le dialogue d'Enma est encore actif et si le thème demandé reste le slot 5,
avec une courte remontée de volume native à la relance, proposée autour de
0,5 s. Déclencher la reprise sur la fin réelle du canal, pas sur un minuteur
de 119 s : une fanfare ou une pause ne doit pas provoquer un redémarrage anticipé.
Quitter le dialogue ou passer au combat annulerait ce mécanisme.

Ce secours conserve le fichier, ne supprime rien, ne remplace pas l'OST et ne
nécessite pas de modifier les dialogues. Il évite le **silence indéfini** mais
répète l'introduction à chaque lecture et ne promet pas une transition musicale
transparente : le fondu terminal déjà contenu dans la source reste perceptible.
Ce changement d'écoute exige donc **l'accord explicite de l'utilisateur**.
Il n'est pas activé, et aucun succès mGBA n'est revendiqué pour ce mécanisme.
Toute réalisation devra rester conditionnelle à la compilation privée pour
préserver le binaire public.

L'autre voie est une validation humaine de marqueurs dans une source musicale
appropriée. Aucun nouvel enregistrement n'est téléchargé ou inventé ici.

## 2. Quatre nouvelles boucles revérifiées

[Rapport mGBA et sorties aux raccords](boucles/TEST_MGBA.json).

| OST | Retour → fin exclusive, échantillons natifs à 13 379 Hz | Retours testés | Corrélation minimale de l'audio au raccord |
|---|---|---:|---:|
| Katies House | 298726 → 1486781 | 5 | 0,9778 |
| Enma Villa | 13389 → 1332961 | 5 | 0,9857 |
| Mount Wildwood in the Past | 53515 → 879198 | 6 | 0,9773 |
| Final Battle, variante C | **462424 → 2474626** | 5 | 0,9564 |

Les points sont inchangés. Les introductions sont conservées une fois ; les
retours natifs ne repartent pas à zéro. Les sorties mGBA capturées aux retours
correspondent aux échantillons attendus, sans arrêt de lecture constaté.
Les appels natifs SE/cri et la sauvegarde Flash des fixtures isolées passent.
Il ne s'agit pas d'une écoute humaine démontrant l'absence de tout clic perceptible.

Final Battle conserve exactement **34,5634202855 → 184,9634501831 s**, cycle de
**150,4000298976 s**, conformément à la variante C choisie.

[Matt prolongé](evenements/TEST_MGBA.json) : cinq retours dans le véritable combat,
maintenu au menu d'action pendant **46 029 frames, 12 min 50,65 s**. Canal et
en-tête contrôlés à chaque frame, aucune interruption détectée. Puis victoire
jouée aux boutons, thème de victoire 22 et conclusion 26 observés. L'allié
renforcé, la progression et le warp sont des fixtures explicites ; les équipes
adverses et les résultats ne sont pas modifiés pendant le combat.

## 3. Niveaux des 31 OST : écart identifié, aucun gain appliqué

**[Tableau complet des 31 morceaux](VOLUMES_31.md)** · [CSV](VOLUMES_31.csv) ·
[mesures natives et pics](VOLUMES_31_MGBA.json).

Les 31 mesures proviennent du mélangeur réel mGBA, sur l'introduction et un cycle
complets, ou l'enregistrement entier pour Enma, plus 30 frames de marge.
L'analyse EBU R128 rejette le continu à 20 Hz uniquement pour la mesure.
Pas d'effets simultanés, de normalisation ni de changement de volume.

| Groupe / morceau | LUFS intégrés | Proposition indicative, non appliquée |
|---|---:|---|
| 26 morceaux initiaux | **−29,2 à −28,9** | Conserver leurs gains |
| Enma Track | **−43,8** | +14,8 dB ; Q8 77 → 423 |
| Katies House | **−38,7** | +9,7 dB ; Q8 109 → 333 |
| Enma Villa | **−38,3** | +9,3 dB ; Q8 108 → 315 |
| Mount Wildwood in the Past | **−38,5** | +9,5 dB ; Q8 101 → 302 |
| Final Battle | **−41,8** | +12,8 dB ; Q8 64 → 279 |

**Cause identifiable :** `data/yokai/mixer_calibration.json` conserve pour ces
cinq slots `private_sample: false`, les mesures de leurs anciens replis et des
gains atténuateurs correspondants. Le moteur applique maintenant ces mêmes gains
aux véritables samples privés. Les valeurs conservées expliquent leur faiblesse.

Les propositions utilisent la cible historique −29 LUFS comme point de départ,
pas comme autorisation de normaliser les 31 morceaux. Le calcul suppose un gain
linéaire ; les arrondis et le mixeur devront être remesurés après accord. Les
pics projetés des cinq corrections restent entre −15,9 et −14,4 dBFS, mais cela
ne remplace ni une nouvelle mesure ni l'écoute. [Propositions détaillées](GAINS_PROPOSES.json)
et [CSV](GAINS_PROPOSES.csv). **Approbation requise pour toute application.**
Ces futurs gains devront être des réglages privés conditionnels : modifier
directement le tableau commun pourrait changer le binaire public. La table
commune et les cinq valeurs actuelles sont conservées dans cette phase.

Aucun écrêtage numérique sur les 31 captures ; pic vrai maximal **−11,4 dBFS**.
Le silence constaté chez Enma vient de la fin du sample, pas d'une saturation.
L'absence d'écrêtage du mixeur ne garantit pas l'absence de défauts déjà contenus
dans les sources compressées ou d'une gêne subjective.

Les [écarts de transitions](ECARTS_TRANSITIONS.json) calculés sur les niveaux
intégrés signalent notamment une baisse d'environ 14,6 LU à l'entrée du dialogue
Enma et une hausse de 12,7 LU entre Final Battle et victoire/conclusion.
Ce sont des différences globales de morceaux, **pas des mesures instantanées
des sauts perçus à ces instants**. Elles motivent l'écoute et les propositions.

Un [parcours exploration → combat sauvage → victoire → exploration](transition/TEST_MGBA.json)
a réellement été joué : fenêtres d'exploration et combat autour de −29,8/−29,9 LUFS,
segment victoire/retour −27,8 LUFS avec effets, puis reprise −30,8 LUFS sur une
autre fenêtre. Aucun écrêtage dans ces captures. Le retour de l'ambiance et le
Multi Exp. permanent ont été vérifiés pendant cette victoire ; aucun réglage
de mixage n'en est déduit automatiquement.

## 4. Ensemble des contrôles finaux

| Contrôle | Résultat et portée |
|---|---|
| Présence des 31 OST | 31 pointeurs et vagues privés contrôlés ; [liaison](LIAISON.json) |
| Lecture des 31 | Audio mGBA comparé au DPCM avant/après SE et cri ; [rapport](lecture/TEST_MGBA.json) |
| Affectations | 104 BGM, 425 en-têtes compilés de cartes et 273 pointeurs SE/fanfares ; [rapport](routage/ROUTAGE_MGBA.json) |
| Quatre nouvelles boucles | 21 retours natifs au total, introductions conservées, raccords comparés ; rapport boucles |
| Matt | Plus de dix minutes, cinq cycles, victoire 22 puis conclusion 26 ; rapport événements |
| Enma | Dialogue original, essai prolongé confirmant la limite, refus et retour à la carte ; rapport Enma |
| Fanfares | **45 cas** : 14 fanfares sur Patrol Mission puis réception d'objet sur chacun des 31 morceaux ; pause/reprise au curseur sans redémarrage ; [rapport](FANFARES_MGBA.json) |
| Bruitages et cris | Pointeurs natifs conservés, appels SE/cri pendant les lectures et les nouvelles boucles, cris terminés ; pas une écoute des 273 effets |
| Exploration/combat | Combat sauvage joué et gagné, ambiance restaurée, réception EXP du partenaire au repos ; rapport transition |
| Contrôle des compilations | `make -j6` privé et public : binaires à jour réutilisés, sans recompilation inutile ; empreintes et limites contrôlées |
| Public | ROM strictement identique à la référence publique |
| Jeu et autres ressources | ROM privée entière identique au commit audio de référence ; scripts, sprites, cartes, équipes, statistiques, évolutions, dialogues et gains préservés ; [preuve](PRESERVATION.json) |

Les mentions `passed` signifient que les contrôles annoncés ont été exécutés
comme prévu. Elles ne transforment pas la limite connue d'Enma en réussite : son
objectif de lecture continue est séparément marqué faux dans le rapport.

Les tests utilisent une vraie initialisation de nouvelle partie, puis des
fixtures explicites de carte/progression/alliés. Ils ne constituent pas une partie
complète ni une traversée des 425 cartes. Pas de test matériel GBA, pas de nouvel
environnement propre ni de compilation depuis un nouveau clone pour cette phase.
**Aucune écoute humaine n'est revendiquée.** Les anciens cycles des 26 morceaux
ne sont pas tous rejoués cinq fois : une lecture complète a été mesurée pour
chacun, et les quatre nouvelles boucles ont reçu les essais répétés spécifiques.

## 5. Taille, empreintes et préservation

ROM privée : **31 589 579 octets**, environ **30,13 Mio**. Limite de 32 Mio
respectée ; marge en fin de ROM **1 964 853 octets**. Remplissage disponible
avant les graphismes : **2 059 785 octets**. L'assertion de non-chevauchement
reste active. Aucune ressource n'est supprimée.

SHA-256 privé inchangé :
`0e7ff7f6096e5b52932e1e1cf090eaee3c53ee7ebe182ebbd5302feee2a2bfce`.

ROM publique : **16 777 216 octets**, SHA-256 inchangé :
`a00527774542439e1ab0976a45421911c8b067d8bd11730de183c453581b3b3c`.

Aucun fichier audio protégé ni ROM n'est publié sur GitHub. Les WAV de transition
et de raccord restent privés ; les mesures de niveaux sont transmises en flux
à FFmpeg sans conserver de copies publiques. Les seuls changements du dépôt sont
les rapports et les outils de vérification de ce chantier.

## 6. Classement des éléments restants

### Bloquant pour une clôture audio sans réserve

- **Enma après une lecture complète :** silence possible si le dialogue reste
  ouvert. La boucle naturelle n'est pas démontrée et le secours proposé attend
  l'accord de l'utilisateur. Cela ne bloque pas le jeu ni les autres scènes,
  mais empêche de promettre une ambiance continue pour ce dialogue.

### Non bloquant pour le fonctionnement du moteur, à valider

- **Mixage : priorité élevée.** Cinq morceaux sont trop faibles relativement
  aux 26 initiaux ; les propositions ciblées attendent l'autorisation demandée.
  Pas de saturation ou de panne de lecture détectée.
- **Écoute des nouvelles boucles et transitions**, notamment le maintien des
  notes de Final Battle C : qualité artistique définitive non validée par les
  seuls tests numériques. Les points approuvés restent inchangés.
- **Appréciation perceptive des pics et variations internes**, y compris les
  passages dynamiques conservés des anciens morceaux. Aucune correction globale
  automatique n'est justifiée ou appliquée.

La phase de vérification est terminée avec ces réserves documentées. **Arrêt du
travail audio ici, sans fusion ni ouverture d'un autre chantier, en attente des
prochaines instructions.**
