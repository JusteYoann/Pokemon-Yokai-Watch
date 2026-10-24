"""Conversion de l'illustration du Short Oni en icône GBA, sans tramage."""
from pathlib import Path
from PIL import Image
ROOT = Path(__file__).resolve().parents[2]
folder = ROOT / 'graphics/short_oni'
source = Image.open(folder / 'source/icone-generee.png').convert('RGBA')
alpha = source.getchannel('A').point(lambda a: 255 if a >= 128 else 0)
source.putalpha(alpha)
sprite = source.crop(alpha.getbbox())
sprite.thumbnail((22, 22), Image.Resampling.NEAREST)
canvas = Image.new('RGBA', (24, 24))
canvas.alpha_composite(sprite, ((24-sprite.width)//2, (24-sprite.height)//2))
colors = [(16, 8, 16), (64, 8, 24), (112, 8, 32), (168, 8, 40),
          (216, 16, 40), (248, 32, 48), (80, 48, 32), (120, 72, 48),
          (160, 104, 64), (216, 184, 112), (248, 240, 184),
          (128, 88, 0), (192, 136, 0), (248, 208, 24), (248, 248, 224)]
result = Image.new('P', (24, 24), 0)
result.putpalette([0,0,0]+[v for c in colors for v in c]+[0]*720)
for y in range(24):
    for x in range(24):
        r,g,b,a = canvas.getpixel((x,y))
        if a:
            idx = min(range(len(colors)), key=lambda i: sum((a-b)**2 for a,b in zip((r,g,b),colors[i])))
            result.putpixel((x,y),idx+1)
result.save(folder/'icon.png', transparency=0)
(folder/'normal.pal').write_text('JASC-PAL\n0100\n16\n0 0 0\n'+'\n'.join(' '.join(map(str,c)) for c in colors)+'\n')
preview = result.convert('RGBA')
preview.save(ROOT/'docs/short-oni-20261025/short-oni.png')
preview.resize((240,240),Image.Resampling.NEAREST).save(ROOT/'docs/short-oni-20261025/short-oni-x10.png')
assert result.size == (24,24) and max(result.getdata()) <= 15
print('Short Oni : 24 × 24, transparence index 0, 15 couleurs opaques maximum.')
