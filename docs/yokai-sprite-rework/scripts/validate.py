#!/usr/bin/env python3
"""Validate candidate files in isolation. Never compiles or changes the game ROM."""
import pathlib,json,zipfile,subprocess,tempfile,hashlib,re,struct,argparse
from PIL import Image
D=pathlib.Path(__file__).resolve().parents[1];R=D.parents[1]
P=argparse.ArgumentParser();P.add_argument('--baseline',type=pathlib.Path);A=P.parse_args()
def sha(b):return hashlib.sha256(b).hexdigest()
def run(*args):return subprocess.check_output(list(map(str,args)),cwd=R)
def decode(raw):
    assert len(raw)==2048
    return bytes((raw[((y//8)*8+x//8)*32+(y%8)*4+(x%8)//2]>>(4*(x%2)))&15 for y in range(64) for x in range(64))
conv=json.loads((D/'conversion.json').read_text());summary=json.loads((D/'summary.json').read_text());previews=json.loads((D/'preview-validation.json').read_text())
checks={'candidate_species':0,'combat_pngs':0,'palette_files_unchanged':0,'preserved_original_views':0,'modified_candidate_views':0,'gba_4bpp_roundtrips':0,'gba_lz77_roundtrips':0,'palette_rgb555_checks':0,'preview_decoder_agreements':0,'missing_resources':[],'rom_linked':False,'emulator_tested':False}
assert summary['examined_species']==151 and len(conv['species'])==51
with zipfile.ZipFile(D/'sources/originals.zip') as z,tempfile.TemporaryDirectory(prefix='yokai-rework-gba-') as tmp:
    T=pathlib.Path(tmp)
    for e in conv['species']:
        n=e['index'];folder=D/'proposals'/f'{n:03}';checks['candidate_species']+=1
        for side in ['front','back']:
            p=folder/f'{side}.png';data=p.read_bytes();assert sha(data)==e['views'][side]['sha256']
            with Image.open(p) as im:
                im.load();assert im.mode=='P' and im.size==(64,64) and im.info.get('transparency')==0
                indices=bytes(im.get_flattened_data());assert max(indices)<16 and 0 in indices and any(indices)
                assert len(im.getpalette())>=48 and data[24:26]==bytes([4,3])
            if e['views'][side]['preserved']:
                assert data==z.read(f'{n:03}/{side}.png');checks['preserved_original_views']+=1
            else:
                assert data!=z.read(f'{n:03}/{side}.png');checks['modified_candidate_views']+=1
            checks['combat_pngs']+=1
            out=T/'view.4bpp';packed=T/'view.4bpp.lz';unpacked=T/'roundtrip.4bpp'
            run(R/'tools/gbagfx/gbagfx',p,out);assert decode(out.read_bytes())==indices;checks['gba_4bpp_roundtrips']+=1
            run(R/'tools/gbagfx/gbagfx',out,packed);run(R/'tools/gbagfx/gbagfx',packed,unpacked);assert unpacked.read_bytes()==out.read_bytes();checks['gba_lz77_roundtrips']+=1
        for kind in ['normal','shiny']:
            p=folder/f'{kind}.pal';data=p.read_bytes();assert data==z.read(f'{n:03}/{kind}.pal');checks['palette_files_unchanged']+=1
            rgb=[tuple(map(int,s.split())) for s in data.decode().splitlines()[3:19]];assert len(rgb)==16
            expected=b''.join(struct.pack('<H',(r>>3)|((g>>3)<<5)|((b>>3)<<10)) for r,g,b in rgb)
            run(R/'tools/gbagfx/gbagfx',p,T/'palette.gbapal');assert (T/'palette.gbapal').read_bytes()==expected;checks['palette_rgb555_checks']+=1
for output in previews['outputs']:
    p=D/output['file'];data=p.read_bytes();assert sha(data)==output['sha256']
    assert data[24:26]==bytes([8,2]) and data[28]==0
    with Image.open(p) as im:
        im.load();assert im.mode=='RGB' and im.size==tuple(output['size'])
        assert len(im.getcolors(im.width*im.height) or [])>20
        expected=im.tobytes()
    actual=run('magick','-limit','thread','1',p,'-depth','8','RGB:-');assert actual==expected
    checks['preview_decoder_agreements']+=1
links=[]
for name in ['README.md','ANALYSE-151.md']:
    for link in re.findall(r'\]\(([^)]+)\)',(D/name).read_text()):
        path=link.split('#')[0]
        if path and path!='technical-validation.json':assert (D/path).is_file(),(name,link)
        links.append(link)
checks['markdown_links_checked']=len(links)
checks['game_protection']={'status':'not_checked_no_local_baseline'}
if A.baseline is not None:
    assert A.baseline.is_file(),A.baseline
    data=A.baseline.read_bytes();baseline=json.loads(data)
    changed=[p for p,h in baseline.items() if not (R/p).is_file() or sha((R/p).read_bytes())!=h]
    assert not changed,changed
    checks['game_protection']={'status':'passed','checked_files':len(baseline),'changed_files':0,'baseline_sha256':sha(data),'rom_sha256_unchanged':baseline.get('pokefirered.gba'),'local_restore_archive':'/workspace/scratch/yokai-rework-phase1-originals.tar.gz'}
assert checks['combat_pngs']==checks['gba_4bpp_roundtrips']==checks['gba_lz77_roundtrips']==102
assert checks['palette_files_unchanged']==checks['palette_rgb555_checks']==102
assert checks['preview_decoder_agreements']==14 and checks['preserved_original_views']==20
checks['artistic_status']='23 proposals for user review; 28 incomplete trials; no user approval; see individual reservations'
(D/'technical-validation.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(checks,ensure_ascii=False,indent=2))
