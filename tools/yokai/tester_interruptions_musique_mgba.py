#!/usr/bin/env python3
"""Native item/level/heal fanfares, pause, fades, legacy bike music and Flash.

Actual private audio ROM, no ROM patching. Fixture warp/flags only.
"""
import hashlib,json,re,struct
import tester_musiques_integrees_mgba as t
r=t.fixture('RocketHideout_B1F',20,20);results=[]
songs={k:int(v) for k,v in re.findall(r'^#define\s+(\w+)\s+(\d+)\s',(t.ROOT/'include/constants/songs.h').read_text(),re.M)}
def position(n=17):
 ptr=t.channel(r,n);assert ptr is not None,('Sampled BGM voice absent',n)
 assert r.read(ptr+10,2)!=b'\0\0', 'Restored voice has zero mixer volume'
 return r.u32(ptr+40)
def remember():return r.u32(r.symbols['sPausedChannel']+40)
try:
 t.wait_header(r,17)
 for song,wait in [('MUS_OBTAIN_ITEM',400),('MUS_LEVEL_UP',240),('MUS_HEAL',400)]:
  before=position();r.call('PlayFanfare',songs[song]);r.run(20);assert t.channel(r,17) is None
  paused=remember();assert paused>=before
  r.run(wait-20);after=position();assert paused<=after<=paused+wait*224
  assert r.u32(r.symbols['gMPlayInfo_BGM'])==r.symbols['mus_yokai_17']
  results.append({'test':'Actual '+song+' fanfare resumes sampled voice at saved cursor without repeating intro','before':before,'paused':paused,'after':after,'passed':True})
 songid=songs['MUS_YOKAI_DODGY'];before=position();r.call('m4aSongNumStop',songid);r.run(10);assert t.channel(r,17) is None;paused=remember();r.call('m4aSongNumStop',songid);assert remember()==paused
 r.call('m4aSongNumContinue',songid);r.run(120);assert paused<=position()<=paused+122*224
 results.append({'test':'Song-ID Stop twice / Continue preserves exact paused cursor and restores voice','passed':True})
 before=position();r.call('FadeOutBGMTemporarily',2);r.run(120);assert t.channel(r,17) is None;paused=remember();r.call('FadeInBGM',2);r.run(120);assert paused<=position()<=paused+122*224
 results.append({'test':'Temporary fade-out / fade-in restores sampled voice and position','passed':True})
 # Exercise old savedMusic song ID with native cycling state; save format unchanged.
 r.call('SetPlayerAvatarTransitionFlags',2);r.run(20);save=r.u32(r.symbols['gSaveBlock1Ptr']);r.write(save+0x2C,struct.pack('<H',songs['MUS_CYCLING']));r.call('Overworld_PlaySpecialMapMusic');r.run(180);t.wait_header(r,1)
 assert r.read(r.u32(r.symbols['gSaveBlock1Ptr'])+0x2C,2)==struct.pack('<H',songs['MUS_YOKAI_BICYCLE'])
 assert r.call('TrySavingData',0,max_frames=1200)==1;r.write(r.u32(r.symbols['gSaveBlock1Ptr'])+0x2C,b'\0\0');assert r.call('LoadGameSave',0,max_frames=1200)==1
 assert r.read(r.u32(r.symbols['gSaveBlock1Ptr'])+0x2C,2)==struct.pack('<H',songs['MUS_YOKAI_BICYCLE'])
 results.append({'test':'Legacy saved bicycle song migrates to dedicated ID; native Flash save/load retains it','passed':True})
 # Fresh native song start must cancel any pending old sampled voice.
 r.call('PlayFanfare',songs['MUS_OBTAIN_ITEM']);r.run(10);r.call('PlayBGM',songs['MUS_PALLET']);r.run(400);assert t.channel(r,1) is None and t.channel(r,17) is None
 assert r.u32(r.symbols['gMPlayInfo_BGM'])!=r.symbols['mus_yokai_01']
 results.append({'test':'Changing music during fanfare cancels cached voice; no stale sample resurrection','passed':True})
 r.frame.save(t.P/'preuves'/'fanfare-retour-zone.png')
 report={'passed':True,'private_rom_sha256':hashlib.sha256(t.rom.read_bytes()).hexdigest(),'scope':'Native functions and callbacks in actual compiled private ROM, fixture warp/bike saved state; no whole-story or hardware timing claim','results':results}
 (t.P/'TEST_INTERRUPTIONS_MGBA.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
finally:r.close()
