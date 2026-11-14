import sys,struct; import os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from g3text import dec
TYPES="NORMAL FIGHTING FLYING POISON GROUND ROCK BUG GHOST STEEL MYSTERY FIRE WATER GRASS ELECTRIC PSYCHIC ICE DRAGON DARK".split()
GROWTH="MEDIUM_FAST ERRATIC FLUCTUATING MEDIUM_SLOW FAST SLOW".split()
def info(d,stats,names,sp):
    e=d[stats+sp*28:stats+sp*28+26]
    (hp,at,df,spe,sa,sd,t1,t2,catch,exp,ev,i1,i2,gender,egg,fr,growth,eg1,eg2,ab1,ab2,safari,col)=struct.unpack('<6B2BBBHHH6B2BBB',e)
    return dict(id=sp,name=dec(d,names+sp*11,11),hp=hp,atk=at,def_=df,spe=spe,spa=sa,spd=sd,total=hp+at+df+spe+sa+sd,
        types=(TYPES[t1] if t1<18 else t1,TYPES[t2] if t2<18 else t2),catch=catch,exp=exp,ev=f"{ev:04x}",items=(i1,i2),
        gender=gender,egg_cycles=egg,friendship=fr,growth=GROWTH[growth] if growth<6 else growth,egg_groups=(eg1,eg2),abilities=(ab1,ab2),safari=safari,color=col)
if __name__=='__main__':
    d=open(sys.argv[1],'rb').read(); stats=int(sys.argv[2],0); names=int(sys.argv[3],0)
    for sp in range(int(sys.argv[4]),int(sys.argv[5])): print(info(d,stats,names,sp))
