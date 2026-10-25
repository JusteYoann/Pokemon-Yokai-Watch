# MISSION CODEX — INTÉGRATION DES NOUVELLES QUÊTES POSTGAME

## Projet

Dépôt GitHub : `JusteYoann/Pokemon-Yokai-Watch`

Nous poursuivons le développement de notre ROM hack Pokémon Rouge Feu × Yo-kai Watch.

**Objectif : intégrer l'ensemble des nouvelles quêtes postgame décrites ci-dessous dans la version actuelle du jeu.**

### Consignes impératives

1. Inspecter le dépôt, les branches et les événements déjà implémentés avant toute modification.
2. Travailler sur une branche dédiée, sans fusionner sur `master`.
3. Préserver les fonctionnalités existantes, notamment la Terr'heure, Lavanville, Cramois'Île, la Mafiamille et la conclusion scénaristique avec Don Morléone et Don Spiraton.
4. Ne pas réintroduire les contenus d'une ancienne version abandonnée : Limbes Éternelles, Temple Céleste, Sanctuaire divin et anciennes quêtes associées.
5. Utiliser exclusivement les **151 espèces de Yo-kai du hack**. Aucun Pokémon original ne doit apparaître dans les combats, les rencontres sauvages, les cadeaux ou le postgame.
6. Réutiliser prioritairement les sprites, portraits, musiques et ressources déjà présents dans le dépôt.
7. Vérifier les noms internes et les identifiants des espèces. Ne jamais remplacer silencieusement un Yo-kai demandé par un autre.
8. Respecter les contraintes mémoire de la GBA et surveiller la place disponible.
9. Tester les événements dans mGBA, notamment les conditions de déblocage, les combats, les cadeaux et la persistance des sauvegardes.
10. Fournir une ROM de test et un rapport d'intégration.
11. **Ne rien fusionner sur `master` sans autorisation explicite.**

---

# PARTIE 1 — INTRODUCTION DU POSTGAME : LE SEIGNEUR ENMA

## Déclenchement

Après la première victoire à la Ligue :

- Le joueur reprend son aventure dans sa maison, à Bourg Palette.
- Lorsqu'il sort pour la première fois, une cinématique se déclenche automatiquement.
- Le Seigneur Enma apparaît devant lui.
- La cinématique ne se joue qu'une seule fois par sauvegarde.

Utiliser le sprite overworld actuel du véritable Seigneur Enma, pas celui de l'ancien chat violet.

## Dialogue

**Seigneur Enma :**

« Te voilà enfin, [PLAYER]. »

« Je suis Enma, souverain du Yo-kai World. »

« Depuis quelque temps, ton nom revient souvent parmi les Yo-kai. »

« Tu as traversé Kanto, affronté des adversaires redoutables et mis un terme aux agissements de Don Morléone. »

« Peu de personnes auraient été capables d'un tel exploit. »

« Mais j'ai également entendu parler d'une ambition encore plus étonnante. »

« Tu souhaiterais réunir les 151 Yo-kai de ce monde dans ton Médallium ? »

« Intéressant… »

« Sache que personne n'a encore réussi cet exploit. »

« Si tu y parviens, ton nom restera gravé dans l'histoire du Yo-kai World. »

« Et puisque nous parlons de ton Médallium… »

« Je dois t'avouer quelque chose. »

« J'en fais moi-même partie ! »

« Si tu souhaites devenir mon ami, il faudra cependant me retrouver. »

« Je t'attendrai quelque part dans ce vaste monde. »

« Considère cela comme une dernière épreuve. »

« Encore une fois, merci d'avoir protégé ce monde. »

« J'espère que nos chemins se croiseront bientôt, [PLAYER]. »

Enma disparaît.

## Rencontre statique

Enma reste disponible dans la **Grotte Azurée**, à son emplacement prévu.

- Rencontre accessible dans le postgame.
- Aucun autre prérequis nécessaire.
- Le combat permet sa capture normale.
- Si Enma est mis K.O. sans être capturé, il réapparaît après que le joueur a quitté puis rejoint la zone.
- Une fois capturé, il ne réapparaît plus.

Ne pas confondre le Seigneur Enma avec Enma l'Ancien, membre de la Ligue.

---

