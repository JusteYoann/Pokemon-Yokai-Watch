# Capture des 151 Yo-kai selon leur rang

## Diagnostic

Avant cette correction, les **151 indices de capture** correspondaient
exactement à ceux des Pokémon remplacés. Comparaison effectuée avec la source
historique `ab417d12552b25c8434592a942006cc0219932bf` et avec la table de
`pret/pokefirered` ; provenance et empreinte de cette dernière dans
[SOURCE_ROUGE_FEU.json](SOURCE_ROUGE_FEU.json).

Exemples : Scoltine utilisait l’indice 45 de Grolem ; Chiperpiou, 60 comme
Crustabri ; Whisper, 45 comme Carabaffe ; Granpapéti, 90 comme Rapasdepic.
Ces valeurs étaient sans rapport avec leur rang dans le dossier validé.

## Barème appliqué

Les rangs proviennent du CSV validé
`RECUPERATION_PROJET/sources_validees/REPARTITION_OBTENTION_151_YOKAI_CODEX.csv`.

| Rang | Indice natif GBA |
|---|---:|
| E | 255 |
| D | 225 |
| C | 180 |
| B | 120 |
| A | 75 |
| A/S | 60 |
| S | 45 |
| Z | 30 |

L’indice va de 1 à 255 : plus il est élevé, plus la capture est facile.
**Ce n’est pas un pourcentage et le rang E ne signifie pas une capture garantie
à pleine santé.** Les PV, statuts, Balls, nombres aléatoires et arrondis du
moteur continuent à déterminer l’issue. Certains arrondis natifs peuvent donner
la même probabilité à deux indices pour un état de PV précis.

Le seul rang mixte du dossier, Turboss A/S, reçoit l’indice intermédiaire 60.
Enma, classé Z dans le dossier, passe de 3 à 30. Les indices s’appliquent aux
151 entrées, y compris celles obtenues uniquement par cadeau/évolution : cela
n’ajoute aucune rencontre ni nouvelle méthode d’obtention.

140 indices changent ; les 11 autres correspondent déjà au nouveau barème.
Détail complet : [AUDIT_151.json](AUDIT_151.json).

| Yo-kai | Rang | Avant | Après |
|---|---|---:|---:|
| Scoltine | E | 45 | 255 |
| Chiperpiou | E | 60 | 255 |
| Granpapéti | D | 90 | 225 |
| Whisper | C | 45 | 180 |
| Raltesse | D | 45 | 225 |
| Enma | Z | 3 | 30 |

Le moteur de capture, les restrictions des combats de Dresseurs et des boss,
les bonus des Balls et statuts, ainsi que la conversion des indices au Parc
Safari restent natifs. Aucun autre champ de la table des espèces n’est changé.
Le générateur de reconstruction réapplique également ce barème pour éviter
qu’une génération ultérieure rétablisse les anciens taux Pokémon.

## Vérifications et état de livraison

- Compilation publique et compilation privée avec OST : réussies.
- Lecture dans mGBA des **151 indices réellement liés**, dans les deux builds.
- Comparaison octet par octet de la table complète de 412 entrées avec la
  bêta française initiale : seuls les 140 octets attendus de capture changent ;
  toutes les statistiques, types, talents et autres champs restent identiques.
- Vérification de la monotonie des probabilités calculées avec la formule
  entière native et de l’effet des PV, du sommeil et des Balls. Ces calculs de
  référence ne constituent pas une campagne de captures dans l’émulateur.
- Application répétée du générateur : résultat identique.

Ces contrôles portent sur la table et le calcul de référence, pas sur 151
lancers de Balls ni sur un parcours complet. Le parcours joueur reste arrêté.
Le format des sauvegardes n’est pas modifié ; leurs Yo-kai déjà obtenus ne
sont pas retouchés.

Branche de regroupement : `fix/capture-rangs-yokai-20261024`, incluant les
correctifs précédents de Matt et du duo Ariane. **Aucune nouvelle ROM publiée** :
la livraison attend les autres retours de bêta-test, comme demandé.
Aucune fusion sur master.
