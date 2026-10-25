# Seigneur Enma : taille et retrait du Mont Braise

Le Seigneur Enma reprend le modèle royal créé pour les caméos, conservé dans le commit `3abcd3586`. Son image est adaptée par échantillonnage au plus proche voisin, sans changer ses proportions : **12 pixels de largeur visible comme Nathan**, avec **21 pixels de hauteur frontale contre 19 pour Nathan**. Les trois orientations et la palette overworld dédiée sont conservées. Le portrait de combat reste inchangé. Les conversions du dépôt préservent désormais cette sélection approuvée sans nouveau redimensionnement.

L’Enma à côté de Gorgouille était l’ancien PNJ de défi postgame au Mont Braise. Il est maintenant masqué à chaque entrée et retiré lors des retours terrain, y compris lorsqu’un ancien objet était déjà chargé. Son emplacement interne et ses scripts sont conservés pour ne pas déplacer les identifiants des autres personnages. Gorgouille et Alizon Bie restent présents selon les conditions habituelles. La rencontre capturable d’Enma reste dans la Grotte Azurée et ne dépend pas d’une victoire contre cet ancien caméo.

Les deux souvenirs de l’introduction du postgame ont également été recapturés avec Enma à sa nouvelle taille.

[Tests ciblés mGBA](TESTS_MGBA.json) : absence au Mont Braise avant et après la Ligue, présence de Gorgouille et d’Alizon après leurs prérequis, retrait d’un ancien objet chargé, ressource et palette natives d’Enma dans la Grotte Azurée, largeur comparée à Nathan, introduction postgame conservée. Les tests emploient des parties isolées préparées ; aucune sauvegarde utilisateur n’est ouverte ou modifiée.

[Enma dans la Grotte Azurée](enma-grotte-azuree-x3.png) · [Mont Braise corrigé](mont-braise-gorgouille-alizon-x3.png) · [ROM](Pokemon_Yokai_Watch_Beta_0.1_Enma_Corrige.gba).

Cette ROM conserve le nouvel écran titre fourni dans `3aea66407`. Aucun format de sauvegarde ni aucune musique n’a changé. Branche dédiée, aucune fusion sur master.
