"""Check actual per-frame OAM: visible enlarged battlers use double-size mode."""
import struct

def inspect(r):
 oam=list(struct.iter_unpack('<HHHH',r.read(r.symbols['gMain']+0x38,1024)));checked=0
 for b in range(r.read(r.symbols['gBattlersCount'],1)[0]):
  sid=r.read(r.symbols['gBattlerSpriteIds']+b,1)[0]
  if sid>=64:continue
  sp=r.symbols['gSprites']+68*sid;flags=r.read(sp+0x3e,1)[0]
  if not flags&1 or flags&4 or r.u32(sp+8)!=r.symbols['gAnims_MonPic']:continue
  attr0,attr1,attr2=struct.unpack('<HHH',r.read(sp,6))
  for a0,a1,a2,_ in oam[:r.read(r.symbols['gOamLimit'],1)[0]]:
   if a2&0xf3ff!=attr2&0xf3ff or a1>>14!=3 or (a0>>14)!=0 or ((a0>>8)&3)==2:continue
   matrix=(a1>>9)&31
   assert ((a0>>8)&3)==3,('Extended OAM fallback',b,hex(a0),matrix)
   checked+=1
 return checked
