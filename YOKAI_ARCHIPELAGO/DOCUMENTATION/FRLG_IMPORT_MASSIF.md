# Import classique massif — 16 novembre 2026

**625 checks actifs par défaut, soit 551 de plus que le jalon74.** Avec l’option Terr’heure historique :626. Aucun nouvel événement exclusif Yo-kai ajouté. Les74 identifiants précédents sont conservés (fixture de régression figée).

La référence est le monde FRLG1.1.5 de Vyneras/Archipelago, branche `frlg-stable`, commit `3d1359cf0606cee11eebfecc0d820063bef7c2a2`. Seules ses métadonnées MIT sont réutilisées, avec attribution dans `THIRD_PARTY/FRLG_LICENSE.txt` et le package. Aucun patch binaire vanilla ni code C sans licence explicite importé.

Sur **1715 emplacements examinés** :195 compatibles directement,428 adaptations terminées,843 restant à adapter,249 absents/incompatibles. Cela donne **623 emplacements classiques intégrés**, plus les deux checks Yo-kai déjà présents. Le classement « à adapter » du JSON inclut les428 terminés : filtrer `integrated` et `adaptation_complete` pour distinguer les travaux restants.

| Catégorie originale | Examinés | Intégrés | À adapter encore | Absents/incompatibles |
|---|---:|---:|---:|---:|
| Mémorial | 96 | 0 | 96 | 0 |
| Objets cachés | 184 | 60 | 63 | 61 |
| Dons, CS et badges | 87 | 17 | 34 | 36 |
| Objets au sol | 190 | 111 | 12 | 67 |
| Captures | 386 | 166 | 135 | 85 |
| Boutiques | 166 | 0 | 166 | 0 |
| Visites | 20 | 13 | 7 | 0 |
| Dresseurs | 456 | 256 | 200 | 0 |
| Revanches | 130 | 0 | 130 | 0 |

Les checks actifs comprennent111 objets au sol,60 objets cachés,1 don Surf,5 assistants Chen,3 autres dons,256 dresseurs,166 captures,13 visites et8 badges, plus les deux événements Yo-kai conservés.

## Détection et sauvegarde

- Objets/dons : véritables scripts natifs, flags de remise persistants ; récompense originale supprimée uniquement pour les sources randomisées. Les autres objets de scénario restent natifs.
- Dresseurs : hook `CB2_EndTrainerBattle` après les sorties spéciales Blasters/Terr’heure ; seul `B_OUTCOME_WON` appelle `YokaiAPTrainerVictory`. Les flags de gym/Vs Seeker ne créent jamais de victoire AP. `SetTrainerFlag` conserve disponibles les dresseurs AP non vaincus lorsqu’un script veut les passer automatiquement après le badge/quiz.
- Un registre séparé utilise les32 octets auparavant réservés de la structure AP64octets, sans changer la version1 ni déborder SB2+0xE20..0xE5F. **Capacité256 groupes de dresseurs**, pas assez pour importer tous les456 sans nouvelle étude de sauvegarde. Les variantes de starter partagent un groupe.
- Captures : `GetSetPokedexFlag(n, FLAG_GET_CAUGHT)` ; une espèce seulement vue ne valide rien. L’inventaire repose sur les tables d’apparition natives, les six substitutions pré-Panthéon, un sous-ensemble prouvé des rencontres supplémentaires et les évolutions naturelles. Aucune hypothèse sur les cadeaux aléatoires, échanges ou pierres. Le compteur Chen reste celui des premières151 entrées nationales :23 disponibles sans Flash,59 avec Flash avant Surf,101 après Surf selon les témoins retenus. Ces capacités sont une possibilité de capture, jamais une substitution au compteur réel.
- Visites : `MapPreview_SetFlag` depuis les scripts natifs de transition. Ouvrir une boutique ne compte pas comme achat.
- Transport3 : bitmap128octets et catalogue SHA256 partagé ROM/package/seed. Calcul intermédiaire sur la pile avant publication pour éviter un bitmap vidé pendant le scan. ABI48octets et sauvegarde1 conservées.
- Le client et le serveur traitent les IDs de façon idempotente ; après reconnexion, le jeu peut renvoyer l’ensemble sauvegardé sans nouvelle récompense. La sauvegarde normale reste nécessaire avant de fermer.

## Logique et limites

Surf et Flash sont les deux capacités randomisées. Les autres clefs, badges et étapes narratives restent natives. Les régions de référence sont conservées comme catégories de lieux, mais le graphe utilise trois étapes de capacités (`native_early`, `flash`, `surf`) : ce n’est pas une transplantation complète des accès vanilla ni une mesure des durées de jeu. Les checks d’Argenta à Jadielle ne supposent pas tous une accessibilité immédiate ; les étapes natives restent à jouer. L’arène de Jadielle est bien dans l’étape Surf/badge7.

