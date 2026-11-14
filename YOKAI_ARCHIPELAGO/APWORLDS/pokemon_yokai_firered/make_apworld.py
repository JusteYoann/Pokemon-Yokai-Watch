#!/usr/bin/env python3
"""Package le code propre au mode bonus et son profil mesuré ; aucune ROM ni image."""
import argparse,json
from pathlib import Path
import zipfile

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--profile',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    profile=json.loads(a.profile.read_text())
    if profile['base_sha1']!='40c59a9f240d29a7b16d1dd299b1125513a280c4' or profile['mode']!='bonus':
        p.error('Profil incompatible')
    a.out.mkdir(parents=True,exist_ok=True);output=a.out/'pokemon_yokai_firered.apworld';root=Path(__file__).parent
    with zipfile.ZipFile(output,'w',zipfile.ZIP_DEFLATED) as z:
        for name in ['__init__.py','client.py','archipelago.json']:
            z.write(root/name,'pokemon_yokai_firered/'+name)
        z.writestr('pokemon_yokai_firered/build.json',json.dumps(profile,indent=2)+'\n')
    print(output)

if __name__=='__main__':main()
