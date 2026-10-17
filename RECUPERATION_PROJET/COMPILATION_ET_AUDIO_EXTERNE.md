# Compilation reproductible et audio externe

## Périmètre actuel

Le snapshot récupéré n'intègre pas le gameplay Yo-kai. Les commandes ci-dessous compilent le moteur actif **Rouge Feu d'origine**. Elles ne restaurent pas les fonctionnalités absentes et ne suffisent pas à valider le hack.

La chaîne a été installée sans sudo sous Debian 13 amd64, à partir de paquets vérifiés par APT (signature InRelease et SHA256) et du compilateur public agbcc fixé au commit `da598c1d918402c42c0c0d7128ba14567f3175e9`. Les versions et hashes sont dans `OUTILS_DEBIAN.json`. `INSTALL.md` décrit les autres plateformes ; elles n'ont pas été testées ici.

## Depuis un clone GitHub propre

```sh
git clone --branch recovery/sauvegarde-elements-retrouves https://github.com/JusteYoann/Pokemon-Yokai-Watch.git Pokemon-Yokai-Watch-recovery
cd Pokemon-Yokai-Watch-recovery
# Prérequis Debian : build-essential, git, zlib1g-dev, Python 3.
# Pour les contrôles graphiques : python3-pil, libarchive13.
# Choisir un emplacement personnel hors du dépôt :
export YOKAI_SETUP_DIR=/tmp/yokai-build-tools
bash RECUPERATION_PROJET/scripts/configurer_outils_debian.sh
source "$YOKAI_SETUP_DIR/env.sh"
make -j4
sha1sum -c firered.sha1
sha256sum pokefirered.gba
python3 RECUPERATION_PROJET/scripts/verifier_recuperation.py
python3 RECUPERATION_PROJET/scripts/verifier_archives.py
```

L'installateur télécharge uniquement la chaîne de compilation ; il ne dépend pas des anciens fichiers de jeu privés. Il vérifie les versions et les hashes des paquets verrouillés. Si ces versions ne sont plus proposées par le miroir Debian, utiliser une archive Debian officielle avec signatures/hashes conservés ou mettre à jour le verrou après nouveau contrôle ; ne pas désactiver les vérifications. Les outils agbcc installés dans `tools/agbcc` et les dérivés sont ignorés par Git mais reproductibles depuis leurs sources publiques et le commit fixé.

## Exception musicale obligatoire

**Sans les ressources musicales externes appropriées, une future compilation ne pourra pas être strictement identique musicalement à la version de référence utilisant les OST Yo-kai.**

Les MP3 originaux, échantillons PCM/DPCM et conversions d'enregistrements protégés ne doivent pas être ajoutés au dépôt public. Le paquet externe doit être sauvegardé séparément par le créateur, dans un emplacement privé durable ; un fichier conservé uniquement dans cet environnement n'est pas une sauvegarde fiable. Le dépôt public doit conserver les scripts de génération/import, le format attendu, les paramètres de boucles, les hashes d'assets et leurs identifiants de déclenchement.

### Ce qui est réellement disponible

Les archives originales ont été retéléchargées depuis les pièces jointes historiques et comparées à l'inventaire publié. Les nombres et hashes exacts sont dans `REFERENCES_AUDIO_EXTERNES.json` ; leurs octets restent hors Git. Vérifier un paquet privé fourni séparément :

```sh
python3 RECUPERATION_PROJET/scripts/verifier_audio_externe.py /chemin/prive/archives-ost
```

Ce contrôle est fonctionnel et refuse un paquet dans le checkout public. Il ne convertit ni n'intègre une musique. Les démos MP3 publiques antérieures ne remplacent ni les sources originales ni les assets GBA binaires.

### Ce qui manque encore

Les assets DPCM binaires et scripts privés du prototype ancien n'ont pas été retrouvés. Le mécanisme d'import et le routage audio de la version finale ne peuvent donc pas être présentés comme restaurés. Les vingt OST n'étaient pas intégrées dans les branches publiques retrouvées et ne le sont pas dans cette récupération.

Après récupération ou validation d'une reconstruction, l'import devra prendre un répertoire externe explicite (par exemple `YOKAI_AUDIO_ASSET_DIR`), vérifier les hashes et les en-têtes des fichiers GBA, produire les dérivés localement et contrôler leur taille et les boucles. Un mode `AUDIO=native` pourra conserver l'audio d'origine ; un mode `AUDIO=yokai` devra échouer clairement si une ressource obligatoire manque. **Ces modes sont un contrat d'intégration à réaliser ultérieurement, pas des options déjà ajoutées au Makefile.**

Le build actuel utilise seulement les ressources natives suivies du dépôt et ne requiert pas ce paquet externe. Aucune absence de musique n'est masquée par un faux asset ou un fichier silencieux.
