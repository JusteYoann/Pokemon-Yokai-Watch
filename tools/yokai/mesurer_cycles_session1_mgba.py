#!/usr/bin/env python3
"""Stream native intro+cycle (or full one-shot) to EBU R128, without changing gains."""
import argparse,ctypes,hashlib,json,re,subprocess,tempfile
from mgba_rpc import ROOT,BATCH
from mgba_new_game import new_game
import numpy as np

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--numbers',default='4,23,26')
parser.add_argument('--report',default='CYCLES_LUFS_MGBA.json')
a=parser.parse_args();cfg=json.loads((ROOT/'data/yokai/audio_loops.json').read_text())
loops={r['number']:r for r in cfg['tracks']}
for item in cfg.get('gap_tracks',[]):loops[item['number']]=dict(source_start_samples=0,source_end_samples=item['loop_end_samples'])
r=new_game();base=r.snapshot();rows=[];passed=False;error='Interrupted'
try:
    for n in map(int,a.numbers.split(',')):
        row=loops[n];r.restore(base);r.call('m4aMPlayAllStop')
        frames=(row['source_end_samples']-row['source_start_samples']+223)//224+30
        stats=dict(raw_clipped_samples=0,samples=0,raw_peak_pcm16=0)
        with tempfile.TemporaryFile() as log:
            process=subprocess.Popen(['ffmpeg','-hide_banner','-nostdin','-f','s16le','-ar','65536','-ac','2','-i','pipe:0','-af','highpass=f=20,ebur128=peak=true','-f','null','-'],stdin=subprocess.PIPE,stdout=subprocess.DEVNULL,stderr=log)
            def capture(ptr,count):
                block=ctypes.string_at(ptr,count*4);pcm=np.frombuffer(block,'<i2')
                stats['raw_clipped_samples']+=int(np.count_nonzero((pcm==32767)|(pcm==-32768)))
                stats['raw_peak_pcm16']=max(stats['raw_peak_pcm16'],int(np.max(np.abs(pcm.astype(np.int32)))))
                stats['samples']+=len(pcm);process.stdin.write(block);return count
            cb=BATCH(capture);r.lib.retro_set_audio_sample_batch(cb)
            try:
                r.call('m4aSongNumStart',346+n);r.run(frames)
            finally:
                r.lib.retro_set_audio_sample_batch(r.callbacks[3]);process.stdin.close();assert process.wait()==0
            log.seek(0);text=log.read().decode();summary=text.rsplit('Summary:',1)[-1]
        def number(pattern):return float(re.search(pattern,summary)[1])
        result=dict(number=n,frames=frames,duration_seconds=stats['samples']/131072,
                    integrated_lufs=number(r'I:\s+(-?[\d.]+) LUFS'),lra_lu=number(r'LRA:\s+([\d.]+) LU'),
                    true_peak_dbfs=number(r'Peak:\s+(-?[\d.]+) dBFS'),**stats)
        result['maximum_momentary_lufs']=max(map(float,re.findall(r'\bM:\s*(-?[\d.]+)',text)))
        result['maximum_short_term_lufs']=max(map(float,re.findall(r'\bS:\s*(-?[\d.]+)',text)))
        result['clipping_detected']=stats['raw_clipped_samples']>0
        assert stats['samples']>0 and r.u32(r.symbols['gMPlayInfo_BGM'])==r.symbols[f'mus_yokai_{n:02d}']
        rows.append(result);print('FULL CYCLE',result,flush=True)
    passed=True;error=None
except BaseException as e:error=str(e);raise
finally:
    output=ROOT/'QA_RECETTE_FINALE/SESSION_1_AUDIO'/a.report;output.parent.mkdir(parents=True,exist_ok=True)
    r.close();output.write_text(json.dumps(dict(passed=passed,error=error,
        rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),results=rows,
        scope='Actual native mixer, full intro+one cycle or complete one-shot, plus30-frame startup/end margin; EBU R128 after20Hz DC rejection; no listening, no simultaneous effects, no gain changes. passed means collection completed, not approval of mix.'),indent=2)+'\n')
