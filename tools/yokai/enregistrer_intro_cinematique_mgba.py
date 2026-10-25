#!/usr/bin/env python3
from mgba_rpc import Emulator,ROOT
from film_cible_mgba import Film
import mgba_new_game
r=Emulator(initial_frames=1)
film=Film(r,ROOT/'docs/cinematiques-compilation-20261025/00-titre-introduction.mp4')
mgba_new_game.Emulator=lambda:r
# Same real buttons and naming keyboard as the native new-game helper, with
# readable dialogue pauses. There is no save/script injection during capture.
source=__import__('inspect').getsource(mgba_new_game.new_game)
source=source.replace('r.keys={8} if press and f%16<4 else set()', 'r.keys=film.paced({8}) if press and f%16<4 else set()').replace('r.keys={8} if f%16<4 else set()', 'r.keys=film.paced({8}) if f%16<4 else set()')
namespace=dict(mgba_new_game.__dict__,film=film)
try:
 exec(source,namespace);namespace['new_game']();r.keys=set();r.run(120)
 film.finish(scene='Titre et présentation du monde, Nathan et Matt',controller_only_from_boot=True)
finally:r.close()
