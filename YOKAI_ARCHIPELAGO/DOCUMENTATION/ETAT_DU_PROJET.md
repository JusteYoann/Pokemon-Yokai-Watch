# État actif — 14 novembre 2026

Branche de coordination : `codex/archipelago-five-games-20261114`, depuis Claude `4617e348`. Fangame principal et master intacts.

| Chantier | État réellement vérifié | Manquant |
|---|---|---|
| A — YW1 EUR / Yochix | Title ID EUR identifié ; sonde RPC lecture seule et prototype APWorld ; 4 tests simulés de sonde | Adresses natives, patch/ledger, test du jeu ; génération bloquée par défaut |
| B — YW2 Spectres Psychiques / Juste Yoann | Monde V3 épinglé, génération réelle avec MKW et FR, objectif chapitre 10 sans postgame | Réception/check et reconnexion dans le jeu EUR |
| C — MKW PAL / Krackonyx | Monde 0.4.0, générations réelles ; assembleur local Riivolution, 5 tests synthétiques | Dolphin PAL et personnages visibles avec AP dans la même installation |
| D — Rouge Feu / Kammy64 ou Petit Shiny | Vrai source RC1 retrouvé ; 15 checks, Surf randomisé ; build et vrai réseau mGBA/AP ; sauvegarde à froid ; Goal Panthéon | Étendre checks et autres clefs, affiner Kanto, parcours manuel, GUI Lua/Windows |
| E — Emerald / Dejais | Travaux précédents conservés ; **en attente** | Reprise ultérieure, sans nouvelle demande de fichiers maintenant |

## Rouge Feu : résultat livré

Le source réel possède sa branche locale `codex/firered-archipelago-randomizer-20261114`, depuis le snapshot complet `a589cf00`, commit `d14b93cb`. Les générateurs AP sont sur la branche de coordination publique. Aucune ROM ni ressource privée n’y est publiée.

Build SHA256 : `0f6f0bfb739d246af3a73a7503db5c311c277133b9ce7befca1fcb79facd6c57`. Huit badges natifs en checks séparés ; six objets de la forêt remplacés ; don Safari remplacé par un check. Un Surf dans le pool, avec cinquième badge toujours requis. Les autres clefs restent natives. Inventaire : 351 objets visibles/cachés + don Safari et 67 macros de dons recensées, sans prétendre que tous les candidats sont validés.

Les preuves sont dans [preuves/](preuves/). Le test réel utilise MultiServer, le client officiel et la mémoire réelle mGBA libretro via adaptateur Python. Équipe, positions et contextes d’interaction sont préparés ; les vrais scripts donnent les flags, sans injection des flags de collecte/badge. Test de Wyatt, remises Potion/Surf, remplacement des objets ordinaires et du don Safari, reconnexion, sauvegarde à froid, sac plein et Goal. Le sac plein ne bloque plus les checks sortants : 24 contrôles réseau réussis, avec Goal confirmé dans le journal serveur. La reconstruction propre via le script livré produit un binaire identique. Le Panthéon est joué comme séquence native isolée ; le dernier boss et une partie intégrale ne sont pas testés.

Cinq seeds répétées à **trois** mondes, puis une seed avec les noms des créateurs, sont générées et terminables selon la logique actuelle. Les sphères et dépendances sont enregistrées, sans convertir leurs nombres en minutes. Le graphe FR regroupe encore les étapes natives avant Surf : son nombre de checks logiquement accessibles n’est pas le nombre de checks immédiatement ramassables.

33 tests unitaires réussis, y compris les tests simulés Emerald existants, sans reprise du chantier gelé. Lire [progression et objets](FIRERED_PROGRESSION_ET_OBJETS.md), [guide français](GUIDE_FIRERED_ARCHIPELAGO_FR.md) et [passation](../../CODEX_HANDOFF.md).

## Limites globales

Aucun Multiworld à cinq jeux n’est validé en jeu. Les réceptions natives YW1/YW2/MKW, la configuration graphique Lua Windows et les cinq victoires collectives restent à prouver. Les prototypes bloqués sont séparés des YAML utilisables. YW3 est abandonné ; son historique utile aux transports 3DS reste conservé.

Avant gel d’Emerald, la base française vanilla et la base AP × français ont compilé, sans couche Yo-kai finale ni réception native prouvée. Ces résultats restent historiques et ne valident pas le cinquième slot.
