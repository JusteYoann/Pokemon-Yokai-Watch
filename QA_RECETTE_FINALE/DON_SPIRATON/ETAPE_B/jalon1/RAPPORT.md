# Étape B — jalon 1 : véritable sprite et Morphing

Le sprite harmonisé approuvé est désormais chargé automatiquement sur le sprite
logique de l'adversaire, à l'entrée du combat 744 armé. Il ne s'agit plus d'une
superposition QA. Les quatre OBJ partagent le sprite, la visibilité, la priorité
et le banc de palette natif de l'adversaire. Aucun nouveau sprite overworld.

Centre (176,38), soit quatre pixels plus bas que l'aperçu : silhouette entière
(112×76) visible de y=0 à75, sans réduction ni recouvrement du HUD joueur (y=76).
Les pixels et la palette du fichier approuvé sont inchangés.

Le premier Morphing utilise la tâche et les deux sons natifs. Une variante du
script d'animation applique la mosaïque aux OBJ du grand sprite plutôt qu'au
clone BG limité à64×64. Au point de remplacement natif, les sous-objets sont
retirés, les tuiles sont libérées et Bouh reprend le sprite normal. Les sept
Morphing suivants et les transformations ordinaires gardent le chemin natif.
La palette normale est rétablie après chaque animation comme précédemment.

## Vérifications réelles mGBA

Public et privé : huit espèces distinctes aux niveaux56–63, huit couleurs de PV,
aucune EXP intermédiaire, victoire seulement après la dernière barre, attente du
choix du joueur, apparition personnalisée, tuiles et palette du véritable boss
vérifiées au premier menu puis libérées après son Morphing. Deux déclenchements
sonores natifs par transformation, exactement8 `se_m_teleport` et8
`se_m_minimize`, observés dans les mélangeurs SE : aucun double déclenchement.
Ce contrôle du mélangeur ne constitue pas une écoute humaine.

Captures : `public/premier-choix-avant-morphing.png`,
`prive/premier-choix-avant-morphing.png`, `*/PREMIER_MORPHING.gif`.
Résultats et SHA de ROM : `*/COMBAT_PROTOTYPE_MGBA.json`.

Public :16777216 octets. Privé :31658395 octets (<33554432).
EWRAM :261128/262144, soit +4octets statiques,1016 libres.
IWRAM :29824 public,29888 privé, inchangée.
VRAM OBJ transitoire :192tuiles/6144octets, aucun banc de palette ajouté.
Les ressources graphiques151, cartes, maison d'exil et31 OST sont inchangées.

## Limite de ce jalon

Combat isolé déclenché par le harnais avec un joueur de niveau65 aux statistiques
augmentées. Ce n'est pas encore la recette de la première conquête ni un test
d'équilibrage. Le raccordement normal, la conclusion et le Panthéon suivent aux
jalons2–4. Les anciens outils `tester_spiraton_art_phase_a.py` décrivent l'ancien
aperçu QA et sont historiques ; utiliser le test de combat pour l'art intégré.
