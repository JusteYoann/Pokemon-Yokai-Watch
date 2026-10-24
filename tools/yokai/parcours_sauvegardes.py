"""Read mGBA's native Flash image, including after libretro savestate reloads.
Read-only extraction of EXTDATA_SAVEDATA; no save fields/checksums are edited.
libretro's public SRAM buffer can be stale while mGBA masks writes after reload.
"""
import struct

def native_battery(snapshot):
 pos=0x61000 # sizeof(GBASerializedState), this installed mGBA revision
 while pos+16<=len(snapshot):
  tag,size,offset=struct.unpack_from('<IiQ',snapshot,pos);pos+=16
  if not tag:break
  assert 0<=offset<=len(snapshot) and 0<=size<=len(snapshot)-offset
  if tag==2:
   assert size==131072,size
   data=snapshot[offset:offset+size]
   assert data!=b'\xff'*size,'No native save has been written'
   sectors=[i for i in range(32) if data[i*4096+0xff8:i*4096+0xffc]==bytes.fromhex('25200108')]
   assert len(sectors)>=14,('Incomplete native flash sectors',sectors)
   return data
 raise ValueError('Native Flash image missing from mGBA extended state')
