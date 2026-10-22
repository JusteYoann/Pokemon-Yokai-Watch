# Agent X natif

Face approuvée conservée exactement ; neuf images 16 × 32 (face, dos, profil et pas), profil droit par miroir moteur. Source explicite et palette personnelle dans graphics/yokai_characters/agent_x/source. Les GIF apercu sont des vues de sources ; les GIF et captures mgba sont des tests du moteur.

Test reproductible : python3 tools/yokai/tester_agent_x_complet_mgba.py. Quatre orientations, quatre cycles de marche, flip Est et déplacement horizontal ; tuiles et palette comparées aux fichiers compilés. Coexistence vérifiée avec Nathan, Don Morleone et six Mafiamille, sans injection de graphismes. La palette est allouée avec le gestionnaire natif dans les banques libres12 à15, afin de conserver la palette commune du groupe Morleone. La saturation de toutes les banques et toutes les combinaisons d’effets/reflets ne sont pas testées.

Le portrait est chargé par CreateTrainerPicSprite dans un décor de combat de test. Aucun combat scénaristique Agent X ni équipe inventée ; les autres poses et le portrait attendent le retour artistique du créateur.
