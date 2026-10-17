# Scripts de recherche des sections musicales

Ces cinq scripts conservent les analyses effectivement exécutées pendant la session : comparaison par fenêtres FFT, recherche de périodicité spectrale, puis raffinement à l’échantillon. Ils ne contiennent ni enregistrement ni sample audio. Ils évitent de perdre la méthode de recherche si l’environnement disparaît.

Ce sont des scripts d’étude, avec les chemins privés de la session explicitement présents dans le code (`/workspace/private-audio/dpcm-full-sources/NN.wav`). Adapter ce préfixe si nécessaire et fournir les sources privées avant de les lancer. Dépendances : requirements-audio.txt. Les résultats sont des métadonnées JSON hors du dépôt, jamais de nouveaux morceaux.

Ils ne sélectionnent pas automatiquement un raccord « validé ». Une corrélation de percussion ou d’accord ne suffit pas à identifier une boucle musicale complète. Pour le build, seules les positions épinglées dans `data/yokai/audio_loops.json` sont utilisées, via `generer_audio_prive.py`. La validation réelle est dans les tests mGBA et les rapports de QA_RECETTE_FINALE/INTEGRATION_MUSIQUES.
