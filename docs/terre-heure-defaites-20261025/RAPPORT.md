# Terr’heure — trois variantes avec défaite

Trois enregistrements continus avec le son direct de mGBA, sans coupe ni accélération :

| Vidéo | Grotte | Durée |
| --- | --- | --- |
| [Défaite contre Gargaros](defaite-gargaros-mont-selenite-mgba.mp4) | Mont Sélénite | 1 min 28 s |
| [Défaite contre Ogralos](defaite-ogralos-grotte-sombre-mgba.mp4) | Grotte Sombre | 1 min 25 s |
| [Défaite contre Orqanos](defaite-orqanos-iles-ecume-mgba.mp4) | Îles Écume | 2 min 07 s |

Chaque vidéo montre le déclenchement, l’approche de l’Oni, un véritable combat perdu, le message d’échec, puis le retour à la grotte normale et dix secondes supplémentaires avec les commandes disponibles.

La situation initiale, le stade Oni et une équipe volontairement faible (Seigneur Enma niveau 5, statistiques et capacités naturelles) sont préparés avant la capture. Pendant l’enregistrement, seules les commandes de la manette sont envoyées ; le résultat de combat, les PV et le chronomètre ne sont jamais modifiés. Le jeu produit lui-même la défaite et rétablit l’équipe au retour.

Les vérifications automatiques confirment pour les trois prises le résultat natif `B_OUTCOME_LOST` (2), l’absence de victoire ou de sortie par la porte, les commandes rendues, dix secondes après retour et les PV de l’équipe rétablis à leur maximum. Le mode utilisé est Normal.

Métadonnées : [Gargaros](gargaros.json), [Ogralos](ogralos.json), [Orqanos](orqanos.json).

La ROM est exactement celle des [trois fuites et du fondu après victoire](../terre-heure-regard-oni-20261025/RAPPORT.md). Aucune modification du jeu n’a été nécessaire pour ces vidéos.

SHA-256 ROM : `53c62090c8838a2eff68d6abc019ec9b3f13f44daa1ba679fdb6079faefb101b`.

Branche dédiée : `fix/terre-heure-regard-oni-20261025`. Aucune fusion sur `master`.
