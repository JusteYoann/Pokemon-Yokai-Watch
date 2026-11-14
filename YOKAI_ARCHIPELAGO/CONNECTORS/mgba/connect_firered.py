#!/usr/bin/env python3
"""Client sans GUI pour le mode bonus Rouge Feu, port mGBA réservé et vrais événements réseau."""
import argparse,asyncio,json,logging,os
from pathlib import Path
import sys,time

async def run(a):
    os.environ['SKIP_REQUIREMENTS_UPDATE']='1';sys.path.insert(0,str(a.archipelago.resolve()))
    from CommonClient import server_loop
    import worlds._bizhawk as bizhawk
    from worlds._bizhawk.context import BizHawkClientContext,_game_watcher
    from worlds._bizhawk.client import AutoBizHawkClientRegister
    game='Pokemon Yo-kai FireRed'
    handlers=AutoBizHawkClientRegister.game_handlers.get(('GBA',),{})
    if game not in handlers or handlers[game].profile is None:
        raise RuntimeError('Installer l’APWorld FireRed construit avec le profil de votre compilation')
    # Each process follows only the selected game's port and handler.
    AutoBizHawkClientRegister.game_handlers={('GBA',):{game:handlers[game]}}
    bizhawk.BIZHAWK_SOCKET_PORT_RANGE_START=a.emulator_port;bizhawk.BIZHAWK_SOCKET_PORT_RANGE_SIZE=1
    def event(kind,**values):
        if a.event_log:
            a.event_log.parent.mkdir(parents=True,exist_ok=True)
            with a.event_log.open('a',encoding='utf-8') as f:f.write(json.dumps({'time':time.time(),'event':kind,**values})+'\n')
        logging.info('%s %s',kind,values)
    class Context(BizHawkClientContext):
        def on_package(self,cmd,args):
            super().on_package(cmd,args)
            if cmd=='Connected':event('connected',slot=args['slot'])
            if cmd=='ReceivedItems':event('received_items',index=args['index'],items=[i.item for i in args['items']])
            if cmd=='RoomUpdate' and 'checked_locations' in args:event('checked',locations=args['checked_locations'])
        async def send_msgs(self,msgs):
            await super().send_msgs(msgs)
            for msg in msgs:
                if msg.get('cmd') in ['LocationChecks','StatusUpdate']:event('sent',packet=msg)
    ctx=Context(a.server,os.environ.get('YOKAI_AP_PASSWORD'));ctx.auth=a.slot;ctx.username=a.slot
    ctx.server_task=asyncio.create_task(server_loop(ctx),name='Server')
    if not a.no_cli:ctx.run_cli()
    tasks=[asyncio.create_task(_game_watcher(ctx)),asyncio.create_task(ctx.exit_event.wait())]
    if a.duration:tasks.append(asyncio.create_task(asyncio.sleep(a.duration)))
    try:
        done,_=await asyncio.wait(tasks,return_when=asyncio.FIRST_COMPLETED)
        for task in done:
            if not task.cancelled() and task.exception():raise task.exception()
    finally:
        ctx.exit_event.set()
        for task in tasks:task.cancel()
        await asyncio.gather(*tasks,return_exceptions=True);bizhawk.disconnect(ctx.bizhawk_ctx);await ctx.shutdown()

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--archipelago',type=Path,required=True)
    p.add_argument('--server',default='localhost:38281');p.add_argument('--slot',required=True)
    p.add_argument('--emulator-port',type=int,choices=range(43055,43060),default=43056)
    p.add_argument('--event-log',type=Path);p.add_argument('--duration',type=float);p.add_argument('--no-cli',action='store_true');a=p.parse_args()
    if not (a.archipelago/'MultiServer.py').is_file():p.error('Dossier Archipelago invalide')
    logging.basicConfig(level=logging.INFO,format='%(message)s')
    try:asyncio.run(run(a))
    except KeyboardInterrupt:return 130
    return 0

if __name__=='__main__':raise SystemExit(main())
