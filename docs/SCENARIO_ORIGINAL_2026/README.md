# Pokémon Rouge Feu × Yo-kai Watch — Bible narrative et plan d'intégration

**Version documentaire : 20 octobre 2026**  
**Périmètre : NOUVELLE histoire originale, personnages, arènes, Temple Céleste et postgame.**  
**Dépôt cible :** https://github.com/JusteYoann/Pokemon-Yokai-Watch  
**Branche examinée :** `dev/reconstruction-finalisation`  
**Ne pas fusionner automatiquement cette documentation au code.**

## À lire d'abord

Ce dossier est un **supplément de conception** au dépôt existant, PAS un nouveau projet Pokémon et PAS un remplacement de ses fichiers techniques. Les 151 Yo-kai, leurs sprites de combat, palettes, icônes, graphismes des protagonistes, une grande partie des données et les outils de build existent **déjà** dans le dépôt. Ce pack n'en contient **aucune copie**.

Les documents décrivent la **nouvelle campagne proposée** dans la conversation récente ; la version actuellement codée repose encore largement sur une ancienne campagne. Une information narrativement validée n'est donc pas automatiquement intégrée. Les documents anciens de `RECUPERATION_PROJET/sources_validees/` constituent des sources historiques, mais **leurs attributions de Champions et de Ligue peuvent être dépassées** par la nouvelle direction.

### Statuts obligatoires

- **VALIDÉ** : décision explicitement prise par le créateur dans la conversation ; à respecter.
- **DIRECTION DE CONCEPTION** : choix de design confié à l'assistant ou direction générale approuvée ; valeurs précises encore à revoir dans un jalon de validation.
- **PROPOSÉ** : hypothèse, dialogue exemple, carte ou équipe suggérée, non figée.
- **À DÉCIDER** : question sans réponse ; ne pas compléter au hasard.
- **EXISTANT GITHUB** : fichier repéré dans le dépôt à la date de l'audit ; ne signifie pas que le nouveau scénario y est intégré.
- **À IMPLÉMENTER** / **À TESTER** : nécessité technique, à confirmer par les builds et tests.

**Règle de priorité en cas de conflit :** une décision utilisateur explicite récente prime sur une suggestion de l'assistant et sur une décision ancienne, MAIS si le dernier échange n'indique pas clairement qu'une décision a été remplacée, documenter le conflit et demander confirmation avant modification destructive. Les équipes détaillées de ce pack ne sont pas des données de combat finales.

## Index des documents

| Fichier | Utilité |
|---|---|
| `00_DECISIONS_VALIDEES.md` | Source centrale des contraintes, statuts et oppositions ancien/nouveau |
| `01_UNIVERS_ET_CHRONOLOGIE.md` | Monde, dirigeants, origine de Soranaki, chronologie |
| `02_SCENARIO_COMPLET.md` | Déroulement narratif, chapitres, transitions, conclusion |
| `03_PERSONNAGES_ET_BIOGRAPHIES.md` | Caractères, liens, versions conditionnelles, références visuelles |
| `04_CHAMPIONS_ET_EQUIPES.csv` | Huit Champions, types dominants, équipes provisoires et lieux |
| `04_CHAMPIONS_ET_ARENES.md` | Huit arènes, contraintes, défis, liberté de Codex |
| `05_TEMPLE_CELESTE.md` | Quatre adversaires, progression, équipes thématiques, rôle de Zazel |
| `06_SORANAKI_FINAL.md` | Combat final et mécanique de deux phases, priorité technique |
| `07_POSTGAME.md` | Limbes, Paradis Divin, Enma, rencontres, rematches |
| `08_CARTES_A_MODIFIER.md` | Maps GBA, variantes Zombie Night et Cramois'Île, contraintes de déplacements |
| `09_DIALOGUES.md` | Intentions et exemples de textes, **non validés mot à mot** |
| `10_ASSETS_A_CREER.csv` | Inventaire des nouveaux graphismes/sons et des réutilisations possibles |
| `10_REFERENCES_VISUELLES.md` | Où retrouver chacune des références artistiques déjà reçues |
| `11_PLAN_INTEGRATION_CODEX.md` | Ordre de réalisation, sécurité, tests, critères d'acceptation |
| `12_CONFLITS_ET_QUESTIONS.md` | Points de continuité et contradictions à arbitrer avant codage |
| `13_ETAT_GITHUB_2026-10-20.md` | Audit de lecture, dossiers réellement présents et différences |
| `14_REPARTITION_YOKAI_THEMATIQUES.md` / `14_GROUPES_YOKAI.csv` | Groupes lore fournis par le créateur : passé, USA, trésor, boss |

### Où mettre ces fichiers ?

Dans le dépôt, viser `docs/SCENARIO_ORIGINAL_2026/` pour **ces textes**. Les références visuelles renommées sont fournies dans un autre ZIP sous `REFERENCES_VISUELLES/` ; on peut les garder dans le dossier de référence utilisateur, localement, et ne recopier dans GitHub que les sources autorisées et vraiment nécessaires au build. Le pack complet proposé regroupe les deux sous-arbres sans modifier GitHub.

### Priorité artistique actuelle

**Carte blanche à Codex pour l'architecture et le level design** des huit arènes, du Temple, des Limbes et du Paradis Divin. Les références sont **inspirantes**, non des plans obligatoires. À Lavanville et à Cramois'Île, **ne pas transformer la géographie de base** : variantes de présentation et d'événements uniquement, avec bâtiments/décors historiques possibles pour le passé. Les propositions de puzzles du présent dossier ne doivent pas être interprétées comme contraintes fixes.

### Avertissements techniques

- Référence moteur : décompilation Pokémon FireRed/LeafGreen, ROM GBA, limites de graphismes/palettes/mémoire.
- Ne pas remapper globalement les constantes `SPECIES_*` pour corriger les compositions de dresseurs ; utiliser les identifiants d'espèces actuels.
- Aucun ajout automatique d'une 152e espèce capturable. Soranaki doit faire l'objet d'une architecture de boss distincte si nécessaire.
- Audio privé et ROM ne vont pas dans le dépôt public.
- Toute nouvelle scène doit être testée en conditions de sauvegarde/reprise, et non seulement par appel de fonction isolé.