# PARTIE 2 — CADEAU DU PROFESSEUR CHEN

Après avoir terminé la Ligue, le joueur peut retourner au laboratoire du professeur Chen.

En lui parlant, Chen propose de lui offrir un Jibanyan supplémentaire.

## Dialogue

**Professeur Chen :**

« Ah, [PLAYER] ! »

« Toutes mes félicitations pour ta victoire à la Ligue ! »

« Tes aventures ont considérablement fait progresser nos connaissances sur les Yo-kai. »

« D'ailleurs, j'ai quelque chose pour toi. »

« Ce petit Jibanyan cherche un nouveau partenaire. »

« Et je ne vois personne de mieux placé que toi pour prendre soin de lui ! »

**Vous obtenez JIBANYAN !**

## Conditions

- Cadeau disponible une seule fois après la Ligue.
- Jibanyan est offert directement.
- Prévoir l'envoi au PC si l'équipe est complète.
- Ne pas supprimer le Jibanyan déjà disponible à Céladopole.
- Conserver les mécanismes d'évolution existants.

---

# PARTIE 3 — PREMIÈRE QUÊTE DE MAÎTRE NYADA

## Localisation

Placer Maître Nyada dans un bâtiment approprié sur **l'Île 7**, de préférence une petite maison tranquille.

Vérifier les emplacements disponibles dans les maps existantes.

Il doit utiliser son sprite overworld déjà prévu.

Maître Nyada est un vieux Yo-kai chat, sage, rusé, parfois malicieux et très puissant.

Il ne doit jamais être écrit comme un vieil homme humain.

Éviter les rires répétitifs du type « Ho ho ho ».

## Déclenchement

La quête est disponible après la Ligue.

### Dialogue initial

**Maître Nyada :**

« Tiens donc… Voilà un visage que je ne connais pas. »

« Tu dois être [PLAYER]. »

« J'ai entendu parler de tes exploits. Impressionnant, pour quelqu'un d'aussi jeune. »

« Dis-moi… Que sais-tu de la guerre contre les Perfides ? »

« Il y a bien longtemps, j'ai combattu aux côtés de deux puissants Yo-kai. »

« Kyubi et Octorgone. »

« Deux guerriers exceptionnels… et deux sacrées têtes de mule. »

« Nous avons traversé bien des épreuves ensemble. »

« Malheureusement, une récente dispute nous a séparés. »

« Ils sont partis chacun de leur côté. »

« J'aimerais savoir ce qu'ils deviennent. »

« Pourrais-tu les retrouver et les convaincre de t'accompagner ? »

« Kyubi se trouve aux Îles Écume. »

« Quant à Octorgone, cherche-le du côté de la Centrale électrique. »

« Ils ne sont pas faciles à approcher. Prépare-toi bien. »

## Objectif

Capturer :

- **Kyubi** — Îles Écume.
- **Octorgone** — Centrale électrique.

### Conditions importantes

- Ces deux rencontres statiques n'apparaissent qu'après activation de la quête.
- Les deux Yo-kai doivent être capturables normalement.
- En cas de K.O. sans capture, ils réapparaissent après avoir quitté puis rejoint leur zone respective.
- Une fois capturés, ils ne réapparaissent plus.
- Ne pas retirer leurs éventuelles apparitions dans les équipes des Dresseurs.
- Vérifier que leur capture est correctement reconnue, même si les deux Yo-kai sont stockés au PC.

### Retour auprès de Nyada

**Maître Nyada :**

« Alors… Tu les as retrouvés ? »

« Kyubi et Octorgone… Tous les deux ! »

« Tu m'impressionnes, [PLAYER]. »

« Ces deux-là sont parmi les plus puissants Yo-kai que j'aie connus. »

« Mais leur véritable force ne vient pas seulement de leurs pouvoirs. »

« Elle vient aussi de ce qu'ils ont traversé. »

« Prends bien soin d'eux. »

« J'espère qu'un jour, ils comprendront que notre amitié vaut davantage qu'une vieille dispute. »

« Tiens, accepte ceci pour te remercier. »

Le joueur reçoit une récompense de valeur.

**Récompense proposée : Œuf Chance**, si cet objet est bien disponible et adapté à l'équilibrage du hack. Signaler tout problème avant substitution.

La première quête est alors terminée.

