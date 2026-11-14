#!/usr/bin/env python3
"""Vrai serveur AP + vrai mGBA libretro + client officiel BizHawk.

Le transport émulateur est un adaptateur Python au protocole Lua, branché sur
la mémoire réelle de mGBA, pas une mémoire simulée. Ce test ne valide pas le Lua
GUI. L'équipe et la position sont préparées par fixture ; le combat de Wyatt et
l'obtention du badge sont joués par le moteur, sans poser le flag de badge.
"""
from __future__ import annotations
import argparse,asyncio,base64,hashlib,json,os,struct,subprocess,sys,time,zlib
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]

class NativeTransport:
    def __init__(self,emulator):
        self.r=emulator;self.rom=emulator.rom_buffer.raw[:-1];self.box=emulator.symbols['gYokaiAPMailbox']
        self.requests=0
    def read(self,address,size,domain):
        if size<0 or size>1024*1024:raise ValueError('Read too large')
        if domain=='ROM':return self.rom[address:address+size]
        if domain=='System Bus':return self.r.read(address,size)
        raise ValueError('Unsupported domain '+domain)
    def request(self,req):
        k=req['type'];self.requests+=1
        if k=='PING':return {'type':'PONG'}
        if k=='SYSTEM':return {'type':'SYSTEM_RESPONSE','value':'GBA'}
        if k=='HASH':return {'type':'HASH_RESPONSE','value':format(zlib.crc32(self.rom),'x')}
        if k=='PREFERRED_CORES':return {'type':'PREFERRED_CORES_RESPONSE','value':[]}
        if k=='READ':return {'type':'READ_RESPONSE','value':base64.b64encode(self.read(req['address'],req['size'],req['domain'])).decode()}
        if k=='GUARD':
            wanted=base64.b64decode(req['expected_data'],validate=True)
            return {'type':'GUARD_RESPONSE','value':self.read(req['address'],len(wanted),req['domain'])==wanted,'address':req['address']}
        if k=='WRITE':
            data=base64.b64decode(req['value'],validate=True);adr=req['address']
            if req['domain']!='System Bus' or not (self.box+6<=adr and adr+len(data)<=self.box+32):
                raise ValueError('Test transport permits writes only to AP mailbox input')
            self.r.write(adr,data);return {'type':'WRITE_RESPONSE'}
        if k=='DISPLAY_MESSAGE':return {'type':'DISPLAY_MESSAGE_RESPONSE'}
        raise ValueError('Unsupported '+k)
    async def accept(self,reader,writer):
        try:
            while line:=await reader.readline():
                if line.rstrip()==b'VERSION':writer.write(b'1\n')
                else:
                    responses=[];failed=None
                    for req in json.loads(line):
                        if failed is not None:res=failed
                        else:
                            try:res=self.request(req)
                            except Exception as e:res={'type':'ERROR','err':str(e)}
                        if res['type']=='GUARD_RESPONSE' and not res['value']:failed=res
                        responses.append(res)
                    writer.write(json.dumps(responses).encode()+b'\n')
                await writer.drain()
        except (ConnectionError,asyncio.CancelledError):pass
        finally:writer.close();await writer.wait_closed()

async def wait(condition,seconds=20):
    deadline=time.monotonic()+seconds
    while time.monotonic()<deadline:
        if condition():return
        await asyncio.sleep(.05)
    raise TimeoutError('Timed out waiting for test condition')

def launch_python(python,path,arguments,cwd,env,stdin,stdout):
    # unittest here enables AP's own test-world filter. Server and clients are
    # their real implementations; no protocol/game data is substituted.
    code='import unittest,runpy,sys;sys.argv='+repr([str(path),*arguments])+';runpy.run_path('+repr(str(path))+',run_name="__main__")'
    return subprocess.Popen([python,'-c',code],cwd=cwd,env=env,stdin=stdin,stdout=stdout,stderr=subprocess.STDOUT,text=True)

