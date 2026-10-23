# Audit préalable — Cramois'Île, phase A

Base validée : `2e81a799f2cfcb328cdf4f92b17b9131db6e0f1d`, tête distante vérifiée de `feature/pierre-philosovni-carmin`. Elle contient le suivi d'Ariane, le duo et Coupe, au-dessus des Champions (`e1dcd9132`), de Lavanville et de la finale. Nouvelle branche : `feature/cramois-ile-passe`. Aucune fusion sur master.

Mesures relues dans les deux fichiers de liaison avant modification : EWRAM `0x3fce4` = 261348 octets, 796 libres ; IWRAM publique `0x7480` = 29824 octets, privée 29888 octets. Les ROM et ELF de référence sont archivés localement pour les captures avant/après. La marge antérieure est donc confirmée, et non supposée.

Les treize cartes concernées sont l'extérieur, les quatre étages du Manoir et les huit cartes du groupe intérieur de Cramois : Arène, quatre salles du laboratoire, deux étages du Centre et Boutique. Aucun plan, objet, script, rencontre, puzzle, équipe ni palette source validée ne doit être modifié dans la phase A.

Le moteur possède déjà un sépia, mais cette routine modifie la palette fournie et n'isole pas les interfaces. La piste retenue est une conversion RGB555 lors du transfert vers la palette matérielle, uniquement pour les banques du décor et des acteurs. Les deux buffers originaux sont conservés : le sépia ne se cumule pas, suit les fondus et animations, et disparaît automatiquement hors des contextes autorisés.

Audit des banques : décor de combat BG 2, 3, 4 ; interface de combat BG 0, 1, 5 et 7 ; combattants et portraits OBJ 0 à 3 ; barres de PV et statuts dans des banques OBJ distinctes. Sur la carte, les tuiles du décor utilisent BG 0 à 12 ; les fenêtres standard/dialogues utilisent leurs banques réservées. Ces limites doivent être vérifiées dans mGBA, avec menus et jauges.

Une table de conversion RGB555 de 64 Kio en ROM évitera une allocation permanente et les calculs par couleur pendant VBlank. La version privée dispose encore de plus de 1 Mio ROM libre. Aucun dessin ni PNG/palette approuvé n'est remplacé.

La phase A est un prototype : la palette proposée doit être validée visuellement avant sa fixation. La brume maritime (phase B), les dialogues et quiz (phase C), et la validation exhaustive de progression (phase D) restent des étapes séparées. Le fonctionnement préservé du Manoir et du laboratoire sera distingué de ce qui aura effectivement été testé.