---

# PARTIE 4 — QUÊTE D'ALIZON BIE : PRÉREQUIS À NYADA II

Cette quête s'appuie sur la **Terr'heure**, dont l'intégration fait l'objet d'un travail séparé.

Ne pas reconstruire ou modifier inutilement son fonctionnement.

## Rappel des conditions

Après la Ligue, Alizon Bie apparaît au sommet de la Tour Pokémon de Lavanville.

Elle explique qu'elle enquête sur les Terr'heures et sur leurs trois Oni.

Elle remet au joueur le **Short Oni**, qui augmente les chances de déclencher une Terr'heure lorsqu'il est équipé.

Le joueur doit vaincre successivement :

1. **Gargaros** — 1 Fouétar niveau 75.
2. **Ogralos** — Carpitaine et Turboss niveau 75.
3. **Orqanos** — 4 Super Fouétar niveau 80.

Vérifier la présence exacte des espèces demandées dans les 151 Yo-kai.

La progression vers l'Oni suivant nécessite une victoire en combat ; une simple fuite par la porte ne suffit pas.

Après les trois victoires, le joueur retourne voir Alizon Bie.

Elle lui donne rendez-vous au **Mont Braise**.

À l'ancien emplacement de la rencontre statique de Maître Nyada, placer **Gorgouille niveau 80**.

- Maître Nyada ne doit plus être présent comme rencontre statique à cet endroit.
- Gorgouille devient une récompense exclusive de cette quête.
- Si Gorgouille est mis K.O. sans être capturé, il réapparaît après sortie et retour dans la zone.
- Une fois capturé, il disparaît définitivement.
- Alizon Bie félicite le joueur et conclut la quête.

**La seconde quête de Nyada ne peut commencer qu'après la fin effective de cette quête d'Alizon Bie, capture de Gorgouille comprise.**

Ne pas créer une situation où une victoire contre les trois Oni suffit alors que Gorgouille n'a pas encore été capturé.

---

# PARTIE 5 — DEUXIÈME QUÊTE DE MAÎTRE NYADA : DÉMOPHAGE

## Conditions

La seconde quête de Nyada devient accessible uniquement si :

1. Sa première quête avec Kyubi et Octorgone est terminée.
2. La quête d'Alizon Bie est entièrement terminée.

Le joueur doit quitter le bâtiment de Nyada, puis revenir lui parler.

## Dialogue

**Maître Nyada :**

« Ah, [PLAYER] ! Comment vas-tu ? »

« Cela faisait un moment. »

« Figure-toi que j'ai quelqu'un à te présenter. »

« Un jeune Yo-kai particulièrement prometteur. »

« Il possède une force incroyable, mais manque encore un peu de confiance en lui. »

« Je l'entraîne depuis quelque temps. »

« Retrouve-moi dans la Grotte Azurée. »

« Je pense que vous aurez beaucoup à apprendre l'un de l'autre. »

## Rencontre dans la grotte

Placer Maître Nyada et Démophage ensemble dans une zone accessible de la Grotte Azurée.

Pendant leur présence, empêcher le déclenchement d'une Terr'heure dans cette grotte.

### Scène

**Maître Nyada :**

« Ah, te voilà ! »

« [PLAYER], je te présente Démophage. »

**Démophage :**

« E-Enchanté ! »

« Maître Nyada m'a beaucoup parlé de vous ! »

**Maître Nyada :**

« Démophage possède une force extraordinaire. »

« Il est même capable de dévorer certains Oni. »

« Mais pour devenir un véritable guerrier, la puissance seule ne suffit pas. »

« Il lui faut un adversaire capable de… »

« … »

*Maître Nyada s'endort soudainement.*

**Démophage :**

« …Maître ? »

« MAÎTRE, RÉVEILLEZ-VOUS ! »

**Maître Nyada :**

« Hein ?! Quoi ?! »

« Ah, oui… Où en étais-je ? »

**Démophage :**

« Vous parliez de mon entraînement, Maître ! »

**Maître Nyada :**

« Exactement. »

« [PLAYER], je voudrais que tu affrontes mon apprenti. »

« Ne te fie pas à sa timidité. »

« Lorsqu'il combat, Démophage est redoutable. »

**Démophage :**

