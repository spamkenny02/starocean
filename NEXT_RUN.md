# Reprise : lettre reçue et chemin de Cool

## Blocage de reprise constaté le 28 octobre 2026

L'inspection du workspace `/workspace/scratch/872b8bba255b` confirme l'absence des répertoires `upload/`, `analysis/` et `starocean/`. Les états privés ci-dessous décrivent les derniers points historiques ; ils ne sont plus disponibles dans cette exécution. Aucun nouveau parcours, transfert DMA, rebuild ou test n'a été exécuté le 28 octobre lors de ce constat.

La ROM source exacte doit être remise à disposition dans ce workspace : `upload/Star Ocean FR.smc`, 6 291 456 octets, SHA256 `a31a931a7fb66f2d3486af8d3bda261ea9aa2e40e47a6120cd87f368d332c3dd`. Ne pas rechercher de fichiers privés ailleurs. Les sources, routes et catalogues publics sont récupérables depuis GitHub ; ils ne remplacent pas la ROM privée.

Après restauration : vérifier le SHA256, récupérer les outils publics et le cœur Snes9x instrumenté indiqué dans INPUTS.md, reconstruire la cible avec les positions de lookup conservées, lancer validate_catalog.py et vérifier le round-trip BPS. En l'absence des anciens états, rejouer depuis le reset `route_cool.json` sur l'original et `route_cool_target.json` sur la cible. Vérifier les scènes à l'écran avant de continuer vers Cool ; charger uniquement un état du même SHA256. Aucun état instantané ne constitue une validation de sauvegarde de cartouche.

Échéance visée : **29 octobre 2026 à 22 h, Europe/Paris**. Le scénario complet reste non validé. Le dernier bilan expérimental demeure celui du commit `babd6e580c54cb2086cbb9ddb40f80ab2ac73e38`.



Cool n'est pas encore atteint. La lettre de l'épidémie, le départ de Milly, la sortie de Clatos et les premiers combats extérieurs sont maintenant relevés. Le prototype a terminé un combat extérieur, gagné un niveau et retrouvé le chemin après correction de son trajet.

## Derniers états privés historiques — absents du workspace actuel

- Original, exploration principale : `analysis/runs/fr_cool_original/end.state`, 110 429 images, SHA256 `a31a931a7fb66f2d3486af8d3bda261ea9aa2e40e47a6120cd87f368d332c3dd`. Route : `route_cool.json`.
- Original, point du panneau restauré : `analysis/runs/fr_sign_checkpoint/end.state`, 109 397 images, même SHA256. La capture est identique au premier relevé. C'est un point pratique pour reprendre l'embranchement sans refaire les combats.
- Original, exploration alternative depuis le panneau : `analysis/runs/fr_cool_west_branch/end.state`, 110 038 images, même SHA256. Route : `route_cool_west_branch.json`.
- Prototype courant : `analysis/runs/fr_cool_target_route/end.state`, 115 438 images, SHA256 `f1586ead9c5f1a95dcc8a5825c6bfe9a3190de59337f2e5fc7c338919135cc1c`. Vue : chemin dallé après un combat extérieur. Route complète : `route_cool_target.json`.

Workspace : `/workspace/scratch/872b8bba255b`. Cœur/pilotes dans `analysis/`, sources publiques dans `starocean/analysis/`. Charger uniquement un état du même SHA256 ; tout rebuild modifiant la cible impose une relecture depuis le reset pour cette cible.

## Navigation et limites

Le guide de progression donne Cool au nord, puis la maison de Milly. Les chemins extérieurs ne sont pas des lignes droites : les tentatives de montée au nord et de passage par l'embranchement supérieur droit sont dans les routes, sans arrivée au village encore attestée. Ne pas annoncer Cool sur la seule présence de la mini-carte. Le point du panneau à 109 397 images évite de repartir du départ de Clatos.

Les mêmes touches ne suffisent pas à synchroniser les deux ROMs après les combats. La route commune de 110 429 images passe les contrôles DMA, mais laisse le prototype à un autre endroit dans Clatos. Sa route distincte ajoute une correction pour sortir entre les deux cheminées au nord, puis un combat extérieur. À la sortie de Clatos, laisser finir la courte scène de dialogue avant de marcher.

## Correctif et catalogue

La lecture manquante F9:7029 venait d'une entrée de neuf octets suivie de trois octets nuls : premier pointeur F9:7015, déplacement 20, table à 0x69418. Le dériveur admet maintenant des entrées voisines séparées par ce terminateur nul. `cool_prior_stall_validation.json` conserve l'ancien échec masqué par NMI ; le contrôle des sources DMA non résolues persistantes le repère.

30 578 clés : 2 274 observées sur l'original, 8 demandées par le prototype avec source physique déduite, 28 296 autres déduites/comparées. 72 PC observés, 110 hooks, gestionnaires DMA0/1 de 152 octets ; DMA1 n'est toujours pas exercé en jeu. Les longueurs cumulées sont 2 743 086 octets : conserver les maxima des DMA réellement demandés, pas uniquement l'adresse ou les 32/64 octets d'un match statique.

Préserver `lookup_slots.json.gz` lors des reconstructions (`--lookup-slots ... --write-lookup-slots ...`). Recompiler sdd1.so si nécessaire ; le dériveur utilise SO_SDD1_input_span. Le catalogue, le BPS et les routes sont versionnés ; ni ROM, ni images de jeu, ni états ne doivent être publiés.

## Suite concrète

1. Reprendre l'original au panneau ou à l'exploration alternative et atteindre réellement le village de Cool ; confirmer son nom et la scène de Milly à l'écran.
2. Continuer aussi le prototype depuis son propre état à 115 438 images, avec une route distincte si nécessaire. Vérifier les contrôles et la progression visuelle, en plus des empreintes.
3. Relever les cartes, combats, textes, menus et effets. Fusionner les nouveaux maxima de longueur et repérer les changements de source physique ; garder les déductions séparées des observations originales.
4. Après chaque reconstruction : validate_catalog.py, round-trip BPS, puis replay de la nouvelle cible depuis le reset. SRAM/sauvegarde de cartouche, chargement et matériel restent à tester séparément des états instantanés.

Bilans : replay commun 97 488 DMA et 1 963 tuples vérifiés ; continuation corrigée du prototype 10 311 DMA et 1 115 tuples. Les tuples des deux périmètres peuvent se recouper. Aucun arrêt ou erreur de décompression détecté dans ces contrôles. Le scénario complet reste à couvrir.
