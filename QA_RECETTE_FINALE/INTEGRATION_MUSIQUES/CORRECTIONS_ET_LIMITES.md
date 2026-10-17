# Corrections réellement nécessaires et limites de mesure

## Reprise après fanfare : bug reproduit puis corrigé

Sur la première ROM musicale, l’appel natif PlayFanfare(MUS_OBTAIN_ITEM) coupe les canaux BGM. La reprise standard réactive le séquenceur, mais la note TIE du long échantillon a déjà été jouée : aucun nouvel événement ne recrée sa voix. Après400frames, le bon en-tête musical était toujours sélectionné mais aucune voix ne jouait. FANFARE_AVANT_CORRECTION.json en conserve l’empreinte et le résultat. Ce problème aurait touché les objets/fanfares en exploration.

L’adaptateur privé conserve la voix et sa position exacte avant l’arrêt, puis la restaure dans un canal libre à la reprise. Il ne vole aucun canal aux effets sonores et peut réessayer au frame suivant. Un changement de morceau annule le cache, empêchant une ancienne musique de réapparaître. Les fondus temporaires empruntent la même logique. Aucun format de sauvegarde, calcul du mixer ni décodeur DPCM n’est changé. Le build privé utilise64octets d’IWRAM supplémentaires selon le linker ; le build public n’alloue pas ce cache.

Tests natifs : fanfares objet/niveau/soin ; arrêt répété/reprise par identifiant ; fondu temporaire/reprise ; annulation si le morceau change ; volume de la voix restaurée non nul. Une ancienne valeur savedMusic du vélo est aussi remappée vers le nouvel identifiant, sans changer le format de sauvegarde ; écriture et lecture Flash contrôlées. Voir TEST_INTERRUPTIONS_MGBA.json.

## Repli public

Les repli de la Tour, de la Sylphe et du Bois Baies ont été comparés aux anciennes cartes et corrigés vers les thèmes natifs exacts : mus_poke_tower, mus_silph et mus_viridian_forest. La Sylphe libérée retrouve mus_silph. VERIFICATION_LIAISON.json compare les pointeurs réellement liés et les octets de chaque sample privé.

## Comparaison audio : corriger la mesure, sans masquer un défaut du jeu

Les premières corrélations brutes déclenchaient des alertes sur Hinozall puis sur des morceaux percussifs. Les captures montrent un décalage continu lié au DAC, et le pas d’alignement de1ms/0,5ms pouvait manquer la bonne phase d’un signal riche en harmoniques. Les signaux réellement capturés ont été conservés en privé pour diagnostic. Le résultat initial sans rejet du continu est archivé dans ECHEC_MESURE_AUDIO_SANS_REJET_DC.json.

La mesure finale compare une bande échantillonnée à4kHz, retire le continu, puis interpole sur une grille16kHz pour rechercher le délai. Elle maintient le seuil0,85 et compare aussi la musique après les appels de bruitage/cri. Le format et les fichiers musicaux n’ont pas été modifiés pour faire passer cette mesure. Une corrélation de forme d’onde confirme l’identité technique du signal ; **elle ne remplace pas une écoute perceptive**, un jugement de qualité des voix ou une validation artistique des raccords.

Les fenêtres natives, les captures et les empreintes correspondent aux ROM indiquées dans chaque rapport. Les anciens rapports de tests partiels/échoués restent des preuves historiques, pas le verdict de la version courante. Aucun test ciblé ne prouve le parcours complet du jeu ni les performances sur une console physique.

La comparaison des raccords est maintenant effectuée sur **cinq fenêtres audio réellement sorties de mGBA par morceau**, autour de chaque retour de l’échantillon. Ces fenêtres correspondent au signal décodé fin→début de boucle, pas seulement à la position lue dans la RAM. Les WAV de preuve restent privés. La fréquence d’analyse4kHz et la grille d’alignement16kHz sont des paramètres de mesure ; tous les morceaux restent encodés/lus à **13 379Hz**. La cadence entre raccords est aussi comparée à la durée attendue du sample.

## Bois Baies : raccord superposé à un cri ambiant

La capture du premier raccord du Bois Baies contenait un cri ambiant natif. La trace montre deux voix : la musique reste active et progresse normalement, tandis qu’un canal appartenant à gPokemonCryTracks joue par-dessus. Cela empêchait la fenêtre mélangée de correspondre à la musique seule ; les quatre raccords suivants correspondaient déjà à plus de0,97.

La première sonde de cri lisait le mauvais offset de MusicPlayerTrack.chan (28 au lieu de32). Elle est corrigée et comparée à IsPokemonCryPlaying natif sur un vrai cri sans atténuation. TRACE_FORET_PREMIER_RACCORD.json conserve les données de l’ancien essai, y compris ses booléens de sonde incorrects ; VERIFICATION_LECTURE_CRI.json valide la sonde corrigée.

La recette ne désactive pas les sons de la forêt : elle conserve la fenêtre avec cri et réalise un sixième cycle pour obtenir **cinq raccords audio propres**, en plus de la coexistence observée avec ce cri. Un raccord mal corrélé sans cri natif reste un échec. Cela distingue une superposition sonore normale d’une corruption de musique, sans baisser le seuil ni supprimer les bruitages.