« Je ferai de mon mieux, Maître ! »

« [PLAYER], j'espère que vous êtes prêt ! »

## Combat contre Démophage

Démophage est un Dresseur utilisant son propre portrait de combat et sa propre équipe.

Équipe proposée :

| Yo-kai | Niveau |
|---|---:|
| Scatcheur | 61 |
| Coléroptere | 62 |
| Coach Antonic | 63 |
| Turboss | 64 |
| Démophage | 65 |

Respecter le niveau 65 demandé pour son dernier Yo-kai. Signaler si les tests montrent une difficulté incohérente au vu des prérequis de la quête.

## Après la victoire

**Démophage :**

« Incroyable… »

« Vous êtes vraiment aussi fort que le disait Maître Nyada ! »

**Maître Nyada :**

« Excellent combat. »

« Démophage, qu'as-tu appris ? »

**Démophage :**

« Que même avec une force immense, il me reste encore beaucoup à apprendre ! »

**Maître Nyada :**

« Voilà une bonne réponse. »

**Démophage :**

« [PLAYER]… J'aimerais continuer mon entraînement à vos côtés ! »

« Maître, vous êtes d'accord ? »

**Maître Nyada :**

« Bien entendu. »

« Tu ne progresseras pas en restant toujours dans mon ombre. »

**Vous obtenez DÉMOPHAGE !**

Il s'agit d'un cadeau direct, sans phase de capture.

Prévoir l'envoi au PC en cas d'équipe complète.

## Ticket de la Tour

**Maître Nyada :**

« Avant que tu partes, j'ai une dernière chose pour toi. »

« Prends ce ticket. »

**Vous obtenez le TICKET DE LA TOUR !**

« Il permet d'accéder à la Tour Dresseurs. »

« Les meilleurs combattants de Kanto s'y affrontent. »

« Si tu parviens jusqu'au sommet… »

« Nous nous retrouverons pour une dernière épreuve. »

Fin de la deuxième quête.

---

# PARTIE 6 — TOUR DRESSEURS : ÉPREUVE FINALE DE NYADA

## Accès

La Tour Dresseurs de l'Île 7 reste inaccessible tant que le joueur ne possède pas le Ticket de la Tour.

Préserver la Tour Dresseurs existante de Pokémon Rouge Feu autant que possible.

## Difficulté

Adapter légèrement la difficulté pour la rendre plus accessible :

- Huit étages conservés si compatibles avec la structure actuelle.
- Progression de difficulté raisonnable.
- Pas d'obligation de réussir les quatre modes.
- Une victoire complète dans un seul mode suffit pour débloquer Nyada au sommet.
- Les autres modes restent facultatifs et rejouables.
- Éviter toute pression excessive liée au chronomètre.
- Donner au joueur suffisamment de temps pour choisir ses actions : les types et attaques des Yo-kai sont moins familiers que ceux des Pokémon.
- Conserver la possibilité d'utiliser les objets de soin selon les règles retenues.
- Éviter les compositions artificiellement injustes.
- Les équipes doivent exclusivement utiliser les 151 Yo-kai du hack.

Vérifier le comportement du système de niveaux adaptatifs existant.

## Combat final

Au sommet, Maître Nyada attend le joueur.

**Maître Nyada :**

« Te voilà enfin. »

« Je dois reconnaître que tu as dépassé mes attentes. »

« Tu as retrouvé mes anciens compagnons. »

« Tu as gagné le respect des Oni. »

« Tu as même aidé mon apprenti à progresser. »

« Et maintenant, tu as traversé cette tour. »

« Il est temps de voir ce que tu vaux face à moi. »

« Prépare-toi, [PLAYER]. »

**Combat final contre Maître Nyada.**

Utiliser une équipe de six Yo-kai cohérente avec son identité de maître multitype.

Privilégier son équipe déjà validée pour la Ligue, si elle est présente dans le dépôt.

Respecter notamment ses deux derniers membres :

5. Démophage.
6. Maître Nyada.

Ne pas inventer une nouvelle composition définitive si une équipe validée existe déjà.

## Après la victoire

**Maître Nyada :**

« Je vois… »

« Tu n'as plus besoin de mes épreuves. »

« À présent, c'est toi qui pourrais m'apprendre certaines choses. »

