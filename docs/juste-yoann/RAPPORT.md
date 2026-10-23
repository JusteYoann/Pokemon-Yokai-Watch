# Juste Yoann — cœur préparé, quête non activée

**État : EN COURS. La quête complète n’est pas livrée ni validée.** Branche dédiée `feature/juste-yoann-charme-chroma`, issue de `67b227302`. Aucun merge sur master.

[Demande intégrale](demande/CAHIER_DES_CHARGES.md) · [Audit](AUDIT.md).

## Développé et vérifié

- Vérification des 151 bits natifs « obtenu », indépendante du compteur du diplôme et des bits « aperçu » ; invitation à usage unique et visibilité avec des drapeaux persistants dédiés.
- Objet important Charme Chroma sur l’emplacement réservé nº52, sans modifier les autres identifiants, la taille des poches ni le format de sauvegarde. Description fournie, icône native Grelot Zen réutilisée ; pas de vente, jet ou consommation via les menus natifs.
- Remise protégée par un drapeau, refus propre si la poche est pleine, puis récupération possible une fois libérée. Sauvegarde Flash et véritable Continuer testés.
- Trois tirages de PID pour les espèces shiny autorisées. Chaque tirage bénéficie du multiplicateur Safari. Arrêt au premier succès, OT conservé, création du Yo-kai une seule fois. Sans charme hors Safari, l’ancien chemin de génération reste identique. Les rencontres statiques, cadeaux et Dresseurs ne sont pas reliés à ce calcul.
- Discours, fondu progressif qui épargne les palettes de texte, écran exact THANK FOR PLAY pendant trois secondes avec courte pause musicale, retour des couleurs, remise du cadeau. Une tâche temporaire et une fenêtre de 2688 octets, sans nouvelle variable EWRAM permanente.
- Textes préparés pour Chen, présentation, discours, refus, cadeau et dialogue ultérieur. Équipe exacte décrite avec les identifiants existants dans `data/yokai/juste_yoann.json` ; elle n’est pas encore un Dresseur actif.

## Tests mGBA ciblés

[Public : cœur](core/public/TEST_MGBA.json) · [Privé : cœur](core/prive/TEST_MGBA.json) · [Public : probabilités](core/public/SHINY_NATIF.json) · [Privé : probabilités](core/prive/SHINY_NATIF.json).

Par version, huit contrôles du cœur passent : sac plein/récupération, 151 aperçus insuffisants, 150 obtenus insuffisants, 151 obtenus et invitation, remise unique, sauvegarde/Continuer, 82 lignes mesurées avec la police native, scène complète et restauration des palettes. Les fonctions sont appelées par des fixtures : aucune apparition du nouveau PNJ ni aucun combat contre lui n’est présenté comme testé.

Pour chaque version, quatre situations × deux graines × deux millions de tirages natifs vérifient les taux théoriques à six écarts-types : `1/8192`, `3/8192`, `1-(1-1/8192)^3`, `1-(1-3/8192)^3`. Ce sont des tests du RNG et du calcul de personnalité, pas des millions de captures naturelles.

[Capture THANK FOR PLAY](core/public/thank-for-play.png) · [GIF de la scène seule, chambre sans le nouveau PNJ](core/public/scene-core-sans-pnj.gif) · [Chambre après restauration](core/public/chambre-apres-scene.png).

## Mémoire et compilation

Les deux versions compilent. [Mesures exactes et SHA256](core/MEMOIRE.json).

| Mesure | Public | Privé |
|---|---:|---:|
| ROM fichier | 16777216 | 31750063 |
| Sections ROM occupées | 9781924 | 29774698 |
| EWRAM utilisée / libre | 261368 / 776 | 261368 / 776 |
| IWRAM utilisée / libre | 29824 / 2944 | 29888 / 2880 |

La RAM statique conserve les valeurs de la livraison précédente. Les buffers temporaires utilisent le tas existant. Les graphismes et palettes shiny, les 151 identifiants, les équipes et scripts de Ligue, Yopple, Cramois et la finale ne sont pas modifiés par ce lot.

## Reste à terminer dès réception du PNG original

Le chemin `C:/Users/estab/Downloads/weqrt19_53_30.png` désigne le PC de l’utilisateur. L’aperçu du chat est visible, mais aucun fichier téléchargeable correspondant n’est accessible dans l’environnement. Il faut le PNG joint comme fichier ou un lien direct pour respecter l’interdiction de redessiner.

1. Extraire les deux sprites sans modification artistique, adapter palette et dimensions GBA, créer leurs tables complètes de portrait et d’objet de face immobile.
2. Ajouter le Dresseur avec ses six Yo-kai exacts, ses attaques natives légales, IA classique et paramètres modérés. Valider l’ordre et les deux Démophage en combat.
3. Raccorder l’invitation à Chen en préservant ses autres événements et faire apparaître Juste Yoann dans la chambre avec une position vérifiée. Ces hooks restent volontairement absents : aucun graphisme de substitution n’est intégré.
4. Tester refus, défaite du joueur, retour et nouvelle tentative, victoire réelle, discours unique, cadeau et dialogue final sans revanche ; vérifier les deux variantes du joueur et la sauvegarde de l’événement.
5. Fournir les captures du PNJ, de son introduction en combat et les GIF définitifs. Les preuves actuelles de scène seule ne les remplacent pas.

La liste des treize tests demandés n’est donc pas intégralement validée. Aucune approbation finale de la quête n’est sollicitée à ce stade.

## Reproduction des contrôles déjà disponibles

```bash
source /workspace/.setup/env.sh
make -j6
make -j6 YOKAI_AUDIO_DIR=/workspace/private-audio/lavanville-integration
python3 tools/yokai/tester_yoann_core_mgba.py
python3 tools/yokai/tester_yoann_shiny_mgba.py
YOKAI_QA_ROM="$PWD/pokefirered_audio.gba" python3 tools/yokai/tester_yoann_core_mgba.py
YOKAI_QA_ROM="$PWD/pokefirered_audio.gba" python3 tools/yokai/tester_yoann_shiny_mgba.py
```
