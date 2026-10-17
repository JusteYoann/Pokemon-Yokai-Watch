#!/usr/bin/env python3
"""Reference-only artistic shortlist. Decisions require perceptual validation."""
from pathlib import Path
import ast,csv,json,re,hashlib,collections
R=Path(__file__).resolve().parents[3];D=R/'docs/musique-audit'
def table(name,rows):
 with (D/name).open('w',encoding='utf-8-sig',newline='') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter=';',lineterminator='\n');w.writeheader();w.writerows(rows)
def read(name):return json.loads((D/name).read_text())
audio=read('preuves/ANALYSE_AUDIO.json');by={e['id']:e for e in audio};assert len(by)==len(audio)
games={'YW1':'Yo-kai Watch1','YW2':'Yo-kai Watch2','YW3':'Yo-kai Watch3','YW4':'Yo-kai Watch4','BLASTERS':'Yo-kai Watch Blasters','BUSTERS2':'Yo-kai Watch Busters2','SANGOKUSHI':'Yo-kai Sangokushi'}
def title(e):
 t=re.sub(r'^(?:\d+(?:\.\d+)?|X)\.\s*','',Path(e['member']).stem)
 t=re.sub(r'^Yo[- ]Kai Watch(?: [1-4])? OST -\s*','',t,flags=re.I)
 return re.sub(r' - Yo-Kai.*? OST(?:\(\d+\))?$','',t,flags=re.I)
labels={key:title(e) for key,e in by.items()};archive_rows=[]
module=ast.parse((D/'scripts/extract_rar.py').read_text());archive_inputs=next(ast.literal_eval(n.iter) for n in module.body if isinstance(n,ast.For) and isinstance(n.target,ast.Tuple) and getattr(n.target.elts[0],'id','')=='game')
for game,file in archive_inputs:
 p=Path(file);members=[e for e in audio if e['game']==game and e['archive']==p.name]
 archive_rows.append({'archive':p.name,'jeu':games[game],'acces':'TRANSFÉRÉ ET EXTRAIT, archive autonome','pistes_reellement_inventoriees':len(members),'taille_octets':p.stat().st_size,'sha256_archive':hashlib.sha256(p.read_bytes()).hexdigest(),'remarque':'Lot fourni, pas une preuve d’exhaustivité de l’OST commerciale'})
table('ARCHIVES_ET_ACCES.csv',archive_rows)
rows=[]
for e in audio:
 dup=[x['id'] for x in audio if x['id']!=e['id'] and (x['sha256']==e['sha256'] or x['decoded_mono_11025_sha256']==e['decoded_mono_11025_sha256'])];num=re.match(r'^(\d+(?:\.\d+)?|X)\.',Path(e['member']).name)
 rows.append({'id':e['id'],'archive':e['archive'],'jeu':games[e['game']],'piste':num[1] if num else 'NON NUMÉROTÉE dans le fichier fourni','titre':labels[e['id']],'nom_fichier_original':Path(e['member']).name,'chemin_dans_archive':e['member'],'duree_secondes':round(e['duration_seconds'],3),'codec':e['codec'],'frequence_hz':e['sample_rate'],'canaux':e['channels'],'debit_bps':e['bit_rate'],'doublons_binaires_ou_pcm':','.join(dup) or 'Aucun parmi les fichiers analysés','variante':'Suffixes et Reused conservés ; parenté musicale non déduite de leur seule présence','tempo_bpm_estime':round(e['tempo_estimate_bpm'],1),'confiance_periodicite':round(e['tempo_acf_confidence'],3),'rms_dbfs_mono_analyse':round(e['rms_dbfs'],2),'crete_dbfs_mono_analyse':round(e['peak_dbfs'],2),'centroide_hz_copie_11025':round(e['spectral_centroid_hz'],1),'repetition_offset_secondes_indicatif':round(e['recurrence_offset_seconds'],2),'boucle':e['loop_status'],'elements_audibles':'NON ÉCOUTÉ perceptivement. Décodage complet et mesures réelles ; instruments, voix et émotion non certifiés.','confiance':'Élevée : fichier/durée/décodage. Moyenne/faible : pulsation. Non validée : caractère musical et boucle.','preuve':'preuves/'+e['id']+'.png','sha256_mp3':e['sha256']})
