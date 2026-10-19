# Traduction française intégrale — chantier en cours

Base avant traduction : `4672b88e19d02acbb068cc3106d24fb2521c9542`, branche `dev/reconstruction-finalisation`. Kanto, les identifiants, les équipes, les correspondances d'espèces, les ressources graphiques et les 26 OST sont conservés. Les noms propres géographiques existants ne sont pas renommés par cette mission.

## Lot 1 effectivement traduit et vérifié

461 messages de combat, puis interfaces principales et messages partagés. Les tables de travail sont dans `data/localisation/fr/` : combats, menus, PC/résumé, connexion/crédits, prix et messages communs. Les traductions nommées conservent exactement les variables et codes entre accolades ; seuls les textes et leur cadrage changent. Les libellés communs utilisent une liste explicite de chaînes complètes, excluant les noms des dresseurs, noms d'espèces et mots contextuels Easy Chat. Les noms d'attaques et talents déjà validés sont préservés.

Les noms des types sont localisés en conservant la limite native de six caractères, avec un point pour les abréviations : INSEC., SPECT., ÉLECT., TÉNÈB. Les modèles de descriptions de statuts et de talents en combat sont traduits ; les menus du Parc Safari aussi. Les crédits conservent les noms des auteurs et organismes et traduisent les fonctions, sans attribuer les créations originales à une autre personne.

Les messages d'obtention, échanges, PC, Pension, boutiques, soins, Surf, contrôles de Badges et évaluations du Médallium sont traduits. L'évaluation de Chen rappelle que le partage d'expérience est permanent : aucun changement de récompense ou de mécanique. La révélation du spectre utilise Castelius Max, conformément au SPECIES_MAROWAK réellement lancé par l'événement.

## Vérifications réalisées

- Compilation privée réussie avec les 26 OST : **31 272 243 octets**, sous 32 Mio. Empreinte et preuve que les modifications des sources sont textuelles : [PRESERVATION_LOT1.json](PRESERVATION_LOT1.json).
- mGBA : textes français réellement liés, encodage des accents, largeur native des libellés contrôlés, ouverture par commandes des écrans Médallium, équipe et Sac. [14 contrôles](interfaces/INTERFACE_FR_MGBA.json).
- mGBA : 14 messages affichés par le moteur de dialogue sur la carte, avec variables préparées. [Rapport](dialogues/TEST_MGBA.json), [captures](dialogues/PLANCHE.png). Ce sont des fixtures de rendu, pas un parcours des PNJ ni une validation de toutes les pages.
- Cadrage de 29 dialogues avec la police native et des bornes prudentes pour les noms et variables. Les menus à coordonnées fixes sont exclus du recadrage automatique. [Détails](CADRAGE_DIALOGUES.json).

Les captures ont été ouvertes et examinées. Une compilation et ces contrôles ciblés ne prouvent pas la traduction ni le bon cadrage de tous les écrans du jeu.

## Couverture et suite

[Inventaire initial](COUVERTURE_AVANT.json) : 11 727 chaînes potentielles, 5 047 candidates anglaises et 457 candidates japonaises. L'analyse inclut aussi des textes hérités inutilisés, des descriptions des espèces hors Médallium et des noms propres. Les nombres ne sont donc ni un pourcentage de traduction ni un compteur de répliques réellement accessibles.

[État courant](COUVERTURE.json) et [inventaire des chaînes](INVENTAIRE.csv) servent au suivi. La détection de langue est une heuristique : une chaîne non signalée n'est pas automatiquement française. Les objets générés depuis JSON et les textes inscrits dans des graphismes nécessitent une vérification distincte.

**La traduction complète n'est pas encore terminée.** Restent notamment les dialogues de cartes, les aides et tutoriels, les messages de la Salle Union, le journal de reprise, les descriptions/noms d'objets encore anglais et les mots Easy Chat accessibles. Les textes Yo-kai déjà en français doivent rester cohérents avec les scènes programmées. Les tests de parcours et le contrôle des fenêtres étroites se poursuivent avec les lots suivants.
