# Dialogues restaurés : état de travail

## Ariane Célestin et Usapion — intégré

Références visuelles consultées : `Ariane Celestin.webp` et `100 - Usapion.webp`, récupérables dans les archives de références sauvegardées. Les dialogues sont des adaptations originales, pas des citations officielles. Ton retenu : curiosité enthousiaste, notes et essais de stratégie, sans exposition lourde de l’histoire Yo-kai Watch. Une documentation narrative officielle plus complète reste à établir pour la recette finale.

| Scène | Comportement et texte |
|---|---|
| Introduction | « Un nouveau mystère ! Tes Yo-kai m’intriguent. Usapion et moi, on est prêts ! Tu veux faire un combat ? » |
| Refus | « Pas de souci ! On reste ici encore un peu. » Aucun combat ou flag de victoire. |
| Avant combat aventure | « Allons-y, Usapion ! On va leur montrer ! » |
| Avant combat postgame | « Emperor et moi avons progressé ! À toi de le découvrir ! » |
| Défaite d’Ariane | « Mes calculs étaient presque bons ! Bon, je vais les revoir… » |
| Après victoire | Admiration pour l’équipe du joueur, prise de notes et essai d’une autre stratégie. |
| Cadeau | Pierre Lune, avec indication de l’évolution d’Usapion. Une seule par sauvegarde. |
| Sac plein | « Ton sac est plein. Je te garde la Pierre Lune ! » Le prochain échange suffit. |
| Revisite avant Ligue | Recherches avec Usapion et proposition de revenir après la Ligue. |
| Usapion | Il vérifie son équipement et semble prêt pour l’aventure. |

Texte exact avec sauts de ligne : `data/maps/Route25/scripts.inc`. Les accents et contrôles sont compilés dans la ROM. Le caméo Enma est décrit ci-dessous ; les autres scènes restent à reconstruire. Les équipes des boss verrouillés ne sont pas modifiées par ce chantier.


## Seigneur Enma — épreuve partagée avec la quête 8

Personnalité fondée sur les indications explicites du cahier MUSIQUES_QUETES : énergique, joueur, curieux des humains, admiratif après un beau combat ; pas de souverain froid ou pompeux. Les répliques sont des adaptations originales pour ce hack, pas des citations officielles.

- Première proposition : félicitations pour la Ligue, présentation et curiosité pour la force du joueur, choix Oui/Non.
- Refus : invitation à prendre son temps et à préparer un beau combat ; aucune victoire enregistrée.
- Victoire du joueur : admiration pour le lien avec ses Yo-kai et annonce explicite de l'apparition d'Enma dans la Caverne Azurée.
- Revisite : proposition volontaire de revanche, puis enthousiasme renouvelé après victoire. Aucun cadeau d'objet ni deuxième déblocage.
- Rencontre sauvage : « Enma te lance un regard déterminé ! » à l'emplacement original de Mewtwo.

Texte complet : `data/maps/MtEmber_Summit/scripts.inc` et `data/maps/CeruleanCave_B1F/scripts.inc`. Les 56 lignes ajoutées d'Ariane/Enma sont mesurées avec la fonction native GetStringWidth dans mGBA : `LARGEURS_DIALOGUES_CAMEOS.json`. Deux lignes dépassaient 208 pixels et ont été reformulées. Les musiques DPCM de présentation et de combat restent nécessaires pour achever la quête 8.
