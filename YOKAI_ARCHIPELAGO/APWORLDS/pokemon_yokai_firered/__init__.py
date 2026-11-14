"""Mode bonus natif : la campagne et ses récompenses originales sont préservées.

Ce premier mode fournit de vrais checks de badges et des dons AP consommables.
Il ne prétend pas randomiser les objets clés ou la progression interne de Kanto.
"""
from dataclasses import dataclass
from BaseClasses import Item, ItemClassification, Location, Region
from Options import PerGameCommonOptions
from worlds.AutoWorld import World
from .client import YokaiFireRedClient

GAME='Pokemon Yo-kai FireRed'
LOCATION_BASE=0x594B1000
ITEMS={'Potion':13,'Super Potion':22,'Hyper Potion':21,'Poké Ball':4,'Super Ball':3,
       'Hyper Ball':2,'Repousse':86,'Super Repousse':85,'Max Repousse':84,
       'Antidote':14,'Anti-Para':18,'Réveil':17,'Anti-Brûle':15,'Antigel':16}
# Internal badge bits are the original FireRed bits, not the itinerary order.
CHECKS=['Badge de Wyatt','Badge de Nathan/Katie','Badge d’Ariane','Badge d’Alizon Bie',
        'Badge de Bérénice','Badge de Domniscian','Badge de Nathaniel/Michael','Badge de Steve Jaws']

class YokaiFireRedItem(Item):game=GAME
class YokaiFireRedLocation(Location):game=GAME

@dataclass
class YokaiFireRedOptions(PerGameCommonOptions):
    pass

class YokaiFireRedWorld(World):
    """Fangame Yo-kai RC1, bonus AP sans remplacement des récompenses narratives."""
    game=GAME
    options_dataclass=YokaiFireRedOptions
    topology_present=False
    ut_can_gen_without_yaml=True
    item_name_to_id=ITEMS
    location_name_to_id={name:LOCATION_BASE+i for i,name in enumerate(CHECKS)}

    def create_item(self,name):
        if name=='Victoire':return YokaiFireRedItem(name,ItemClassification.progression,None,self.player)
        return YokaiFireRedItem(name,ItemClassification.useful,ITEMS[name],self.player)

    def create_regions(self):
        menu=Region('Menu',self.player,self.multiworld);kanto=Region('Kanto — campagne native',self.player,self.multiworld)
        self.multiworld.regions += [menu,kanto];menu.connect(kanto)
        for name,code in self.location_name_to_id.items():
            kanto.locations.append(YokaiFireRedLocation(self.player,name,code,kanto))
        goal=YokaiFireRedLocation(self.player,'Panthéon',None,kanto)
        goal.place_locked_item(self.create_item('Victoire'));kanto.locations.append(goal)
        # No AP item blocks the original campaign in bonus mode. All checks and
        # victory are eventually reachable by completing that native campaign.
        self.multiworld.completion_condition[self.player]=lambda state:state.has('Victoire',self.player)

    def create_items(self):
        pool=['Potion','Potion','Super Potion','Super Potion','Hyper Potion','Super Ball','Hyper Ball','Repousse']
        self.multiworld.itempool += [self.create_item(name) for name in pool]

    def get_filler_item_name(self):return 'Potion'

    def fill_slot_data(self):
        return {'protocol':1,'mode':'bonus','goal':'hall_of_fame','location_base':LOCATION_BASE,
                'preserves_original_rewards':True,'progression_randomized':False}
