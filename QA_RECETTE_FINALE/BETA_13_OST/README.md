# Bêta de développement B13 — 18 octobre 2026

**Bêta B13-20261018 — ce n’est pas la version 1.0 finale.**

Ce paquet documentaire identifie la ROM existante, sans recompilation, changement de titre interne ni modification du jeu. Il ne contient ni ROM commerciale, ni enregistrements musicaux, ni échantillons protégés.

| Référence | Valeur |
|---|---|
| Branche | `dev/reconstruction-finalisation` |
| Jalon GitHub épinglé | `822ea2de1951bf46e12cbda6146fae8873532060` |
| Dernier commit modifiant le contenu compilé | `f029b5236e34f9571f48fb928020f5adcff5debc` |
| OST actives | 13 sur les 15 sélectionnées |
| Taille privée | 24 400 776 octets, soit 23,27 Mio |
| SHA-256 privé | `36bbf1f1c759f0e355be122caf68d7d110f86c83c1862bda1e85c72ea37abfc5` |

Les publications documentaires ultérieures ne changent pas ces octets. Le manifeste machine est `BETA.json`. La copie privée conservée dans l’environnement est `/workspace/private-builds/pokemon-yokai-watch-dev-13ost/pokemon-yokai-watch-dev-13ost.gba` ; ce chemin n’est pas un téléchargement GitHub.

**Sous Windows : suivre [WINDOWS_MGBA.md](WINDOWS_MGBA.md)** et son script dédié pour produire directement le fichier `.gba` dans `C:\YokaiBeta`.

## Obtenir la bêta sans redistribuer les ressources protégées

La méthode fournie est une **reconstruction locale** : aucun patch contenant les enregistrements ni ROM complète n’est publié. Utiliser uniquement les archives musicales auxquelles vous avez légalement accès. Les archives personnelles restent hors du dépôt ; ne fournir qu’une copie de chaque lot pour éviter des références audio en double. Le moteur de décompilation ne nécessite pas de ROM commerciale d’entrée ; sa compilation ne confère aucun droit de redistribution des ressources du jeu.

Environnement de référence : Debian 13 amd64, éventuellement dans une VM sous Windows. Voir aussi [INSTALL.md](../../INSTALL.md) dans le dossier racine du dépôt pour les prérequis généraux. L’installateur épinglé ci-dessous requiert notamment Git, make, GCC/G++, Python 3 et les en-têtes zlib. FFmpeg doit être **7.1.5-0+deb13u1**, comme pour le jalon vérifié ; une autre version peut produire des WAV différents, rejetés par les contrôles. Ne pas désactiver ces contrôles.

Dans un dossier neuf, avec vos archives RAR musicales dans un dossier séparé :

```bash
set -euo pipefail
# Préparation Debian : droits d’administration nécessaires pour ces paquets.
sudo apt-get update
sudo apt-get install git build-essential zlib1g-dev python3 python3-venv libarchive13t64 ffmpeg

git clone --branch dev/reconstruction-finalisation https://github.com/JusteYoann/Pokemon-Yokai-Watch.git pokemon-yokai-beta-b13
cd pokemon-yokai-beta-b13
git checkout --detach 822ea2de1951bf46e12cbda6146fae8873532060

export YOKAI_SETUP_DIR="$PWD/../outils-beta-b13"
bash RECUPERATION_PROJET/scripts/configurer_outils_debian.sh
source "$YOKAI_SETUP_DIR/env.sh"
python3 -m venv "$YOKAI_SETUP_DIR/venv"
source "$YOKAI_SETUP_DIR/venv/bin/activate"
python -m pip install -r tools/yokai/requirements-audio.txt
ffmpeg -version

# Adapter ce chemin : toutes les archives de référence, y compris leurs lots complémentaires.
archives_dir=/chemin/vers/mes_archives_musicales
private_dir="$(cd .. && pwd)/audio-prive-beta-b13"
python tools/yokai/extraire_audio_prive.py --output "$private_dir/extracted" "$archives_dir"/*.rar
python tools/yokai/preparer_ost_dpcm.py --extracted-manifest "$private_dir/extracted/manifest-private.json" --private-output "$private_dir/sources" --jobs 4
python tools/yokai/generer_audio_prive.py --full-source-dir "$private_dir/sources" --output "$private_dir/integration" --jobs 4
make -j4 YOKAI_AUDIO_DIR="$private_dir/integration"

python - <<'PY'
import hashlib, pathlib, shutil
rom = pathlib.Path('pokefirered_audio.gba')
expected = '36bbf1f1c759f0e355be122caf68d7d110f86c83c1862bda1e85c72ea37abfc5'
actual = hashlib.sha256(rom.read_bytes()).hexdigest()
assert actual == expected, f'ROM différente : {actual} ; ne pas la présenter comme B13 vérifiée'
assert rom.stat().st_size == 24400776
out = pathlib.Path('../pokemon-yokai-BETA-B13-20261018.gba')
shutil.copyfile(rom, out)
print(out.resolve(), actual)
PY
```

