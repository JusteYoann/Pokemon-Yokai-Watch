# État du projet — Yo-kai Watch Multiworld Archipelago

Mis à jour : 2026-11-14 (jalon 1). Légende : ✅ testé ici · 🧪 implémenté, non testé · 📋 plan · ⛔ bloqué.

## Organisation

Un dépôt (`JusteYoann/Pokemon-Yokai-Watch`), une branche autorisée (`claude/yokai-watch-archipelago-arch-vugpet`),
un dossier par chantier sous `YOKAI_ARCHIPELAGO/`. Les agents de recherche n'écrivent que leur rapport
(`DOCUMENTATION/chantiers/`) ; seul le coordinateur commite : aucun conflit possible entre agents.

| Chantier | Responsable | État | Prochaine preuve attendue |
|---|---|---|---|
| F — Central | coordinateur | ✅ Archipelago 0.6.9 ; générations réelles YW2+Émeraude et YW2+**Yo-kai Emerald** | génération à 5 slots |
| E — Pokémon Yo-kai Emerald | coordinateur (cette session) | ✅ build anglaise AP + Yo-kai (73/73), APWorld, génération, patch appliqué ; ⛔ build française bloquée ici | communication mGBA ↔ serveur |
| A — Yo-kai Watch 2 | coordinateur | ✅ intégration existante V3 (doryan-meunier) générée dans le multiworld | test en jeu sur votre PC (Zakuro/Azahar) |
| B — Yo-kai Watch 3 | — | ⛔ aucun projet existant ; exige votre dump + rétro-ingénierie | lire un flag de progression (sonde RPC) |
| C — Mario Kart Wii | agent C (rapport) | 🧪 base trouvée : `toent/Archipelago-MKWii` v0.4.0 (MIT), PAL `RMCP01` ; ⛔ exécution non autorisée ici | votre accord pour l'exécuter, puis génération |
| D — Rouge Feu × Yo-kai | agent D (en cours) | 📋 audit de la ROM 32 Mio en cours | rapport D |

## Ce qui fonctionne réellement (testé dans ce conteneur)

| Test (§15) | Résultat |
|---|---|
| 7 — génération Multiworld | ✅ 2 slots : YW2 + Yo-kai Emerald (183/187 objets croisés) ; ✅ YW2 + Émeraude officielle |
| 1 — démarrage | ✅ Yo-kai Emerald (build source) jusqu'à l'écran titre dans mGBA ; autres jeux : non testés |
| 2, 3, 4, 5, 6, 9 — connexion, checks, objets, sauvegarde, victoire | ❌ non testés |
| 8 — logique | ✅ la génération Archipelago valide l'accessibilité (playthrough calculé) |
| 10 — installation Windows propre | ❌ non testé |

## Blocages et actions de votre côté

1. **Compilation de la décompilation française** : refusée deux fois par une règle de permission de cet environnement.
   Soit vous l'autorisez (réglages de permissions de Claude Code), soit vous lancez `SCRIPTS/build_emerald.sh … fr …`
   sur votre PC (WSL2).
2. **Mario Kart Wii** : exécuter le monde tiers `toent/Archipelago-MKWii` a été refusé à l'agent puis à moi ; dites-moi si
   vous autorisez son exécution. Il exige un ISO **PAL** (`RMCP01`) et Dolphin 2512+. Les pages GameBanana des mods Yo-kai
   sont bloquées par le réseau de cette session (autoriser `gamebanana.com` pour les lire).
3. **Yo-kai Watch 3** : votre dump EUR de la cartouche (jamais transmis : les tests se font sur votre PC avec la sonde).
4. **Rouge Feu** : selon le rapport D, le code source du fangame sera probablement nécessaire.