table('INVENTAIRE_OST.csv',rows)
slots=list(csv.DictReader((D/'EMPLACEMENTS_MUSICAUX_KANTO.csv').open(encoding='utf-8-sig'),delimiter=';',lineterminator='\n'));proposals=[]
def row(place,base,key='',why='',scope='',alternative='',native='',plan='Aucun changement durant cette phase',decision=None):
 a=by.get(key);proposals.append({'emplacement':place,'portee':scope,'pokemon_original':base,'candidat_id':key,'candidat_yokai':Path(a['member']).name if a else '', 'jeu':games[a['game']] if a else 'Pokémon natif','candidat_natif':native,'decision':decision or ('A_VALIDER' if key or native else 'CONSERVER'),'justification':why,'alternative':alternative or 'Conserver '+base,'confiance':'Proposition sans écoute perceptive ; mesures et contexte séparés, audition nécessaire' if key or native else 'Conservation par défaut, pas une prétendue comparaison d’écoute','adaptation_future':plan,'preuve':'preuves/'+key+'.png' if a else 'EMPLACEMENTS_MUSICAUX_KANTO.csv'})
for e in slots:row(e['constante'],e['morceau_pokemon_original'],why='Conserver les usages non ciblés ; exceptions locales décrites dans leurs lignes dédiées.',scope='Slot moteur partagé, voir ses utilisateurs réels dans l’inventaire')
def local(place,mapname,key,why,alternative=''):
 music=json.loads((R/f'data/maps/{mapname}/map.json').read_text())['music'].lower();row(place,music,key,why,'Affectation locale : '+mapname,alternative,plan='Après accord : choix audio local, boucle et retour testés ; aucun événement narratif, équipe ou récompense modifié')
