> **Version de test FR0.5.0 — 16 novembre :**628 checks ; Coupe/Surf/Force/Flash randomisés, Vol utile.620 détecteurs avec redémarrage,44 contrôles réseau,37 protections et finale native testés. Configuration quatre jeux préparée ; génération à quatre bloquée ici par le package Emerald français0.2.1 absent du système de fichiers. Voir [version de test et procédure quatre jeux](FIRERED_VERSION_TEST_4_JEUX.md). Les résultats précédents restent historiques.

## Situation corrigée — retour utilisateur du 16 novembre 2026

Cette mise à jour prévaut sur les anciens états « Emerald en attente » ou « YW2/MKW seulement générés » ci-dessous. Elle rapporte le fonctionnement indiqué par l’utilisateur ; elle n’ajoute pas de tests effectués sur ce poste.

| Jeu | État actuel | Suite |
|---|---|---|
| Pokémon Yo-kai Emerald | Fonctionnel selon le retour utilisateur | Conserver l’intégration existante |
| Yo-kai Watch 2 : Spectres Psychiques EUR | Fonctionnel selon le retour utilisateur | Conserver l’intégration existante |
| Mario Kart Wii | Archipelago fonctionnel selon le retour utilisateur | Ajouter le mod visuel Yo-kai dans la même installation |
| Pokémon Rouge Feu × Yo-kai Watch | Intégration en développement,625 checks actifs et tests natifs/réseau documentés | Poursuivre la couverture et les essais de progression |
| Yo-kai Watch 1 EUR | Seule intégration de jeu encore absente ; prototype technique présent | Développer l’intégration jouable |

Le test collectif final avec les cinq jeux reste à réaliser après l’intégration de YW1. Ne pas redemander les fichiers Emerald pour cette simple correction de statut, ni recommencer les intégrations déclarées fonctionnelles. Les limites et preuves locales des anciens essais restent conservées comme historique.

> **Jalon courant — import massif du 16 novembre :** [rapport et limites](FRLG_IMPORT_MASSIF.md). 625 checks par défaut (626 avec Terr’heure),74 anciens IDs conservés ; transport3, sauvegarde1 et registre256 dresseurs. Les descriptions15/74 ci-dessous sont historiques. Le graphe de progression reste regroupé et les cinq jeux ensemble ne sont pas validés.

Tests du jalon :617 détecteurs natifs et persistance à froid,2057 assertions ;37 protections ;36 contrôles avec vrai serveur/mGBA dont Wyatt et un dresseur ordinaire joués ;5 seeds résolubles à trois mondes. Captures et256 victoires sont vérifiées par fixtures natives, pas par166 captures et256 combats joués.

> **État actif au 16 novembre :** [extension FRLG validée](FRLG_EXTENSION_VALIDEE.md). 74 checks par défaut, Surf/Flash randomisés ; 15 anciens IDs conservés. 211 contrôles de sources natifs, 37 contrôles de protections, 37 tests unitaires, 15 seeds à trois mondes. Le test réseau étendu a réussi. Les cinq jeux ensemble et Windows restent non validés. Les sections suivantes décrivent le jalon historique du 14 novembre.

# Historique des vérifications locales — 14 novembre 2026

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
