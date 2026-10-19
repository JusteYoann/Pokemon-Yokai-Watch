#!/usr/bin/env python3
"""Apply reviewed French text by symbol, without touching identifiers or scripts.

TSV format: source-path<TAB>symbol<TAB>French text, with literal engine escapes.
Control placeholders must be identical, including repeated occurrences.
"""
import argparse,collections,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def controls(text):
    return collections.Counter(re.findall(r'\{[^}]+\}|\\(?:x[0-9a-fA-F]{2}|[0-9]{1,3})',text))
def replace(path,symbol,new):
    text=path.read_text()
    if path.suffix=='.inc':
        pattern=re.compile(r'(^'+re.escape(symbol)+r'::?\n)((?:[ \t]*\.string "(?:\\.|[^"\\])*"[^\n]*\n)+)',re.M)
        matches=list(pattern.finditer(text));assert len(matches)==1,(path,symbol,len(matches))
        m=matches[0];old=''.join(re.findall(r'\.string "((?:\\.|[^"\\])*)"',m[2]));value=m[1]+'    .string "'+new+'"\n'
    else:
        pattern=re.compile(r'((?:static\s+)?const\s+u8\s+'+re.escape(symbol)+r'\s*(?:\[[^\]]*\])+\s*=\s*_\(\s*)((?:"(?:\\.|[^"\\])*"\s*)+)(\))')
        matches=list(pattern.finditer(text));assert len(matches)==1,(path,symbol,len(matches))
        m=matches[0];old=''.join(re.findall(r'"((?:\\.|[^"\\])*)"',m[2]));value=m[1]+'"'+new+'"'+m[3]
    assert controls(old)==controls(new),(path,symbol,'placeholder mismatch',controls(old),controls(new))
    assert not any(c in new for c in ['"','\t','\n','\r']),(path,symbol,'Use escaped line breaks and engine quotes')
    if old==new:return False
    path.write_text(text[:m.start()]+value+text[m.end():]);return True
def main():
    p=argparse.ArgumentParser();p.add_argument('tables',nargs='+',type=Path);a=p.parse_args();count=0;files=set()
    for table in a.tables:
        for line in table.read_text().splitlines():
            if not line or line.startswith('#'):continue
            source,symbol,translation=line.split('\t',2);translation=translation.replace(r'\s',' ');path=ROOT/source
            if replace(path,symbol,translation):count+=1;files.add(source)
    print(json.dumps({'changed_texts':count,'files':len(files)}))
if __name__=='__main__':main()
