#!/usr/bin/env python3
"""Real four-slot server test with SIMULATED game checks, not four emulators.

Routes actual seed placements through four WebSocket clients, tests duplicate
checks, reconnect and server save/restart. No admin item injection or fake Goal.
The isolated server save is temporary; the players' seed stays untouched.
"""
import argparse,asyncio,json,os,subprocess,sys,tempfile,time,uuid
from pathlib import Path

async def until(predicate,seconds=20):
    end=time.monotonic()+seconds
    while time.monotonic()<end:
        if predicate():return
        await asyncio.sleep(.04)
    raise TimeoutError('Server test condition timed out')

async def scenario(a,report):
    os.environ.update(SKIP_REQUIREMENTS_UPDATE='1',AP_TEST_WORLDS='yokaiwatch2,mkwii,pokemon_yokai_firered,pokemon_yokai_emerald')
    import unittest  # official AP_TEST_WORLDS filtering
    sys.path.insert(0,str(a.archipelago.resolve()))
    import websockets
    from MultiServer import Context
    from NetUtils import encode,decode
    from Utils import version_tuple
    data=Context.decompress(a.multidata.read_bytes())
    slots=data['slot_info'];assert len(slots)==4
    choices={}
    for origin,locations in sorted(data['locations'].items()):
        for loc,(item,dest,flags) in sorted(locations.items()):
            if origin!=dest and flags&1:choices.setdefault((origin,dest),(loc,item,flags))
    assert {s for s,d in choices}=={d for s,d in choices}==set(slots)
    def ok(label,value=True):
        if not value:raise AssertionError(label)
        report['checks'].append(label);print('PASS',label,flush=True)
    class Client:
        def __init__(self,slot):
            self.slot=slot;self.ws=None;self.task=None;self.connected=None
            self.items=[];self.received_packets=0;self.errors=[]
        async def consume(self):
            try:
                async for raw in self.ws:
                    for packet in decode(raw):
                        cmd=packet['cmd']
                        if cmd=='Connected':self.connected=packet
                        elif cmd=='ConnectionRefused':self.errors.append(packet);raise RuntimeError(str(packet))
                        elif cmd=='ReceivedItems':
                            idx=packet['index'];self.items[idx:]=list(packet['items']);self.received_packets+=1
            except websockets.ConnectionClosed:pass
        async def open(self):
            for attempt in range(100):
                try:self.ws=await websockets.connect(f'ws://127.0.0.1:{a.port}',open_timeout=1);break
                except OSError:await asyncio.sleep(.1)
            else:raise TimeoutError('Local server did not start')
            room=decode(await self.ws.recv());assert any(p['cmd']=='RoomInfo' for p in room)
            await self.ws.send(encode([{'cmd':'Connect','password':'','game':slots[self.slot].game,
                'name':slots[self.slot].name,'uuid':'four-test-'+str(self.slot),'items_handling':7,
                'tags':['AP'],'slot_data':True,'version':version_tuple}]))
            self.task=asyncio.create_task(self.consume())
            await until(lambda:self.connected is not None or bool(self.errors))
            if self.errors:raise RuntimeError(str(self.errors))
            assert self.connected['slot']==self.slot
        async def send(self,packet):await self.ws.send(encode([packet]))
        async def sync(self):
            before=self.received_packets;await self.send({'cmd':'Sync'})
            await until(lambda:self.received_packets>before)
        async def close(self):
            if self.ws:await self.ws.close()
            if self.task:await asyncio.gather(self.task,return_exceptions=True)
    clients={};proc=None;log=None
    with tempfile.TemporaryDirectory(prefix='four-server-',dir=a.out.parent) as temp:
        save=Path(temp)/'test.apsave'
        isolated_multidata=Path(temp)/'test.archipelago'
        isolated_multidata.write_bytes(a.multidata.read_bytes())
        # AP0.6.9 parses --savefile but its main ignores it. Use an isolated
        # multidata sibling instead, preserving the actual players' folder.
        def launch():
            code='import unittest,runpy,sys;sys.argv='+repr(['MultiServer.py','--host','127.0.0.1','--port',str(a.port),str(isolated_multidata)])+';runpy.run_path("MultiServer.py",run_name="__main__")'
            return subprocess.Popen([sys.executable,'-c',code],cwd=a.archipelago,env=os.environ.copy(),stdin=subprocess.PIPE,stdout=log,stderr=subprocess.STDOUT,text=True)
        async def open_all():
            result={i:Client(i) for i in slots}
            await asyncio.gather(*(c.open() for c in result.values()));return result
        try:
            log=(a.out.parent/'four-real-server.log').open('w');proc=launch();clients=await open_all()
            for i in slots:ok('Authenticated actual slot '+slots[i].name)
            for (origin,dest),(loc,item,flags) in choices.items():
                await clients[origin].send({'cmd':'LocationChecks','locations':[loc]})
                await until(lambda:any(x.item==item and x.location==loc and x.player==origin for x in clients[dest].items))
                ok('Actual seed progression routed '+slots[origin].name+' -> '+slots[dest].name)
            # Sync guarantees that the complete received-item list is observed.
            await asyncio.gather(*(c.sync() for c in clients.values()))
            expected={i:list(c.items) for i,c in clients.items()}
            for origin in slots:
                locations=[loc for (s,d),(loc,item,flags) in choices.items() if s==origin]
                await clients[origin].send({'cmd':'LocationChecks','locations':locations})
            await asyncio.gather(*(c.sync() for c in clients.values()))
            for i,c in clients.items():ok('Duplicate checks award no second item '+slots[i].name,c.items==expected[i])
            await asyncio.gather(*(c.close() for c in clients.values()));clients=await open_all()
            for i,c in clients.items():
                await c.sync()
                ok('Reconnect preserves indexed items '+slots[i].name,c.items==expected[i])
                own={loc for (s,d),(loc,item,flags) in choices.items() if s==i}
                ok('Reconnect confirms origin checks '+slots[i].name,own.issubset(c.connected['checked_locations']))
            proc.stdin.write('/save\n');proc.stdin.flush();await until(lambda:save.exists() and save.stat().st_size>0)
            ok('Real server wrote isolated save to disk')
            await asyncio.gather(*(c.close() for c in clients.values()));clients={}
            proc.terminate();proc.wait(timeout=10);proc=launch();clients=await open_all()
            for i,c in clients.items():
                await c.sync()
                ok('Server restart restores items '+slots[i].name,c.items==expected[i])
                own={loc for (s,d),(loc,item,flags) in choices.items() if s==i}
                ok('Server restart restores checks '+slots[i].name,own.issubset(c.connected['checked_locations']))
            report.update(passed=True,seed_name=data['seed_name'],tested_slots={i:slots[i].name for i in slots},
                simulated_location_checks=len(choices),routed_progression_directions=len(choices),
                incoming_progression_items={slots[i].name:sum(1 for s,d in choices if d==i) for i in slots})
        finally:
            await asyncio.gather(*(c.close() for c in clients.values()),return_exceptions=True)
            if proc and proc.poll() is None:proc.terminate();proc.wait(timeout=10)
            if log:log.close()

def main():
    p=argparse.ArgumentParser(description=__doc__)
    for n in ('archipelago','multidata','out'):p.add_argument('--'+n,type=Path,required=True)
    p.add_argument('--port',type=int,default=38284);a=p.parse_args();a.out.parent.mkdir(parents=True,exist_ok=True)
    report={'passed':False,'kind':'real_four_slot_server_simulated_game_checks','four_native_games_tested':False,
            'admin_item_injection':False,'goal_injection':False,'checks':[]}
    try:asyncio.run(scenario(a,report))
    except Exception as e:
        import traceback;traceback.print_exc();report['error']=str(e)
    a.out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');return 0 if report['passed'] else 1

if __name__=='__main__':raise SystemExit(main())
