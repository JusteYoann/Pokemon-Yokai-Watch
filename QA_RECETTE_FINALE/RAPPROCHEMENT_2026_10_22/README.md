# Rapprochement sélectif — prologue et huit trophées

Branche de référence : `dev/reconstruction-finalisation`. Départ `855018780`. Autre chantier observé : `codex/reprise-scenario-2026-10-22`, initialement `bed91b6a7`, puis `65b62bd88` avec Azuria. Aucun merge global; aucune suppression de branche ni écrasement de son travail.

## Changements intégrés

1. Coexistence visible humains/Yo-kai, Matt présenté comme ami plutôt que petit-fils de Chen; rivalité amicale et objectif huit trophées.
2. Scène de remise d'une Yo-kai Watch récente avant le choix du partenaire, puis Médallium ancien au retour du colis. Aucune nouvelle table d'espèce, aucun nouvel objet mécanique ni format de sauvegarde.
3. Français du laboratoire complété: derniers textes anglais traduits et dernières mentions de Matt appelant Chen Papi supprimées, y compris dans les messages postgame. Identifiants techniques historiques conservés.
4. Contrôle explicite des huit indicateurs natifs à l'entrée de l'actuelle Ligue, en préparation du Temple. Toutes les conditions Sevii/National existantes du garde sont conservées après ce contrôle. Réévaluation à chaque approche plutôt qu'une autorisation mémorisée dans la carte.

Ces sources proviennent de deux commits de l'autre branche, avec adaptations locales documentées. **Aucun sprite de l'autre Codex ni changement d'équipe de Champion n'a été intégré.** Wyatt conserve notre équipe et ses récompenses. Les graphismes, tables de données, musique et cadrages sont contrôlés inchangés dans `NON_REGRESSION.json`.

## Tests

- Compilations publique et privée réussies; tailles/SHA dans `BUILD.json`. Privé31589579octets, sous32Mio,26OST conservées.
- `introduction/TEST_INTRODUCTION_MGBA.json`: introduction native par manette, choix Nathan/Katie, saisie réelle du prénom AA, aucune saisie du prénom rival, Matt fixe et arrivée dans la chambre.
- `prologue/TEST_PROLOGUE_MGBA.json`: six contrôles réussis sur les deux variantes, scènes natives montre/Médallium, retrait du colis, cinq Balls, menu et persistance Flash. Téléportations et variables de progression explicitement préparées; parcours et premier combat exclus de ce banc.
- `prologue/LARGEURS_LABO_INTRO_ACCES.json`:282lignes mesurées avec la police native, prénom de sept W et variables de quatorze W; toutes dans208pixels. Cela ne signifie pas que toutes les pages ont été relues visuellement.
- `acces/TEST_ACCES_TEMPLE_MGBA.json`:256combinaisons de trophées, huit franchissements réellement refusés pour un trophée manquant différent, recul sûr, Flash et passage effectif avec les huit. La première salle reste celle de la Ligue actuelle: **ce test ne valide pas un Temple déjà construit**.
- `starters/TEST_TROIS_STARTERS_MGBA.json`:six branches de test (trois starters × deux protagonistes). Chaque partenaire est réellement donné par la Ball sélectionnée au niveau5, sans injection de créature/statistique/capacité; Matt reçoit la variante attendue. Combat déclenché en marchant vers la sortie, retour au terrain, soins et sauvegarde/rechargement du choix. Les six combats se terminent par une défaite avec la stratégie volontairement élémentaire « répéter la première attaque »; la progression fonctionne. Ce résultat ne valide ni une stratégie gagnante ni l'équilibrage du tutoriel, qui reste à revoir en recette.
- Les captures de la montre, du laboratoire après Médallium, du refus d'accès et de la présentation de Matt ont été ouvertes et examinées. Les scènes sont des captures du moteur, pas des compositions graphiques.

Commandes après activation de l'environnement:

```sh
export YOKAI_QA_ROM="$PWD/pokefirered_audio.gba"
export YOKAI_QA_ELF="$PWD/pokefirered_audio.elf"
python3 tools/yokai/tester_prologue_scenario_mgba.py
python3 tools/yokai/tester_acces_temple_mgba.py
python3 tools/yokai/tester_textes_prologue_mgba.py
python3 tools/yokai/tester_trois_starters_prologue_mgba.py
YOKAI_INTRO_QA_DIR="$PWD/QA_RECETTE_FINALE/RAPPROCHEMENT_2026_10_22/introduction" python3 tools/yokai/tester_introduction_mgba.py
```

## Limites et suite

Chen est provisoirement conservé comme présentateur et interlocuteur: la répartition Steve/Bérénice du nouveau scénario n'est pas terminée, et aucun portrait non approuvé n'est imposé. Les chapitres Argenta/Azuria de l'autre branche doivent être rapprochés séparément. Pas de partie complète, de validation d'équilibrage, ni de preuve de collection151sur une sauvegarde. Les divergences créatives sont consignées avant toute reprise supplémentaire.

## Diagnostics du banc de test

Trois images `starters/diagnostic-pilote-*.png` sont conservées pour traçabilité: (1) les pressions A relançaient le dialogue de Chen après la fin de scène, (2) le banc utilisait à tort `gEnemyPartyCount` pour attendre une équipe de dresseur au lieu de lire ses membres natifs, (3) son trajet direct passait par la case occupée par Matt. Les corrections concernent uniquement le pilote: fin de texte avec B, vérification directe des six emplacements adverses, détour d'une case. Aucun assouplissement du comportement du jeu ni injection d'une équipe gagnante. Le dernier rapport couvre les six cas complets.
