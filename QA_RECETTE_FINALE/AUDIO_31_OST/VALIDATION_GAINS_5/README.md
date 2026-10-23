# Validation expérimentale des cinq gains privés

Branche `audio/integration-31-ost`. Référence avant correction :
`221adb3ddfe8b8e162aa4e1105de9662921b6e8c`. Aucune fusion.

Les cinq corrections approuvées sont appliquées sous `YOKAI_PRIVATE_AUDIO`.
Les valeurs publiques d'origine sont conservées. Aucun fichier musical, point
de boucle, bruitage, cri, affectation ou élément de gameplay n'a été modifié.
Enma Track reste volontairement en lecture unique, sans fondu ni redémarrage.

## Mesures avant/après dans le mélangeur réel mGBA

Mesures EBU R128 sur la sortie stéréo native mGBA/libretro à 65 536 Hz,
introduction + un cycle entier, ou morceau entier pour Enma, avec marge de
30 images. Filtre de mesure 20 Hz pour rejeter la composante continue ; aucun
traitement ajouté au jeu. Les fenêtres et le protocole sont identiques à ceux
du [bilan précédent](../CLOTURE_31_OST/VOLUMES_31_MGBA.json).
Les mesures de niveau isolent la musique, sans effet simultané ; les tests de
régression distincts incluent les appels natifs aux bruitages et cris.

| OST | Correction Q8 effective, dB | LUFS avant → après | Pic vrai dBFS avant → après | LRA LU avant → après | Échantillons écrêtés après |
|---|---:|---:|---:|---:|---:|
| Enma Track | +14.797 | -43.8 → **-28.8** | -29.2 → **-13.7** | 6.3 → 10.1 | 0 |
| Katies House | +9.700 | -38.7 → **-28.7** | -25.3 → **-15.4** | 6.5 → 7.2 | 0 |
| Enma Villa | +9.298 | -38.3 → **-28.9** | -25.2 → **-15.6** | 4.7 → 5.0 | 0 |
| Mount Wildwood in the Past | +9.514 | -38.5 → **-28.8** | -24.8 → **-14.7** | 2.8 → 2.9 | 0 |
| Final Battle – Are You Ready? | +12.788 | -41.8 → **-28.7** | -28.3 → **-14.9** | 5.6 → 6.5 | 0 |

Les valeurs entières Q8 approuvées sont 77→423, 109→333, 108→315,
101→302 et 64→279. Leur arrondi représente au maximum environ 0,02 dB
par rapport aux corrections demandées. Aucun plafonnement de sécurité ni
normalisation supplémentaire n'a été nécessaire. Le gain acoustique mesuré
n'est pas exactement le rapport Q8 : le moteur quantifie les volumes et le
signal PCM ; le seuil de sélection EBU R128 peut aussi modifier LUFS/LRA.
La LRA d'Enma augmente de 6,3 à 10,1 LU mesurés : sa dynamique n'a pas été
compressée et ses données sont strictement identiques. Ces observations ne
constituent pas une validation à l'écoute.

Données : [comparaison CSV](COMPARAISON.csv), [comparaison JSON](COMPARAISON.json),
[sortie après correction](APRES_MGBA.json).

## Boucles et événements réellement testés

- Slot 8 : 5 retours natifs, introduction non répétée, contrôle continu du canal et du pointeur, corrélation initiale 0.9815.
- Slot 13 : 5 retours natifs, introduction non répétée, contrôle continu du canal et du pointeur, corrélation initiale 0.9683.
- Slot 14 : 6 retours natifs, introduction non répétée, contrôle continu du canal et du pointeur, corrélation initiale 0.9926.
- Slot 25 : 5 retours natifs, introduction non répétée, contrôle continu du canal et du pointeur, corrélation initiale 0.9825.

- Final Battle conserve exactement la variante C : 34,5634202855 s →
  184,9634501831 s (échantillons 462424 → 2474626).
- Combat réel contre Matt, maintenu au menu d'action natif pendant
  **46 029 images, soit environ 770,65 s (12 min 50,65 s)** : cinq retours de
  boucle, aucun arrêt du canal ; victoire via contrôleur, musique de victoire
  native slot 22 puis conclusion slot 26. Progression, téléportation et équipe
  renforcée sont des fixtures de test en mémoire, pas des modifications du jeu.
- Dialogue réel avec Enma tenu ouvert 150,68 s : le morceau se termine comme
  prévu vers 119 s et le silence final est confirmé (RMS alternatif 0).
  Refuser l'offre restitue normalement la musique d'exploration.
  C'est la limitation explicitement acceptée par l'utilisateur. Le champ
  historique `requested_continuous_music_goal_met=false` et la mention
  « still needs approval » dans le test décrivent l'ancien objectif de lecture
  continue ; aucune boucle ou solution de secours n'est désormais demandée.
- 31/31 sources vérifiées dans le mélangeur, avant/après bruitages et cris.
- 45 tests de fanfares réussis : les 14 fanfares natives et les reprises
  après obtention d'objet sur les 31 OST.
- 31/31 ressources liées vérifiées contre les sources privées ; masque complet.

Preuves : [boucles](boucles/TEST_MGBA.json), [Matt et Enma](evenements/TEST_MGBA.json),
[lecture des 31 OST](lecture/TEST_MGBA.json), [fanfares](FANFARES_MGBA.json),
[liaison](LIAISON.json). Les captures sont des captures du moteur.
Les tests sont automatisés dans mGBA, pas une écoute humaine ni une partie
complète de l'aventure. Aucune qualité musicale subjective n'est certifiée.

## Intégrité et compilation

Les deux compilations ont réussi. ROM privée : **31 589 579 octets**, environ
30,13 Mio ; marge à 32 Mio : **1 964 853 octets**.

SHA-256 privé :
`6854d73f666d540d4327afa9ed7896c0909004df1f342707361d316176b11ced`.

SHA-256 public, strictement inchangé :
`a00527774542439e1ab0976a45421911c8b067d8bd11730de183c453581b3b3c`.

Le [contrôle intégral](PRESERVATION.json) impose exactement **10 octets modifiés**,
les cinq mots de gain de 16 bits, sans déplacement de symbole. Tous les autres
octets de la ROM privée sont identiques, y compris les 31 données audio,
leurs boucles, les 26 autres gains, le moteur, les graphismes et le gameplay.
Aucune ROM ni ressource audio protégée n'est publiée.

## Conclusion et arrêt du chantier

**Aucun blocage technique détecté dans le périmètre approuvé.** Les 31 OST sont
actives : 30 bouclent, Enma reste en lecture unique selon la décision validée.
La fin d'Enma laisse donc un silence si le dialogue se prolonge.

**Non bloquant :** écoute humaine du mixage et des raccords, notamment de la
variante C expérimentale. Aucun jugement artistique définitif n'est déduit
des corrélations ou des mesures de niveau.

Le chantier audio s'arrête ici jusqu'à nouvel ordre. Aucune autre tâche ni
fusion n'est engagée.
