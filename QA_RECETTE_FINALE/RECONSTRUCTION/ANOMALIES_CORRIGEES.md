# Anomalies de la reconstruction — preuves et limites

- **Probabilité du troisième starter au Canyon Sesor** : un slot terrestre vaut 4 %, et non 5 %. Une case de 1 % lui a été ajoutée ; Komasan, Padrézo et Kappacap totalisent chacun 5 %. Le contrôle indépendant des poids détecte cet écart.
- **Matt overworld découpé en morceaux** : la conversion générique des PNG groupait les tuiles sur toute la planche. Une règle explicite groupe chaque frame 16×32. Le comparateur binaire vérifie l’ordre exact des neuf frames ; les captures mGBA corrigées sont conservées.
- **Direction d’une frame de Matt** : le dessin généré regarde à droite. Les commandes d’animation appliquent le retournement approprié pour les marches vers l’ouest et l’est.
- **Fossile non choisi et deuxième récompense du Dojo** : les anciennes exclusivités rendaient des familles manquantes dans une partie. Les fossiles achetables sont reconnus par l’inventaire ; les deux cadeaux du Dojo ont des flags distincts. L’envoi des deux cadeaux au PC a été testé.
- **Anciennes sorties d’évolution hors roster et attaques d’origine** : tables actives retargetées aux données validées, avec contrôle des 56 évolutions et des 151 apprentissages réellement liés.
- **Noms trop longs** : abréviations terminées par un point, avec table complète des noms canoniques. Pas de changement de SPECIES_*.
- **Pilote de test d’Ariane** : des temporisations fixes tentaient une nouvelle interaction trop tôt ou s’arrêtaient avant la fin du cadeau. Le pilote attend l’état réel du script, utilise les boutons du jeu et exige qu’une interaction démarre effectivement. Des fixtures comportant un nom de joueur correctement terminé et une équipe valide sont requises. Ces corrections du pilote ne prouvent pas un défaut de l’aventure.

- **Enma capturable sans duel caméo** : ajout de la condition de première victoire réelle, contrôle sur entrée de carte et sur interaction. La capture ajoute un verrou permanent distinct ; une revanche ne peut pas recréer l'objet capturable.
- **Deux dialogues Enma dépassaient 208 pixels** : reformulation, puis mesure des 56 lignes Ariane/Enma par la police native du jeu. Le comptage des caractères seul n'est pas utilisé comme preuve.
- **Pilote du test Enma** : attente de l'état réel de chargement des cartes ; plusieurs fonctions statiques portent le même nom dans les contrôleurs de combat, toutes leurs adresses sont conservées pour reconnaître le menu. Les cas Flash utilisent des instances indépendantes : la restauration libretro n'emploie pas les mêmes flags savedata que sa sérialisation. Une fixture à deux membres utilise l'option SET ; la réponse automatique Oui au menu SHIFT ouvrait normalement le menu d'équipe. Ces corrections sont celles du pilote, pas des modifications des combats du jeu.

## Restent ouverts

Dessins shiny définitifs et cornes de Robonyan 28, personnages Nathan/Katie, autres caméos, overworld statiques restants (Misterre, Octorgone, Mademoaiselle), traduction complète, rendements d’expérience/capture hérités des anciens slots à auditer, équilibrage du parcours, dix quêtes, musiques DPCM, toutes les animations de capacités et parcours intégral de l’aventure. Le verdict global reste **NON PRÊT**.
