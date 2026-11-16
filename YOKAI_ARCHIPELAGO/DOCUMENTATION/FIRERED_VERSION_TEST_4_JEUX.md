# Rouge Feu0.5.0 et premier essai à quatre — 16 novembre 2026

## Version de test Rouge Feu

**628 checks actifs par défaut,629 avec l’option Terr’heure.** Les625 identifiants précédents sont conservés ; trois sources classiques supplémentaires sont adaptées : Coupe dans la conclusion Philosovni d’Ariane, Vol dans le refuge Route16 et Force contre le Dentier du Safari. Aucun nouveau sprite, changement de scénario, d’équipe ou de statistique. Le fangame principal est intact.

Coupe, Surf, Force et Flash sont maintenant des objets de progression AP ; Vol est utile et facultatif. Leurs cinq remises originales sont remplacées. Les autres clefs, tickets et badges restent natifs. Recevoir Coupe ne pose plus `FLAG_GOT_HM01` via `PhilosovniRefreshHM` : le flag est réservé à la récompense locale, qui reste collectable après réception distante. Le Dentier conserve sa collecte, son contrôle et sa consommation natives.

Les règles séparent désormais les accès Coupe, Coupe+Flash, Coupe+Flash+Surf et la fin de Ligue qui exige aussi Force. Routes9/10 et l’arène d’Ariane sont derrière Coupe ; Route16 et Fuchsia derrière Coupe+Flash ; Route Victoire, Ligue et sources de la grotte glacée derrière Force également. Les captures de l’étape maritime sont conservativement placées derrière les quatre capacités, afin de ne pas sous-estimer les obstacles de leurs témoins d’acquisition. Vol n’est jamais indispensable. Les badges requis par le moteur demeurent requis : recevoir une CS ne donne pas de badge et ne valide pas sa quête.

Le graphe reste un regroupement conservateur de capacités et d’étapes natives ; ce n’est pas une transplantation exhaustive des entrées FRLG. Boutiques, revanches et Mémorial restent exclus. Le registre256 dresseurs et la sauvegarde AP64octets restent inchangés, transport3/sauvegarde1. Nouvelle partie et nouvelle seed avec le nouveau catalogue obligatoires ; pas de migration d’ancienne seed.

## Tests exécutés

- Compilation depuis une copie neuve du snapshot complet, sans objets de build copiés : binaire identique.
- **620 détecteurs**,2068 assertions dans mGBA : scripts natifs, fixtures de captures/victoires, conservation après sauvegarde et redémarrage à froid. Ce ne sont pas620 parcours physiques complets.
- **44 contrôles avec vrai serveur, client officiel et mGBA** : notamment réception des cinq CS, indépendance du don Coupe, sac plein, envois sortants, reconnect, Wyatt, dresseur ordinaire, captures préparées, et Goal Panthéon.
- **37 protections natives** ; **35 tests unitaires réussis**,8 tests Emerald historiques ignorés faute de leurs fixtures. Trois tests supplémentaires refusent un Emerald absent ou remplacé par du vanilla.
- **Trois seeds à trois mondes** résolubles avec628 checks FR et les quatre capacités indispensables ; une seed optionnelle avec629. Les règles interdisent le Panthéon lorsqu’il manque l’une des quatre capacités. Cela ne valide pas encore une seed à quatre.
- **Finale native complète depuis le quatrième membre du Conseil** : sa victoire, porte, entrée normale, Don Morleone, Don Spiration, conclusion, Panthéon, crédits, sauvegarde et Continuer réussis. Position et équipe renforcée sont des fixtures initiales ; pas d’injection d’issue de combat ou de flag d’histoire ensuite. Ce n’est ni une partie complète depuis le début, ni un test d’équilibrage. Le test réseau du Goal est distinct.

Les preuves JSON sont dans `preuves/firered_cs_*.json`, `firered_finale_normale_ap.json`, `firered_reconstruction_cs.json` et `generation_cs_*.json`. Aucun asset ou enregistrement de jeu n’est publié avec ces preuves.

ROM SHA256 : `94e9cec46c19b351b0ef655c6b11df88237552746e2cdd18c0dac258ad16fc2b`. Source complète locale : `codex/firered-classic-bulk-20261116`, commit `e8695f8564a66795a92d30fa4cd97fe78bb5f2fe`, depuis RC1 `a589cf0057fd0f579d003d8dd58616b3f4649ea2`. Le code d’intégration et les générateurs sont publiés ; sources complètes avec assets, ROM et packages privés restent locaux.

