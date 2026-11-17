État du17 novembre : le package Emerald français0.2.1 a été reçu et le dossier `quatre_jeux/` a généré la seed1711202601 avec succès. Le blocage de fichier absent décrit plus bas est historique. Voir `DOCUMENTATION/SEED_QUATRE_JEUX_20261117.md` pour distinguer génération, serveur quatre slots et tests natifs.

# Slots des créateurs

YW1 EUR : Yochix ; YW2 EUR : Juste Yoann ; Rouge Feu : Kammy64 ou Petit Shiny (nom technique `RougeFeu`) ; MKW PAL : Krackonyx ; Emerald : Dejais.

**Premier essai collectif : `quatre_jeux/`.** Quatre YAML uniquement, un par jeu : YW2, FR, MKW, Emerald. Le statut fonctionnel Emerald/YW2/MKW est confirmé par l’utilisateur ; le mod visuel MKW reste à ajouter. Installer le package Emerald français0.2.1 réellement utilisé par Dejais, signature `pokemon emerald / yokai ap fr2`. Ce fichier est absent de l’environnement actuel ; le script de génération bloque plutôt que d’employer une ancienne build. Fournir le package en pièce jointe permet de reprendre. Aucun substitut vanilla.

`jouables/` contient les trois YAML des tests locaux historiques (YW2/FR/MKW). `en_attente/` conserve les anciens modèles, dont YW1 encore absent. Ne pas fournir ces dossiers en même temps au générateur. Le nom « en attente » de l’ancien modèle Emerald ne décrit plus le statut utilisateur de ce jeu.

Paramètres : équilibrage65, accessibilité complète, pièges désactivés, YW2 chapitre10 sans postgame, Emerald Panthéon sans postgame. FR0.5.0 :628 checks et quatre CS de progression ; Terr’heure optionnelle désactivée. Ces paramètres ne garantissent pas une durée d’attente.

Utiliser `SCRIPTS/generate_four_game_seed.py` et lire `DOCUMENTATION/FIRERED_VERSION_TEST_4_JEUX.md`. Le script vérifie la composition des quatre slots et les packages avant génération. Les YAML seuls ne prouvent pas les échanges dans les jeux. Ne jamais renommer un slot après génération.
