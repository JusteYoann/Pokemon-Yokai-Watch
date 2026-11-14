"""Première randomisation : six objets et un don remplacés, huit badges bonus.

Surf est maintenant un objet de progression AP ; les autres clés restent natives. Le graphe représente
leur accessibilité finale, pas la durée des combats ni les étapes de Kanto.
"""
from dataclasses import dataclass
import json
import pkgutil
from BaseClasses import Item, ItemClassification, Location, Region
from Options import PerGameCommonOptions
from worlds.AutoWorld import World
from .client import YokaiFireRedClient

GAME='Pokemon Yo-kai FireRed'
LOCATION_BASE=0x594B1000
ITEMS={'Potion':13,'Super Potion':22,'Hyper Potion':21,'Poké Ball':4,'Super Ball':3,
       'Hyper Ball':2,'Repousse':86,'Super Repousse':85,'Max Repousse':84,
       'Antidote':14,'Anti-Para':18,'Réveil':17,'Anti-Brûle':15,'Antigel':16,'CS03 Surf':341}
# Internal badge bits are the original FireRed bits, not the itinerary order.
CHECKS=['Badge de Wyatt','Badge de Nathan/Katie','Badge d’Ariane','Badge d’Alizon Bie',
        'Badge de Bérénice','Badge de Domniscian','Badge de Nathaniel/Michael','Badge de Steve Jaws']
PICKUPS=[c for c in json.loads(pkgutil.get_data(__package__,'checks.json'))['checks'] if c['status']=='active']

class YokaiFireRedItem(Item):game=GAME
class YokaiFireRedLocation(Location):game=GAME

@dataclass
class YokaiFireRedOptions(PerGameCommonOptions):
    pass

class YokaiFireRedWorld(World):
    """Fangame RC1 : collectes remplacées, Surf progression AP, autres clefs natives."""
    game=GAME
    options_dataclass=YokaiFireRedOptions
    topology_present=False
    ut_can_gen_without_yaml=True
    item_name_to_id=ITEMS
    location_name_to_id={**{name:LOCATION_BASE+i for i,name in enumerate(CHECKS)},
                         **{c['name_fr']:c['id'] for c in PICKUPS}}

    def create_item(self,name):
        if name=='Victoire':return YokaiFireRedItem(name,ItemClassification.progression,None,self.player)
        classification=ItemClassification.progression if name=='CS03 Surf' else ItemClassification.filler
        return YokaiFireRedItem(name,classification,ITEMS[name],self.player)

    def create_regions(self):
        menu=Region('Menu',self.player,self.multiworld);kanto=Region('Kanto — campagne native',self.player,self.multiworld)
        sea=Region('Kanto — accès maritime',self.player,self.multiworld)
        self.multiworld.regions += [menu,kanto,sea];menu.connect(kanto)
        kanto.connect(sea,rule=lambda state:state.has('CS03 Surf',self.player))
        for name,code in self.location_name_to_id.items():
            region=sea if name in CHECKS[6:] else kanto
            region.locations.append(YokaiFireRedLocation(self.player,name,code,region))
        goal=YokaiFireRedLocation(self.player,'Panthéon',None,sea)
        goal.place_locked_item(self.create_item('Victoire'));sea.locations.append(goal)
        # Surf gates the maritime finale. Other native keys remain at their
        # original sources, so the pre-Surf campaign has no other AP item gate.
        self.multiworld.completion_condition[self.player]=lambda state:state.has('Victoire',self.player)

    def create_items(self):
        pool=['Potion','Potion','Super Potion','Super Potion','Hyper Potion','Super Ball','Hyper Ball','Repousse']
        pool += ['Poké Ball','Antidote','Potion','Potion','Potion','Antidote','CS03 Surf']
        self.multiworld.itempool += [self.create_item(name) for name in pool]

    def get_filler_item_name(self):return 'Potion'

    def fill_slot_data(self):
        return {'protocol':1,'mode':'surf_randomized','goal':'hall_of_fame_record',
                'location_base':LOCATION_BASE,'pickup_ids':[c['id'] for c in PICKUPS],
                'replaced_rewards':[c['flag'] for c in PICKUPS],
                'badges_native':True,'progression_randomized':['CS03 Surf']}
