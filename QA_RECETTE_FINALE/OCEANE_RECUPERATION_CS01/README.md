# Récupération de Coupe sur une ancienne sauvegarde

Le jalon précédent empêchait de nouveaux départs de l’Océane sans CS01, mais ne réparait pas les sauvegardes déjà affectées. Le marin existant du port de Carmin peut maintenant remettre la récompense manquante, y compris après le départ du bateau.

## Conditions exactes

- `FLAG_GOT_HM01` doit déjà être défini : aucun accès anticipé à Coupe.
- `ITEM_HM01` doit être réellement absent du sac.
- Le résultat réel d’`additem` est contrôlé. Si la Boîte CT ne peut pas être créée faute de place, le marin attend que le joueur revienne; aucun autre drapeau n’est modifié.
- Après remise, le contrôle de présence de la CS empêche tout doublon, y compris après sauvegarde/rechargement.

La récupération fonctionne en parlant au marin et par chacune des deux cases de contrôle du quai. Après récupération ou refus du sac, ces deux contrôles reprennent le déplacement natif vers le haut du quai. Une interaction suivante conserve les destinations Sevii normales. Aucun PNJ, objet de quête, prix, combat ni format de sauvegarde ajouté.

## Vérifications natives

`tester_recuperation_cs01_mgba.py` : **14 cas mGBA réussis** avec Nathan et Katie : six réparations aux trois états Sevii (0,1,5), deux refus du sac plein suivis de libération de place et réessai, deux gardes sans ancien drapeau de récompense, quatre accès par les deux cases du quai avec réinteraction sans doublon. Les quatre menus Tri-Passe/Passe Prisme sont réellement affichés puis annulés par B; la progression des ferries reste inchangée.

Les sauvegardes testées sont des **fixtures explicites** reproduisant l’état ancien déjà constaté : récompense déclarée obtenue, bateau parti et CS absente. Les appels natifs Flash et Continuer sont effectués, avec préparation de `SaveMapView` et contrôle du terrain conservé. Aucun fichier de sauvegarde réel du joueur n’a été fourni; aucune partie complète n’est revendiquée.

Le sous-dossier `obtention-normale/` réexécute séparément les six cas natifs capitaine/remise/départ du jalon précédent sur cette ROM. Les sorties sont isolées pour conserver les anciens rapports avec leur empreinte historique.

Les nouveaux textes sont mesurés dans la police native, avec un prénom joueur de 7W, limite 208px. Les captures du port et des menus de ferry sont ouvertes pour inspection. Les deux compilations passent; profil privé 31 589 579 octets, sous 32 Mio. Les 26 OST, données des espèces, équipes, statistiques, sprites et règles shiny ne sont pas modifiés. Voir `BUILD_NON_REGRESSION.json` pour les empreintes et la liste des deux fichiers actifs modifiés.

```sh
source /workspace/.setup/env.sh
YOKAI_QA_ROM=$PWD/pokefirered_audio.gba YOKAI_QA_ELF=$PWD/pokefirered_audio.elf python3 tools/yokai/tester_recuperation_cs01_mgba.py
```

## Portes Mystères : décision en attente

Le chapitre n’est pas ajouté par ce correctif. Le pack décrit l’alliance puis la trahison du Dr Jobard à Carmin/Yopple et le rôle de Bérénice, mais ne fournit pas de déroulé précis des épreuves ni de sprite identifié du Dr Jobard. Le dépôt contient le scientifique générique de Rouge Feu, pas un dessin approuvé du personnage. Une question a été soumise au créateur : autoriser un premier prototype explicitement provisoire avec ce scientifique et de petites salles réversibles, ou attendre le déroulé/design. Aucun remplacement artistique ni chapitre improvisé n’est activé avant cette réponse.

## Reproductibilité GitHub

Le clone indépendant utilisé pour les précédentes compilations propres a été avancé depuis GitHub jusqu’à `a50fd9fb3`, puis recompilé avec ses propres objets. Les ROM publique et privée sont identiques octet par octet à celles testées. Aucune source ou objet local du dépôt de développement n’a été copié; la version privée utilise les mêmes ressources audio externes. Résultats dans `REPRODUCTIBILITE.json`.

Pour rejouer les six contrôles de remise normale sans écraser le rapport historique, avec les variables ROM/ELF ci-dessus définies :

```sh
PYTHONPATH=tools/yokai python3 - <<'PYTEST'
import tester_oceane_progression_mgba as q
q.OUT = q.ROOT / 'QA_RECETTE_FINALE/OCEANE_RECUPERATION_CS01/obtention-normale'
q.OUT.mkdir(exist_ok=True)
assert len(q.captain_cases()) == 6
PYTEST
```
