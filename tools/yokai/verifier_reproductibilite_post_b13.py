#!/usr/bin/env python3
"""Compare actual public/private ROMs with a pristine separately built GitHub clone."""
import argparse,hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--clean-clone',type=Path,required=True);p.add_argument('--decoder-proof',type=Path,required=True);a=p.parse_args();clone=a.clean_clone.resolve();assert clone!=ROOT
 rows=[]
 for name in ['pokefirered.gba','pokefirered_audio.gba']:
  local=(ROOT/name).read_bytes();clean=(clone/name).read_bytes();assert local==clean,(name,'ROMs differ; investigate without changing locks');rows.append(dict(target=name,bytes=len(local),local_sha256=hashlib.sha256(local).hexdigest(),clean_clone_sha256=hashlib.sha256(clean).hexdigest(),byte_identical=True))
 assert not subprocess.check_output(['git','-C',str(clone),'status','--porcelain'],text=True)
 proof=json.loads(a.decoder_proof.read_text());assert proof['passed']
 loops=json.loads((ROOT/'data/yokai/audio_loops.json').read_text())['tracks'];assert len(proof['results'])==len(loops)
 pins={r['number']:r['pcm_wav_sha256'] for r in loops}
 for r in proof['results']:assert r['passed'] and r['wav_sha256']==pins[r['number']]
 out=ROOT/'QA_RECETTE_FINALE/POST_B13';(out/'audio/DECODAGE_REPRO.json').write_text(json.dumps(proof,indent=2)+'\n')
 hashes={str(p.relative_to(ROOT/'tools/agbcc')):hashlib.sha256(p.read_bytes()).hexdigest() for folder in ['bin','lib'] for p in (ROOT/'tools/agbcc'/folder).glob('*') if p.is_file()}
 report={'passed':True,'source_commit':subprocess.check_output(['git','-C',str(clone),'rev-parse','HEAD'],text=True).strip(),'github_branch':'dev/reconstruction-finalisation','clone_command':'git clone --depth 1 --single-branch --branch dev/reconstruction-finalisation https://github.com/JusteYoann/Pokemon-Yokai-Watch.git <empty-directory>','tracked_tree_pristine_after_build':True,'game_objects_or_generated_graphics_copied':False,'toolchain_cache_reused':True,'agbcc_source_commit':'da598c1d918402c42c0c0d7128ba14567f3175e9','toolchain_binary_hashes':hashes,'binutils':subprocess.check_output(['arm-none-eabi-as','--version'],text=True).splitlines()[0],'builds':['bash build_tools.sh','make -j4','generer_audio_prive.py with locked private WAVs into a new private directory','make -j4 YOKAI_AUDIO_DIR=<new-private-directory>'],'private_source_decode':'18 separate fresh MP3 decodes match locked WAV SHA; audio/DECODAGE_REPRO.json','results':rows,'limits':['Fresh GitHub checkout on same cloud host, not a new OS/VM or Windows PC','Pinned cached compiler/runtime reused, no cached game objects, generated graphics or private DPCM copied into clone','Private source recordings are external; public fallback ROM differs musically','Not a whole-adventure or perceptual acceptance test']}
 (out/'REPRODUCTIBILITE_CLONE_GITHUB.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print('PASS: two byte-identical clean builds and18 verified private source decodes')
if __name__=='__main__':main()
