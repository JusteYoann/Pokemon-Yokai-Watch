import struct,sys
F=[('version','I'),('language','I'),('gameName','32s'),('monFrontPics','I'),('monBackPics','I'),('monNormalPalettes','I'),('monShinyPalettes','I'),
('monIcons','I'),('monIconPaletteIds','I'),('monIconPalettes','I'),('monSpeciesNames','I'),('moveNames','I'),('decorations','I'),
('flagsOffset','I'),('varsOffset','I'),('pokedexOffset','I'),('seen1Offset','I'),('seen2Offset','I'),('pokedexVar','I'),('pokedexFlag','I'),
('mysteryEventFlag','I'),('pokedexCount','I'),('lens','17s'),('pad','3x'),('saveBlock2Size','I'),('saveBlock1Size','I'),('partyCountOffset','I'),
('partyOffset','I'),('warpFlagsOffset','I'),('trainerIdOffset','I'),('playerNameOffset','I'),('playerGenderOffset','I'),('frontierStatusOffset','I'),
('frontierStatusOffset2','I'),('externalEventFlagsOffset','I'),('externalEventDataOffset','I'),('unk18','I'),('speciesInfo','I'),('abilityNames','I'),
('abilityDescriptions','I'),('items','I'),('moves','I'),('ballGfx','I'),('ballPalettes','I'),('gcnLinkFlagsOffset','I'),('gameClearFlag','I'),
('ribbonFlag','I'),('bagcounts','6s'),('pad2','2x'),('pcItemsOffset','I'),('giftRibbonsOffset','I'),('enigmaBerryOffset','I'),('enigmaBerrySize','I'),
('moveDescriptions','I'),('unk20','I')]
def parse(d):
    fmt='<'+''.join(f for _,f in F); vals=struct.unpack_from(fmt,d,0x100)
    names=[n for n,f in F if not f.endswith('x')]
    return dict(zip(names,vals))
if __name__=='__main__':
    a=parse(open(sys.argv[1],'rb').read()); b=parse(open(sys.argv[2],'rb').read())
    for k in a:
        va,vb=a[k],b[k]
        fmtv=lambda v: hex(v) if isinstance(v,int) else v.hex() if isinstance(v,bytes) and k!='gameName' else v
        print(f"{k:26s} {str(fmtv(va)):>34s} {str(fmtv(vb)):>34s} {'' if va==vb else '<-- DIFF'}")
