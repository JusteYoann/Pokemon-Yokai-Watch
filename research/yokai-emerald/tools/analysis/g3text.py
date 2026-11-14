import sys, re
ENC={}
for i,c in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ"): ENC[c]=0xBB+i
for i,c in enumerate("abcdefghijklmnopqrstuvwxyz"): ENC[c]=0xD5+i
for i,c in enumerate("0123456789"): ENC[c]=0xA1+i
ENC[' ']=0x00; ENC['!']=0xAB; ENC['?']=0xAC; ENC['.']=0xAD; ENC['-']=0xAE; ENC["'"]=0xB4; ENC[',']=0xB8; ENC['é']=0x1B
DEC={v:k for k,v in ENC.items()}; DEC[0xFE]='\\n'; DEC[0xFA]='\\l'; DEC[0xFB]='\\p'
def enc(s): return bytes(ENC[c] for c in s)
def dec(b,off,n=200):
    out=[]
    for x in b[off:off+n]:
        if x==0xFF: break
        out.append(DEC.get(x,'{%02X}'%x))
    return ''.join(out)
if __name__=='__main__':
    d=open(sys.argv[1],'rb').read()
    for w in sys.argv[2:]:
        hits=[m.start() for m in re.finditer(re.escape(enc(w)),d)]
        print(w,len(hits),[hex(h) for h in hits[:8]])