« Tu as mérité bien plus qu'un simple trophée. »

« J'aimerais t'accompagner dans tes prochaines aventures. »

**Vous obtenez MAÎTRE NYADA !**

### Fonctionnement

- Maître Nyada est offert directement.
- Aucune capture nécessaire.
- Cadeau unique par sauvegarde.
- Envoi au PC si l'équipe est complète.
- Nouvelle possibilité de combattre Nyada ensuite, mais sans recevoir un deuxième exemplaire.
- **Maître Nyada ne doit pas être obtenable normalement ailleurs dans le jeu.**

---

# PARTIE 7 — HOVERNYAN : REMATCH À CRAMOIS'ÎLE

Dans le postgame, le joueur peut retrouver Michael/Nathaniel à Cramois'Île.

Respecter son identité, son rôle familial et la chronologie déjà développée autour du passé de Cramois'Île.

Hovernyan doit continuer à se tenir près de lui avec son sprite overworld.

## Déroulement

- Le joueur lui parle après la Ligue.
- Un second combat est proposé.
- Après sa défaite, Michael/Nathaniel décide de confier Hovernyan au joueur.
- Hovernyan est offert directement.
- Cadeau unique.
- Envoi au PC si nécessaire.

### Dialogue proposé

**Michael/Nathaniel :**

« Tu as beaucoup changé depuis notre dernière rencontre. »

« J'aimerais voir jusqu'où tu as progressé. »

Après sa défaite :

« Impressionnant… »

« Je crois qu'Hovernyan et toi avez encore beaucoup de choses à accomplir ensemble. »

« Prends bien soin de lui. »

**Vous obtenez HOVERNYAN !**

Adapter les dialogues à ceux déjà présents dans le jeu et préserver les événements de la phase C.

---

# PARTIE 8 — QUÊTE DU SCIENTIFIQUE : LE GÉNIE INCOMPRIS

## Principe

Ajouter un scientifique récurrent, très prétentieux, persuadé d'être un génie de la robotique.

Après chaque défaite, il s'énerve, annonce une nouvelle invention et change de ville.

Quête facultative disponible après la Ligue.

## Rencontre 1 — Lavanville

Le scientifique est particulièrement visible puisqu'il est le seul humain ordinaire dans les environs.

**Scientifique :**

« Ah ! Enfin quelqu'un de normal dans cette ville ! »

« Écoute-moi bien, jeune Dresseur. »

« Tu as devant toi un véritable génie de la robotique ! »

« Après des années de recherches, j'ai conçu un Yo-kai absolument révolutionnaire ! »

« Une merveille de technologie ! »

« ADMIRE… ROBONYAN ! »

**Combat : Robonyan niveau 60.**

Après sa défaite :

« QUOI ?! »

« Impossible ! Mes calculs étaient parfaits ! »

« Ça ne peut être qu'un défaut de fabrication… »

« Peu importe ! Je vais améliorer mon invention ! »

« Et la prochaine fois, tu vas le regretter ! »

Le scientifique disparaît de Lavanville.

## Rencontre 2 — Carmin-sur-Mer

Le scientifique se trouve près du port.

**Scientifique :**

« TOI ?! »

« Parfait ! Justement, je te cherchais ! »

« J'ai compris pourquoi tu avais gagné la dernière fois. »

« Mon précédent modèle était technologiquement dépassé ! »

« Mais cette fois, j'ai corrigé absolument TOUS ses défauts ! »

« Plus rapide ! Plus puissant ! Plus intelligent ! »

« Voici… ROBONYAN F ! »

**Combat : Robonyan F niveau 65.**

Après sa défaite :

« NON ! NON ! NON ! »

« Mais comment c'est possible ?! »

« J'ai pourtant dépensé toutes mes économies dans cette amélioration ! »

« Très bien. Tu ne me laisses pas le choix. »

« Je vais concevoir le modèle ULTIME ! »

« Notre prochaine rencontre sera la dernière ! »

## Rencontre 3 — Safrania

Placer le scientifique près de l'entrée de Yopple.

**Scientifique :**

« … »

« Je savais que tu viendrais. »

« Cette fois, je ne vais pas perdre mon temps avec de grands discours. »

« J'ai investi jusqu'à mon dernier centime dans ce projet. »

