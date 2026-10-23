# Pokémon Rouge Feu × Yo-kai Watch — Quête secrète : Juste Yoann et le Charme Chroma

**Dépôt GitHub :** `JusteYoann/Pokemon-Yokai-Watch`

**IMPORTANT : AUCUN MERGE SUR `master` SANS MON AUTORISATION EXPLICITE.**

Je souhaite intégrer une nouvelle quête de fin de jeu permettant de rencontrer et d'affronter Juste Yoann, le créateur du ROM hack.

Cette quête représente une conclusion symbolique à la complétion des 151 Yo-kai du Médallium.

Elle doit être indépendante de la finale scénaristique avec Don Morléone et Don Spiraton.

## 1. Conditions de déblocage

Juste Yoann ne doit pas être présent dans le jeu tant que les conditions suivantes ne sont pas remplies :

1. Le joueur a obtenu les **151 espèces de Yo-kai** du Médallium.
2. Le joueur retourne au laboratoire du professeur Chen.
3. Le joueur déclenche le dialogue spécial de félicitations du professeur.

Attention : le Médallium doit être réellement complété. Avoir simplement aperçu les 151 espèces ne suffit pas.

Le suivi de cette condition doit être fiable et persistant après sauvegarde.

Il ne faut pas modifier la numérotation actuelle des 151 Yo-kai ni casser le fonctionnement du Pokédex/Médallium.

## 2. Événement du professeur Chen

Après la complétion du Médallium, Chen possède un nouveau dialogue :

**PROF. CHEN :**

« Incroyable ! Tu as réussi ! »

« Les 151 Yo-kai de Kanto sont désormais enregistrés dans ton Médallium ! »

« Voilà un exploit dont tu peux être fier ! »

« Ah ! J'allais oublier... »

« Une personne assez particulière est venue me voir récemment. »

« Elle m'a demandé de te prévenir qu'elle t'attendait... chez toi ! »

« Tu devrais aller voir de qui il s'agit. »

Après cette conversation, un drapeau permanent autorise l'apparition de Juste Yoann.

Ce dialogue spécial ne doit pas se répéter indéfiniment.

## 3. Apparition de Juste Yoann

**Localisation définitive : chambre du joueur, à l'étage de sa maison à Bourg Palette.**

Juste Yoann apparaît uniquement lorsque le professeur Chen a validé la complétion du Médallium.

Il est immobile, orienté vers le joueur.

### Sprites

Utiliser exclusivement l'image de référence fournie :

`weqrt19_53_30.png`

Elle contient :

- À gauche : le portrait de combat définitif de Juste Yoann.
- À droite : son sprite overworld définitif.

Les deux apparences sont VALIDÉES.

**Ne pas les redessiner ni modifier leurs couleurs, leurs proportions ou leur design.**

Adapter uniquement leurs dimensions, leurs palettes et leurs formats techniques aux contraintes du moteur GBA.

Le sprite overworld utilise une seule orientation de face.

Aucune animation de marche n'est nécessaire. Si le moteur impose plusieurs orientations, utiliser les mêmes données graphiques.

Vérifier que son emplacement dans la chambre ne bloque ni le PC, ni les déplacements, ni les autres événements.

## 4. Premier dialogue

Lorsque le joueur lui parle :

**JUSTE YOANN :**

« Ah ! Te voilà enfin ! »

« Alors comme ça, c'est toi qui as réussi à compléter le Médallium ? »

« Je dois reconnaître que tu m'impressionnes ! »

« Tu sais quoi ? Avant de discuter, j'ai une petite proposition à te faire... »

« Ça te dit un dernier combat ? »

Afficher un choix :

- OUI : lancement du combat.
- NON : Juste Yoann reste sur place et le joueur peut revenir lui parler.

## 5. Équipe de Juste Yoann

Juste Yoann possède exactement six Yo-kai.

| Ordre | Yo-kai | Niveau |
|---|---|---|
| 1 | Démophage | 70 |
| 2 | Fouétar | 70 |
| 3 | Camaïeul | 70 |
| 4 | Terminyanator | 70 |
| 5 | Démophage | 70 |
| 6 | Seigneur Enma | 70 |

