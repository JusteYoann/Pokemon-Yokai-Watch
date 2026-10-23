# Audit de la quête Juste Yoann

Base : `67b227302`, branche dédiée `feature/juste-yoann-charme-chroma`. Aucun merge sur master.

- Le Médallium repose sur les bits natifs « aperçu » et « obtenu ». La condition vérifie individuellement les 151 bits obtenus, y compris les espèces mythiques, plutôt que le compteur de diplôme qui comporte des exceptions.
- Chen possède déjà plusieurs branches scénaristiques et un événement de complétion. L’invitation doit s’insérer sans supprimer ses événements existants et avec son propre drapeau permanent.
- La chambre du joueur ne contient aucun objet événement. Son PC est en `(1,1)`, l’escalier en `(10,2)` ; le placement du nouvel objet sera validé en mGBA avec son graphisme définitif.
- Les bits persistants `0x331` à `0x334` sont disponibles après les allocations de Yopple. Aucun agrandissement de SaveBlock n’est nécessaire.
- L’objet inutilisé nº52 peut accueillir le Charme Chroma sans modifier le nombre ou les identifiants des autres objets. Importance 2, poche objets importants, aucune utilisation de combat ; réemploi de l’icône Grelot Zen.
- L’équipe demandée correspond aux espèces `40,59,89,133,40,150`, toutes au niveau 70. Les deux Démophage sont intentionnels. Des attaques natives de montée en niveau, aucun objet tenu, un paramètre IV 100 et une IA classique suffisent ; aucune modification de statistiques de base n’est requise.
- Le bonus Safari existant transforme 24 résultats XOR sur 65536 avant la création du Yo-kai. Le charme effectue jusqu’à trois tirages et conserve le premier succès ; chaque tentative Safari conserve son taux triplé. Les cadeaux, rencontres statiques et équipes de Dresseur ne passent pas par ce chemin. La politique existante autorisant les shinies pour 84 espèces et tous les assets shiny restent intacts.
- Le fondu peut utiliser un masque qui épargne les palettes de texte pendant le discours, puis une petite fenêtre temporaire et une tâche pour THANK FOR PLAY. Aucune variable EWRAM permanente n’est nécessaire.

## Graphismes : résolution après cet audit

Le premier aperçu n’était pas disponible sous forme de fichier dans l’environnement. L’utilisateur a ensuite autorisé une reproduction, demandé une peau presque blanche, puis approuvé le résultat et demandé son intégration. Cette reproduction est maintenant conservée dans `graphics/juste_yoann/source/reproduction-peau-claire.png` et convertie en formats GBA. Aucun fichier supplémentaire n’est attendu.

Le PNJ, son portrait, son équipe et les hooks de Chen/chambre sont désormais intégrés. Les tests et captures définitifs figurent dans [le rapport](RAPPORT.md), dossier `integration/`.
