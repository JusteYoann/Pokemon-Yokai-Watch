# Audit de phase C

Base visuellement validée : `a8c97b3ca`, branche `feature/cramois-ile-passe`. Aucun merge sur master.

L'Arène conserve le plan, les six portes, leurs drapeaux persistants et leurs Dresseurs de Rouge Feu. Les scripts de bonnes réponses ouvrent les portes ; les mauvaises réponses lancent les combats puis ouvrent les portes après victoire. Le combat direct utilise déjà les mêmes routines. Les questions encore présentes sont celles de Pokémon, avec réponses OUI/NON/NON/NON/OUI/NON. Le cahier des charges initial fixe déjà les six questions Yo-kai et NON/OUI/OUI/OUI/OUI/OUI : aucune nouvelle question à faire approuver.

Le Champion reste l'objet natif Blaine, résolu dynamiquement vers Nathaniel (garçon) ou Michael (fille), y compris après sauvegarde. Portraits et équipe de six sont déjà intégrés. Les dialogues d'introduction, défaite, Badge Volcan, CT38 et après combat existent et doivent être conservés. La rencontre humoristique et la réplique du moi du futur manquent. Aucune année canonique n'a été trouvée : ne pas employer l'année du PC ; proposer un échange relatif à soixante ans en attendant une date du créateur.

Une apparition secondaire à Parmanie possède déjà ses propres combats, flags et récompense Pierre Plante. Elle est indépendante : conserver ses scripts, équipes et drapeaux. Ne pas réutiliser ses drapeaux pour le don d'Hovernyan. Le drapeau de Ligue native `FLAG_SYS_GAME_CLEAR` existe : le nouveau second combat peut en dépendre, après la victoire d'Arène. Réutiliser l'équipe du Champion plutôt qu'inventer une équipe postgame non validée.

Don : commande native `givemon`, qui sait envoyer au PC lorsque l'équipe est pleine et signale `MON_CANT_GIVE` si tout est plein. Un drapeau de victoire postgame séparé de celui du don permet de réclamer la récompense plus tard sans refaire le combat. Drapeaux persistants libres 0x32C–0x32E ; aucun élargissement de sauvegarde ni EWRAM statique nécessaire.

Hovernyan overworld absent du dépôt. La planche Switch nommée n'a pas été retrouvée dans les fichiers et archives accessibles ; le créateur fournit ensuite une référence face/dos dans le chat. Intégrer une adaptation de cette référence dans de nouveaux fichiers, sans toucher aux 5821 graphismes validés ni à son sprite de combat. Le Champion ne se déplace pas dans les scènes existantes : placer un compagnon statique adjacent, sans système de suivi permanent supplémentaire. Contrôler les cases et palettes en mGBA. Les scènes ajoutées restent stationnaires et gardent les deux personnages côte à côte.

Mémoire de référence : EWRAM 261368 octets (776 libres), IWRAM publique 29824 et privée 29888. Réutiliser les objets et commandes natives, les palettes de PNJ et les flags existants ; aucun nouveau gestionnaire par image.