« Des années de recherches, des centaines de prototypes et des milliers d'heures de travail… »

« Tout ça pour créer une seule chose. »

« Le Yo-kai parfait. »

« ROBONYAN 28 ! »

**Combat : Robonyan 28 shiny niveau 70.**

Après sa défaite :

« … »

« … »

« J'ABANDONNE !!! »

« La robotique, c'est terminé ! »

« Toutes ces années à construire des machines pour qu'un gamin vienne les démolir en cinq minutes ! »

« Franchement, les Yo-kai robots, c'est NUL ! »

« Tu sais quoi ? Je vais rentrer chez moi. »

« Je vais devenir streamer. »

« Au moins, je pourrai jouer aux jeux vidéo toute la journée ! »

« Tiens, prends cette ferraille. J'en veux plus ! »

**Vous obtenez ROBONYAN 28 shiny !**

« Et surtout, ne viens pas me demander de le réparer ! »

« Maintenant, si tu veux bien m'excuser, j'ai une carrière sur Internet à commencer ! »

Le scientifique disparaît définitivement.

## Contraintes

- Les rencontres sont strictement séquentielles.
- Le Robonyan 28 offert doit être réellement shiny dans ses données.
- Utiliser la palette shiny standard actuelle de Robonyan 28, sans recréer une variante spéciale.
- Cadeau unique.
- Envoi au PC si l'équipe est complète.
- Cette quête ne bloque pas l'obtention normale de Robonyan ni de Robonyan 28.
- Vérifier que Robonyan F est effectivement disponible parmi les 151 espèces.
- Si Robonyan F n'existe pas dans le roster, signaler ce blocage sans créer arbitrairement une 152e espèce.

### Dialogue facultatif après la quête

Un employé de Yopple peut dire :

« Un scientifique bizarre traînait ici l'autre jour… »

« Il criait qu'il allait devenir une star d'Internet. »

« Je me demande ce qu'il est devenu… »

---

# PARTIE 9 — AUDIT DES 151 YO-KAI

Le ROM hack utilise uniquement 151 Yo-kai.

Effectuer un audit des contenus postgame pour empêcher toute apparition d'un Pokémon original provenant des générations supplémentaires.

Vérifier :

- Rencontres sauvages.
- Dresseurs des Îles Sevii.
- Dresseurs de la Tour Dresseurs, dans tous les modes.
- Cadeaux.
- Échanges.
- Œufs et reproductions.
- Évolutions.
- Événements scriptés.
- Rencontres statiques.
- Équipes des rematchs.

Ne pas modifier inutilement le système interne des identifiants Pokémon.

L'objectif est que **toutes les espèces réellement rencontrables ou obtenables dans le jeu soient exclusivement les 151 Yo-kai validés**.

Préserver le fonctionnement du Médallium.

---

# PARTIE 10 — MÉDALLIUM ET COMBAT SECRET CONTRE JUSTE YOANN

Cette séquence a déjà été conçue précédemment.

**Avant toute modification, rechercher son implémentation actuelle et vérifier qu'elle fonctionne. Ne pas la réécrire inutilement.**

Rappel des conditions :

1. Le joueur complète les 151 entrées du Médallium.
2. Il retourne voir le professeur Chen.
3. Chen lui annonce que quelqu'un l'attend chez lui.
4. Juste Yoann apparaît dans la maison du joueur.
5. Le joueur peut lui parler et l'affronter.

## Équipe de Juste Yoann

Six Yo-kai autour du niveau 70 :

- Démophage.
- Démophage.
- Fouétar.
- Camaueil.
- Terminyanator.
- Seigneur Enma.

Après sa défaite, Yoann :

- Félicite le joueur.
- Admet ne pas être le meilleur stratège : « Nyleco est bien meilleur que moi. »
- Remercie le joueur d'avoir joué au jeu, de suivre sa chaîne YouTube et de soutenir ses projets.
- Exprime son ambition d'aller très loin et son espoir que le joueur sera présent lorsque cela arrivera.

L'écran devient progressivement blanc.

Afficher :

**THANK FOR PLAY**

Puis l'écran revient à la normale.

Yoann offre le **Charme Chroma**.

Conserver le cumul du Charme Chroma avec le bonus shiny ×3 du Parc Safari.

