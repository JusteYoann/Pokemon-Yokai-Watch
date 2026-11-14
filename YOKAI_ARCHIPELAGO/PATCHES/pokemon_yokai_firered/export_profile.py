#!/usr/bin/env python3
"""Exporte les adresses MESURÉES du canal C après compilation, pas des offsets vanilla."""
import argparse,hashlib,json,struct,subprocess
from pathlib import Path
BASE_SHA1='40c59a9f240d29a7b16d1dd299b1125513a280c4'

def export(rom,elf):
    symbols={}
    for line in subprocess.check_output(['arm-none-eabi-nm','--defined-only',str(elf)],text=True).splitlines():
        f=line.split()
        if len(f)==3:symbols[f[2]]=int(f[0],16)
    image=rom.read_bytes();offset=symbols['gYokaiAPRomInfo']-0x08000000
    info=image[offset:offset+81]
    if info[:8]!=struct.pack('<IHH',0x31504B59,1,48) or info[40:81].split(b'\0')[0].decode()!=BASE_SHA1:
        raise ValueError('Mauvais module AP, base ou ABI')
    return {'version':1,'mode':'bonus','base_sha1':BASE_SHA1,'rom_sha256':hashlib.sha256(image).hexdigest(),
            'rom_info':symbols['gYokaiAPRomInfo'],'mailbox':symbols['gYokaiAPMailbox'],
            'saveblock2_pointer':symbols['gSaveBlock2Ptr'],'main':symbols['gMain'],
            'overworld_callback':symbols['CB2_Overworld']|1,'save_storage_offset':0xE20,'save_storage_bytes':64}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('rom',type=Path);p.add_argument('elf',type=Path);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(export(a.rom,a.elf),indent=2)+'\n');print(a.out)

if __name__=='__main__':main()
