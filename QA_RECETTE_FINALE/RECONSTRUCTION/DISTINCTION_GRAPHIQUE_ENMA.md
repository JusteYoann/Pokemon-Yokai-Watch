# Correction : la créature Enma utilisait le sprite du personnage

Le contrôle des nouvelles directives a confirmé que les deux événements partageaient OBJ_EVENT_GFX_YOKAI_ENMA154. Ce dessin représente le Seigneur Enma humain ; il ne correspond pas au félin violet à flammes du sprite de combat approuvé de l’espèce150. Les tests précédents prouvaient le déblocage et la capture mais ne détectaient pas cette confusion graphique.

Une ressource originale dédiée est créée à partir de `graphics/yokai/150/front.png`, sans redessiner ni modifier ce sprite de combat. Source conservée dans `graphics/yokai_characters/enma_creature/source/generated-sprite.png`, réduction technique et indexation par `tools/yokai/convertir_enma_creature.py`, palette normale16entrées RGB555, index0 transparent, overworld32×32. L’aperçu sur damier est un vrai PNG opaque. Une seule pose frontale est adaptée à cette rencontre stationnaire ; elle utilise les animations natives inanimées.

L’identifiant168 est ajouté après les anciens, sans les renuméroter. Palette dédiée0x1126 et table de reflet. **Seul l’objet capturable de CeruleanCave_B1F change d’affectation**. Le Seigneur Enma demeure154 au Mont Braise ; portrait, équipe, dialogues, Kyubi, scripts, flags de déblocage et capture sont conservés. Aucun changement de sauvegarde ou de données des151espèces.

Contrôles : build, ressources liées comparées à l’indexation4bpp attendue, palette et dimensions, test natif Enma étendu pour vérifier l’identifiant de créature et sa palette chargée. Le drapeau Médallium capturé est également vérifié absent après victoire du dresseur et présent uniquement après la véritable capture. Voir TEST_ENMA_MGBA.json et la capture `preuves/enma-debloque-caverne-azuree.png`.

Cette correction ne valide pas encore Misterre, Mademoaiselle et Octorgone : leurs overworld dédiés restent à traiter. Aucun parcours intégral n’est annoncé.
