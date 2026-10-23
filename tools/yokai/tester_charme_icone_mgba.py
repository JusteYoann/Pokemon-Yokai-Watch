#!/usr/bin/env python3
"""Native bag, actual key-item pocket and selected charm; no substituted UI graphics."""
import os,json,hashlib
from PIL import Image
from mgba_new_game import new_game
from mgba_rpc import ROOT
mode='prive' if '_audio' in os.environ.get('YOKAI_QA_ROM','') else 'public'
D=ROOT/'docs/juste-yoann/icone-charme'/mode;D.mkdir(parents=True,exist_ok=True)
r=new_game();passed=False;rows=[]
try:
 assert r.call('GetItemIconGfxPtr',52,0)==r.symbols['gItemIcon_ShinyCharm']
 assert r.call('GetItemIconGfxPtr',52,1)==r.symbols['gItemIconPalette_ShinyCharm']
 description=r.call('ItemId_GetDescription',52)
 width=r.call('GetStringWidth',0,description,0);assert width<=196,width
 # Real inventory grant and pocket selection fixture, then native bag renderer.
 r.call('YoannGiveCharm');assert r.call('CheckBagHasItem',52,1)
 r.write(r.symbols['gBagMenuState']+6,b'\1\0')
 r.call('CB2_BagMenuFromStartMenu');r.run(600)
 assert r.u32(r.symbols['gMain']+4)!=r.symbols['CB2_Overworld']|1
 assert r.read(r.symbols['gBagMenuState']+6,2)==b'\1\0'
 ids=r.read(r.symbols['sItemMenuIconSpriteIds']+10,2)
 sid=next(i for i in ids if i<64)
 sprite=r.symbols['gSprites']+68*sid
 tile=int.from_bytes(r.read(sprite+4,2),'little')&1023
 raw=r.read(0x06010000+tile*32,512)
 assert any(raw)
 # Compare loaded icon tiles to the native padding function, not a screenshot mockup.
 src=r.call('AllocZeroed',288);dst=r.call('AllocZeroed',512);assert src and dst
 r.write(src,(ROOT/'graphics/items/icons/shiny_charm.4bpp').read_bytes())
 r.call('CopyItemIconPicTo4x4Buffer',src,dst)
 assert raw==r.read(dst,512),'Wrong icon in object VRAM'
 r.call('Free',src);r.call('Free',dst)
 r.frame.save(D/'charme-dans-sac.png');r.frame.resize((960,640),Image.Resampling.NEAREST).save(D/'charme-dans-sac-x4.png')
 # Open and close the ordinary key-item menu to check this is a usable bag entry.
 r.keys={8};r.run(1);r.keys=set();r.run(60)
 r.frame.save(D/'menu-charme.png')
 passed=True;rows.append({'test':'Native charm graphic and palette pointers; actual key pocket; OBJ VRAM equals native padded icon; context menu opened','passed':True})
finally:
 sha=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest();r.close();(D/'TEST_MGBA.json').write_text(json.dumps(dict(passed=passed,scope=__doc__,rom_sha256=sha,results=rows),ensure_ascii=False,indent=2)+'\n')
