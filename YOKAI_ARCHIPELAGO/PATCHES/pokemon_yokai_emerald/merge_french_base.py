#!/usr/bin/env python3
"""Fusion locale reproductible AP Flit × décompilation FR, sans ressources Yo-kai.

Résout uniquement le couple de commits verrouillés et ses conflits relus :
logique AP conservée, traductions FR par symbole avec mêmes placeholders.
Le résultat reste une base AP française partielle tant que les nouveaux textes
AP ne sont pas traduits et que le jeu complet n'a pas été testé.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import re
import subprocess
import tarfile

ROOT=Path(__file__).resolve().parents[2]
EXPECTED_CONFLICTS=set('''Makefile
data/maps/DewfordTown_Gym/scripts.inc
data/maps/FortreeCity_Gym/scripts.inc
data/maps/GraniteCave_StevensRoom/scripts.inc
data/maps/LavaridgeTown_Gym_1F/scripts.inc
data/maps/LittlerootTown/scripts.inc
data/maps/LittlerootTown_BrendansHouse_1F/scripts.inc
data/maps/MauvilleCity_BikeShop/scripts.inc
data/maps/MauvilleCity_Gym/scripts.inc
data/maps/MirageTower_4F/scripts.inc
data/maps/MossdeepCity_Gym/scripts.inc
data/maps/OldaleTown/scripts.inc
data/maps/PetalburgCity_Gym/scripts.inc
data/maps/Route103/scripts.inc
data/maps/RustboroCity_DevonCorp_3F/scripts.inc
data/maps/RustboroCity_Gym/scripts.inc
data/maps/SlateportCity_Harbor/scripts.inc
data/maps/SlateportCity_SternsShipyard_1F/scripts.inc
data/maps/SootopolisCity_Gym_1F/scripts.inc
data/scripts/repel.inc
data/text/birch_speech.inc
data/text/match_call.inc
data/text/obtain_item.inc
data/text/pkmn_center_nurse.inc
src/battle_message.c
src/battle_util.c
src/data/credits.h
src/data/region_map/region_map_sections.json
src/data/text/item_descriptions.h
src/strings.c'''.splitlines())
CONFLICT=re.compile(r'^<<<<<<<[^\n]*\n(.*?)^=======\n(.*?)^>>>>>>>[^\n]*\n?',re.M|re.S)
ASM_TEXT=re.compile(r'^(\w+)::?\n((?:[ \t]+\.string[^\n]*(?:\n|$))+)',re.M)
C_TEXT=re.compile(r'^\s*(?:(?:static|extern)\s+)?const u8\s+(\w+)\[\]\s*=\s*',re.M)


def placeholders(text):return sorted(re.findall(r'\{[^{}]+\}',text))


def c_strings(text):
    result={}
    for m in C_TEXT.finditer(text):
        i=m.end();quote=None;escape=False
        while i<len(text):
            ch=text[i]
            if escape:escape=False
            elif quote:
                if ch=='\\':escape=True
                elif ch==quote:quote=None
            elif ch in '\"\'':quote=ch
            elif ch==';':
                result[m[1]]=(m.start(),i+1,text[m.end():i+1]);break
            i+=1
    return result


def localize(text, french, asm):
    replacements=[];skipped=[]
    if asm:
        old={m[1]:m for m in ASM_TEXT.finditer(text)}
        for m in ASM_TEXT.finditer(french):
            if m[1] not in old:continue
            src=old[m[1]]
            if placeholders(src[2])!=placeholders(m[2]):skipped.append(m[1]);continue
            replacements.append((src.start(2),src.end(2),m[2]))
    else:
        old=c_strings(text)
        for key,(_,_,value) in c_strings(french).items():
            if key not in old:continue
            start,end,previous=old[key]
            if placeholders(previous)!=placeholders(value):skipped.append(key);continue
            # Keep declaration/visibility from the AP side; replace only the initializer.
            match=C_TEXT.match(text,start)
            replacements.append((match.end(),end,value))
    for start,end,value in sorted(replacements,reverse=True):text=text[:start]+value+text[end:]
    return text,len(replacements),skipped


def restore_declared_strings(text, french, header):
    """Retain French-only exports referenced by the merged menu code."""
    existing=c_strings(text);restored=[]
    declared=set(re.findall(r'extern const u8\s+(\w+)\[\]',header))
    for key,(start,end,_) in c_strings(french).items():
        if key in declared and key not in existing:
            text+='\n'+french[start:end]+'\n';restored.append(key)
    return text,restored


def git(repo,*args):
    return subprocess.check_output(['git','-C',str(repo),*args],text=True).strip()


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--ap-source',type=Path,required=True)
    p.add_argument('--fr-source',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args(argv)
    lock={e['id']:e for e in json.loads((ROOT/'CONFIG/dependencies.lock.json').read_text())['dependencies']}
    ap=lock['emerald_ap_code']['commit'];fr=lock['emerald_fr']['commit']
    for path,expected in [(a.ap_source,ap),(a.fr_source,fr)]:
        if git(path,'rev-parse','HEAD')!=expected:raise SystemExit(f'Commit inattendu dans {path}')
    if a.output.exists() and any(a.output.iterdir()):raise SystemExit('Le dossier de sortie doit être neuf ou vide')
    try:git(a.ap_source,'cat-file','-e',fr)
    except subprocess.CalledProcessError:
        subprocess.run(['git','-C',str(a.ap_source),'fetch','--filter=blob:none',lock['emerald_fr']['url'],fr],check=True)
    merged=subprocess.run(['git','-C',str(a.ap_source),'merge-tree','--write-tree','--name-only',ap,fr],capture_output=True,text=True)
    if merged.returncode not in (0,1):raise SystemExit(merged.stderr)
    lines=merged.stdout.split('\n\n',1)[0].splitlines();tree=lines[0];conflicts=set(lines[1:])
    if conflicts!=EXPECTED_CONFLICTS:
        raise SystemExit(f'Conflits différents de la résolution relue : {sorted(conflicts ^ EXPECTED_CONFLICTS)}')
    a.output.mkdir(parents=True,exist_ok=True)
    proc=subprocess.Popen(['git','-C',str(a.ap_source),'archive',tree],stdout=subprocess.PIPE)
    with tarfile.open(fileobj=proc.stdout,mode='r|') as archive:archive.extractall(a.output,filter='data')
    if proc.wait()!=0:raise SystemExit('Échec de git archive')
    report={'ap_commit':ap,'fr_commit':fr,'merged_tree':tree,'conflicts':sorted(conflicts),
            'policy':'AP logic; FR strings matched by symbol and placeholder contract',
            'translation_count':0,'placeholder_mismatches':{},'game_tested':False,'yokai_layer_applied':False}
    for name in conflicts:
        target=a.output/name;text=target.read_text();text=CONFLICT.sub(lambda m:m[1],text)
        if name=='src/data/credits.h':
            # The two upstreams use incompatible declaration styles (individual
            # structs versus one-element arrays). A line merge duplicates the
            # entries. Keep the coherent AP layout, then localize its strings.
            text=git(a.ap_source,'show',ap+':'+name)+'\n'
        if '<<<<<<<' in text or '>>>>>>>' in text:raise SystemExit(f'Conflit non résolu : {name}')
        if name=='src/battle_util.c':
            # French upstream renamed this parameter. The AP early return stays.
            text=text.replace('return TRUE; // not good for a randomizer otherwise\n    if (GetBattlerSide(battler) == B_SIDE_OPPONENT)',
                              'return TRUE; // not good for a randomizer otherwise\n    if (GetBattlerSide(battlerId) == B_SIDE_OPPONENT)')
        if name.endswith(('.inc','.c','.h')):
            text,count,skipped=localize(text,(a.fr_source/name).read_text(),name.endswith('.inc'))
            report['translation_count']+=count
            if skipped:report['placeholder_mismatches'][name]=skipped
            if name=='src/strings.c':
                text,restored=restore_declared_strings(text,(a.fr_source/name).read_text(),
                                                      (a.output/'include/strings.h').read_text())
                report['restored_exports']=restored
        elif name.endswith('.json'):
            current=json.loads(text);translated=json.loads((a.fr_source/name).read_text())
            byid={r['id']:r for r in translated['map_sections']}
            for row in current['map_sections']:
                for key in ('name','display_name'):
                    if key in byid.get(row['id'],{}):row[key]=byid[row['id']][key]
            text=json.dumps(current,indent=2,ensure_ascii=False)+'\n'
        target.write_text(text)
    # The zero-diff non-conflicting French changes are already in the merged tree.
    (a.output/'FRENCH_MERGE_REPORT.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps(report,ensure_ascii=False))
    return 0

if __name__=='__main__':raise SystemExit(main())