Si une source manque, fournir le fichier correspondant depuis ses propres archives ; ne pas remplacer une piste ni contourner son empreinte. Les 15 références sont recensées dans `QA_RECETTE_FINALE/INTEGRATION_MUSIQUES/SOURCES_V1.json` ; le profil n’active que les 13 validées.

Cette chaîne a déjà produit une ROM **octet pour octet identique** depuis un clone GitHub propre et des échantillons régénérés indépendamment ; voir `../VERSION_1_DEVELOPPEMENT/REPRODUCTIBILITE.json`. Ce contrôle a été fait sur la même machine cloud, pas dans une nouvelle VM. La commande complète n’a pas été rejouée pour cette livraison : la ROM existante a été conservée et vérifiée.

Sans les archives musicales, `make -j4` compile la variante publique de repli, **sans les 13 OST Yo-kai** : elle n’est donc pas cette bêta musicale. Sa SHA-256 est `7f4248b27ec01f4d32acdcacc11c3b1bb5f03ef434431bea099ba85d1496b4ac`.

## Jouer dans mGBA

Ouvrir `pokemon-yokai-BETA-B13-20261018.gba` dans une version récente de mGBA. Créer une nouvelle partie ; utiliser le menu du jeu **Sauvegarder**, puis **Continuer** au lancement suivant. Conserver le fichier `.sav` à côté de la ROM avec le même nom de base, dans un dossier accessible en écriture. Le format de sauvegarde est Flash 128 Kio. Faire une copie de toute ancienne sauvegarde avant un essai ; sa migration depuis d’anciens jalons n’est pas validée.

`TEST_BETA_MGBA.json` décrit le contrôle réel sur l’empreinte privée ci-dessus : introduction et prénom au clavier pour Nathan et Katie, menu Sauvegarder, export de la Flash vers un fichier `.sav`, fermeture de l’émulateur, nouvelle instance et rechargement par Continuer. Captures dans `preuves/`. Le démarrage, Nouvelle partie, l’introduction, le menu Sauvegarder et Continuer sont parcourus par entrées de manette ; aucun appel RPC n’initialise la partie ou n’écrit la sauvegarde. Cela ne constitue pas une partie complète. Aucun fichier de sauvegarde de test n’est distribué au joueur.

## Réserves connues

Les captures avant sauvegarde et après Continuer sont strictement identiques pour chacun des deux protagonistes. Une première suspicion visuelle de décor noir après rechargement a été écartée par cette comparaison : le cadrage était déjà identique avant sauvegarde. Aucun correctif ni changement de ROM n’a été appliqué.

- Enma Track et Final Battle – Are You Ready? restent en repli natif ; seules 13 OST sont actives.
- Direction artistique shiny non finalisée ; cornes de Robonyan 28 non actives. Le verrou sans statut shiny des 67 espèces exclues est conservé.
- Traduction française et références contextuelles encore incomplètes.
- Équilibrage et progression naturelle jusqu’aux niveaux 60–70 non validés par une partie intégrale.
- Aventure principale, postgame et obtention effective des 151 sur une seule sauvegarde pas intégralement parcourus.
- Contrôles automatisés des 354 animations réalisés, mais revue visuelle humaine exhaustive et mesure sur matériel GBA non réalisées.

Les dix nouvelles quêtes et autres ajouts reportés par les dernières directives ne sont pas annoncés comme présents. Les fonctions du jalon restent inchangées. **Bêta pour essais ; NON PRÊT pour une sortie 1.0 finale.** La mission de finalisation reste ouverte.
