# Reprise — mission finale v1, jalon fonctionnel sauvegardé

Branche `dev/reconstruction-finalisation`. Dernier code/données du jeu : **f029b5236e34f9571f48fb928020f5adcff5debc**. Les commits suivants sont outils/preuves/rapports. Master reste **037335f4c725d7c9aecdac87066f2002b4bd7e14**. La consigne courante est `RECUPERATION_PROJET/sources_validees/MISSION_FINALE_V1.md`, qui remplace les anciennes priorités20musiques/quêtes. **Aucune nouvelle quête pour la v1.0.**

## Travail terminé — ne pas refaire

-151Yo-kai/données, personnages Nathan/Katie, Matt obligatoire, équipes, sept groupes caméos, MultiExp et67exclusions shiny conservés.
- Treize OST de la sélection15 actives et testées ; deux encore natives de repli, pas d’enregistrement manquant. Profil actif `data/yokai/audio_loops.json`, catalogue26slots historiques dont15sélectionnés. Rangs et destinations dans `QA_RECETTE_FINALE/INTEGRATION_MUSIQUES/ETAT_15_OST_V1.csv`. Mount Wildwood/Harrisville/MiniBoss retirés par demande utilisateur ; retours natifs. Aucun20ancien à restaurer automatiquement.
- SanFantastico, Uptown, MysticGrove, HoppersGorge et TakeCare ajoutés, Ghoulfather personnel ajouté. Intro/loop source mesurées ; DPCM13379Hz. Cinq raccords audio réels par piste ; sons/cris/fanfares/reprises testés. La conclusion prend place après Matt, Panthéon/crédits/Continuer testés avec équipe forte et arrivée directe (pas une partie intégrale).
- Nouveaux overworlds32×32 : MisterreRoutes12/16, OctorgoneCentrale, MademoaiselleÎlesÉcume. Quatre captures réelles testées. KyubiMontBraise et EnmaCaverne distinct du Seigneur conservés. Léo/Jibanyan :9images, dialogues français, téléporteur/restitution native testés pour les deux sexes.
-1850chaînes de vocabulaire harmonisées ; menus/aide/sauvegarde et34messages combat français. Médallium50px : menu8tuiles ; affichage et six tris/comptes151même après déblocage national. Deux en-têtes générés avaient des changements locaux : correction pérenne dans items.json et display_name régional/gabarit, noms techniques inchangés. Clone propre désormais strictement identique.
- Animations354 :1448cas mGBA,2côtés et contextes normal/shiny,8capacités à deux tours aussi au second stade. Les2attentes initiales Tunnel étaient un défaut de fixture (sélecteur recréant le rebond), corrigé sans toucher le jeu ; second passage complet terminé. Palette/tuiles stables sauf Morphing/Clonage attendus.46cas SFXchargés sous DPCM sans perte de voix. Pas de validation visuelle exhaustive.

## ROM et reproduction

ROM privée de développement, **pas v1.0 finale** : `/workspace/private-builds/pokemon-yokai-watch-dev-13ost/pokemon-yokai-watch-dev-13ost.gba` ;24400776octets (23,27Mio), SHA256`36bbf1f1c759f0e355be122caf68d7d110f86c83c1862bda1e85c72ea37abfc5`. Publique native16Mio paddés SHA256`7f4248b27ec01f4d32acdcacc11c3b1bb5f03ef434431bea099ba85d1496b4ac`.

Les deux reconstruits depuis GitHub sont identiques octet par octet (`/workspace/repro-v1-finale`, outils `/workspace/repro-tools`). Sources musicales régénérées depuis les archives privées, pas copie des objets/ROM. Même machine cloud, pas nouvelleVM. Détails : `QA_RECETTE_FINALE/VERSION_1_DEVELOPPEMENT/README.md`, `REPRODUCTIBILITE.json`, `VERDICT.json`.

Sources privées15 : `/workspace/private-audio/v1-full-sources/` ; profil13 : `/workspace/private-audio/v1-integration/` ; démos audio réelles dans `previews/`. Profil indépendant `/workspace/private-audio/repro-v1-integration/`. Aucun MP3/WAV/DPCM/ROM à publier. Le build public n’en dépend pas ; instructions locales d’audio privé documentées, FFmpeg/version WAV épinglés.

## Prochain travail obligatoire

1. Terminer les boucles fiables d’**Enma Track**, slot5, et **Final Battle – Are You Ready?**, slot25. LesMP3/WAV sont présents. Hooks Enma dialogue et MattChampion préparés, natifs de repli. Ne pas activer une boucle arbitraire ou substituer Sangokushi. Méthodes exécutées conservées dans `tools/yokai/analyses_boucles/v1/` ; positions validées seules dans JSON. Ne pas reprendre les20anciens choix.
2. Direction artistique des84shiny et prise en charge complète des dessins alternatifs. Robonyan28 noir/or avec cornes possède déjà son front/back/source sous `graphics/yokai_shiny_artwork/019/`, **inactif** : ne pas le présenter intégré. Préserver137normaux protégés et aucun statut shiny pour67exclus. Vérifier combats, capture, résumé, PC et transformations après le futur rendu alternatif.
3. Français intégral et correspondances contextuelles encore incomplètes ;1850substitutions de vocabulaire ne constituent pas une traduction de toute l’histoire/descriptions. Garder Kanto, villes et identifiants. Respecter données et équipes validées.
4. Équilibrage léger/EXP : résultat réel de parcours60–70 non validé. Véritable traversée début→Ligue→postgame et collection151non réalisées. Ne pas appeler les warps/équipes fortes une partie complète. La recette native disponible ne lève pas ces réserves.

Quêtes10/scientifique/Coach/RedSupplémentaire/JusteYoann/cinématique nouvelle sont reportées, ne plus les compter comme nécessaires pour ce jalon. Conserver les événements historiques et la géographie : KyubiMontBraise, MademoaiselleÎlesÉcume. **Verdict global : NON PRÊT pour v1.0 finale.** Continuer les corrections à partir de cette base, sans recommencer les développements ou les campagnes qui passent et ne sont pas affectés par de nouveaux changements.
