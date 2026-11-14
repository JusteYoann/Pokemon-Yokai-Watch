# ROADMAP — étapes restantes

🖥 = sur votre PC. Les durées sont indicatives (voir IMPLEMENTATION_STRATEGY.md).

## Phase 0 — Autorisations et vérifications (en parallèle, avant tout développement de contenu)

1. 🖥 Me transmettre le **lien de publication** du hack (ou le nom du créateur) : il n'a pas été trouvé en ligne.
2. Envoyer les demandes d'autorisation (PERMISSION_REQUEST.md) : créateur, dessinateurs (via le créateur),
   Flit (code C AP), Zunawe (code C du patch officiel).
3. 🖥 Partie de 30 min sur le hack dans mGBA : rencontrer un Yo-kai (Route 101/102/103), ouvrir les pages Pokédex de
   Komajiro et Whisper, le résumé de Whisper (type 255). Noter tout plantage.
4. 🖥 Dumper votre cartouche **Émeraude française** et compiler `qigast/pokeemeraude` (BUILD_GUIDE.md §2) :
   les SHA-1 doivent être égaux.

## Phase 1 — Jalon « anglais AP » (2-4 semaines)

1. Forker `FlitPix/pokeemerald` (branche `combo`) ou le code officiel s'il est obtenu → `yokai-emerald-ap`.
2. Ajouter la couche Yo-kai en source, générée par `tools/yokai_extract.py` (étape à automatiser : JSON/PNG →
   `src/data/pokemon/*.h`, `graphics/pokemon/<nom>/`, `include/constants/species.h`, `pokedex.h`,
   `wild_encounters.json`, graphismes de Brendan/May, panneau de Bourg-en-Vol).
   Corriger : type de Whisper, Pokédex 389/392, Blizzaria niv. 1-100 ; retirer Jirachi/Celebi/Ho-Oh sauvages.
3. Forker le monde AP correspondant → « Pokemon Yo-kai Emerald », régénérer `extracted_data.json`, 418 espèces,
   Pokédex 53 octets.
4. 🖥 Tests réels mGBA + connecteur Lua (BUILD_GUIDE.md §5) : les 8 vérifications de la mission (sauf le français).
5. Partie test avec les autres jeux du multiworld.

## Phase 2 — Jalon « français » (3-6 semaines)

1. Porter les couches AP et Yo-kai sur `qigast/pokeemeraude` (fusion git, résolution des conflits de textes).
2. Traduire : noms Yo-kai (noms officiels français à vérifier), catégorie, 6 descriptions (avec l'accord du
   créateur), panneau de crédits, textes ajoutés par le code AP.
3. Monde AP : hash de base = Émeraude **française**, nom de ROM distinct.
4. 🖥 Partie complète jusqu'au Conseil 4 dans un multiworld à 5 jeux ; vérifier sauvegarde et reconnexion.

## Phase 3 — Finition et distribution

1. Patch de distribution (BPS) généré par script, vérification « pas d'asset non autorisé ».
2. Guide joueur français (installation mGBA/BizHawk, connecteur, YAML).
3. CI : compilation + `compare_with_vanilla.py` + tests du monde AP (`worlds/<monde>/test`).

## Crédits à porter dans le jeu et la documentation

Créateur de « Pokémon Yo-kai Emerald » (à identifier) ; Ludo (sprite de Jibanyan) ; SonGoku et Nicowico (autres
sprites) ; pret (pokeemerald, agbcc) ; DizzyEgg et Qigast (décompilation française) ; Zunawe (Archipelago Pokémon
Émeraude, connecteur mGBA) ; Flit (fork AP) ; l'équipe Archipelago ; Level-5 (Yo-kai Watch) et Game Freak / The
Pokémon Company (Pokémon), propriétaires des marques.
