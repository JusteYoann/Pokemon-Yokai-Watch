# Pré-évaluation de faisabilité GBA — aucun arrangement réalisé

## État réellement inspecté

Le projet utilise le moteur m4a, ses séquences MPlay/Sappy, les banques `sound/voice_groups.inc`, les échantillons et la table `sound/song_table.inc`. Les séquences issues de MIDI sont générées par `tools/mid2agb`, selon le Makefile et `sound/songs/midi/midi.cfg`. Les MP3 n’ont pas été intégrés, convertis en MIDI, transformés en pistes de la ROM ni découpés en samples livrables.

La table liée contient347 entrées, dont les 91 identifiants musicaux de256 à 346 ; le reste inclut sons et entrée muette, pas347 musiques. Les 425 en-têtes de carte et711 références littérales ont été inventoriés. Le relevé complémentaire contient263 sites d’appels audio statiques/dynamiques : un appel paramétré n’est pas toujours une affectation spécifique et un appel déclaré ne prouve pas une exécution.

## Limites effectives du moteur actuel

| Élément | Observation de source | Conséquence |
|---|---|---|
|Pistes BGM|10 dans `sound/music_player_table.inc`|10 canaux séquencés ne garantissent pas10 voix PCM simultanées|
|Mixage DirectSound configuré|5 dans `src/m4a.c:m4aSoundInit`|Concurrence entre musique, cris et effets ; prévoir des arrangements parcimonieux|
|Maximum structurel|`MAX_DIRECTSOUND_CHANNELS=12`|Ce maximum de structure ne signifie pas que12 sont actifs ; ne pas augmenter sans profilage|
|Fréquence du mixeur|`SOUND_MODE_FREQ_13379`|Environ13,379kHz pour le mixeur ; ce n’est pas l’obligation que tous les samples aient cette fréquence|
|PSG/CGB|Extension `MPlayExtender(gCgbChans)`|Ondes carrées, onde programmable et bruit peuvent compléter le PCM ; timbres et priorité à tester|
|Jingles|`src/sound.c:sFanfares`, compteur de durée, pause/reprise BGM|Remplacer un jingle par un MP3 long casserait potentiellement l’attente et le rythme même si le son se lance|
|Reprise et effets|FadeIn/Out, PlayCry et ducking natifs|Tester les automations, cris, transition combat et retour carte ; pas seulement la lecture isolée|

Objectif indicatif pour un futur premier arrangement : trois voix PCM musicales soutenues, quelques parties PSG, puis évaluer les crêtes et SFX. Ce n’est pas une limite absolue ni une qualité garantie ; des drums et notes longues peuvent consommer plusieurs voix. Une éventuelle hausse du mixeur serait une décision technique séparée, jamais une simple activation du nombre12.

## ROM, RAM et coût du mauvais raccourci

Le build QA inchangé occupe **15480620 octets utiles** dans une capacité cible32 Mio (33554432 octets), soit une marge théorique18073812 octets. Le fichier actuel est rembourré à 16 Mio ; taille du fichier et occupation utile ne sont pas identiques. EWRAM261044 octets et IWRAM29824 octets étaient déjà utilisées dans le build QA. Aucun nouvel espace RAM audio n’est alloué dans cette phase.

À titre de calcul, pas de conversion réalisée : un enregistrement mono8 bits à 13379 Hz de trois minutes pèse environ 2408220 octets (2,30 Mio). Les 80 fichiers accessibles représentent12819,88s : ce simple scénario PCM demanderait environ 171517164 octets, plus de cinq fois une ROM32 Mio, sans nouvelles banques, code ou métadonnées. Même les 22 références présélectionnées représentent environ 3893,26s et dépasseraient la capacité totale avec cette stratégie. L’intégration brute de ces enregistrements n’est donc pas une solution ; la taille d’un MP3 ne représente pas son coût une fois décodé.

Ce calcul n’affirme pas que le moteur se limite à un seul format de sample ni qu’aucune autre compression n’existe. Il démontre pourquoi « rééchantillonner des MP3 » n’est pas synonyme d’adapter une bande-son séquencée. La taille finale d’un arrangement n’est pas connue avant transcription et choix des samples ; aucun budget fictif par piste n’est annoncé.

