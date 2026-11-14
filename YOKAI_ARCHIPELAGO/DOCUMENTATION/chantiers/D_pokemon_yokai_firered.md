# Chantier D : Pokémon Rouge Feu × Yo-kai Watch (« Yo-kai Watch GBA 1.0 »), audit technique

Date : 2026-11-14. Analyse en lecture seule de la ROM fournie par l'utilisateur. La ROM n'a été ni modifiée ni copiée dans un dépôt git. Les copies de travail sont restées dans le scratchpad de session.
Repère de lecture : **[V]** = vérifié par mesure ou exécution dans cette session. **[S]** = supposé ou déduit, non prouvé.

---

## 1. Résumé et verdict

* **[V] Il s'agit d'une build de la décompilation pret/pokefirered**, compilée avec agbcc, et non d'un hack binaire.
  * Tout le code vanilla est décalé de façon progressive (+0x4 au début, jusqu'à +0x14BB4 à la fin).
  * Des fonctions entières sont identiques octet pour octet, mais à d'autres adresses.
  * Les variables IWRAM et EWRAM ont été déplacées.

  Seule une recompilation produit ces trois effets à la fois. Aucun moteur étendu n'est présent :
  * pas de CFRU ni de DPE ;
  * pas d'augmentation du nombre d'espèces : 412 emplacements, Pokédex de 386 ;
  * pas d'augmentation du nombre d'objets : 375.

  Le contenu Yo-kai **remplace** des emplacements vanilla : 304 Yo-kai occupent les espèces 1-251 et 277-329.
* **[V] Le patch de base FRLG communautaire (Vyneras, apworld 1.1.5) ne s'applique pas.** Il exige une ROM vanilla de MD5 `e26ee0d4…` (FR rév. 0), alors que la ROM fournie a pour MD5 `72ad2cd5…`. De plus, son client refuserait explicitement cette ROM, comme détaillé au §4.
* **[V] Un connecteur externe seul est techniquement possible pour un prototype.** Les drapeaux sont lisibles, le sac est inscriptible et un compteur peut être gardé dans la sauvegarde. Les adresses RAM du fangame ont été retrouvées et confirmées en exécution sous mGBA.
* **Limite d'un connecteur seul :** il ne peut pas *remplacer* l'objet trouvé à un emplacement. Il ne fait qu'ajouter des objets, sans message en jeu.
* **[S] Une vraie randomisation demande donc de modifier le jeu.** La voie saine est le code source du fangame (dépôt git de la décompilation), pour y fusionner le code de réception d'objets. Le patch AP lui-même n'est pas portable : c'est une branche de 930 fichiers et +64 000 lignes.

**Verdict.**
* **Prototype :** faisable dès maintenant avec un connecteur mGBA (Lua) ou BizHawk et la ROM telle quelle.
* **Intégration complète :** demander le code source à l'auteur, ou à l'utilisateur s'il en est l'auteur.

---

## 2. Identité de la ROM

| Élément | Valeur | Statut |
|---|---|---|
| Fichier | `Yo-kai Watch GBA 1.0.gba` (scratchpad `frlg_upload/`) | [V] |
| SHA-1 / MD5 | `40c59a9f240d29a7b16d1dd299b1125513a280c4` / `72ad2cd5ddb135217ffaafc289234254` | [V] |
| En-tête GBA | « POKEMON FIRE », code BPRE, maker 01, révision 0 | [V] |
| En-tête GF (0x100) | version 4 (FireRed), langue 2 (anglais), `gameName = "pokemon red version"` | [V] |
| Taille | 33 553 675 o (0x1FFFD0B). La ROM est pleine sur 32 Mio, avec des données utiles réparties sur toute la plage | [V] |
| Langue du texte | **Français** : noms Yo-kai, noms Hoenn français (Carvanha, Libégon…), attaques (« Poing Karaté »), menu « NOUVEAU JEU » | [V] |
| Chaînes d'outils | Aucune trace HMA, XSE, AdvanceMap ou CFRU. Seuls subsistent les chemins `C:/WORK/POKeFRLG/...` d'origine Game Freak | [V] |
| Démarrage | Démarre dans mGBA 0.10.2 jusqu'au menu principal « NOUVEAU JEU ». Une seule capture, hors dépôt : `scratchpad/frlg_run/out/titre.png` | [V] |

Référence vanilla : une copie de la décompilation a été compilée dans le scratchpad (`frlg_ref/`). Le résultat donne `pokefirered.gba: OK`, avec SHA-1 `41cb23d8…` et MD5 `e26ee0d4…`, identique à la ROM attendue par AP.

### Preuves « build de décompilation » plutôt que « hack binaire » [V]
1. **Décalage progressif du code** (`objgrowth.py`). Le début de chaque fichier objet vanilla est retrouvé dans le fangame, avec un décalage qui croît le long de `.text` :
   * `sprite.o` +0x4 ;
   * `battle_main.o` +0x250 ;
   * `battle_script_commands.o` +0xDE0 ;
   * `overworld.o` +0x2670 ;
   * `party_menu.o` +0x5430 ;
   * `pokemon_summary_screen.o` +0x5F54 ;
   * `m4a.o` +0x14BB4.

   Un éditeur binaire ne peut pas déplacer tout le code de cette façon.
2. **Fonctions identiques octet pour octet mais déplacées.** 2 505 fonctions ont été retrouvées par motif unique de 24 octets, par exemple `CreateSprite` 0x08006F8C → 0x08006F90 et `_calloc_r` 0x081E9DCC → 0x081FE980. Le compilateur est donc agbcc, le même que pour la référence. [S] Une build `modern` (gcc) ne donnerait pas ces correspondances.
3. **Variables RAM déplacées.** Les déplacements sont mesurés sur les pools littéraux et cohérents sur des centaines de références :
   * IWRAM : +0x560, soit 0x560 octets de nouvelles variables, par exemple `gSaveBlock1Ptr` 0x03005008 → 0x03005568 ;
   * EWRAM : +0x64, +0x88 ou +0x94 selon la zone.
4. **Tables déplacées « en place ».** Toutes les tables pointées par l'en-tête GF ont glissé de +0x14C44 à +0x3EAA4, sans être redirigées vers de l'espace libre. C'est ce que produit un éditeur de liens.

Le code ajouté ou modifié représente environ 25 Kio répartis dans de nombreux fichiers : combat, terrain, menu d'équipe, résumé, Pokédex, `main.c`, `load_save.c`, `evolution_scene.c`, `learn_move.c`. Il faut y ajouter environ 60 Kio de données entre la fin de `src/` et `libgcnmultiboot`.

Point ouvert [S] : une zone 0x740000–0xCB0000 n'existe pas dans le `ld_script.ld` vanilla. Elle contient notamment `gEvolutionTable`, déplacée à 0x08740C00, une adresse alignée et isolée. Deux explications sont possibles : un `ld_script` modifié, ou une insertion après compilation par un outil binaire. Ce point n'est pas tranché.

---

## 3. Contenu modifié mesuré

| Élément | Vanilla FR | Fangame | Statut |
|---|---|---|---|
| Emplacements d'espèces (table de noms) | 412 | 412, **non étendu** | [V] |
| `pokedexCount` (en-tête GF) | 386 | 386 | [V] |
| Yo-kai | — | **304** : espèces 1-251 (Jibanyan, Komasan, Whisper…) et 277-329 (Égaroni, Éleknyan… Vito). Les emplacements 252-276 restent « ? » | [V] |
| Pokémon restants | — | 330-411 : Hoenn en français, présents dans les tables mais **jamais** dans les rencontres ni les équipes | [V] |
| Rencontres sauvages | 132 en-têtes, 113 espèces | 132 en-têtes, mêmes cartes, **80 espèces, toutes Yo-kai** | [V] |
| Dresseurs | 742 | **760** (nouveaux : « Ariane », « Seig. Enma », « Katie »…), 289 espèces Yo-kai | [V] |
| Cartes | 43 groupes, 425 cartes | 43 groupes, **426 cartes** (+1 dans le groupe 9) | [V] |
| Événements de carte | — | 41 cartes avec un nombre de PNJ/warps/triggers différent, 27 nouveaux flags d'objets (0x304…0x359, 0x4AB…) | [V] |
| Objets cachés | 183 | 183, mots identiques sur les 425 cartes communes | [V] |
| Musique | 347 chansons | ~379 entrées. Musique changée sur 423 des 425 cartes | [V] / [S] pour le nombre exact |
| Objets | 375 | 375, **mêmes ID**. Les nouveaux objets occupent des emplacements vanilla inutilisés (100 « Yo-kai Watch », 101 « Médallium », 4 « Yo-kai Ball ») | [V] |
| Types | 111 lignes d'efficacité | 123 lignes, un **type d'indice 18** apparaît | [V] |
| Flags de badges | `setflag FLAG_DEFEATED_BROCK` (0x4B0) et `FLAG_BADGE01_GET` (0x820) | Séquence identique dans le script d'arène d'Argenta (0x08174BA1). Ondine : 0x4B1 et 0x821 | [V] |
| Sauvegarde | SaveBlock1 = 0x3D68, SaveBlock2 = 0xF24, flags @0xEE0, vars @0x1000, tailles de poches 42/30/13/58/43/30 | **identiques**, valeurs calculées par `sizeof` dans l'en-tête GF | [V] |
| Format de sauvegarde | — | Pas de changement de structure détecté. `load_save.c` a cependant été modifié | [S] |

### Emplacement des tables principales (fangame) [V]
| Table | Adresse vanilla | Adresse fangame |
|---|---|---|
| gSpeciesNames | 0x08245EE0 | 0x082621AC |
| gSpeciesInfo (stats de base) | 0x08254784 | 0x08273B3C |
| gEvolutionTable | 0x08259754 | 0x08740C00 |
| gLevelUpLearnsets | 0x0825D7B4 | 0x08279F30 |
| gMonFrontPicTable | 0x082350AC | 0x08249CF0 (images vers 0x08D2F…) |
| gTrainers | 0x0823EAC8 | 0x0825A9FC |
| gWildMonHeaders | 0x083C9CB8 | 0x083FAB18 |
| gMapGroups | 0x083526A8 | 0x0836F0AC |
| gMapLayouts | 0x0834EB8C | 0x0836B56C |
| gItems | 0x083DB028 | 0x0840B070 |
| gBattleMoves / gMoveNames | 0x08250C04 / 0x08247094 | 0x0826F5B8 / 0x08263360 |
| gScriptCmdTable / gSpecials / gStdScripts | 0x0815F9B4 / 0x0815FD60 / 0x08160450 | 0x08166738 / 0x08166AE4 / 0x0816733C |
| gPokedexEntries | 0x0844E850 | 0x0848D2F4 |

---

## 4. Intégrations FRLG Archipelago existantes (vérifiées)

* **Le monde officiel AP 0.6.9 n'inclut pas FRLG** (fait établi en amont).
* **Monde communautaire : `vyneras/Archipelago`**, branche `frlg-stable`, commit `3d1359c` du 2026-10-12, `worlds/pokemon_frlg`, apworld **1.1.5**, AP ≥ 0.6.7. Il a été cloné dans `scratchpad/frlg_ap/vyneras_ap` [V].
  * **ROM exigée :** `rom.py` → `FIRERED_REV0_HASH = "e26ee0d44e809351c8ce2d73c7400cdd"` (rév. 1 : `51901a6e…`, plus LeafGreen). `world.py` utilise `UserFilePath.md5s = PokemonFireRedProcedurePatch.hash`, si bien que le fichier ROM est **validé par MD5**. Le MD5 du fangame, `72ad2cd5…`, est rejeté [V].
  * **Patch de base :** `data/base_patch_firered.bsdiff4` (bsdiff4 binaire), appliqué sur la ROM vanilla, suivi de jetons (`token_data`). Un bsdiff appliqué à une autre ROM produit des données sans valeur [V].
  * **Client :** BizHawk (`worlds/_bizhawk`, `connector_bizhawk_generic.lua`), sans support mGBA [V]. Sa fonction `validate_rom` :
    * lit le nom à 0x108. Le fangame contient exactement `"pokemon red version"`, ce qui déclenche « You appear to be running an unpatched version », puis `return False` ;
    * compare la somme de contrôle stockée à 0x1B8 (`rom_checksum = 9673481`). Le fangame contient à cet endroit le champ vanilla `giftRibbonsOffset` (0x309C).

    Le client refuserait donc le fangame **à deux niveaux** [V].
  * **Mécanisme d'objets [V] :**
    * le client écrit dans `gArchipelagoReceivedItem`, une variable EWRAM **ajoutée par le patch** (id u16, index u16, drapeau « plein », drapeau « afficher ») ;
    * le jeu patché distribue l'objet et affiche le message ;
    * le compteur d'objets reçus est stocké dans la sauvegarde à `gSaveBlock1Ptr + 0x3DE8`, au-delà de la taille vanilla 0x3D68. Le patch **agrandit SaveBlock1** et déplace les flags à +0x1130. Cette disposition est incompatible avec celle du fangame (flags @0xEE0) ;
    * les vérifications passent par la lecture des flags (deux blocs de 0x90 octets), des shops et du Pokédex, avec des gardes « dans l'overworld » (gMain + 0x38) et « SaveBlock non déplacé ».
* **Source C du patch :** `github.com/vyneras/pokefirered`, branches `archipelago-dev` (7b481d8, 2026-08-31) et `archipelago-merge`.
  * Fichiers ajoutés : `src/archipelago.c`, `include/archipelago.h`, `data/scripts/archipelago.inc`, `common_syms/archipelago.txt`.
  * Écart avec `master` : **930 fichiers, +64 041 / −28 497 lignes** [V].
  * **Licence :** aucun fichier LICENSE à la racine de ce fork, comme pour pret/pokefirered [V]. Le dépôt AP de Vyneras est sous MIT (en-tête LICENSE) [V].

  Conclusion [S] : il faut porter le *code* (archipelago.c et ses points d'accroche) dans le source du fangame, pas fusionner la branche entière.
* **Autres pistes [V] :** la recherche GitHub ne trouve que des miroirs (`sdwoodard/Archipelago`, copie de `frlg-stable`) et le tracker `vyneras/pokemon-frlg-tracker`. Aucune intégration AP pour un hack FRLG Yo-kai n'a été trouvée.

---

## 5. Architecture recommandée

### Option A : connecteur externe seul (prototype, ROM inchangée)
* **Émulateur :** mGBA 0.10.2 avec Lua. `libmgba` est liée à `liblua5.4` [V]. L'API `emu:read16` / `write16` et les sockets sont disponibles [S, non testés ici]. BizHawk reste possible via `worlds/_bizhawk`.
* **Client Python :** une sous-classe `BizHawkClient` ou un client mGBA maison, qui :
  1. lit `gSaveBlock1Ptr` et `gSaveBlock2Ptr` à chaque tick, car ils bougent au chargement ;
  2. lit les flags pour détecter les checks ;
  3. écrit les objets reçus directement dans les poches du sac ;
  4. tient un compteur d'objets reçus dans la sauvegarde.
* **Limites :**
  * l'objet vanilla de l'emplacement est quand même obtenu (pas de remplacement) ;
  * aucun message en jeu ;
  * donner un Yo-kai (structure Pokémon chiffrée et sommée) est possible mais complexe ;
  * les adresses sont propres à la version 1.0 du fangame et casseront à chaque mise à jour.

### Option B : patch de jeu (intégration complète, recommandée à terme)
* Porter dans **le source du fangame** :
  * la variable `gArchipelagoReceivedItem` et sa distribution dans l'overworld (`archipelago.c`) ;
  * les objets AP ;
  * la table d'emplacements, en remplaçant les `finditem`/`giveitem` par des emplacements AP ;
  * `gArchipelagoInfo` (auth) ;
  * un compteur en sauvegarde.
* Fournir un patch `.apfirered`-like dont la base est la ROM « Yo-kai Watch GBA 1.0 » (MD5 `72ad2cd5…`). Le monde AP aura son propre jeu de données (cartes, flags, Yo-kai), extrait du source.
* Sans le source, une option B « binaire » reste théoriquement possible : patcher les ID d'objets dans les scripts et insérer une routine ARM/Thumb de réception dans l'espace libre. Mais la ROM est pleine (32 Mio presque entièrement utilisés) [V], et chaque version du fangame casserait le patch. Cette voie est **déconseillée**.

---

## 6. Prototype minimal proposé (option A)

Adresses du fangame v1.0 :
* **[V]** = déduites du binaire puis confirmées en exécution dans un état mGBA au menu principal (`scratchpad/frtools/mgbastate.py`) ;
* **[V-stat]** = déduites statiquement, confirmées seulement par plusieurs références concordantes.

| Symbole | Vanilla | Fangame | Statut |
|---|---|---|---|
| `gSaveBlock1Ptr` | 0x03005008 | **0x03005568** (valeur à l'exécution : 0x02025608) | [V] |
| `gSaveBlock2Ptr` | 0x0300500C | **0x0300556C** (valeur : 0x02024664) | [V] |
| `gPokemonStoragePtr` | 0x03005010 | 0x03005570 (valeur : 0x020293F0) | [V] |
| `gMain` (`callback2` à +4) | 0x030030F0 | **0x03003650** (au menu : callback2 = 0x0800C2E5) | [V] |
| `CB2_Overworld` (valeur de `callback2` en jeu) | 0x080565B5 | **0x08058DB1** (pool de `CB1_Overworld` à 0x08058CB4) | [V-stat] |
| `sGlobalScriptContextStatus` (2 = aucun script) | 0x03000EA8 | 0x03000EA8 | [V-stat] |
| `gQuestLogState` (0 = pas de rejeu de journal) | 0x0203ADFA | 0x0203AE82 | [V-stat] |
| `gPaletteFade` | 0x02037AB8 | 0x02037B40 | [V-stat] |

1. **Événement réel à détecter : premier badge.**
   * `FLAG_BADGE01_GET` = 0x820, dans `[SB1 + 0xEE0 + 0x104]`, bit 0, soit `SB1 + 0xFE4` bit 0 ;
   * ou `FLAG_DEFEATED_BROCK` = 0x4B0, soit `SB1 + 0xF76` bit 0.

   Le script d'arène du fangame pose bien ces deux flags [V]. Autres checks possibles, avec les mêmes formules :
   * objets cachés : `FLAG_HIDDEN_ITEMS_START` = 0x3E8, 183 objets inchangés [V] ;
   * dresseurs : 0x500 + id.
2. **Donner un objet sans modifier la ROM.**
   * **Garde :** `callback2 == 0x08058DB1`, `sGlobalScriptContextStatus == 2`, `gQuestLogState == 0`, et pointeur SB1 stable avant et après l'écriture.
   * **Poche :** l'octet `pocket` (+26) de l'entrée `gItems` (0x0840B070 + id × 44) donne la poche (1 = Objets, 2 = Objets rares, 3 = Balls, 4 = CT/CS, 5 = Baies). Les poches sont à `SB1` + 0x310 / 0x3B8 / 0x430 / 0x464 / 0x54C (42 / 30 / 13 / 58 / 43 emplacements).
   * **Écriture :** chaque emplacement contient `{u16 itemId, u16 quantity ^ (u16)encryptionKey}`, avec `encryptionKey` = `*(u32*)(SB2 + 0xF20)`. On cherche l'emplacement du même ID ou le premier vide, on écrit la quantité chiffrée, puis on incrémente le compteur.
   * Le compteur et le sac sont dans le même SaveBlock1. Un reset sans sauvegarde les remet donc en arrière ensemble, et le client renverra l'objet : pas de perte et pas de doublon [S, logique à tester].
3. **Éviter les doublons : compteur en sauvegarde.**
   * Proposition : variable `VAR_0x409E`, inutilisée dans le source vanilla. Elle se trouve à `SB1 + 0x1000 + 0x9E × 2` = `SB1 + 0x113C`.
   * Aucun motif `setvar`/`addvar`/`compare`/`copyvar` ne la mentionne dans la ROM vanilla ni dans le fangame [V-stat, heuristique]. Mêmes résultats pour 0x409F, 0x40C5, 0x40C9, 0x40CA.
   * Alternative : `berryBlenderRecords` / `unused_632` (SB1 + 0x62C, 12 octets inutilisés en vanilla, sauvegardés).
   * Il faut confirmer avec le source que le fangame n'utilise pas ces octets [S].
   * Logique : `if compteur < len(items_received) and garde : donner items_received[compteur], compteur += 1`.
4. **Zone de RAM libre.** Elle n'est pas nécessaire en option A, puisqu'aucun code du jeu ne lirait une boîte aux lettres. En option B, le build ajoute naturellement une variable EWRAM, comme `gArchipelagoReceivedItem` chez Vyneras. Aucune zone « libre » sûre n'a été garantie dans ce binaire. Les octets EWRAM non référencés ne peuvent pas être prouvés libres sans le `.map` du fangame [S].
5. **Test proposé (non exécuté, pour ne pas jouer l'aventure) :**
   * charger une sauvegarde de l'utilisateur, déjà après Argenta ;
   * vérifier le bit `SB1 + 0xFE4` ;
   * injecter une Potion (ID 13, poche 1) ;
   * ouvrir le sac et vérifier ;
   * sauvegarder, recharger, puis contrôler `SB1 + 0x113C`.

---

## 7. Ce qui est demandé à l'utilisateur

1. **Le code source du fangame**, c'est-à-dire le dépôt de décompilation pokefirered modifié avec son historique git si possible, ou au minimum le `.map` / `.elf` de la build 1.0. Il est nécessaire pour trois raisons précises :
   * **Remplacer les objets d'emplacement :** il faut modifier les scripts `finditem`/`giveitem`/`setflag`, ce que l'on fait proprement dans `data/maps/*/scripts.inc` et non par patch binaire d'une ROM pleine.
   * **Ajouter le code de réception :** distribution d'objets et de Yo-kai avec message, compteur en sauvegarde, auth du slot. Ce code s'insère en C (port de `archipelago.c`) et oblige à recompiler.
   * **Extraire des données fiables pour l'apworld :** liste exacte des flags réellement utilisés par les nouveaux scripts (27 nouveaux flags d'objets mesurés), vars libres, nouvelle carte, logique de progression. Sans le source, ces données restent des heuristiques à chaque version.

   Sans source, on reste limité au prototype de l'option A.
2. **L'autorisation de l'auteur** pour distribuer un patch dérivé, si l'utilisateur n'est pas l'auteur, et des précisions sur sa licence.
3. **Une sauvegarde `.sav` existante**, idéalement juste avant et juste après le premier badge, pour tester le prototype sans jouer l'aventure.
4. **Le choix de l'émulateur cible** : mGBA (Lua) ou BizHawk (client AP existant).

---

## 8. Distinction vérifié / supposé (récapitulatif)

**Vérifié [V] :**
* identité de la ROM ;
* build de décompilation agbcc (décalages progressifs, fonctions identiques déplacées, RAM déplacée) ;
* absence d'expansion d'espèces et d'objets ;
* comptes d'espèces, rencontres, dresseurs, cartes, objets cachés et types ;
* flags de badge posés par les scripts ;
* tailles de SaveBlock identiques ;
* adresses `gSaveBlock1Ptr` / `gSaveBlock2Ptr` / `gMain` confirmées à l'exécution ;
* démarrage de la ROM ;
* hash, patch, client et mécanisme d'objets du monde AP de Vyneras ;
* absence de LICENSE dans le fork pokefirered ;
* présence de Lua dans mGBA.

**Vérifié statiquement [V-stat] :** `CB2_Overworld`, `sGlobalScriptContextStatus`, `gQuestLogState`, et les variables candidates sans motif de script.

**Supposé [S] :**
* origine de la zone 0x740000–0xCB0000 ;
* nombre exact de chansons ;
* format interne de la sauvegarde intact malgré la modification de `load_save.c` ;
* `VAR_0x409E` réellement libre dans le fangame ;
* comportement de l'injection directe dans le sac (non testé en jeu) ;
* API de sockets Lua de mGBA pour le connecteur.

### Outils et traces (scratchpad, hors dépôt)
`/tmp/claude-0/-home-user-Pokemon-Yokai-Watch/ccc78bc9-687a-5103-9a24-ee08d8d8b309/scratchpad/` :
* `frtools/` : `funcmatch.py`, `objgrowth.py`, `rammap.py`, `rommap.py`, `content.py`, `mapevents.py`, `gym.py`, `mgbastate.py`, `mapsyms.py`, ainsi que les sorties `rammap.txt`, `rommap.txt` et `objgrowth.txt` ;
* `frlg_ref/` : build vanilla de référence ;
* `frlg_ap/` : clones de Vyneras ;
* `frlg_run/` : exécution mGBA et état.
