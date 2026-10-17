# État de reprise actuel — priorité musique

Branche : **dev/reconstruction-finalisation**. Master préservée. Dernier changement du jeu testé : **8ff0c49f6** ; les publications suivantes complètent uniquement les rapports et instructions.

## Présent et testé

Les151Yo-kai, leurs données/attaques/évolutions, équipes validées, rencontres, Multi Exp., Matt obligatoire, séries Nathan/Katie et sept groupes caméos sont conservés. Chen/Watch passive/Médallium, distinction Seigneur Enma et créature Enma, sprite félin de la Caverne Azurée conservés. Kyubi reste au Mont Braise, Mademoaiselle aux Îles Écume. Les67espèces exclues gardent le verrou de statut shiny.

**10OST réellement intégrées dans le build privé** : vélo1 ; Domniscian2 ; Tour4 ; combat Seigneur Enma6 ; Sylphe occupée11 ; Bois Baies14 ; Conseil4 15 ; Île2 16 ; Repaire Rocket17 ; employés/Mafiamille20. Les huit combats/rematches du Conseil4 sont routés, Matt et les champions d’arène conservent leurs thèmes natifs.51routes contrôlées nativement. Le script Giovanni2 reçoit uniquement la transition vers la Sylphe libérée : vrai déclencheur de coordonnées, combat et retour musical testés, sans réinitialisation manuelle depuis le test.

Pipeline DPCM mono13379Hz actif, sources privées générées puis liées normalement par make. La perte de voix après fanfare est reproduite et corrigée avec restitution de position. Arrêt/reprise, fondus, sons/cris et Flash testés.64octets d’IWRAM supplémentaires uniquement dans le build privé ; EWRAM inchangée.

## Rapports de référence

**QA_RECETTE_FINALE/INTEGRATION_MUSIQUES/README.md** et ETAT_20_OST.csv donnent les20choix, leurs coûts et leur état réel. TEST_MGBA.json et TEST_MGBA_CLONE_GITHUB.json : dix déclencheurs en ROM, cinquante raccords audio propres. Le Bois Baies ajoute un cycle pour le raccord superposé à un cri natif, sans couper les bruitages. TEST_INTERRUPTIONS_MGBA.json, TEST_LIBERATION_SYLPHE_MGBA.json, ROUTAGE_COMBATS_MGBA.json et REPRODUCTIBILITE.json complètent les preuves. Les fixtures (warps, flags, équipe forte) ne constituent pas une partie complète ni un test d’équilibrage.

ROM privée : **21 667 712octets,20,66Mio** sous32Mio. ROM publique :16Mio paddés, thèmes de repli, aucune source externe requise. Les deux versions sont identiques octet pour octet à leur reconstruction GitHub avec outils indépendants et DPCM régénérés, sans copie d’objets/ROM locaux. Même machine cloud, pas une seconde VM. Empreintes exactes dans REPRODUCTIBILITE.json. Aucun enregistrement protégé ni ROM publié.

Les quinze sections optimisées et cinq sources encore entières totalisent14 024 099octets de samples, contre23 248 952avant. Aucun morceau retiré. La projection20est favorable mais ne constitue pas20intégrations.

## Prochain point de reprise

**Ne pas refaire le pipeline ou les dix intégrations validées sans nouveau changement.** Terminer les boucles des pistes3(The Ghoulfather),5(Enma Track),7(Nates House),8(Katies House),12(Blossom Heights), en conservant leurs introductions. Les fichiers sont présents : ne pas demander de nouvelles archives en les supposant manquants. Le thème personnel de Don Morleone reste réservé ; aucune substitution Sangokushi.

Les pistes9/10attendent les événements Coach,18/19le scientifique. Ne pas créer de nouveaux personnages/quêtes seulement pour augmenter le compteur musical durant une session consacrée à la musique. Enma Villa13reste optionnel tant qu’une scène cohérente ne le justifie pas. The Very Curious Yo-kai Watch reste supplémentaire, non intégré et n’a remplacé aucun des20choix.

Les activations sont dans data/yokai/audio_loops.json. Le build privé vérifie les empreintes WAV et génère sa table optionnelle ; instructions complètes dans le README musical. L’ancien journal est conservé dans HISTORIQUE_REPRISE_AVANT_INTEGRATION_MUSICALE.md et dans Git.

## Ressources privées et reproduction

- Archives : /workspace/private-audio/recovery/ ;80MP3 extraits : /workspace/private-audio/extracted/manifest-private.json.
- WAV/source et coûts complets : /workspace/private-audio/dpcm-full-sources/.
- Profil final : /workspace/private-audio/integration-v2/ ; démos mGBA8s et raccords dans previews/.
- Reconstruction indépendante : /workspace/private-audio/repro-integration-v2/ ; checkout /workspace/repro-musique-integration.

Ne jamais publier MP3, WAV, DPCM protégés ou ROM. Ils sont régénérables depuis les sources privées épinglées ; sans elles le build public est musicalement différent. Tous les outils/configurations/sources nécessaires au build public et à la génération privée sont sauvegardés sur GitHub.

## Réserves globales

Restent notamment : dessins shiny finaux84 (Robonyan28 à cornes sauvegardé mais inactif), overworld Misterre/Mademoaiselle/Octorgone, Léo/français intégral, cinématique, équilibrage et traversée principale/postgame. Les dix quêtes sont facultatives et de dernière priorité. Pas d’écoute perceptive humaine ni de profilage console physique. **Jeu global : NON PRÊT ; musique :10/20, recette ciblée réussie.** Aucun merge vers master ne résulte de ces tests.