## Travail nécessaire à partir des seuls MP3

1. Vérifier les droits et garder les références hors du dépôt public.
2. Auditionner et relever mélodie, basse, rythme, harmonie, forme et limites de boucle. Les mesures de tempo ont une ambiguïté demi/double ; le profil tonal global n’est pas une tonalité certifiée.
3. Obtenir si possible une partition/MIDI autorisé, ou transcrire. Une transcription polyphonique automatique risque de confondre harmonies, percussions, doublures, réverbération et variations. Aucune transcription fidèle n’est garantie par l’outil.
4. Réorchestrer pour une palette homogène : quelques timbres partagés avec Rouge Feu, percussions sobres, basse et mélodie lisibles, PSG utile. Ne pas chercher à reproduire littéralement la production3DS/Switch sur GBA.
5. Produire la séquence et sa banque, vérifier notes/voix, priorité, volume et véritable boucle en mesures. Réserver les samples longs aux usages justifiés, pas à tout le mix MP3.
6. Tester un seul prototype validé avant d’arranger les vingt-deux références présélectionnées.

La phase actuelle ne crée même pas ce prototype : elle s’arrête à la proposition. Le premier essai pourrait concerner le vélo si le créateur le retient, ou un thème de maison plus simple une fois sa transcription évaluée.

## Affectations partagées et routage futur

- Une modification globale de `MUS_PALLET` toucherait les maisons et le Bourg extérieur. Deux thèmes de maison selon le genre nécessiteraient un choix audio local ; ne pas modifier les personnages ou leurs événements.
- Une modification de `MUS_SEVII_ROUTE` toucherait bien plus que le Canyon. Affecter uniquement les cartes choisies, sans changer rencontres ni progression.
- `GetBattleBGM` dans `src/pokemon.c` utilise la classe du dresseur. Les 20 équipes de caméos sont aujourd’hui de classe PKMN_TRAINER et utilisent le thème dresseur. Donner un thème au Seigneur Enma exige un futur sélecteur musical ciblé, sans changer classe, stats ou équipe pour détourner le routage.
- Enma sauvage utilise `MUS_VS_MEWTWO` via `src/battle_setup.c`, les trois remplacements d’oiseaux utilisent le chemin légendaire. Ne pas assimiler ce routage au thème de la carte ou à celui du caméo Seigneur Enma.
- Matt avant Champion, Giovanni hors arène et le Conseil4 ne disposent pas déjà de tous les thèmes distincts envisagés. Une nouvelle proposition doit préciser si elle remplace un slot ou ajoute un contexte, avec un fallback natif.

## Batterie de tests après validation uniquement

Lecture séquencée, voix perdues avec cris/SFX, écoute du mix, volume, latence d’entrée, consommation CPU dans les animations sensibles, début/fin de combat, victoire, jingle, retour carte, changement d’étage, vélo/surf, refus de caméo et revanche, capture et sauvegarde/reprise. Répéter en émulateur GBA avec captures audio et, si possible, sur matériel réel. Une compilation réussie ne prouve aucun de ces résultats.

Le contrôle exécuté ici est une relance du build existant : `make -j4` répond «Nothing to be done», la ROM reste au SHA QA `84d3bffbb7e74322aa69d5df211f774576d00b1e3e16eec3794c5b74fc66e186`. Aucun test de nouvelle musique en jeu n’est revendiqué. Un essai de `make -q` a fait propager le mode requête aux sous-makes des outils et a échoué au garde du Makefile ; la relance normale a confirmé l’absence de problème de build. Aucun code n’a été corrigé pour cela.

## Droits et diffusion

Conformément au document fourni, les MP3 restent dans les pièces jointes et le scratch privé. Aucun MP3, MIDI dérivé ou enregistrement commercial n’est commité dans cette mission. Une adaptation reste fondée sur une composition protégée : vérifier les autorisations avant toute diffusion publique, ou employer des compositions originales/ressources autorisées. Le commit local de sauvegarde du développement et une éventuelle publication du projet sont deux opérations distinctes ; aucun push ni merge n’est fait ici.
