# Pourquoi le premier arrangement ne convenait pas

Le retour du créateur est retenu : le premier rendu n’est pas une adaptation artistique acceptable. Les validations précédentes établissaient qu’une séquence pouvait jouer dans le moteur, pas que la musique était fidèlement transcrite. Il ne fallait pas traiter cette preuve technique comme une validation musicale.

## Défauts confirmés de la méthode de production

1. **La partition de référence n’existait pas.** Basic Pitch estimait des notes dans un mix polyphonique. Les probabilités du modèle ont ensuite servi à sélectionner une mélodie et une basse, sans vérification auditive note par note. Une harmonique, une note d’accompagnement et une mélodie peuvent être confondues. Aucune de ces estimations n’avait été authentifiée par une partition ou un musicien.
2. **Une grande part des événements était recomposée.** Sur les 1 118 notes de A1, 288 arpèges provenaient d’accords major/minor/sus inférés, 144 coups de batterie et 288 charlestons provenaient d’un motif imposé. Ces 720 événements n’étaient pas une transcription des parties originales. Même une bonne fréquence moyenne de notes ne permet pas de retrouver le motif reconnaissable du morceau.
3. **Les filtres et la quantification altéraient les phrases.** La sélection de registre a d’abord omis des passages graves. La quantification à la double croche peut déplacer une attaque d’environ 65 ms ; la fusion des notes répétées et la continuité imposée par le modèle peuvent supprimer des articulations ou tenir une mauvaise note. Les dernières corrections de registre ne certifiaient pas les phrases restantes.
4. **Les timbres et l’équilibre n’étaient pas validés.** Accordéon, guitare et basse PSG étaient des choix de compatibilité moteur. Ils ne prouvaient pas que les instruments ou leurs rôles correspondaient au disque. Des queues de notes consomment aussi des voix : cinq pistes ne signifient pas cinq voix PCM ni absence de vol de voix.
5. **La boucle était validée mécaniquement seulement.** Une similarité de chroma, des GOTO et un nombre de ticks cohérent ne déterminent ni le premier temps ni un raccord musical naturel. La première démonstration conservait cette incertitude.

## Ce qui est reproduit, et ce qui ne l’est pas

A1 a été rejoué dans une copie privée de la ROM, sur une carte native, pendant cinq retours complets. La musique de la zone revient en descendant du vélo. Le test ne détecte pas de saturation numérique, d’arrêt du lecteur musical. Cela ne contredit pas les défauts audibles signalés : les notes, les timbres et les articulations peuvent être mauvais tout en formant un programme M4A valide.

Les contrôles ne permettent pas d’identifier avec certitude un unique « bug audio » expliquant le ressenti. En particulier, un vol de queue de note ou un mauvais timbre n’est pas exclu par un compteur de voix sous le plafond. Le mauvais résultat s’explique déjà par les limites avérées de la reconstruction musicale.

## Version A2 réellement produite

A2 retire la grille d’accords inventés et le motif complet de charleston/batterie. Sa mélodie, sa basse, sa voix secondaire et ses accents s’appuient sur les activations et attaques observées ; les estimations faibles restent filtrées. Les pénalités de continuité et les rejets d’harmoniques ont été revus pour préserver davantage d’attaques. La flûte remplace le premier timbre de mélodie et l’équilibre est recentré sur cette ligne. Le candidat d’entrée dans la section principale est commun à la méthode B.

Une copie expérimentale de la banque 141 réduit les coefficients de release de la guitare 24 et de la flûte 73 à 96. Les ondes natives sont réutilisées ; les autres musiques du jeu ne reçoivent pas cette banque. Cette mesure réduit certaines queues sans garantir une réserve de voix : le maximum observé reste de cinq voix PCM. Le coût est **2 288 octets de séquence et 1 536 octets de banque copiée**, soit **3 824 octets**, sans nouvelle onde audio.

La version A2 passe les mêmes tests de cinq boucles et de descente du vélo, puis un test supplémentaire avec le véritable bouton SELECT et le vélo enregistré. Elle est fournie pour comparaison, **pas comme reproduction fidèle certifiée**. Les estimations de hauteur et d’instrument restent susceptibles d’être fausses ; les accents issus du modèle ne sont pas une transcription fiable de batterie.

## Peut-on améliorer significativement A ?

Le moteur GBA ne l’interdit pas : les musiques natives montrent qu’un arrangement élaboré peut fonctionner avec ce nombre de pistes. Une amélioration importante passe par une transcription vérifiée à l’oreille ou depuis une partition/MIDI autorisé, un travail de voicing et d’instrumentation, puis une revue du raccord. La reconstruction automatique actuelle ne suffit pas à garantir une identité immédiatement reconnaissable.

**Recommandation pour A : ne pas lancer la conversion en série à partir de ce modèle.** A2 permet de comparer une révision technique, mais n’est pas une preuve de qualité pour les 21 autres titres. Aucune nouvelle écoute perceptive ou correction humaine des notes par l’agent n’est revendiquée.
