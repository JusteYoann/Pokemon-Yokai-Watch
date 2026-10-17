"""Apply only the user's supplied lexicon; context never becomes a heard mood."""
from pathlib import Path
import csv,json,re
D=Path(__file__).resolve().parents[1];text=(D/'source-data/DIRECTION_MUSICALE_POKEMON_YOKAI_WATCH_CODEX.md').read_text();lex={}
for line in text.splitlines():
 parts=[x.strip() for x in line.split('|')[1:-1]]
 if len(parts)==2 and parts[0] not in ['Terme anglais dans les OST','---'] and not parts[0].startswith('---'):lex[parts[0]]=parts[1]
patterns=[('Springdale',r'springdale'),("Nate / Nate's",r'\bnates?\b'),("Katie / Katie's",r'\bkaties?\b'),("Natsume / Natsume's",r'\bnatsumes?\b'),("Hailey Anne / Hailey Anne's",r'hailey annes?'),('Dukeville',r'dukes?ville'),('Zombie Night',r'zombie night'),('New Yorkai',r'new yo.?kai city|new yorkai'),('Bada Bing Tower',r'bada.?bing tower'),('The Ghoulfather',r'ghoulfather'),('Blasters',r'blasters'),('Blasters T / Blasters Basecamp',r'blasters (?:t\b|basecamp)'),('Club Koma',r'club koma'),('Time For Horse',r'time for.*horse'),('San Fantastico',r'san fantastico'),('Harrisville',r'harrisville'),('Old / Past (dans YW2)',r'\bold springdale\b|\bin the past\b'),('Venoct',r'venoct'),('Master Nyada',r'master nyadas?'),('Wildwood',r'wildwood'),('Infinite Tunnel',r'infinite tunnel'),('Terror Time',r'terror time'),('Robonyan 3000',r'robonyan 3000'),('Captain Thunder',r'captain thunder'),('Hinozall',r'hinozall'),('Whismellowman',r'whismellowman'),('Zazel / Zazelmare',r'zazel')]
rows=[]
for e in json.loads((D/'preuves/ANALYSE_AUDIO.json').read_text()):
 title=re.sub(r' - Yo-Kai.*? OST(?:\(\d+\))?$','',Path(e['member']).stem,flags=re.I);matched=[key for key,p in patterns if re.search(p,title,re.I)]
 rows.append({'id':e['id'],'fichier':Path(e['member']).name,'termes_du_lexique':' | '.join(matched),'contexte_original_fourni':' | '.join(lex[k] for k in matched) if matched else 'Pas de correspondance explicite dans le lexique : titre conservé, contexte supplémentaire non inventé.','statut':'Contexte issu du cahier du créateur, pas une ambiance entendue et pas une affectation obligatoire','source':'source-data/DIRECTION_MUSICALE_POKEMON_YOKAI_WATCH_CODEX.md'})
with (D/'LEXIQUE_ET_CONTEXTES.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]),delimiter=';',lineterminator='\n');w.writeheader();w.writerows(rows)
print('Applied user lexicon to',len(rows),'reference rows')
