# Soranaki — histoire, combat final et cas techniques

## Origine — VALIDÉ

**Kuuten**, associé à la reine Oni **Shuka**, est accusé d'un complot contre le père de Shuka et emprisonné ; sa rancœur le transforme en **Soranaki**. Enma l'Ancien finit par le sceller longtemps avant l'époque actuelle. Don Morleone veut le réveiller pour asseoir sa domination sur Kanto. Les règles du scellement et du rituel manquent encore de décisions explicites.

Une **fresque/illustration de prophétie** est disponible : `REFERENCES_VISUELLES/SORANAKI/ref_soranaki_fresque_prophetie.webp`. Sa place exacte (Temple, musée, manuscrit, ruines) est à décider ; ne pas en faire un mécanisme obligatoire avant validation.

## Déclenchement final — VALIDÉ

- Après Agent X, le joueur atteint le sanctuaire.
- Don Morleone a **déjà invoqué** Soranaki.
- Matt arrive, prononce une intervention et **soigne toute l'équipe** du joueur AVANT le combat phase 1.
- Le joueur enchaîne **phase 1**, transition et **phase 2 sans aucune restauration de PV, PP ni statut entre les deux**.
- Après la victoire de la phase 2, Soranaki disparaît de la trame principale ; Morleone et Agent X fuient furieux ; Enma révèle qui il est et ouvre le Panthéon.

## Phase 1 — VALIDÉ en intention, À IMPLÉMENTER

- Apparence de première forme : `SORANAKI/ref_soranaki_premiere_forme.webp`.
- Afficher une **barre de PV exceptionnellement grande** (interface spécifique ou compteur multi-segments) ; éviter les fuites d'entiers, des divisions erronées ou l'écrasement des jauges standard.
- Soranaki peut se transformer temporairement en apparences d'autres Yo-kai, **tout en conservant ses propres couleurs**. La forme doit rester identifiable comme Soranaki. La liste des apparences, le rythme et le comportement exact après transformation sont encore ouverts.
- NE PAS changer globalement les sprites, palettes ou statistiques de ces espèces ; l'effet appartient exclusivement à ce boss.
- Respecter un ordre de gameplay explicite : entrée, combat, victoire phase 1, transition scénarisée. Éviter les captures sauvages, objets de capture ou oublis de flags qui cassent le scénario.

## Phase 2 — VALIDÉ en intention, À IMPLÉMENTER

- Forme humanoïde et plus dangereuse ; `SORANAKI/ref_soranaki_forme_maten.webp` est la **référence artistique**. Le nom « Maten Soranaki » reste **à confirmer comme nom affiché**.
- Monologue de Soranaki avant le deuxième combat : texte d'intention, non définitif.
- **AUCUN SOIN entre les phases.** Conserver tous les états de l'équipe : PV, statut, PP et KO. Ne pas recharger automatiquement un objet, ni recréer une équipe pleine sous prétexte d'un nouveau combat.
- Combat tactiquement plus dur que la première phase, sans abus d'injustices irréversibles. Les attaques, valeurs et niveau du boss doivent découler de tests.

## Postgame — VALIDÉ sur le principe

Un **nouveau combat facultatif contre Soranaki** existe au fond des Limbes Éternelles. Puisque Soranaki disparaît après la fin, **l'explication** de ce rematch (écho du pouvoir, souvenir scellé, autre épreuve) est À DÉCIDER ; ne pas dire qu'il « est ressuscité » sans consentement.

## Recommandations techniques et critères d'acceptation

1. **Prototype autonome d'abord** : tester l'énorme jauge, les transformations et la transmission d'état entre les deux phases dans un environnement isolé.
2. **Ne pas renuméroter le Pokédex des 151** pour intégrer les formes temporaires de Soranaki. Si la mécanique nécessite des identifiants internes réservés au boss, documenter leur rôle non capturable.
3. **Tests de plusieurs états** : joueur full HP, un Yo-kai KO, PP épuisés, statuts, sacs pleins, abandon/défaite, interruption de la transition, sauvegarde avant boss.
4. **Sans automatisme de soin au changement de phase**. La guérison de Matt ne se déclenche qu'avant la phase 1.
5. **Validation d'affichage** : aucune corruption de VRAM, palette, sprite de l'adversaire ou écran de fin ; jauge entière cohérente.
6. **Fuite Morleone/Agent X** : ne jamais rejouer leur arrivée en boucle après victoire ; flags persistants.
7. **Victoire** : ouvre Panthéon, puis crédits et postgame sans provoquer de capture ou de retour intempestif à l'écran titre.

## Ce qui n'est PAS décidé

- Comment Don Morleone brise le sceau d'Enma l'Ancien.
- Combien de transformations temporaires apparaissent en phase 1, et vers quelles espèces.
- Les capacités, niveaux, types, résistances et PV exacts des deux formes.
- La nature juridique/magique de la résurgence des Limbes.
- Les textes définitifs du monologue de la phase 2.

Les propositions de mécaniques avancées ne sont **pas** déjà présentes dans la ROM par simple existence d'un sprite de référence.
