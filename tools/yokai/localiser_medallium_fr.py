#!/usr/bin/env python3
"""French factual profiles from the active 151 species; no invented creature lore.
Only text fields change. Numeric size/weight/scaling data remain untouched.
"""
import csv,json,re
from localiser_fr import ROOT,replace
from cadrer_dialogues_fr import measure

def main():
    roster=json.loads((ROOT/'data/yokai/noms_affiches.json').read_text())
    stats=(ROOT/'src/data/pokemon/species_info.h').read_text()
    path=ROOT/'src/data/pokemon/pokedex_entries.h';entries=path.read_text()
    abilities={r['constant']:r['nom_fr'] for r in csv.DictReader((ROOT/'data/yokai/ability_names_fr.csv').open(),delimiter=';')}
    types=dict(NORMAL='Normal',FIGHTING='Combat',FLYING='Vol',POISON='Poison',GROUND='Sol',ROCK='Roche',BUG='Insecte',GHOST='Spectre',STEEL='Acier',FIRE='Feu',WATER='Eau',GRASS='Plante',ELECTRIC='Électrik',PSYCHIC='Psy',ICE='Glace',DRAGON='Dragon',DARK='Ténèbres')
    records=[];rows=[]
    for mon in roster:
        species=mon['species_constant'];dex=species.replace('SPECIES_','NATIONAL_DEX_')
        b=re.search(r'\['+species+r'\]\s*=\s*\{(.*?)\n    \}',stats,re.S)[1]
        ts=list(dict.fromkeys(re.findall(r'TYPE_(\w+)',re.search(r'\.types\s*=\s*\{(.*?)\}',b)[1])))
        ab=re.search(r'\.abilities\s*=\s*\{(ABILITY_\w+)',b)[1]
        # Highest non-HP combat stat, using the actual active stats. Ties stable.
        ranking=[(int(re.search(r'\.'+field+r'\s*=\s*(\d+)',b)[1]),name) for field,name in [('baseAttack','Attaque'),('baseDefense','Défense'),('baseSpAttack','Attaque Spéciale'),('baseSpDefense','Défense Spéciale'),('baseSpeed','Vitesse')]]
        atout=max(ranking,key=lambda v:v[0])[1]
        lines=['Type: '+' / '.join(types[t] for t in ts)+'.','Atout: '+atout+'.','Talent: '+abilities[ab]+'.']
        # Dex printer uses 1px letter spacing in addition to the native font.
        widths=[measure(line)+len(line) for line in lines];assert max(widths)<=224,(species,widths)
        pattern=re.compile(r'(\['+dex+r'\]\s*=\s*\{)(.*?)(\n    \})',re.S)
        m=pattern.search(entries);assert m,(species,dex)
        symbol=re.search(r'\.description\s*=\s*(\w+)',m[2])[1]
        updated=re.sub(r'(\.categoryName\s*=\s*_)\(".*?"\)',r'\1("Yo-kai ")',m[2])
        entries=entries[:m.start()]+m[1]+updated+m[3]+entries[m.end():]
        for header in ['pokedex_text_fr.h','pokedex_text_lg.h']:
            rel='src/data/pokemon/'+header;rows.append((rel,symbol,r'\n'.join(lines)));replace(ROOT/rel,symbol,r'\n'.join(lines))
        records.append(dict(number=mon['numero_yokai'],name=mon['nom_yokai'],species=species,symbol=symbol,types=[types[t] for t in ts],primary_ability=abilities[ab],strongest_non_hp_stat=atout,description=lines,width_pixels_with_spacing=widths))
    assert len(records)==151
    path.write_text(entries)
    # REVISION0 stops categories at a space; avoid duplicating its former suffix.
    replace(ROOT/'src/strings.c','gText_PokedexPokemon','')
    (ROOT/'data/localisation/fr/11_medallium.tsv').write_text('# Factual profiles from validated combat data; no fictional lore added.\n'+''.join('\t'.join(row)+'\n' for row in rows))
    (ROOT/'data/localisation/fr/medallium_fr.json').write_text(json.dumps(dict(source='Active species_info.h + canonical ability_names_fr.csv + noms_affiches.json. Category is generic Yo-kai; profile gives actual types, highest non-HP base stat and primary ability, not official Yo-kai Watch lore.',entries=records),ensure_ascii=False,indent=2)+'\n')
    print('French Medallium profiles:',len(records))
if __name__=='__main__':main()
