# TECHNICAL_COMPARISON — les six configurations (+ Zakuro en référence)

Catégories : **Confirmé** / **Probable** / **Non vérifié** / **Bloquant**. « Difficulté » = travail pour obtenir une
intégration Archipelago jouable de bout en bout (1 = intégration, 5 = recherche lourde + fork d'outil).
Aucune mesure de performance n'a été faite : **aucun chiffre n'est donné** (voir §3 pour les tests à mener).

## 1. Tableau principal

| Config | Jeu tourne | EUR | Stabilité connue | Accès progression | Recevoir objets | Difficulté | Principaux risques | Confiance | Tests restants |
|---|---|---|---|---|---|---|---|---|---|
| **YW2 + Azahar** | Confirmé (mod V3, 2124.3) | Confirmé | Probable (bêta du mod) ; #1636 boss JPN, #2172 Vulkan | Confirmé (GDB, boîte `0x0091C000`) ; RPC Non vérifié en 2124.3 | Confirmé (patch code + dons) | **1** | Ψ Blasters de YW2 cassé (#170, Bloquant pour l'option `blasters` du mod) ; seule 2124.3 validée ; stub GDB fragile | **Élevée** | partie FR complète dans notre multiworld ; #170 en EUR ; RPC dispo en 2124.3 ? |
| **YW2 + Clockwork** | Probable (jeu le plus testé, **USA**) | Non vérifié | Non vérifié (pas d'interpréteur de secours) | Non vérifié (aucune API ; à développer) | **Bloquant** (patch de code refusé, `mods.cpp:136`) | **5** | refaire tout le patch YW2 en crochets C ; fork Clockwork | Élevée (sur le blocage) | aucun utile tant que le patch n'est pas porté |
| **YW3 + Azahar** | Non vérifié | Non vérifié | Non vérifié (aucune issue trouvée) | Probable (RPC/GDB + patch) | Probable (patch + fonctions internes) | **4** | patch entièrement à écrire ; compat EUR inconnue | Moyenne | démarrage, 1re heure, boss, sauvegarde, FR |
| **YW3 + Clockwork** | Non vérifié | Non vérifié | Non vérifié | Non vérifié (crochets à développer) | Probable (crochets, prototype B) | **5** | idem + fork + chemins non recompilés = plantage | Faible | tout |
| **Blasters + Azahar** | Non vérifié | Non vérifié | Non vérifié ; risque UDS/Pia (famille de #170) | Probable (RPC/GDB + patch) | Probable (patch) | **4** | jeu solo dépendant du sans fil local ; mise à jour 2.0 = autre code | Faible | mission solo, boss, Moon Rabbit Crew, sauvegarde |
| **Blasters + Clockwork** | Probable (Blasters cité, UDS tracée sur Blasters) | Non vérifié | Non vérifié (issue #5 fermée) | Non vérifié (à développer) | Probable (crochets) | **5** | fork ; projet d'un mois ; EUR « new » | Faible | tout |
| *YW2 + Zakuro* (réf.) | Confirmé (défaut du mod) | Confirmé | Probable (bêta) ; Ψ Blasters solo corrigé (patch 0005) | Confirmé (GDB ajouté par le mod) | Confirmé (patch code, recompilé avec) | **1** | un seul mainteneur ; fork du mod (5 patchs) | Élevée | partie complète |
| *YW3 + Zakuro* (réf.) | Confirmé (déclaratif, `COMPATIBILITY.md:38`) | Confirmé (déclaratif) | Probable | Probable (GDB + patch ; overrides 3dsrecomp) | Probable | **3-4** | patch à écrire ; stabilité à vérifier | Moyenne | partie complète |
| *Blasters + Zakuro* (réf.) | Non vérifié (absent de la liste) | Non vérifié | Non vérifié | Probable | Probable | **4** | inconnu | Faible | tout |

Références : AZAHAR_AUDIT.md, CLOCKWORK_AUDIT.md (dont §6 Zakuro), GAME_COMPATIBILITY.md, PROTOTYPE_RESULTS.md.

## 2. Critères transverses

| Critère | Azahar | Clockwork | Zakuro |
|---|---|---|---|
| Installation Windows | installeur/zip officiel ; réglage RPC ou GDB à cocher | release + **compilateur C requis** (Build Tools VS) pour compiler chaque jeu | zip ; compilateur auto (gcc/clang ou Zig téléchargé) ; ~4 min la 1re fois (mod YW2) |
| Manettes | SDL, mature | SDL3, rebindable | SDL3 (patch 0003 du mod), PS/Xbox/Switch |
| Risque de plantage | issues connues (Vulkan → OpenGL) ; JIT mature | **arrêt** sur tout saut non recompilé | interpréteur de secours |
| Sauvegardes | format console ; save states | par jeu ; import JKSM | par jeu ; séparées d'Azahar |
| Diagnostic | GDB, journal, save states, RPC (captures, stats) | traces d'appels (`RECOMP_TRACE_CALLS`), captures F12 | GDB (mod), journal |
| Reproductibilité | save states + `SetInput` RPC (rejouer des entrées) | aucune (pas de save states) | non documenté |
| Mods de code | oui (code.bps/exheader) | **non** | oui (+ recompilation avec le mod) |
| Licence | GPLv3 | MIT | MIT |
| Maturité | Citra (≈10 ans) + Azahar | **1 mois**, 17 commits | ~2 mois, 374 commits, 1 mainteneur |

## 3. Performances : rien n'est mesuré, voici comment le faire

Pas de benchmark fiable publié pour ces jeux sur ces trois moteurs. Protocole (NEXT_STEPS.md phase 1) :
1. même PC, même dump, même scène (save state Azahar / sauvegarde identique ailleurs) : **Springdale de jour**
   (YW2), **une mission Blasters solo**, **Saint Peanutsburg** (YW3) ;
2. 5 minutes par scène ; relever FPS jeu (RPC `GetPerfStats` sous Azahar ; overlay pour les autres),
   mémoire du processus (Gestionnaire des tâches), temps de chargement d'une zone au chronomètre ;
3. noter tout plantage, glitch, softlock, avec la version exacte du moteur.
