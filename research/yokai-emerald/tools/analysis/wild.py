import struct,re,json,sys,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from locate import symbols
R=lambda p:p-0x08000000
COUNTS={'land':12,'water':5,'rock':5,'fish':10}
def parse(D,start):
    out=[];o=start
    while True:
        g,n=D[o],D[o+1]
        if g==0xFF and n==0xFF: break
        ptrs=struct.unpack_from('<4I',D,o+4); e={'group':g,'num':n}
        for k,p in zip(COUNTS,ptrs):
            if p:
                rate,lst=struct.unpack_from('<BxxxI',D,R(p))
                e[k]=[struct.unpack_from('<BBH',D,R(lst)+4*i) for i in range(COUNTS[k])]
        out.append(e); o+=20
    return out
def find_headers(V,H,vstart):
    """locate hack gWildMonHeaders from the first vanilla land list"""
    first=parse(V,vstart)[0]
    vland_info=struct.unpack_from('<I',V,vstart+4)[0]
    vlist=struct.unpack_from('<I',V,R(vland_info)+4)[0]
    chunk=V[R(vlist):R(vlist)+48]
    for m in re.finditer(re.escape(chunk),H):
        lp=struct.pack('<I',0x08000000+m.start())
        for m2 in re.finditer(re.escape(lp),H):
            info=m2.start()-4
            ip=struct.pack('<I',0x08000000+info)
            for m3 in re.finditer(re.escape(ip),H):
                hdr=m3.start()-4
                if H[hdr:hdr+2]==V[vstart:vstart+2]: return hdr
def find_headers2(V,H,vstart,n=20):
    keys=b''.join(V[vstart+20*i:vstart+20*i+4] for i in range(n))
    for o in range(0,len(H)-20*n,4):
        if all(H[o+20*i:o+20*i+4]==keys[4*i:4*i+4] for i in range(n)): return o
