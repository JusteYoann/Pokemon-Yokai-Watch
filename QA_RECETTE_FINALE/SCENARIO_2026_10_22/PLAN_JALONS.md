# Plan de jalons — nouveau pack, après combats

Chaque lot : reproduction -> source -> compilation publique/privée -> mGBA ciblé -> rapport -> commit et push. Aucun push sur master. Ne pas refaire les 151 dessins ni rétablir les tables historiques.

1. **A/B — Sécurisation et audit** : conserver le pack et ses confirmations, figer le point de départ, matrice des écarts, clone GitHub propre. Critère : sources conformes aux faits documentés, deux builds comparés octet à octet avec mêmes ressources privées externes.
2. **C1 — Argenta/Wyatt et sécurité texte** : réutiliser portraits et overworld approuvés, garder exactement l'équipe/CT/flags existants, adapter textes et profil. Raccourcir le texte de défaite en déplaçant les explications dans le dialogue de terrain. Critère : aucune écriture après tampon300, combat réel par contrôleur, trophée1, CT39 unique et reprise si sac plein, sauvegarde/rechargement. Pas de nouvelle quête musée.
3. **C2 — Fondation du scénario** : résoudre répartition Steve/Bérénice et ressources manquantes; retirer les contradictions invisibilité et Matt petit-fils. Définir registre des huit trophées et compatibilité sauvegardes, avant modification des flags. Les équipes nouvelles non spécifiées ne sont pas inventées.
4. **C3 — Arènes et Portes Mystères** : Azuria et Carmin avec branches de protagoniste, puis Yopple/Safrania et Parmanie. Tests entrée, défaite, victoire, récompense unique, réinteraction et rechargement. Conserver les caméos non concernés.
5. **C4 — Nouveaux chapitres** : Zombie Night/Alyzon, Terr'heure, Cramois passé. Verrous de sortie, pertes, réapparitions et retours à définir avant carte finale. Tester tous moyens d'évasion du passé.
6. **C5 — Jadielle et Temple** : huit trophées stricts, Zazel, quatre adversaires dans l'ordre, Agent X unique. Matt soigne avant Morleone; Morleone puis Soranaki sans soin entre phases. Valider d'abord le design des formes et équipes manquantes.
7. **C6 — Postgame et 151** : Limbes/Sanctuaire, Enma ancien grand-père; parcours d'obtention sur sauvegarde unique. Ne pas déclarer cette garantie sur la base du seul compteur statique.
8. **D/E — Recette et livraison** : traversées Nathan/Katie, checkpoints rechargeables, français, transitions musicales, animations, courbe XP et taille. Rebuild depuis GitHub, manifeste SHA et limites honnêtes. V1 non prête tant que P0/P1 subsistent.

Aucune durée calendaire fiable n'est annoncée avant résolution du scénario et des nombreuses ressources absentes. La date publique visée n'est pas un critère de validation technique.

## Point de reprise après Carmin / Océane

- Wyatt, fondation du prologue et contrôle des huit trophées, Azuria, puis Carmin/Ariane ont chacun un jalon publié avec tests ciblés (voir les dossiers dédiés). Leurs nouvelles équipes provisoires ne sont pas une validation globale de l’équilibrage.
- Usapyon décoratif a été retiré de Carmin à la demande du créateur (`292bd4fb0`), sans toucher à sa place dans l’équipe.
- La liaison native de l’Océane est maintenant testée : trois branches de Matt avec Nathan/Katie, CS01 réellement remise avant d’autoriser le départ, reprise après refus du sac, vraie cinématique et accès à l’arène par Coupe. Voir [rapport Océane](../OCEANE_2026_10_22/README.md).
- Prochain lot scénaristique : Portes Mystères / Dr Jobard, puis Yopple / Safrania. Bérénice comme donneuse de Coupe n’est pas encore intégrée; le capitaine actuel reste provisoire. Ne pas réintroduire les anciens castings Bérénice/Giraud Champions, ni annoncer le chapitre complet sur la seule base de ces correctifs de progression.
