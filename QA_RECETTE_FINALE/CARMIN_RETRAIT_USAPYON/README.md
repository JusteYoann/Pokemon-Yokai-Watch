# Retrait décoratif d’Usapyon — Carmin

À la demande du créateur, seul le sixième acteur de la carte de l’arène de Carmin est retiré. Ariane reste à sa position. Les dessins, palettes, dialogues, équipe, récompenses, musique et données des espèces sont inchangés. Usapyon reste le quatrième membre de son équipe.

## Compatibilité des sauvegardes

Le marqueur de révision de l’arène passe de 0x32C à 0x32D. Une sauvegarde antérieure chargée dans cette arène est replacée une seule fois à l’entrée intérieure (5,17). Les anciens modèles d’acteurs en cache sont effacés avant de recharger la carte, afin de supprimer aussi le sixième acteur mémorisé. Les continuations suivantes conservent la position. Aucun changement du format des sauvegardes.

## Vérifications effectuées

- Compilations publique et privée réussies; taille privée 31 589 579 octets, sous 32 Mio. Empreintes dans BUILD.json.
- Deux nouvelles parties réellement lancées dans mGBA, garçon et fille, puis fixtures explicites de déplacement et de progression.
- Ariane visible, Usapyon absent de la carte. Captures PNG natives ouvertes et vérifiées.
- Sauvegarde Flash, chargement et Continuer avec un ancien sixième modèle d’acteur injecté et l’ancien marqueur 0x32C : le modèle disparaît, les drapeaux de progression sont conservés. Second Continuer : position conservée.
- Interaction native avec Ariane après migration : menu de combat atteint; équipe générée [96,17,51,100], donc Usapyon toujours présent; musique de combat 377.
- Les fichiers des équipes, dialogues, espèces, sprites, palettes et musiques n’ont pas été modifiés.

Ces tests ciblent ce retrait et sa compatibilité. Ils ne constituent pas une nouvelle traversée complète du jeu ni une nouvelle validation d’équilibrage. Le rapport historique CARMIN_2026_10_22 et ses captures montrant le compagnon décrivent la version précédente.

Reproduction :

```sh
source /workspace/.setup/env.sh
YOKAI_QA_ROM=$PWD/pokefirered_audio.gba YOKAI_QA_ELF=$PWD/pokefirered_audio.elf python3 tools/yokai/tester_retrait_usapyon_carmin_mgba.py
```
