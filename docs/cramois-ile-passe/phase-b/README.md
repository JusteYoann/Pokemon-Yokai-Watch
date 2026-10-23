# Phase B — frontière temporelle maritime

**Implémentation technique terminée, rendu visuel proposé pour approbation. Phase C non commencée.**

Branche : `feature/cramois-ile-passe`. Base validée : `1f335d268`. Audit : `ffcb45377`. Code : `fb28a6add`. Aucun merge sur master.

## GIF et captures natives

- **[Arrivée à Cramois'Île — Route 20](public/arrivee-route20.gif)** : mer normale, entrée progressive, nuages denses, dissipation et île sépia.
- **[Départ vers Kanto — Route 20](public/depart-route20.gif)** : île sépia, traversée inverse, mer normale.
- [Arrivée par le nord](public/arrivee-route21.gif) et [départ par le nord](public/depart-route21.gif). Le trajet contourne réellement les rochers et îlots. Les Dresseurs ne sont pas désactivés ; une rencontre peut interrompre le parcours selon leurs déplacements, avec combat natif conservé dans l'enregistrement.
- [Mer avant la brume](public/mer-avant-brume-x4.png), [entrée](public/entree-brume-x4.png), [densité maximale](public/brume-dense-x4.png), [sortie](public/sortie-brume-x4.png), [arrivée sépia](public/arrivee-sepia-x4.png), [retour vers Kanto](public/retour-kanto-x4.png).
- [Menu dans la brume](public/menu-dans-brume-x4.png), [Sac sans brume](public/sac-sans-brume-x4.png), [combat maritime sans brume](public/combat-mer-sans-brume-x4.png), [arrivée par Vol](public/vol-arrivee-x4.png).

Les PNG natifs font 240 × 160 ; les agrandissements utilisent le plus proche voisin. Les GIF enregistrent les images de mGBA à environ quinze images par seconde, sans recolorisation ajoutée après capture ni simulation graphique. Les mêmes fichiers et tests de la version privée sont dans [prive](prive).

## Comportement intégré

La brume blanche/grise ne se déclenche qu'en Surf sur deux bandes locales : Route 20, colonnes 2 à 18 sur 120 ; Route 21 Sud, lignes 30 à 46 sur 50. L'opacité augmente vers le centre puis diminue, avec lissage entre les cases. Le mouvement inverse ou un demi-tour réutilise la même progression spatiale. Il n'y a ni dialogue ni confirmation.

Les nuages défilent lentement. Ils réutilisent la texture horizontale native de Rouge Feu et une palette grise propre, indépendante des ressources météo et de la teinte verte de Lavanville. Le système n'écrit pas la météo sauvegardée et ne remplace aucun Dresseur, objet, événement, terrain ou collision.

Du côté intérieur de la frontière, les dernières cases maritimes prennent progressivement le sépia sous la brume. Elles possèdent déjà la teinte de l'île au raccord de cartes : l'aller et le retour évitent ainsi un changement brutal visible à la limite. Cette interpolation reste locale aux deux bandes et à leurs quelques cases côté île. Le traitement déjà validé des treize cartes de Cramois, de leurs intérieurs et de leurs combats est inchangé.

Il n'y a aucun nuage sur Cramois ou ses intérieurs. Les ressources temporaires sont libérées à la sortie et lors des changements de contexte. Les menus plein écran et les combats ne reçoivent pas la brume. Le retour sur la carte recrée l'effet uniquement si le joueur se trouve encore dans la bande en Surf. Vol, Téléport, Tunnel et Corde Sortie utilisent leurs effets natifs et arrivent directement dans le bon état visuel, sans traversée maritime imposée.

## Tests des deux versions

[Résumé et empreintes ROM](VALIDATION.json) · [Rapport public](public/TEST_MGBA.json) · [Rapport privé](prive/TEST_MGBA.json) · [Préservation](PRESERVATION.json) · [Compilation publique](COMPILATION-public.txt) · [Compilation privée](COMPILATION-prive.txt).

Pour chaque version, les contrôles exécutés dans mGBA couvrent :

- Traversées au contrôleur des vraies connexions Route 20 / Cramois et Route 21 Sud / Cramois, dans les deux sens.
- Trois demi-tours et passages répétés, avec quinze sprites au maximum et libération complète après chaque sortie.
- Save/Continue dans la brume et sur l'île ; Sac, menu et retour sans duplication de sprites.
- Rencontre sauvage engagée depuis la brume, combat sans brume et retour à l'effet local après victoire.
- Absence de brume sur chacune des treize cartes et véritable sortie par la porte du Centre.
- Effets natifs de Vol et Téléport depuis la zone dense vers Cramois ; entrée réelle du Manoir puis sorties natives par Corde Sortie et Tunnel.
- Nouveau passage maritime avec le drapeau postgame comme fixture.
- Réexécution des **40 contrôles de phase A** : sépia, intérieurs, combats, interfaces, victoire de Nathaniel et Badge Volcan, variante Michael, couleurs normales ailleurs et effet nocturne d'origine de Lavanville.
- Réexécution des **14 régressions Ariane** : suivi, rappels, Save/Continue, entrepôt, duo avec Usapion, fuite des sbires, Coupe et fin du suivi.

Les rapports détaillés restent dans [régressions de phase A](regressions/phase-a) et [régressions Ariane](regressions/ariane). Ils portent l'empreinte exacte de la nouvelle ROM ; les anciens rapports de phase A n'ont pas été écrasés.

## Mémoire et ressources

| Mémoire statique | Phase A | Phase B | Écart |
|---|---:|---:|---:|
| EWRAM, publique et privée |261348 octets|261368 octets|+20|
| Marge EWRAM |796 octets|776 octets|−20|
| IWRAM publique |29824 octets|29824 octets|0|
| IWRAM privée |29888 octets|29888 octets|0|

La brume utilise temporairement quinze emplacements de sprites déjà préalloués par le moteur, 2048 octets de tuiles en VRAM et une banque OBJ de seize couleurs. Elle n'ajoute aucun format de sauvegarde ni grosse allocation permanente. La table sépia de 64 Kio existante est partagée par un nouvel accesseur en lecture seule ; ses données et les fonctions précédentes de phase A sont conservées exactement.

Les 5821 PNG/palettes approuvés, les 1880 fichiers de cartes/layouts, les 151 Yo-kai, les équipes, les dialogues, le quiz et les scripts préexistants sont inchangés. Les 31 flux audio privés sont vérifiés à leur emplacement réel dans la ROM. Les sources de Carmin, du duo, d'Ariane, de Lavanville, de la Mafiamille et de la finale restent identiques. Aucune ROM ni musique privée n'est publiée.

## Contraintes, fixtures et éléments non vérifiés

La GBA ne mélange pas deux plans OBJ entre eux. Les nuages passent donc derrière les acteurs, dont les palettes sont éclaircies progressivement pour conserver leur lisibilité dans la brume. Les fenêtres de dialogue et menus restent devant. Le mélange alpha matériel est local aux routes à météo calme ; le moteur reprend ses registres lors du retrait. Les fondus et la désactivation native des transferts de palette sont respectés. Les buffers de palettes ne sont pas recolorés : chaque image repart des couleurs originales.

Les fixtures commencent par une vraie nouvelle partie, placent le joueur, renforcent son équipe et donnent 250 pas de Repousse. Melissa est réellement battue avant de filmer son couloir maritime ; aucun PNJ n'est supprimé et aucun drapeau de victoire n'est forcé. Le trajet nord est calculé depuis les collisions et les terrains d'eau originaux, puis parcouru par les touches. Les éventuels autres combats de Dresseurs utilisent également le contrôleur. Les PV ennemis et les issues ne sont pas modifiés.

Les tests des déplacements spéciaux exécutent leurs véritables animations et chargements, avec destinations explicitement préparées. Ils ne prouvent pas l'obtention des CS, les badges nécessaires, le choix depuis tous les menus de Vol ou la consommation d'un objet Corde Sortie depuis le Sac. La résurrection des fossiles et le puzzle complet du Manoir jusqu'à la Clé ne sont pas rejoués ici ; leurs sources, cartes et événements restent inchangés. Le postgame est testé avec un drapeau de fin comme fixture, sans prétendre avoir rejoué la Ligue dans cette phase.

Le moteur s'abstient d'afficher la brume lorsqu'une autre météo utilise le mélange. En cas de manque de sprites, de palette ou de VRAM, les ressources partielles sont libérées et l'effet réessaie sans supprimer d'acteur existant ; cette saturation n'a pas été injectée artificiellement dans les tests. Les deux corridors maritimes usuels sont vérifiés ; les usages inhabituels et toutes les combinaisons de menus/effets ne constituent pas une couverture exhaustive. Pas de validation sur GBA physique ni de nouvelle certification d'écoute des musiques.

**Arrêt après la phase B pour approbation visuelle. Aucun dialogue ni quiz de phase C n'est intégré.**

[Audit préalable](AUDIT.md) · [Demande de phase B](DEMANDE.md) · [Plan global](../PLAN.md).
