#!/usr/bin/env python3
"""Help has a fixed 208x104 answer panel, unlike scrolling field messages."""
import json,re
from localiser_fr import ROOT,replace
from cadrer_dialogues_fr import measure
p=ROOT/'data/localisation/fr/17_aide.tsv';rows=[];report=[]
for row in p.read_text().splitlines():
 f,k,t=row.split('\t',2)
 if k=='Help_Text_AnswerHowAreCavesDifferent':t=r'Les grottes sont dangereuses.\nDes Yo-kai sauvages peuvent surgir\lpartout. Utilise des remèdes\lou retourne te faire soigner.\lDe nouvelles villes peuvent se cacher\lde l’autre côté. Ne renonce pas!$'
 if k=='Help_Text_HowToUseHM':t=t.replace('Une capacité de CS est dure à oublier!','Une CS s’oublie difficilement.')
 def width(s):
  # Font width plus conservative bound for graphical control symbols.
  return measure(s)+12*len(re.findall(r'\{(?:CIRCLE_\w+|PLUS|TRIANGLE|BIG_MULT_X|LEFT_PAREN|RIGHT_PAREN)\}',s))
 single_line=not re.search(r'\\[nlp]',t)
 parts=re.split(r'\\[nlp]',t)
 if len(parts)>1 and k!='Help_Text_DefineStatusProblem':
  # Reflow prose as paragraphs, retaining type-chart sections and numbered steps.
  paragraphs=re.split(r'\\p',t);parts=[]
  for paragraph in paragraphs:
   paragraph=re.sub(r'\\[nl]', ' ',paragraph)
   parts.extend(x.strip() for x in re.split(r'(?=\{CIRCLE_[1-5]\})',paragraph) if x.strip())
 wrapped=[]
 for part in parts:
  indent=re.match(r' *',part)[0];line=indent
  words=re.findall(r'(?:\{[^}]+\}|[^\s{])+',part)
  for word in words:
   candidate=line+(' ' if line.strip() else '')+word
   if line.strip() and width(candidate)>208:
    wrapped.append(line);line=indent+word
   else:line=candidate
  wrapped.append(line)
 if single_line:assert len(wrapped)==1,('One-line help menu overflow',k,wrapped)
 assert len(wrapped)<=7,(k,'Answer panel too tall',wrapped)
 new=r'\n'.join(wrapped)
 assert all(width(line)<=208 for line in wrapped),(k,wrapped)
 replace(ROOT/f,k,new);rows.append('\t'.join([f,k,new]));report.append(dict(symbol=k,lines=len(wrapped),max_conservative_pixels=max(map(width,wrapped))))
p.write_text('\n'.join(rows)+'\n')
(ROOT/'QA_RECETTE_FINALE/LOCALISATION_FR/AIDE_CADRAGE.json').write_text(json.dumps(dict(entries=len(report),fixed_width=208,max_answer_lines=7,scope='Native normal-font table, conservative extra glyph widths, PLAYER7; no silent clipping or field-dialogue scrolling assumption.',results=report),ensure_ascii=False,indent=2)+'\n')
print('HELP LAYOUT PASS',len(report))
