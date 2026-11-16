#!/usr/bin/env python3
"""Package le code Archipelago Rouge Feu et son profil mesuré ; aucune ROM ni image."""
import argparse,json
from pathlib import Path
import zipfile

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--profile',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    profile=json.loads(a.profile.read_text())
    if profile['base_sha1']!='40c59a9f240d29a7b16d1dd299b1125513a280c4' or profile['mode']!='classic_bulk':
        p.error('Profil incompatible')
    a.out.mkdir(parents=True,exist_ok=True);output=a.out/'pokemon_yokai_firered.apworld';root=Path(__file__).parent
    if json.loads((root/'checks.json').read_text())['catalog_sha256']!=profile['catalog_sha256']:
        p.error('Le catalogue ne correspond pas à cette compilation')
    with zipfile.ZipFile(output,'w',zipfile.ZIP_DEFLATED) as z:
        for name in ['__init__.py','client.py','archipelago.json','checks.json']:
            z.write(root/name,'pokemon_yokai_firered/'+name)
        z.write(root.parent.parent/'THIRD_PARTY/FRLG_LICENSE.txt','pokemon_yokai_firered/FRLG_LICENSE.txt')
        z.writestr('pokemon_yokai_firered/build.json',json.dumps(profile,indent=2)+'\n')
    print(output)

if __name__=='__main__':main()
