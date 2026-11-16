"""RC1 checks mapped from MIT FRLG metadata; native rules supersede vanilla."""
from dataclasses import dataclass
import json
import pkgutil
from BaseClasses import Item, ItemClassification, Location, LocationProgressType, Region
from Options import PerGameCommonOptions, Toggle
from worlds.AutoWorld import World
from .client import YokaiFireRedClient

GAME='Pokemon Yo-kai FireRed'
LOCATION_BASE=0x594B1000
DATA=json.loads(pkgutil.get_data(__package__,'checks.json'))
PICKUPS=[c for c in DATA['checks'] if c['status']=='active']
CHECKS=['Badge de Wyatt','Badge de Nathan/Katie','Badge d’Ariane','Badge d’Alizon Bie',
        'Badge de Bérénice','Badge de Domniscian','Badge de Nathaniel/Michael','Badge de Steve Jaws']
ITEMS={'Potion':13,'Super Potion':22,'Hyper Potion':21,'Poké Ball':4,'Super Ball':3,
       'Hyper Ball':2,'Repousse':86,'Super Repousse':85,'Max Repousse':84,
       'Antidote':14,'Anti-Para':18,'Réveil':17,'Anti-Brûle':15,'Antigel':16,'CS03 Surf':341,'CS05 Flash':343}
for c in PICKUPS:
    if 'native_item_id' not in c:continue
    code=c['native_item_id']
    if code in ITEMS.values():continue
    name=c['item_name']
    if name in ITEMS:name+=f' ({code})'
    ITEMS[name]=code
NAMES={code:name for name,code in ITEMS.items()}
PROGRESSION={'CS03 Surf','CS05 Flash'}
USEFUL={NAMES[c['native_item_id']] for c in PICKUPS if 'native_item_id' in c and
        (c['kind']=='aide' or c['original_item'].startswith(('ITEM_TM','ITEM_MOON_STONE')))}-PROGRESSION

class YokaiFireRedItem(Item):game=GAME
class YokaiFireRedLocation(Location):game=GAME
class RandomTerreur(Toggle):
    """Optional random first apparition; no progression item can ever be placed here."""
    display_name='Terr’heure aléatoire (récompense secondaire uniquement)'

@dataclass
class YokaiFireRedOptions(PerGameCommonOptions):
    random_terreur: RandomTerreur

class YokaiFireRedWorld(World):
    game=GAME
    options_dataclass=YokaiFireRedOptions
    topology_present=True
    ut_can_gen_without_yaml=True
    item_name_to_id=ITEMS
    location_name_to_id={**{name:LOCATION_BASE+i for i,name in enumerate(CHECKS)},
                         **{c['name_fr']:c['id'] for c in PICKUPS}}

    def enabled(self,c):return c['access']!='optional_random' or bool(self.options.random_terreur)
    def create_item(self,name):
        if name=='Victoire':return YokaiFireRedItem(name,ItemClassification.progression,None,self.player)
        classification=ItemClassification.progression if name in PROGRESSION else ItemClassification.useful if name in USEFUL else ItemClassification.filler
        return YokaiFireRedItem(name,classification,ITEMS[name],self.player)

    def access(self,kind):
        if kind=='surf':return lambda state:state.has_all(PROGRESSION,self.player)
        if kind=='flash':return lambda state:state.has('CS05 Flash',self.player)
        return lambda state:True

    def create_regions(self):
        menu=Region('Menu',self.player,self.multiworld);self.multiworld.regions.append(menu)
        regions={}
        def region(name,kind):
            key=(name,kind)
            if key not in regions:
                regions[key]=Region(name+' ['+kind+']',self.player,self.multiworld)
                self.multiworld.regions.append(regions[key]);menu.connect(regions[key],rule=self.access(kind))
            return regions[key]
        for i,name in enumerate(CHECKS):
            kind='surf' if i>=6 else 'flash' if i>=3 else 'native_early'
            r=region(DATA['badge_checks'][i]['map'],kind)
            r.locations.append(YokaiFireRedLocation(self.player,name,LOCATION_BASE+i,r))
        for c in PICKUPS:
            if not self.enabled(c):continue
            r=region(c.get('upstream_region') or c['map'],c['access'])
            loc=YokaiFireRedLocation(self.player,c['name_fr'],c['id'],r);r.locations.append(loc)
            if c.get('caught_required'):
                n=c['caught_required'];cap=DATA['capture_capacity']
                loc.access_rule=lambda state,n=n,cap=cap:cap['pre_surf_count_with_level30_evolutions' if state.has('CS05 Flash',self.player) else 'pre_flash_count']>=n
            if c['access']=='optional_random':
                loc.progress_type=LocationProgressType.EXCLUDED
                loc.item_rule=lambda item:not item.advancement and not (item.classification & ItemClassification.trap)
        r=region('Panthéon','surf');goal=YokaiFireRedLocation(self.player,'Panthéon',None,r)
        goal.place_locked_item(self.create_item('Victoire'));r.locations.append(goal)
        self.multiworld.completion_condition[self.player]=lambda state:state.has('Victoire',self.player)

    def create_items(self):
        pool=['Potion','Potion','Super Potion','Super Potion','Hyper Potion','Super Ball','Hyper Ball','Repousse']
        for c in PICKUPS:
            if self.enabled(c):pool.append(NAMES[c['native_item_id']] if 'native_item_id' in c else 'Potion')
        self.multiworld.itempool += [self.create_item(name) for name in pool]

    def get_filler_item_name(self):return 'Potion'
    def fill_slot_data(self):
        return {'protocol':2,'mode':'expanded_checks','goal':'hall_of_fame_record',
                'catalog_sha256':DATA['catalog_sha256'],'location_base':LOCATION_BASE,
                'check_ids':[c['id'] for c in PICKUPS],'pickup_ids':DATA['legacy_pickup_ids'],
                'replaced_rewards':[c['flag'] for c in PICKUPS if c.get('original_reward')=='replaced'],
                'badges_native':True,'progression_randomized':sorted(PROGRESSION)}