local('Maison du joueur Nathan','PalletTown_PlayersHouse_1F','YW1-d7a88e41','Identité domestique recherchée ; réutiliser ce même fichier pour le dialogue du caméo Nathan. La parenté avec Katie reste à auditionner.')
local('Maison du joueur Katie','PalletTown_PlayersHouse_1F','YW1-606b835b','Variante domestique assortie recherchée, même palette future. Ne pas attribuer Natsume’s House à Katie : personnages distincts dans le lexique.')
proposals[-2]['portee']='PalletTown_PlayersHouse_1F et2F, seulement joueur masculin ; extérieur MUS_PALLET intact';proposals[-1]['portee']='Mêmes deux maps, seulement joueuse ; condition de genre native préservée'
local('Céladopole extérieur','CeladonCity','YW1-bbe94e34','Pulsation relativement régulière99,4, projet de respiration urbaine. Même plage de tempo que Uptown2/4 ne signifie pas même ambiance ; écoute indispensable.')
local('Manoir de Cramois’Île','PokemonMansion_1F','YW1-3fb46a59','Contrastes d’enveloppe réellement visibles ; candidat d’exploration inquiétante, caractère non certifié. Ne pas étendre à Lavanville/Tour.')
proposals[-1]['portee']='Les quatre étages du Manoir, sans généraliser à une autre carte utilisatrice du slot'
local('Canyon Sesor','SevenIsland_SevaultCanyon','YW3-81d9c99a','Basecamp3 :155,9s, périodicité0,73 contre0,47 dans Basecamp Busters2. Priorité de prototype : déplacement prolongé plus régulièrement pulsé, pas une supériorité artistique prouvée.','Basecamp Busters2 ou thème natif ; Time For A Horse Ride! à comparer, pas un usage obligé')
local('Bois aux Baies','ThreeIsland_BerryForest','YW4-d1555377','Proposition de respiration forestière postgame, sans changer la Forêt de Jade. Tempo peu fiable0,25 : ne pas décrire le morceau comme métronomique.')
local('Île3 ville','ThreeIsland','YW2-0e6bfd8c','Réaffectation du port San Fantastico à un hub Sevii ;107,7 estimés et périodicité0,59. Intention de respiration, non une ambiance entendue.')
local('Sylphe occupée','SilphCo_1F','YW3-5dbaaed5','Bada-Bing Tower comme recherche pour l’ascension d’un bâtiment occupé :210,5s,92,3 estimés. Ne pas inventer50 étages ou importer la Mafiamille dans le scénario Rocket.')
proposals[-1]['portee']='Étages de Sylphe pendant l’occupation seulement ; après libération, fallback natif à valider'
local('Maître Nyada148 — acquisition existante','SevenIsland_SevaultCanyon','YW2-5d271d4a','Motif d’acquisition spéciale envisagé ;105,5s et pulsation très incertaine0,14. Pas de nouveau combat ni de PNJ Maître Nyada inventé.')
local('Seigneur Enma — dialogue','MtEmber_Summit','BL-50568e39','119s, développement plus long que Yo-kai World59,8s pour une attente variable. Enma Villa211s est une alternative, pas une affectation automatique par le titre.')
row('Vélo','mus_cycling','YW1-6b2ae63e','117,5 BPM estimés, périodicité0,71 ; hypothèse de déplacement récurrent. Comparer Time For A Horse Ride! sans choisir la plus célèbre.','Slot vélo entier, les routes à pied gardent leurs affectations',plan='Boucle, passage marche/vélo/surf, priorité musicale et retour à tester')
for e in proposals:
 if e['emplacement']=='MUS_CYCLING':e.update(candidat_id='YW1-6b2ae63e',candidat_yokai=Path(by['YW1-6b2ae63e']['member']).name,jeu=games['YW1'],decision='A_VALIDER',justification='Voir la proposition Vélo : choix du slot entier, non appliqué.',preuve='preuves/YW1-6b2ae63e.png')
# Existing dialogue contexts. Shared motifs here mean deliberate reuse of a file,
# never a claimed musical relationship between independently supplied tracks.
for place,key,why in [('Ariane — dialogues','YW4-c601bc8f','Hailey Anne = Ariane dans le lexique ;143,6s et périodicité0,74. Reused est un intitulé fourni, pas une filiation démontrée avec un fichier absent.'),('Katie caméo — dialogues','YW4-7ff108d1','Katie’s Theme comme identité de caméo ;194,7s et périodicité0,69. Variante selon le protagoniste, sans conflit avec la Katie jouable.'),('Nathan caméo — dialogues','YW1-d7a88e41','Reprise intentionnelle du même fichier que la maison Nathan, pas une nouvelle variation prétendument existante.'),('Nathaniel/Michael — dialogues','YW2-c14e0d68','Contexte du passé renseigné par le lexique et durée246,6s ; proposer un rappel familial sans réécrire les scènes ou imposer une tristesse non entendue.')]:
 row(place,{'Ariane — dialogues':'mus_route24','Katie caméo — dialogues':'mus_celadon','Nathan caméo — dialogues':'mus_celadon','Nathaniel/Michael — dialogues':json.loads((R/'data/maps/FuchsiaCity_SafariZone_Entrance/map.json').read_text())['music'].lower()}[place],key,why,'Uniquement interactions existantes de ces caméos ; les conditions garçon/fille restent intactes',plan='Audio local seulement : restaurer la carte sur Non, après cadeau et après combat')
