# Obtenir un vrai fichier .gba sous Windows — bêta B13

La ROM privée existe encore : **24 400 776 octets (23,27 Mio)**, avec **13 OST**. Elle a été vérifiée sans recompilation. Aucun mécanisme de pièce jointe privée de fichier n’est disponible dans cet environnement ; le fichier n’est pas publié sur GitHub. La procédure ci-dessous construit **le véritable fichier `.gba` sur votre ordinateur**, à partir des sources publiques et de vos propres archives musicales. Aucun patch à appliquer, aucun enregistrement musical téléchargé par le script.

Version **BETA-B13-20261018**, pas une version 1.0. Dernier jalon fonctionnel testé : [`ff1cb36b2ecbe7b8ce167e375a6bff378df31347`](https://github.com/JusteYoann/Pokemon-Yokai-Watch/commit/ff1cb36b2ecbe7b8ce167e375a6bff378df31347), branche `dev/reconstruction-finalisation`. Les publications suivantes ne concernent que la livraison et sa documentation. Les derniers changements des sources compilées remontent à `f029b5236e34f9571f48fb928020f5adcff5debc`.

## 1. Installer Debian dans WSL2

Dans **PowerShell en administrateur**, sous Windows 10 compatible WSL2 ou Windows 11 :

```powershell
wsl --install -d Debian
```

Redémarrer si Windows le demande. Ouvrir Debian et créer le compte Linux et son mot de passe si demandé. Pour une installation WSL existante, conserver ses distributions et données ; ne pas désinscrire ni réinitialiser de distribution. Vérifier :

```powershell
wsl --list --verbose
wsl -d Debian -- cat /etc/debian_version
wsl -d Debian -- uname -m
```

La méthode reproductible exige **Debian 13, architecture x86_64**, et idéalement WSL2. Si Debian est déjà une autre version, ne pas lancer de mise à niveau aveugle ; utiliser une installation Debian 13 distincte. Cette procédure n’est pas validée sur Windows ARM.

## 2. Préparer vos ressources

Dans PowerShell :

```powershell
New-Item -ItemType Directory -Force C:\YokaiBeta\archives
```

Copier dans `C:\YokaiBeta\archives` **vos archives musicales Yo-kai Watch légalement obtenues**, avec les lots complémentaires nécessaires. Une seule copie de chaque lot : des références audio en double sont refusées. Ne pas utiliser les archives de sprites à leur place. Les titres exacts attendus figurent dans [SOURCES_V1.json](../INTEGRATION_MUSIQUES/SOURCES_V1.json) ; les 15 sources sont attendues par le préparateur, mais seules les 13 pistes validées seront activées. Les deux autres restent en repli natif.

Il faut une connexion Internet pour installer les outils et récupérer les sources. Les archives et les échantillons restent sur votre ordinateur. Prévoir de l’espace pour le compilateur, les sources et les fichiers audio décompressés, au-delà des 23,27 Mio du résultat.

## 3. Télécharger et exécuter le compilateur de bêta

Dans PowerShell normal :

```powershell
Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/JusteYoann/Pokemon-Yokai-Watch/dev/reconstruction-finalisation/QA_RECETTE_FINALE/BETA_13_OST/compiler_beta_windows_wsl.sh' -OutFile 'C:\YokaiBeta\compiler_beta_windows_wsl.sh'
wsl -d Debian -- bash /mnt/c/YokaiBeta/compiler_beta_windows_wsl.sh /mnt/c/YokaiBeta/archives /mnt/c/YokaiBeta
```

Le script demande le **mot de passe Debian** pour installer les dépendances avec `sudo` ; aucun mot de passe GitHub n’est requis pour cloner le dépôt public. Il crée un nouveau dossier Linux pour chaque tentative et ne touche pas à vos autres clones. La compilation se fait sur le disque Linux de WSL, puis le résultat validé est copié sur Windows. Il épingle le commit du jalon B13 et ne modifie ni `master` ni les sources du jeu.

Le script exige FFmpeg **7:7.1.5-0+deb13u1** et les outils épinglés du dépôt. Si cette version n’est plus proposée par Debian, il s’arrête : conserver le message d’erreur pour préparer une chaîne archivée vérifiée. Ne pas enlever la vérification SHA-256 ni remplacer arbitrairement le décodeur. Si une référence manque, le script précise le titre ; fournir cette référence depuis vos archives avant de réessayer.

## 4. Ouvrir le résultat dans mGBA Windows

À la fin, le fichier est :

```text
C:\YokaiBeta\pokemon-yokai-BETA-B13-20261018.gba
```

Le fichier `.manifest.json` voisin identifie la version. Dans PowerShell :

```powershell
(Get-Item C:\YokaiBeta\pokemon-yokai-BETA-B13-20261018.gba).Length
Get-FileHash C:\YokaiBeta\pokemon-yokai-BETA-B13-20261018.gba -Algorithm SHA256
```

Résultats attendus : **24400776 octets**, SHA-256 :

```text
36bbf1f1c759f0e355be122caf68d7d110f86c83c1862bda1e85c72ea37abfc5
```

Ouvrir **ce `.gba`** dans mGBA Windows via **File → Load ROM**. Utiliser une nouvelle partie et le menu **Sauvegarder** du jeu, puis **Continuer** au lancement suivant. Le fichier de sauvegarde Flash est de 128 Kio ; garder son nom de base identique à celui de la ROM et conserver le dossier accessible en écriture. Sauvegarder à part ses anciennes parties : leur migration n’est pas validée.

La variante `make` publique sans archives musicales donne aussi un `.gba`, mais sans les 13 OST Yo-kai ; ce n’est pas la bêta musicale décrite ici.

## Tests réellement effectués et limites

Sur la ROM privée de cette empreinte, mGBA libretro a démarré, parcouru Nouvelle partie et l’introduction, accepté un prénom personnalisé, puis créé une sauvegarde par le menu du jeu pour **Nathan et Katie**. La Flash a été exportée vers un vrai `.sav`, puis rechargée par **Continuer dans une nouvelle instance** ; prénom, sexe et carte sont conservés et les captures avant/après sont identiques. Voir [TEST_BETA_MGBA.json](TEST_BETA_MGBA.json) et [les captures](preuves/).

La chaîne Linux sous-jacente a déjà produit la même ROM depuis un clone GitHub propre et des ressources privées régénérées : [preuve de reproductibilité](../VERSION_1_DEVELOPPEMENT/REPRODUCTIBILITE.json). **Cette nouvelle enveloppe Windows/WSL n’a pas été exécutée sur un PC Windows dans cet environnement Linux** ; sa syntaxe et l’étape d’export/SHA-256 ont été vérifiées. Cela ne remplace pas un test Windows réel.

Problèmes connus : deux OST non finalisées (Enma Track et Final Battle – Are You Ready?), dessins shiny et cornes shiny de Robonyan 28 encore à finaliser, français partiel, équilibrage et parcours intégral principal/postgame non validés. Les 67 espèces exclues restent sans statut shiny. Les dix nouvelles quêtes reportées ne sont pas annoncées comme intégrées. **Bêta pour essais, pas une sortie finale validée.** [Rapport complet](README.md).


## Si la taille est correcte mais le SHA-256 diffère

**Ne pas changer le SHA attendu et ne pas refaire toute la compilation.** Le script de compilation mis à jour produit désormais automatiquement `diagnostic-b13.json` en cas d’échec final ; pour la tentative déjà conservée, utiliser la procédure de diagnostic ci-dessous. Le préfixe du SHA et la taille ne localisent pas les différences. Conserver le dossier `/home/yoann/yokai-beta-b13.…` affiché par le script.

Le générateur original valide déjà l’empreinte des WAV actifs avant compilation. Atteindre le contrôle final rend peu probable une mauvaise référence musicale, mais il faut également comparer les DPCM et les sections réellement liées. Une nouvelle compilation propre du même commit a encore produit l’empreinte B13 attendue dans l’environnement de référence ; le problème Windows n’est pas reproduit à ce stade.

Dans PowerShell :

```powershell
Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/JusteYoann/Pokemon-Yokai-Watch/dev/reconstruction-finalisation/QA_RECETTE_FINALE/BETA_13_OST/diagnostiquer_windows_wsl.sh' -OutFile 'C:\YokaiBeta\diagnostiquer_windows_wsl.sh'
```

Retrouver les dossiers dans Debian, sans en effacer :

```powershell
wsl -d Debian -- bash -lc 'ls -dt /home/yoann/yokai-beta-b13.*'
```

Remplacer `XXXXXXXX` par le suffixe exact de la tentative concernée, puis :

```powershell
wsl -d Debian -- bash /mnt/c/YokaiBeta/diagnostiquer_windows_wsl.sh /home/yoann/yokai-beta-b13.XXXXXXXX
```

Envoyer **`C:\YokaiBeta\diagnostic-b13.json`** dans la conversation. Le diagnostic lit les fichiers existants, ne recompile rien et ne modifie pas la ROM. Il télécharge uniquement du code de diagnostic public et des empreintes de référence. Il n’envoie aucun fichier automatiquement. Le JSON contient des versions et empreintes : sources MP3 sélectionnées indépendamment du nom de l’archive RAR, WAV, DPCM, 651 objets compilés, sections de l’ELF et blocs de ROM. Aucun contenu audio, ROM ni secret n’est inclus. Les numéros de version ne suffisent pas : les sections allouées des objets sont comparées en ignorant les informations de débogage et chemins de compilation.

La correction de la cause exacte nécessite ce rapport ; aucune différence propre au PC Windows ne peut être identifiée à partir du seul préfixe `505eabc4`. Ne pas considérer le fichier divergent comme la bêta B13 vérifiée tant que l’écart n’est pas expliqué.
