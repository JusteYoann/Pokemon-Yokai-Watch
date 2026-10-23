#!/usr/bin/env python3
"""Produce the reviewable chapter report from the completed native/static checks."""
from pathlib import Path
import json,re,hashlib,subprocess
R=Path(__file__).resolve().parents[2];D=R/'docs/lavanville-zombie-night/finalisation'
def get(file):return json.loads((D/file).read_text())
audit=get('AUDIT_STATIQUE.json');public=get('public/TEST_MGBA.json');private=get('prive/TEST_MGBA.json');audio=get('prive/AUDIO_MGBA.json');finale=get('regressions/prive/FINALE_NORMALE_MGBA.json');patrols={m:get(m+'/PATROUILLES_MGBA.json') for m in ['public','prive']}
assert all(x['passed'] for x in [audit,public,private,audio,finale,*patrols.values()])
fonts={m:get(m+'/DIALOGUES_MGBA.json') for m in ['public','prive']}
roms={}
for mode,file in [('public','pokefirered.gba'),('prive','pokefirered_audio.gba')]:
 data=(R/file).read_bytes();sha=hashlib.sha256(data).hexdigest();report=public if mode=='public' else private;assert sha==report['rom_sha256']==patrols[mode]['rom_sha256']
 assert fonts[mode]['passed'] and sha==fonts[mode]['rom_sha256']
 if mode=='prive':assert sha==audio['rom_sha256']==finale['rom_sha256']
 text=(R/Path(file).with_suffix('.map')).read_text();ew=int(re.search(r'^ewram\s+0x\w+\s+(0x\w+)',text,re.M)[1],16);iw=int(re.search(r'^iwram\s+0x\w+\s+(0x\w+)',text,re.M)[1],16)
 assert len(data)<=33554432 and ew<=262144 and iw<=32768
 roms[mode]=dict(bytes=len(data),sha256=sha,remaining_rom_bytes=33554432-len(data),ewram=ew,iwram=iw,chapter_checks=len(report['results']))
