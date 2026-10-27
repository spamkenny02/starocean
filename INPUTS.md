# Entrées privées et reproduction

ROM française attendue : `upload/Star Ocean FR.smc`, 6 291 456 octets, SHA256 `a31a931a7fb66f2d3486af8d3bda261ea9aa2e40e47a6120cd87f368d332c3dd`.

Pour reconstruire le prototype d’ouverture :

```sh
g++ -shared -fPIC -O2 -fwrapv analysis/sdd1_standalone.cpp -o analysis/sdd1.so
python analysis/build_routine_prototype.py
python analysis/make_bps_prototype.py
```

Les patches dans `patches/` se décompressent avec gzip. Le patch `opening` couvre l’ouverture ; le patch `extended` suit les résultats et limites de STATUS.md. Les deux restent expérimentaux et ne doivent pas être présentés comme des patches pour le jeu entier.

Les scripts exploratoires des étapes antérieures demandent aussi la ROM anglaise et le patch anglais fournis séparément, ainsi que les catalogues qu’ils génèrent. Aucun de ces fichiers privés n’est inclus.

Le cœur de test est Snes9x au commit `1bcc369e89f08243e0a462882fb1f3e42e51de3a`. Le patch d’instrumentation et le pilote headless sont inclus. Le pilote demande numpy et Pillow.

Le code du décompresseur conserve sa licence Snes9x. Aucune licence globale nouvelle n’est attribuée aux contenus tiers.

## Reconstruction élargie

```sh
python analysis/build_routine_prototype.py --catalog catalog_extended.json.gz --callsites extended_callsites.json --output FR_extended_experimental.sfc --report routine_port_extended.json --channels 0,1 --full-keys
python analysis/validate_catalog.py
python analysis/make_bps_prototype.py --target FR_extended_experimental.sfc --output Star_Ocean_FR_extended_EXPERIMENTAL.bps
```

SHA256 cible élargie : `10837701a3b53b572346785e95b77148e3aadd9ecc23bc37824a0f798e02d91e`.

Les outils `match_french_streams.py`, `align_pointer_contexts.py` et `merge_catalogs.py` servent à enrichir le catalogue à partir des données privées et des traces. Un bloc seulement déduit doit rester distinct d’un bloc exécuté. Les fichiers `route_menus.json` et `extended_callsites.json` figent les entrées et sites vérifiés pour ce jalon.

`run_headless.py` peut charger un état du même SHA256 de ROM pour continuer un relevé. Ces états sont privés et ne prouvent pas le fonctionnement des sauvegardes de cartouche. Le pilote doit rester à côté du cœur compilé dans `analysis/snes9x/libretro/`.

## Parcours des voleurs et de Baird

`route_story_oct27.json` contient le parcours complet depuis le reset, avec les mêmes entrées automatiques d'introduction que `run_headless.py`. Il inclut les déplacements exploratoires du jalon précédent avant la sortie du QG. `route_story_baird.json` prolonge cette route jusqu’à 64 145 images. Les 60 820 premières images correspondent au premier point après Baird sur la référence française ; les animations et décisions de combat peuvent diverger dans le prototype. Une capture différente n'établit donc pas à elle seule une erreur graphique, et une empreinte connue ne prouve pas toute la scène.

```sh
SO_CAPTURE_FRAMES=41526,45620,47495,50939,52744,56449,60819,64144 python analysis/run_headless.py 'upload/Star Ocean FR.smc' fr_story_baird_reference 64145 analysis/route_story_baird.json
SO_CAPTURE_FRAMES=41526,45620,47495,50939,52744,56449,60819,64144 python analysis/run_headless.py analysis/FR_extended_experimental.sfc fr_baird_three_keys 64145 analysis/route_story_baird.json
python analysis/compare_replays.py analysis/runs/fr_story_baird_reference analysis/runs/fr_baird_three_keys --min-redirected 40000 --output analysis/story_validation.json
```

Recompiler le cœur après application de `snes9x_port_test.patch` : une ancienne bibliothèque peut sous-compter les transferts si elle filtre les anciennes adresses des gestionnaires. `story_observed.json.gz` contient uniquement les tuples d'adresses/longueurs, empreintes, points d'appel, canaux et nombres d'occurrences de la référence, sans octets décompressés.

Dans une session interactive, `{"save":true}` écrit un état instantané et un `run.json` portant le SHA256 de la ROM. Ce mécanisme ne teste pas la sauvegarde de cartouche.
