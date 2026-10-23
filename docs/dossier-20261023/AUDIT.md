# Audit initial — 23 octobre 2026

Branche dédiée `feature/dossier-ligue-yopple-20261023`, base `0fa1808fe55b87d9837ba90e33485dbcc089a8e3`. Aucun merge. Les corrections de Cramois (dont sépia constant) sont déjà dans cette base et doivent rester intactes.

## Décisions reçues pendant l'audit

- Domniscian remplace Bérénice à Safrania ; Bérénice remplace Koga à Parmanie, spécialité Psy. Conserver les ressources originales et les apparitions secondaires.
- Seigneur Enma nº150 : Psy, PV100/Atq130/Déf90/Vit120/AtqSpé150/DéfSpé90 validés.
- Correction de la demande Multi Exp : supprimer le partage AUTOMATIQUE ; conserver l'objet tenu et le cadeau de Chen. La section 6 du document joint est donc remplacée par cette instruction.

## État réel et conflits

- Ligue : huit entrées initiales/revanche ; équipes actives `sYokaiParty_ELITE_FOUR_*`. Quatre salles natives puis finale Don Morléone/Spiraton séparée. Ordre des envois actuellement libre : il faut imposer l'ordre validé.
- Bérénice est déjà installée à Safrania. Ressources complètes disponibles ; aucun besoin de les recréer. Nouveau déplacement validé ci-dessus.
- Domniscian, employés rouge/bleu et Seigneur Enma royal possèdent déjà leurs graphismes dans `graphics/yokai_characters/{domniscian,employe_rouge,employe_bleu,enma}`. Leurs combats postgame existent déjà dans `data/scripts/yokai_cameos_boss.inc`. Aucun réveil narratif à Yopple identifié dans les scripts consultés : ne pas en inventer.
- Rencontres fixes réelles : Kyubi est actuellement au Mont Braise et Mademoaiselle aux Îles Écume (contrairement au résumé du dossier). Il faut les réaligner avec le tableau demandé : Nyada verrouillé au Mont Braise, Kyubi aux Îles Écume, Mademoaiselle sauvage Route Victoire. Octorgone est déjà à la Centrale.
- Grotte Azurée : condition additionnelle `FLAG_YOKAI_ENMA_WON` présente ; retirer cette seule condition de quête en conservant les accès généraux et les drapeaux de capture.
- Multi Exp automatique retrouvé dans `Cmd_getexp` : réservistes vivants récompensés même sans objet. Restaurer la distribution native conditionnée par l'objet, en préservant la protection Spiraton et le rendement spécial du Colosse.
- Chromatiques : 84 espèces autorisées par `yokai_shiny.h`. Cette règle existante doit être préservée ; bonus Safari local uniquement, PID/OT cohérents.
- Enma l'Ancien : illustration présente, overworld fidèle encore absent des ressources identifiées. Référence demandée. Ne pas fabriquer un asset présenté comme validé.
- Attribution de `personnage_safrania_3_vues.png` à confirmer (ressemble au Seigneur Enma royal), équipe Acier de Domniscian soumise séparément.
- Audio : public et privé ont des liaisons distinctes. Conserver les 31 OST privées et les thèmes réservés Cramois/Ligue/finale. Ne supprimer que des données prouvées inaccessibles, avec tableaux/pointeurs stables.

## Découpage prévu

1. Distribution d'expérience, bonus Safari, rencontres et équilibrage nº150.
2. Ligue : équipes, ordre, textes et ressources graphiques disponibles.
3. Safrania/Yopple/Parmanie : intégration après décisions ciblées.
4. Audit audio et retrait prudent des ressources confirmées inutilisées.
5. Compilations publique/privée, tests mGBA, preuves et bilan ROM/RAM.

Les identifiants des 151 espèces, la finale, les variantes garçon/fille, les apparitions secondaires et Cramois restent des invariants de vérification.

## Clôture des questions

Les décisions finales et leurs preuves remplacent les hypothèses initiales ci-dessus : voir [RAPPORT.md](RAPPORT.md). La planche trois vues est bien Domniscian ; les références finales de Zazel/Nyada/Enma l’Ancien ont été fournies pendant le travail. Le réveil à Yopple était une mauvaise interprétation : aucun réveil n’est créé. Les employés se combattent après la Ligue, et Domniscian se redéfie comme Champion dans son Arène.
