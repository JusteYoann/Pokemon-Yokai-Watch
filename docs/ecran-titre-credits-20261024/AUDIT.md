# Audit avant intégration — écran titre et crédits

Base : `585605095`, après nettoyage des graphismes Pokémon inutilisés. Branche dédiée : `feature/ecran-titre-credits-20261024`. Arbre de travail initial propre ; aucune fusion sur master.

## État constaté

- Entrée et titre personnalisés existants dans `src/yokai_presentation.c`, appelés par `intro.c` et `title_screen.c`. Ils montrent une composition nocturne fixe, des textes et `MUS_YOKAI_CURIOUS`. Le tutoriel Chen est distinct, dans le menu de nouvelle partie.
- Le titre actuel utilise un fondu audio sur START. Le menu standard ne garantit pas explicitement l'arrêt de la BGM : arrêt immédiat à ajouter aux transitions et aux entrées du menu.
- Les crédits utilisent encore le moteur natif dans `src/credits.c`. `MUS_CREDITS` est associé à `MUS_YOKAI_TAKE_CARE`. Ce morceau sert ailleurs et doit être conservé.
- ROM réellement occupée : publique 15 948 716 octets ; privée 31 710 079 octets. Réserve privée sur 32 Mio : 1 844 353 octets. EWRAM : 261 368 octets ; éviter tout gros tampon statique supplémentaire.
- Le MP3 de crédits fourni précédemment est présent. Le nouveau dossier en contient également une copie ; vérifier l'identité des fichiers avant conversion. Durée attendue : environ 255,14 secondes.

## Budget prévisionnel

À 13 379 Hz, DPCM natif, le morceau complet demande 1 760 104 octets : il ne resterait que 84 249 octets avant code, images et tables. À 12 000 Hz, le DPCM complet devrait demander environ 1,58 Mo, laissant environ 266 Ko. Comparer les conversions et mesurer le build final ; aucun raccourcissement du morceau ni retrait d'autre musique autorisé ici.

Le titre utilisera des BG natifs distincts pour fresque, logo et texte. Objectif : fresque 512×160 à palette limitée, tuiles dédupliquées, carte 64×32 ; logo fixe et mélange alpha progressif ; défilement d'environ 2,5 pixels/seconde. Vérifier le nombre de tuiles et les adresses VRAM avant intégration. Les souvenirs seront compressés en tuiles et chargés un par un, sans conserver 32 images en RAM.

## Étapes testables

1. Carton noir silencieux `by Juste Yoann`, logo original fourni, fresque adaptée, cinq secondes de révélation, START et menu silencieux. Captures et comparaison sonore de musiques déjà présentes ; choix présenté comme proposition jusqu'à revue de Yoann.
2. Conversion privée des crédits, ajout isolé d'un nouvel identifiant musical ; préserver les 31 pistes et l'usage de Take Care ailleurs. Vérifier durée, fin, décodage, budget réel et version publique sans audio privé.
3. Préparer les états de jeu et capturer les souvenirs dans mGBA, avec leurs conditions et provenance. Confronter le storyboard aux événements réellement présents. Pierre est remplacé par Wyatt ; Usapion a été retiré de l'overworld de l'enquête. Adaptations soumises à Yoann avant modification de ces intentions.
4. Diaporama de crédits natif : 31 scènes de 7–8 s, finale d'environ 30 s ; vrais sprites pour le groupe, variantes garçon/fille, textes indépendants et fond noir. Aucune illustration générée pour les souvenirs.
5. Compilations publique/privée ; tests boot, présence/absence de sauvegarde, options, retour, nouvelle partie/continuer ; lecture complète des crédits et captures. Revue visuelle et sonore avant toute fusion.

Les timings seront exprimés en images GBA (cadence réelle environ 59,73 Hz) afin d'éviter une dérive de synchronisation sur quatre minutes. L'audit de progression ne doit pas transformer le montage final en nouveau contenu scénaristique ou modifier les drapeaux de sauvegarde.
