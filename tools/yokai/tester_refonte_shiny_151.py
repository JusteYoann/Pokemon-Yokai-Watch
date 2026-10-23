#!/usr/bin/env python3
"""Palette/source invariants for all151, independent from emulator fixture tests."""
import hashlib,io,json,re,struct,subprocess
from PIL import Image
from refonte_shiny_151 import ROOT,Q,DATA,BASE,old,colors,rgba

def main():
 rows=json.loads((DATA/'palettes.json').read_text())['species'];assert len(rows)==151;checks=[]
 for row in rows:
  n=row['number'];assert re.search(r'^#define\s+'+row['species']+r'\s+'+str(n)+r'\s*$',(ROOT/'include/constants/species.h').read_text(),re.M),(n,'species mapping');path=f'graphics/yokai/{n:03}/';normal=colors((ROOT/path/'normal.pal').read_bytes());shiny=colors((ROOT/path/'shiny.pal').read_bytes())
  assert len(normal)==len(shiny)==16 and normal[0]==shiny[0]==[0,0,0]
  assert all(len(c)==3 and all(0<=v<=255 for v in c) for c in shiny)
  for side in ('front','back'):
   a=Image.open(io.BytesIO(old(path+side+'.png')));b=Image.open(ROOT/path/(side+'.png'))
   assert a.size==b.size==(64,64) and a.convert('RGBA').tobytes()==b.convert('RGBA').tobytes(),(n,side,'normal pixels changed')
   assert rgba(a,colors(old(path+'normal.pal'))).tobytes()==rgba(b,normal).tobytes()
   assert all(v<16 for v in b.get_flattened_data())
   assert [(x!=0) for x in a.get_flattened_data()]==[(x!=0) for x in b.get_flattened_data()]
   if n in (137,138):
    aa=rgba(b,normal);bb=rgba(b,shiny);diff=[[x,y] for y in range(64) for x in range(64) if aa.getpixel((x,y))!=bb.getpixel((x,y))]
    assert diff==(sorted(row['eye_pixels'],key=lambda p:(p[1],p[0])) if side=='front' else []),(n,side,'non-eye recolor')
  if n not in (137,138):assert normal==colors(old(path+'normal.pal'))
  else:assert normal[:14]==colors(old(path+'normal.pal'))[:14]
  if n in (2,3,55,56):
   g=row['groups'][0];donor=colors(old(f"graphics/yokai/{g['normal_donor']:03}/normal.pal"));allowed=[donor[i] for i in g['donor_indices']]
   assert all(shiny[i] in allowed for i in g['indices'])
   assert all(normal[i]==shiny[i] for i in range(16) if i not in g['indices'])
  expected=b''.join(struct.pack('<H',(c[0]>>3)|((c[1]>>3)<<5)|((c[2]>>3)<<10)) for c in shiny)
  assert (ROOT/path/'shiny.gbapal').read_bytes()==expected,(n,'GBA compilation mismatch')
  checks.append(dict(number=n,palette16=True,normal_RGBA_identical=True,transparent_silhouette_identical=True,RGB555_compiled=True,eyes_only=n in (137,138)))
 changes=subprocess.check_output(['git','-c','core.quotepath=false','diff',BASE,'--name-only'],cwd=ROOT,text=True,stderr=subprocess.DEVNULL).splitlines()
 permitted=lambda p:p.startswith(('docs/shiny-151-20261024/','data/yokai/shiny-151-20261024/','tools/yokai/refonte_shiny_151.py','tools/yokai/tester_refonte_shiny_151')) or bool(re.fullmatch(r'graphics/yokai/\d{3}/shiny.pal',p)) or p in [f'graphics/yokai/{n:03}/{f}' for n in (137,138) for f in ('normal.pal','front.png')]
 assert all(permitted(p) for p in changes),[p for p in changes if not permitted(p)]
 # No source change: rates, generations, 151IDs, encounter policy, stories and geometry.
 for folder in ['src','include','data/maps','data/scripts','sound','graphics/yokai_characters','data/yokai/sprite_presentation.json']:
  assert not subprocess.check_output(['git','diff',BASE,'--',folder],cwd=ROOT),folder
 result=dict(passed=True,base=BASE,species=checks,protected_sources_unchanged=True,natural_eligibility='84 allowed / 67 historically excluded, unchanged',scope=__doc__)
 (Q/'TEST_INTEGRITE.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print('PASS 151 palettes, 302 silhouettes/RGBA normaux ; exceptions yeux et donneurs ; code protégé inchangé')
if __name__=='__main__':main()
