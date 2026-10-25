# Dialogues : cohérence et personnalités

ROM bêta française du 25 octobre 2026, basée sur `58f2245a5`. Cette mise à jour réécrit 63 dialogues principaux dans 23 fichiers et corrige le nom public « Don Spiration ». Elle ne constitue pas une validation complète de la progression ni de l’équilibrage.

## Histoire et origines de la Watch

Chen est un chercheur qui confie une Watch au joueur, et ne prétend plus l’avoir inventée. Il présente Steve Jaws comme le concepteur du modèle moderne et le fondateur de Yopple, entreprise rachetée par Domniscian.

Les premiers prototypes sont révélés seulement dans le chapitre de Cramois’Île. Nathaniel ou Michael remarque le modèle inconnu au poignet du joueur, explique travailler sur les premiers prototypes et veut examiner son mécanisme. Hovernyan explique que la brume nous a ramenés soixante ans dans le passé et permet de retrouver notre époque. Sa réplique « Pas de tournevis dans l’avenir! » conserve une touche légère. Le passage est ancien : la Pierre Philosovni ne l’a pas créé récemment.

L’enquête sur la Pierre suit désormais une piste explicite : acquisition au repaire, recherches à Yopple, puis utilisation par Morléone pour fusionner les forces de ses hommes avec les siennes. Après Jadielle, il abandonne les petites affaires et vise un autre pouvoir ; son retour à la Ligue reprend cette ambition. Le prestige du titre sert son influence, sans lui attribuer un pouvoir politique automatique. Sa défaite souligne la différence entre assembler des forces et unir des volontés.

Maître Nyada se souvient du combat de la Ligue lorsqu’il retrouve le joueur en postgame. Les références à ses anciens compagnons et les étapes de ses quêtes sont conservées. Juste Yoann confirme être le mystérieux visiteur évoqué par Alizon.

## Voix des personnages

Les traits sont répartis pour varier les échanges sans ajouter une expression forcée à chaque phrase.

| Personnage | Voix et caractère |
| --- | --- |
| Chen | Curieux, chaleureux, encourage l’observation et les petites questions. |
| Nathan | Héros ordinaire, autodérision et préoccupations concrètes. |
| Matt | Compétitif, impatient et taquin, mais solidaire quand la situation l’exige. |
| Katie | Calme, attentive, humour discret envers Jibanyan. |
| Wyatt | Enthousiasme pour l’aventure, le terrain et les mystères. |
| Ariane | Hypothèses, expériences, curiosité débordante. |
| USApion | Réponses sèches et pratiques, « dany » employé avec mesure. |
| Léo | Inventeur distrait ; plaisante sur sa transformation et ses provisions de chocolat. |
| Bérénice | Réservée, énigmatique, humour sur ses prédictions. |
| Nathaniel | Bricoleur obstiné ; outils et confiance dans ses compagnons. |
| Michael | Idées multiples, atelier encombré et prototypes à étincelles. |
| Hovernyan | Guide pragmatique, protecteur et pince-sans-rire. |
| Don Morléone | Dettes, affaires et influence ; fierté puis recul après sa défaite. |
| Domniscian | Image de marque, résultats et excuses commerciales. |
| Steve Jaws | Essais, prototypes et envie d’inventer, sans arrogance commerciale. |
| Maître Nyada | Maître exigeant et sage ; humour autour des siestes. |
| Démophage | Impressionnant mais timide et gourmand ; répliques distinguées de celles de Nyada. |
| Alizon Bie | Enthousiaste, affectueuse, humour macabre et intrépide. |
| Enma | Souverain chaleureux, joueur, attentif aux liens plutôt qu’à la possession. |
| Enma Ancien | Ton plus posé et solennel. |
| Zazel | Vouvoiement, dossiers, protocole et pause thé. |
| Scientifique | Escalade de vantardises robotiques ; sa progression comique existante est conservée. |
| Orqanos | Répliques brèves et menaçantes conservées. |
| Juste Yoann | Ton personnel, chaleureux et complice ; conclusion « THANK FOR PLAY » conservée. |

Les pages Fandom ont refusé les requêtes depuis cet environnement (403). La réécriture s’appuie sur les traits établis, les dialogues existants et les indications du projet ; elle ne présente pas une recherche wiki comme une vérification réussie. Les noms français sont conservés.

## Vérifications

- Compilation audio complète réussie.
- Nouvelle partie native mGBA pour les deux personnages jouables ; substitutions Nathaniel/Michael vérifiées dans la scène de Cramois.
- 63 textes compilés, 520 lignes après substitution par genre, mesurées avec les polices natives 2 et 4 : largeur maximale de 196 pixels, noms du joueur testés avec sept « W ». Les messages restent sous la capacité contrôlée du tampon.
- 64 scènes rejouées avec succès sur la ROM livrée : fin des scripts, reprise des déplacements et ouverture du menu, avec les exceptions attendues pendant la Terr’heure et la conclusion de la Ligue.
- Discours d’Argenta : huit arrivées réelles depuis la Route 2, réparties entre les deux personnages jouables ; Centre, musée, sortie, retour et menu vérifiés.
- Comparaison structurelle : seules les chaînes de texte ont changé dans les 23 fichiers de dialogues ; mouvements, conditions, récompenses, combats et équipes sont conservés. Deux fichiers C corrigent seulement l’orthographe publique de Don Spiration.

Ces essais utilisent des scènes isolées préparées et une équipe renforcée. Ils ne remplacent pas une partie continue ni un test d’équilibrage. Aucune nouvelle vidéo n’a été produite.

Les preuves sont dans [TESTS_TEXTES.json](TESTS_TEXTES.json), [verification/BILAN.json](verification/BILAN.json) et les rapports individuels. [MODIFICATIONS.json](MODIFICATIONS.json) contient les 63 dialogues réécrits sous une forme lisible.

[Télécharger la ROM](Pokemon_Yokai_Watch_Beta_0.1_Dialogues_Coherents.gba) — [SHA-256](SHA256.txt).
