# Développement actif Pokémon × Yo-kai Watch

Branche : `dev/reconstruction-finalisation`. **NON PRÊT — reconstruction en cours.** `master` et la branche de récupération restent préservés. Les rapports de récupération décrivent un instantané historique ; leurs contrôles d'identité avec Rouge Feu original ne s'appliquent plus à cette branche modifiée.

## Compiler et contrôler

Debian 13 amd64 : `bash RECUPERATION_PROJET/scripts/configurer_outils_debian.sh`, puis `source /workspace/.setup/env.sh` et `make -j4`. Les instructions générales des autres plateformes restent dans INSTALL.md. La ROM est un dérivé local ignoré ; ne pas la publier.

`python3 tools/yokai/verifier_rom.py` contrôle les données réellement liées dans la ROM, les 151 noms abrégés, statistiques et talents, les 56 évolutions et les 906 ressources graphiques. Ce contrôle est distinct d'une recette dans mGBA. Ne pas utiliser `firered.sha1` comme hash attendu du hack.

## Premier jalon reconstruit

- 151 noms canoniques dans les sources, avec abréviations de 10 caractères terminées par un point si nécessaire ; correspondances SPECIES_* inchangées. Table des noms affichés dans data/yokai/noms_affiches.json.
- Statistiques, types et talents validés actifs pour les 151 espèces.
- 56 évolutions actives, sans les anciennes évolutions croisées vers des espèces hors roster. Méthode Noko : amitié >=220 et Œuf Chance tenu, montée de niveau, objet non consommé.
- 151 listes CT/CS actives.
- 151 faces et dos, icônes et empreintes récupérés intégrés. 14 redesigns approuvés appliqués exclusivement. Les 137 autres graphismes normaux et les icônes/empreintes sont comparés aux octets historiques.
- Croissance harmonisée MEDIUM_FAST pour les 151 afin d'éviter des sauts de niveau lors d'une évolution entre anciens emplacements aux courbes incompatibles ; choix secondaire non fixé par les CSV, documenté ici.

## Reste à reconstruire et vérifier

Listes d'attaques complètes et attaques à l'évolution ; obtentions/scripts/rencontres et équipes validées ; Nathan/Katie/Matt ; caméos ; partage Exp. ; noms de capacités/talents et dialogues français ; shiny finaux et verrou des 67 exclus ; musiques DPCM ; dix quêtes ; recette complète et contrôle d'un clone propre.

Les palettes shiny actuellement raccordées sont HISTORIQUES, pas une validation de la direction artistique finale. Aucune fonctionnalité non testée ne doit être annoncée terminée. Les états et preuves sont conservés dans QA_RECETTE_FINALE/RECONSTRUCTION/.

Les fichiers PNG/palettes sont les sources maintenables. Les .4bpp/.gbapal/.lz sont générés par le build et ignorés. Le script outils/yokai est `tools/yokai/reconstruire_base.py` ; il reconstruit le premier jalon depuis les sources validées et l'instantané original. Ne pas le relancer aveuglément après des retouches ultérieures : il réécrit ses fichiers de sortie, dont les palettes historiques.