Cette conclusion doit rester accessible : vérifier que les 151 Yo-kai peuvent réellement être obtenus dans une même sauvegarde.

---

# PARTIE 11 — ORDRE GLOBAL ET DÉPENDANCES

Respecter ce schéma de progression :

```text
VICTOIRE À LA LIGUE
│
├── Rencontre avec le Seigneur Enma
│   └── Capture d'Enma dans la Grotte Azurée
│
├── Professeur Chen
│   └── Cadeau : Jibanyan
│
├── Michael / Nathaniel à Cramois'Île
│   └── Rematch → Cadeau : Hovernyan
│
├── Scientifique
│   ├── Lavanville : Robonyan
│   ├── Carmin-sur-Mer : Robonyan F
│   └── Safrania : Robonyan 28 shiny
│
├── MAÎTRE NYADA — QUÊTE I
│   └── Capturer Kyubi et Octorgone
│       └── Récompense de Nyada
│
└── ALIZON BIE — TERR'HEURE
    └── Vaincre Gargaros, Ogralos et Orqanos
        └── Capturer Gorgouille au Mont Braise

NYADA I + ALIZON BIE TERMINÉES
│
└── MAÎTRE NYADA — QUÊTE II
    └── Combat contre Démophage
        ├── Cadeau : Démophage
        └── Ticket de la Tour
            └── TOUR DRESSEURS
                └── Battre Nyada au sommet
                    └── Cadeau : Maître Nyada

151 YO-KAI ENREGISTRÉS
│
└── Professeur Chen
    └── Rencontre secrète avec Juste Yoann
        └── Cadeau : Charme Chroma
```

---

# PARTIE 12 — VALIDATIONS ET TESTS

Avant de considérer la mission terminée, tester au minimum :

### Progression

- Les événements postgame sont bloqués avant la Ligue.
- Les cinématiques uniques ne se rejouent pas.
- Chaque quête conserve sa progression après sauvegarde et rechargement.
- Les conditions de déblocage sont respectées.
- Aucune quête ne peut être bloquée définitivement par erreur.

### Captures

- Kyubi, Octorgone, Enma et Gorgouille réapparaissent après un K.O. sans capture.
- Ils ne réapparaissent plus après capture.
- Les captures sont correctement enregistrées dans le Médallium.

### Cadeaux

- Jibanyan, Hovernyan, Démophage, Maître Nyada et Robonyan 28 shiny sont bien reçus.
- Les cadeaux ne peuvent pas être obtenus plusieurs fois.
- Une équipe complète ne provoque pas la perte d'un cadeau.
- Robonyan 28 possède bien l'attribut shiny.

### Tour Dresseurs

- La tour refuse l'accès sans ticket.
- L'accès est débloqué après la quête de Démophage.
- Les équipes n'utilisent aucun Pokémon original.
- La difficulté reste raisonnable.
- Le combat contre Nyada fonctionne.
- Le cadeau final est unique.

### Compatibilité

- Les événements existants ne sont pas cassés.
- La Terr'heure fonctionne toujours.
- Les entrées et sorties de zones restent valides.
- Aucun personnage ne bloque un passage essentiel.
- Aucun dialogue ne déborde ou ne s'affiche incorrectement.
- La ROM compile et fonctionne dans mGBA.
- La consommation de mémoire reste acceptable.

---

# LIVRABLES ATTENDUS

À la fin du travail, fournir :

1. La branche contenant les modifications.
2. La liste des fichiers modifiés.
3. Un récapitulatif précis des quêtes intégrées.
4. Les éventuelles différences entre la demande et l'implémentation.
5. Les contrôles et tests réalisés.
6. Une ROM `.gba` de test.
7. Si possible, quelques captures ou GIF des principales nouvelles cinématiques.
8. Une liste des problèmes restants.

**Ne pas fusionner sur `master`.**

Si une incompatibilité majeure apparaît, notamment une espèce absente des 151, un manque de mémoire ou un conflit avec une quête existante, arrêter la partie concernée et demander une décision. Ne pas remplacer silencieusement le contenu validé.

L'objectif est de produire un postgame riche, cohérent et entièrement jouable, sans dénaturer l'aventure principale ni rendre le 100 % inutilement pénible.