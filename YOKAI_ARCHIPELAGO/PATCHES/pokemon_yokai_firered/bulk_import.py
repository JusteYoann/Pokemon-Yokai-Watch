"""Technical correspondence for every FRLG category. No game assets imported."""
from collections import Counter,defaultdict
import json,re
from pathlib import Path
from inventory_checks import constants

EARLY_MAPS={'PalletTown','ViridianCity','PewterCity','CeruleanCity','VermilionCity','ViridianForest','DiglettsCave',
    'MtMoon','Route1','Route2','Route3','Route4','Route5','Route6','Route9','Route10','Route11','Route24','Route25'}
LATE_MAPS={'LavenderTown','CeladonCity','SaffronCity','FuchsiaCity','PokemonTower','RockTunnel','RocketHideout','SilphCo',
    'SafariZone','Route7','Route8','Route12','Route13','Route14','Route15','Route16','Route17','Route18'}
SEA_MAPS={'CinnabarIsland','PokemonMansion','SeafoamIslands','PowerPlant','VictoryRoad','IndigoPlateau','PokemonLeague',
    'Route19','Route20','Route21','Route22','Route23'}
def access_for_map(name):
    if name=='ViridianCity_Gym':return 'surf' # native door needs badge7, unlike the rest of the town
    prefix=name.split('_')[0]
    if prefix in SEA_MAPS:return 'surf'
    if prefix in LATE_MAPS:return 'flash'
    if prefix in EARLY_MAPS:return 'native_early'
    return None