Îles, Grotte Inconnue, bateau manquable et sources sans preuve pré-Ligue ne sont pas activés. Les apparitions additionnelles réservées au passé, à une position, ou à un jet de rareté supplémentaire ne servent pas de témoins d’accès. Les boutiques demandent un vrai hook de transaction ; les revanches un registre par palier ; le Mémorial une correspondance précise avec l’état des entrées. Ces catégories ont été examinées mais ne sont pas fonctionnelles. Terr’heure reste désactivée par défaut et exclut progression/pièges.

Une nouvelle seed, une nouvelle partie et le package issu du même build sont nécessaires. Se connecter **avant les premières collectes et combats** : les anciens flags dresseurs ne permettent pas de distinguer une vraie victoire des validations automatiques. Aucune migration arbitraire de seed existante. Les tests de génération concernent trois mondes ; le Multiworld à cinq jeux, le parcours intégral et l’interface Lua Windows restent à valider.

## Reproduire

Voir le [guide français](GUIDE_FIRERED_ARCHIPELAGO_FR.md). Le script `SCRIPTS/build_firered.sh` vérifie le snapshot RC1 complet puis applique les générateurs sans modifier le fangame principal. La racine vanilla de ce dépôt ne convient pas.

Source complet local : branche `codex/firered-classic-bulk-20261116`, commit `d287d375cd253f8a729581f884768d3811b1e549`, depuis RC1 `a589cf0057fd0f579d003d8dd58616b3f4649ea2`. Les binaires hôtes du compilateur ne sont pas inclus dans ce commit. ROM SHA256 : `1af5821cc9d03a744b125fe9281c95208e5dfe7fd27c1c2b8f65a5ab7464ee56`. Aucune ROM, sauvegarde ni ressource graphique privée publiée.

Le [fichier de correspondance complet](CORRESPONDANCE_CLASSIQUE_COMPLETE.json) expose les1715 lignes, IDs originaux et Yo-kai, scripts/cartes/témoins et motifs de désactivation. Générateurs : `PATCHES/pokemon_yokai_firered/expand_checks.py`, `bulk_import.py`, `prepare_source.py`. Tests et résultats : `TESTS/verify_firered_expanded.py`, `verify_firered_native.py`, `verify_firered_network.py`, `verify_multiworld_generation.py` et [preuves](preuves/).

## Résultats exécutés sur cette ROM

- **617 IDs de détecteurs** vérifiés dans mGBA, soit toutes les entrées actives hors badges et Terr’heure optionnelle ; **2057 assertions**, dont la conservation de chacun après sauvegarde native, destruction/recréation du cœur et Continuer. Les visites passent par les chargements réels de cartes ; objets/cadeaux par leurs scripts réels. Les256 victoires utilisent le handler C avec fixtures, les166 captures le getter/setter natif avec cohérence vu/capturé. Cela ne prouve pas256 combats ni166 captures joués.
- **36 contrôles réseau** réussis avec MultiServer, client officiel et mémoire réelle mGBA. Wyatt et un dresseur ordinaire (Route3, Colton) sont combattus par le moteur avec touches simulées, sans injecter victoire/flag. Les checks sont acquittés par le serveur, y compris les captures préparées par fixture ; un reset de flag dresseur ne renvoie pas le check. Dons distants, reconnexion, sac plein et Goal Panthéon passent. Le contexte d’interaction, l’équipe et les déplacements restent des fixtures.
- **37 protections natives** réussies (seed/slot, compteur, répétition, états occupés, journal, sac plein, sauvegarde froide).
- **5 seeds réelles à trois mondes** générées et résolubles selon le modèle déclaré :3 par défaut avec625 checks,2 avec Terr’heure et626 checks. Aucun objet indispensable sur l’option aléatoire.
- **32 tests unitaires réussis sur40 découverts** ;8 tests Emerald simulés restent ignorés faute des variables de fixture, chantier gelé. Contrats des74 IDs, unicité/borne du registre, exclusion du postgame et couverture des9 catégories vérifiés.

**618 checks distincts ont une preuve de détection native**, dont le badge Wyatt. Les7 autres badges sont conservés et raccordés mais pas rejoués dans cette campagne. Cela correspond à616 checks classiques et2 événements historiques Yo-kai. Le parcours physique complet de chaque emplacement et une partie intégrale restent à tester.

La reconstruction propre utilise une copie neuve du snapshot vérifié, sans objets ni dossier `build`. **Ne pas employer `make clean` sur ces entrées** : la règle vanilla supprime aussi des ressources binaires livrées comme sources, notamment les palettes Zombie Night, puis leur régénération générique ne retrouve pas le format16 couleurs. Un essai de cette méthode a échoué ; le script de copie/compilation fourni conserve les entrées du manifeste et reconstruit correctement tous les objets.
