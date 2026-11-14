# PROTOTYPE_RESULTS — tests réellement effectués

Environnement : conteneur Linux, mGBA **0.10.2** (Qt, paquet Ubuntu) sous écran X virtuel (Xvfb) piloté par
`xdotool`, captures internes de mGBA (F12) ; Archipelago **0.6.9** (`f5b97c5`) depuis les sources ; agbcc
(`da598c1`) et arm-none-eabi-gcc 13.2.1.

Légende : **RÉEL-JEU** = exécuté dans le jeu sous mGBA · **RÉEL** = vrai outil (Archipelago, compilateur), sans
jeu en cours · **STATIQUE** = lecture de la ROM · **NON FAIT** = à faire (raison donnée).

## Les huit vérifications demandées

| # | Vérification | Statut | Détail |
|---|---|---|---|
| 1 | Lancement du jeu dans mGBA | **RÉEL-JEU : OK** | ROM du hack : logo, écran titre « Emerald Version », menu, discours du Prof. Seko |
| 2 | Affichage de Nathan ou Katie | **RÉEL-JEU : OK** | choix « BOY » : nouveau garçon (cheveux bruns en épis, chemise rouge) ; « GIRL » : nouvelle fille (queue de cheval, nœud rose) ; sprite de terrain du garçon sur l'écran du nom, palette correcte |
| 3 | Présence des Yo-kai | **STATIQUE : OK** ; en jeu : NON FAIT | 6 espèces, sprites face/dos/icône rendus depuis la ROM, 106 emplacements sauvages. Une rencontre en jeu demande de marcher dans les hautes herbes (1 % sur la Route 101) : à faire sur PC |
| 4 | Textes français | **NON FAIT** | aucune version française n'existe encore ; la compilation de la décompilation française a été **bloquée par une règle de permission** de cet environnement |
| 5 | Connexion à un serveur Archipelago | **NON FAIT avec le hack** (impossible : aucun code AP dans le hack) | côté Archipelago : génération réelle d'une graine Pokémon Émeraude **OK** (C1) |
| 6 | Envoi d'un check | NON FAIT | nécessite le patch reconstruit (stratégie C) |
| 7 | Réception d'un objet | NON FAIT | idem |
| 8 | Persistance après sauvegarde / reconnexion | NON FAIT | idem ; le mécanisme (compteur en sauvegarde) est documenté dans ARCHIPELAGO_COMPATIBILITY.md |

## Tests Archipelago réels

| Test | Résultat | Nature |
|---|---|---|
| C1 Génération d'une graine à 2 joueurs (Pokémon Émeraude + APQuest), objectif champion | OK : `.apemerald` produit | RÉEL |
| C2 Validation officielle de la ROM du hack (MD5 attendu `605b89b6…`) | **REFUSÉE** : `File hash does not match` | RÉEL |
| C2 bis Validation de l'Émeraude vanilla compilée depuis pret/pokeemerald | **ACCEPTÉE** | RÉEL |
| C3 Patch forcé sur le hack | ROM produite, **16 %** d'octets communs avec la vraie ROM AP, **écran blanc** dans mGBA pendant 15 s | RÉEL-JEU |
| C3 bis Même graine sur la vanilla | démarre : logo Game Freak, intro, écran titre | RÉEL-JEU |

Note d'honnêteté : un premier essai de C3 donnait « 100 % identiques ». C'était un artefact : Archipelago garde la
première ROM source **en cache** (`Files.py`, `get_source_data_with_cache`). Le script `poc/ap_patch_check.py`
réinitialise ce cache entre deux ROM ; les chiffres ci-dessus viennent de la version corrigée.

## Analyses statiques reproductibles

| Outil | Résultat |
|---|---|
| `tools/analysis/compare_with_vanilla.py` | en-tête GF, tables vanilla identiques, 6 espèces ajoutées, rencontres modifiées, 0 dresseur modifié |
| `tools/yokai_extract.py` | données complètes des 6 Yo-kai + graphismes + rapport d'anomalies (type 255, Pokédex, niv. 1-100) |
| Table de référence de HMA-CE contre la ROM | 27/377 repères valides (vanilla : 370/377) |

Correction : une lecture de la table d'évolution avec une taille d'entrée erronée (6 au lieu de 8 octets) m'avait
fait annoncer « Jibanyan évolue en Bekipan ». **C'est faux** : aucun Yo-kai n'évolue. La taille correcte a été
validée sur deux espèces vanilla (Bulbizarre, Goélise).

## Captures (non versionnées)

Les captures et images extraites montrent des graphismes du jeu et du créateur : elles ne sont pas mises dans le
dépôt. Pour les reproduire : `poc/mgba_drive.sh` (voir BUILD_GUIDE.md §4).

## Ce qui reste à faire sur votre PC

Voir ROADMAP.md, phase 0 : partie réelle de 30 min sur le hack (rencontre d'un Yo-kai, Pokédex de Whisper et
Komajiro, résumé de Whisper), compilation de `qigast/pokeemeraude` et comparaison avec **votre** cartouche
française, puis le prototype AP (jalon 1).
