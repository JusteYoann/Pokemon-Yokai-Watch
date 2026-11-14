"""Premier modèle YW1 EUR : génération expérimentale bloquée par défaut.

La logique ci-dessous est une proposition de rangs, pas une carte vérifiée des
flags de la ROM. Le patch ARM et le profil d'adresses EUR ne sont pas encore
implémentés. Le mode expérimental sert aux tests du graphe et du protocole.
"""
from dataclasses import dataclass
from BaseClasses import Item,ItemClassification,Location,Region
from Options import Toggle,PerGameCommonOptions,OptionError
from worlds.AutoWorld import World

GAME='Yo-kai Watch 1'
BASE=0x594B0100
ITEMS={'Montre rang D':BASE+1,'Montre rang C':BASE+2,'Montre rang B':BASE+3,
       'Montre rang A':BASE+4,'Nourriture':BASE+5,'Soin':BASE+6}
CHECKS={'Montre obtenue':0x594B0000,'Amitié avec Jibanyan':0x594B0001,
        'Épreuve de rang D':0x594B0002,'Épreuve de rang C':0x594B0003,
        'Épreuve de rang B':0x594B0004,'Épreuve de rang A':0x594B0005,
        'Épreuve de rang S':0x594B0006,'Boss final vaincu':0x594B0007}

class ExperimentalLogic(Toggle):
    """Tests uniquement : le profil EUR et les règles du jeu réel ne sont pas encore validés."""
    display_name='Autoriser le modèle non vérifié (tests uniquement)'
    default=0

@dataclass
class YokaiWatch1Options(PerGameCommonOptions):
    experimental_logic:ExperimentalLogic

class YW1Item(Item):game=GAME
class YW1Location(Location):game=GAME

class YokaiWatch1World(World):
    """Yo-kai Watch 1 européen : modèle en développement, pas encore jouable avec AP."""
    game=GAME
    options_dataclass=YokaiWatch1Options
    topology_present=True
    item_name_to_id=ITEMS
    location_name_to_id=CHECKS

    def generate_early(self):
        if not self.options.experimental_logic:
            raise OptionError('Yo-kai Watch 1 : patch et profil EUR non validés. Ce modèle n’est pas une intégration jouable. '
                              'experimental_logic: true est réservé aux tests explicites.')

    def create_item(self,name):
        classification=ItemClassification.progression if name.startswith('Montre rang') or name=='Victoire' else ItemClassification.filler
        return YW1Item(name,classification,ITEMS.get(name),self.player)

    def create_regions(self):
        regions={name:Region(name,self.player,self.multiworld) for name in ['Menu','Rang E','Rang D','Rang C','Rang B','Rang A']}
        self.multiworld.regions+=list(regions.values());regions['Menu'].connect(regions['Rang E'])
        for previous,next_rank in [('E','D'),('D','C'),('C','B'),('B','A')]:
            regions['Rang '+previous].connect(regions['Rang '+next_rank],rule=lambda state,rank=next_rank:state.has('Montre rang '+rank,self.player))
        placement={'Montre obtenue':'E','Amitié avec Jibanyan':'E','Épreuve de rang D':'E',
                   'Épreuve de rang C':'D','Épreuve de rang B':'C','Épreuve de rang A':'B',
                   'Épreuve de rang S':'A','Boss final vaincu':'B'}
        for name,code in CHECKS.items():
            region=regions['Rang '+placement[name]];region.locations.append(YW1Location(self.player,name,code,region))
        # This is the graph proposal only. The native final boss event is not
        # mapped to an address, and its true rank requirements remain to verify.
        victory=YW1Location(self.player,'Victoire de scénario',None,regions['Rang B'])
        victory.place_locked_item(self.create_item('Victoire'));regions['Rang B'].locations.append(victory)
        self.multiworld.completion_condition[self.player]=lambda state:state.has('Victoire',self.player)

    def create_items(self):
        names=['Montre rang D','Montre rang C','Montre rang B','Montre rang A','Nourriture','Nourriture','Soin','Soin']
        self.multiworld.itempool += [self.create_item(name) for name in names]

    def get_filler_item_name(self):return 'Nourriture'

    def fill_slot_data(self):
        return {'prototype':True,'playable':False,'title_id':'0004000000167800','logic_verified_in_game':False,
                'events':CHECKS,'items':ITEMS,'native_addresses':None}
