#!/usr/bin/env python3
"""Revue explicite des151 zones + rampes HLS stables (aucun canal RGB écrêté).
Le diagnostic classe toutes les nuances utilisées : zone ou conservation voulue.
"""
import colorsys
from collections import Counter
from pathlib import Path

def rgb555(c):return tuple(v>>3<<3 for v in c)
def luma(c):return sum(x*w for x,w in zip(c,(.2126,.7152,.0722)))/255

def reviewed(n,groups,normal,weights,path):
 line=next(l for l in Path(path).read_text().splitlines() if l.startswith(str(n)+'|'))
 _,changes,protected=line.split('|');keep=set(map(int,protected.split(','))) if protected else set()
 groups=[dict(g,indices=list(g['indices'])) for g in groups]
 for entry in changes.split(';') if changes else []:
  label,rest=entry.split(':');part=rest.split('=');ids=list(map(int,part[0].split(',')))
  if len(part)==2:
   h=part[1];target=[int(h[i:i+2],16) for i in (0,2,4)]
  else:
   found=next((g for g in groups if g['zone']==label),None)
   assert found,(n,label)
   target=found['target']
  for g in groups:g['indices']=[i for i in g['indices'] if i not in ids]
  match=next((g for g in groups if g['zone']==label and g['target']==target),None)
  if match:match['indices'].extend(ids)
  else:groups.append(dict(zone=label,indices=ids,target=target))
 # Remove true black shared with silhouette/eyes from material ramps.
 for g in groups:
  black={i for i in g['indices'] if max(normal[i])<40 and n not in (137,138)}
  keep.update(black);g['indices']=[i for i in g['indices'] if i not in keep]
 groups=[g for g in groups if g['indices']]
 covered={i for g in groups for i in g['indices']};used={i for i,c in weights.items() if i and c}
 assert not (covered & keep),(n,'dual role',covered&keep)
 assert used<=covered|keep,(n,'missing',used-covered-keep)
 assert len(covered)==sum(len(g['indices']) for g in groups),(n,'duplicate index')
 shiny=[c.copy() for c in normal]
 for g in groups:
  ids=g['indices'];ordered=sorted(ids,key=lambda i:luma(normal[i]));half=sum(weights[i] for i in ids)/2;total=0;anchor=ordered[-1]
  for i in ordered:
   total+=weights[i]
   if total>=half:anchor=i;break
  h,light,sat=colorsys.rgb_to_hls(*(v/255 for v in g['target']));mid=luma(normal[anchor])
  for i in ids:
   # Compress extremes: AA and near-duplicate source hues become a single ramp.
   ratio=(luma(normal[i])+.025)/(mid+.025)
   ratio=1 if .78<=ratio<=1.22 else max(.125,round(ratio*8)/8)
   level=max(.045,min(.96,light*ratio**.9))
   chroma=(max(g['target'])-min(g['target']))/255
   saturation=min(sat,.18) if chroma<.12 else sat
   saturation*=.70+.30*min(1,level/.35)
   shiny[i]=[round(v*255) for v in colorsys.hls_to_rgb(h,level,saturation)]
  g['shade_model']='HLS, luminance ratio quantized at 1/8; original contrast preserved; near-neutral metals desaturated'
 return groups,keep,shiny

def write_gallery(q,rows):
 from html import escape
 header='''<!doctype html><html lang="fr"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>151 shiny — revue de lisibilité</title><style>body{font:16px system-ui;background:#d8dce2;color:#151c27;margin:24px}body.sombre{background:#252a35;color:#eee}header{position:sticky;top:0;background:inherit;padding:8px;z-index:1}input,button{font:inherit;padding:8px}main{display:grid;grid-template-columns:repeat(auto-fit,minmax(330px,1fr));gap:16px}article{padding:8px;border:1px solid #8888;border-radius:6px}img{image-rendering:pixelated;max-width:100%}figure{margin:0;display:flex}figure img{width:48%}details{font-size:14px}h2{font-size:18px}.natif{width:64px!important;height:64px}</style><header><h1>151 shiny — révision 2</h1><p>Face et dos seuls : contours, visage et matières se jugent sans le normal.</p><input placeholder="Nº ou nom" oninput="document.querySelectorAll('article').forEach(a=>a.hidden=!a.dataset.nom.includes(this.value.toLowerCase()))"><button onclick="document.body.classList.toggle('sombre')">Fond clair / sombre</button><button onclick="document.querySelectorAll('figure img').forEach(i=>i.classList.toggle('natif'))">Taille native / zoom</button></header><main>'''
 links=['# Galerie des 151 shiny — révision2','','Chaque vue se consulte indépendamment du sprite normal. Transparence conservée, contours et positions inchangés.','', '| Nº | Yo-kai | Face seule | Dos seul | Normal / shiny | mGBA |','|---|---|---|---|---|---|']
 for row in rows:
  n=row['number'];name=escape(row['name']);header+=f'<article data-nom="{n:03} {name.lower()}"><h2>{n:03} {name}</h2><figure><img alt="Face" src="apercus/{n:03}-front-shiny.png"><img alt="Dos" src="apercus/{n:03}-back-shiny.png"></figure><details><summary>Normal, source et méthode</summary><img src="apercus/{n:03}-comparaison-x4.png"><p>{escape(row["reference"])}</p><p>'+('Masques localisés : matières partageant une couleur séparées.' if row['masked_texture'] else 'Palette intégralement classée par zone ; nuances harmonisées.')+'</p></details></article>'
  links.append(f"| {n:03} | {row['name']} | [Face](apercus/{n:03}-front-shiny.png) | [Dos](apercus/{n:03}-back-shiny.png) | [Comparer](apercus/{n:03}-comparaison-x4.png) | [Combat](mgba/public/{n:03}-comparaison-x2.png) |")
 (q/'index.html').write_text(header+'</main></html>');(q/'GALERIE.md').write_text('\n'.join(links)+'\n')
