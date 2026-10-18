#!/usr/bin/env python3
"""Native map objects/four facings; temporary spawn fixture, no map/source events added."""
import argparse,hashlib,json,re,struct
from PIL import Image,ImageDraw
from mgba_rpc import ROOT
from mgba_new_game import new_game
parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--stage',required=True);args=parser.parse_args()
P=ROOT/'QA_RECETTE_FINALE/POST_B13/SESSION_2_GRAPHISMES/overworld'/args.stage;P.mkdir(parents=True,exist_ok=True)
C={k:int(v,0) for k,v in re.findall(r'^#define\s+(\w+)\s+(0x[0-9a-fA-F]+|\d+)\b',
   '\n'.join((ROOT/f'include/constants/{n}.h').read_text() for n in ['event_objects','event_object_movement']),re.M)}
people=[('nathan','OBJ_EVENT_GFX_YOKAI_NATHAN'),('katie','OBJ_EVENT_GFX_YOKAI_KATIE'),('matt','OBJ_EVENT_GFX_BLUE'),
 ('ariane','OBJ_EVENT_GFX_ARIANE'),('nathaniel','OBJ_EVENT_GFX_YOKAI_NATHANIEL'),('michael','OBJ_EVENT_GFX_YOKAI_MICHAEL'),
 ('wyatt','OBJ_EVENT_GFX_YOKAI_WYATT'),('domniscian','OBJ_EVENT_GFX_YOKAI_DOMNISCIAN'),
 ('employe-rouge','OBJ_EVENT_GFX_YOKAI_EMPLOYEROUGE'),('employe-bleu','OBJ_EVENT_GFX_YOKAI_EMPLOYEBLEU'),
 ('don-morleone','OBJ_EVENT_GFX_YOKAI_DONMORLEONE'),('mafiamille-1','OBJ_EVENT_GFX_YOKAI_MAFIAMILLE1'),
 ('mafiamille-2','OBJ_EVENT_GFX_YOKAI_MAFIAMILLE2'),('mafiamille-3','OBJ_EVENT_GFX_YOKAI_MAFIAMILLE3'),
 ('lord-enma','OBJ_EVENT_GFX_YOKAI_ENMA'),('leo-jibanyan','OBJ_EVENT_GFX_YOKAI_LEO_JIBANYAN'),
 ('usapyon','OBJ_EVENT_GFX_USAPION_CAMEO'),('misterre','OBJ_EVENT_GFX_YOKAI_MISTERRE'),
 ('octorgone','OBJ_EVENT_GFX_YOKAI_OCTORGONE'),('mademoaiselle','OBJ_EVENT_GFX_YOKAI_MADEMOAISELLE'),
 ('kyubi','OBJ_EVENT_GFX_YOKAI_KYUBI'),('enma-creature','OBJ_EVENT_GFX_YOKAI_ENMA_CREATURE')]
groups=json.loads((ROOT/'data/maps/map_groups.json').read_text());maps={n:(i,j) for i,k in enumerate(groups['group_order']) for j,n in enumerate(groups[k])}
r=new_game();rows=[];passed=False;error='Interrupted'
try:
    r.call('CreateMon',r.symbols['gPlayerParty'],1,30,31,1,100,1,0);r.write(r.symbols['gPlayerPartyCount'],b'\x01')
    r.call('VarSet',0x4050,3);r.call('VarSet',0x4055,9)
    g,n=maps['PalletTown'];r.call('SetWarpDestination',g,n,255,8,16);r.call('WarpIntoMap');r.call('SetMainCallback2',r.symbols['CB2_LoadMap']|1);r.run(600)
    base=r.snapshot()
    for name,constant in people:
        r.restore(base);gfx=C[constant]
        object_id=r.call('SpawnSpecialObjectEventParameterized',gfx,C['MOVEMENT_TYPE_FACE_DOWN'],200,17,23,3)
        assert object_id<16,(name,object_id)
        obj=r.symbols['gObjectEvents']+36*object_id;assert r.read(obj+5,1)[0]==gfx
        frames=[];poses=[]
        for direction,label in [(1,'sud'),(2,'nord'),(3,'ouest'),(4,'est')]:
            r.call('ObjectEventTurn',obj,direction);r.run(30)
            sprite=r.symbols['gSprites']+68*r.read(obj+4,1)[0]
            assert r.read(sprite+62,1)[0]&1,(name,'Sprite inactive')
            assert not r.read(sprite+62,1)[0]&4,(name,'Sprite invisible')
            frames.append(r.frame.copy());r.frame.save(P/f'{name}-{label}.png')
            poses.append(dict(direction=label,position=list(struct.unpack('<hh',r.read(sprite+32,4))),
                              anim_num=r.read(sprite+42,1)[0],oam_attribute1=int.from_bytes(r.read(sprite+2,2),'little')))
        sheet=Image.new('RGB',(960,180),(224,224,224));d=ImageDraw.Draw(sheet)
        for i,f in enumerate(frames):d.text((i*240+4,2),name+' '+poses[i]['direction'],fill='black');sheet.paste(f,(i*240,20))
        sheet.save(P/(name+'-quatre-directions.png'))
        rows.append(dict(person=name,graphics_id=gfx,actual_native_map_sprite=True,temporary_spawn_only=True,poses=poses,
            walking_policy='Native9-frame walk exists' if name in ['nathan','katie','matt'] else 'Stationary event or creature; native facing poses, not a claimed new walking animation'))
        print('OW',name,flush=True)
    passed=True;error=None
except BaseException as e:error=str(e);r.frame.save(P/'diagnostic.png');raise
finally:
    r.close();(P/'TEST_GALERIE_MGBA.json').write_text(json.dumps(dict(passed=passed,error=error,
        rom_sha256=hashlib.sha256(r.rom_buffer.raw[:-1]).hexdigest(),results=rows,
        scope='Real new-game then actual native object spawning on Pallet Town as a temporary RAM fixture; four orientations rendered. Not actual story placements/interactions or a whole adventure.'),ensure_ascii=False,indent=2)+'\n')
if passed:
    # Fixed-camera fixture crop in screen coordinates, not sprite.pos1: native
    # map rendering also applies global sprite/camera offsets. Full native
    # frames above remain the primary evidence (no hidden-background crops).
    sheet=Image.new('RGB',(1408,900),(224,224,224));draw=ImageDraw.Draw(sheet)
    for i,row in enumerate(rows):
        x=i%4*352;y=i//4*150;draw.text((x+4,y+2),row['person'],fill='black')
        for j,pose in enumerate(row['poses']):
            frame=Image.open(P/f"{row['person']}-{pose['direction']}.png")
            view=frame.crop((132,44,172,92)).resize((80,96),Image.Resampling.NEAREST)
            sheet.paste(view,(x+86*j,y+20))
    sheet.save(P/'planche-22-acteurs.png')
