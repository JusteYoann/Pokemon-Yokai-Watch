# Audit et choix techniques

Base : feature/champions-yokai-watch, e1dcd9132aa8666fb1798c90a731859f1632313e. Branche dédiée : feature/pierre-philosovni-carmin. Aucun merge master.

Toutes les branches distantes ont été actualisées et les événements Argenta, Carmin, Océane, Route25, Champions et Lavanville examinés. Les branches historiques ne sont pas fusionnées : elles redistribuent les rôles des Champions différemment de la version validée.

Le moteur offre le double local et le multi en liaison. Le contrôleur LinkPartner ne prend aucune décision hors liaison ; il n'est pas un partenaire IA. Le chapitre utilise donc le double local et ajoute un contrôleur de décisions pour le seul emplacement allié. Usapion occupe un septième emplacement RAM temporaire, hors des six membres du joueur. PARTY_SIZE et les structures sauvegardées restent à six. Les menus et récompenses d'expérience restent réservés à l'équipe du joueur. Un drapeau de combat dédié isole cette adaptation. Les deux sbires ont chacun un seul Yo-kai, sans réserve ; leur paire utilise un enregistrement Dresseur dédié. Les six membres du joueur restent disponibles.

Ressources existantes : Ariane, Usapion, Mafiamille, portraits, tilesets General/VermilionCity et Building/SilphCo. Aucun PNG ni palette validé modifié. Ariane et Usapion n'ont que des poses statiques validées : la mise en scène utilise des étapes de rendez-vous et des transitions de carte, sans inventer de frames de marche. Ariane n'a pas de portrait de dos validé ; l'introduction conserve le dos du joueur et nomme explicitement Ariane lors de l'envoi d'Usapion.

L'entrepôt est une nouvelle petite carte, ajoutée en fin du groupe intérieur de Carmin pour préserver les identifiants existants. La quête est indépendante des badges et de l'Océane. Le soin du capitaine et le départ du navire deviennent indépendants de FLAG_GOT_HM01 ; le capitaine ne donne plus la CS. Les anciennes sauvegardes ayant déjà Coupe peuvent faire l'enquête sans recevoir de doublon.

États persistants : 0 invitation, 1 enquête/reprise après défaite, 2 victoire/récompense en attente, 3 conclusion. Le combat n'avance l'état qu'en cas de victoire. Le don de CS est validé après ajout effectif ; un sac plein permet de reparler à Ariane. La défaite rend la main dans l'entrepôt après soin de l'équipe, sans flag de victoire.

Aucun développement de l'intrigue hors Argenta/Carmin. Aucun objet Pierre obtenu ni représenté. Aucun changement du combat final.

Le port original comportait une clôture bloquant l'accès terrestre au quai oriental. Trois tuiles de passage sont ouvertes ; une cabane de seize tuiles, copiées du bâtiment natif de Carmin, accueille l'entrée. Les dix warps historiques restent à leur index ; le nouveau est ajouté à l'index10, et son unique destination intérieure est l'index0 (numérotation native à partir de zéro).

Un rafraîchissement ON_LOAD réapplique seulement ces19 tuiles après restauration du map-view sauvegardé : les anciennes sauvegardes de Carmin ne peuvent masquer le nouvel accès. Les acteurs sérialisés de Carmin, son Arène et le nouvel entrepôt sont reconstruits depuis les templates courants sur Continue. Les autres cartes conservent leurs règles antérieures.

La règle Make de maps.o ne suivait pas les fichiers map.bin/border.bin ; ses dépendances sont ajoutées pour que les changements de collisions soient pris en compte aussi en compilation incrémentale.
