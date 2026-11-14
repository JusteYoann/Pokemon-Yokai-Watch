import re,struct
def symbols(mapfile):
    syms={}
    for line in open(mapfile):
        m=re.match(r'\s+0x([0-9a-f]{8})\s+(\w+)\s*$',line)
        if m: syms.setdefault(m.group(2),int(m.group(1),16))
    return syms
def locate(V,H,vaddr,length=48,skip=0):
    """find vanilla bytes [vaddr+skip:+length] in hack; returns hack addr of vaddr (or list)"""
    o=vaddr-0x08000000+skip
    chunk=V[o:o+length]
    hits=[m.start() for m in re.finditer(re.escape(chunk),H)]
    return [0x08000000+h-skip for h in hits]
def ptr_table(V,H,syms,name):
    """pointer table: locate first pointed-to target, then pointer to it in hack"""
    v=syms[name]-0x08000000
    first=struct.unpack_from('<I',V,v)[0]
    tgt=locate(V,H,first,32)
    if len(tgt)!=1: return None
    p=struct.pack('<I',tgt[0]); hits=[m.start() for m in re.finditer(re.escape(p),H)]
    return [0x08000000+x for x in hits]