async def scenario(a,report):
    os.environ['YOKAI_QA_ROM']=str(a.build/'pokefirered_audio.gba');os.environ['YOKAI_QA_ELF']=str(a.build/'pokefirered_audio.elf')
    os.environ['MGBA_LIBRETRO_PATH']=str(a.libretro);sys.path.insert(0,str(a.build/'tools/yokai'))
    from mgba_new_game import new_game
    from postgame_qa_common import QA
    r=new_game();transport=NativeTransport(r);tcp=None;server=None;client=None;frames=None
    q=QA.__new__(QA);q.r=r;q.flags={};q.P=a.out.parent;q.checks=[]
    q.reverse={address|1:name for name,address in r.symbols.items()}
    groups=json.loads((a.build/'data/maps/map_groups.json').read_text())
    q.maps={name:(i,j) for i,key in enumerate(groups['group_order']) for j,name in enumerate(groups[key])}
    env=dict(os.environ,SKIP_REQUIREMENTS_UPDATE='1',AP_TEST_WORLDS='yokaiwatch2,mkwii,pokemon_yokai_firered')
    logs=[];events=a.out.parent/'firered-client-events.jsonl'
    if events.exists():events.unlink()
    def records():
        return [json.loads(l) for l in events.read_text().splitlines()] if events.exists() else []
    def ok(name,cond):
        if not cond:raise AssertionError(name)
        report['checks'].append(name);print('PASS',name,flush=True)
    def start_client(number):
        log=(a.out.parent/f'firered-client-{number}.log').open('w');logs.append(log)
        return launch_python(a.python,ROOT/'YOKAI_ARCHIPELAGO/CONNECTORS/mgba/connect_firered.py',
            ['--archipelago',str(a.archipelago),'--slot','Yoann_FireRed','--server',f'127.0.0.1:{a.server_port}',
             '--emulator-port',str(a.emulator_port),'--no-cli','--event-log',str(events)],str(a.archipelago),env,subprocess.DEVNULL,log)
    async def game_frames():
        while True:r.run(3);await asyncio.sleep(.005)
    try:
        tcp=await asyncio.start_server(transport.accept,'127.0.0.1',a.emulator_port,limit=2*1024*1024)
        serverlog=(a.out.parent/'firered-real-server.log').open('w');logs.append(serverlog)
        server=launch_python(a.python,a.archipelago/'MultiServer.py',
            ['--host','127.0.0.1','--port',str(a.server_port),'--loglevel','info','--disable_save',str(a.multidata)],
            str(a.archipelago),env,subprocess.PIPE,serverlog)
        frames=asyncio.create_task(game_frames());client=start_client(1)
        await wait(lambda:any(e['event']=='connected' for e in records()))
        box=transport.box
        await wait(lambda:r.read(box+39,1)==b'\1')
        ok('Real AP server authenticated the FireRed slot',client.poll() is None)
        before=r.call('BagGetQuantityByItemId',13)
        server.stdin.write('/send Yoann_FireRed Potion\n');server.stdin.flush()
        await wait(lambda:r.u32(box+32)==1)
        ok('Server gift reached real native bag',r.call('BagGetQuantityByItemId',13)==before+1)
        ok('Client received the actual AP item packet',any(e['event']=='received_items' and 13 in e['items'] for e in records()))
        client.terminate();client.wait(10);client=start_client(2)
        await wait(lambda:sum(e['event']=='connected' for e in records())>=2)
        await asyncio.sleep(1)
        ok('Network reconnect does not duplicate native gift',r.call('BagGetQuantityByItemId',13)==before+1 and r.u32(box+32)==1)
        if 'YokaiAPTryCollect' in r.symbols:
            server.stdin.write('/send Yoann_FireRed CS03 Surf\n');server.stdin.flush()
            await wait(lambda:r.call('BagGetQuantityByItemId',341)==1)
            ok('Progression Surf from real server reached native inventory',r.u32(box+32)==2)
            bag=r.u32(r.symbols['gSaveBlock1Ptr'])+0x310
            saved_bag=[(int.from_bytes(r.read(bag+4*i,2),'little'),r.call('GetBagItemQuantity',bag+4*i+2)) for i in range(42)]
            for i in range(42):
                r.write(bag+4*i,struct.pack('<H',13));r.call('SetBagItemQuantity',bag+4*i+2,999)
            server.stdin.write('/send Yoann_FireRed Potion\n');server.stdin.flush()
            await wait(lambda:int.from_bytes(r.read(box+36,2),'little')==3)
            ok('Real network gift stays pending when native bag is full',r.u32(box+32)==2)
        # Controlled party/position fixture, then native dialogue and battle.
        frames.cancel();await asyncio.gather(frames,return_exceptions=True);frames=None
        q.mon(0,65,100);r.call('SetMonMoveSlot',r.symbols['gPlayerParty'],280,0)
        q.warp('PewterCity_Gym',6,6);r.call('PlayerFaceDirection',2)
        ok('Badge is not set before the actual battle',r.call('FlagGet',0x820)==0)
        q.script('PewterCity_Gym_EventScript_Brock')
        for f in range(30000):
            if r.read(box+40,2)[0]&1:break
            if q.callback()=='BattleMainCB2':
                from pilote_combat_mgba import battle_keys
                r.keys=battle_keys(r,f)
            else:r.keys={8} if f%16<2 else set()
            r.run()
            if f%20==0:await asyncio.sleep(0)
        else:raise TimeoutError('Wyatt native battle did not award badge')
        r.keys=set();frames=asyncio.create_task(game_frames())
        ok('Wyatt native battle/script awarded badge',r.call('FlagGet',0x820)==1)
        await wait(lambda:any(e['event']=='sent' and e['packet'].get('cmd')=='LocationChecks' and 0x594B1000 in e['packet']['locations'] for e in records()))
        await wait(lambda:any(e['event']=='checked' and 0x594B1000 in e['locations'] for e in records()))
        ok('Real badge check acknowledged by AP server',True)
        if 'YokaiAPTryCollect' in r.symbols:
            ok('Outgoing badge check succeeds while receive queue is blocked by full bag',r.u32(box+32)==2)
            # Battles may rotate the save encryption key. Restore logical
            # quantities through the native setter, never old ciphertext.
            bag=r.u32(r.symbols['gSaveBlock1Ptr'])+0x310
            for i,(item,quantity) in enumerate(saved_bag):
                r.write(bag+4*i,struct.pack('<H',item));r.call('SetBagItemQuantity',bag+4*i+2,quantity)
            q.drain()  # finish any remaining native gym reward dialogue
            await wait(lambda:r.u32(box+32)>=3)
            ok('Pending network gift resumes after freeing bag',True)
            frames.cancel();await asyncio.gather(frames,return_exceptions=True);frames=None
            for flag,x,y,item,check in [(0x156,5,41,4,0x594B2156),(1000,3,22,13,0x594B23E8)]:
                # Prepare the native interaction context, then run its real
                # script. No collection flag or reward is injected.
                q.warp('ViridianForest',x,y+1)
                quantity=r.call('BagGetQuantityByItemId',item)
                ok('Ordinary source is uncollected before interaction '+str(flag),r.call('FlagGet',flag)==0)
                if flag==0x156:
                    r.write(r.symbols['gSpecialVar_LastTalked'],struct.pack('<H',6))
                    q.script('ViridianForest_EventScript_ItemPokeBall')
                else:
                    for name,value in [('gSpecialVar_0x8004',flag),('gSpecialVar_0x8005',item),('gSpecialVar_0x8006',1)]:
                        r.write(r.symbols[name],struct.pack('<H',value))
                    q.script('EventScript_HiddenItemScript')
                q.drain();r.run(10)
                ok('Native ordinary interaction sets check '+str(flag),r.call('FlagGet',flag)==1)
                ok('Original ordinary reward replaced '+str(flag),r.call('BagGetQuantityByItemId',item)==quantity)
                frames=asyncio.create_task(game_frames())
                await wait(lambda:any(e['event']=='checked' and check in e['locations'] for e in records()))
                ok('Server acknowledged ordinary check '+str(flag),True)
                frames.cancel();await asyncio.gather(frames,return_exceptions=True);frames=None
            q.warp('SafariZone_SecretHouse',3,4)
            ok('Surf source not consumed by receiving remote Surf',r.call('FlagGet',0x239)==0)
            q.script('SafariZone_SecretHouse_EventScript_Attendant');q.drain();r.run(10)
            ok('Native Safari gift validates its AP check',r.call('FlagGet',0x239)==1)
            ok('Native Safari gift does not duplicate randomized Surf',r.call('BagGetQuantityByItemId',341)==1)
            frames=asyncio.create_task(game_frames())
            await wait(lambda:any(e['event']=='checked' and 0x594B2239 in e['locations'] for e in records()))
            ok('Server acknowledged randomized Surf source',True)
            frames.cancel();await asyncio.gather(frames,return_exceptions=True);frames=None
            q.warp('PokemonLeague_HallOfFame',5,12)
            q.wait(lambda:r.call('GetGameStat',10)>0,limit=24000)
            r.keys=set();r.run(180)
            # Targeted endpoint fixture: skip credits by placing the player in
            # an overworld map after the real Hall record/save. No goal injection.
            q.warp('Route1',10,18)
            frames=asyncio.create_task(game_frames())
            await wait(lambda:any(e['event']=='sent' and e['packet'].get('cmd')=='StatusUpdate' and e['packet'].get('status')==30 for e in records()))
            await wait(lambda:'Yoann_FireRed (Team #1) has completed their goal.' in (a.out.parent/'firered-real-server.log').read_text())
            ok('Real native Hall record triggers Goal packet to server',True)
            report['hall_endpoint_position_prepared_by_fixture']=True
        report['requests']=transport.requests;report['passed']=True
    finally:
        if frames:frames.cancel();await asyncio.gather(frames,return_exceptions=True)
        for proc in [client,server]:
            if proc and proc.poll() is None:proc.terminate();proc.wait(10)
        if tcp:tcp.close();await tcp.wait_closed()
        for log in logs:log.close()
        r.close()

def main():
    p=argparse.ArgumentParser(description=__doc__)
    for name in ['build','libretro','archipelago','multidata','out']:p.add_argument('--'+name,type=Path,required=True)
    p.add_argument('--python',default=sys.executable);p.add_argument('--server-port',type=int,default=38281);p.add_argument('--emulator-port',type=int,default=43056);a=p.parse_args()
    a.out.parent.mkdir(parents=True,exist_ok=True)
    report={'passed':False,'kind':'real_server_real_mgba_libretro','gui_lua_tested':False,
            'party_and_location_prepared_by_fixture':True,'ordinary_interaction_context_prepared_by_fixture':True,
            'badge_flag_injected':False,'complete_playthrough':False,'checks':[]}
    try:asyncio.run(scenario(a,report))
    except Exception as e:
        import traceback;traceback.print_exc();report['error']=str(e)
    a.out.write_text(json.dumps(report,indent=2)+'\n');return 0 if report['passed'] else 1

if __name__=='__main__':raise SystemExit(main())
