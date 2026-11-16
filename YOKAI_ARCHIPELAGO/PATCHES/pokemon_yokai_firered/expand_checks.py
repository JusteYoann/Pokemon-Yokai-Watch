"""Audited expansion, retaining all legacy IDs. MIT reference metadata is attributed."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
from inventory_checks import inventory,constants

PROJECT=Path(__file__).resolve().parents[2]
EARLY={'Route2','ViridianForest','ViridianCity','PewterCity','Route4','Route24','Route25',
       'MtMoon_1F','MtMoon_B1F','MtMoon_B2F'}
LATE={'RockTunnel_1F','RockTunnel_B1F','PokemonTower_3F','PokemonTower_4F','PokemonTower_5F',
      'PokemonTower_6F','PokemonTower_7F','RocketHideout_B1F','RocketHideout_B2F','RocketHideout_B3F','RocketHideout_B4F'}
AIDES=[('Route2_EastBuilding','FLAG_GOT_HM05','ITEM_HM05',10),
       ('Route10_PokemonCenter_1F','FLAG_GOT_EVERSTONE_FROM_OAKS_AIDE','ITEM_EVERSTONE',20),
       ('Route11_EastEntrance_2F','FLAG_GOT_ITEMFINDER','ITEM_ITEMFINDER',30),
       ('Route16_NorthEntrance_2F','FLAG_GOT_AMULET_COIN_FROM_OAKS_AIDE','ITEM_AMULET_COIN',40),
       ('Route15_WestEntrance_2F','FLAG_GOT_EXP_SHARE_FROM_OAKS_AIDE','ITEM_EXP_SHARE',50)]

def capture_capacity(source):
    species=constants(source/'include/constants/species.h')
    active_ids=set(map(int,re.search(r'bool8 BestiarySpeciesActive.*?ids\[\] = \{([^}]+)',
        (source/'src/yokai_bestiary.c').read_text(),re.S)[1].split(',')))
    first={'MAP_ROUTE'+str(i) for i in [1,2,3,4,5,6,9,10,11,24,25]}|{
        'MAP_VIRIDIAN_FOREST','MAP_MT_MOON_1F','MAP_MT_MOON_B1F','MAP_MT_MOON_B2F','MAP_DIGLETTS_CAVE',
        'MAP_VIRIDIAN_CITY','MAP_CERULEAN_CITY','MAP_VERMILION_CITY'}
    second=first|{'MAP_ROUTE'+str(i) for i in range(1,19)}|{'MAP_CELADON_CITY','MAP_FUCHSIA_CITY'}
    data=json.loads((source/'src/data/wild_encounters.json').read_text());found=[set(),set()];evidence=[[],[]]
    for group in data['wild_encounter_groups']:
        for entry in group.get('encounters',[]):
            if 'LeafGreen' in entry['base_label']:continue
            mp=entry['map']
            for stage in (0,1):
                eligible=mp in (first if stage==0 else second) or (stage==1 and mp.startswith(('MAP_SAFARI_ZONE','MAP_ROCK_TUNNEL','MAP_POKEMON_TOWER')))
                if not eligible:continue
                for method in ('land_mons','fishing_mons'):
                    if entry.get(method,{}).get('encounter_rate',0)<=0:continue
                    mons=entry.get(method,{}).get('mons',[])
                    if stage==0 and method=='fishing_mons':mons=mons[:2] # native Old Rod; others in Fuchsia/Route12
                    for mon in mons:
                        number=species.get(mon['species'],0)
                        if 1<=number<=151 and number in active_ids:
                            found[stage].add(number);evidence[stage].append({'map':mp,'method':method,'species':number})
    # Only natural level evolutions <=30; don't assume AP stones, trade or late levels.
    evos=[]
    for line in (source/'src/data/pokemon/evolution.h').read_text().splitlines():
        m=re.match(r'\s*\[(\d+)\]',line)
        if m:
            for level,dest in re.findall(r'\{EVO_LEVEL, (\d+), (\d+)\}',line):
                if int(level)<=30 and int(dest)<=151 and int(dest) in active_ids:evos.append((int(m[1]),int(dest),int(level)))
    used=[]
    expanded=set(found[1])
    changed=True
    while changed:
        changed=False
        for src,dest,level in evos:
            if src in expanded and dest not in expanded:
                expanded.add(dest);used.append({'from':src,'to':dest,'level':level});changed=True
    assert len(found[0])>=10 and len(expanded)>=50,'Capture capacity insufficient for native thresholds'
    return {'counter':'GetKantoPokedexCount(FLAG_GET_CAUGHT), first151 national entries, not all301',
        'pre_flash_count':len(found[0]),'pre_surf_count_with_level30_evolutions':len(expanded),
        'pre_flash_species':sorted(found[0]),'pre_surf_species':sorted(expanded),'level_evolutions_used':used,
        'wild_evidence':evidence,'assumptions':['Native Pokedex, rods, Cut, story keys and shops remain available; no encounter randomization.',
            'AP models capability to catch; the native aide still checks the actual caught count. No seen-count substitution.']}

def build_catalog(source):
    data=inventory(source);flags=constants(source/'include/constants/flags.h');items=constants(source/'include/constants/items.h')
    var=constants(source/'include/constants/vars.h')
    reference=json.loads((PROJECT/'DOCUMENTATION/FRLG_COMPARAISON.json').read_text())
    ref={r['native_flag']:r for r in reference['rows'] if r['native_flag']}
    legacy=[c['id'] for c in data['checks'] if c['status']=='active']
    item_records={v['itemId']:v for v in json.loads((source/'src/data/items.json').read_text())['items']}
    for c in data['checks']:
        if c['kind']=='hidden':
            bg=json.loads((source/f"data/maps/{c['map']}/map.json").read_text()).get('bg_events',[])
            c['underfoot']=next(e.get('underfoot',False) for e in bg if e.get('flag')==c['flag'])
        r=ref.get(c['flag'])
        if r:c.update(upstream_key=r['upstream_key'],upstream_ap_id=r['upstream_ap_id'],upstream_region=r['upstream_region'],category=r['category'])
        c['access']='flash' if c['map'] in LATE or c['map']=='SafariZone_SecretHouse' else 'native_early'
        if c['status']=='active':continue
        record=item_records.get(c['original_item'],{})
        if c['map'] in EARLY|LATE and r and c['quantity']==1 and not c.get('underfoot',False) and record.get('pocket') in ('POCKET_ITEMS','POCKET_POKE_BALLS','POCKET_TM_CASE','POCKET_BERRIES') and not c['original_item'].startswith('ITEM_HM'):
            # Never activate renewable hidden flags: these are not durable checks.
            renewable=(source/'src/renewable_hidden_items.c').read_text()
            if c['flag'] in renewable:continue
            c.update(status='active',original_reward='replaced',prerequisites=['Progression native',c['access']],risks=[])
            c['name_fr']=f"{c['map']} — {'objet caché' if c['kind']=='hidden' else 'objet'} ({c['x']},{c['y']})"
    for mp,flag,item,threshold in AIDES:
        path=source/f'data/maps/{mp}/scripts.inc';text=path.read_text()
        assert re.search(r'\.equ REQUIRED_\w+MONS, '+str(threshold)+r'\b',text)
        assert 'giveitem_msg ' in text and '\tsetflag '+flag in text
        data['checks'].append({'id':0x594B2000+flags[flag],'name_fr':f'Assistant Chen — {threshold} espèces capturées',
            'map':mp,'flag':flag,'flag_value':flags[flag],'original_item':item,'quantity':1,'kind':'aide',
            'status':'active','original_reward':'replaced','source':f'data/maps/{mp}/scripts.inc',
            'script_source':f'data/maps/{mp}/scripts.inc','script':mp+'_EventScript_Aide','mandatory':False,
            'validation':f'FlagGet({flag}), native caught-count >= {threshold}', 'caught_required':threshold,
            'access':'flash' if threshold>=30 else 'native_early','prerequisites':[f'{threshold} captured in native Kanto counter'],
            'upstream_key':'NPC_GIFT_'+flag[5:],'upstream_region':ref.get(flag,{}).get('upstream_region'),'category':'NPC_GIFT','risks':[]})
    for name,variable,value,code,mp,access in [
        ('Bingo-kai — pièces de bienvenue','VAR_BINGO_GIFTS',3,0,'ViridianForest','native_early'),
        ('Jibanyan — amitié conclue','VAR_JIBANYAN_FRIEND',3,1,'ViridianCity_Mart','native_early')]:
        data['checks'].append({'id':0x594B4000+code,'name_fr':name,'kind':'event','variable':variable,
            'variable_value':var[variable],'target_value':value,'map':mp,'access':access,'status':'active',
            'category':'FANGAME_EVENT','original_reward':'native_protected_separate_AP_check',
            'source':'src/bingo_kai.c','script_source':'data/scripts/bingo_kai.inc','mandatory':False,
            'validation':f'VarGet({variable}) == {value}','prerequisites':['Native introduction/quest'], 'risks':[]})
    data['checks'].append({'id':0x594B4002,'name_fr':'Terr’heure — première manifestation','flag':'FLAG_ONI_FIRST_SEEN',
        'flag_value':flags['FLAG_ONI_FIRST_SEEN'],'kind':'event','access':'optional_random','map':'Caves éligibles',
        'status':'active','category':'FANGAME_EVENT','original_reward':'native_preserved_filler_only',
        'source':'src/terre_heure.c:539','script_source':'src/terre_heure.c:539','mandatory':False,
        'validation':'FlagGet(FLAG_ONI_FIRST_SEEN)','prerequisites':['Random native event'],'risks':['RNG: filler only, option disabled by default']})
    active=[c for c in data['checks'] if c['status']=='active']
    assert len({c['id'] for c in active})==len(active)
    assert set(legacy).issubset(c['id'] for c in active)
    assert len(active)+8<=512
    for c in active:
        if 'original_item' in c:
            c['native_item_id']=items[c['original_item']]
            c['item_name']=item_records[c['original_item']]['english']
    data['legacy_pickup_ids']=legacy;data['capture_capacity']=capture_capacity(source)
    canonical=[(c['id'],c.get('flag_value',0),c.get('variable_value',0),c.get('target_value',0)) for c in active]
    data['catalog_sha256']=hashlib.sha256(json.dumps(canonical,separators=(',',':')).encode()).hexdigest()
    data['summary_active']=dict(Counter(c['kind'] for c in active));return data