**Les deux Démophage sont intentionnels. Ne pas en remplacer un.**

Le Seigneur Enma doit être l'espèce n°150, qui remplace Mewtwo, et non Enma l'Ancien.

L'équipe doit utiliser les identifiants d'espèces déjà présents dans le dépôt.

### Difficulté

Malgré ses Yo-kai de niveau 70, Juste Yoann ne doit pas être un superboss extrêmement optimisé.

- Utiliser une IA de Dresseur classique.
- Ne pas donner de statistiques artificiellement augmentées.
- Ne pas lui donner d'objets tenus particulièrement abusifs.
- Utiliser des attaques légales déjà disponibles dans le ROM hack.
- Préserver les caractéristiques naturelles des six Yo-kai.

Ce combat doit être amusant et relativement accessible à un joueur ayant terminé le Médallium.

## 6. Dialogue après la première victoire

Après sa défaite, Juste Yoann prononce le dialogue suivant :

**JUSTE YOANN :**

« Ahahah ! Eh bien, tu m'as eu ! »

« Bon... Je vais être honnête avec toi. »

« Je suis peut-être pas le meilleur stratège de Yo-kai Watch. »

« Nyleco est bien meilleur que moi à ce petit jeu ! »

« Mais tu sais... »

« Il y a quelque chose que j'aimerais te dire. »

« Quelque chose d'un peu plus personnel. »

### Début du fondu blanc

À partir de cet instant, l'écran commence à blanchir progressivement.

Le fondu doit être très lent et suivre l'avancement des dialogues.

Les textes doivent rester parfaitement lisibles.

**JUSTE YOANN :**

« Merci. »

« Merci d'avoir pris le temps de jouer à ce jeu. »

« Merci de t'être abonné à ma chaîne YouTube, de regarder mes vidéos et de soutenir mon travail. »

« Tu ne t'en rends peut-être pas compte, mais ça représente énormément pour moi. »

### Intensification du blanc

« J'ai toujours eu de grandes ambitions. »

« Des rêves qui peuvent parfois sembler complètement démesurés... »

« Mais je crois sincèrement qu'un jour, je pourrai les réaliser. »

« Et si ce jour arrive... »

L'écran devient presque entièrement blanc.

« J'espère que tu seras encore là pour le voir. »

« Alors, du fond du cœur... »

« Merci d'avoir fait un bout de chemin avec moi. »

## 7. Écran final — THANK FOR PLAY

L'écran devient entièrement blanc.

Faire disparaître temporairement les interfaces habituelles.

Afficher au centre de l'écran, en lettres sombres :

**THANK FOR PLAY**

Respecter exactement cette formulation.

Le texte doit apparaître proprement, avec une transition douce.

Le maintenir quelques secondes à l'écran.

Prévoir un court silence pour renforcer l'émotion.

Ensuite, faire progressivement revenir les couleurs normales de la chambre.

Le joueur retrouve Juste Yoann face à lui.

Attention : ce fondu est uniquement un effet visuel temporaire. Il ne doit pas corrompre les palettes, les effets météo, les menus ou les combats.

## 8. Récompense — Charme Chroma

Après le retour à la normale :

**JUSTE YOANN :**

« Bon ! Assez parlé ! »

« Tiens, j'ai quelque chose pour toi ! »

Afficher :

**Vous recevez le CHARME CHROMA !**

Puis :

**JUSTE YOANN :**

« Avec ça, tu devrais avoir un peu plus de chance de rencontrer des Yo-kai chromatiques ! »

« Et qui sait ? Peut-être qu'on se retrouvera un jour pour une nouvelle aventure ! »

### Fonctionnement de l'objet

Créer le **Charme Chroma**, un objet rare appartenant aux objets importants.

Description :

« Un mystérieux charme offert par Juste Yoann. Augmente les chances de rencontrer des Yo-kai chromatiques. »

L'objet doit être conservé après sauvegarde et impossible à recevoir plusieurs fois.

Il ne doit pas pouvoir être vendu, jeté ou consommé.

## 9. Probabilités shiny

Le Charme Chroma applique trois tirages de chromaticité au lieu d'un lors de la génération des Yo-kai sauvages.

