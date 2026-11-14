# B — Yo-kai Watch 2 Spectres Psychiques EUR

Slot Juste Yoann. Intégration doryan-x100 réutilisée au commit épinglé dans `CONFIG/dependencies.lock.json`, V3. Les APWorlds YW2, MKW et Rouge Feu sont chargés ensemble sous AP0.6.9 et génèrent réellement des parties. Aucun fork du protocole serveur n’est nécessaire à ce jalon.

Les YAML actifs imposent `objectif: finir_chapitre_10`, `apres_jeu: aucun`, `pieges: false`. Le port existant force lui-même l’absence de checks postgame pour cet objectif. Les chapitres, objets, règles, conditions de victoire et liaisons du client proviennent du port V3 ; ne pas emprunter ses adresses pour YW1.

Le port fournit un pont GDB (24689) et des transports documentés pour sa version EUR, avec transactions arrêtant le processeur. Les écarts Azahar/Zakuro restent à vérifier dans la configuration finale. Une récompense envoyée par FR au slot YW2 et enregistrée par le vrai serveur ne prouve pas la réception dans la sauvegarde YW2 : aucun exemplaire du jeu EUR n’a été connecté dans ces essais.

À faire : installer localement le patch V3 sur la copie du joueur, connecter le client fourni au même serveur et tester check, réception, déconnexion, sauvegarde et objectif chapitre10. Réutiliser les mécanismes existants plutôt que créer un second prototype concurrent.
