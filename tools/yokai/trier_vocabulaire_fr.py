#!/usr/bin/env python3
"""Sort localized Easy Chat views without changing saved word IDs or unlock flags."""
import re,json,unicodedata,collections
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];D=ROOT/'src/data/easy_chat'
def key(t):
 t=t.replace('Œ','OE').replace('œ','oe')
 return ''.join(c for c in unicodedata.normalize('NFKD',t).upper() if c.isalnum() and not unicodedata.combining(c))
texts={};groups={};changes=[]
for p in sorted(D.glob('easy_chat_group_*.h')):
 s=p.read_text();local=dict(re.findall(r'static const u8 (\w+)\[\] = _\("([^"]*)"\)',s));texts.update(local)
 refs=re.findall(r'\.text = (\w+)',s)
 if refs:
  order=sorted(range(len(refs)),key=lambda i:(key(local[refs[i]]),i));counter=iter(order)
  s=re.sub(r'(\.alphabeticalOrder = )\d+',lambda m:m[1]+str(next(counter)),s)
  assert sorted(order)==list(range(len(refs)));groups['EC_GROUP_'+p.stem.removeprefix('easy_chat_group_').upper()]=[local[x] for x in refs]
  p.write_text(s)
# Display-only value lists for moves/species must also follow localized names.
move=dict(re.findall(r'\[(MOVE_\w+)\]\s*= _\("([^"]*)"\)',(ROOT/'src/data/text/move_names.h').read_text()))
mon=dict(re.findall(r'\[(SPECIES_\w+)\]\s*= _\("([^"]*)"\)',(ROOT/'src/data/text/species_names.h').read_text()))
for file,pat,names in [('pokemon','SPECIES_',mon),('pokemon2','SPECIES_',mon),('move_1','MOVE_',move),('move_2','MOVE_',move)]:
 p=D/f'easy_chat_group_{file}.h';s=p.read_text();m=re.search(r'(static const u16 \w+\[\] = \{)(.*?)(\n\};)',s,re.S);ids=re.findall(r'\b'+pat+r'\w+\b',m[2]);ordered=sorted(ids,key=lambda x:(key(names[x]),x));assert collections.Counter(ids)==collections.Counter(ordered)
 p.write_text(s[:m.start()]+m[1]+'\n'+''.join('    '+x+',\n' for x in ordered).rstrip('\n')+m[3]+s[m.end():])
constants=(ROOT/'include/constants/easy_chat.h').read_text();wordIds={name:(group,int(idx,0)) for name,group,idx in re.findall(r'#define (EC_WORD_\w+)\s+\((EC_GROUP_\w+) << 9\) \| (0x[\da-fA-F]+|\d+)',constants)}
def display(code):
 if code in wordIds:
  group,i=wordIds[code];return groups[group][i]
 m=re.fullmatch(r'EC_(POKEMON2?|MOVE2?)\((\w+)\)',code);assert m,code
 return (mon['SPECIES_'+m[2]] if m[1].startswith('POKEMON') else move['MOVE_'+m[2]])
p=D/'easy_chat_words_by_letter.h';s=p.read_text();blocks=[];original=[];split_homonyms=[]
for body in re.findall(r'static const u16 sEasyChatWordsByLetter_\w+\[\] = \{(.*?)\};',s,re.S):
 body=re.sub(r'//[^\n]*','',body);tokens=re.findall(r'-1|\b\d+\b|EC_WORD_\w+|EC_(?:POKEMON2?|MOVE2?)\(\w+\)',body);i=0
 while i<len(tokens):
  if tokens[i]=='-1':
   n=int(tokens[i+1]);block=tokens[i:i+n+2];i+=n+2
  else:block=[tokens[i]];i+=1
  original.extend(block)
  if block[0]=='-1' and len({display(x) for x in block[2:]})>1:
   split_homonyms.append(dict(ids=block[2:],french=[display(x) for x in block[2:]]));blocks.extend([[x] for x in block[2:]])
  else:blocks.append(block)
letters=['Others']+list('ABCDEFGHIJKLMNOPQRSTUVWXYZ');views={c:[] for c in letters}
for block in blocks:
 text=display(block[2] if block[0]=='-1' else block[0]);k=key(text);initial=k[:1];bucket=initial if initial in views and initial!='Others' else 'Others';views[bucket].append((k,block))
new=['#include "easy_chat.h"','#include "constants/easy_chat.h"',''];after=[];counts={}
for letter in letters:
 view=sorted(views[letter],key=lambda x:x[0]);counts[letter]=len(view);assert len(view)<=270,(letter,len(view))
 new.append('static const u16 sEasyChatWordsByLetter_'+letter+'[] = {')
 for _,block in view:
  after.extend(block)
  if block[0]=='-1':new.append('    -1, '+block[1]+', // Same species in two vocabulary groups')
  for code in block[2:] if block[0]=='-1' else block:new.append('    '+code+',')
 new.extend(['};',''])
assert collections.Counter(x for x in original if x.startswith('EC_'))==collections.Counter(x for x in after if x.startswith('EC_')),'Saved word IDs changed'
new.append('static const struct EasyChatWordsByLetter sEasyChatWordsByLetterPointers[] = {')
for letter in letters:
 count=sum(len(b) for _,b in views[letter]);new.append('    {.words = sEasyChatWordsByLetter_'+letter+', .numWords = '+str(count)+'},')
new.extend(['};','']);p.write_text('\n'.join(new))
report=dict(words_reviewed=len(texts),saved_word_ids_unchanged=True,unlock_flags_unchanged=True,former_homonyms_split=split_homonyms,alphabetical_block_counts=counts,max_alphabetical_blocks=max(counts.values()),capacity=270)
out=ROOT/'docs/traduction-complete-20261024';out.mkdir(exist_ok=True);(out/'TRI_VOCABULAIRE.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False))
