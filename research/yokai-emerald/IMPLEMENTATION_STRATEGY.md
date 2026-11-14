# IMPLEMENTATION_STRATEGY — trois stratégies comparées

Les durées sont des **ordres de grandeur** pour une personne qui connaît le C et la décompilation, à temps partiel.
Elles ne viennent d'aucune mesure : elles servent à comparer les stratégies entre elles.

## Stratégie A — Adapter Archipelago au ROM hack binaire

Garder la ROM du créateur et y greffer le code Archipelago.

| Critère | Évaluation |
|---|---|
| Difficulté | **Très élevée** : réécrire en assembleur/patchs binaires tout le patch de base AP (réception d'objets, messages, options, centaines de modifications de scripts) sur un binaire compilé par un GCC inconnu, sans symboles |
| Risques | **Bloquant** : patch AP actuel inapplicable (testé : ROM corrompue, écran blanc) ; impossible de régénérer `extracted_data.json` sans source |
| Temps | plusieurs mois, issue incertaine |
| Dépendances | aucune source, outils binaires seulement |
| Français | non résolu (HMA cassé sur cette ROM : 27/377 références valides) |
| Stabilité / maintenance | très faible ; chaque correctif du monde AP officiel serait à reporter à la main |
| Reproductibilité | faible |
| Autorisations | créateur (on redistribuerait un dérivé de sa ROM) |

## Stratégie B — Intégrer les modifications Yo-kai à Archipelago Emerald

Partir de l'Émeraude AP et y ajouter Nathan/Katie et les Yo-kai.

- **En binaire**, sur la ROM AP : ajouter 6 espèces impose d'agrandir une dizaine de tableaux dimensionnés par
  `NUM_SPECIES`, le Pokédex et la sauvegarde. Même problème que A. **Non viable.**
- **En source**, sur le code C du patch AP : c'est la stratégie C appliquée à une base AP. Elle dépend de
  l'accès au code C (officiel : non trouvé ; Flit : public).

## Stratégie C — Reconstruire le hack sur une décompilation (recommandée)

Recréer en source les modifications Yo-kai (mesurées précisément, voir ROM_ANALYSIS.md) sur une décompilation qui
porte aussi le code Archipelago.

| Critère | Évaluation |
|---|---|
| Difficulté | **Moyenne** : ajout de 6 espèces (opération documentée de la décompilation : ~15 fichiers), remplacement de sprites, 1 panneau, ~106 emplacements sauvages ; fusion de deux forks de pret (AP + français) |
| Risques | fusion `pokeemeraude` (français) × fork AP (anglais) : conflits sur les mêmes fichiers (textes, menus, sac) ; format de sauvegarde nouveau (normal pour AP) |
| Temps | jalon anglais jouable en AP : 2-4 semaines ; version française : +3-6 semaines ; finition : +2-4 semaines |
| Dépendances | pret/pokeemerald (base du hack), code C AP (Flit ou officiel), `qigast/pokeemeraude`, Archipelago ≥ 0.6.x, agbcc |
| Français | **textes officiels** via la cartouche française du joueur + ~20 textes Yo-kai et ~100-300 textes AP à traduire |
| Stabilité | élevée : on corrige au passage les bugs du hack (type 255, Pokédex, Blizzaria niv. 1-100), et la logique AP est générée depuis notre build |
| Maintenance | bonne : fusion des mises à jour pret / AP par git |
| Reproductibilité | **totale** : `make` + scripts ; aucune ROM ni asset propriétaire dans le dépôt |
| Autorisations | **créateur** (données et sprites Yo-kai), **dessinateurs** (Ludo, SonGoku, Nicowico), **auteur du code AP** (Flit et/ou Zunawe : pas de licence sur le code C), crédits pret / DizzyEgg / Qigast |

### Précaution « travail du créateur »

L'outil `tools/yokai_extract.py` lit le contenu **dans la ROM du hack fournie par chaque joueur** et produit les
fichiers source au moment de la compilation. Ainsi :
- tant que le créateur n'a pas répondu, **rien de son travail n'est dans notre dépôt** ;
- s'il refuse la redistribution, le projet reste utilisable par qui possède sa ROM, sans republier ses assets ;
- s'il accepte, on peut versionner les assets avec ses crédits.

## Recommandation

**Stratégie C, en deux jalons :**

1. **Jalon « anglais AP »** : fork AP (code C de Flit, ou officiel s'il est obtenu) + couche Yo-kai.
   But : valider tôt la boucle Archipelago complète (checks, objets, sauvegarde, reconnexion) avec Nathan, Katie et
   les Yo-kai, **avant** d'investir dans la traduction (conforme à la consigne « ne pas traduire avant d'avoir
   vérifié la compatibilité »).
2. **Jalon « français »** : porter les deux couches (AP + Yo-kai) sur `qigast/pokeemeraude`, traduire les textes
   ajoutés, passer le monde forké sur le hash de l'Émeraude française.

Pourquoi pas A ou B binaire : c'est **mesuré**, pas supposé. Le patch existant est inapplicable, HMA perd 93 % de
ses repères sur cette ROM, et le code du hack ne correspond même pas à une build de référence.

## Le monde Archipelago

Fork du monde (MIT) nommé « Pokemon Yo-kai Emerald » :
- `extracted_data.json` régénéré depuis notre build ;
- 418 espèces, dont les 6 Yo-kai disponibles en sauvage, pour le dexsanity et le mélange des rencontres ;
- hash de base = Émeraude **US** (jalon 1) puis **FR** (jalon 2) ;
- client inchangé dans son principe (flags + compteur en sauvegarde), offsets recalculés, Pokédex sur 53 octets ;
- pas de collision avec le monde officiel (nom de jeu et nom de ROM distincts) : les deux peuvent coexister dans le
  même multiworld.
