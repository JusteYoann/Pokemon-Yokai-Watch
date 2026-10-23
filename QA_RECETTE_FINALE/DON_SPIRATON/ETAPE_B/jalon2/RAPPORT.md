# Étape B — jalon 2 : entrée normale

La salle du Maître choisit désormais Don + trois sbires avant GAME_CLEAR, Matt
seul après GAME_CLEAR. Deux flags temporaires gèrent leur visibilité, aucun
nouveau flag permanent. L'entrée normale fait avancer le joueur jusqu'à(6,10)
puis appelle l'unique cinématique existante. Aucun appel RPC au scénario.

Les deux ROM passent le test `tester_spiraton_entree_normale_mgba.py` : combats
743 puis744, soin natif des PV/PP/statuts y compris d'un équipier K.O., palettes
Matt6/Don10 indépendantes, convergence, disparition sous flash blanc >99%,
attente du premier choix, niveaux56–63. Captures et SHA dans public/ et prive/.

Limite exacte : départ préparé au seuil de la salle du Maître avec équipe QA ;
ni Conseil4 ni Panthéon revendiqués ici. La conclusion et le raccordement final
restent le jalon3. La maison d'exil, les équipes et les OST restent inchangées.
