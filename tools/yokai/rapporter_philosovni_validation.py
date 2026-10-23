#!/usr/bin/env python3
"""Publish a review report only when all native proofs match the final ROMs."""
from pathlib import Path
import json,hashlib,subprocess,re
from mgba_rpc import ROOT
D=ROOT/'docs/pierre-philosovni';V=D/'validation';commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
report=dict(base='e1dcd9132aa8666fb1798c90a731859f1632313e',branch='feature/pierre-philosovni-carmin',implementation_commit=commit,versions={})
paths=['TEST_MGBA.json','LIMITES_MGBA.json','DIALOGUES_MGBA.json','NAVETERAN_MGBA.json','CAPTURES_MGBA.json','../regressions/champions/{mode}/TEST_CHAMPIONS_MGBA.json','../regressions/lavanville/{mode}/TEST_MGBA.json','../regressions/argenta/{mode}/TEST_MGBA.json','../regressions/finale/{mode}/FINALE_NORMALE_MGBA.json']
for mode,file in [('public','pokefirered.gba'),('prive','pokefirered_audio.gba')]:
 rom=ROOT/file;sha=hashlib.sha256(rom.read_bytes()).hexdigest();checks=[]
 for path in paths:
  p=(V/mode/path.format(mode=mode)).resolve();j=json.loads(p.read_text());assert j['passed'],str(p);assert j['rom_sha256']==sha,('stale ROM',str(p))
  checks.append(dict(file=str(p.relative_to(D)),checks=len(j.get('checks',j.get('results',[]))) or j.get('lines_checked',1)))
 log=(V/f'COMPILATION-{mode}.txt').read_text();assert not re.search(r'(?:error:|Error |undefined reference|overflowed by)',log)
 ewram=int(re.search(r'EWRAM:\s+(\d+) B',log)[1]);iwram=int(re.search(r'IWRAM:\s+(\d+) B',log)[1]);assert rom.stat().st_size<=32*1024*1024 and ewram<256*1024 and iwram<32*1024
 report['versions'][mode]=dict(rom_sha256=sha,rom_bytes=rom.stat().st_size,rom_margin_bytes=32*1024*1024-rom.stat().st_size,ewram_bytes=ewram,ewram_margin_bytes=256*1024-ewram,iwram_bytes=iwram,iwram_margin_bytes=32*1024-iwram,proofs=checks)
