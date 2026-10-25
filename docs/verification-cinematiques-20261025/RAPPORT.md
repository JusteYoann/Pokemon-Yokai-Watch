# Vérification des reprises de contrôle après les cinématiques

**64 scènes contrôlées : aucun blocage constaté dans les scénarios testés.** Les contrôles sont exécutés sur la ROM mise à jour contenant le déplacement du Mafiamille et le nom SHORT ONI.

Le pilote rejoue les scènes existantes dans mGBA, avec leurs prérequis préparés sur des parties isolées et des équipes de test niveau 100. Il attend la fin du script, vérifie que les commandes sont déverrouillées, déplace réellement le joueur avec la manette et ouvre le menu START. Pour la Terr’heure active, la restriction de menu prévue est conservée ; pour la fin de la Ligue, le retour après les crédits est attendu. Ces contrôles ne constituent pas une aventure continue ni une preuve de toutes les combinaisons possibles de sauvegardes.

## Contrôles supplémentaires

- **Argenta** : huit arrivées réelles depuis la Route 2, quatre entrées pour chacun des deux personnages. Discours terminé, visite du Centre et du musée, sortie vers la Route 2 et retour : commandes et menu disponibles.
- **Anciens déclencheurs** : retours et déplacements pour garçon et fille après Argenta, Lavanville, l’enquête de Carmin, Cramois’Île, l’Océane, Yopple et les quatre salles du Conseil 4. Les scènes déjà terminées ne bloquent pas les passages.
- **Gorgouille** : approche, capture, K.O. et chemins déjà dégagés ; départ d’Alizon et reprise des déplacements vérifiés.
- **Titre** : animation de sept secondes, entrée dans le menu, retour au titre, nouvelle partie et sauvegarde/Continuer vérifiés.

Aucun correctif supplémentaire de script de cinématique n’a été nécessaire pendant cette vérification. Les erreurs de préparation du pilote de test ont été corrigées avant le bilan final : constantes de déclencheurs, états des visites et dresseurs déjà vaincus dans le postgame.

Les résultats détaillés sont dans [BILAN.json](BILAN.json), les rapports individuels ci-dessous, [Argenta garçon](argenta-0/TEST_MGBA.json), [Argenta fille](argenta-1/TEST_MGBA.json), [retours garçon](retours/garcon/TEST_MGBA.json) et [retours fille](retours/fille/TEST_MGBA.json). Les compléments de Gorgouille et du titre figurent dans leurs sous-dossiers.

| Scène | Résultat |
| --- | --- |
| 01-chen-depart | Validé |
| 01b-choix-partenaire | Validé |
| 01c-matt-laboratoire | Validé |
| 01d-medallium | Validé |
| 01e-tutoriel-capture | Validé |
| 02-argenta | Validé |
| 02b-matt-route22 | Validé |
| 02c-matt-azuria | Validé |
| 02d-chaussures | Validé |
| 02e-fossiles | Validé |
| 03-ariane-rencontre | Validé |
| 03b-matt-oceane | Validé |
| 03c-capitaine | Validé |
| 03d-depart-oceane | Validé |
| 04-enquete-entrepot | Validé |
| 05-zombie-night | Validé |
| 06-cramois-rencontre | Validé |
| 07-yopple-liberation | Validé |
| 07b-matt-yopple | Validé |
| 07c-matt-route22 | Validé |
| 08-finale | Validé |
| 09-terreur | Validé |
| 10-enma-postgame | Validé |
| 10b-chen-jibanyan | Validé |
| 11-nyada-premiere-quete | Validé |
| 12-nyada-retour-amis | Validé |
| 13-alizon-quete-oni | Validé |
| 14-alizon-rendez-vous | Validé |
| 16-nyada-seconde-quete | Validé |
| 17-demophage | Validé |
| 18-nyada-sommet | Validé |
| 19-scientifique-lavanville | Validé |
| 20-scientifique-carmin | Validé |
| 21-scientifique-yopple | Validé |
| 21b-chen-invitation | Validé |
| 22-yoann | Validé |
| 23-leo-transformation | Validé |
| 23b-leo-separateur | Validé |
| 24-repaire-morleone | Validé |
| 25-champion-don-exil | Validé |
| 26-lorelei-grotte | Validé |
| 27-perdue-sauvetage | Validé |
| 28-depart-sevii | Validé |
| 28b-motards-argument | Validé |
| 28c-motards-depart | Validé |
| 29-retour-sevii | Validé |
| 30-saphir-vol | Validé |
| 31-entrepot-admin1 | Validé |
| 32-entrepot-admin2 | Validé |
| 33-entrepot-scientifique | Validé |
| 34-celio-rubis | Validé |
| 35-celio-saphir | Validé |
| arene-01 | Validé |
| arene-02 | Validé |
| arene-03 | Validé |
| arene-04 | Validé |
| arene-05 | Validé |
| arene-06 | Validé |
| arene-07 | Validé |
| arene-08 | Validé |
| conseil-01 | Validé |
| conseil-02 | Validé |
| conseil-03 | Validé |
| conseil-04 | Validé |

Empreinte de la ROM : `41d62f157ef47859eb52bd88718861f8fc22eca5e1d64d1846734589e32537dd`.
