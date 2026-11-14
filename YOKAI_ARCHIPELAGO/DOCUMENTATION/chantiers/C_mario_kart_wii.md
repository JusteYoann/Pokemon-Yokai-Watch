# Chantier C : Mario Kart Wii × Yo-kai Watch (Archipelago, Dolphin, Windows)

Date de la recherche : 2026-11-14. Référence Archipelago : clone local `ArchipelagoMW/Archipelago` à `f5b97c5e` (2026-11-06), `Utils.__version__ = "0.6.9"`.

Légende utilisée partout :
- **[VÉRIFIÉ-CODE]** : lu dans le code ou le README d'un dépôt cloné pendant cette recherche.
- **[ANNONCÉ]** : seulement vu dans une page de releases, un extrait de moteur de recherche ou une documentation tierce, sans lecture du code ni de la page source.
- **[NON TROUVÉ]** : cherché, rien trouvé.
- **[NON VÉRIFIÉ]** : pas pu contrôler (réseau bloqué ou test refusé).

---

## 1. Résumé (verdict)

**C'est faisable, avec une seule base sérieuse : `toent/Archipelago-MKWii`.** Ce dépôt contient un apworld `mkwii` (v0.4.0) et un client Python autonome qui passe par `dolphin_memory_engine`. Il vise **uniquement la version PAL (`RMCP01`)**. Le jeu n'est pas patché : le client lit et écrit la RAM de Dolphin en direct, et touche aussi le fichier de sauvegarde `rksys.dat`.

