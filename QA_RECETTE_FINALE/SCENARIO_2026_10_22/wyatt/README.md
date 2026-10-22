# Lot C1 — Wyatt Champion d'Argenta

**Implémenté et testé sur le moteur, sans modifier l'équipe validée.** L'identifiant technique `TRAINER_LEADER_BROCK`, ses trois membres, niveaux, capacités, talents, objets, CT39, récompense monétaire et flag du premier trophée restent inchangés. Le portrait et le sprite de terrain déjà approuvés de Wyatt sont réutilisés; aucune image n'est dessinée ou remplacée.

## Modifications

- L'objet1 de l'Arène affiche Wyatt; le dresseur et son profil de Fame Checker (profil des personnages) utilisent son nom et son portrait. Les identifiants historiques Brock restent stables.
- Textes de l'Arène, mentions de son rôle à Argenta et au Mont Sélénite, biographie et journal cohérents avec Wyatt. La terminologie Trophée Roche s'applique à son dialogue; la conversion globale de l'interface des huit trophées reste un autre lot.
- Défaite raccourcie de332à90octets pour un prénom A, en déplaçant l'explication de Flash dans le dialogue de terrain existant. Capacité du tampon:300octets. Le chemin natif exact passe par `GetTrainerALoseText`, qui développe d'abord les variables de terrain.
- `roles_champions.json` et son applicateur séparent l'identité scénaristique des équipes validées. L'importeur d'équipes réapplique cette identité après génération; l'applicateur est idempotent. L'importeur complet n'a pas été relancé pour ce lot.

## Tests réellement exécutés

- Compilations publique et privée réussies. `BUILD.json` donne tailles et empreintes; privé:31589579octets, inférieur à32Mio. Les26OST existantes sont conservées.
- Nouvelle partie réelle avec Nathan, puis Katie, téléportation de fixture devant le Champion et interactions/combat gagnés par commandes de manette. Trophée1 et CT39 obtenus, aucun doublon lors d'une nouvelle interaction.
- Cas CT39 déjà empilée999fois: combat gagné, récompense différée; retrait de la pile puis réinteraction, sans nouveau combat, donne bien une CT39. Il s'agit d'une saturation de pile, pas d'un sac rempli de faux objets.
- Sauvegarde Flash native et rechargement: flags de victoire/trophée/CT39 et objet conservés, pour les deux personnages.
- Défaite/retour au centre de soins: aucun trophée, victoire ou CT39 accordé.
- Construction native de l'équipe comparée aux trois membres verrouillés, y compris ordre, niveaux, attaques, talents et objets.
- Expansion native du texte: aucun octet des48octets sentinelles voisins modifié après correction, contre débordement reproduit avant.
-134lignes contrôlées avec la mesure native de police normale et un prénom de sept W: toutes dans208pixels.
-1774fichiers de données, graphismes et audio contrôlés inchangés par rapport au jalon d'audit, ainsi que tous les scripts de gameplay. Voir `NON_REGRESSION.json`.
- Captures natives `*-map.png`, `*-combat-150.png`, `*-combat-800.png`, `*-apres.png`. Les captures Nathan terrain/portrait/combat ont aussi été ouvertes et examinées visuellement.

## Limites

Les victoires utilisent une équipe de fixture surpuissante et la défaite une équipe de1PV: elles ne valident pas l'équilibrage. La téléportation ne valide pas l'accès depuis Bourg Palette. Les autres arènes et le nouveau scénario restent à intégrer. Les menus globaux et leurs noms de trophées ne sont pas annoncés convertis. Ce lot n'est pas une recette complète ni une v1 finale.