code_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip()
metadata=dict(branch='feature/lavanville-zombie-night',base='7110ce41b',implementation_commit=code_commit,roms=roms,static_audit_passed=True,native_font_lines={m:fonts[m]['lines_checked'] for m in fonts},protected_branches=audit['protected_branches'],all_original_151_data_and_encounters_preserved=True,all_selected_sprite_pngs_identical=True,unchanged_audio_streams=30,changed_audio_track=14,native_patrol_replays_pass=True,native_finale_eight_forms_hof_continue_pass=True,limitations=['Whole-track Zombie Night repetition retains the source fade-out and silence; seamless musical loop and human listening are not validated','Functional battle scenarios use a boosted QA party; no full normal-difficulty adventure or human balance playtest is claimed','Map/script entry fixtures are identified in each test; native route replays use controller input without position patches','Future rematch is condition-only: no rematch team is invented','No general all-city, all-move or all-menu exhaustive regression is claimed'])
(D/'VALIDATION.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2)+'\n')
def team_line(t):return ' / '.join(f"{m['name']} {m['level']}" for m in t)
team_rows='\n'.join('| '+k.replace('sYokaiParty_CHANNELER_','').replace('sLavenderSummit','Sommet ')+ ' | '+team_line(t)+' |' for k,t in audit['tower_teams'].items())
leader_rows='\n'.join('| '+str(i+1)+' | '+m['name']+' | '+str(m['species'])+' | '+str(m['level'])+' | '+', '.join(v['name'] for v in m['moves'])+' |' for i,m in enumerate(audit['alyzon']))
rom_rows='\n'.join('| '+m+' | '+str(v['bytes'])+' | '+str(v['ewram'])+' | '+str(v['iwram'])+' | `'+v['sha256']+'` |' for m,v in roms.items())
readme=f'''# Lavanville / Tour Pokémon / Alyzon Bie — chapitre intégré

Branche **feature/lavanville-zombie-night**, base `7110ce41b`, commit d'implémentation `{code_commit}`. Aucune fusion sur master ou sur les branches audio, Mafiamille et Don Spiraton. [Demande de référence](DEMANDE.md), [validation structurée](VALIDATION.json), [audit de préservation et équipes complètes](AUDIT_STATIQUE.json), [liste des fichiers](FICHIERS_MODIFIES.txt).

## Ce qui fonctionne

Lavanville est en nuit permanente dès son chargement, avec brume verte native translucide, animée lentement. La teinte s'applique seulement à la sortie matérielle des palettes de terrain : aucun cumul dans les couleurs source, aucun filtre imposé aux écrans de Sac/équipe. Les fenêtres de dialogue et les couleurs des personnages sont conservées. La sortie vers une route ou un intérieur rétablit les effets prévus pour sa carte ; la Tour conserve sa brume blanche d'origine aux étages3–7.

Quatre errants utilisent la marche validée et leurs quatre images de combat existantes. Le premier suit six cases précises loin des portes ; le sprinteur parcourt les cases12–16 de sa rangée, le colosse surveille un passage, le spectral erre dans une zone bornée. Les maisons1 et de l'ancien refuge abritent aussi des zombies. Les habitants ordinaires sont remplacés, tout en gardant les services du Centre, de la Boutique et du spécialiste des surnoms. Les combats directs ne peuvent être capturés ni fuis, se terminent par K.O., ne retirent pas le PNJ et restent répétables. Une immunité temporaire couvre les sorties de combat et les entrées dans la ville ou ses maisons infestées.

La Tour conserve sept étages, ses objets, ses rencontres sauvages ordinaires et sa zone de soin. Les Yo-kai sauvages restent identifiables, capturables et fuyables sans Scope. Les treize équipes existantes des étages3–6 sont conservées. Les trois combats du sommet reçoivent des enregistrements distincts : les équipes Mafiamille partagées ne changent pas. Les seize zombies Dresseurs utilisent tous le même overworld, restent visibles, et leur victoire n'est pas réinitialisée. Les approches des escaliers4F et6F imposent un combat chacune, une seule fois, indépendamment de la position du PNJ.

L'introduction d'Alyzon est déclenchée automatiquement une seule fois. Le placement s'adapte à l'entrée utilisée : un zombie approche, Alyzon se place entre lui et le joueur, se tourne vers lui, puis vers le joueur après son départ. Elle explique la Zombie Night, présente son badge, évoque le visiteur discret sans nommer Matt, puis rejoint la Tour par un chemin calculé sur les collisions. Les contrôles sont rendus et le flag est sauvegardé. Si une ancienne sauvegarde reprend dans un emplacement sans place pour les trois cases de scène, les dialogues restent accessibles sans bloquer le joueur ; les quatre arrivées usuelles testées jouent toute la scène.

Au sommet, Alyzon est une vraie Championne du moteur, présentée comme **CHAMPIONNE ALYZON BIE**. Sa victoire remet le quatrième badge existant et conserve ses effets, dont FORCE et les conditions des huit badges. La CT19 reste disponible, avec reprise du don si le Sac est plein. Mémogre reste réservé pour la fin, y compris dans la sélection de remplacement et les changements forcés.

L'ancienne Arène de Céladopole est sa résidence : Matt avant le badge, Alyzon ensuite, sans combat. La future revanche exige à la fois le flag de Ligue et une entrée au Panthéon ; seul un dialogue d'attente est prévu, sans inventer d'équipe.

Le passage du Casino est verrouillé avant le badge, y compris pour un ancien interrupteur déjà ouvert. Le repaire, ses sbires, Don Morléone, ses équipes et ses musiques sont conservés. La récompense du Scope devient la **FLÛTE YO-KAI**. Une ancienne sauvegarde où Don est vaincu et le Scope déjà pris retrouve la récompense si la Flûte manque. Le flag de réveil n'est fixé qu'après obtention réelle de l'objet. Les deux Misterre des Routes12/16 gardent leurs mécaniques natives et sont réveillables. Le garde de Safrania dépend désormais de cette étape plutôt que du sauvetage supprimé de Fuji.

Fuji est retiré des objets, du don de Flûte, du sommet et des dialogues accessibles du chapitre. Sa fiche n'est plus affichée par le Mémorydex/Fame Checker ; son ancien emplacement de sauvegarde reste réservé. Les photos accessibles du laboratoire ne le réintroduisent plus. La fiche d'Erika devient celle d'Alyzon. Les labels et flags historiques encore utiles restent stables ; les reprises sur les cartes refondues rechargent les bons modèles et remplacent aussi les anciens acteurs sérialisés, au lieu de restaurer les humains/Fuji.

## Ressources et code

Aucun sprite validé n'est redessiné. L'audit vérifie l'identité des PNG avec la base avant ce chapitre.

| Élément | Ressource / code |
|---|---|
| Alyzon, carte et portrait | `graphics/yokai_characters/alyzon/` ; IDs173 et160 |
| Zombies, marche commune | `graphics/yokai_zombies/errant/overworld.png` ; ID174, banque8 |
| Quatre images de combat | `graphics/yokai_zombies/{{errant,sprinteur,colosse,spectral}}/battle-front.png` |
| Portrait des zombies Dresseurs | image existante de l'errant, ID161 |
| Scène, adversaires directs, palettes et compatibilité | `src/lavanville.c`, `include/lavanville.h` |
| Ambiance | `src/overworld.c`, `src/field_weather*.c`, carte LavenderTown |
| Badges, résidence, Flûte, gardes et escaliers | scripts et événements des cartes concernées |
| Équipes et portrait de Championne | `src/data/trainers.h`, `src/data/trainer_parties.h` |
| Capture/fuite et apparence des errants | hooks dédiés dans le moteur de combat ; aucun fichier de statistiques des151 modifié |

Les adversaires directs utilisent un gabarit interne de Pokémon existant, avec statistiques propres à l'instance et apparence limitée au combat zombie. Ils ne constituent pas de nouvelles entrées capturables au Médallium. Le gabarit n'est pas marqué comme vu par ces rencontres. Les banques de palette de reflet7/8 sont réservées aux personnages du chapitre ; une future scène cumulant ces PNJ et des reflets d'eau concurrents devra revoir cette allocation.

## Équipes

Les données détaillées, types, statistiques de base et capacités se trouvent dans l'audit JSON. Les noms abrégés ci-dessous sont ceux des151 dans la ROM.

| Ordre | Yo-kai | ID | Niveau | Capacités légales au niveau demandé |
|---|---|---:|---:|---|
{leader_rows}

Triptic-tac est bien l'ID44 (`SPECIES_GLOOM`), et non Télémir43. Les quatre sont déjà de type Spectre ; aucun type n'a changé. L'ordre d'envoi0→1→2→3 est observé dans le vrai combat.

| Zombie Dresseur / ancien ID conservé | Équipe |
|---|---|
{team_rows}

Les errants sont au niveau24, de type Spectre. Statistiques finales propres au combat :

| Variante | PV | Attaque | Défense | Vitesse | Att. Spé. | Déf. Spé. |
|---|---:|---:|---:|---:|---:|---:|
| Errant |85|50|45|28|35|40|
| Sprinteur |70|54|34|72|32|36|
| Colosse |110|62|62|19|28|42|
| Spectral |78|30|35|48|55|62|

Cette répartition distingue vitesse, résistance et attaque spéciale, sans toucher aux151. Les épreuves fonctionnelles ne constituent pas une validation humaine d'équilibrage en difficulté normale.

## Dialogues définitifs

[Transcription](DIALOGUES.md). Les nouveaux dialogues sont en français, avec pages de deux lignes. Chaque ligne est mesurée par la vraie police GBA : contrôle de208 pixels maximum. Les119 lignes littérales modifiées sont aussi vérifiées séparément : [publique](public/DIALOGUES_MGBA.json), [privée](prive/DIALOGUES_MGBA.json). Les textes des services et du rival qui ne changent pas de rôle restent ceux du projet.

## Compilation et mémoire

| Version | Octets ROM | EWRAM | IWRAM | SHA-256 |
|---|---:|---:|---:|---|
{rom_rows}

Limites : ROM33554432 octets, EWRAM262144, IWRAM32768. Les valeurs EWRAM/IWRAM restent celles de la base. La brume utilise20 sprites météo natifs et2048 octets de tuiles partagées ; les tuiles des quatre combattants sont vérifiées en VRAM. Aucun buffer plein écran supplémentaire. Le petit état d'immunité n'est pas sauvegardé ; le chemin d'introduction libère ses allocations temporaires après usage.

La version privée active bien Zombie Night (Town), identifiant360, emplacement14. Ses blocs audio originaux sont conservés, et les trente autres flux sont identiques. La piste complète se répète désormais au lieu de s'arrêter après environ99 secondes. **Son fondu final et son silence initial restent présents : ce n'est pas une boucle musicale annoncée sans raccord audible, et aucune écoute humaine n'est revendiquée.** La version publique utilise le repli musical natif prévu dans le moteur, sans redistribution des OST.

## Tests réellement exécutés

- **{len(public['results'])} scénarios/contrôles du chapitre dans chaque version** : police, quatre arrivées, nuit/brume, retour intérieur/route, quatre combats directs, vraie tentative de fuite et de Master Ball refusée, répétition d'un errant, vraie capture sauvage dans la Tour, victoire de Dresseur sauvegardée en Flash, équipe et ordre exacts d'Alyzon, badge et absence de répétition, résidence, condition Ligue+Panthéon, récupération de Flûte sur ancienne sauvegarde, deux escaliers obligatoires par déplacements, zone de soin par déplacement, réveils des deux Misterre, passage du repaire et sauvegarde/reprise avec ancien modèle humain simulé.
- Patrouilles observées dans mGBA, palette d'un PNJ vert ordinaire conservée à côté d'un zombie. Deux trajets évitant les combats sont trouvés puis **rejoués sans interruption par contrôles seuls**, après extinction de l'immunité : entrée ouest→Tour et entrée ouest→Route12, dans les deux versions. La recherche peut revenir à un état temporaire après un essai raté ; le trajet accepté est ensuite rejoué depuis son état initial sans écritures de position ni désactivation de vision.
- Audit statique exhaustif de **{audit['patrol_occupied_tile_combinations']} combinaisons de cases occupées** : aucun seuil de porte occupé, entrées et sorties toujours reliées par les collisions. Ce contrôle ne prétend pas simuler tous les cônes de vision ni tous les timings possibles.
- Audio privé :31 emplacements présents,30 flux inchangés,19500 frames rendues dans mGBA avec énergie audio contrôlée au cours de quatre passages successifs, sans relancer la chanson par script.
- Non-régression privée : **Lance→entrée normale dans la finale→Don Morléone→soin des six Yo-kai→flash→huit formes de Don Spiraton→conclusion→Panthéon→crédits→sauvegarde et Continuer**. Le pilote utilise une équipe de test renforcée ; aucun résultat de bataille ni PV ennemis n'est forcé.
- Empreintes intactes des données, évolutions, capacités, noms et rencontres des151, des PNG retenus, des treize anciennes équipes de la Tour et des références protégées de branches.

Résultats : [publique](public/TEST_MGBA.json), [privée](prive/TEST_MGBA.json), [patrouilles publiques](public/PATROUILLES_MGBA.json), [privées](prive/PATROUILLES_MGBA.json), [audio](prive/AUDIO_MGBA.json), [finale](regressions/prive/FINALE_NORMALE_MGBA.json).

## Captures et clips

- [Introduction complète](public/introduction.gif)
- [Nuit et brume](public/ville-nuit-brume-x3.png), [patrouilles](public/patrouilles.gif)
- [Esquive vers la Tour](public/esquive-vers-tour.gif), [vers la Route12](public/esquive-vers-route12.gif)
- [Quatre images de combat](public/combat-errant-x3.png) : errant, [sprinteur](public/combat-sprinteur-x3.png), [colosse](public/combat-colosse-x3.png), [spectral](public/combat-spectral-x3.png)
- [Portrait d'Alyzon pendant son véritable combat](public/alyzon-portrait-natif-x3.png), [remise du badge](public/alyzon-remise-badge-x3.png)
- [Capture sauvage conservée](public/tour-capture-reussie-x3.png), [zone de soin](public/tour-soin-x3.png)
- Résidence [avant](public/residence-avant-x3.png) et [après](public/residence-apres-x3.png)
- [Récompense Flûte](public/flute-repaire-x3.png), Misterre [Route12](public/misterre-route12-x3.png) et [Route16](public/misterre-route16-x3.png)

Ces captures proviennent du moteur mGBA, pas de montages. Les positions initiales de test et l'équipe renforcée sont des fixtures décrites dans les rapports.

## Reproduction

```sh
source /workspace/.setup/env.sh
make -j6
python tools/yokai/preparer_audio_lavanville.py --source-dir /workspace/private-audio/argenta-integration --output /workspace/private-audio/lavanville-integration
make -j6 YOKAI_AUDIO_DIR=/workspace/private-audio/lavanville-integration
python tools/yokai/auditer_lavanville_finalisation.py
python tools/yokai/verifier_dialogues_lavanville_mgba.py
YOKAI_QA_ROM=$PWD/pokefirered_audio.gba python tools/yokai/verifier_dialogues_lavanville_mgba.py
python tools/yokai/tester_lavanville_chapitre_mgba.py
YOKAI_QA_ROM=$PWD/pokefirered_audio.gba python tools/yokai/tester_lavanville_chapitre_mgba.py
python tools/yokai/tester_lavanville_patrouilles_mgba.py
YOKAI_QA_ROM=$PWD/pokefirered_audio.gba python tools/yokai/tester_lavanville_patrouilles_mgba.py
YOKAI_QA_ROM=$PWD/pokefirered_audio.gba python tools/yokai/tester_lavanville_audio_mgba.py
YOKAI_QA_ROM=$PWD/pokefirered_audio.gba YOKAI_FINALE_REPORT_DIR=docs/lavanville-zombie-night/finalisation/regressions/prive python tools/yokai/tester_spiraton_finale_normale_mgba.py
```

Les chemins audio désignent des ressources privées locales ; aucun fichier musical protégé ni ROM n'est ajouté au dépôt. Les scripts utilisent le cœur libretro mGBA installé dans l'environnement de travail.

## Limites explicites

Le chapitre est codé et ses scénarios fonctionnels sont vérifiés. Une aventure humaine complète depuis le début, un équilibrage humain avec des équipes ordinaires, tous les timings de poursuite, tous les objets/capacités/menus et toutes les villes ne sont pas déclarés testés. Le raccord de répétition de Zombie Night reste à écouter ; la source complète garde son fondu d'origine. La revanche post-Ligue est volontairement une condition et un dialogue, sans équipe ni combat supplémentaire.
'''
(D/'README.md').write_text(readme)
# Source-faithful dialogue transcript, rather than a separately rewritten version.
trans=['# Dialogues définitifs — transcription des scripts\n','Les coupures ci-dessous sont celles des sources. Les services et le rival conservent leurs textes existants.\n']
for file in ['LavenderTown','PokemonTower_7F','CeladonCity_Gym','PokemonTower_2F','CeladonCity_GameCorner']:
 s=(R/f'data/maps/{file}/scripts.inc').read_text()
 for m in re.finditer(r'^(Lavender\w*Text_\w+)::\n((?:\s*\.string[^\n]*\n)+)',s,re.M):
  fragments=re.findall(r'\.string "(.*)"',m[2]);text=''.join(fragments).replace('\\p','\n\n').replace('\\n','\n').replace('$','')
  trans.append('## '+m[1]+'\n\n'+text+'\n')
(D/'DIALOGUES.md').write_text('\n'.join(trans))
files=set(subprocess.check_output(['git','diff','--name-only','7110ce41b'],cwd=R,text=True).splitlines())|set(subprocess.check_output(['git','ls-files','--others','--exclude-standard'],cwd=R,text=True).splitlines());files.add(str((D/'FICHIERS_MODIFIES.txt').relative_to(R)));(D/'FICHIERS_MODIFIES.txt').write_text('\n'.join(sorted(files))+'\n')
print(json.dumps(metadata,ensure_ascii=False))
