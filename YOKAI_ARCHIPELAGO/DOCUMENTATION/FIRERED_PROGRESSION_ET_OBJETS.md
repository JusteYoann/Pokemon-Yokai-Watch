# Rouge Feu Archipelago : progression et traitement des récompenses

Jalon expérimental du 14 novembre 2026. Sources du vrai fangame RC1, pas le moteur vanilla de ce dépôt. Aucun changement aux espèces, statistiques, talents, équipes, rencontres, cartes ou scénario.

## Périmètre actif

15 checks : huit badges, quatre objets visibles de la Forêt de Jade, deux objets cachés de cette forêt et le don de la Maison Secrète du Safari. Les sept collectes/dons **remplacent** leur récompense native ; les badges conservent leur effet natif et ajoutent un check distinct. Aucun check postgame.

Les données détaillées sont dans `APWORLDS/pokemon_yokai_firered/checks.json` : 351 sources visibles/cachées et un don activé, plus une file d’audit de 67 macros de dons (dont ce don). Ces nombres ne s’additionnent pas en nombre de checks prêts. Les autres sources restent candidates ou exclues, avec leurs prérequis explicitement non validés. Les dons C et appels indirects restent à inventorier. Les noms de candidats contenant des noms internes de cartes ne sont pas encore une localisation française définitive.

Identifiants ordinaires : `0x594B2000 + valeur du flag natif`. Les huit badges conservent `0x594B1000..0x594B1007`. Les flags restent l’autorité persistante, lus par le canal natif. Pas de seconde récompense locale, pas de flag arbitraire partagé avec l’Aspirateur ou Blasters. Les sept flags sont exposés dans les bits 8 à 14 ; les badges dans 0 à 7. Une nouvelle partie et une nouvelle seed sont nécessaires ; ne pas convertir une sauvegarde de campagne déjà avancée.

## Objets

| Classe | Éléments du jalon | Traitement |
|---|---|---|
| Progression randomisée | CS03 Surf (`ITEM_HM03`, 341) | Un exemplaire dans le pool ; aucune remise native au Safari |
| Secondaires | Potion, Super Potion, Hyper Potion, Poké Ball, Super Ball, Hyper Ball, Repousse, Super Repousse, Max Repousse, Antidote, Anti-Para, Réveil, Anti-Brûle, Antigel | Dons natifs via whitelist ; pool actuel de 14 consommables + Surf |
| Progression native protégée | Autres CS, billets/clefs, Colis, Thé, Poké Flûte, état scénaristique | Pas dans le pool, remise originale conservée ; audit avant extension |
| Techniques exclus | Métadonnées de sauvegarde, états internes des quêtes, données Yopple/Blasters/Aspirateur | Aucun objet AP ne les écrit |

Les consommables ne sont pas marqués progression. Aucune espèce ni évolution ne devient un objet AP dans cette version. Pas de piège. Une collecte ordinaire peut envoyer un objet de progression d’un autre monde ; les cinq seeds de test démontrent ce placement libre.

## Surf : règle conservée et dépendance nouvelle

`src/field_hm.c:FieldHMUnlocked` exige la CS et le cinquième badge. `FieldHMGetUser` exige un partenaire vivant, pas l’apprentissage de l’attaque. Ces fonctions sont intactes. Recevoir Surf ne donne pas le badge ni le flag du don Safari. Le don valide son propre check même si Surf a déjà été reçu ; il ne donne jamais un second exemplaire.

Le graphe AP regroupe la campagne native avant Surf dans une région. Les badges 7 et 8 et le Panthéon sont derrière Surf. Les six premiers badges et la Maison Secrète sont atteignables par la progression native sans Surf ; toutes leurs autres clefs restent en place. Il s’agit d’un modèle de possibilité finale, pas de l’ordre chronologique des étapes ni d’une mesure de temps. Les 13 checks logiquement ouverts sans objet AP ne sont pas 13 checks immédiatement ramassables : la cible initiale concrète repose sur les six collectes de la forêt, après les premiers événements natifs. Les déplacements manuels vers toutes leurs cases restent à vérifier.

