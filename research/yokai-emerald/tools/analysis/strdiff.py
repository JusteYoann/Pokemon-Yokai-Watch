import sys,os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from g3text import DEC
OK=set(DEC)|{0xFC,0xFD,0xFE,0xFA,0xFB,0xB0,0xB1,0xB2,0xB3,0xB5,0xB6,0xB7,0xBA,0xF0}
def strings(d,minlen=8):
    out={};i=0;n=len(d)
    while i<n:
        j=i
        while j<n and d[j] in OK and d[j]!=0xFF:
            if d[j]==0xFC: j+=2  # control code + arg
            elif d[j]==0xFD: j+=2
            else: j+=1
        if j<n and d[j]==0xFF and j-i>=minlen:
            s=d[i:j]
            letters=sum(1 for x in s if 0xBB<=x<=0xEE)
            if letters>=0.5*len(s): out.setdefault(bytes(s),i)
            i=j+1
        else: i=max(j,i)+1
    return out
def show(b):
    r=[]
    k=0
    while k<len(b):
        x=b[k]
        if x in (0xFC,0xFD): r.append('{%02X%02X}'%(x,b[k+1] if k+1<len(b) else 0)); k+=2; continue
        r.append({0xFE:'\\n',0xFA:'\\l',0xFB:'\\p',0xB0:'…',0xB1:'“',0xB2:'”',0xB3:'‘',0xB5:'♂',0xB6:'♀',0xBA:'/',0xF0:':'}.get(x,DEC.get(x,'{%02X}'%x))); k+=1
    return ''.join(r)
v=strings(open(sys.argv[1],'rb').read()); h=strings(open(sys.argv[2],'rb').read())
new={s:o for s,o in h.items() if s not in v}; gone={s:o for s,o in v.items() if s not in h}
print("vanilla strings",len(v),"hack strings",len(h),"new/modified",len(new),"vanilla absent",len(gone))
for s,o in sorted(new.items(),key=lambda x:x[1]): print("NEW 0x%06X %s"%(o,show(s)))
print("-----")
for s,o in sorted(gone.items(),key=lambda x:x[1]): print("GONE 0x%06X %s"%(o,show(s)))
