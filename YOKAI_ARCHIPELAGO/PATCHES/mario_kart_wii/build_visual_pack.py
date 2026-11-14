#!/usr/bin/env python3
"""Assemble un pack Riivolution visuel PAL, à partir de VOS fichiers .szs.

Aucun mod, ISO, circuit ou code PowerPC n'est téléchargé ou embarqué. Les chemins
disc sont ceux indiqués par l'auteur du mod dans un manifeste local explicite.
"""
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path,PurePosixPath
import shutil
import xml.etree.ElementTree as ET

ALLOWED=('/Race/Driver/','/Race/Kart/','/Scene/UI/')


def build(manifest,output,iso=None,replace=False):
    data=json.loads(manifest.read_text())
    if data.get('game_id')!='RMCP01':raise ValueError('Le client AP exige Mario Kart Wii PAL RMCP01')
    if iso:
        with iso.open('rb') as f:identifier=f.read(6)
        if identifier!=b'RMCP01':raise ValueError('L’image fournie n’est pas un ISO PAL RMCP01 ; aucun patch appliqué')
    if not data.get('files'):raise ValueError('Ajouter les fichiers du mod au manifeste, sans les publier dans Git')
    plan=[]
    for i,row in enumerate(data['files']):
        disc=row['disc'];parts=PurePosixPath(disc).parts
        if '..' in parts or not disc.startswith(ALLOWED) or not disc.lower().endswith('.szs'):
            raise ValueError('Seuls les modèles/portraits sont autorisés, jamais les circuits ou paramètres : '+disc)
        source=(manifest.parent/row['source']).resolve()
        if not source.is_file() or source.suffix.lower()!='.szs':raise ValueError('Archive visuelle .szs manquante : '+row['source'])
        if source.read_bytes()[:4] not in (b'Yaz0',bytes.fromhex('55aa382d')):
            raise ValueError('Le fichier n’est pas une archive SZS/U8 reconnue : '+row['source'])
        digest=hashlib.sha256(source.read_bytes()).hexdigest()
        if row.get('sha256') and row['sha256']!=digest:raise ValueError('SHA-256 différent pour '+row['source'])
        external=Path('yokai_mkw/assets')/f'{i:03d}_{source.name}'
        plan.append((source,external,disc,digest))
    xmlpath=output/'riivolution/yokai-mkw.xml'
    owned=[xmlpath,output/'yokai_mkw/INSTALLATION.json']+[output/e for _,e,_,_ in plan]
    if not replace and any(p.exists() for p in owned):raise ValueError('Un pack Yo-kai existe déjà : conserver sa copie ou utiliser --replace')
    root=ET.Element('wiidisc',version='1');ET.SubElement(root,'id',game='RMCP',developer='01')
    options=ET.SubElement(root,'options');section=ET.SubElement(options,'section',name='Yo-kai Watch × Archipelago')
    option=ET.SubElement(section,'option',name='Personnages et portraits Yo-kai',default='1')
    choice=ET.SubElement(option,'choice',name='Activés');ET.SubElement(choice,'patch',id='yokai_visuals')
    patch=ET.SubElement(root,'patch',id='yokai_visuals')
    for source,external,disc,digest in plan:
        target=output/external;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,target)
        ET.SubElement(patch,'file',disc=disc,external='/'+external.as_posix(),resize='true',create='false')
    ET.indent(root);xmlpath.parent.mkdir(parents=True,exist_ok=True)
    ET.ElementTree(root).write(xmlpath,encoding='utf-8',xml_declaration=True)
    result={'game_id':'RMCP01','name':data.get('name','Pack visuel Yo-kai personnel'),
            'native_ap_game':'Mario Kart Wii','characters':data.get('characters',[]),
            'same_dolphin_instance_required':True,'emulation_tested':False,
            'mod_credit':data.get('credit'),'source_url':data.get('source_url'),
            'files':[{'disc':d,'external':e.as_posix(),'sha256':h} for _,e,d,h in plan]}
    (output/'yokai_mkw/INSTALLATION.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('manifest',type=Path);p.add_argument('--output',type=Path,required=True)
    p.add_argument('--iso',type=Path);p.add_argument('--replace',action='store_true');a=p.parse_args()
    try:print(json.dumps(build(a.manifest,a.output,a.iso,a.replace),indent=2,ensure_ascii=False))
    except (ValueError,OSError) as e:p.exit(2,str(e)+'\n')

if __name__=='__main__':main()
