#!/usr/bin/env python3
"""Sonde YW1 EUR en lecture seule. Aucune adresse YW2/YW3 n'est réutilisée.

Azahar : activer le serveur RPC (port 45987), lancer votre jeu européen.
Sans --range, seule l'identité du processus est interrogée. Les lectures sont
explicites et leurs résultats restent locaux. Ceci n'est pas un client AP jouable.
"""
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'research/yokai-3ds/poc'))
from ykap.azahar_rpc import AzaharRpc
TITLE_ID=0x0004000000167800


def collect(rpc,ranges):
    processes=rpc.processes();matches=[p for p in processes if p.title_id==TITLE_ID]
    if len(matches)!=1:raise ValueError('Un seul Yo-kai Watch 1 EUR doit être lancé ; autre jeu/région refusé')
    current=rpc.current_process()
    if current!=matches[0].pid:raise ValueError('Le processus RPC courant n’est pas YW1 EUR ; ne pas lire une autre mémoire')
    report={'title_id':f'{TITLE_ID:016X}','pid':current,'game_memory_written':False,
            'archipelago_communication_tested':False,'reads':[]}
    for address,size in ranges:
        if not 1<=size<=1024*1024 or not 0<=address<2**32 or address+size>2**32:
            raise ValueError('Plage invalide (maximum 1 Mio par lecture explicite)')
        data=rpc.read(address,size)
        report['reads'].append({'address':f'0x{address:08X}','size':size,'hex':data.hex(),
                                'sha256':hashlib.sha256(data).hexdigest()})
    return report


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--host',default='127.0.0.1');p.add_argument('--port',type=int,default=45987)
    p.add_argument('--range',action='append',default=[],metavar='ADRESSE:TAILLE');p.add_argument('--out',type=Path)
    a=p.parse_args();ranges=[]
    for text in a.range:
        try:address,size=text.split(':');ranges.append((int(address,0),int(size,0)))
        except ValueError:p.error('Format --range : 0xADRESSE:TAILLE')
    rpc=AzaharRpc(a.host,a.port)
    try:report=collect(rpc,ranges)
    except ValueError as e:p.exit(2,str(e)+'\n')
    finally:rpc.close()
    text=json.dumps(report,indent=2,ensure_ascii=False)+'\n'
    if a.out:a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(text)
    else:print(text,end='')

if __name__=='__main__':main()
