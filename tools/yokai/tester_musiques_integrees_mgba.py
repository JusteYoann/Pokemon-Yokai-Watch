#!/usr/bin/env python3
"""Real optional audio ROM: native map music, registered bicycle and NPC battles.

Five full sample-loop wraps per active cue, real libretro audio and native SFX.
Fixture warps/flags/strong party are explicit; not full adventure or hardware QA.
Private audio demos remain outside checkout. Public reports contain metadata only.
"""
import argparse,ctypes,hashlib,json,os,struct,wave
from collections import deque
from pathlib import Path
import numpy as np
from scipy.signal import resample_poly,fftconvolve
from mgba_rpc import ROOT,Emulator,BATCH
import tester_cameos_boss_mgba as boss
from dpcm_m4a import decode
P=ROOT/'QA_RECETTE_FINALE/INTEGRATION_MUSIQUES';P.mkdir(parents=True,exist_ok=True);(P/'preuves').mkdir(exist_ok=True)
G=json.loads((ROOT/'data/maps/map_groups.json').read_text());MAPS={name:(i,j) for i,key in enumerate(G['group_order']) for j,name in enumerate(G[key])}
CONFIG=json.loads((ROOT/'data/yokai/audio_loops.json').read_text());LOOPS={r['number']:r for r in CONFIG['tracks']}
private=Path(os.environ['YOKAI_AUDIO_DIR']);rom=Path(os.environ['YOKAI_QA_ROM']);manifest=json.loads((private/'manifest.json').read_text());results=[]
def channel(r,n):
 waveptr=r.symbols[f'yokai_wave_{n:02d}']
 for i in range(5):
  ptr=r.symbols['gSoundInfo']+80+64*i
  if r.u32(ptr+36)==waveptr and r.read(ptr,1)[0]&0x83:return ptr
 return None
def fixture(name='PalletTown',x=10,y=10):
 group,num=MAPS[name];r=boss.fixture({'map':num,'boss':{'x':x,'y':y}}) if group==1 else None
 if r is None:
  r=Emulator();r.call('SetSaveBlocksPointers');r.call('Sav2_ClearSetDefault');r.call('CB2_NewGame');r.run(180)
  r.call('CreateMon',r.symbols['gPlayerParty'],1,100,31,1,100,0,0);r.write(r.symbols['gPlayerPartyCount'],b'\x01')
  r.call('SetWarpDestination',group,num,255,x,y);r.call('WarpIntoMap');r.call('SetMainCallback2',r.symbols['CB2_LoadMap']|1)
  for f in range(1800):
   r.run()
   if f>60 and r.u32(r.symbols['gMain']+4)==r.symbols['CB2_Overworld']|1:break
  else:raise AssertionError('Map not ready')
  r.run(300)
 return r
def pulse(r,key):
 r.keys=set();r.run(4);r.keys={key};r.run(2);r.keys=set();r.run(120)
def wait_header(r,n,limit=1800):
 for f in range(limit):
  r.run()
  if r.u32(r.symbols['gMPlayInfo_BGM'])==r.symbols[f'mus_yokai_{n:02d}'] and channel(r,n):return
 raise AssertionError(('Expected actual private song not playing',n,hex(r.u32(r.symbols['gMPlayInfo_BGM']))))