assignments={
 'TRAINER_CAMEO_LORD_ENMA':('YW1-ad29ca7b','Final Battle :202,1s, variations d’énergie visibles. Réserver un climax optionnel distinct du Champion et d’Enma sauvage. Alternative Zazelmare/Whismellowman après audition.'),
 'TRAINER_CAMEO_ARIANE_POST':('BL-16e40425','Captain Thunder :163,5s, périodicité0,58. Revanche distincte du dialogue ; intensité effective à comparer, pas à déduire du tempo.'),
 'TRAINER_CAMEO_DOMNISCIAN':('SG-98064728','Réaffectation Boss Yo-kai :193,3s. Ne pas préférer Hinozall uniquement pour son nom ; version English et voix éventuelles non vérifiées.'),
 'TRAINER_CAMEO_DON_MORLEONE':('SG-634d3b4c','Soruka :254,4s, périodicité0,64. Climax de faction recherché, sans revendiquer un style noir/jazz entendu. Alternative explicite The Ghoulfather.'),
 'TRAINER_CAMEO_EMPLOYEE_RED':('SG-0504f7f1','Motif commun aux deux employés ;210,9s et117,5 estimés. Comparer Robonyan3000 sans créer ce boss.'),
 'TRAINER_CAMEO_EMPLOYEE_BLUE':('SG-0504f7f1','Même fichier de faction que l’autre employé ; aucune rencontre ajoutée.'),
 'TRAINER_CAMEO_MAFIA_SMALL':('SG-4e7616eb','Motif commun aux trois Mafiamille ;213,8s et107,7 estimés. Contraste réel avec employés à écouter.'),
 'TRAINER_CAMEO_MAFIA_TALL':('SG-4e7616eb','Même fichier que les autres Mafiamille.'),
 'TRAINER_CAMEO_MAFIA_BROAD':('SG-4e7616eb','Même fichier que les autres Mafiamille.')}
for who in ['NATHAN','KATIE']:
 for stage in ['ADV','POST']:assignments[f'TRAINER_CAMEO_{who}_{stage}']=('YW2-37feafcc','vs. Yo-kai ~2~ :161,8s, périodicité0,58. Thème de défi commun aux protagonistes caméos ; les combats sauvages et les autres dresseurs restent Pokémon.')
for e in csv.DictReader((D/'CAMEOS_AUDIO.csv').open(encoding='utf-8-sig'),delimiter=';',lineterminator='\n'):
 key,why=assignments.get(e['trainer'],('', 'Conserver le thème dresseur faute de remplacement justifié ; pas20 thèmes imposés pour20 équipes.'))
 row(e['trainer'],e['current_music'].lower(),key,why,'Ce dresseur précis, pas toute sa classe',plan='Après validation : routage musical par ID ; ni classe, équipe, ordre, choix Oui/Non, cadeau ou drapeau modifié')
row('Matt avant Champion','mus_vs_trainer',why='Projet de variation rappelant le motif de rencontre Matt ; ce n’est pas un arrangement déjà créé. Ne pas assimiler simple encounter315 à un long combat.',scope='Combats Matt uniquement',native='Projet : motif MUS_ENCOUNTER_RIVAL + variation de MUS_VS_TRAINER',plan='Évaluer la composition native après validation ; aucune séquence écrite ici')
row('Matt Champion','mus_vs_champion',why='Préserver le climax Pokémon natif, distinct du super-boss optionnel Seigneur Enma',scope='Champion')
for place,base in [('Giovanni Repaire/Sylphe','mus_vs_trainer'),('Giovanni Arène','mus_vs_gym_leader')]:
 row(place,base,'SG-29d6bca9','Noruka comme motif commun des trois étapes de Giovanni, pas de changement de son scénario ; durée263,1s, tempo143,6 peu fiable0,30. Progression de tension à vérifier réellement.','IDs Giovanni uniquement',plan='Routage audio ciblé futur ; boss, arène et progression préservés')