def obtainable_dex(source,maps):
    """Positive witness: fixed wild encounters or natural evolutions, no random gifts."""
    species=constants(source/'include/constants/species.h')
    text=(source/'include/constants/pokedex.h').read_text()
    enum=re.search(r'enum\s*\{(.*?)\};',text,re.S)[1]
    enum=re.sub(r'/\*.*?\*/|//[^\n]*','',enum,flags=re.S)
    dex={};value=0
    for token in enum.split(','):
        token=token.strip()
        if not token:continue
        parts=token.split('=');name=parts[0].strip()
        if len(parts)>1:value=int(parts[1].strip(),0)
        dex[name]=value;value+=1
    active=set(map(int,re.search(r'bool8 BestiarySpeciesActive.*?ids\[\] = \{([^}]+)',(source/'src/yokai_bestiary.c').read_text(),re.S)[1].split(',')))
    mapping={species['SPECIES_'+name]:dex['NATIONAL_DEX_'+name] for name in re.findall(r'SPECIES_TO_NATIONAL\((\w+)\)',(source/'src/pokemon.c').read_text())
             if 'SPECIES_'+name in species and 'NATIONAL_DEX_'+name in dex and species['SPECIES_'+name] in active}
    # GenerateWildMon deliberately substitutes these wild species before HOF.
    banned={species[k] for k in ('SPECIES_VENONAT','SPECIES_DODUO','SPECIES_ZAPDOS','SPECIES_CHARMELEON','SPECIES_NIDORAN_F','SPECIES_DEWGONG')}
    fallback=species['SPECIES_CLOYSTER']
    rank={'native_early':0,'flash':1,'surf':2};found={};evidence={};methods={}
    data=json.loads((source/'src/data/wild_encounters.json').read_text())
    for group in data['wild_encounter_groups']:
        for entry in group.get('encounters',[]):
            if 'LeafGreen' in entry['base_label'] or entry['map'] not in maps:continue
            stage=access_for_map(maps[entry['map']]['name'])
            if not stage:continue
            for method in ('land_mons','water_mons','fishing_mons'):
                info=entry.get(method,{})
                if info.get('encounter_rate',0)<=0:continue
                methods.setdefault(entry['map'],set()).add(method)
                for slot,mon in enumerate(info.get('mons',[])):
                    sid=species.get(mon['species']);sid=fallback if sid in banned else sid;access=stage
                    if method=='water_mons':access='surf'
                    if method=='fishing_mons' and slot>=2 and stage=='native_early':access='flash'
                    if sid in mapping and (sid not in found or rank[access]<rank[found[sid]]):
                        found[sid]=access;evidence[sid]={'map':entry['map'],'method':method,'slot':slot,'species':sid,'access':access}
    # A conservative subset of the real weighted extra pool: no past, urban,
    # position restriction or extra rare roll. Native 80% base encounters remain.
    groups=json.loads((source/'data/maps/map_groups.json').read_text())
    order={(i,j):name for i,key in enumerate(groups['group_order']) for j,name in enumerate(groups[key])}
    ids={mp['name']:mid for mid,mp in maps.items()}
    table=(source/'src/data/yokai_bestiary_encounters.h').read_text()
    for raw in re.findall(r'^\s*\{([0-9,]+)\},',table,re.M):
        values=list(map(int,raw.split(',')))
        if len(values)!=13:continue
        sid,group,number,area,low,high,weight,past,x1,y1,x2,y2,chance=values
        name=order.get((group,number));mid=ids.get(name);stage=access_for_map(name) if name else None
        method={0:'land_mons',1:'water_mons',4:'fishing_mons'}.get(area)
        if not stage or not weight or past or chance>1 or (x1,y1,x2,y2)!=(0,0,255,255) or method not in methods.get(mid,set()):continue
        sid=fallback if sid in banned else sid
        if area==1:stage='surf'
        if sid in mapping and (sid not in found or rank[stage]<rank[found[sid]]):
            found[sid]=stage;evidence[sid]={'map':mid,'method':method,'species':sid,'access':stage,'native_extra_pool':True}
    evolutions=[]
    for line in (source/'src/data/pokemon/evolution.h').read_text().splitlines():
        m=re.match(r'\s*\[(\d+)\]',line)
        if m:
            for mode,level,target in re.findall(r'\{(EVO_LEVEL|EVO_FRIENDSHIP), (\d+), (\d+)\}',line):
                if int(target) in mapping:evolutions.append((int(m[1]),int(target),mode,int(level)))
    for _ in range(10):
        changed=False
        for parent,target,mode,level in evolutions:
            if parent not in found:continue
            stage=found[parent]
            if rank[stage]<1:stage='flash' # no assumptions about early grinding / friendship
            if mode=='EVO_LEVEL' and level>30:
                if level>50:continue
                stage='surf'
            if target not in found or rank[stage]<rank[found[target]]:
                found[target]=stage;evidence[target]={'from':parent,'species':target,'evolution':mode,'level':level,'access':stage};changed=True
        if not changed:break
    return {mapping[sid]:{'species':sid,'access':stage,'witness':evidence[sid]} for sid,stage in found.items() if sid in mapping},mapping

def scan_source(source):
    blocks={};sources={}
    for path in sorted((source/'data').rglob('*.inc')):
        label=None;body=[];line_no=0
        def save():
            if label:blocks[label]='\n'.join(body);sources[label]=f'{path.relative_to(source)}:{line_no}'
        for n,line in enumerate(path.read_text(errors='replace').splitlines(),1):
            m=re.match(r'^(\w+)::?\s*(?:@.*)?$',line)
            if m:save();label=m[1];body=[];line_no=n
            elif label:body.append(line)
        save()
    maps={}
    for path in sorted((source/'data/maps').glob('*/map.json')):
        data=json.loads(path.read_text());maps[data['id']]=data
    return blocks,sources,maps

