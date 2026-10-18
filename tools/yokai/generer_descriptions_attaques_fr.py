#!/usr/bin/env python3
"""Author-reviewed Gen3 French descriptions, wrapped using the actual native font table."""
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def main():
 source=ROOT/'data/yokai/move_descriptions_fr.txt';rows={int(n):s for n,s in (l.split('|',1) for l in source.read_text().splitlines())};assert sorted(rows)==list(range(1,355))
 glyph={m[1]:int(m[2],16) for m in re.finditer(r"^'(.*?)'\s*= ([0-9A-F]{2})$",(ROOT/'charmap.txt').read_text(),re.M)};glyph["'"]=glyph['’']
 font=list(map(int,re.findall(r'\d+',re.search(r'static const u8 sFontNormalLatinGlyphWidths\[\]\s*=\s*\{(.*?)\}',(ROOT/'src/text.c').read_text(),re.S)[1])))
 def width(s):return sum(font[glyph[c]] for c in s)
 text=(ROOT/'src/move_descriptions.c').read_text();ids={k:int(v) for k,v in re.findall(r'^#define\s+(MOVE_\w+)\s+(\d+)\b',(ROOT/'include/constants/moves.h').read_text(),re.M)};symbols={ids[m]:s for m,s in re.findall(r'\[(MOVE_\w+)\s*-\s*1\]\s*=\s*(gMoveDescription_\w+)',text)};assert sorted(symbols)==list(range(1,355));proof=[]
 for n,desc in rows.items():
  lines=['']
  for word in desc.split():
   assert width(word)<=112,(n,'Word too wide',word)
   trial=(lines[-1]+' '+word).strip()
   if width(trial)<=112:lines[-1]=trial
   else:lines.append(word)
  assert len(lines)<=4,(n,desc,lines)
  literal='\\n'.join(lines);pattern=r'(const u8 '+symbols[n]+r'\[\]\s*=\s*_\(")(.*?)("\);)';text,count=re.subn(pattern,lambda m:m[1]+literal+m[3],text,flags=re.S);assert count==1
  proof.append(dict(move_id=n,symbol=symbols[n],text=desc,lines=lines,widths=[width(s) for s in lines]))
 (ROOT/'src/move_descriptions.c').write_text(text)
 out=ROOT/'QA_RECETTE_FINALE/POST_B13/traduction';out.mkdir(exist_ok=True);(out/'DESCRIPTIONS_354.json').write_text(json.dumps({'scope':'354 original concise French descriptions based on native Gen3 effects; source font widths, not yet actual menu rendering','max_line_pixels':112,'max_lines':4,'entries':proof},ensure_ascii=False,indent=2)+'\n');print('PASS',len(proof),'wrapped descriptions')
if __name__=='__main__':main()
