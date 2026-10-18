#!/usr/bin/env python3
"""Contact sheet only: original Red, frozen previous art, current native art."""
import csv
import io
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

R = Path(__file__).resolve().parents[2]
Q = R / 'QA_RECETTE_FINALE/POST_B13/SESSION_2_GRAPHISMES/RED_STRICT_V3'
BASE = 'daff2e5b824c4e76dc89270820a0574ffc15f3ae'
actors = [
    ('nathaniel', 'Nathaniel', 'Cape repliée dans le gabarit ; tête et jambes compactes.'),
    ('wyatt', 'Wyatt', 'Chapeau erroné retiré ; cheveux roux et lunettes ; gabarit Red.'),
    ('don_morleone', 'Don Morleone', 'Costume, chapeau et cheveux conservés ; corps et jambes compacts.'),
    ('mafiamille_1', 'Mafiamille 1', 'Nouveau modèle commun aux trois agents.'),
    ('mafiamille_2', 'Mafiamille 2', 'Copie binaire du même sprite de carte ; portrait de combat conservé.'),
    ('mafiamille_3', 'Mafiamille 3', 'Copie binaire du même sprite de carte ; portrait de combat conservé.'),
    ('employe_rouge', 'Employé rouge', 'Modèle commun compact, tête claire, costume rouge.'),
    ('employe_bleu', 'Employé bleu', 'Même géométrie et tête ; variante de couleur du costume.'),
    ('michael', 'Michael', 'Chevelure sans casquette, tenue et pendentif ; gabarit Red.'),
    ('enma', 'Seigneur Enma', 'Cheveux et vêtement resserrés dans le gabarit de Red.'),
    ('domniscian', 'Domniscian', 'Personnage compact ; bureau retiré uniquement sur la carte.'),
    ('matt', 'Matt', 'Dessin existant conservé ; neuf poses recalées sur les bornes de Red.'),
    ('ariane', 'Ariane', 'Dessin existant conservé ; hauteur et ancrage recalés sur Red.'),
    ('katie', 'Katie', 'Conservée après examen ; 59 poses inchangées, comme Nathan.'),
]
font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 16)
small = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 12)
red = Image.open(R / 'graphics/object_events/pics/people/red_normal.png').convert('RGBA')
sheet = Image.new('RGB', (940, 74 + 148 * len(actors)), (225, 225, 225))
draw = ImageDraw.Draw(sheet)
draw.text((12, 6), 'Sprites de carte : Red / avant / après — agrandissement ×4 sans lissage', font=font, fill='black')
for x, label in [(190, 'RED — référence'), (442, 'AVANT'), (694, 'APRÈS')]:
    draw.text((x, 38), label, font=font, fill='black')
rows = []
for row, (actor, label, action) in enumerate(actors):
    rel = f'graphics/yokai_characters/{actor}/' + ('normal.png' if actor == 'katie' else 'overworld.png')
    old = Image.open(io.BytesIO(subprocess.check_output(['git', 'show', f'{BASE}:{rel}'], cwd=R))).convert('RGBA')
    new = Image.open(R / rel).convert('RGBA')
    width = 32 if actor == 'domniscian' else 16
    y = 74 + row * 148
    draw.text((10, y + 52), label, font=font, fill='black')
    draw.line((0, y + 143, 940, y + 143), fill=(165, 165, 165))
    for column, (im, native_width) in enumerate([(red, 16), (old, width), (new, width)]):
        for pose in range(3):
            p = im.crop((pose * native_width, 0, (pose + 1) * native_width, 32)).resize((native_width * 4, 128), Image.Resampling.NEAREST)
            x = 188 + column * 252 + pose * 80
            # Domniscian's technical 32px cell is centered on the same actor axis.
            sheet.paste(p, (x - (native_width - 16) * 2, y + 10), p)
    bounds = [new.crop((i * width, 0, (i + 1) * width, 32)).getbbox() for i in range(3)]
    rows.append(dict(personnage=label,ressource=rel,action=action,modifie=actor!='katie',bornes_face_dos_profil=str(bounds),portrait_combat='inchangé',palette='inchangée'))
Q.mkdir(parents=True, exist_ok=True)
sheet.save(Q / 'COMPARAISON_RED_AVANT_APRES.png')
with (Q / 'CONTROLE_INDIVIDUEL.csv').open('w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator='\n');writer.writeheader();writer.writerows(rows)
print('Contact sheet and individual audit written.')
