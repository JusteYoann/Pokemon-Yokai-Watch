# Étape B — jalon 3 : conclusion, Panthéon et sauvegarde

Conclusion intégrée avec les répliques de Don, Matt et Chen du document autorisé,
uniquement redistribuées sur les lignes GBA. Don et les trois gardes sortent par
des parcours distincts ; Matt reste, Chen entre ensuite. La réprimande native du
rival est aussi retirée du parcours de revanche. Aucun changement de maison.

## Parcours mGBA public et privé réussi

Le harnais commence devant Lance avec une équipe QA renforcée et l'option
native de combat Fixe. Il gagne réellement ce combat puis franchit sa porte par
les touches. Aucun flag de victoire, résultat de combat, pointeur de script ou
warp intermédiaire n'est injecté ensuite :

Lance → entrée normale → Don743 → soin HP/PP/statuts des six équipiers → fusion
masquée en blanc → Spiraton744, sprite réel et attente du choix → niveaux56–63
→ conclusion → départ de Don et des gardes → Chen → warp de scénario normal
vers le Panthéon → inscription et sauvegarde natives → crédits jusqu'aux états
17/18 → véritable Continuer → postgame.

Les victoires743/744 et GAME_CLEAR sont toujours présentes après Continuer.
Les tuiles du grand sprite sont libérées. Le premier combat contre Don ne pose
pas GAME_CLEAR. La maison d'exil est déverrouillable par ces flags obtenus
normalement ; sa vérification suit au jalon4.

Les captures `*/etape-6.png`, `*/etape-8.png`, `*/pantheon-natif.png`,
`*/postgame-apres-continue.png` et les JSON `*/FINALE_NORMALE_MGBA.json` documentent
le résultat, les SHA des ROM, les huit niveaux et les étapes.

## Limites

Le point initial et l'équipe sont des fixtures. Ce test prouve le dernier
segment de la Ligue à partir de Lance, sans raccourci dans la nouvelle finale.
Il ne prouve pas un parcours complet depuis le choix du starter ni l'équilibrage
avec statistiques normales. Une fixture d'équipier K.O./empoisonné/PP0 est placée
à l'entrée de la salle du Maître pour mesurer le soin, sans toucher aux flags.
