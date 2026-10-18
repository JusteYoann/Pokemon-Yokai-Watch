# Recherches exécutées pour les quinze choix v1

Ces deux scripts conservent les recherches réellement exécutées dans cette session. Ils lisent uniquement les WAV privés et produisent/affichent des métadonnées. Aucun enregistrement n’est inclus. Les chemins privés de session restent explicites ; fournir les WAV13379Hz épinglés, ou adapter le préfixe pour les rejouer. Les numéros sont les slots stables du catalogue, pas le rang dans la sélection15.

`recherche_recurrences.py` compare plusieurs fenêtres audio et des séquences spectrales ; `recherche_reprises_longues.py` étudie les reprises tardives des premiers motifs. Cette seconde recherche a retrouvé le cycle complet de Ghoulfather (~227,82248s) que les fenêtres commençant trop tard ne pouvaient pas observer. Les scores près d’un silence doivent être interprétés avec prudence (division par une énergie presque nulle), jamais pris pour une validation.

Ces études ne définissent pas automatiquement une boucle acceptable. Seules les positions épinglées dans `data/yokai/audio_loops.json` et leurs tests mGBA font référence. Les recherches sur Enma Track et Final Battle restent insuffisantes pour activer ces deux pistes ; aucune substitution approximative ne les remplace. Les fichiers source sont présents, donc ne pas demander de nouvelles archives en les supposant absents.
