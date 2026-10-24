#!/usr/bin/env python3
"""Inventory visible source literals. English detection is a triage heuristic,
never proof that unflagged text is French or that every screen was tested.
"""
import argparse,collections,csv,json,re,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[2];Q=R/'QA_RECETTE_FINALE/LOCALISATION_FR';Q.mkdir(exist_ok=True)
EN=re.compile(r"\b(the|this|that|your|you|with|was|were|would|can't|don't|have|has|been|from|please|what|which|will|when|how|are|is|it|to|and|for|of|not|can|want|battle|moves|wild|trainer|caught)\b",re.I)
def entries(path,text):
    if path.suffix in ('.inc', '.s'):
        for m in re.finditer(r'^(\w+)::?\n((?:[ \t]*\.string "(?:\\.|[^"\\])*"[^\n]*\n)+)',text,re.M):
            yield m[1],text[:m.start()].count('\n')+1,''.join(re.findall(r'\.string "((?:\\.|[^"\\])*)"',m[2]))
    else:
        for m in re.finditer(r'_\(\s*((?:"(?:\\.|[^"\\])*"\s*)+)\)',text):
            prefix=text[max(0,m.start()-160):m.start()];ids=re.findall(r'\b(\w+)\s*(?:\[[^\]]*\])?\s*=',prefix)
            yield ids[-1] if ids else '',text[:m.start()].count('\n')+1,''.join(re.findall(r'"((?:\\.|[^"\\])*)"',m[1]))
def main():
    p=argparse.ArgumentParser();p.add_argument('--baseline');p.add_argument('--output',type=Path,default=Q);a=p.parse_args();rows=[]
    out=a.output;out.mkdir(parents=True,exist_ok=True)
    for path in sorted(list((R/'data').rglob('*.inc'))+list((R/'data').rglob('*.s'))+list((R/'src').rglob('*.c'))+list((R/'src').rglob('*.h'))):
        rel=str(path.relative_to(R))
        if a.baseline:
            res=subprocess.run(['git','show',a.baseline+':'+rel],cwd=R,capture_output=True,text=True)
            if res.returncode:continue
            text=res.stdout
        else:text=path.read_text()
        for label,line,value in entries(path,text):
            clean=re.sub(r'\{[^}]*\}|\\[nlp]|\$', ' ',value)
            if not re.search(r'[A-Za-zÀ-ÿ\u3040-\u30ff]',clean):continue
            rows.append(dict(file=rel,symbol=label,line=line,text=value,english_candidate=bool(EN.search(clean)),japanese_candidate=bool(re.search(r'[\u3040-\u30ff]',clean))))
    suffix='_AVANT' if a.baseline else ''
    fields=['file','symbol','line','text','english_candidate','japanese_candidate']
    with (out/f'INVENTAIRE{suffix}.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,lineterminator='\n');w.writeheader();w.writerows(rows)
    candidates=[x for x in rows if x['english_candidate'] or x['japanese_candidate']]
    counts=collections.Counter(x['file'] for x in candidates)
    report=dict(source_reference=a.baseline or 'working tree',visible_literals=len(rows),english_candidates=sum(x['english_candidate'] for x in rows),japanese_candidates=sum(x['japanese_candidate'] for x in rows),files_to_review=dict(counts.most_common()),warning='Heuristic triage only. Proper names, unused legacy text and mixed-language text require contextual review. JSON-generated item text and bitmap text require separate inspection.')
    (out/f'COUVERTURE{suffix}.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='files_to_review'},ensure_ascii=False));print(list(counts.most_common(15)))
if __name__=='__main__':main()
