# Plan — Cramois'Île, soixante ans dans le passé

Base : branche validée `feature/pierre-philosovni-carmin`, commit `2e81a799f`. Travail sur `feature/cramois-ile-passe`, sans merge sur master. [Demande originale](CAHIER_DES_CHARGES.md).

## Phase A — Prototype visuel

- Audit des cartes, des palettes, des portraits et de la mémoire avant modification.
- Conversion RGB555 dorée appliquée aux treize cartes de l'île, aux PNJ et au joueur sur la carte, aux décors et aux combattants.
- Exclusion des palettes des interfaces ; menus plein écran dans leurs couleurs natives.
- Captures natives avant/après et démonstrations de combats, dans les deux versions.
- Mesure de mémoire et contrôle des ressources préservées ; réexécution du suivi d'Ariane et du duo.
- **Validation visuelle du joueur encore attendue.** Le prototype n'est pas une direction artistique définitivement approuvée.

## Phase B — Frontière maritime, après revue du prototype

Brume blanche/grise progressive sur les accès Route 21 Sud et Route 20, dans les deux sens, avec restauration des palettes. Aucun brouillard sur l'île ou ses intérieurs ; aucune réutilisation de la brume verte de Lavanville. Surf, collisions, retours après sauvegarde et déplacements spéciaux doivent rester fonctionnels. Les GIF de cette frontière ne seront produits qu'une fois son implémentation réelle réalisée.

## Phase C — Scénario et Arène

Rencontre humoristique avec Nathaniel pour le garçon et Michael pour la fille, sans que le grand-père croie jamais au voyage temporel. L'année évoquée devra s'appuyer sur la chronologie du jeu, pas sur l'horloge de l'ordinateur. Aucun lien causal confirmé avec la Pierre Philosovni, l'OVNI ou la Mafiamille.

Conserver exactement Métaurolog 40, Sirénité 41, Sal de bain 41, Brumella 42, Faux Kappa 43 et Hovernyan 45, les récompenses et la Clé Secrète. Réutiliser le quiz et les portes existantes. Questions, dans l'ordre et avec les réponses fixées :

1. « Jibanyan possède-t-il seulement deux fusions différentes ? » — NON.
2. « Whisper est-il resté enfermé pendant plus de 200 ans ? » — OUI.
3. « Steve Jaws est-il le créateur de la Yo-kai Watch moderne ? » — OUI.
4. « Le Bingo-kai est-il indispensable pour compléter le Médallium ? » — OUI.
5. « Hovernyan s'est-il déjà fait appeler Méga-nyan ? » — OUI.
6. « L'équipe des Blasters de Coach Antonic apparaît-elle dans plus de trois jeux différents ? » — OUI.

Bonne réponse : porte ouverte sans combat ; mauvaise réponse : combat du Dresseur ; combat direct toujours possible. Mesurer tous les textes avec la police GBA. Conserver la réplique après victoire : « Et si tu croises mon moi du futur, dis-lui qu'il a intérêt à être devenu un sacré Champion ! ».

## Phase D — Validation complète

Parcourir réellement les deux frontières, tous les bâtiments et sorties, le Manoir jusqu'à la Clé, la résurrection des fossiles, les six réponses correctes et incorrectes, les deux variantes de Champion et les récompenses. Tester les sauvegardes, les déplacements spéciaux et le retour après une Ligue réellement terminée. Contrôler les combats, les menus, les statuts et les jauges, l'absence de sépia résiduel, Carmin et Lavanville. Distinguer explicitement parcours réels et fixtures. Publier les rapports, captures et mesures avant/après, sans ROM ni audio privé.