def run_song(r,n,trigger):
 wait_header(r,n);r.keys=set();r.run(30);ptr=channel(r,n);assert ptr
 chunks=[];ring=deque(maxlen=200);sum_frames=[0];seam_audio=[];pending=[]
 def audio_callback(data,frames):
  block=ctypes.string_at(data,frames*4);ring.append(block)
  if sum_frames[0]<8*65536:chunks.append(block)
  sum_frames[0]+=frames
  return frames
 callback=BATCH(audio_callback);r.lib.retro_set_audio_sample_batch(callback)

 first=r.u32(ptr+40);prev=first;wraps=[];frames=0;row=LOOPS[n];loop_start=row['source_loop_start_samples']-row['source_start_samples'];period=row['source_end_samples']-row['source_loop_start_samples'];max_frames=int((row['source_end_samples']-row['source_start_samples']+period*5)/224)+1800
 for f in range(max_frames):
  if f==120:r.call('PlaySE',boss.C.get('SE_SELECT',5))
  if f==240:r.call('PlayCry_Normal',1,0)
  r.run();frames+=1;pos=r.u32(ptr+40)
  if pos+100<prev:
   assert loop_start<=pos<=loop_start+900,(n,'Intro returned or invalid loop',pos,loop_start)
   wraps.append({'frame':frames,'sample_after_wrap':pos})
   pending.append((frames+40,len(wraps)))
  if pending and frames>=pending[0][0]:
   _,which=pending.pop(0);seam_audio.append((which,b''.join(ring)))
  if len(seam_audio)==5:break
  prev=pos
  if f%2048==0:assert channel(r,n)==ptr and r.u32(r.symbols['gMPlayInfo_BGM'])==r.symbols[f'mus_yokai_{n:02d}']
 else:raise AssertionError((n,'Five loops not completed',wraps))
 assert len(wraps)==5 and len(seam_audio)==5
 assert all(abs((b['frame']-a['frame'])-period/224)<2 for a,b in zip(wraps,wraps[1:]))
 assert r.call('IsCryFinished')!=0
 # Compare real mixer output with encoded reference, in a low band independent of volume.
 audio=np.frombuffer(b''.join(chunks),dtype='<i2').reshape(-1,2).mean(axis=1)
 actual=resample_poly(resample_poly(audio,125,2048),4,1) # bandlimit4kHz, align on16kHz grid; reject DAC DC bias below
 blob=(private/f'{n:02d}.dpcm').read_bytes();size=struct.unpack_from('<I',blob,12)[0];decoded=np.array(decode(blob[16:],size),float)
 expected=decoded[first:first+round(8*13379)]
 if len(expected)<8*13379:expected=np.r_[expected,decoded[loop_start:loop_start+8*13379]]
 reference=resample_poly(resample_poly(expected,4000,13379),4,1)
 def correlate(second):
  template=reference[round(second*16000):round((second+1)*16000)];template=template-template.mean()
  search=actual[round((second-.25)*16000):round((second+1.25)*16000)]
  corr=fftconvolve(search,template[::-1],mode='valid')
  variance=fftconvolve(search**2,np.ones(len(template)),mode='valid')-fftconvolve(search,np.ones(len(template)),mode='valid')**2/len(template)
  energy=np.sqrt(np.maximum(1e-12,variance*sum(template**2)))
  return float(max(corr/energy))
 identity=correlate(.5);after_cry_identity=correlate(6)
 if identity<=.85:
  debug=private/'debug';debug.mkdir(exist_ok=True)
  np.savez(debug/f'{n:02d}-identity.npz',actual=actual,decoded=decoded,first=first,raw=audio)
  r.frame.save(P/'preuves'/f'ost-{n:02d}-diagnostic.png')
 assert min(identity,after_cry_identity)>.85,(n,'Actual decoded source not recognizable before/after SFX',identity,after_cry_identity,first)
 # Actual audio across each of the five native loop boundaries, not just RAM counters.
 seam_reference=np.r_[decoded[-round(.35*13379):],decoded[loop_start:loop_start+round(.35*13379)]]
 seam_template=resample_poly(resample_poly(seam_reference,4000,13379),4,1);seam_template-=seam_template.mean();seam_scores=[]
 for which,raw_seam in seam_audio:
  signal=np.frombuffer(raw_seam,dtype='<i2').reshape(-1,2).mean(axis=1)
  signal=resample_poly(resample_poly(signal,125,2048),4,1)
  c=fftconvolve(signal,seam_template[::-1],mode='valid');variance=fftconvolve(signal**2,np.ones(len(seam_template)),mode='valid')-fftconvolve(signal,np.ones(len(seam_template)),mode='valid')**2/len(seam_template)
  score=float(max(c/np.sqrt(np.maximum(1e-12,variance*sum(seam_template**2)))));seam_scores.append(score)
  debug=private/'previews';debug.mkdir(exist_ok=True)
  with wave.open(str(debug/f'{n:02d}-loop-{which}.wav'),'wb') as w:w.setnchannels(2);w.setsampwidth(2);w.setframerate(65536);w.writeframes(raw_seam)
 assert min(seam_scores)>.85,(n,'Actual loop audio does not match wrapped encoded waveform',seam_scores)
 demo=private/'previews';demo.mkdir(exist_ok=True)
 with wave.open(str(demo/f'{n:02d}-mgba-8s.wav'),'wb') as w:w.setnchannels(2);w.setsampwidth(2);w.setframerate(65536);w.writeframes(b''.join(chunks))
 r.frame.save(P/'preuves'/f'ost-{n:02d}-en-jeu.png');r.lib.retro_set_audio_sample_batch(r.callbacks[3])
 assert r.call('TrySavingData',0,max_frames=1200)==1
 assert r.u32(r.symbols['gMPlayInfo_BGM'])==r.symbols[f'mus_yokai_{n:02d}']
 results.append({'number':n,'passed':True,'trigger':trigger,'five_native_loop_wraps':wraps,'five_actual_audio_seam_correlations':seam_scores,'native_samples_per_frame':224,'expected_frames_per_cycle':period/224,'intro_not_repeated':True,'audio_reference_pearson_correlation':identity,'after_SFX_and_cry_correlation':after_cry_identity,'analysis_sample_rate_hz':4000,'alignment_grid_hz':16000,'initial_native_sample_position':first,'select_SFX_and_cry_native_calls':True,'cry_completed':True,'native_Flash_save_with_music':True,'native_frames':frames,'source_sample_period':period,'perceptual_listening_validated':False,'audio_demo':'Private output/previews only, not public GitHub'})

