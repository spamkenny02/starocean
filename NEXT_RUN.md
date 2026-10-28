# Reprise : lettre reçue et chemin de Cool

## Reprise courante — 28 octobre, fichiers restaurés

La ROM exacte a été remise à disposition, SHA256 vérifié ; les sources et le cœur instrumenté sont restaurés. Le blocage décrit dans STATUS.md est historique. Les relances ont été réactivées. L'échéance visée reste le 29 octobre 2026 à 22 h Paris, sans couverture complète revendiquée.

Les fichiers de cette restauration sont dans `starocean/analysis/`, le cœur dans `analysis/snes9x/` (lien local depuis starocean/analysis/snes9x). Les états ci-dessous sont des états d'émulateur, pas des sauvegardes de cartouche :

- Original au panneau : `starocean/analysis/runs/fr_restore_sign/end.state`, 109 397 images. Capture identique à l'ancienne ; point conseillé pour lire le panneau et reprendre la navigation.
- Original, passage étroit : `starocean/analysis/runs/fr_cool_resume/end.state`, 113 265 ; route complète `analysis/route_cool_recovery.json`.
- Original après le combat « Voleur rigolo » : `starocean/analysis/runs/fr_cool_branch2/end.state`, 116 527 ; route complète `analysis/route_cool_recovery_branch.json`. Vue : côté ouest d'un écran avec grande colonne centrale. Navigation non résolue, Cool absent.
- Cible courante : `starocean/analysis/runs/fr_recovery_recheck/end.state`, 115 438, SHA256 `faa3735e12320fc700f85ce86abda2f638bb8aa583cf6c3315d3b4822807bd32` ; route `route_cool_target.json`, finale identique au jalon historique. C'est le replay retenu, 107 799 DMA vérifiés.
- Cible, exploration distincte : `starocean/analysis/runs/fr_recovery_target_extension/end.state`, 124 303, même SHA256 ; route complète `route_recovery_target_extension.json`. Vue : rivière et chemin dallé. **N'a pas rejoint la nouvelle carte de l'original.** 2 513 DMA vérifiés sur cette seule continuation.

Catalogue : 30 579 clés, 2 282 observées, 72 PC observés, DMA0 seulement. Nouvelle source $ED:E9F4 sur 64 octets. Le patch gzip, les positions de lookup et le catalogue correspondent à la nouvelle cible ; les anciens états cible f1586e… ne doivent pas y être chargés.

Prochaine action : lire le panneau sur l'original restauré, résoudre l'embranchement vers Cool, puis adapter la navigation depuis le propre état de la cible. Les tentatives par le couloir au pied de la colonne finissent dans un cul-de-sac. Ne pas annoncer de validation de cette carte sur la cible sur la seule réussite DMA d'un trajet divergent. Si les états disparaissent, reconstruire les routes depuis le reset avec leur SHA256 exact.

Les contrôles courants sont `recovery_target_validation.json`, `recovery_extension_validation.json`, `recovery_observation_validation.json` et `recovery_scenario_coverage.json`. Deux captures tronquées ont été exclues du replay retenu ; le premier essai au journal tronqué n'est pas une validation.

## Historique du point précédent

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
