#!/usr/bin/env python3
"""Wrap translated standard dialogue with native font widths and name bounds.
Only selected two-line dialogue is wrapped, never fixed menus/credit layouts.
"""
import json,re,sys
from pathlib import Path
from localiser_fr import ROOT,replace
font=(ROOT/'src/text.c').read_text()
widths=list(map(int,re.findall(r'\d+',re.search(r'sFontNormalLatinGlyphWidths\[\]\s*=\s*\{(.*?)\}',font,re.S)[1])))
glyph={m[1]:int(m[2],16) for m in re.finditer(r"^'(.*?)'\s*= ([0-9A-F]{2})$",(ROOT/'charmap.txt').read_text(),re.M)};glyph["'"]=glyph['’']
def sample(token):
    name=token[1:-1]
    if name=='POKEBLOCK':return 'W'*5
    if name in ['PLAYER','B_PLAYER_NAME']:return 'W'*7
    if name=='RIVAL':return 'Matt'
    if name.startswith('B_'):
        if 'NAME_WITH_PREFIX' in name:return 'Ennemi '+'W'*10
        if 'NAME' in name:return 'W'*13 if 'TRAINER' in name or 'LINK_' in name else 'W'*10
        if 'ABILITY' in name:return 'W'*13
        if 'MOVE' in name:return 'W'*12
        if 'ITEM' in name:return 'W'*14
        if 'PREFIX' in name:return 'W'*10
        if 'BUFF' in name:return 'W'*14
    if name.startswith('STR_VAR_') or name.startswith('DYNAMIC '):return 'W'*14
    return ''
def measure(text):
    text=re.sub(r'\{[^}]+\}',lambda m:sample(m[0]),text)
    return sum(widths[glyph[ch]] for ch in text if ch!='$')
def wrap(text):
    result=[];line=0
    for part in re.split(r'(\\[nlp])',text):
        if part in ['\\n','\\l','\\p']:
            result.append(part);line=0 if part=='\\p' else line+1;continue
        # Keep placeholders as atomic words, including control arguments.
        words=re.findall(r'(?:\{[^}]+\}|[^\s{])+',part);current=''
        for word in words:
            candidate=(current+' '+word) if current else word
            if current and measure(candidate)>208:
                result.extend([current,'\\n' if line==0 else '\\l']);line+=1;current=word
            else:current=candidate
        result.append(current)
    return ''.join(result)
def main():
    changed=[]
    for name in sys.argv[1:]:
        path=Path(name);lines=[]
        for row in path.read_text().splitlines():
            if not row or row.startswith('#'):lines.append(row);continue
            source,symbol,text=row.split('\t',2);text=text.replace(r'\s',' ')
            eligible=source.endswith('.inc') or (source=='src/battle_message.c' and ('\\n' in text or ('{B_' in text and not symbol.startswith('gText_'))))
            if eligible and not any(x in text for x in ['{CLEAR','{COLOR','{PALETTE']):
                new=wrap(text)
                if new!=text:
                    replace(ROOT/source,symbol,new);changed.append({'file':source,'symbol':symbol,'before':text,'after':new});text=new
            text=text.rstrip(' ')+r'\s'*(len(text)-len(text.rstrip(' ')))
            lines.append(source+'\t'+symbol+'\t'+text)
        path.write_text('\n'.join(lines)+'\n')
    out=ROOT/'QA_RECETTE_FINALE/LOCALISATION_FR/CADRAGES';out.mkdir(exist_ok=True)
    (out/('-'.join(Path(x).stem for x in sys.argv[1:])+'.json')).write_text(json.dumps({'max_normal_font_pixels':208,'dynamic_names':'Player7; mon10+enemy prefix; item14; move12; ability13; generic variables14 wide W glyphs','scope':'Translated standard battle dialogue and selected ASM dialogue only; fixed menu layouts excluded','changed':changed},ensure_ascii=False,indent=2)+'\n');print('Wrapped',len(changed),'dialogues')
if __name__=='__main__':main()