def main(numbers):
 for n in numbers:
  print('START',n,flush=True)
  if n in [2,6,20]:
   spec=json.loads((ROOT/'data/yokai/cameos_boss.json').read_text());actors={a['name']:a for a in spec['actors']}
   actor=actors['Domniscian'] if n==2 else actors['EmployeRouge'] if n==20 else {'x':11,'y':6}
   r=boss.fixture({'map':57 if n in [2,20] else 101,'boss':actor})
   if n==2:
    for flag in actor['need']:r.call('FlagSet',boss.C[flag])
   boss.interact(r)
   for f in range(4000):
    if r.u32(r.symbols['gMain']+4)==r.symbols['BattleMainCB2']|1 and r.u32(r.symbols['gMPlayInfo_BGM'])==r.symbols[f'mus_yokai_{n:02d}']:break
    r.keys={8} if f%16<4 else set();r.run()
   else:raise AssertionError(('Actual NPC battle not started',n))
   r.keys=set();r.run(600);run_song(r,n,'Actual optional NPC battle through A/Yes; progression flags/strong party prepared')
   # Finish the actual optional fight using legal controller input; native return to exploration.
   won=0x316 if n==2 else 0x303 if n==6 else 0x314
   before=r.call('GetGameStat',9);boss.fight(r,won,f'audio-boss-{n:02d}')
   r.run(240);assert r.u32(r.symbols['gMPlayInfo_BGM'])!=r.symbols[f'mus_yokai_{n:02d}'];results[-1]['actual_battle_finished_and_exploration_music_restored']=True
  else:
   name,x,y={1:('PalletTown',10,10),4:('PokemonTower_1F',10,10),11:('SilphCo_11F',10,15),14:('ThreeIsland_BerryForest',10,10),16:('TwoIsland',10,10),17:('RocketHideout_B1F',20,20)}[n]
   r=fixture(name,x,y)
   if n==11:
    r.call('FlagClear',boss.C['FLAG_HIDE_SILPH_ROCKETS']);r.call('Overworld_ChangeMusicToDefault')
   if n==1:
    r.call('AddBagItem',boss.C['ITEM_BICYCLE'],1);r.write(r.u32(r.symbols['gSaveBlock1Ptr'])+0x296,struct.pack('<H',boss.C['ITEM_BICYCLE']));pulse(r,2);assert r.read(r.symbols['gPlayerAvatar'],1)[0]&6
   run_song(r,n,'Registered Bicycle SELECT' if n==1 else 'Native warp/map music: '+name)
   if n==1:
    pulse(r,2);assert not r.read(r.symbols['gPlayerAvatar'],1)[0]&6;assert r.u32(r.symbols['gMPlayInfo_BGM'])!=r.symbols['mus_yokai_01'];results[-1]['second_SELECT_restores_zone_music_and_on_foot']=True
   elif n==11:
    r.call('FlagSet',boss.C['FLAG_HIDE_SILPH_ROCKETS']);r.call('Overworld_ChangeMusicToDefault');r.run(240);assert r.u32(r.symbols['gMPlayInfo_BGM'])!=r.symbols['mus_yokai_11'];results[-1]['liberated_Silph_returns_native_music']=True
  r.close();print('PASS',n,flush=True)
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--tracks',default='1,2,4,6,11,14,16,17,20');a=parser.parse_args()
 try:main([int(n) for n in a.tracks.split(',')]);passed=True;error=None
 except Exception as e:passed=False;error=str(e);raise
 finally:
  (P/'TEST_MGBA.json').write_text(json.dumps({'passed':locals().get('passed',False),'error':locals().get('error','Interrupted'),'private_rom_sha256':hashlib.sha256(rom.read_bytes()).hexdigest(),'private_rom_bytes':rom.stat().st_size,'scope':'Real map/bicycle/NPC music in compiled optional audio ROM; fixture warps/flags; five native full loops. Not whole story, hardware profiling or perceptual listening.','results':results},indent=2)+'\n')
