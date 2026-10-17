#!/usr/bin/env python3
"""Check evidence cardinality, music isolation and exact pre-existing file hashes."""
from pathlib import Path
import csv,json,hashlib,subprocess,re,tarfile
from PIL import Image
R=Path(__file__).resolve().parents[3];D=R/'docs/musique-audit';B=R.parent/'scratch/music-before'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rows(file):return list(csv.DictReader((D/file).open(encoding='utf-8-sig'),delimiter=';'))
audio=json.loads((D/'preuves/ANALYSE_AUDIO.json').read_text());assert len(audio)==80 and all(e['full_decode_passed'] for e in audio)
inv=rows('INVENTAIRE_OST.csv');assert len(inv)==80 and {e['id'] for e in inv}=={e['id'] for e in audio}
assert next(e for e in inv if e['id']=='BL-92f81647')['piste']=='28.5'
proposals=rows('PROPOSITION_BANDE_SON.csv');selected={e['candidat_id'] for e in proposals if e['candidat_id']};rejected={e['id'] for e in rows('MUSIQUES_ECARTEES.csv')};assert len(selected)==22 and len(rejected)==58 and not selected&rejected and selected|rejected=={e['id'] for e in inv}
assert all(e['decision'] in ['CONSERVER','A_VALIDER','REMPLACER'] for e in proposals);assert not any(e['decision']=='REMPLACER' for e in proposals)
assert all(e['decision']=='A_VALIDER' for e in proposals if e['candidat_id'])
assert len(rows('ARCHIVES_ET_ACCES.csv'))==14
assert len(rows('EMPLACEMENTS_MUSICAUX_KANTO.csv'))==91 and len(rows('MUSIQUES_PAR_CARTE.csv'))==425 and len(rows('CAMEOS_AUDIO.csv'))==20
assert not any(p.suffix.lower() in ['.mp3','.wav','.ogg','.flac','.rar','.zip','.gba','.mid','.midi'] for p in D.rglob('*') if p.is_file())
for e in audio:
 p=Path(e['local_path']);assert sha(p)==e['sha256']
 with Image.open(D/'preuves'/(e['id']+'.png')) as im:im.load();assert im.format=='PNG' and im.size==(1000,400) and len(im.convert('RGB').getcolors(400001) or[])>20
baseline=json.loads((B/'manifest.json').read_text());changed=[]
for name,h in baseline.items():
 p=R/name
 if not p.exists() or sha(p)!=h:changed.append(name)
assert not changed,changed
romhash=sha(R/'pokefirered.gba');assert romhash=='84d3bffbb7e74322aa69d5df211f774576d00b1e3e16eec3794c5b74fc66e186'
checkpoint='145044ec29f4ad7ee03c1942e8a925d15a9f89e1';assert subprocess.check_output(['git','rev-parse','qa/recette-finale'],text=True).strip()==checkpoint
subprocess.run(['git','merge-base','--is-ancestor',checkpoint,'HEAD'],check=True)
with tarfile.open(B/'sources-and-derived.tar.gz') as tar:
 assert len(tar.getmembers())==len(baseline)
 for name,h in baseline.items():assert hashlib.sha256(tar.extractfile(name).read()).hexdigest()==h,('backup content',name)
checkfile=D/'preuves/PRESERVATION_ET_VALIDATION.json'
checkfile.write_text(json.dumps({'status':'passed','qa_checkpoint_commit':checkpoint,'audit_branch':subprocess.check_output(['git','branch','--show-current'],text=True).strip(),'snapshot_files_exactly_preserved':len(baseline),'changed_preexisting_files':changed,'rom_sha256':romhash,'raw_music_in_audit_directory':False,'audio_files_decoded_in_full':80,'signal_analysis_seconds':sum(e['duration_seconds'] for e in audio),'perceptual_listening_count':0,'selected_reference_ids':sorted(selected),'unselected_reference_ids':sorted(rejected),'slots':91,'maps':425,'cameo_parties':20,'build_recheck':'make -j4: Nothing to be done; existing ROM preserved, no musical integration tested','transfer_limit_bytes':33554432,'currently_blocked_lots':0,'archives_received_including_independent_lots':14,'no_git_push_or_merge':True,'scope':'All currently received lots extracted, full ffprobe/ffmpeg decoding and DSP, linked song table and source audit. No claim of commercial OST completeness or perceptual listening; not gameplay QA or GBA arrangement playback.'},ensure_ascii=False,indent=2)+'\n')
missing=[]
for p in D.rglob('*.md'):
 for _,target in re.findall(r'\[([^\]]+)\]\(([^)]+)\)',p.read_text()):
  if not target.startswith(('http','#')) and not (p.parent/target.split('#')[0]).exists():missing.append((str(p),target))
assert not missing,missing
print('PASS audit:',len(baseline),'initial files exact;80 full audio decodes;22 candidates +58 reserves;91 music slots;425 maps;20 cameo parties;PNG and links;ROM unchanged')