## État du test à quatre

Slots préparés : RougeFeu / Pokémon Yo-kai FireRed ; Dejais / Pokémon Yo-kai Emerald ; Juste Yoann / Yo-kai Watch2 ; Krackonyx / Mario Kart Wii. YW1 exclu. Les trois autres jeux restent fonctionnels selon le retour utilisateur ; le mod visuel MKW reste à ajouter et n’est pas nécessaire au protocole AP.

**Génération à quatre bloquée par un fichier absent sur ce poste :** l’APWorld français Emerald0.2.1 avec signature `pokemon emerald / yokai ap fr2`. L’utilisateur a donné son chemin, mais celui-ci n’existe pas dans l’environnement de cette conversation. Le générateur refuse de substituer une ancienne build ou Emerald vanilla. Le fichier peut être fourni en pièce jointe et restera local. Son absence ne remet pas en cause son fonctionnement sur le poste du joueur. Ni génération ni échange natif à quatre ne sont déclarés réussis.

Le dossier `CONFIG/createurs/quatre_jeux` et `SCRIPTS/generate_four_game_seed.py` sont prêts. Le script contrôle les quatre noms de jeux, le catalogue FR, la version/signature Emerald, génère avec Archipelago officiel puis vérifie victoire collective, sphères et participation des quatre slots aux échanges de progression. Le rapport garde `four_native_games_tested=false` : une génération résoluble n’est pas une preuve de communication en jeu.

## Lancer le premier essai

1. Reconstruire FR avec `SCRIPTS/build_firered.sh` depuis les sources complètes RC1 ; voir le [guide FR](GUIDE_FIRERED_ARCHIPELAGO_FR.md). Ne pas lancer `make clean` sur les entrées binaires originales : repartir d’une copie neuve vérifiée.
2. Copier le package **Emerald français0.2.1 validé** et le package FR issu de cette build dans `Archipelago/custom_worlds`, à côté des mondes YW2/MKW épinglés. Utiliser `SCRIPTS/install_worlds.py` avec `--emerald-apworld` et `--firered-apworld`. Garder les packages privés hors Git.
3. Depuis le dépôt, avec le Python des dépendances Archipelago :

```sh
python YOKAI_ARCHIPELAGO/SCRIPTS/generate_four_game_seed.py \
  --archipelago /chemin/Archipelago --out /chemin/seed-quatre --seed 1611202604
```

Le dossier joueurs par défaut ne contient que les quatre YAML. Ne pas ajouter YW1 ni les modèles historiques. Emerald : objectif Panthéon, postgame exclu ; YW2 : chapitre10 sans postgame ; pièges désactivés. Le dossier de sortie et ses éventuels patchs Emerald restent locaux, car ils peuvent embarquer des données privées.

4. Si `RESULTAT.json` indique `passed: true`, ouvrir le ZIP produit avec `MultiServer.py` et conserver son fichier `.apsave`. Ne pas utiliser `--disable_save` pour la partie des joueurs. Garder le spoiler complet pour l’organisateur uniquement.
5. Appliquer à Emerald le fichier `.apyokaiemerald` produit par cette seed, avec sa base française autorisée. FR utilise la ROM AP reconstruite et un nouveau fichier de sauvegarde. Installer le même APWorld sur générateur/serveur/client.
6. Connecter les quatre installations validées au même serveur, avec leurs noms exacts. Pour FR : `CONNECTORS/mgba/connect_firered.py --archipelago <AP> --server <serveur:port> --slot RougeFeu --emulator-port 43056`. Pour Emerald : `connect_emerald.py --archipelago <AP> --server <serveur:port> --slot Dejais --emulator-port 43055 --record <journal.jsonl>`. Les Lua mGBA correspondants utilisent ces ports distincts. Les clients YW2/MKW sont ceux de leurs intégrations validées.
7. Collecter un vrai check dans chaque jeu ; constater son acquittement serveur et sa récompense dans le jeu destinataire. Tester une récompense distante en direction de chacun des quatre jeux, puis sauvegarde, fermeture et reconnexion sans duplication. Conserver journaux et hashes des packages. Ce relevé sera la preuve du premier échange à quatre ; il n’est pas encore effectué ici.

Ne pas renommer un joueur après génération. Le mod visuel MKW sera ajouté à la même installation Dolphin ultérieurement. Les sphères ne représentent pas des minutes ; garder la règle d’indice après20minutes de blocage réel.