row('Conseil4','mus_vs_gym_leader',why='Comparer cette ressource Pokémon déjà liée pour distinguer Conseil4 et arènes ; source native ne signifie pas audition ni qualité supérieure certifiée.',scope='Classe ELITE_FOUR uniquement ; arènes conservent leur thème',native='MUS_RS_VS_GYM_LEADER / mus_rs_vs_gym_leader',plan='Routage par classe audio après accord ; ressource existante, pas de nouveau MP3 ni équipe')
row('Enma sauvage Grotte Azurée','mus_vs_mewtwo',why='Garder une identité sonore différente de Seigneur Enma ; capture et accès inchangés',scope='Rencontre fixe Enma')
table('PROPOSITION_BANDE_SON.csv',proposals)
selected={e['candidat_id'] for e in proposals if e['candidat_id']};reasons={
 'B2-5c92ab0d':('Titre Pokémon conservé ; aucun hymne Busters2 imposé.','Défi postgame existant après audition.'),
 'B2-4c9c8595':('Basecamp3 choisi pour prototype comparatif : périodicité0,73 contre0,47, pas un classement artistique.','Alternative principale au Canyon ; ne pas affirmer une mélodie commune sur le seul nom.'),
 'YW1-3da6cd49':('Pas de poursuite Terror Time existante ; Footsteps impose un contrôle perceptif.','Brève tension Rocket après écoute, sans nouvel événement.'),
 'YW1-54ae45c8':('Enma Track préféré provisoirement au dialogue pour son développement119s contre59,8s.','Alternative de dialogue, boucle non validée.'),
 'BL-78b5c4d1':('Hailey Anne4 désormais proposée pour le dialogue Ariane ; pas deux thèmes de dialogue concurrents.','Alternative si le caractère du thème4 ne convient pas.'),
 'BL-dd878014':('Pas de combat Robonyan3000 ajouté, ni musique imposée selon la couleur shiny.','Alternative aux employés Domniscian.'),
 'BL-ab6d1ed7':('Un seul choix principal de super-boss ; Zazelmare reste un comparatif.','Alternative au combat Seigneur Enma.'),
 'BL-92f81647':('Hinozall n’est pas obligatoire pour Domniscian. English ne prouve ni absence ni présence de chant.','Alternative à Boss Yo-kai après écoute et contrôle des voix.'),
 'SG-975cf362':('Pas d’espace de repos supplémentaire à créer pour utiliser la piste.','Alternative à Blossom Heights.'),
 'YW2-a12652e8':('Venoct = Octorgone, mais un titre de personnage/Wayfarer ne démontre pas l’adéquation à un combat légendaire.','Introduction Octorgone après audition ; pas de remplacement automatique par nom.'),
 'YW4-65294aac':('Natsume est la fille de Nathan, pas Katie ; aucune maison Natsume n’est ajoutée.','Réaffectation possible à une autre scène si l’audition le justifie.'),
 'YW4-c065f9e5':('Pas de second thème principal Ariane/Usapyon en plus de Hailey Anne4.','Alternative au dialogue ou revanche, seulement après comparaison.'),
 'YW4-8ba41c3f':('Maison Nathan1 conservée comme référence et reprise de caméo ; ne pas retenir toutes les versions.','Alternative à la maison si la production4 s’adapte mieux.'),
 'YW3-998d67f9':('Ne pas choisir Ghoulfather pour Don Morleone sur la seule traduction du nom ; Soruka est le premier comparatif, sous réserve d’écoute.','Alternative prioritaire au boss Don Morleone.'),
 'YW3-8c2265b7':('Vélo1 et Canyon Basecamp3 restent les premiers choix ; aucun cheval, rodéo ou contexte nouveau créé.','Route adaptée ou vélo après comparaison perceptive.'),
 'YW3-62905c7d':('Pas de nouvelle Villa Enma dans Kanto ; dialogue actuel utilise une autre référence.','Alternative à Enma Track avant Seigneur Enma.'),
 'YW3-f191975f':('Aucune invasion de zombies/mairie nouvelle demandée.','Tension d’une scène existante après écoute.'),
 'YW3-e9a93e2b':('Pas de système nocturne Zombie Night ajouté ni déduit du titre.','Événement existant sous réserve de pertinence musicale.'),
 'YW3-1b28fffc':('Casino conserve son thème natif ; Club Koma ne justifie pas une boîte de nuit nouvelle.','Éventuelle scène existante de divertissement, après audition.'),
 'YW2-8c26bf90':('Référence22,3s trop courte pour une longue route sans arrangement important ; pas de scène Komasan ajoutée.','Accent ponctuel existant après validation.'),
 'YW2-329fbef3':('Aucun train jouable n’est ajouté.','Réaffectation possible, pas usage obligatoire dicté par le titre.')}
