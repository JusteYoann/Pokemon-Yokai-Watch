# Pokémon Rouge Feu × Yo-kai Watch — Phase C : Nathaniel/Michael et Arène de Cramois'Île

La phase B (brume maritime temporelle) est **validée visuellement**.

Tu es autorisé à commencer la phase C sur la branche `feature/cramois-ile-passe`.

**INTERDICTION ABSOLUE DE MERGER SUR `master` SANS MON AUTORISATION EXPLICITE.**

## 1. Contexte

Cramois'Île se situe 60 ans dans le passé.

Les deux premières phases sont terminées :

- Phase A : sépia sur toute l'île, les intérieurs et les combats.
- Phase B : brume temporelle lors des traversées maritimes depuis les Routes 20 et 21.

La phase C doit désormais intégrer et finaliser les événements autour de Nathaniel/Michael, du quiz et de l'Arène.

Commence par auditer les scripts, événements, dialogues, cartes et ressources déjà présents dans le dépôt. Préserve tout ce qui fonctionne.

## 2. Nathaniel / Michael

Nathaniel ou Michael, selon la variante prévue dans le scénario, est le grand-père du protagoniste.

Il doit être présent à Cramois'Île, dans cette époque située 60 ans dans le passé.

Consignes :

- Réutiliser les sprites déjà fournis et les ressources du dépôt.
- Respecter sa personnalité et son importance scénaristique.
- Conserver les dialogues et événements déjà validés.
- Vérifier les conditions d'apparition et la cohérence des deux variantes.
- Préserver les événements prévus autour de sa victoire et du Badge Volcan.

Ne pas réécrire le scénario existant sans nécessité.

## 3. Hovernyan — Compagnon permanent

Hovernyan est le compagnon emblématique de Nathaniel/Michael.

Son sprite overworld doit être basé sur le fichier fourni :

`Nintendo Switch - Yo-kai Watch 4++ - Yo-kai (Omamori Tribe) - Hovernyan.png`

Ce fichier contient plusieurs orientations du personnage.

Consignes :

- Adapter fidèlement le sprite au style Pokémon Rouge Feu.
- Préserver les proportions, les couleurs et la cape rouge.
- Hovernyan doit constamment se tenir à côté de Nathaniel/Michael lors de ses apparitions à Cramois'Île.
- S'ils se déplacent pendant une cinématique, Hovernyan doit accompagner son maître.
- Ne pas créer d'animations superflues.
- Ne pas remplacer ou modifier le sprite de combat d'Hovernyan.

### Obtention postgame

Après avoir terminé la Ligue, le joueur pourra affronter Nathaniel/Michael une deuxième fois.

Après sa défaite, celui-ci offrira Hovernyan au protagoniste.

Cette récompense doit :

- Être exclusive au postgame.
- Nécessiter la victoire lors du deuxième affrontement.
- Ne pouvoir être obtenue qu'une seule fois.
- Gérer correctement une équipe complète.
- Être enregistrée durablement dans la sauvegarde.

Ne pas faire disparaître rétroactivement Hovernyan des événements situés 60 ans dans le passé.

Si cet événement dépend de systèmes postgame non encore disponibles, préparer proprement ses conditions sans inventer une nouvelle conclusion scénaristique.

## 4. Quiz de l'Arène

Finaliser le quiz de l'Arène de Cramois'Île en respectant sa structure déjà développée.

- Examiner les questions et mécanismes existants.
- Vérifier les bonnes et mauvaises réponses.
- Vérifier l'ouverture des passages.
- Préserver les combats associés.
- Éviter les blocages de progression.
- Adapter les éléments encore liés à Pokémon lorsque cela est nécessaire pour notre univers Yo-kai Watch.

Ne pas inventer de nouvelles questions définitives sans me les présenter pour validation.

## 5. Préservation des autres systèmes

Cette phase ne doit pas casser :

- La brume temporelle de phase B.
- Le sépia de phase A.
- Les rencontres sauvages et combats.
- Le système de sauvegarde.
- Les événements d'Ariane et Usapion à Carmin-sur-Mer.
- Lavanville et ses effets nocturnes.
- Les événements de la Mafiamille.
- L'enquête de la Pierre Philosovni.
- La finale avec Don Morléone et Don Spiraton.
- Les 151 Yo-kai et leurs données existantes.

Ne touche pas aux musiques, aux autres Champions ou aux systèmes sans rapport avec la phase C.

## 6. Contraintes techniques

La marge EWRAM annoncée à la fin de la phase B est de seulement 776 octets.

Privilégie donc la réutilisation des ressources et évite toute augmentation inutile de mémoire permanente.

L'objectif est de conserver la compatibilité avec les deux versions du projet.

Vérifie notamment :

- Les collisions et les déplacements de Hovernyan.
- Les interactions avec Nathaniel/Michael.
- Les sauvegardes pendant les événements.
- Les différentes conditions de progression.
- La transition entre Arène et événements scénaristiques.
- L'absence de régression des phases A et B.

## 7. Livrables attendus

Je souhaite :

1. Un rapport d'audit des éléments déjà présents.
2. L'intégration des éléments manquants de phase C.
3. Des captures et GIF des cinématiques importantes.
4. Des tests mGBA sur les deux versions.
5. Un rapport sur la mémoire utilisée.
6. La liste exacte des fichiers modifiés.
7. Un bilan des éléments terminés et des éventuelles limites techniques.

Effectue les modifications sur `feature/cramois-ile-passe` ou sur une branche de travail dérivée, sans écraser le travail existant.

**Ne fusionne rien sur `master`.**

Arrête-toi après les tests et les captures pour attendre ma validation visuelle et scénaristique.

L'objectif est d'obtenir une phase C fonctionnelle, fidèle à notre scénario et prête à être examinée avant toute intégration définitive.