#!/usr/bin/env python3
"""Ajoute le canal AP sur une COPIE du snapshot RC1 exact ; ne modifie jamais la source d'entrée."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import shutil
from expand_checks import build_catalog

HERE=Path(__file__).resolve().parent
EXPECTED='4192f6ac785eed8a431fdbb322712818c31c4bfd9573e647ee791b04452ed329'


def replace_once(text,old,new):
    if text.count(old)!=1:raise ValueError(f'Ancre différente du snapshot RC1 : {old[:70]!r}')
    return text.replace(old,new,1)


def prepare(source,output):
    source=source.resolve();output=output.resolve()
    if source==output or source.is_relative_to(output) or output.is_relative_to(source):
        raise ValueError('La sortie doit être une copie séparée, hors de la source')
    if output.exists():raise ValueError('Le dossier de sortie existe déjà ; aucun écrasement automatique')
    metadata=json.loads((source/'SOURCE_ROM05.json').read_text())
    if metadata.get('expected_sha256')!=EXPECTED:raise ValueError('Ce ne sont pas les sources RC1 de la ROM05')
    # Validate original inputs, not merely a user-supplied version label.
    manifest=json.loads((source/'SOURCE_FILES_SHA256.json').read_text())
    for relative,digest in manifest.items():
        if not relative.startswith(('src/','include/','data/','graphics/','private/')) and relative not in ['Makefile','config.mk','ld_script.ld']:
            continue
        path=source/relative
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest()!=digest:
            raise ValueError(f'Snapshot modifié : {relative}. Préserver cette variante et fournir RC1 séparément.')
    ignore=shutil.ignore_patterns('.git','build','__pycache__','*.o','*.d','*.elf','*.map','*.sym','*.sav','*.sgm')
    shutil.copytree(source,output,ignore=ignore)
    for p in output.glob('*.gba'):p.unlink()  # generated outputs only, not data/mb_*.gba payloads
    return install(output)


def install(output):
    """Apply once to a separate, clean baseline checkout (including source worktrees)."""
    for name,target in [('yokai_ap.c','src'),('yokai_ap.h','include')]:
        shutil.copy2(HERE/'native'/name,output/target/name)
    p=output/'src/overworld.c';s=p.read_text()
    s=replace_once(s,'#include "global.h"\n','#include "global.h"\n#include "yokai_ap.h"\n')
    anchor='    TerreHeureFogUpdate();\n    UpdateTilesetAnimations();\n    DoScheduledBgTilemapCopiesToVram();\n}'
    s=replace_once(s,anchor,anchor[:-2]+'\n    if (gMain.callback2 == CB2_Overworld) YokaiAPUpdate();\n}')
    p.write_text(s)
    p=output/'ld_script.ld';s=p.read_text()
    s=replace_once(s,'        src/manoir_perfide.o(.text .rodata);\n',
                   '        src/manoir_perfide.o(.text .rodata);\n        src/yokai_ap.o(.text .rodata);\n')
    p.write_text(s)
    catalog=build_catalog(output)
    # YoppleInDungeon means "map supports the vacuum", not "vacuum busy".
    # Read-only getter: don't suppress all AP communication in ordinary caves.
    p=output/'src/yopple_devices.c';s=p.read_text()
    s=replace_once(s,'bool8 YoppleInDungeon(void){return VacuumMap()!=NULL;}',
        'bool8 YoppleInDungeon(void){return VacuumMap()!=NULL;}\n'
        'bool8 YoppleAPBusy(void){struct VacuumSave *s=State();return s->magic==VACUUM_MAGIC && s->phase!=0;}')
    p.write_text(s)
    p=output/'include/yopple_devices.h';s=p.read_text()
    s=replace_once(s,'bool8 YoppleInDungeon(void);','bool8 YoppleInDungeon(void);\nbool8 YoppleAPBusy(void);');p.write_text(s)
    active=[c for c in catalog['checks'] if c['status']=='active']
    pickups=[c for c in active if c.get('original_reward')=='replaced']
    legacy={c['id']:c for c in active}
    legacy_flags=[legacy[code]['flag'] for code in catalog['legacy_pickup_ids']]
    allowed=set(c['original_item'] for c in pickups)|{'ITEM_POTION','ITEM_SUPER_POTION','ITEM_HYPER_POTION',
        'ITEM_POKE_BALL','ITEM_GREAT_BALL','ITEM_ULTRA_BALL','ITEM_REPEL','ITEM_SUPER_REPEL','ITEM_MAX_REPEL',
        'ITEM_ANTIDOTE','ITEM_PARALYZE_HEAL','ITEM_AWAKENING','ITEM_BURN_HEAL','ITEM_ICE_HEAL'}
    header=f'#define YOKAI_AP_PICKUP_COUNT {len(pickups)}\n#define YOKAI_AP_CHECK_COUNT {len(active)}\n'
    header+=f'#define YOKAI_AP_CATALOG_HASH "{catalog["catalog_sha256"]}"\n'
    for name,values in [('sYokaiAPPickupFlags',[c['flag'] for c in pickups]),('sYokaiAPLegacyFlags',legacy_flags),('sYokaiAPAllowedItems',sorted(allowed))]:
        header+='static const u16 '+name+'[] = {\n'+''.join('    '+v+',\n' for v in values)+'};\n'
    header+='static const u16 sYokaiAPCheckData[][3] = {\n'+''.join(
        '    {'+str(0xFFFE if c['kind']=='trainer' else 0xFFFD if c['kind']=='pokedex' else c.get('flag_value',0))+', '
        +str(c['persistent_index'] if c['kind']=='trainer' else c['dex_number'] if c['kind']=='pokedex' else c.get('variable_value',0))+', '
        +str(c.get('target_value',0))+'},\n' for c in active)+'};\n'
    header+='static const u16 sYokaiAPTrainerSlots[][2] = {\n'+''.join(
        f'    {{{trainer}, {c["persistent_index"]}}},\n' for c in active if c['kind']=='trainer' for trainer in c['trainer_ids'])+'};\n'
    (output/'include/yokai_ap_checks.h').write_text(header)
    p=output/'src/battle_setup.c';s=p.read_text()
    s=replace_once(s,'#include "global.h"\n','#include "global.h"\n#include "yokai_ap.h"\n')
    anchor='    if (sTrainerBattleMode == TRAINER_BATTLE_EARLY_RIVAL)\n'
    # This anchor is scoped to the actual end callback, after special modes return.
    start=s.index('static void CB2_EndTrainerBattle(void)\n{')
    tail=s[start:];tail=replace_once(tail,anchor,
        '    if (gBattleOutcome == B_OUTCOME_WON) YokaiAPTrainerVictory(gTrainerBattleOpponent_A);\n'+anchor)
    s=s[:start]+tail
    s=replace_once(s,'void SetTrainerFlag(u16 trainerId)\n{\n    FlagSet(TRAINER_FLAGS_START + trainerId);\n}',
        'void SetTrainerFlag(u16 trainerId)\n{\n    if (YokaiAPKeepTrainerAvailable(trainerId)) return;\n    FlagSet(TRAINER_FLAGS_START + trainerId);\n}')
    p.write_text(s)
    p=output/'data/scripts/item_ball_scripts.inc';s=p.read_text()
    for c in active:
        if c['kind']!='ball':continue
        old=c['script']+'::\n\tfinditem '+c['original_item']+'\n\tend'
        new=(c['script']+'::\n\tlock\n\tfaceplayer\n\tsetvar VAR_0x8004, '+c['flag']
             +'\n\tcallnative YokaiAPTryCollect\n\tgoto_if_eq VAR_RESULT, 2, YokaiAP_ConnectFirst'
             +'\n\tremoveobject VAR_LAST_TALKED\n\tmsgbox YokaiAP_TextCheck, MSGBOX_DEFAULT\n\trelease\n\tend')
        s=replace_once(s,old,new)
    s+='''
YokaiAP_ConnectFirst::
\tmsgbox YokaiAP_TextConnect, MSGBOX_DEFAULT
\treleaseall
\tend

YokaiAP_HiddenCollected::
\tmsgbox YokaiAP_TextCheck, MSGBOX_DEFAULT
\treleaseall
\tend

YokaiAP_TextCheck::
\t.string "Emplacement Archipelago validé !$"

YokaiAP_TextConnect::
\t.string "Connecte le client Archipelago\\n"
\t.string "avant de prendre cet objet.$"
'''
    p.write_text(s)
    # Keep native caught-count tests and refusal paths. Only replace the reward.
    for c in active:
        if c['kind']!='npc_gift':continue
        p=output/c['source'];s=p.read_text();import re
        label=re.search(r'^'+re.escape(c['gift_label'])+r'::?\s*(?:@[^\n]*)?$',s,re.M)
        if label is None:raise ValueError('Gift label changed: '+c['gift_label'])
        end=re.search(r'^\w+::?',s[label.end():],re.M)
        finish=label.end()+end.start() if end else len(s)
        body=s[label.end():finish]
        body=re.sub(r'\tcheckitemspace '+re.escape(c['original_item'])+r'(?:,\s*1)?\n\tgoto_if_eq VAR_RESULT, FALSE, \w+\n','',body,count=1)
        body=replace_once(body,c['gift_macro'],'setvar VAR_0x8004, '+c['flag']+'\n\tcallnative YokaiAPTryCollect\n'
            '\tgoto_if_eq VAR_RESULT, 2, YokaiAP_ConnectFirst\n\tmsgbox YokaiAP_TextCheck, MSGBOX_DEFAULT\n\tsetvar VAR_RESULT, TRUE')
        p.write_text(s[:label.end()]+body+s[finish:])
    for c in active:
        if c['kind']!='aide':continue
        p=output/c['source'];s=p.read_text()
        import re
        pattern=r'\tcheckitemspace '+c['original_item']+r'\n\tgoto_if_eq VAR_RESULT, FALSE, \w+\n\tgiveitem_msg [^\n]+'
        match=re.search(pattern,s)
        if match is None:raise ValueError('Aide gift anchor differs: '+c['source'])
        s=replace_once(s,match[0],'\tsetvar VAR_0x8004, '+c['flag']+'\n\tcallnative YokaiAPTryCollect\n'
            '\tgoto_if_eq VAR_RESULT, 2, YokaiAP_ConnectFirst\n\tmsgbox YokaiAP_TextCheck, MSGBOX_DEFAULT')
        p.write_text(s)
    p=output/'data/scripts/obtain_item.inc';s=p.read_text()
    s=replace_once(s,'EventScript_HiddenItemScript::\n\tlockall\n',
        'EventScript_HiddenItemScript::\n\tlockall\n\tcallnative YokaiAPTryCollect\n'
        '\tgoto_if_eq VAR_RESULT, 1, YokaiAP_HiddenCollected\n'
        '\tgoto_if_eq VAR_RESULT, 2, YokaiAP_ConnectFirst\n')
    p.write_text(s)
    p=output/'data/maps/SafariZone_SecretHouse/scripts.inc';s=p.read_text()
    s=replace_once(s,'\tcheckitemspace ITEM_HM03\n\tgoto_if_eq VAR_RESULT, FALSE, SafariZone_SecretHouse_EventScript_NoRoomForHM03\n'
        '\tgiveitem_msg SafariZone_SecretHouse_Text_ReceivedHM03FromAttendant, ITEM_HM03',
        '\tsetvar VAR_0x8004, FLAG_GOT_HM03\n\tcallnative YokaiAPTryCollect\n'
        '\tgoto_if_eq VAR_RESULT, 2, YokaiAP_ConnectFirst\n\tmsgbox YokaiAP_TextCheck, MSGBOX_DEFAULT')
    p.write_text(s)
    report={'base_sha256':EXPECTED,'mode':'classic_bulk','catalog_sha256':catalog['catalog_sha256'],'modified':['src/overworld.c','src/battle_setup.c','ld_script.ld','data/scripts/item_ball_scripts.inc','data/scripts/obtain_item.inc'],
            'added':['src/yokai_ap.c','include/yokai_ap.h','include/yokai_ap_checks.h'],'save_storage':{'block':2,'offset':'0xE20','bytes':64},
            'replaced_pickups':[c['flag'] for c in pickups],
            'preserved':['species','stats','learnsets','evolutions','encounters','trainers','maps','story','other_original_rewards']}
    report['modified'].append('data/maps/SafariZone_SecretHouse/scripts.inc')
    report['modified'] += ['src/yopple_devices.c','include/yopple_devices.h']
    report['modified'] += [c['source'] for c in active if c['kind']=='aide']
    report['modified'] += [c['source'] for c in active if c['kind']=='npc_gift']
    report['modified']=sorted(set(report['modified']))
    (output/'YOKAI_AP_SOURCE_PATCH.json').write_text(json.dumps(report,indent=2)+'\n')
    return report


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--source',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args()
    try:print(json.dumps(prepare(a.source,a.output),indent=2))
    except (ValueError,OSError) as e:p.exit(2,str(e)+'\n')

if __name__=='__main__':main()
