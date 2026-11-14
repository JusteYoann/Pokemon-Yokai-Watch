# A — Yo-kai Watch 1 EUR, étude et prototype

Remplace définitivement YW3. Slot Yochix. Les recherches GitHub web et dans l’index communautaire épinglé n’ont pas identifié de port YW1 exploitable ; cela ne prouve pas qu’aucun projet privé ou non indexé n’existe.

Title ID EUR vérifié dans les données de compatibilité : `0004000000167800`. Zakuro déclare YW1 EUR jouable avec ses versions récentes (v0.2.7+), mais ce n’est pas un test personnel ni une preuve qu’un patch AP sera accepté. Le support Clockwork d’un jeu ne garantit pas le fonctionnement d’adresses ou hooks empruntés à YW2.

Architecture proposée : établir les événements et un ledger natif sur la vraie version EUR, avec Azahar RPC/GDB pour l’observation/recherche et un connecteur AP. Réutiliser le transport de YW2, pas ses adresses mémoire. Une sauvegarde seule ne garantit ni remise immédiate ni idempotence.

`CONNECTORS/3ds/probe_yokai_watch_1.py` vérifie titre et PID avant lecture. Aucune adresse par défaut, aucune écriture. Quatre tests RPC simulés passent. Le prototype APWorld propose rangs et événements de chapitres/amis/boss, mais **ses prérequis n’ont pas été mesurés en jeu** : génération refusée par défaut, option expérimentale réservée aux tests. Aucune ROM ni clé n’est téléchargée.

À faire : traces EUR, détection des vrais checks, remise des objets, ledger sauvegardé, logique de rang et quêtes vérifiée, transport et victoire contre un serveur réel. Ce slot n’est pas jouable.
