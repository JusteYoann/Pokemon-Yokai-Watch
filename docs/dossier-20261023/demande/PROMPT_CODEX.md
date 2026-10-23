# Pokémon Rouge Feu × Yo-kai Watch — Dossier consolidé à implémenter

**Dépôt :** `JusteYoann/Pokemon-Yokai-Watch`  
**Date de préparation :** 23 octobre 2026  
**Autorisation :** préparer et implémenter sur **une branche de travail dédiée**, après audit, mais **NE JAMAIS fusionner sur `master` sans l'autorisation explicite de Yoann**.

## 0. Règles impératives

1. Auditer l'état réel du dépôt et les branches récentes avant toute modification. Les nouvelles scènes de Cramois sont développées en parallèle sur `feature/cramois-ile-passe` : **ne pas écraser ni perturber ce travail**, ni déclencher de fusion automatique. Coordonner les changements qui touchent Cramois lorsque la phase C sera prête.
2. Les numéros des 151 espèces sont fixes et les identifiants `SPECIES_*` d'origine doivent rester en place. Le fichier de référence des noms est `src/data/text/species_names.h` sur la branche de développement, et les types sont dans `src/data/pokemon/species_info.h`. La branche `master` peut encore contenir les noms Pokémon originaux.
3. Ne créer aucune nouvelle espèce et ne pas inventer de nouvelles attaques. Pour les équipes et les attaques, utiliser uniquement des espèces et capacités déjà présentes ou compatibles avec le moteur.
4. Préserver les systèmes déjà développés : Carmin/Ariane/Usapion, Lavanville, Mafiamille, enquête de la Pierre Philosovni, Yopple/Safrania, Cramois phases A/B/C, et **la finale scénaristique Don Morléone / Don Spiraton**.
5. Garder des commits lisibles, compiler les versions publique et privée lorsque possible, tester sous mGBA, et rendre un rapport de fichiers modifiés, tests, captures, RAM et taille ROM.
6. Toutes les décisions ci-dessous sont validées, **sauf ce qui est explicitement marqué « à définir »**. Ne pas trancher seul un choix narratif majeur ni inventer des références graphiques absentes.

## 1. Ligue : quatre adversaires, six Yo-kai chacun — VALIDÉ

Ordre strict : **Zazel → Enma l'Ancien → Orqanos → Maître Nyada**. Ces quatre personnages sont des Dresseurs et ne doivent pas être confondus avec les espèces du Pokédex portant des noms proches.

### 1.1 Zazel — stratégie Psy/Ténèbres

| Ordre | Yo-kai | Niveau | Rôle attendu |
|---|---|---:|---|
| 1 | Bonneto | 52 | Entrave, Ténèbres |
| 2 | Baku | 53 | Sommeil et pression Psy |
| 3 | Fourchelang | 54 | Couverture Psy |
| 4 | Emperor | 55 | Résistance Acier/Ténèbres |
| 5 | Savantard | 56 | Pression Psy |
| 6 | Octorgone | 58 | Ace offensif Ténèbres |

Style : confusion, sommeil et autres altérations disponibles dans le moteur, tactiques de statut et changement de rythme. Ne pas inventer d'attaques pour obtenir cet effet.

### 1.2 Enma l'Ancien — anciens et royaux

| Ordre | Yo-kai | Niveau |
|---|---|---:|
| 1 | Faux Kappa | 54 |
| 2 | Potofeu | 55 |
| 3 | Tauracle | 56 |
| 4 | Hovernyan | 57 |
| 5 | Shogunyan | 58 |
| 6 | Kyubi | 60 |

Style : lignée des Yo-kai du passé et des figures prestigieuses, puissance polyvalente. **Enma l'Ancien n'est pas le Seigneur Enma, espèce n°150.**

### 1.3 Orqanos — force brute Combat/Roche

