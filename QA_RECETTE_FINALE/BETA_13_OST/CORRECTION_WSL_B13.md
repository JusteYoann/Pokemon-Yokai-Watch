# B13 : écart Windows identifié et correction sans recompilation

## Cause démontrée

Le rapport du PC Windows donne `505eabc4470f967aa2d6c6441f923dfa0ea530a16008de8b41a1bcfda1287b79`, pour 24 400 776 octets. Le commit est bien `ff1cb36b2ecbe7b8ce167e375a6bff378df31347`, avec des sources suivies intactes. Les sources MP3 sélectionnées, WAV, DPCM, en-têtes générés et les sections des **651 objets du jeu** sont identiques à la référence. Seule `lib_text` diffère.

La cause est l’ordre des **247 membres de `libc.a`**. Le Makefile amont d’agbcc construit sa liste par `find` sans tri. L’ordre du parcours dépend du système de fichiers ; il modifie l’ordre des membres de l’archive, puis l’ordre des passerelles d’appels ARM/Thumb générées par GNU ld. Sur cette ROM, cela modifie **25 octets**, entre les offsets `0x1deed0` et `0x1ebecd`, sans changer sa taille. Il ne s’agit pas de 25 erreurs de gameplay.

Preuve locale : reconstruire seulement les bibliothèques dans un nouveau répertoire, avec le même compilateur et les mêmes outils, puis relier les **objets existants**, reproduit exactement le SHA complet du PC Windows. Tous les membres de bibliothèque ont le même contenu dans leurs sections allouées ; `libgcc.a` a le même ordre, `libc.a` un ordre différent. Remettre uniquement l’ordre B13 dans `libc.a` et refaire l’édition de liens produit exactement :

```text
36bbf1f1c759f0e355be122caf68d7d110f86c83c1862bda1e85c72ea37abfc5
```

Les versions Python diffèrent entre PC et cloud, mais elles ne sont pas responsables de cet écart : tous les intermédiaires musicaux et objets correspondants sont identiques. Les versions FFmpeg, GCC et binutils indiquées sont conformes. Les SHA différents des exécutables hôtes agbcc ne suffisent pas à diagnostiquer une différence de code cible ; la permutation de l’archive reproduit à elle seule la différence observée.

## Réparer votre compilation conservée

**Ne pas relancer l’ancien compilateur complet. Ne pas effacer le dossier de diagnostic.** Dans PowerShell :

```powershell
Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/JusteYoann/Pokemon-Yokai-Watch/dev/reconstruction-finalisation/QA_RECETTE_FINALE/BETA_13_OST/reparer_windows_wsl.sh' -OutFile 'C:\YokaiBeta\reparer_windows_wsl.sh'
wsl -d Debian -- bash /mnt/c/YokaiBeta/reparer_windows_wsl.sh
```

Le script trouve automatiquement le dossier si une seule compilation B13 connue existe sous votre compte Linux. En cas de plusieurs candidats, il affiche leurs chemins et s’arrête sans deviner. Indiquer alors explicitement le bon dossier :

```powershell
wsl -d Debian -- bash /mnt/c/YokaiBeta/reparer_windows_wsl.sh /home/yoann/yokai-beta-b13.XXXXXXXX
```

Remplacer `XXXXXXXX` par le suffixe existant. Aucun `sudo`, aucune réinstallation, aucun téléchargement de musique, aucune recompilation du jeu.

Le correctif :

1. Télécharge uniquement les outils publics et leurs empreintes de référence.
2. Exige le commit attendu, une ROM d’entrée B13 connue et des sources suivies intactes.
3. Compare les sources audio, les fichiers générés et les 651 objets à la référence.
4. Vérifie les sections allouées des 277 membres de `libgcc.a` et `libc.a`. Toute différence de code arrête la réparation.
5. Réordonne les membres de l’archive concernée selon le verrou B13, **en conservant intégralement les octets de chaque membre** et une sauvegarde de l’archive précédente.
6. Exécute seulement GNU ld, gbafix et objcopy avec les objets existants et les options de liaison d’origine. Aucun appel à make, GCC, agbcc ou FFmpeg.
7. Exige la taille et le SHA-256 B13 exacts avant export. Vérifie aussi que la ROM et tous les objets d’origine sont restés inchangés.

Le fichier divergent d’origine reste dans le dossier de compilation. Les résultats de l’édition de liens et le rapport sont conservés dans un sous-dossier `b13-repair-*`. Un éventuel fichier différent déjà présent dans le dossier de sortie n’est jamais écrasé.

## Ouvrir la ROM obtenue

```text
C:\YokaiBeta\pokemon-yokai-BETA-B13-20261018.gba
```

Un manifeste `.manifest.json` voisin atteste l’empreinte vérifiée et les 13 OST. Contrôle facultatif supplémentaire dans PowerShell :

```powershell
Get-FileHash C:\YokaiBeta\pokemon-yokai-BETA-B13-20261018.gba -Algorithm SHA256
```

Ouvrir ce `.gba` dans mGBA Windows, via **File → Load ROM**. Utiliser une nouvelle partie de bêta ; conserver les sauvegardes existantes à part. Les [réserves B13](README.md#réserves-connues) restent applicables : cette opération ne finalise pas les shiny, les textes, les deux dernières OST ni la recette complète. Aucune nouvelle fonctionnalité n’est ajoutée.

## Prévention pour les prochaines reconstructions

`BIBLIOTHEQUES_B13_LOCK.json` conserve l’ordre de référence et les empreintes des sections allouées de chaque membre. `normaliser_bibliotheques_b13.py` vérifie le code et canonise l’ordre en préservant les membres. L’installateur Debian appelle désormais cette normalisation avant installation des bibliothèques. Le compilateur Windows fait de même pour les bibliothèques mises en cache et installées, y compris avec le checkout B13 ancien.

L’empreinte de ROM attendue et les contrôles WAV/DPCM restent inchangés. Aucun code de bibliothèque, ROM ou audio protégé n’est publié : le verrou ne contient que des noms et empreintes. Les tests ont été effectués sous Linux sur la divergence **exactement reproduite**, pas dans un Windows WSL distant. La réparation sur le PC doit encore être exécutée ; son propre contrôle SHA empêche l’export d’une ROM différente.
