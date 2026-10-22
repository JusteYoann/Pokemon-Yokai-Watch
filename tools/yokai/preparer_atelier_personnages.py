#!/usr/bin/env python3
"""Inventory and contact sheets only: never writes game graphics or engine data."""
import csv
import hashlib
import json
import re
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'docs/atelier-personnages'
CUSTOM = ROOT / 'graphics/yokai_characters'

# Production roster, not a claim that these roles are already implemented.
CAST = [
    ('nathan', 'Nathan', 'Protagoniste et champion alternatif', 'joueur'),
    ('katie', 'Katie', 'Protagoniste et championne alternative', 'joueur'),
    ('matt', 'Matt', 'Rival, trois apparitions de combat', 'rival'),
    ('ariane', 'Ariane', 'Championne', 'pnj'),
    ('wyatt', 'Wyatt', 'Champion', 'pnj'),
    ('inspecteur_giraud', 'Inspecteur Giraud', 'Demandé dans la mission de production ; affectation de Champion à clarifier sans changer les arènes', 'pnj'),
    ('nathaniel', 'Nathaniel', 'Ancêtre, version jeune du chapitre du passé', 'pnj'),
    ('michael', 'Michael', 'Ancêtre, version jeune du chapitre du passé', 'pnj'),
    ('enma', 'Seigneur Enma', 'Personnage narratif, distinct de la créature capturable', 'pnj'),
    ('enma_civil', 'Enma — tenue civile', 'Apparition déguisée à Argenta', 'carte'),
    ('domniscian', 'Domniscian', 'Boss et caméo existant', 'pnj'),
    ('don_morleone', 'Don Morleone', 'Antagoniste et champion', 'pnj'),
    ('mafiamille_1', 'Mafiamille 1', 'Carte commune, combat distinct', 'pnj'),
    ('mafiamille_2', 'Mafiamille 2', 'Carte commune, combat distinct', 'pnj'),
    ('mafiamille_3', 'Mafiamille 3', 'Carte commune, combat distinct', 'pnj'),
    ('employe_rouge', 'Employé rouge', 'Même silhouette de carte que le bleu, palette distincte', 'pnj'),
    ('employe_bleu', 'Employé bleu', 'Même silhouette de carte que le rouge, palette distincte', 'pnj'),
    ('dr_jobard', 'Dr Jobard', 'En pause : ne pas poursuivre son redesign maintenant', 'pause'),
    ('berenice', 'Bérénice', 'Scientifique et casting demandé dans la nouvelle mission ; affectation d’arène à clarifier sans modifier le scénario', 'pnj'),
    ('steve_jaws', 'Steve Jaws', 'Introduction, champion et Yopple', 'pnj'),
    ('mark_orckerberg', 'Mark Orckerberg', 'Allié de Yopple', 'carte'),
    ('whisper_majordome', 'Whisper — majordome', 'Champion de Parmanie', 'pnj'),
    ('alyzon', 'Alyzon', 'Championne, Zombie Night', 'pnj'),
    ('zazel', 'Zazel', 'Gardien du Temple ; combat supplémentaire non présumé', 'carte'),
    ('laure', 'Laure', 'Temple ; composition du combat duo à préciser dans les sources', 'pnj'),
    ('marge', 'Marge', 'Temple ; composition du combat duo à préciser dans les sources', 'pnj'),
    ('lady_perpetua', 'Lady Perpetua', 'Adversaire du Temple', 'pnj'),
    ('mckraken', 'McKraken', 'Adversaire du Temple, morphologie particulière', 'pnj'),
    ('agent_x', 'Agent X', 'Dernier adversaire du Temple', 'pnj'),
    ('soranaki', 'Soranaki', 'Climax ; formes et boss spécial à définir sans inventer', 'special'),
    ('yopple_bot', 'Yopple Bot', 'Mini-boss ; format de combat à confirmer', 'special'),
    ('juste_yoann', 'Juste Yoann', 'Quête créateur ; retrouver la référence déjà envoyée avant dessin', 'pnj'),
    ('coach_antonic', 'Coach Antonic', 'Quête entraînement et trois accompagnateurs', 'pnj'),
    ('scientifique_quete', 'Scientifique récurrent', 'Même identité aux quatre apparitions ; ne pas confondre avec Jobard', 'pnj'),
    ('fan_jibanyan', 'Fan de Jibanyan', 'PNJ de quête ; ressource générique possible', 'carte'),
    ('grand_pere_quete', 'Grand-père disparu', 'PNJ de quête ; ressource générique possible', 'carte'),
    ('specialiste_shiny', 'Spécialiste des chromatiques', 'PNJ de quête ; ressource générique possible', 'carte'),
    ('red', 'Red', 'Personnage distinct de Nathan ; conserver ressources originales', 'original'),
    ('jibanyan_scene', 'Jibanyan — acteur de scène', 'Accompagnateur du Coach ; réutilisation possible du Jibanyan de Léo', 'creature'),
    ('komasan_scene', 'Komasan — acteur de scène', 'Accompagnateur du Coach', 'creature'),
    ('whisper_scene', 'Whisper — acteur de scène', 'Accompagnateur du Coach, distinct de la tenue majordome', 'creature'),
    ('triptic_tac_scene', 'Triptic-tac — acteur de scène', 'Voyage dans le passé', 'creature'),
    ('hovernyan_scene', 'Hovernyan — acteur de scène', 'Demandé dans la mission de production ; apparition à relever dans les scripts', 'creature'),
    ('usapyon_scene', 'Usapyon — ressource de personnage', 'Demandé dans la mission ; ne pas réintroduire automatiquement le décor retiré', 'creature'),
    ('oni_scene', 'Oni — acteurs de Terr’heure', 'Espèces, variantes et animations de poursuite à relever avant production', 'creature'),
    ('misterre_scene', 'Misterre — rencontre statique', 'Morphologie de créature, hors gabarit humain', 'creature'),
    ('mademoaiselle_scene', 'Mademoaiselle — rencontre statique', 'Îles Écume ; morphologie de créature', 'creature'),
    ('octorgone_scene', 'Octorgone — rencontre statique', 'Centrale ; morphologie de créature', 'creature'),
    ('kyubi_scene', 'Kyubi — rencontre statique', 'Mont Braise ; morphologie de créature', 'creature'),
    ('enma_creature', 'Enma — créature capturable', 'Distinct du Seigneur Enma narratif', 'creature'),
    ('enma_ancien', 'Enma l’Ancien', 'Sanctuaire Divin ; ne pas inventer une forme non spécifiée', 'special'),
]