rejected=[]
for key,e in by.items():
 if key in selected:continue
 if key in reasons:why,alt=reasons[key]
 else:
  t=labels[key].lower()
  if any(w in t for w in ['title','very curious','choose a name','tutorial']):why='Titre, introduction, nom du joueur et tutoriels restent Pokémon ; le rôle du titre fourni ne rend pas son remplacement nécessaire.';alt='Réaffectation possible après audition, pas une nouvelle scène imposée.'
  elif any(w in t for w in ['zombie','terror']):why='Aucune invasion/poursuite ajoutée pour employer ce thème ; les scènes existantes conservent leur rythme narratif.';alt='Éventuel accent Rocket sur un événement existant après écoute.'
  elif any(w in t for w in ['uptown','southmond','sparkopolis','east pine','dukesville','city','peaceful','harrisville','station','springs','castletown']):why='Les villes et routes natives sont majoritairement conservées ; Blossom Heights et San Fantastico suffisent à la première sélection urbaine, sans certifier leur supériorité perceptive.';alt='Comparer à Céladopole/Île3 ou garder le thème Pokémon, sans renommer les lieux.'
  elif any(w in t for w in ['wood','grove','dungeon','tunnel']):why='Les longues explorations gardent leurs thèmes natifs, sauf les contextes ciblés Manoir/Bois aux Baies. Pas de nouveau tunnel infini.';alt='Alternative à Hospital ou Mystic Grove après audition et contrôle des boucles.'
  elif any(w in t for w in ['treasure','blasters t','patrol','hideout','detective','dodgy']):why='Basecamp3 au Canyon et Bada-Bing à Sylphe sont les choix de recherche ; ne pas multiplier les musiques ou ajouter des missions pour utiliser le reste.';alt='Comparer aux mêmes contextes existants, sans changer l’intrigue.'
  elif any(w in t for w in ['vs.','battle','conquest']):why='La progression de boss possède déjà ses premiers candidats ; pas de nouveau boss ajouté ni de sélection par seule homonymie.';alt='Comparer au boss existant approprié dans la fiche, après écoute ; vérifier voix et densité.'
  else:why='Aucun remplacement supplémentaire justifié pour cette première sélection ; instruments et émotion non certifiés, aucun jugement définitif de qualité.';alt='Conserver comme réserve pour une comparaison perceptive contextualisée.'

 rejected.append({'id':key,'jeu':games[e['game']],'archive':e['archive'],'fichier_origine':e['member'],'statut':'NON RETENU COMME CHOIX PRINCIPAL, PROVISOIRE','raison':why,'alternative_plausible':alt,'limite':'Signal réellement analysé ; aucune écoute perceptive, aucun jugement définitif de qualité.'})