**Les personnages Yo-kai peuvent cohabiter avec cette intégration**, à trois conditions :
1. le mod se limite à remplacer des fichiers (`.szs`/`.brres`/`.tpl`), sans code injecté ;
2. le mod est chargé par Riivolution dans Dolphin (fichiers remplacés par nom, l'ID reste `RMCP01`) ou intégré dans une image PAL reconstruite **en gardant l'ID `RMCP01`** ;
3. on n'utilise **aucun** pack à code (Retro Rewind, CTGP-R, MKW-SP, packs Pulsar). Ces packs injectent du code et changent la mémoire et la sauvegarde que le client attend.

Il reste deux réserves :
- Le verrouillage visuel « ? » du client repère les icônes vanilla par leur SHA-256. Un mod qui remplace l'icône de Luigi ou de Toadette rend ce verrou visuel inopérant pour ce personnage. Le blocage en jeu, lui, continue de fonctionner, car il passe par l'ID du personnage.
- Aucune page de mod Yo-kai n'a pu être lue : gamebanana.com, mkwiiki.org, wiki.tockdom.com et youtube.com sont bloqués par le proxy de cette session. Les informations sur les mods sont donc toutes **[ANNONCÉ]**, tirées d'extraits de moteur de recherche.

**Meilleure base : `toent/Archipelago-MKWii` (v0.4.0, licence MIT héritée d'Archipelago), plus un mod Yo-kai de type remplacement de fichiers chargé par Riivolution « My Stuff » sur une image PAL `RMCP01`.**

---

## 2. Intégrations Archipelago trouvées

| Dépôt | Commit / date | Licence | État vérifié | Version du jeu | Méthode |
|---|---|---|---|---|---|
| [toent/Archipelago-MKWii](https://github.com/toent/Archipelago-MKWii) | `a8949c5f9261bc70112c2e5336d91bfa0dc3c475`, 2026-11-09 (clone `--depth 1`) | MIT (fichier `LICENSE` d'Archipelago à la racine du fork, aucune licence propre à `worlds/mkwii`) | **[VÉRIFIÉ-CODE]** : apworld complet (`worlds/mkwii`, `archipelago.json` world_version 0.4.0, minimum_ap_version 0.6.6) et client `worlds/mkwii/MKWii Client/` (env. 10 000 lignes en tout) | **PAL `RMCP01` seulement.** Les adresses NTSC valent toutes `0x00000000` dans `dme_addresses.py`, et le client refuse tout autre ID (`dolphin_memory.py` l. 381-387). Pas de vérification de hash de l'ISO, seulement l'ID en RAM. | Pas de patch ISO, pas de Riivolution, pas de Gecko. Lecture et écriture de la RAM par `dolphin_memory_engine`, plus quelques écritures de code PowerPC en RAM (voir 2.1), plus remplacement de `rksys.dat` par une sauvegarde vide fournie. |
| « Manual: Mario Kart Wii » (0.0.1+magnetico) | — | — | **[ANNONCÉ]** par un extrait de recherche sur une liste de lobby AP (ap-lobby.ionium.us, bloqué ici). Aucun dépôt trouvé sur GitHub. | — | Un world « Manual » se coche à la main, sans client. |
| Index communautaire [silasary/apworlds](https://github.com/silasary/apworlds) | `07a0c72f`, 2026-11-14 | — | **[VÉRIFIÉ-CODE]** : `index/mkwii.json` pointe vers `toent/Archipelago-MKWii` et c'est la seule entrée Mario Kart Wii (les autres sont MK64, Double Dash, MK7, MK8DX, MK World) | — | — |
| Autres (CTGP/MKW-SP + AP, NTSC) | — | — | **[NON TROUVÉ]** avec les recherches GitHub `search/repositories` et `search/code` (« mario kart wii archipelago », « mkwii ap », « RMCP01 dolphin_memory_engine », etc.) ni sur le web | — | — |

À noter : les mondes AP voisins (Double Dash `aXu-AP/archipelago-double-dash`, MK DS, MK8DX) existent, mais ils concernent d'autres jeux.

### 2.1 Détail de `toent/Archipelago-MKWii` [VÉRIFIÉ-CODE sauf mention contraire]

- **Activité** : dernier commit le 2026-11-09. Releases v0.2.0 à v0.4.0 entre avril et novembre ; v0.4.0 date du 09 Nov et elle est marquée Latest [ANNONCÉ, page Releases lue par WebFetch]. L'API GitHub du dépôt est refusée à cette session (403), le clone public a fonctionné.
- **Base AP du fork** : `Utils.__version__ = "0.6.7"`. L'apworld déclare `minimum_ap_version: 0.6.6`, il devrait donc se charger sous 0.6.9 **[NON VÉRIFIÉ]**. Un test de génération sur une copie de 0.6.9 a été refusé par la politique de permissions de la session.
- **Prérequis (README)** : un ISO PAL **non modifié**, Dolphin 2512+ (minimum 5.0-3981), « Enable Memory Size Override » désactivé, Python 3.13 sous Linux. Sous Windows on lance `mkwii_client.exe` (PyInstaller). Les releases contiennent 4 fichiers chacune, dont le nom n'a pas pu être lu.
- **Client** : `MKWii Client/mkwii_client.py`. Il s'appuie sur `CommonClient` d'AP mais **n'est pas** un composant du Launcher (`worlds/LauncherComponents.py` ne cite pas mkwii). Il a sa propre console, un tracker séparé (`tracker_process.py`) et un DeathLink (chute hors piste).
  - Accroche : `dme.hook()`, puis lecture de `0x80000000` (6 octets) qui doit valoir `RMCP01`.
  - Pointeurs PAL fixes : `SYSTEM_MANAGER_PTR 0x809BD748`, `RACE_CONFIG_PTR 0x809BD728`, `RACE_MGR_PTR_ADDR 0x809BD730`, etc. Ensuite le client suit des chaînes d'offsets.
  - Déblocages : écrits **à la fois** dans la structure runtime (`manager+0x9034`, pas de 0x93F0 par licence) et dans le tampon `rksys` en RAM. Les commentaires disent « verified against 25 progressive PAL save snapshots ».
  - Blocage des déblocages vanilla : le client **écrit du code en RAM**, `li r3,-1; blr` à `0x80854FA4`, ou à défaut `li r3,-1` à `0x805EB920`. Ce point dépend du code PAL d'origine.
  - Persos, coupes et véhicules par défaut (sans bit de sauvegarde) : le client réécrit `RaceConfig+0xC24` (perso) et `+0xC20` (véhicule) avant le chargement de la course, et redirige la coupe ou gèle le tour.
  - Verrou visuel « ? » (`menu_lock.py`, `icon_assets.py`) : le client cherche en MEM2 les textures d'icônes **vanilla** grâce aux SHA-256 de `icon_manifest.json` (`"game": "RMCP01"`, 12 persos par défaut et 4 coupes de base), les capture la première fois dans `bins/`, puis écrit la texture « ? » par-dessus.
  - Seule la licence en haut à gauche est prise en charge.
  - Avertissements du README : ne pas utiliser l'accélération de Dolphin (des checks sautent) ; le client se décroche parfois (`/hook`, `/status`).
- **Checks (locations)**, `locations.py` :
  - 8 coupes × 4 cylindrées (50/100/150/Miroir) × 6 paliers (3e, 2e, 1re place, 1, 2 et 3 étoiles), soit 192 ;
  - 32 courses × 4 cylindrées « 1st Place », soit 128 ;
  - total brut 320, filtré par les options `enabled_ccs`, `enabled_cup_check_tiers` et `include_race_checks`. Les courses se valident aussi en VS.
  - Contre-la-montre : **pas implémenté** (prévu d'après le README).
- **Objets**, `items.py` :
  - 32 déblocages coupe × cylindrée ;
  - 2 modes (karts/motos 50cc et 100cc) ;
  - 14 persos à bit de sauvegarde (Bébé Daisy … Mii A/B) et 12 persos par défaut (Mario, Luigi, …, avec `lock_default_characters`, actif par défaut) ;
  - 18 karts et 18 motos (dont 9+9 par défaut) ;
  - 18 déblocages d'objets de course ;
  - 14 objets de remplissage (un objet donné en course) ;
  - 6 pièges, présents dans les données mais **non gérés par le client** (`enable_traps` doit rester à false) ;
  - « Victory Trophy ».
- **Victoire** (`rules.py`, `__init__.py`) : des « Victory Trophy » sont placés d'avance sur le palier et la cylindrée choisis, pour chaque coupe (`goal_difficulty`, défaut 1 étoile ; `goal_cc`, défaut Miroir). Il faut en posséder `cups_required_for_goal` (défaut 6) pour obtenir « Victory ».
- **État de test** : selon le README, « Fully completable from start to finish » [ANNONCÉ]. Problèmes connus en v0.4.0 : affichage et verrouillage des Mii, et environ 0,5 s de retard d'affichage à l'écran des véhicules [ANNONCÉ]. Les notes de v0.3.2 disent que le NTSC n'est pas pris en charge et que l'auteur n'a pas de copie NTSC [ANNONCÉ].

---

## 3. Mods Yo-kai pour Mario Kart Wii

Aucune page n'a pu être lue : `gamebanana.com`, `api.gamebanana.com`, `web.archive.org`, `youtube.com`, `mkwiiki.org` et `wiki.tockdom.com` sont refusés par le proxy (connect_rejected / ENOTFOUND). Tout ce qui suit vient des titres et extraits renvoyés par WebSearch : **[ANNONCÉ]**. Format, région et conditions d'utilisation restent **[NON VÉRIFIÉ]**.

| Mod | Perso remplacé | Format | Auteur | Conditions d'utilisation | Région | Source |
|---|---|---|---|---|---|---|
| **Jibanyan in Mario Kart Wii 5.0** (GameBanana 413572) | **Luigi** (catégorie « Luigi ») [ANNONCÉ] | [NON VÉRIFIÉ], probablement des `.szs` de remplacement (voir 4) | EvesNotCool [ANNONCÉ] | [NON VÉRIFIÉ] | [NON VÉRIFIÉ] | extrait WebSearch ; une vidéo YouTube « Jibanyan in Mario Kart Wii 3.0 (Download) » renverrait vers cette page |
| **Jibanyan! (With Custom Animations)** (GameBanana 653194) | **Toadette** [ANNONCÉ] | [NON VÉRIFIÉ] | EnmanuTM [ANNONCÉ] | [NON VÉRIFIÉ] | [NON VÉRIFIÉ] | extrait WebSearch |
| **Yokai Watch Mario Kart Wii Menus and Icons** (GameBanana 455364) | aucun (catégorie Other/Misc : menus et icônes) [ANNONCÉ] | [NON VÉRIFIÉ], sans doute des `Scene/UI/*.szs` | EvesNotCool [ANNONCÉ] | [NON VÉRIFIÉ] | [NON VÉRIFIÉ] | extrait WebSearch |
| Komasan, Whisper, USApyon, etc. | — | — | — | — | — | **[NON TROUVÉ]** |
| (hors sujet) Ultimate Yo-Kai Watch Character Pack (GameBanana 455480) | — | — | — | — | — | c'est pour **Mario Kart 7**, pas Wii [ANNONCÉ] |

Format habituel des mods de personnages MKW [VÉRIFIÉ-CODE, README et `install.sh` de `KoJesko/mkw-costume-installer`, MIT, `948f0ddf`, 2026-10-14] : dossiers `Race/` (modèles par véhicule `<kart>-<code>.szs`), `Driver/`, `Award/<code>.brres`, `Icons/` et `Voices/`, plus `<code>-allkart.szs` (véhicules de l'écran de sélection). Selon ce même README :
- « My Stuff » remplace les fichiers **par nom, seulement les noms présents sur le disque retail » ;
- un modèle ne peut aller que sur le personnage pour lequel il a été riggé ;
- les modèles sont identiques d'une région à l'autre (PAL, NTSC…).

---

## 4. Compatibilité mods × Archipelago

| Point | Analyse | Statut |
|---|---|---|
| ID du jeu | Le client exige `RMCP01` en `0x80000000`. Riivolution sous Dolphin (« Start with Riivolution patches ») garde l'ID du disque. Une image reconstruite avec Wiimms ISO/SZS Tools doit **garder** `RMCP01` (pas d'ID de mod du type `RMCP12`). | analyse à partir du code [VÉRIFIÉ-CODE] ; comportement de Dolphin et Riivolution [ANNONCÉ] |
| Adresses de code statiques | Le client écrit dans le code à `0x80854FA4` / `0x805EB920` et lit des pointeurs fixes en `0x809B…` / `0x809C…`. Un mod qui ne remplace que des modèles ou textures ne touche pas `main.dol` ni `StaticR.rel`, donc rien ne bouge. **Incompatibles** : les packs qui injectent du code. Par exemple le XML Riivolution d'OptPack (pack Pulsar, [VÉRIFIÉ-CODE] `Optllizer/OptPack` `8a288bf4`) contient des `<memory offset="0x80242698" …>` et charge `Loader.pul` en `0x80004000`. Retro Rewind, CTGP-R et MKW-SP sont dans le même cas. | [VÉRIFIÉ-CODE] |
| Pack « costume » Retro Rewind | `mkw-costume-installer` installe **dans Retro Rewind**, donc **pas utilisable** avec l'AP. | [VÉRIFIÉ-CODE] |
| Sauvegarde | Le client remplace `rksys.dat` (dossier de sauvegarde Wii de Dolphin, titre `RMCP`) par une sauvegarde vide et lit et écrit le tampon `rksys` en RAM. Un mod qui ne fait que remplacer des fichiers ne change pas la sauvegarde. Les packs Pulsar redirigent la sauvegarde (option « savetosd… » dans OptPack), donc conflit. | [VÉRIFIÉ-CODE] |
| Identité des personnages | Jibanyan sur Luigi reste l'ID `0x07` « Luigi » pour l'AP. L'objet AP s'appellera « Luigi », pas « Jibanyan ». Il faut une table de correspondance côté joueur ou tracker (renommer dans l'apworld = fork). Jibanyan sur Toadette correspond à l'objet « Toadette » (perso à bit de sauvegarde). | [VÉRIFIÉ-CODE] (`mkwii_info_lib.CHARACTER_ID_TO_NAME`) |
| Verrou visuel « ? » | `icon_manifest.json` contient les SHA-256 des icônes **vanilla** des 12 persos par défaut, dont **Luigi**. Si le mod remplace l'icône de Luigi, la capture ne la trouve jamais et le « ? » ne s'affiche pas sur Jibanyan. Le client émet alors un simple avertissement (`icon_assets.py` l. 141-175). Le **blocage réel** (réécriture de `RaceConfig+0xC24`) fonctionne toujours. Toadette n'est pas dans le manifeste : son verrou passe par le bit de sauvegarde, il n'y a pas de problème. | [VÉRIFIÉ-CODE] |
| Mod « Menus and Icons » | S'il remplace des `Scene/UI/*.szs`, le verrou visuel des **véhicules** cherche les panes nommées (`hatena`, `chara`, …) en MEM2. Un layout modifié qui renommerait ces panes casserait cet affichage, mais pas le blocage. Contenu du mod inconnu. | [NON VÉRIFIÉ] |
| Mémoire | Un modèle custom plus lourd peut faire planter le jeu (problème de mod, pas d'AP). Le client exige « Memory Size Override » **désactivé**. | [ANNONCÉ] (README) |
| Deux mods Jibanyan | Luigi (413572) et Toadette (653194) ne se gênent pas (fichiers différents), mais on aurait deux Jibanyan. Une seule entrée suffit. | analyse |

---

## 5. Checks et objets possibles

- **Déjà disponibles dans toent** (voir 2.1) : podiums et étoiles par coupe, cylindrée et palier ; 1re place par course et cylindrée. Objets : coupes, persos, véhicules, objets de course, remplissage.
- **Annoncés comme prévus par l'auteur** : contre-la-montre et pièges [ANNONCÉ].
- **Ajouts possibles pour le thème Yo-kai, dans un fork de l'apworld (pas obligatoires pour un prototype)** :
  - alias d'affichage (« Luigi » remplacé par « Jibanyan ») dans `items.py`, le tracker et `mkwii_info_lib.py`, en gardant les IDs ;
  - une option de départ qui force le perso Yo-kai comme perso de départ (le client gère déjà les persos de départ pré-donnés quand `lock_default_characters` est actif).
- **Hors de portée sans recherche RAM supplémentaire** : contre-la-montre, missions et Battle. Aucun pointeur n'est présent dans `dme_addresses.py`.

---

## 6. Prototype minimal proposé (PC Windows)

1. **Matériel** : une copie personnelle de Mario Kart Wii **PAL**, dumpée soi-même. Vérifier dans Dolphin (Propriétés, Info) que l'ID est `RMCP01`. Aucune image n'est fournie ici.
2. **Dolphin** : installer Dolphin 2512 ou plus récent (README toent). Dans Config, Advanced, décocher « Enable Memory Size Override ». Ne pas utiliser l'accélération ni les savestates pendant les essais.
3. **Sauvegarder** l'ancien `rksys.dat` : clic droit sur MKWii, « Open Wii Save Folder ».
4. **Archipelago 0.6.9** : copier `mkwii.apworld` (release v0.4.0 de toent) dans `custom_worlds/` de l'installation AP. Générer une partie solo avec un YAML qui laisse `enable_traps: false`. La compatibilité 0.6.9 est **à confirmer** à cette étape.
5. **Mod Yo-kai** : lire la page GameBanana 413572 (bloquée ici) pour connaître le format, la licence et la région. Si le mod fournit des `.szs` simples :
   - placer les fichiers dans `Dolphin Emulator/Load/Riivolution/` sous un XML qui ne fait **que** du remplacement de fichiers (`<folder external=… disc=…>` ou `<file …>`), sans aucun `<memory>` ;
   - ou utiliser un XML « My Stuff » minimal de ce type.

   Lancer avec un clic droit sur le jeu, « Start with Riivolution patches », pour vérifier que Jibanyan remplace Luigi.
6. **Contrôle d'ID** : en jeu, l'outil Dolphin Memory Engine (ou la commande `/status` du client) doit lire `RMCP01` en `0x80000000`.
7. **Client** : lancer `mkwii_client.exe` (release toent), choisir le `rksys.dat`, rester sur l'écran de sélection de licence, puis démarrer Dolphin **en mode Riivolution**, se connecter au serveur AP et utiliser la licence en haut à gauche.
8. **Tests de non-régression** :
   - finir une course en 50cc et vérifier que le check part ;
   - recevoir l'objet « Luigi » et vérifier que Jibanyan devient jouable ;
   - tant que l'objet manque, choisir Jibanyan et vérifier la redirection vers un perso autorisé ;
   - vérifier qu'aucun déblocage vanilla ne s'applique (patch `0x80854FA4`) ;
   - noter que le « ? » ne s'affiche pas sur l'icône de Jibanyan (attendu).
9. **Optionnel** : un petit fork de l'apworld qui renomme les objets pour l'affichage.

---

## 7. Blocages

1. **Mods non lus** : GameBanana, YouTube, MKWiiki, Tockdom et web.archive.org sont inaccessibles dans cette session. Format, licence et région des mods Yo-kai restent **[NON VÉRIFIÉ]**. Il faut autoriser `gamebanana.com` dans les réglages réseau de la session, ou lire les pages à la main.
2. **PAL seulement** : un ISO NTSC (`RMCE01`) ne marchera pas. Les adresses NTSC sont toutes à `0x0`.
3. **Packs à code exclus** : Retro Rewind, CTGP-R, MKW-SP et les packs Pulsar sont incompatibles avec le client (code injecté, sauvegarde redirigée). Les mods Yo-kai pensés pour ces packs (slots de costumes) ne conviennent pas.
4. **Verrou visuel** inopérant sur un personnage dont l'icône est remplacée. C'est cosmétique.
5. **Compatibilité AP 0.6.9 non testée** : le fork est en 0.6.7. L'exécution de `Generate.py` sur une copie 0.6.9 a été refusée par la politique de permissions.
6. **Client autonome** (pas de bouton dans le Launcher AP 0.6.9) : décrochages occasionnels de Dolphin d'après le README, Linux seulement avec Dolphin flatpak. Sans conséquence pour Windows.
7. **Licence des mods** : les modèles Yo-kai appartiennent à Level-5. Les conditions de redistribution sont inconnues, donc ne pas redistribuer les fichiers dans un dépôt du projet.

---

## 8. Principe du connecteur Dolphin dans Archipelago (référence TWW)

- `worlds/tww/TWWClient.py` [VÉRIFIÉ-CODE, AP 0.6.9] :
  - utilise `dolphin_memory_engine` (`worlds/tww/requirements.txt` : `dolphin-memory-engine>=1.3.0`), avec `hook()`, `is_hooked()`, `read_bytes`, `write_bytes` et `un_hook()` ;
  - contrôle l'ID `GZLE99` en `0x80000000`. C'est l'ID **modifié par le randomiseur TWW, qui patche l'ISO** ;
  - lit le nom de slot en RAM (`SLOT_NAME_ADDR 0x803FE8A0`) ;
  - donne les objets en écrivant dans un tableau en RAM (`GIVE_ITEM_ARRAY_ADDR`), qu'un code ajouté par le patch consomme ;
  - détecte les checks en lisant des champs de bits ;
  - le tout dans une boucle asynchrone qui se reconnecte (l. 640-691).
- **MKW (toent) prend une autre approche** : pas de patch ISO et ID vanilla `RMCP01`. Les objets sont des bits de déblocage écrits en RAM et dans le tampon de sauvegarde, les checks viennent du tampon GP de `rksys` et de `RaceManager`, et le seul code modifié l'est en RAM, à chaud (2 écritures). Avantage pour notre chantier : **aucun conflit avec un mod de fichiers chargé par Riivolution**, contrairement à une intégration qui imposerait son propre ISO patché.
- Pour aller plus loin (contre-la-montre, Battle, NTSC), il faudrait trouver de nouveaux pointeurs par comparaison de RAM, comme l'auteur l'a fait (« memory snapshot diffing »), et compléter `dme_addresses.py`.

---

## 9. Sources

Dépôts clonés et lus (copies locales sous `/tmp/claude-0/-home-user-Pokemon-Yokai-Watch/ccc78bc9-687a-5103-9a24-ee08d8d8b309/scratchpad/mkw_research/`) :
- https://github.com/toent/Archipelago-MKWii, commit `a8949c5f` (2026-11-09)
- https://github.com/toent/Archipelago-MKWii/releases (lu par WebFetch)
- https://github.com/silasary/apworlds, `index/mkwii.json`, commit `07a0c72f`
- https://github.com/KoJesko/mkw-costume-installer, commit `948f0ddf`
- https://github.com/Optllizer/OptPack, `OptPack/riivolution/optpack.xml`, commit `8a288bf4`
- Archipelago 0.6.9 (clone local), `worlds/tww/TWWClient.py`

Pages vues seulement en extrait de moteur de recherche (non ouvertes, accès bloqué) :
- https://gamebanana.com/mods/413572 (Jibanyan in Mario Kart Wii 5.0, Luigi, EvesNotCool)
- https://gamebanana.com/mods/653194 (Jibanyan! With Custom Animations, Toadette, EnmanuTM)
- https://gamebanana.com/mods/455364 (Yokai Watch Mario Kart Wii Menus and Icons, EvesNotCool)
- https://gamebanana.com/mods/455480 (pack Yo-kai pour Mario Kart 7, hors sujet)
- https://www.youtube.com/watch?v=AneiqBXzxUI (Jibanyan in Mario Kart Wii 3.0)
- https://wikiwiki.jp/gcwiiemu/Tips_Launch_Game_with_Riivolution (Riivolution intégré à Dolphin depuis 5.0-15407)
- https://newerteam.com/wii/help/dolphinriivo.html (procédure « Start with Riivolution patches »)
