# Cartes, variantes et événements — spécifications de géographie

## Principes VALIDÉS

**LAVANVILLE ZOMBIE NIGHT = géographie inchangée.** On conserve le plan de la ville de Pokémon Rouge Feu. La variante concerne uniquement lumière/couleurs/ambiance, musique, acteurs et événements.

**CRAMOIS'ÎLE PASSÉE = même géographie fondamentale.** Le joueur reconnaît les rues et côtes ; des bâtiments/décors/PNJ peuvent refléter leur état historique, mais pas de nouvelle île. Les intérieurs peuvent être adaptés et il faut une vraie version d'époque du Manoir et de l'arène si le moteur le demande.

**HUIT ARÈNES / TEMPLE / LIMBES / PARADIS = CARTE BLANCHE À CODEX.** Il conçoit le level design adapté aux idées des personnages. Ne pas exiger les anciens plans de Rouge Feu ; il peut réutiliser des maps ou en créer de nouvelles sous budget GBA.

## Maps du dépôt existant à connaître

Les chemins ci-dessous étaient présents au moment de l'audit ; ils sont des **points de départ**, pas des preuves que les nouvelles scènes y sont déjà programmées.

| Besoin | Emplacement du dépôt existant | Travail demandé |
|---|---|---|
| Prologue | `data/maps/PalletTown_ProfessorOaksLab/` | Montre, Médallium, Matt, Chen |
| Rencontre Argenta | `data/maps/PewterCity/` | Rassemblement Morleone + Enma incognito |
| Arène Wyatt | `data/maps/PewterCity_Gym/` | Nouvelle identité Roche/exploration |
| Arène Nathan/Katie | `data/maps/CeruleanCity_Gym/` | Champion conditionnel, Feu |
| Bérénice | `data/maps/VermilionCity_Gym/` | Portes Mystères, Psy |
| Ancienne arène Céladopole | `data/maps/CeladonCity_Gym/` | **Sans neuvième trophée** ; reconversion à décider |
| Mafiamille Céladopole | `data/maps/CeladonCity_GameCorner/`, `data/maps/RocketHideout_B1F/` ... | Option d'intrigue Agent X, non validée |
| Ariane | `data/maps/SaffronCity_Gym/` | Station spatiale Acier |
| Giraud | `data/maps/FuchsiaCity_Gym/` | Enquête/Combat |
| Lavanville | `data/maps/LavenderTown/` | Zombie Night : état de carte, pas refonte du plan |
| Tour Pokémon | `data/maps/PokemonTower_1F/` ... `PokemonTower_7F/` | Événements Zombie Night / Alyzon, salle au sommet proposée |
| Cramois'Île actuelle | `data/maps/CinnabarIsland/` | Retour temporel / grand-père âgé postgame |
| Manoir | `data/maps/PokemonMansion_1F/` ... `PokemonMansion_B1F/` | Rencontre Triptic-tac / versions du passé |
| Arène du passé | `data/maps/CinnabarIsland_Gym/` + clone/variante | Champion jeune, septième trophée |
| Jadielle | `data/maps/ViridianCity_Gym/` | Don Morleone, huitième trophée |
| Ancienne Ligue | `data/maps/PokemonLeague_LoreleisRoom/` ... `PokemonLeague_HallOfFame/` | Remplacer le sens narratif par le Temple/Panthéon |
| Île 7 | `data/maps/SevenIsland/` et secteurs associés | Combat Seigneur Enma postgame |
| Centrale | `data/maps/PowerPlant/` | Octorgone |
| Îles Écume | `data/maps/SeafoamIslands_1F/` ... `SeafoamIslands_B4F/` | Kyubi ou Mademoaiselle, à arbitrer |
| Mont Braise | `data/maps/MtEmber_Summit/` | Kyubi ou Mademoaiselle, à arbitrer |
| Caverne Azurée | `data/maps/CeruleanCave_B1F/` | Enma n°150 existant à examiner |

## Zombie Night — transitions obligatoires

1. Sauvegarde du bon état de carte et des flags avant déclenchement.
2. Passage en ambiance nocturne (palette, éclairage, BGM et option de filtres compatibles GBA).
3. Retrait/remplacement des **habitants humains** par zombies. **Ne pas expliquer qu'ils ont été transformés.**
4. Contact zombie → **combat contre son équipe Yo-kai**. Un NPC ne doit pas infliger de dégâts via collisions hors combat.
5. Alyzon parle de ses observations et permet d'avancer vers l'objectif.
6. Fin d'événement : retour à l'état normal des rues, personnages et musiques, quelle que soit la route choisie par le moteur.
7. À DÉCIDER : cloche de la Tour, déclencheurs de fin, état des zombies battus, défaite, fuite, sortie par portes/Vol.
8. Sauvegarder au milieu de Zombie Night, éteindre/recharger, terminer et vérifier que les PNJ reviennent correctement.

**Important** : éviter de créer une « deuxième ville physique » sans raison ; l'implémentation peut réutiliser la carte courante avec variantes d'events, ou cloner une map de même layout si nécessaire, mais le **résultat visuel et navigable doit conserver le même plan**.

## Cramois'Île — transitions obligatoires

1. Au présent, le Champion est annoncé absent ; indice vers le Manoir Pokémon.
2. Interaction avec Triptic-tac → flash blanc/filtre sépia, **même position logique** dans un manoir passé, avec sortie cohérente.
3. Triptic-tac refuse le retour immédiat.
4. Le joueur traverse **seulement Cramois'Île passée**, rejoint son Champion conditionnel, gagne le trophée et obtient son aide.
5. Triptic-tac autorise de nouveau la transition vers le présent.
6. Après cette quête, aller-retour entre les deux époques de l'île devient permanent.
7. À éviter absolument : Vol, Surf, Téléport, Tunnel, trous de carte, bateau et autres moyens de quitter le passé vers Kanto. Désactiver ou intercepter proprement les sorties, sans bloquer définitivement un objet dans le sac.
8. Tester sauvegardes dans manoir, extérieur, arène et état entre combat/retour ; équipe pleine, KO, défaite, rechargement.

## Temple et nouveaux donjons

- Codex crée des salles originales pour les quatre adversaires et une pièce de sanctuaire Soranaki, sans chercher à plaquer les quatre anciennes salles à l'identique.
- **Bingo-kai et Panthéon** : privilégier l'appel au Hall of Fame existant, avec nouvelle scène narrative préalable.
- Les **Limbes** et le **Paradis Divin** sont deux ensembles postgame distincts ; si leurs passages s'enchaînent, prévoir au moins un retour vers Kanto.
- Création de tilesets à partir de références : validation artistique et budget VRAM obligatoires ; jamais copier des captures 3DS directement comme carte GBA.

## Tests de navigation, collision et progression

Pour chaque nouvelle map : collisions, priorités de couches, escaliers, portes, retour après combat, reprise après sauvegarde, inaccessibilité prématurée des zones, fonctionnement des badges, warp IDs, musique sur entrée/sortie, possibilité de traverser toutes les salles sans blocage. Tester en **Nathan et Katie** pour chaque embranchement.
