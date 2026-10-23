# Ariane accompagne le joueur

Branche : `feature/pierre-philosovni-carmin`. Code : `a1f84a20d`. Aucun merge sur master.

Usapion n'a plus d'acteur sur les cartes : quai de Carmin, entrepôt et Route 25. Ses ressources validées restent archivées et son rôle de partenaire dans le combat duo est conservé.

Ariane suit automatiquement le joueur dès l'acceptation du premier dialogue d'enquête. Elle reprend les cases parcourues, suit les virages et laisse passer le joueur lors d'un demi-tour. Le suivi reprend aux portes et après Save/Continue. Il cesse à la conclusion de l'enquête ; Ariane retrouve alors son Arène.

Après 300 images de jeu sans déplacement, environ cinq secondes, Ariane indique la destination. Le rappel n'est déclenché qu'une fois par arrêt : il faut se déplacer pour le réarmer. Menus, dialogues, transitions et combats suspendent le compteur. Sur le quai, elle indique la cabane ; dans l'entrepôt, les voix des sbires ; ailleurs, le retour à Carmin. Si la remise de Coupe attend une place dans le sac, elle le rappelle à la place.

## Captures natives mGBA

- [Suivi en mouvement, virages et demi-tours — GIF](public/suivi-mgba.gif).
- [Ariane et Nathan sur le quai](public/suivi-x4.png).
- [Rappel automatique après cinq secondes](public/rappel-cinq-secondes-x4.png).
- [Entrée dans l'entrepôt](public/entrepot-x4.png).
- [Rappel à l'intérieur](public/rappel-entrepot-x4.png).
- [Fin de l'enquête](public/fin-x4.png).

PNG natifs 240 × 160 ; agrandissements au plus proche voisin. Les GIF sont des images enregistrées dans mGBA, sans audio. Les mêmes vérifications et captures figurent dans [prive](prive).

## Vérification

[Résumé et empreintes](VALIDATION.json) · [Tests publics](public/TEST_MGBA.json) · [Tests privés](prive/TEST_MGBA.json) · [Préservation](PRESERVATION.json).

Les deux versions compilent. Pour chacune : 14 contrôles fonctionnels mGBA et mesure de 201 lignes avec la police GBA, sans dépassement. Les contrôles comprennent l'acceptation réelle, les pas au contrôleur, les virages et demi-tours, le rappel automatique et son absence de répétition, une pause dans le menu, Save/Continue sur le quai et dans l'entrepôt, une véritable entrée par la porte, le dialogue avec le compagnon, le combat duo gagné, la fuite des deux sbires, Coupe et la fin du suivi. Un cas complémentaire vérifie une récompense en attente après voyage et sauvegarde, sans supprimer d'autres PNJ.

Les fixtures partent d'une nouvelle partie, placent le joueur et renforcent son équipe pour le test de combat. Elles n'altèrent ni les ennemis, ni leurs PV, ni l'issue du combat. Le cas de récompense après voyage utilise explicitement l'état d'attente 2. Cela ne représente pas une traversée complète de Kanto ni un nouveau test d'équilibrage.

Les 5821 PNG/palettes validés restent identiques, ainsi que les données des 151 Yo-kai, les équipes préexistantes et les 31 flux audio privés. Sur Route 25, seule la suppression de l'acteur Usapion est autorisée par la comparaison ; le script secondaire d'Ariane reste intact. Les précédents parcours complets Champions/Lavanville/finale restent documentés avec leurs anciennes empreintes dans le dossier historique ; ils ne sont pas présentés comme rejoués pour cette modification.

## Intégration et limites

Aucun sprite ni palette n'a été redessiné. Le moteur déplace les poses existantes d'Ariane ; aucun nouveau cycle graphique de marche n'est inventé. La présence du compagnon dépend de l'état de quête déjà sauvegardé, sans agrandir le format des sauvegardes. Les anciennes sauvegardes des trois cartes sont réconciliées avec les nouveaux acteurs. Les identifiants des deux sbires ont été corrigés après suppression d'Usapion.

Le suivi utilise une file des dernières cases du joueur, un acteur dynamique et une banque de palette libre parmi les banques PNJ/reflets 7 à 11. Il réutilise les mouvements, collisions et sauts natifs ; le joueur peut passer devant Ariane pour éviter de bloquer les passages. Lors de Surf, elle est masquée et le suivi reprend sur terre. Si les 16 emplacements d'acteurs sont occupés, le système attend un emplacement libre sans supprimer de PNJ ; si le chemin est perdu ou la file déborde, il replace le compagnon sur une case adjacente accessible. Ces cas de secours, Surf et toutes les connexions possibles de Kanto n'ont pas fait l'objet d'une validation exhaustive.

Ajout RAM : 116 octets. EWRAM totale 261348 octets, 796 libres ; IWRAM 29824 publique / 29888 privée. Les compilations et les empreintes des ROM sont fournies sans publier de ROM ni de musique privée.
