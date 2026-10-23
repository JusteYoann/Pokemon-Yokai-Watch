# PROMPT POUR CODEX — Refonte intégrale des 151 shiny (FRLG x Yo-kai Watch)

## Référentiel et périmètre

Repo : JusteYoann/Pokemon-Yokai-Watch.
Ce ZIP contient 63 références d'artwork individuelles, 2 références supplémentaires et
un tableau exhaustif `PALETTES_151.csv` qui associe chaque ID **fixe** de 001 à 151
à sa consigne et à sa référence. Le CSV prévaut sur les anciennes palettes.
Lire `INVENTAIRE_151.md` et `CONSIGNES_VISUELLES.md` avant toute écriture.

**Interdiction absolue de fusionner sur master sans autorisation explicite de Yoann.**
Travailler sur une branche de travail dédiée, avec des commits séparés.
Préserver les 151 SPECIES_* d'origine : aucune renumérotation.
Ne pas toucher à la logique de rencontre (Charme Chroma, Safari x3, taux shiny).
La scène finale Don Morléone / Don Spiraton et le scénario sont hors périmètre.

## Exécution demandée

1. AUDIT LECTURE SEULE : identifier le HEAD exact, l'arborescence de palettes, les sprites
   front/back, les éventuels sprites alternatifs, la génération des palettes et les
   limitations GBA. Relever les écarts entre noms humains et noms internes.
2. Établir pour chaque espèce les zones colorées du NORMAL (peau, cheveux, vêtements,
   armure, ornement, yeux, queue...) et les teintes CIBLES de sa référence.
   Références d'artwork prioritaires; ne pas utiliser les anciens shiny du ROM hack
   comme autorité artistique. Les références ne doivent PAS provoquer un redessin.
3. Pour les familles, reproduire une identité chromatique cohérente sur les zones
   analogues, pas une transplantation naïve des index de palette.
   Les exceptions #002 Bandinyan et #003 Épinyan prévalent sur #001 Jibanyan.
   Pour #008 Whisper, utiliser Whisperocrates. Pour #066/#067, utiliser l'artwork
   supplémentaire de la sirène. Pour #137/#138, SEUL l'œil change.
4. Appliquer aux sprites de face ET de dos et aux palettes réellement utilisées
   en combat, sans changement de forme, d'animation ou de style pixel art.
   Vérifier les contraintes 16 couleurs et les index transparents quand applicables;
   préserver contraste, anti-aliasing d'origine et teintes d'ombrage structurées.
5. PRODUIRE AVANT VALIDATION : planche(s) contact 151 couples NORMAL / SHINY
   numérotés et nommés, avec zoom nearest-neighbor, et rapport par espèce :
   source, palette, éventuelle approximation ou difficulté, face/dos.
   Fournir également les 151 résultats individuels pour inspection.
6. Tests techniques : build(s) disponibles, intégrité des palettes, non-régression,
   absence de débordement de palette, vérification sur émulateur si possible.
   Ne pas affirmer qu'un test a été passé sans l'avoir exécuté.
7. ARRÊT POUR VALIDATION VISUELLE DE YOANN avant intégration définitive
   ou fusion sur master. Signaler chaque anomalie ou référence contradictoire.

## Prudence sur les noms

- La chaîne du dépôt pour #034 est « Métaureau. », alors que des échanges évoquaient
  « Métaurolog ». Ne pas confondre les deux : vérifier le mapping interne et soumettre
  l'ambiguïté si le sprite ne correspond pas au Yo-kai voulu.
- Noms tronqués dans l'UI du jeu : employer impérativement les numéros/constantes
  SPECIES_* du CSV pour identifier les fichiers; ne jamais déduire le mapping du nom.
- Les propositions de couleurs validées ici sont une direction artistique; demander
  arbitrage si un rendu pixel art s'écarte trop d'une référence.

## Livrables attendus

- Branche de travail + commits isolés; **aucun merge**.
- Planche 151 normal/shiny, sprites de face et dos inspectables.
- Tableau d'audit concordant avec le CSV, tests, limites techniques et logs.
- Liste des décisions restant à confirmer si besoin.