table('MUSIQUES_ECARTEES.csv',rejected)
# Comparisons name real available files, plus native fallbacks, rather than
# inventing missing tracks or claiming that title matching establishes emotion.
comparisons={
 'Vélo':['YW1-6b2ae63e','YW3-8c2265b7'],
 'Maison Nathan':['YW1-d7a88e41','YW4-8ba41c3f'],
 'Maison Katie':['YW1-606b835b','YW4-7ff108d1','YW4-65294aac'],
 'Céladopole':['YW1-bbe94e34','YW2-193c764e','YW4-01723eb6','SG-975cf362'],
 'Manoir':['YW1-3fb46a59','YW2-2365f37c'],
 'Canyon':['YW3-81d9c99a','B2-4c9c8595','YW3-8c2265b7','YW3-5bfe4561'],
 'Sylphe occupée':['YW3-5dbaaed5','YW3-950c6e76','SG-0504f7f1'],
 'Dialogue Ariane':['YW4-c601bc8f','BL-78b5c4d1','YW4-c065f9e5'],
 'Revanche Ariane':['BL-16e40425','YW2-37feafcc'],
 'Nathaniel/Michael':['YW2-c14e0d68','YW2-ca2287b9','YW2-d38adb94'],
 'Dialogue Seigneur Enma':['BL-50568e39','YW3-62905c7d','YW1-54ae45c8'],
 'Combat Seigneur Enma':['YW1-ad29ca7b','BL-ab6d1ed7'],
 'Domniscian':['SG-98064728','BL-92f81647'],
 'Don Morleone':['SG-634d3b4c','YW3-998d67f9'],
 'Giovanni':['SG-29d6bca9','SG-634d3b4c']}
comp=[]
for context,keys in comparisons.items():
 for rank,key in enumerate(keys,1):
  e=by[key];comp.append({'contexte':context,'rang_de_comparaison_pas_note_artistique':rank,'id':key,'titre':Path(e['member']).name,'jeu':games[e['game']],'duree_s':round(e['duration_seconds'],1),'tempo_estime':round(e['tempo_estimate_bpm'],1),'periodicite':round(e['tempo_acf_confidence'],2),'rms_dbfs_mono':round(e['rms_dbfs'],1),'premier_passage_a_ecouter':'0:15–0:45, puis introduction et deux répétitions ; adapter aux pistes courtes','statut':'À auditionner : durée/pulsation/RMS ne prouvent pas timbre, émotion ou qualité de transition','preuve':'preuves/'+key+'.png'})
table('FICHES_COMPARAISON.csv',comp)
# Preserve full literal/dynamic call inventory.
calls=[]
for root in [R/'src',R/'data']:
 for p in sorted(root.rglob('*')):
  if not p.is_file() or p.suffix not in ['.c','.h','.inc','.s']:continue
  for n,line in enumerate(p.read_text(errors='replace').splitlines(),1):
   if re.search(r'\b(?:PlayBGM|PlayNewMapMusic|FadeInNewBGM|PlayMapChosenOrBattleBGM|PlayBattleBGM|PlayFanfare|SaveMapMusic|FadeOutBGM|FadeOutAndPlayNewMapMusic|Overworld_PlaySpecialMapMusic)\s*\(|\b(?:playbgm|playfanfare|fademusic|setmapmusic|fadedefaultbgm|fadeoutbgm|fadeinbgm|savebgm|restorebgm)\b',line):calls.append({'file':str(p.relative_to(R)),'line':n,'appel':line.strip(),'analyse':'Source examinée statiquement ; paramètre variable ≠ affectation spécifique prouvée, pas une exécution.'})
table('APPELS_AUDIO_STATIQUES_ET_DYNAMIQUES.csv',calls)
summary={'jeux_annonces':7,'jeux_representes':len({e['game'] for e in audio}),'lots_rar_accessibles':len(archive_rows),'lots_actuels_bloques':0,'mp3_inventories_et_decodes_integralement':len(audio),'duree_analysee_secondes':sum(e['duration_seconds'] for e in audio),'mp3_ecoutes_perceptivement':0,'references_mp3_proposees':len(selected),'mp3_non_retenus_principalement':len(rejected),'jeux_avec_choix_principal':sorted({by[k]['game'] for k in selected}),'pistes_par_jeu':dict(collections.Counter(e['game'] for e in audio)),'slots_moteur_musique':91,'cartes_auditees':425,'lignes_proposition':len(proposals),'appels_audio_releves':len(calls),'phase':'ANALYSE DU CORPUS REÇU ET PRÉSÉLECTION À VALIDER ; aucune écoute perceptive ni intégration','integration_audio':False,'arrangement':False}
(D/'preuves/SYNTHESE_PHASE1.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n');print(json.dumps(summary,ensure_ascii=False))
