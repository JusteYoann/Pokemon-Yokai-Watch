# Pilote de recette : attaques épuisées et combats longs

Le contrôle indépendant au jalon c700fdeb2 a échoué lors du combat Don Morleone : le pilote appuyait uniquement sur A. La cause exacte de cet ancien arrêt n’est pas instrumentée ; Rancune est une hypothèse, pas un fait démontré. Une régression dédiée part maintenant d’une première attaque légalement épuisée : l’ancien pilote reste bloqué, le nouveau choisit une attaque autorisée par le moteur et remporte le vrai combat. Voir TEST_PILOTE_PP_MGBA.json.

Le premier correctif a ensuite atteint sa limite de 25 000 itérations lors d’une revanche : le curseur était bien sur la deuxième attaque, PP15, face au Doyen Doyagari (PV18). Ce n’était donc plus un blocage sur PP0. La capture et les données sont conservées dans preuves/cameo-morleone-revanche-1-echec-pilote.*. Le budget passe à 60 000 itérations pour laisser se terminer les combats avec soins et renforcements défensifs. La suite complète réussit alors ; les équipes, capacités et statistiques des adversaires restent inchangées.

Le pilote observe la RAM et appelle CheckMoveLimitations ; il sélectionne avec la croix directionnelle. Il n’écrit pas les PP, le curseur ni le résultat du combat. Les fixtures de victoire utilisent une équipe artificiellement forte avec quatre attaques ; cela vérifie les scripts, jamais l’équilibrage. La fixture de régression initialise explicitement PP1=0 avant le combat.

Le rapport principal est désormais remplacé par un résultat d’échec si le test lève une exception, afin qu’un ancien succès ne soit plus confondu avec un nouvel essai inachevé. Une vérification depuis GitHub doit utiliser ce nouveau pilote ; le premier essai natif du clone c700 n’est pas annoncé réussi.