def write_csv(path, rows, fields):
    with path.open('w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)


def checker(size):
    im = Image.new('RGB', size)
    d = ImageDraw.Draw(im)
    for y in range(0, size[1], 8):
        for x in range(0, size[0], 8):
            c = 202 if (x//8+y//8) % 2 else 226
            d.rectangle((x, y, x+7, y+7), fill=(c, c, c))
    return im


def preview_rgba(path):
    with Image.open(path) as src:
        im = src.convert('RGBA')
        # Some native assets rely on palette entry zero without PNG tRNS.
        # This is a preview interpretation only; the source is never rewritten.
        if src.mode == 'P' and 'transparency' not in src.info:
            im.putalpha(Image.frombytes('L', src.size, bytes(0 if k == 0 else 255 for k in src.tobytes())))
        return im


def sheet(paths, target, title):
    width = 1120
    y = 40
    blocks = []
    for path in paths:
        im = preview_rgba(path)
        scale = min(4, max(1, (width-40)//im.width))
        im = im.resize((im.width*scale, im.height*scale), Image.Resampling.NEAREST)
        blocks.append((path, im, scale, y))
        y += im.height+46
    out = checker((width, max(100, y)))
    d = ImageDraw.Draw(out)
    d.text((12, 10), title+' — fichiers existants, pas validation artistique', fill='black')
    for path, im, scale, y in blocks:
        d.text((12, y), f'{path.relative_to(ROOT)} | x{scale}', fill='black')
        out.paste(im, (12, y+20), im)
    out.save(target)


def main():
    OUT.mkdir(exist_ok=True, parents=True)
    (OUT/'planches').mkdir(exist_ok=True)
    files = subprocess.check_output(['git', 'ls-files', 'src', 'data'], cwd=ROOT, text=True).splitlines()
    refs = {}
    for name in files:
        path = ROOT/name
        if path.suffix not in ('.c', '.h', '.inc', '.s', '.json'):
            continue
        for match in re.finditer(r'INCBIN_\w+\("(graphics/[^"\n]+)"\)', path.read_text(errors='replace')):
            source = re.sub(r'\.(?:4bpp|8bpp)(?:\.lz)?$', '.png', match[1])
            if source.endswith('.png'):
                refs.setdefault(source, []).append(name)
    candidates = set()
    for folder in [ROOT/'graphics/object_events/pics/people', ROOT/'graphics/trainers/front_pics', ROOT/'graphics/trainers/back_pics']:
        candidates.update(folder.glob('*.png'))
    for folder in CUSTOM.iterdir():
        if folder.is_dir() and folder.name not in ('overworld_red_v3', 'overworld_frlg_v2'):
            candidates.update(p for p in folder.glob('*.png') if 'preview' not in p.stem)
    # Includes creature actors associated with scenes; keep separate from human scale.
    candidates.update((CUSTOM/'static_yokai').glob('*/overworld.png'))
    rows = []
    for path in sorted(candidates):
        rel = str(path.relative_to(ROOT))
        with Image.open(path) as im:
            im.load()
            rows.append(dict(path=rel, width=im.width, height=im.height, mode=im.mode,
                             used_colors=len(set(im.getdata())), png_transparency=str(im.info.get('transparency', 'absente')),
                             sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                             source_references=';'.join(sorted(set(refs.get(rel, [])))),
                             state='reference_source_a_verifier_en_jeu' if refs.get(rel) else 'fichier_present_activation_non_prouvee'))
    write_csv(OUT/'RESSOURCES_EXISTANTES.csv', rows, list(rows[0]))
    cast = []
    gallery = ['# Galerie de travail des personnages', '',
               'Planches des fichiers existants, sans retouche ni activation dans le jeu. Chaque planche conserve toutes les cases des fichiers. Ce ne sont pas des captures mGBA et leur présence ne vaut pas validation artistique.', '']
    player_assets = ['normal.png', 'surf_run.png', 'bike.png', 'vs_seeker_bike.png', 'fish.png', 'item.png', 'front.png', 'back.png', 'intro.png', 'credits.png', 'region_icon.png']
    for key, name, role, kind in CAST:
        folder = CUSTOM/key
        aliases = {'jibanyan_scene': 'leo_jibanyan', 'misterre_scene': 'static_yokai/misterre',
                   'mademoaiselle_scene': 'static_yokai/mademoaiselle', 'octorgone_scene': 'static_yokai/octorgone'}
        if key in aliases:
            folder = CUSTOM/aliases[key]
        assets = sorted(p for p in folder.glob('*.png') if 'preview' not in p.stem) if folder.exists() else []
        if key == 'kyubi_scene':
            assets = [CUSTOM/'enma/kyubi_overworld.png']
        if key == 'red':
            assets = [ROOT/'graphics/object_events/pics/people/red_normal.png', ROOT/'graphics/trainers/back_pics/red_back_pic.png']
        required = player_assets if kind == 'joueur' else (['overworld.png', 'battle_early.png', 'battle_late.png', 'battle_champion.png', 'intro.png', 'credits.png'] if kind == 'rival' else ['overworld.png', 'battle.png'] if kind == 'pnj' else ['overworld.png'])
        missing = [a for a in required if not (folder/a).exists()] if kind != 'original' else []
        state = 'en_pause' if kind == 'pause' else 'original_a_preserver' if kind == 'original' else 'existant_a_revoir' if assets else 'a_preparer_ou_reutiliser'
        cast.append(dict(id=key, nom=name, role=role, profil=kind, etat=state, ressources_attendues=';'.join(required), fichiers_a_retrouver_ou_creer=';'.join(missing), fichiers_presents=';'.join(str(p.relative_to(ROOT)) for p in assets)))
        gallery.extend([f'## {name}', '', f'{role}. État : `{state}`.', ''])
        if assets:
            sheet(assets, OUT/'planches'/f'{key}.png', name)
            gallery.extend([f'![{name}](planches/{key}.png)', ''])
        else:
            gallery.extend(['Pas de dossier graphique dédié retrouvé sous cet identifiant. Vérifier les alias, références et possibilités de réutilisation avant de conclure à une ressource manquante.', ''])
    write_csv(OUT/'PERSONNAGES_ET_BESOINS.csv', cast, list(cast[0]))
    (OUT/'GALERIE.md').write_text('\n'.join(gallery), encoding='utf-8')
    # Technical silhouettes extracted from the selected scale reference.
    # These guides are not new character drawings and are never linked by the game.
    (OUT/'gabarits').mkdir(exist_ok=True)
    nathan = preview_rgba(CUSTOM/'nathan/normal.png')
    template = Image.new('RGBA', (64, 32))
    overview = checker((960, 70+len([c for c in cast if c['fichiers_presents']])*100))
    draw = ImageDraw.Draw(overview)
    draw.text((12, 10), 'Carte : existants x4, pas des nouveaux dessins ni des captures mGBA', fill='black')
    for i in range(4):
        j = min(i, 2)
        frame = nathan.crop((j*16, 0, (j+1)*16, 32))
        if i == 3:
            frame = frame.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        alpha = frame.getchannel('A')
        mask = Image.new('RGBA', frame.size, (88, 88, 88, 255))
        mask.putalpha(alpha)
        template.paste(mask, (i*16, 0))
    template.save(OUT/'gabarits/humanoide-nathan-4-directions.png')
    enlarged = checker((512, 256))
    enlarged.paste(template.resize((512, 256), Image.Resampling.NEAREST), (0, 0), template.resize((512, 256), Image.Resampling.NEAREST))
    enlarged.save(OUT/'gabarits/humanoide-nathan-4-directions-x8.png')
    row_number = 0
    for c in cast:
        if c['profil'] in ('creature', 'special'):
            continue
        paths = [ROOT/p for p in c['fichiers_presents'].split(';') if p]
        path = next((p for p in paths if p.name in ('normal.png', 'overworld.png', 'red_normal.png')), None)
        if path is None:
            continue
        im = preview_rgba(path)
        draw.text((12, 65+row_number*100), c['nom'], fill='black')
        for i in range(3):
            frame = im.crop((16*i, 0, 16*(i+1), 32)).resize((64, 128), Image.Resampling.NEAREST)
            overview.paste(frame, (280+i*200, 25+row_number*100), frame)
        row_number += 1
    # Enough height for the final row including its transparent padding.
    overview.crop((0, 0, 960, 25+max(0, row_number-1)*100+148)).save(OUT/'APERÇU_PERSONNAGES_EXISTANTS.png')
    summary = dict(resource_baseline='ca9855b2d75ccdfee7d531ed8a3bc3391de1e48e',
                   files_inventoried=len(rows), cast_entries=len(cast),
                   cast_with_existing_art=sum(bool(c['fichiers_presents']) for c in cast),
                   referenced_in_source=sum(bool(r['source_references']) for r in rows),
                   all_png_decoded=True, gameplay_or_active_art_modified=False,
                   limits=['INCBIN reference is not proof of live event use', 'Missing dedicated folder does not establish lost art', 'No animation playback or emulator validation in this inventory', 'Cast is consolidated from current specifications; generic NPC resources are catalogued separately'])
    (OUT/'INVENTAIRE.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == '__main__':
    main()