assert json.loads((V/'PRESERVATION.json').read_text())['passed']
report['passed']=True;(V/'VALIDATION.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
(D/'README.md').write_text(f'''# Le mystère de la Pierre Philosovni

Chapitre intégré sur **feature/pierre-philosovni-carmin**, depuis la version validée des Champions, Lavanville et Don Morléone. Aucun merge sur master.

Code : `{commit}`. Base : `e1dcd9132aa8666fb1798c90a731859f1632313e`.

Wyatt exprime ses inquiétudes après le discours d'Argenta, une seule fois avant son premier défi. Il ignore le nom de la Pierre. Son équipe, son badge et sa CT restent inchangés. À Carmin, trois habitants commentent l'accident ; Ariane et Usapion proposent l'enquête sur le quai. Le joueur peut refuser puis revenir. L'entrepôt est accessible à pied, sans Coupe ni Surf.

La conversation des sbires révèle seulement le nom de la Pierre, sa récupération après le crash, sa destination Céladopole et les phénomènes étranges qu'ils lui associent. L'origine du vaisseau reste inconnue. L'artefact n'est ni montré ni remis au joueur. Aucun développement ajouté à Céladopole, Safrania ou à la Ligue.

## Combat et progression

Le duo utilise quatre vrais combattants : le joueur et Usapion21 contrôlé par Ariane, contre Ralbouc18 et Potofeu19, un par sbire. Les six membres du joueur sont disponibles, y compris le sixième en remplacement volontaire. Une adaptation isolée du double local ajoute100 octets RAM pour le partenaire temporaire ; elle ne transforme pas le multi en liaison en système IA. Les deux sbires utilisent un enregistrement de paire dédié, sans réserves. Les doubles ordinaires gardent leurs deux commandes humaines.

La fuite et la capture sont refusées par les règles Dresseur natives. Usapion choisit une attaque valide, vise les adversaires, consomme ses PP et peut tomber K.O. sans emprunter un membre du joueur. Il n'est jamais sauvegardé dans l'équipe. Une défaite soigne le joueur et permet de recommencer, sans victoire enregistrée.

Après victoire, les sbires fuient ; la Pierre a déjà quitté Carmin. Ariane remet Coupe, une seule fois, puis retrouve son Arène. Un sac plein laisse la récompense en attente, y compris après Save/Continue. Une ancienne sauvegarde possédant déjà la CS n'en reçoit pas une seconde. Si Usapion gagne alors que toute l'équipe du joueur est K.O., celle-ci est soignée avant le retour sur carte.

Le capitaine soigne toujours son mal de mer et conserve la logique de départ de l'Océane, mais ne remet plus Coupe. La récompense d'Ariane ne déclenche pas le départ du navire. Navétéran reste un Yo-kai sauvage20 rencontrable et capturable dans le couloir du navire. Coupe reste soumise au **Badge Cascade**, règle native conservée. L'énigme des interrupteurs, les Dresseurs, le Badge Foudre, la CT et l'équipe validée d'Ariane restent intacts.

## Captures mGBA

[Rencontre et entrée de l'entrepôt](validation/public/carmin-rencontre-x3.png) · [Deux sbires à l'introduction](validation/public/deux-sbires-introduction-x3.png) · [Combat Duo](validation/public/combat-duo-x3.png) · [Sixième membre actif](validation/public/sixieme-membre-actif-x3.png) · [Remise de Coupe](validation/public/remise-cs-coupe-x3.png) · [Utilisation de Coupe](validation/public/coupe-arbre-carmin-x3.png) · [Navétéran](validation/public/naveteran-oceane-x3.png).

[GIF de la rencontre](validation/public/ariane-rencontre.gif) · [Conversation de l'entrepôt](validation/public/entrepot-revelation.gif) · [Combat et victoire](validation/public/combat-duo-victoire.gif) · [Défaite réelle](validation/public/combat-duo-defaite.gif).

Les PNG natifs mesurent240×160 ; les agrandissements et GIF utilisent le plus proche voisin. La capture rapprochée de la CS rejoue la récompense en attente (état2 fourni comme fixture) ; le test complet obtient auparavant la victoire réelle.

## Validation des deux versions finales

| Vérification exécutée dans mGBA | Publique | Privée |
|---|---:|---:|
| Chapitre, marche native, dialogue, victoire/défaite/reprise, sauvegardes, Océane, retour à l'Arène |21 contrôles |21 contrôles |
| Ancien map-view Flash, refus fuite/capture, sixième membre, K.O., sac plein, Coupe et double ordinaire |11 contrôles |11 contrôles |
| Mesure des textes par la police GBA |192 lignes, aucun dépassement |192 lignes, aucun dépassement |
| Navétéran20 : rencontre, capture Master Ball réelle et retour sur carte |Réussi |Réussi |
| Champions : dix victoires natives, huit badges et variantes garçon/fille |Réussi |Réussi |
| Lavanville et progression Mafiamille associée |28 scénarios |28 scénarios |
| Discours d'Argenta depuis l'entrée nord20 |Réussi |Réussi |
| Lance, finale normale Morléone/Spiraton, huit formes, Panthéon, crédits, Save/Continue |Réussi |Réussi |

[Rapport et empreintes des ROM](validation/VALIDATION.json) · [Préservation binaire](validation/PRESERVATION.json) · [Compilation publique](validation/COMPILATION-public.txt) · [Compilation privée](validation/COMPILATION-prive.txt).

Les rapports détaillés restent dans [public](validation/public) et [prive](validation/prive), avec l'empreinte de leur ROM. Les fixtures placent le joueur sur les cartes, configurent son équipe de test ou les cas limites explicités. Les ennemis, leurs PV et les issues des combats ne sont pas modifiés pour obtenir une réussite. Le cas sac plein remplit artificiellement les58 emplacements CT/CS, situation de robustesse distincte d'un inventaire normal.

## Ressources et contraintes techniques

Les5821 PNG/palettes préexistants sont conservés (comparaison des fins de ligne normalisées pour les palettes). Les151 fiches, évolutions, types et statistiques, tous les anciens enregistrements Dresseur et les31 flux audio privés restent identiques. La finale et les événements protégés de Lavanville, Koga, Mafiamille et des apparitions secondaires sont conservés. Aucune musique protégée ni ROM n'est publiée ici.

Le nouveau décor assemble des tuiles existantes : cabane sur le quai, passage de trois tuiles dans la clôture et intérieur14×12 avec éléments du tileset SilphCo. Le chargement réapplique uniquement les19 nouvelles tuiles du quai après restauration du map-view d'une ancienne sauvegarde ; les identifiants des cartes/layouts historiques restent inchangés.

Ariane et Usapion réutilisent leurs poses validées. Les rendez-vous et changements de carte remplacent un suivi animé continu ; aucun cycle de marche nouveau n'est inventé. Aucun portrait de dos d'Ariane n'étant validé, l'introduction montre le dos du joueur, les deux sbires puis les quatre Yo-kai, avec attribution explicite d'Usapion à Ariane. Le combat ne comprend pas de réserve pour Ariane ni pour les sbires. L'IA du partenaire privilégie la puissance des capacités valides ; elle n'est pas une IA de stratégie avancée.

ROM publique :16 777 216 octets. ROM privée :31 675 163 octets, sous32 Mio. EWRAM :261 232 octets, **912 octets libres**. IWRAM :29 824 publique /29 888 privée. Les contrôles fonctionnels utilisent notamment une équipe QA renforcée ; ils ne constituent pas une traversée complète de Kanto avec une équipe normale ni une validation exhaustive de l'équilibrage. Les31 OST sont vérifiées par leurs données binaires, sans nouvelle certification d'écoute ou de boucle audio.

[Audit et solution retenue](AUDIT.md) · [Dialogues définitifs](DIALOGUES.md) · [Équipes](EQUIPES.md) · [Fichiers modifiés](FICHIERS_MODIFIES.txt).
''')
print('Final report PASS: all native proofs match both final ROM hashes')
