import struct
from PIL import Image
def lz10(d,o):
    assert d[o]==0x10, hex(d[o]); size=d[o+1]|d[o+2]<<8|d[o+3]<<16; o+=4; out=bytearray()
    while len(out)<size:
        flags=d[o]; o+=1
        for b in range(8):
            if len(out)>=size: break
            if flags&(0x80>>b):
                x=d[o]<<8|d[o+1]; o+=2; ln=(x>>12)+3; disp=(x&0xFFF)+1
                for _ in range(ln): out.append(out[-disp])
            else: out.append(d[o]); o+=1
    return bytes(out), o
def pal(d,o,n=16):
    out=[]
    for i in range(n):
        c=struct.unpack_from('<H',d,o+2*i)[0]; out.append(((c&31)*255//31,((c>>5)&31)*255//31,((c>>10)&31)*255//31))
    return out
def tiles4bpp(raw,wtiles,htiles,palette,transparent=True):
    img=Image.new('RGBA',(wtiles*8,htiles*8))
    px=img.load()
    for t in range(wtiles*htiles):
        tx,ty=t%wtiles,t//wtiles
        for y in range(8):
            for x in range(8):
                b=raw[t*32+y*4+x//2]; c=(b>>4) if x&1 else (b&15)
                r,g,bb=palette[c]; px[tx*8+x,ty*8+y]=(r,g,bb,0 if (c==0 and transparent) else 255)
    return img
def frames(raw,fw,fh,n,palette):
    """object event pics: n frames of fw x fh tiles each, stored frame after frame"""
    per=fw*fh*32; sheet=Image.new('RGBA',(fw*8*n,fh*8))
    for i in range(n): sheet.paste(tiles4bpp(raw[i*per:(i+1)*per],fw,fh,palette),(i*fw*8,0))
    return sheet
