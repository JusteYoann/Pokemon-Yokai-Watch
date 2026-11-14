# Chantier E — Pokémon Yo-kai Emerald (journal)

## Architecture retenue (prouvée)

```
décompilation pret + code AP de Flit (fork FlitPix/pokeemerald, combo, fd64301)
      + couche Yo-kai (PATCHES/pokemon_yokai_emerald/yokai_source_patch.py, lit VOTRE ROM du hack)
      -> make -> ROM « pokemon emerald / yokai ap v0.1 »
      -> make extract -> base_patch.bsdiff4 (depuis votre Émeraude de base) + extracted_data.json (418 espèces)
      -> APWORLDS/pokemon_yokai_emerald/make_apworld.py -> pokemon_yokai_emerald.apworld (fork MIT du monde de Flit)
```

Le hack binaire du créateur ne peut pas recevoir le code Archipelago (testé : patch refusé, ROM forcée non démarrable,
`research/yokai-emerald/PROTOTYPE_RESULTS.md`). Ses ajouts sont donc reconstruits en source : graphismes lus dans votre
ROM, données de jeu = fiches validées.

## Décisions appliquées

| Sujet | Décision | Origine |
|---|---|---|
| Stats, types, talents, attaques, CT/CS, rencontres | fiches validées (`research/yokai-emerald/balance/yokai_balance.json`) | utilisateur |
| « Regard Touchant » (6e gén.) | Rugissement | validé par l'utilisateur |
| « Protection », « Lance-Boue » | Reflect, Mud Sport (noms français de 2005) | lecture littérale, signalée |
| Whisper niv. 38 | doublon d'Onde Folie (proposition Feinte en attente) | spécification |
| Gargaros | Sentier Sinuroc 20-23 (alternative Route 119 non appliquée) | spécification |
| Talent | même talent dans les deux emplacements | sûreté (aucun tirage) |
| Pokédex Komajiro/Whisper | textes remis à la bonne espèce (bug du hack) | risque de blocage |
| Cris | empruntés : Miaouss, Caninos, Pikachu, Lippoutou, Mackogneur, Fantominus | hack non analysé |
| Empreintes | vides | non extraites |
| Crédits | panneau de Bourg-en-Vol : SnappleRainKirby (KirbyLemonRain sur X), Ludo, SonGoku, Nicowico | créateur |
| Randomisation | le monde de Flit n'a pas d'option starter/rencontres : Jibanyan et les zones restent fixes | vérifié dans `options.py` |

## Tests réalisés (dans ce conteneur)

| Test | Résultat |
|---|---|
| Build pret anglaise + couche Yo-kai | ✅ compile ; 73/73 (`TESTS/verify_emerald_build.py`), sprites identiques au hack ; démarre (mGBA) |
| Build fork AP de Flit + couche Yo-kai | ✅ compile ; 73/73 ; nom de ROM correct |
| `make extract` | ✅ 418 espèces dans extracted_data.json |
| Génération YW2 + Yo-kai Emerald | ✅ 183/187 objets croisés |
| Application du `.apyokaiemerald` sur Émeraude US vanilla | ✅ MD5 contrôlé, ROM produite, 73/73 |
| Build française | ⛔ refusée par une règle de permission (2 fois) |
| Communication mGBA ↔ client ↔ serveur | ❌ à faire (connecteur `Zunawe/bhc-substitutes/mgba`) |

## Reste à faire

1. Build française : fusion AP de Flit × `qigast/pokeemeraude` (votre ROM France = SHA-1 `ca666651…` = cible de cette
   décompilation), traduction des textes ajoutés par le code AP.
2. Test de communication réel (mGBA + Lua + BizHawk Client + serveur local) : un objet reçu, un check envoyé,
   sauvegarde/reconnexion.
