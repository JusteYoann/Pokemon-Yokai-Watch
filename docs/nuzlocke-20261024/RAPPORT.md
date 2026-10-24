# Mode Normal / Nuzlocke

Branche dédiée : `feature/mode-nuzlocke-20261024`, issue de la branche de nuit progressive de Lavanville. Les corrections de captures par rang, d'abandon et de combat duo restent incluses. Aucun changement sur master et aucune nouvelle ROM publiée.

## Règles intégrées

Le choix Normal / Nuzlocke apparaît pendant la création de partie, après le choix garçon/fille. L'écran précise que les K.O. sont définitifs et qu'une défaite totale efface la partie. Le choix est enregistré et n'est pas modifiable en cours de partie. Les anciennes sauvegardes restent en mode Normal.

En Nuzlocke :

- Un Yo-kai mis K.O. en combat ou par le poison hors combat meurt définitivement. Il ne peut être ressuscité par les soins, Rappels, objets ou une reconstruction depuis le PC. Les morts sont retirés de l'équipe après le combat ou les messages de poison, lorsque les indices de combat ne sont plus utilisés.
- Seule la première rencontre sauvage admissible d'une zone peut être capturée. La zone est consommée dès cette rencontre, même sans lancer de Ball, en cas de fuite, de K.O. ou d'échec. Plusieurs lancers restent possibles pendant cette première rencontre.
- Selon la précision validée par l'utilisateur, les espèces déjà obtenues sont ignorées pour déterminer cette première rencontre. Leur capture reste interdite, même après mort ou libération. Les espèces obtenues par cadeau et les évolutions inscrites au Médaillium sont également prises en compte.
- Les shinies sont capturables malgré une zone consommée ou une espèce déjà obtenue. Leur rencontre ne consomme pas la tentative ordinaire de la zone.
- Une zone correspond au nom de lieu de la carte (`regionMapSectionId`) : les différents étages d'un même lieu partagent donc la même tentative.
- Les restrictions de rencontre commencent à la remise du Médaillium et des premières Balls chez Chen, pour ne pas perdre la Route 1 lors du trajet du colis sans Balls. Chen donne 10 Balls au lieu de 5 lors de cette première remise. Les prix des Balls baissent de 20 % ; les autres objets conservent leur prix.
- Si l'équipe est décimée mais qu'un survivant reste au PC, il rejoint l'équipe et le joueur retourne au Centre. Les alliés temporaires, dont celui d'Ariane, ne comptent pas parmi les survivants personnels. Une équipe composée uniquement d'œufs n'est pas une équipe apte au combat.
- Sans survivant dans l'équipe ou les 14 boîtes, le jeu efface les deux générations de la sauvegarde et affiche le game over. A ramène au démarrage, sans option Continuer valide. Cela concerne la batterie courante de la ROM ; le jeu ne supprime pas les copies de fichiers ou états rapides conservés à l'extérieur par l'émulateur.

Les démonstrations de capture et les combats en liaison sont exclus des règles du défi. Les cadeaux ne consomment pas de rencontre sauvage. Le mode Normal conserve les règles existantes.

## Vérifications ciblées dans mGBA

Les deux versions compilent. Essais avec le personnage garçon sur la version publique et fille sur la version privée :

- 15 contrôles natifs de politique et de persistance par version : choix du mode par boutons, première rencontre, doublons, libération, shinies, trajet sans Balls, prix, soins/Rappels/PC, poison, survivant dans la dernière case de la dernière boîte, sauvegarde batterie puis Continuer, effacement intégral et redémarrage sans sauvegarde valide.
- 5 scénarios de combat par version : fuite réelle puis refus de capture dans le Sac sans consommation de Ball ; capture réelle de la première rencontre avec ajout correct du Yo-kai à l'équipe ; attaque fatale avec secours du PC et retour au Centre avec les commandes déverrouillées ; attaque fatale sans réserve ; défaite réelle contre un dresseur. Les dégâts et résultats ne sont pas injectés.
- 3 contrôles supplémentaires par version : première remise native de 5 Balls en Normal, 10 en Nuzlocke, soins/captures/prix ordinaires en Normal.
- Les 10 anciennes sauvegardes du parcours chargé avec Continuer restent lisibles, avec équipe, niveaux, PV et position préservés ; leurs fichiers sources restent identiques.

Ces essais utilisent des équipes, des positions, des adversaires et des drapeaux préparés. Des états de branche permettent d'isoler les scénarios. Il ne s'agit pas d'une traversée intégrale du jeu en Nuzlocke, ni d'une reprise de la campagne générale interrompue.

Résultats : [public](public/TEST.json), [combats publics](public/COMBATS.json), [Normal public](public/NORMAL.json), [privé](prive/TEST.json), [combats privés](prive/COMBATS.json), [Normal privé](prive/NORMAL.json), [anciennes sauvegardes](COMPATIBILITE_SAVES.json).

Captures : [choix du mode](public/choix-mode.png), [capture refusée](public/capture-refusee.png), [survivant du PC au Centre](public/survivant-pc.png), [game over après défaite réelle](public/defaite-reelle.png).

## Technique et compilation

Le suivi des zones et des espèces utilise l'ancien espace inutilisé de 400 octets à `SaveBlock1 + 0x348C`. La taille et les décalages de la sauvegarde ne changent pas. Une signature identifie uniquement les nouvelles parties Nuzlocke. Un bit de ruban inutilisé marque les morts pendant le combat pour bloquer les tentatives de résurrection avant le retrait de l'équipe. Les indices de l'allié temporaire sont exclus.

Les règles sont centralisées dans `src/nuzlocke.c`, avec des appels lors de l'initialisation, des rencontres, captures, K.O., soins et sorties de combat. Les scripts de Chen conservent leur variante Normal.

ROM publique compilée : 16 777 216 octets avec remplissage. ROM privée : 33 452 051 octets, soit +1 880 octets par rapport à la nuit progressive seule. Empreintes : [COMPILATION.json](COMPILATION.json). Les musiques ne sont pas modifiées.

Reproduction après compilation et chargement de l'environnement :

```bash
python tools/yokai/tester_nuzlocke_mgba.py
python tools/yokai/tester_nuzlocke_combats_mgba.py
python tools/yokai/tester_nuzlocke_normal_mgba.py
```

Pour la version privée, définir `NUZ_MODE=prive`, `NUZ_GENDER=1`, `YOKAI_QA_ROM=$PWD/pokefirered_audio.gba` et `YOKAI_QA_ELF=$PWD/pokefirered_audio.elf`.
