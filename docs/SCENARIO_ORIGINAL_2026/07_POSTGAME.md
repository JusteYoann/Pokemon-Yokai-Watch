# Postgame — contenu défini, réalisation à organiser

## Philosophie du postgame — VALIDÉ

Le jeu doit proposer un prolongement qualitatif mais **ne pas accumuler d'extensions superficielles**. Priorités : Limbes Éternelles, Paradis Divin, trois rencontres légendaires, Seigneur Enma sur Île 7, rematch de Nathaniel âgé (Michael âgé à confirmer) et petit caméo Domniscian. Redistribuer **deux ou trois Yo-kai existants** comme rencontres exclusives de chacun des deux grands donjons.

## 1. Limbes Éternelles

- Donjon sombre, souterrain, inspiré du système de **huit cercles** de l'Infinite Inferno de Yo-kai Watch.
- Le **plan détaillé est librement conçu par Codex** ; les captures et le plan de référence dans `REFERENCES_VISUELLES/LIEUX/LIMBES_ETERNELLES/` sont des inspirations, PAS des maps GBA à recopier pixel par pixel.
- Zone postgame, accessible après les crédits ; entrée précise dans Kanto **à décider** (petite cabane, trappe, grotte, etc., simple suggestion).
- **Soranaki au fond** pour un combat facultatif. Sa justification narrative doit préserver sa disparition de la fin principale ; « écho » ou « épreuve du sceau » restent des propositions.
- **Rencontres exclusives proposées** : Tristos, Sorcophage, Lulugubre. Vérifier chaînes d'évolution, disponibilité de chaque famille et historique des obtentions validées avant déplacement.
- **Wobblewok** : personnage du donjon d'origine, mais non validé comme boss additionnel dans notre fan game. Ne pas imposer sa présence.

## 2. Sanctuaire / Paradis Divin

- Ascension dans une zone céleste après ou indépendamment des Limbes (enchaînement exact À DÉCIDER).
- Apparence lumineuse et surnaturelle ; **ne pas confondre avec le Temple Céleste de la Ligue**.
- **Enma l'Ancien au sommet**, adversaire facultatif.
- Puisqu'il est mort avant le jeu, sa représentation (manifestation spirituelle, souvenir, test divin) **n'est pas encore décidée**. Pas de résurrection arbitraire.
- **Rencontres exclusives proposées** : Maître Nyada, Tata Aura, Castelius III. Vérifier obtentions historiques (Castelius III est déjà vendu Route 4 dans les règles existantes), évolution et impacts avant fixation. Une espèce n'est « exclusive » que si son unique voie d'obtention est réellement déplacée et si l'ensemble des 151 reste accessible.
- **Kat Kraydel** : boss du donjon d'origine, **non validé** comme boss additionnel de notre jeu.

## 3. Seigneur Enma — Île 7 des îles Sevii

**VALIDÉ comme nouvelle destination pour le combat facultatif contre le souverain.** À distinguer soigneusement du Yo-kai **Enma n°150 capturable** dans la ROM historique, qui a une rencontre fixe à la Caverne Azurée. Il s'agit de deux rôles techniques différents (dresseur/PNJ et espèce), et non de l'ajout d'une nouvelle espèce.

À intégrer : trouver un lieu thématique accessible sur l'Île 7, créer ou réaffecter son script de combat, préserver les sauvegardes et déterminer si les revanches sont répétables. L'ancien événement Enma **au Mont Braise** dans `data/yokai/cameo_enma.json` doit être migré sans supprimer la capture nº150 à la Caverne Azurée par erreur.

## 4. Trois rencontres légendaires fixes

- **Octorgone — Centrale électrique** : convergence entre les choix récents et les données du dépôt, peu de conflit de lieu.
- **Kyubi** et **Mademoaiselle** : CONTRADICTION EXPLICITE À ARBITRER avant modification. Les sources historiques du dépôt (`RECUPERATION_PROJET/sources_validees/REPARTITION_YOKAI_VALIDEE_CODEX.md`, `DEVELOPPEMENT_YOKAI.md`) donnent **Kyubi au Mont Braise** et **Mademoaiselle aux Îles Écume**. La présentation récente faite en conversation les a **inversés** (Kyubi aux Îles Écume ; Mademoaiselle au Mont Braise) sans confirmation explicite de l'inversion par le créateur. Ne pas écraser une rencontre statique tant que cet emplacement n'est pas confirmé.
- **Enma nº150 — Caverne Azurée** : rencontre ancienne active sous conditions dans le dépôt ; continuité exacte dans le nouveau récit à vérifier.

## 5. Nathaniel / Michael âgés — présent de Cramois'Île

Nathaniel âgé doit être **affrontable dans son arène au présent** après le scénario, dans la continuité alternative où il est toujours vivant. L'équivalent Michael âgé dans la route de Katie est cohérent mais **non explicitement validé**. Prévoir les sprites et dialogues selon les deux routes ; ne pas annoncer une double revanche si seul Nathaniel est approuvé.

## 6. Domniscian — caméo uniquement

Une scène amusante et brève, pas une quête majeure. Ancienne implémentation postgame : Domniscian + employés au 11e étage de la Sylphe SARL dans le dépôt ; conserver ou déplacer librement **après validation**, mais ne pas le nommer constructeur du Temple ou fournisseur des souhaits. Les références et sprites existent (`graphics/yokai_characters/domniscian/`).

## 7. Grille de vérification

| Contenu | Condition d'accès | Objectif | Statut |
|---|---|---|---|
| Limbes | Après Panthéon | Soranaki rematch | VALIDÉ concept, NON CODÉ nouveau scénario |
| Paradis Divin | Après Panthéon, séquence à choisir | Enma l'Ancien | VALIDÉ concept, carte NON CODÉE |
| Île 7 | Après Panthéon | Seigneur Enma | VALIDÉ nouvelle destination ; ancien événement ailleurs |
| Centrale | Condition de progression originale à réévaluer | Octorgone | VALIDÉ |
| Îles Écume / Mont Braise | À arbitrer | Kyubi / Mademoaiselle | CONFLIT de lieux |
| Cramois'Île présente | Après chapitre temporel et Panthéon | Nathaniel âgé | VALIDÉ |
| Sylphe ou lieu à choisir | Postgame | Domniscian caméo | VALIDÉ principe ; lieu ouvert |

## Équilibrage postgame

- Rematches et rencontres légendaires doivent rester obtenables sans objet d'échange ni condition inter-version.
- Niveaux, taux d'apparition, capacités, récompenses et éventuelles répétitions **non fixés**.
- Aucune boucle d'obtention permettant duplication involontaire de Yo-kai uniques.
- Garder une issue aux donjons depuis chaque étage, un système de retour et une sauvegarde reprise sans softlock.