La logique de remplissage empêche de placer Surf derrière l’accès maritime qui le requiert. Les tests de génération vérifient aussi que le Panthéon n’est pas accessible sans Surf. Ce modèle devra être détaillé avant de randomiser d’autres clefs : conserver un graphe permissif après leur suppression native pourrait produire des softlocks.

## Sources à tracer avant extension du pool

| Objet | Sources réelles et mécanisme | Point à protéger |
|---|---|---|
| Coupe | `data/scripts/philosovni.inc:Philosovni_Reward`, `src/philosovni.c:PhilosovniRefreshHM` | Don dans la quête personnalisée, état 3 et invitation à l’arène ; la possession peut déjà synchroniser `FLAG_GOT_HM01` |
| Vol | `data/maps/Route16_House/scripts.inc` | `FLAG_GOT_HM02`, accès natif à la maison |
| Surf | `data/maps/SafariZone_SecretHouse/scripts.inc` | **Implémenté** : flag de collecte distinct de la possession |
| Force | `data/maps/FuchsiaCity_WardensHouse/scripts.inc` | Échange du Dentier, consommation de l’objet et `FLAG_GOT_HM04` |
| Flash | `data/maps/Route2_EastBuilding/scripts.inc` | Test natif de collection : seuil 10 dans cette source ; `FLAG_GOT_HM05` |
| CS06–08 | `src/field_hm.c`, scripts d’îles et objets correspondants | Disponibilité pré-Ligue à vérifier avant tout ajout, ne pas importer la logique vanilla |
| Passe bateau | `data/maps/Route25_SeaCottage/scripts.inc` | Séquence de transformation et sortie de Léo |
| Poké Flûte | `data/maps/RocketHideout_B4F/scripts.inc:RocketHideout_B4F_EventScript_SilphScope` | Le script nommé SilphScope donne **la Flûte** dans ce fangame ; restauration automatique si absente |
| Clé Ascenseur | Même carte, script du sbire | Don visible après combat, accès à l’ascenseur |
| Carte Magnétique | `data/scripts/item_ball_scripts.inc`, carte Yopple/Silph | Portes et cinématiques associées à tracer |
| Clé Secrète | Même fichier, manoir de Cramois’Île | Arène et filtre/passé personnalisés à préserver |
| Thé | `data/maps/CeladonCity_Condominiums_1F/scripts.inc`, quatre guérites | Consommation par le premier garde puis ouverture partagée |
| Colis de Chen | Boutique de Jadielle, laboratoire de Bourg Palette | Tutoriel et remise de départ protégés dans ce jalon |

Les règles d’utilisation natives des CS sont : Coupe/badge 2, Vol/3, Surf/5, Force/4, Flash/1, Éclate-Roc/6, Cascade/7, Plongée/8. La sortie sous-marine reste permise par le code pour éviter d’enfermer une ancienne sauvegarde. L’existence d’une règle ne prouve pas que la CS est nécessaire à la victoire.

## Victoire réellement tracée

La première finale personnalisée est dans `data/maps/PokemonLeague_ChampionsRoom/spiraton.inc`. Après le combat gagné, elle pose `FLAG_DEFEATED_CHAMP`, joue la sortie de Don et conduit au Panthéon. La scène du Panthéon appelle le script commun qui **efface** ce flag avant `EnterHallOfFame` : le conserver comme condition finale serait erroné.

`src/post_battle_event_funcs.c:EnterHallOfFame` pose `FLAG_SYS_GAME_CLEAR` avant la sauvegarde du record. `src/hall_of_fame.c:Task_Hof_TrySaveData` lance `TrySavingData(SAVE_HALL_OF_FAME)` ; `src/save.c:HandleSavingData` incrémente `GAME_STAT_ENTERED_HOF` et sérialise le jeu. La condition AP exige donc le flag de fin **et un compteur Panthéon positif**, puis un état sûr de l’overworld. Le client envoie `CLIENT_GOAL`. Elle n’exige ni Médallium complet ni activité postgame.

Tests : le flag seul échoue ; la vraie scène crée un record et le Goal survit à une reprise à froid. L’équipe et l’arrivée dans la salle sont préparées par fixture : cela ne remplace pas un test du combat final complet. L’intégrité des scripts finaux est également vérifiée par leur absence dans les fichiers modifiés.