def expand(data,source,project):
    reference=json.loads((project/'DOCUMENTATION/FRLG_COMPARAISON.json').read_text())
    blocks,locations,maps=scan_source(source);byname={m['name']:m for m in maps.values()}
    flags=constants(source/'include/constants/flags.h');opponents=constants(source/'include/constants/opponents.h')
    itemids=constants(source/'include/constants/items.h')
    records={r['itemId']:r for r in json.loads((source/'src/data/items.json').read_text())['items']}
    refs={r['upstream_key']:r for r in reference['rows']};byflag={r['native_flag']:r for r in reference['rows'] if r['native_flag']}
    renewable=(source/'src/renewable_hidden_items.c').read_text()
    existing={c['id'] for c in data['checks'] if c['status']=='active'}
    # Ordinary reward sources are taken from actual object/bg events, not map names alone.
    for c in data['checks']:
        if c['status']=='active' or c['kind'] not in ('ball','hidden'):continue
        stage=access_for_map(c['map']);ref=byflag.get(c['flag']);record=records.get(c['original_item'],{})
        if not stage or not ref or c['quantity']!=1 or c.get('underfoot') or c['flag'] in renewable:continue
        if record.get('pocket') not in ('POCKET_ITEMS','POCKET_POKE_BALLS','POCKET_TM_CASE','POCKET_BERRIES'):continue
        if c['original_item'].startswith('ITEM_HM'):continue
        c.update(status='active',access=stage,original_reward='replaced',category=ref['category'],
            upstream_key=ref['upstream_key'],upstream_region=ref['upstream_region'],upstream_ap_id=ref['upstream_ap_id'],
            prerequisites=['Native campaign',stage],risks=[])
        c['name_fr']=f"{c['map']} — {'objet caché' if c['kind']=='hidden' else 'objet'} ({c['x']},{c['y']})"

    # Only trainer commands reachable from object/coordinate scripts on actual maps.
    seen_trainers=defaultdict(list);owners=defaultdict(list)
    for mid,mp in maps.items():
        stage=access_for_map(mp['name'])
        if not stage:continue
        # Conditional/hidden actors and coordinate-only story battles need their
        # own spawn proof. Standard trainers/NPCs with flag0 are present actors.
        roots={e['script'] for e in mp.get('object_events',[]) if e.get('script') and str(e.get('flag','0'))=='0'}
        for root in sorted(roots):
            todo=[root];seen=set()
            while todo:
                label=todo.pop()
                if label in seen or 'rematch' in label.lower() or label not in blocks:continue
                seen.add(label);body=blocks[label]
                if re.search(r'goto_if_unset FLAG_SYS_GAME_CLEAR, (?:EventScript_Return|EventScript_ReleaseEnd)',body):continue
                owners[label].append({'map':mp['name'],'access':stage,'root':root,'label':label,'source':locations[label]})
                for token in re.findall(r'\btrainerbattle_(?:single|no_intro|double)\s+(TRAINER_\w+)',body):
                    if 'REMATCH' not in token:seen_trainers[token].append({'map':mp['name'],'access':stage,'root':root,'label':label,'source':locations[label]})
                for line in body.splitlines():
                    if re.match(r'\s*(?:goto|call)',line):
                        target=re.findall(r'\b\w+\b',line.split('@')[0])[-1:]
                        if target and target[0] in blocks:todo.append(target[0])

    trainer_rows=[];trainer_groups=set()
    for row in reference['rows']:
        key=row['upstream_key']
        if row['category']!='TRAINER':continue
        token=key.removesuffix('_REWARD');matches=seen_trainers.get(token,[])
        aliases=[token]
        if any(x in token for x in ('BULBASAUR','SQUIRTLE','CHARMANDER')):
            base=re.sub('BULBASAUR|SQUIRTLE|CHARMANDER','{}',token)
            aliases=[base.format(x) for x in ('BULBASAUR','SQUIRTLE','CHARMANDER')]
            matches=[m for a in aliases for m in seen_trainers.get(a,[])]
        if not matches or not all(a in opponents for a in aliases):continue
        group=tuple(sorted(opponents[a] for a in aliases))
        if group in trainer_groups:continue
        if len(trainer_rows)>=256:continue # 32 bytes already reserved in the unchanged64-byte AP save
        trainer_groups.add(group)
        match=min(matches,key=lambda m:('native_early','flash','surf').index(m['access']))
        stage='surf' if any(s in token for s in ('LATE','CHAMPION','ELITE','LORELEI','AGATHA','BRUNO','LANCE')) else match['access']
        trainer_rows.append({'id':0x594B6000+row['upstream_ap_id'],'name_fr':'Dresseur — '+row['name_original'],
            'kind':'trainer','category':'TRAINER','status':'active','access':stage,'map':match['map'],
            'trainer_ids':[opponents[a] for a in aliases],'persistent_index':len(trainer_rows),
            'flag_values':[flags['TRAINER_FLAGS_START']+opponents[a] for a in aliases],
            'source':match['source'],'script_source':match['source'],'script':match['root'],
            'upstream_key':key,'upstream_ap_id':row['upstream_ap_id'],'upstream_region':row['upstream_region'],
            'original_reward':'native_battle_money_preserved_separate_AP_check','validation':'Won trainer battle callback, separate persistent AP victory bit; native flags are not proof',
            'mandatory':False,'prerequisites':['Native campaign',stage],'risks':[]})
    data['checks']+=trainer_rows

    # One-shot gifts: require both a real rooted NPC script and an actual
    # one-time flag test. Never infer a gift just from FLAG_GOT_* existing.
    active_flags={c.get('flag') for c in data['checks'] if c['status']=='active'}
    for row in reference['rows']:
        flag=row.get('native_flag')
        if row['category']!='NPC_GIFT' or not flag or flag in active_flags or flag not in flags:continue
        for label,body in blocks.items():
            if not owners.get(label) or not re.search(r'\bsetflag\s+'+flag+r'\b',body):continue
            gifts=re.findall(r'^\s*(giveitem(?:_msg)?\s+[^\n]+)',body,re.M)
            if len(gifts)!=1:continue
            match=re.search(r'\bITEM_\w+',gifts[0])
            if not match:continue
            item=match[0];record=records.get(item,{})
            parts=gifts[0].split(',');quantity_index=2 if gifts[0].lstrip().startswith('giveitem_msg') else 1
            if len(parts)>quantity_index and parts[quantity_index].strip()!='1':continue
            if record.get('pocket') not in ('POCKET_ITEMS','POCKET_POKE_BALLS','POCKET_TM_CASE','POCKET_BERRIES') or item.startswith('ITEM_HM'):continue
            candidates=[m for m in owners[label] if re.search(r'goto_if_set\s+'+flag+r'\b',blocks.get(m['root'],'')) or re.search(r'goto_if_set\s+'+flag+r'\b',body)]
            if not candidates:continue
            m=min(candidates,key=lambda m:('native_early','flash','surf').index(m['access']))
            data['checks'].append({'id':0x594B2000+flags[flag],'name_fr':'Cadeau — '+row['name_original'],
                'kind':'npc_gift','status':'active','category':'NPC_GIFT','access':m['access'],'map':m['map'],
                'flag':flag,'flag_value':flags[flag],'original_item':item,'quantity':1,
                'source':locations[label].split(':')[0],'script_source':locations[label],'script':m['root'],
                'gift_label':label,'gift_macro':gifts[0].strip(),'upstream_key':row['upstream_key'],'upstream_region':row['upstream_region'],
                'original_reward':'replaced','validation':'Native one-time gift flag after successful rooted script',
                'mandatory':False,'prerequisites':['Native gift requirements',m['access']],'risks':[]})
            active_flags.add(flag);break

    # Classical field gifts with positively traced fangame sources. Cut moved
    # from the ship to Ariane's Philosovni conclusion; receiving it is not quest completion.
    for flag,item,mp,path,label,macro,stage in [
        ('FLAG_GOT_HM01','ITEM_HM01','VermilionCity','data/scripts/philosovni.inc','Philosovni_Reward','giveitem ITEM_HM01, 1','native_early'),
        ('FLAG_GOT_HM02','ITEM_HM02','Route16_House','data/maps/Route16_House/scripts.inc','Route16_House_EventScript_Woman','giveitem_msg Route16_House_Text_ReceivedHM02FromGirl, ITEM_HM02','flash'),
        ('FLAG_GOT_HM04','ITEM_HM04','FuchsiaCity_WardensHouse','data/maps/FuchsiaCity_WardensHouse/scripts.inc','FuchsiaCity_WardensHouse_EventScript_GiveGoldTeeth','giveitem_msg FuchsiaCity_WardensHouse_Text_ReceivedHM04FromWarden, ITEM_HM04','flash')]:
        body=(source/path).read_text()
        assert macro in body and 'setflag '+flag in body
        row=byflag[flag]
        data['checks'].append({'id':0x594B2000+flags[flag],'name_fr':{'ITEM_HM01':'Ariane — récompense Coupe','ITEM_HM02':'Refuge Route16 — récompense Vol','ITEM_HM04':'Gardien Safari — récompense Force'}[item],
            'kind':'npc_gift','status':'active','category':'NPC_GIFT','access':stage,'map':mp,
            'flag':flag,'flag_value':flags[flag],'original_item':item,'quantity':1,
            'source':path,'script_source':path,'script':label,'gift_label':label,'gift_macro':macro,
            'upstream_key':row['upstream_key'],'upstream_region':row['upstream_region'],'original_reward':'replaced',
            'validation':'Native gift completion flag, never remote item receipt','mandatory':False,
            'prerequisites':['Native quest or Gold Teeth retained; received HM does not complete source',stage],'risks':[]})

    # Pure visit markers are native persistent map-preview flags.
    for row in reference['rows']:
        if row['category']!='TOWN_VISIT':continue
        mp=maps.get(row['upstream_map'])
        if not mp:continue
        stage=access_for_map(mp['name']);path=source/f"data/maps/{mp['name']}/scripts.inc"
        if not stage or not path.exists():continue
        match=re.search(r'\bsetworldmapflag\s+(FLAG_WORLD_MAP_\w+)',path.read_text())
        if not match or match[1] not in flags:continue
        flag=match[1]
        data['checks'].append({'id':0x594BA000+flags[flag],'name_fr':'Visite — '+row['name_original'],
            'kind':'visit','category':'TOWN_VISIT','status':'active','access':stage,'map':mp['name'],
            'flag':flag,'flag_value':flags[flag],'source':f'data/maps/{mp["name"]}/scripts.inc',
            'upstream_key':row['upstream_key'],'upstream_region':row['upstream_region'],
            'original_reward':'native_fly_access_preserved_separate_AP_check','mandatory':False,
            'validation':'MapPreview_SetFlag during actual transition','prerequisites':['Visit map',stage],'risks':[]})

    # Extend the already audited encounter/level-evolution model to captured checks.
    # Do not add species only obtainable from postgame, random gifts, trades or stones.
    obtainable,mapping=obtainable_dex(source,maps)
    # Aides use the same actual pre-HOF acquisition witnesses, not raw vanilla slots.
    cap=data['capture_capacity']
    for label,max_rank in [('pre_flash',0),('pre_surf',1),('post_surf',2)]:
        nums=sorted(n for n,p in obtainable.items() if n<=151 and ('native_early','flash','surf').index(p['access'])<=max_rank)
        cap[label+'_species']=nums
        cap['pre_surf_count_with_level30_evolutions' if label=='pre_surf' else label+'_count']=len(nums)
    species_ids=constants(source/'include/constants/species.h')
    names={species_ids.get(token):name for token,name in re.findall(
        r'\[(SPECIES_\w+)\]\s*=\s*_\("([^"]+)"\)',(source/'src/data/text/species_names.h').read_text())}
    for number,proof in sorted(obtainable.items()):
        stage=proof['access']
        key=f'POKEDEX_REWARD_{number:03d}';row=refs.get(key)
        if not row:continue
        data['checks'].append({'id':0x594B8000+number,'name_fr':f'Médallium — {names.get(proof["species"],str(proof["species"]))} ({number:03d})',
            'kind':'pokedex','category':'POKEDEX','status':'active','access':stage,'map':'Collection native',
            'dex_number':number,'species_id':proof['species'],'acquisition_witness':proof['witness'],'upstream_key':key,'upstream_ap_id':row['upstream_ap_id'],'upstream_region':row['upstream_region'],
            'source':'src/pokedex.c:GetSetPokedexFlag','original_reward':'new_collection_AP_check',
            'mandatory':False,'validation':'GetSetPokedexFlag(number, FLAG_GET_CAUGHT), seen alone insufficient',
            'prerequisites':['Catch obtainable native species',stage],'risks':[]})

    active=[c for c in data['checks'] if c['status']=='active'];active_keys={c.get('upstream_key'):c for c in active}
    # Eight badge mappings are not item-source flags in the vanilla patched ROM.
    for i,c in enumerate(data['badge_checks'],1):active_keys[f'BADGE_{i}']=c
    correspondence=[]
    rematch_source=(source/'src/vs_seeker.c').read_text()
    fame_source='\n'.join(body for body in blocks.values() if 'famechecker' in body)
    for row in reference['rows']:
        key=row['upstream_key'];entry=active_keys.get(key)
        cls='compatible' if entry else 'a_adapter';reason='Integrated native event'
        adapted=bool(entry and (key in ('BADGE_4','NPC_GIFT_GOT_HM01') or entry.get('kind') in ('aide','trainer','pokedex')))
        if adapted:cls='a_adapter'
        if not entry:
            cat=row['category'];reason={'SHOP_ITEM':'Successful purchase needs a transaction hook; opening the shop is not a purchase.',
                'TRAINER_REMATCH':'Repeatable VS Seeker tier selection differs; no reliable independent first-tier ledger yet.',
                'FAME_ENTRY':'Native Fame Checker entry storage and retained characters need mapping.'}.get(cat,'No pre-League source/access proof or reward protected by story.')
            if row['status'] in ('disabled_postgame_or_sevii','absent_or_unresolved','disabled_replaced_reward'):
                cls='absent_ou_incompatible';reason=row['reason']
            if cat=='POKEDEX' and key not in active_keys:
                n=int(key.rsplit('_',1)[1]);cls='a_adapter' if n in mapping.values() else 'absent_ou_incompatible'
                reason='Native acquisition before victory not proved.' if cls=='a_adapter' else 'No active native species for this national entry.'
        evidence=[]
        if row['category']=='TRAINER' and key.removesuffix('_REWARD') in seen_trainers and not entry:
            reason='Rooted native battle exists; current64-byte save has room for256 persistent trainer checks, already allocated.'
            evidence=seen_trainers[key.removesuffix('_REWARD')]
        if row['category']=='TRAINER_REMATCH':
            token=key.removesuffix('_REWARD')
            if token in rematch_source:evidence=[{'source':'src/vs_seeker.c','token':token}]
        if row['category']=='FAME_ENTRY':
            character=key.removeprefix('FAME_CHECKER_').rsplit('_',1)[0]
            if 'FAMECHECKER_'+character in fame_source:evidence=[{'source':'Native famechecker commands','character':character}]
        if row['category']=='SHOP_ITEM' and row['upstream_map'] in maps:
            native_map=maps[row['upstream_map']]['name']
            evidence=[{'map':native_map,'source':m['source'],'command':label} for label,body in blocks.items() if 'pokemart' in body
                      for m in owners.get(label,[]) if m['map']==native_map]
        correspondence.append({**row,'classification':cls,'adaptation_complete':adapted,'integrated':bool(entry),'yokai_id':entry['id'] if entry else None,'bulk_reason':reason,'category_evidence':evidence})
    data['id_formula']='Preserved badge/flag IDs; trainer 0x594B6000+upstream AP ID; capture 0x594B8000+national dex; visit 0x594BA000+native flag'
    data['limits']=['Only positively matched pre-League sources are active; unknown sources remain disabled.',
        'Native campaign/story keys remain; AP access groups Flash/Surf capabilities rather than every narrative condition.',
        '256 separate persistent trainer victory groups exhaust the existing reserved32-byte ledger.',
        'No shops/rematches/Fame entries activated; no optional RNG check can contain progression.',
        'Native fixtures and representative played battles are distinct from a complete physical playthrough.']
    data['bulk_correspondence']={'total':len(correspondence),'summary':dict(Counter(r['classification'] for r in correspondence)),
        'by_category':{cat:dict(Counter(r['classification'] for r in correspondence if r['category']==cat)) for cat in sorted({r['category'] for r in correspondence})},'rows':correspondence}
    return data

def augment_catalog(source,data):
    return expand(data,source,Path(__file__).resolve().parents[2])