Le bonus précédemment validé du Parc Safari est maintenu.

**Les deux bonus sont cumulables.**

| Situation | Probabilité approximative |
|---|---|
| Sans bonus | 1/8 192 |
| Parc Safari sans charme | 1/2 731 |
| Charme Chroma hors Safari | 1/2 731 |
| Charme Chroma + Parc Safari | 1/911 |

Au Parc Safari, chaque tirage du Charme Chroma bénéficie du taux triplé.

Conserver la cohérence des identifiants de personnalité et de la détermination shiny du moteur de troisième génération.

Le Charme Chroma ne doit pas modifier :

- Les statistiques des Yo-kai.
- Les probabilités de capture.
- Les probabilités de fuite.
- Les rencontres de Dresseurs.
- Les rencontres statiques ou cadeaux qui ne sont pas concernés par les bonus de rencontres sauvages.

IMPORTANT : **Ne modifier aucune palette ou aucun sprite shiny existant.** Le chantier artistique des shinies est actuellement en pause.

## 10. Comportement après la quête

Après sa première défaite :

- Juste Yoann reste présent dans la chambre du joueur.
- Le discours émotionnel ne se déclenche plus.
- Le Charme Chroma ne peut plus être offert une seconde fois.

Nouveau dialogue lorsque le joueur lui reparle :

**JUSTE YOANN :**

« Hé, merci encore pour tout. »

« J'espère qu'on vivra plein d'autres aventures ensemble ! »

La possibilité d'un nouveau combat pourra être décidée ultérieurement. Ne pas ajouter de rematch automatiquement.

## 11. Compatibilité et préservation

Ne surtout pas casser les fonctionnalités existantes :

- Les 151 Yo-kai et leurs évolutions.
- Le Médallium.
- Les événements du professeur Chen.
- La maison du joueur.
- Les sauvegardes.
- Le Parc Safari.
- La Ligue avec Zazel, Enma l'Ancien, Orqanos et Maître Nyada.
- Les événements de Cramois'Île.
- Yopple et Domniscian.
- La Mafiamille.
- La finale Don Morléone / Don Spiraton.

Ne pas modifier les musiques existantes sans nécessité.

Privilégier la réutilisation des ressources et éviter les allocations permanentes inutiles, notamment au regard de la faible marge EWRAM constatée pendant le développement de Cramois'Île.

## 12. Tests obligatoires

Vérifier sous mGBA :

1. Avec un Médallium incomplet, Juste Yoann est absent.
2. Avec 151 espèces obtenues mais sans avoir reparlé à Chen, Juste Yoann est absent.
3. Après validation par Chen, Juste Yoann apparaît dans la chambre.
4. Le refus du combat ne bloque rien.
5. Les six Yo-kai de Juste Yoann sont corrects, notamment les deux Démophage.
6. Le combat peut être perdu sans bloquer la progression.
7. Après victoire, le dialogue et le fondu blanc se déroulent correctement.
8. Le texte THANK FOR PLAY s'affiche correctement.
9. Les couleurs reviennent normalement après la scène.
10. Le Charme Chroma est reçu une seule fois.
11. Le charme reste acquis après sauvegarde et chargement.
12. Les bonus shiny fonctionnent dans Kanto et au Parc Safari, séparément et ensemble.
13. Les scènes précédentes et les autres systèmes visuels continuent de fonctionner.

## 13. Livrables

Je souhaite recevoir :

- Un audit de l'existant.
- La liste des fichiers modifiés.
- Les commits réalisés sur une branche dédiée.
- Une capture du sprite overworld dans la chambre.
- Une capture de l'introduction du combat.
- Un GIF du fondu blanc et de THANK FOR PLAY.
- Un GIF de l'obtention du Charme Chroma.
- Les résultats des tests mGBA.
- Un bilan de mémoire EWRAM/IWRAM et de taille ROM.

**AUCUN MERGE SUR MASTER.**

Arrête-toi après l'implémentation, les tests et les preuves visuelles pour attendre mon approbation.

Cette quête doit constituer un remerciement personnel aux joueurs qui ont terminé le Médallium, sans remplacer la véritable conclusion de l'histoire.