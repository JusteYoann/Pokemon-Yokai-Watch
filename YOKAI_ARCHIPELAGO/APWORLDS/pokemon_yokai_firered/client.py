"""Vrai client AP pour le canal C du fangame ; aucun accès sans profil de build validé."""
from __future__ import annotations
import hashlib
import json
import logging
import pkgutil
import struct
import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient
from NetUtils import ClientStatus

MAGIC=0x31504B59
BASE_SHA1='40c59a9f240d29a7b16d1dd299b1125513a280c4'
GAME='Pokemon Yo-kai FireRed'
LOCATION_BASE=0x594B1000
logger=logging.getLogger('Client')


def decode(raw):
    if len(raw)!=48:raise ValueError('Mailbox FireRed : 48 octets requis')
    u16=lambda n:int.from_bytes(raw[n:n+2],'little')
    u32=lambda n:int.from_bytes(raw[n:n+4],'little')
    return {'magic':u32(0),'version':u16(4),'command':u16(6),'slot':u16(8),'item':u16(10),
            'index':u32(12),'seed':raw[16:32],'applied':u32(32),'error':u16(36),
            'ready':raw[38],'bound':raw[39],'checks':u16(40),'goal':raw[42],'quantity':u16(44)}


class YokaiFireRedClient(BizHawkClient):
    game=GAME
    system='GBA'
    patch_suffix=None  # one source-built AP ROM, no fake per-seed binary patch

    def __init__(self):
        try:self.profile=json.loads(pkgutil.get_data(__package__,'build.json'))
        except (OSError,TypeError,FileNotFoundError):self.profile=None
        self.confirmed=False;self.reported_checks=None;self.last_error=None

    async def validate_rom(self,ctx):
        if self.profile is None:return False
        try:
            rom=(await bizhawk.read(ctx.bizhawk_ctx,[(self.profile['rom_info']-0x08000000,81,'ROM')]))[0]
            if int.from_bytes(rom[:4],'little')!=MAGIC or rom[4:8]!=struct.pack('<HH',3,48):return False
            if rom[8:40].split(b'\0',1)[0].decode('ascii')!=GAME:return False
            if rom[40:81].split(b'\0',1)[0].decode('ascii')!=BASE_SHA1:return False
            raw=(await bizhawk.read(ctx.bizhawk_ctx,[(self.profile['mailbox'],48,'System Bus')]))[0]
            snap=decode(raw)
            if snap['magic']!=MAGIC or snap['version']!=3:return False
            native_hash=(await bizhawk.read(ctx.bizhawk_ctx,[(self.profile['catalog_hash_address']-0x08000000,65,'ROM')]))[0]
            if native_hash.rstrip(b'\0').decode('ascii')!=self.profile['catalog_sha256']:return False
        except (bizhawk.RequestFailedError,UnicodeError,ValueError):return False
        ctx.game=GAME;ctx.want_slot_data=True;ctx.items_handling=0b111;ctx.watcher_timeout=0.1
        self.confirmed=False;self.reported_checks=None;self.last_error=None
        return True

    def on_package(self,ctx,cmd,args):
        if cmd=='Connected':
            self.confirmed=False;self.reported_checks=None;self.last_error=None;ctx.finished_game=False

    async def game_watcher(self,ctx):
        if ctx.server is None or ctx.server.socket.closed or ctx.slot_data is None:return
        if ctx.slot_data.get('protocol')!=3 or self.profile is None or ctx.slot_data.get('mode')!=self.profile['mode'] or ctx.slot_data.get('catalog_sha256')!=self.profile['catalog_sha256']:
            raise RuntimeError('Le slot et le canal FireRed utilisent des protocoles différents')
        if self.profile is None or not ctx.server_seed_name or not ctx.slot:return
        box=self.profile['mailbox']
        seed=hashlib.sha256(ctx.server_seed_name.encode('utf-8')).digest()[:16]
        try:
            raw,pointer,bits=await bizhawk.read(ctx.bizhawk_ctx,[(box,48,'System Bus'),
                                  (self.profile['saveblock2_pointer'],4,'System Bus'),(self.profile['checks'],self.profile['checks_bytes'],'System Bus')])
            snap=decode(raw)
            if snap['magic']!=MAGIC or snap['version']!=3 or not snap['ready']:return
            guards=[(box,struct.pack('<IH',MAGIC,3),'System Bus'),(box+6,b'\0\0','System Bus'),
                    (box+38,b'\1','System Bus'),(self.profile['saveblock2_pointer'],pointer,'System Bus')]
            if not self.confirmed:
                if snap['error']==1 and snap['seed']==seed and snap['slot']==ctx.slot:
                    if self.last_error!=1:logger.error('Sauvegarde liée à une autre graine/slot : aucun don ni check envoyé.')
                    self.last_error=1;return
                if snap['bound'] and snap['seed']==seed and snap['slot']==ctx.slot and snap['error'] in (0,3):
                    self.confirmed=True
                else:
                    await bizhawk.guarded_write(ctx.bizhawk_ctx,[(box+8,struct.pack('<H',ctx.slot),'System Bus'),
                        (box+16,seed,'System Bus'),(box+6,struct.pack('<H',1),'System Bus')],guards)
                    return
            if not snap['bound'] or snap['seed']!=seed or snap['slot']!=ctx.slot:
                self.confirmed=False;return
            checks={LOCATION_BASE+i for i in range(8) if snap['checks'] & (1<<i)} & ctx.server_locations
            ids=ctx.slot_data.get('check_ids',[])
            if not ids or len(ids)>self.profile['checks_bytes']*8:raise RuntimeError('Liste des collectes FireRed incompatible')
            checks |= {code for i,code in enumerate(ids) if bits[i//8] & (1<<(i%8))} & ctx.server_locations
            if checks!=self.reported_checks:
                await ctx.check_locations(checks);self.reported_checks=checks
            if snap['goal'] and not ctx.finished_game:
                await ctx.send_msgs([{'cmd':'StatusUpdate','status':ClientStatus.CLIENT_GOAL}]);ctx.finished_game=True
            if snap['command']:
                if snap['error']==3 and self.last_error!=3:
                    logger.warning('Sac plein : libère de la place pour recevoir l’objet AP. Les checks continuent d’être envoyés.')
                self.last_error=snap['error']
                return  # don't overwrite the native pending receive request
            self.last_error=None
            if snap['error'] in (2,4,5):
                raise RuntimeError(f'Canal FireRed refuse le don (code {snap["error"]}) ; inventaire préservé')
            if snap['applied']>=len(ctx.items_received):return
            item=ctx.items_received[snap['applied']]
            guards += [(box+16,seed,'System Bus'),(box+32,struct.pack('<I',snap['applied']),'System Bus')]
            await bizhawk.guarded_write(ctx.bizhawk_ctx,[(box+10,struct.pack('<HI',item.item,snap['applied']+1),'System Bus'),
                         (box+6,struct.pack('<H',2),'System Bus')],guards)
        except (bizhawk.RequestFailedError,bizhawk.NotConnectedError):return