| Ordre | Yo-kai | Niveau |
|---|---|---:|
| 1 | Passpa | 56 |
| 2 | Coach Antonic | 57 |
| 3 | Rocky Badboya | 58 |
| 4 | Turboss | 59 |
| 5 | Gorgouille | 60 |
| 6 | Mademoaiselle | 62 |

Style : attaques physiques et résistance, forte pression directe. Mademoaiselle demeure présente dans son équipe **même si sa rencontre fixe du Mont Braise a changé**.

### 1.4 Maître Nyada — Maître de Ligue multitype

| Ordre | Yo-kai | Niveau |
|---|---|---:|
| 1 | Blizzaria | 58 |
| 2 | Émettor | 59 |
| 3 | Sir Dragon | 60 |
| 4 | Robonyan F | 61 |
| 5 | **Démophage** | **63** |
| 6 | **Maître Nyada (espèce n°148)** | **65** |

Les **deux dernières positions sont impératives**. Le personnage Maître Nyada combat d'abord comme Dresseur puis envoie, en ultime combattant, l'espèce Maître Nyada. Faire une équipe multitype réellement équilibrée.

### 1.5 Graphismes Ligue

- Zazel : `library_originals/Nintendo Switch - Yo-kai Watch 4++ - Yo-kai (Onnen Tribe) - Zazel.png` et `library_originals/Zazel_le_Bdfgon.webp`.
- Enma l'Ancien : `library_originals/Enma_l'Ancien.webp` (illustration) ; **sprite overworld à retrouver / confirmer**.
- Orqanos : `library_originals/Nintendo Switch - Yo-kai Watch 4++ - Yo-kai (Oni Tribe) - Orcanos(1).png` et `library_originals/Orqanos_Peinture_de_guerre.webp`.
- Maître Nyada : `library_originals/Nintendo Switch - Yo-kai Watch 4++ - Yo-kai (Mononoke Tribe) - Master Nyada.png` et `library_originals/Ma_tre_Nyada.webp`.
- Ces **sept fichiers issus des références précédemment fournies** sont joints à ce ZIP. Si la référence overworld d'Enma l'Ancien est introuvable, demander sa transmission, sans fabriquer une représentation supposée fidèle.
- Les Dresseurs restent généralement immobiles dans leurs salles : **pas besoin d'animations complètes de marche**.

## 2. Rencontres spéciales et espèces

| Endroit | Espèce statique | Contraintes |
|---|---|---|
| Mont Braise | **Maître Nyada (n°148, `SPECIES_DRAGONAIR`)** | Remplace Mademoaiselle. Rencontre / capture inaccessible normalement avant la quête postgame dédiée (à concevoir plus tard). Ne pas rendre Nyada capturable prématurément. |
| Îles Écume | **Kyubi** | Rencontre fixe conservée ; nouvel overworld selon `references/kyubi_overworld_yw4.png`. |
| Centrale | **Octorgone** | Rencontre fixe conservée ; nouvel overworld selon `references/octorgone_overworld_yw4.png`. |
| Grotte Azurée | **Seigneur Enma (n°150, `SPECIES_MEWTWO`)** | Rencontre fixe, **sans quête préalable**, remplace l'ancien « Enma chat violet ». |

### 2.1 Seigneur Enma — refonte n°150

- Conserver le numéro 150 et `SPECIES_MEWTWO` ; remplacer l'identité et les visuels de l'ancien chat violet par **Seigneur Enma**.
- Référence de design avec épée : `references/seigneur_enma_combat.webp`.
- Refaire **sprite de combat de face, sprite de dos**, et sprite overworld de Seigneur Enma. Pour l'overworld, chercher d'abord une référence dédiée dans le dépôt ; ne pas déduire un sprite définitif de l'illustration si une meilleure référence existe.
- Revoir les statistiques, attaques apprises et éventuelles données associées. **Proposition chiffrée non encore validée :** PV 100, Atq 130, Déf 90, Atq Spé 150, Déf Spé 90, Vit 120 (total 680), type Psy provisoire. **Soumettre à Yoann avant de figer cet équilibrage.**
- Retirer uniquement la quête préalable conditionnant son apparition dans la Grotte Azurée ; respecter les autres accès/conditions générales du jeu.

### 2.2 Mademoaiselle n°147 — nouvelle rencontre sauvage VALIDÉE

- **Route Victoire : 5 % de rencontres sauvages**, niveau **45–48**, type Roche.
- Elle n'est plus une rencontre statique au Mont Braise.
- Ajuster les tables de rencontres de façon à préserver un total de probabilités cohérent (100 %) sans retirer involontairement une espèce importante. Choisir la ou les zones d'intérieur de la Route Victoire cohérentes et documenter exactement la table modifiée.

## 3. Safrania, Yopple et Domniscian

### 3.1 Entreprise et Champion

- **Sylphe SARL devient Yopple** (noms, enseignes, dialogues et événements pertinents).
- Yopple a créé la Yo-kai Watch moderne, les Yo-kai Balls, le Yo-kai Pad, l'aspirateur à Yo-kai et diverses technologies.
- **Steve Jaws** est le **fondateur** de Yopple et l'origine historique de ses inventions.
- **Domniscian** est son ancien concurrent, qui a **racheté** Yopple. Il en est le PDG actuel, **pas l'inventeur**. Son caractère vaniteux doit transparaître dans ses dialogues.
- Il devient **Champion de Safrania, spécialiste Acier**, à la place du Champion d'origine encore présent. Auditer l'état des remplacements et signaler toute collision avec un Champion déjà remplacé avant de supprimer du contenu.
- L'invasion de Yopple par la Mafiamille doit être résolue avant le combat d'Arène.
- Après son sauvetage, Domniscian donne au joueur **une Master Ball**, puis lui donne rendez-vous dans son Arène **dans la même ville**. Le cadeau n'est pas conditionné à la victoire à l'Arène.
- **Équipe et niveaux de Domniscian : À DÉFINIR avec Yoann**. Ne pas inventer une équipe définitive. Préparer éventuellement le support technique séparément.

### 3.2 Employés de Yopple

- Des employés sont visibles dans le bâtiment durant l'aventure.
- Leurs **sprites seraient déjà dans GitHub** : effectuer une recherche dans les assets/branches avant de créer quoi que ce soit. Documenter les chemins retrouvés.
- Pendant le **postgame**, lorsque le protagoniste se réveille dans les locaux de Yopple dans l'événement scénaristique prévu, certains employés deviennent affrontables.
- Ne pas inventer la raison de ce réveil ni déplacer l'événement : auditer les scripts existants et préserver l'enchaînement narratif. Équipes de Yo-kai existants, thème technologique et Acier/Électrik approprié, à calibrer au postgame.
- L'image `references/personnage_safrania_3_vues.png` a été envoyée au moment du travail sur Domniscian/Safrania ; elle montre trois vues d'un personnage. **Confirmer son attribution exacte avant de l'utiliser comme Domniscian.**

## 4. Cramois'Île — Hovernyan et Nathaniel/Michael

- Les phases A (sépia) et B (brume maritime) sont validées ; la phase C est en cours sur `feature/cramois-ile-passe`. **Ne pas écraser ni dupliquer leur implémentation.**
- L'overworld d'Hovernyan près de Nathaniel/Michael doit utiliser `references/hovernyan_overworld_yw4.png` ; le Yo-kai reste **constamment à côté de son maître** dans les scènes de Cramois'Île, le suit lors des mouvements scénarisés, sans animations inutiles. Aucun remplacement du sprite de combat n'est demandé.
- **Postgame :** après un **deuxième combat gagné** contre Nathaniel/Michael, ce personnage offre Hovernyan au joueur, une seule fois. Prévoir sauvegarde durable et gestion d'équipe pleine. Ne pas modifier rétroactivement les scènes du passé (60 ans avant le présent).
- Adapter la variante Nathaniel/Michael au choix / scénario existant sans inventer un nouveau critère.

## 5. Parc Safari — chromatiques x3

- Dans **toutes les zones du Parc Safari**, la probabilité de Yo-kai shiny en rencontre sauvage est exactement **3/8192** si le taux standard de Rouge Feu est de 1/8192, soit environ 0,03662 % (environ 1/2730,67).
- Le reste du jeu conserve le taux normal. Le bonus est local au Parc Safari, pas aux cadeaux, œufs ni rencontres fixes hors Safari ; il ne modifie pas les captures et fuites.
- Attention à l'implémentation Gen III : conserver la cohérence entre PID, Dresseur secret/visible et statut chromatique. Éviter une méthode qui ne marche pas pour les rencontres Safari ou qui régénère un individu en boucle. Tester statistiquement le taux et les limites de cartes.

## 6. Supprimer le Multi Exp du jeu

- Retirer l'obtention et l'utilisation du **Multi Exp / Exp. Share comme objet tenu**. Ce n'est pas un système moderne d'expérience automatique pour toute l'équipe.
- Auditer les cadeaux, objets au sol, inventaires, scripts et autres voies d'obtention.
- Le scientifique / assistant de Chen qui le donnait doit proposer une autre récompense **à valider avec Yoann** ; ne pas inventer un objet définitif.
- Préserver les identifiants internes si les supprimer présente un risque. Le comportement d'expérience normal reste inchangé.

## 7. Nettoyage réel des musiques inutilisées — objectif : récupérer de la place ROM

**Il est expressément demandé de supprimer réellement les données inutilisées de la compilation ROM**, pas seulement de désactiver des appels à ces musiques.

Procéder en plusieurs étapes :

1. Faire un audit des musiques, séquences, banques d'échantillons et tables actuellement embarquées ; identifier pour chacune les références dans les cartes, scripts, combats, menus, événements, postgame, versions publique et privée.
2. Comparer aux OST Yo-kai Watch intégrées et aux musiques prévues mais encore non utilisées pour la Ligue, Cramois et la finale Don Morléone / Don Spiraton.
3. **Conserver les pistes nécessaires ou possiblement réservées au développement.** Fournir d'abord une liste des suppressions envisagées et demander validation si l'utilisation future est ambiguë.
4. Retirer les données/ressources des éléments **confirmés inutilisés** de la construction ROM et nettoyer les tables/pointeurs prudemment. Éviter les identifiants cassés, sons manquants et corruptions de mémoire.
5. Comparer l'espace ROM réellement occupé avant/après (public et privé), en distinguant taille de fichier, sections, marges disponibles et gains mesurés. Compiler et tester les scènes audio survivantes.

**Ne jamais effacer une OST privée ni du travail existant sans preuve qu'il est inutilisé et sans l'accord nécessaire.** Si un nettoyage risque de perturber la phase C, le différer ou l'isoler sur une branche dédiée.

## 8. Livrables et point d'arrêt

- Audit initial par sujet et risques de conflits entre branches.
- Plan de commits / branches séparant au besoin audio, Ligue, rencontres, Safrania, Safari et objets.
- Implémentation des seuls points pleinement spécifiés ; **questions ciblées pour les détails non validés** (équipe Domniscian, stats Seigneur Enma, cadeau remplaçant le Multi Exp, attribution de sprites incertaine, contenus narratifs absents).
- Build public/privé, tests mGBA, captures/GIF pertinents, contrôles de progression et des rencontres.
- Tableau récapitulant chemins modifiés, espèces / niveaux, taux Safari, récompenses, références graphiques et **octets ROM réellement gagnés**.
- **Aucune fusion sur `master`.** S'arrêter et présenter le résultat pour validation explicite de Yoann.

## Fichiers graphiques joints

Voir `REFERENCES.md` pour les **douze images incluses**, dont sept références des Dresseurs de Ligue.
