# Nuit progressive autour de Lavanville

Les 32 dernières cases des Routes 8, 10 et 12 avant Lavanville assombrissent progressivement le décor selon la distance à la ville. La teinte diminue en repartant. À la frontière, elle rejoint exactement la nuit déjà utilisée en ville. Le nord de la Route 10 reste de jour.

Le calcul porte uniquement sur les palettes matérielles du décor extérieur. Les buffers sources, les palettes des personnages et les banques d'interface restent intacts. La brume et les zombies conservent leur périmètre actuel. Aucun changement du format de sauvegarde, des musiques ou du scénario.

## Vérifications ciblées

Compilation des versions publique et privée réussie. Dans mGBA, 54 contrôles par version : quinze positions sur les trois routes, franchissement réel des trois connexions à pied dans les deux sens, comparaison de toutes les couleurs matérielles avec la transformation attendue, arrêt de dix secondes sans accumulation, menu d'équipe et retour, intérieurs, routes éloignées et teinte nocturne historique de la ville. Les équipes, drapeaux et positions initiales sont préparés pour ces essais ; il ne s'agit pas d'une nouvelle traversée complète de l'aventure.

- [Résultats privés](prive/TEST.json) et [publics](public/TEST.json).
- Marche vers la ville : [Route 8](public/Route8-marche.gif), [Route 10](public/Route10-marche.gif), [Route 12](public/Route12-marche.gif).
- [Jour](public/Route8-00.png), [mi-distance](public/Route8-16.png), [arrivée](public/Route8-32.png).

Le profilage isolé de la routine de palette mesure 25 956 cycles sur la Route 8, contre 124 sans effet auparavant ; en ville, 25 852 contre 22 688. Cela reste inférieur aux 83 776 cycles de VBlank pour cette routine seule et ne constitue pas une mesure de tout le VBlank ni un test sonore. Détails : [PROFIL_CYCLES.json](PROFIL_CYCLES.json).

ROM privée compilée : 33 450 171 octets (+192). ROM publique : 16 110 184 octets. Aucune nouvelle ROM publiée, conformément à la demande de regrouper les corrections avant livraison. Aucun changement sur master.

## Reproduire

Après compilation et chargement de l'environnement de développement :

```bash
NUIT_MODE=prive YOKAI_QA_ROM=$PWD/pokefirered_audio.gba YOKAI_QA_ELF=$PWD/pokefirered_audio.elf python tools/yokai/tester_nuit_progressive_mgba.py
NUIT_MODE=public YOKAI_QA_ROM=$PWD/pokefirered.gba YOKAI_QA_ELF=$PWD/pokefirered.elf python tools/yokai/tester_nuit_progressive_mgba.py
```
