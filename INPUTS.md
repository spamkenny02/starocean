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

Ce commit appartient au dépôt amont `https://github.com/snes9xgit/snes9x.git` (il n'est pas présent dans le miroir `libretro/snes9x` testé lors de la restauration). Depuis la racine de ce projet :

```sh
git clone https://github.com/snes9xgit/snes9x.git analysis/snes9x
git -C analysis/snes9x checkout 1bcc369e89f08243e0a462882fb1f3e42e51de3a
git -C analysis/snes9x apply ../snes9x_port_test.patch
make -C analysis/snes9x/libretro -j2 LTO= CXX=g++ CC=gcc
```

Le code du décompresseur conserve sa licence Snes9x. Aucune licence globale nouvelle n’est attribuée aux contenus tiers.

## Reconstruction élargie

```sh
python analysis/build_routine_prototype.py --catalog catalog_extended.json.gz --callsites extended_callsites.json --output FR_extended_experimental.sfc --report routine_port_extended.json --channels 0,1 --full-keys --lookup-slots lookup_slots.json.gz
python analysis/validate_catalog.py
python analysis/make_bps_prototype.py --target FR_extended_experimental.sfc --output Star_Ocean_FR_extended_EXPERIMENTAL.bps
```

SHA256 cible élargie courante : `eda13e6d09f0783e6854d552a1a62e4a460ae7c32b00143d9dbb1aec2ccc0aa0`. Le SHA256 faa3735e… reste historique. Le SHA256 f1586e… cité dans les anciens bilans reste historique.

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

## Sources DMA appariées et stabilité des recherches

La routine française autour de l’offset source `0x39900` charge deux fois 64 octets : la première adresse provient des trois octets à Y, la seconde ajoute le déplacement à Y+3 à l’adresse basse, en conservant la banque CPU. Le script `derive_paired_dma_sources.py` vérifie la signature du code, la consommation du décodeur pour le premier bloc et des suites d’au moins deux entrées espacées de neuf octets. `paired_dma_anchors.json.gz` fige les adresses et sources utilisées comme ancrages ; aucune donnée graphique n’y figure. La régénération reproduit exactement `paired_dma_sources.json.gz`. Ces 12 277 sources secondaires sont des déductions statiques, pas autant de lectures exécutées.

Recompiler `sdd1.so` avec le source fourni avant d’exécuter ce script : il expose maintenant `SO_SDD1_input_span`, uniquement pour l’analyse. `merge_catalogs.py` incorpore les déductions avec la priorité 3, les demandes du prototype avec la priorité 9 et les observations originales avec la priorité 10.

Le manifeste `lookup_slots.json.gz` conserve les cases déjà attribuées pour limiter les changements du parcours de recherche. Après un ajout au catalogue, passer aussi `--write-lookup-slots lookup_slots.json.gz` au constructeur et versionner le manifeste mis à jour. La recherche et toutes les destinations sont validées avant écriture ; conserver des cases ne garantit pas une équivalence générale de timing avec l’original.

`route_chapter2.json` prolonge la route jusqu’à 85 650 images sur l’original. Le prototype doit toujours être contrôlé à l’écran : les mêmes touches ne garantissent pas la même progression après des combats dont le timing diffère.

Dernier replay complet : `route_chapter2.json`, 85 650 images, label `fr_chapter2_groups2`. Utiliser `compare_replays.py` avec la référence reconstruite sur cette même route. Le contrôle des sources DMA persistantes est nécessaire : un arrêt peut rester masqué par des interruptions NMI et ne jamais être échantillonné directement à `$64:8096`.

```sh
SO_CAPTURE_FRAMES=41526,45620,47495,50939,52744,56449,60819,64144,67377,70047,73392,76941,80474,81599,85649 python analysis/run_headless.py 'upload/Star Ocean FR.smc' fr_chapter2_reference 85650 analysis/route_chapter2.json
SO_CAPTURE_FRAMES=41526,45620,47495,50939,52744,56449,60819,64144,67377,70047,73392,76941,80474,81599,85649 python analysis/run_headless.py analysis/FR_extended_experimental.sfc fr_chapter2_groups2 85650 analysis/route_chapter2.json
python analysis/compare_replays.py analysis/runs/fr_chapter2_reference analysis/runs/fr_chapter2_groups2 --min-redirected 40000 --output analysis/story_validation.json
```

## Lettre et chemin de Cool

`route_cool.json` enregistre l’original jusqu’à 110 429 images. La même route de touches, rejouée depuis le reset sur le prototype, passe les contrôles DMA mais laisse le personnage à un autre endroit de Clatos. La route distincte `route_cool_target.json` ajoute une correction de déplacement puis un combat extérieur, terminé à 115 438 images. Les deux validations ont des périmètres différents : `cool_validation.json` porte le replay commun ; `cool_target_route_validation.json` porte uniquement la continuation depuis l’état du même SHA256 à 110 429 images.

```sh
SO_CAPTURE_FRAMES=85649,87934,94869,98669,100050,101780,104240,107271,109396,110428 python analysis/run_headless.py analysis/FR_extended_experimental.sfc fr_cool_new_patch 110429 analysis/route_cool.json
python analysis/compare_replays.py analysis/runs/fr_cool_reference analysis/runs/fr_cool_new_patch --min-redirected 50000 --output analysis/cool_validation.json
```

La référence se reconstruit depuis le reset avec la ROM originale et `route_cool.json`, ou par continuation d’un état original du même SHA256. La route target complète se rejoue depuis le reset avec `route_cool_target.json` ; le relevé publié de sa continuation a été produit dans play_session.py depuis l’état courant à 110 429 images.

Le format des tables appariées accepte maintenant aussi deux entrées séparées par trois octets nuls. Le cas contrôlé est l’entrée à `0x69418` : `$F9:7015` + 20 donne `$F9:7029`. Le filtre précédent ne retenait pas cette lecture. Les entrées restent des déductions statiques jusqu’à observation sur l’original.

play_session.py conserve désormais `cpu_samples.json` après chaque commande, avec PC, touches et source/longueur DMA0. Les états enregistrent aussi leur frame de départ et les captures. Ces journaux facilitent la détection d’un arrêt masqué par NMI et distinguent une continuation d’un replay complet.


## Reprise après perte du workspace — 28 octobre

La ROM rejointe sous `Star Ocean FR(1).smc` a exactement le SHA256 attendu. Un lien local `upload/Star Ocean FR.smc` rétablit le chemin des pilotes. Le dépôt public et le cœur Snes9x ont été restaurés ; la ROM anglaise et le patch anglais ne sont pas nécessaires pour reconstruire le catalogue déjà publié.

Le fusionneur accepte maintenant une base publique et des traces originales explicitement choisies, sans dépendre des anciennes analyses privées :

```sh
python analysis/merge_catalogs.py --base analysis/catalog_extended.json.gz --trace analysis/runs/fr_cool_resume/sdd1.csv
```

Les chemins de `--base` et `--trace` sont relatifs au répertoire courant. Le script contrôle le SHA256 de provenance dans run.json, conserve les maxima de longueur et les priorités existantes, et refuse les conflits de sources physiques. Le contrôle indépendant des empreintes des relevés de cette reprise figure dans recovery_observation_validation.json. Ne pas lancer le mode historique sans base lorsque les analyses privées requises sont absentes.

La route `route_cool_recovery.json` rejoint l'original à 113 265 images ; `route_cool_recovery_branch.json` prolonge jusqu'à 116 527. `route_recovery_target_extension.json` est une tentative distincte de navigation sur la cible, non une preuve d'équivalence de scénario. Les résultats courants sont dans recovery_target_validation.json et recovery_extension_validation.json.


## Contrôles possibles sans entrée privée

```sh
python analysis/audit_public_evidence.py
python analysis/compose_route.py analysis/route_cool.json analysis/route_sign_front_continuation.json --checkpoint 109397 --output analysis/route_sign_front_from_reset.json
python analysis/compose_route.py analysis/route_cool.json analysis/route_sign_neighbor_continuation.json --checkpoint 109397 --output analysis/route_sign_neighbor_from_reset.json
```

L'audit ne remplace ni validate_catalog.py sur les octets reconstruits, ni le round-trip BPS, ni les replays. Les fichiers `route_sign_*_from_reset.json` ne changent pas les touches des segments historiques ; leur nouvelle composition reste à rejouer avec la ROM exacte. Les métadonnées distinguent les clés historiquement observées des clés dont le relevé détaillé demeure publié.


## Relevés de Cool — 29–30 octobre

`route_oct29_cool_original.json` compose les segments originaux réellement exécutés jusqu'à 131 767 images. `route_oct29_cool_target.json` compose le reset et les continuations propres à la cible jusqu'à l'entrée de Cool à 129 651. Ces fichiers ne prouvent pas un second replay intégral d'un seul tenant. `route_oct29_river_original.json` conserve séparément l'exploration de la rive est ; `route_oct29_target_missing.json` garde les touches de l'ancien échec sur faa3735e… à CF:8A5D. Les références de ROM et périmètres figurent dans `oct30_cool_scenario_coverage.json` et NEXT_RUN.md.

```sh
python analysis/validate_original_trace.py analysis/runs/fr_oct29_tablet/sdd1.csv --output analysis/runs/fr_oct29_tablet/independent_validation.json
```

Le validateur original exige le SHA exact, vérifie indépendamment chaque empreinte source/longueur et refuse les conflits physiques. Il ne certifie pas la progression visuelle. `run_headless.py` écrit désormais `start_frame` pour distinguer un lancement depuis le reset d'une continuation. Le champ des anciens relevés de cette reprise a été complété depuis les commandes connues ; les états restent privés et ne sont pas des sauvegardes SRAM.
