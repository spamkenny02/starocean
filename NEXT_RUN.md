# Point de reprise courant — 30 octobre 2026

Les fichiers privés sont actuellement présents. Les sections plus bas décrivent l'historique et des points parfois perdus ; cette section fait foi pour la reprise courante.

- Original : `analysis/runs/fr_oct29_tablet/end.state`, **131 767**, SHA256 `a31a931a7fb66f2d3486af8d3bda261ea9aa2e40e47a6120cd87f368d332c3dd`. Cool, scène chez Maltos/Milly couverte ; dialogue extérieur de Dorn et Milly encore ouvert. Finir cette scène, vérifier le retour effectif à Clatos et reprendre le départ vers Metox. Route depuis le reset : `analysis/route_oct29_cool_original.json` (composition de segments exécutés, pas un nouveau replay intégral d'un seul tenant).
- Cible : `analysis/runs/fr_oct30_target_resume/end.state`, **129 651**, SHA256 `eda13e6d09f0783e6854d552a1a62e4a460ae7c32b00143d9dbb1aec2ccc0aa0`. Titre « Village Cool » visible à l'entrée. Rejouer d'abord l'homme infecté, l'arrivée de Milly puis la maison de Maltos, en adaptant les déplacements. Route complète : `analysis/route_oct29_cool_target.json`. Ne charger aucun état de faa3735e… dans cette cible.
- Contrôle technique supplémentaire : `analysis/runs/fr_oct30_metadata_check/end.state`, 129 711, même SHA cible ; simple attente de 60 images destinée à vérifier `start_frame`, pas un nouveau jalon de scénario.

Catalogue : 30 588 clés, 2 343 observées, neuf ajouts et 52 promotions depuis 178f919 ; 72 PC observés, 110 hooks, DMA0 seulement. L'ancien arrêt CF:8A5D / 24 576 octets est corrigé et franchi en replay depuis le reset. Validations : `oct29_rebuilt_target_validation.json`, `oct30_target_*_validation.json`, `oct30_bps_validation.json`, `oct30_cool_scenario_coverage.json`.

En cas de perte d'états, reconstruire les routes depuis le reset avec la ROM et le SHA correspondants. Les états ci-dessus sont des états instantanés d'émulateur ; aucune validation de sauvegarde de cartouche n'en découle. Ni Metox, ni Calnus, ni le scénario entier ne sont validés. Aucun nouveau cycle autonome ne doit présenter la cible de calendrier comme accomplie.

---

# Reprise après nouvelle perte du workspace

Dernier travail du 29 octobre : audit ROM-free dans `analysis/public_evidence_audit.json`. Les routes complètes `analysis/route_sign_front_from_reset.json` et `analysis/route_sign_neighbor_from_reset.json` sont prêtes pour une reprise depuis le reset ; leur composition a été vérifiée, pas rejouée. La ROM manque toujours. Aucun compteur de scénario nouveau.


## Nouvelle perte du workspace — 28 octobre 2026

Une maintenance a de nouveau supprimé les fichiers locaux, y compris la pièce jointe française remise à disposition le matin, le cœur compilé et les états. La vérification après maintenance confirme leur absence et les sessions interactives ne sont plus accessibles. Aucun accès de lecture permettant de restaurer la pièce jointe n'est exposé ici ; ne pas chercher de fichiers privés dans d'autres espaces.

Le dernier jalon technique publié reste **178f919** : 30 579 clés, 2 282 observées, 72 PC observés et cible `faa3735e12320fc700f85ce86abda2f638bb8aa583cf6c3315d3b4822807bd32`. Aucun nouveau patch ni contrôle complet n'a été publié depuis. Des combats supplémentaires et un décompte exploratoire de 26 clés potentiellement promouvables avaient été relevés, mais les traces ont disparu avant fusion, vérification indépendante et publication : **ne pas les ajouter au compteur de couverture**.

Deux continuations originales effectivement rejouées avant la maintenance sont désormais conservées sans ROM, image ou état :
- `analysis/route_sign_front_continuation.json`, départ 109 397, arrivée 111 942 : lecture du panneau depuis sa face avant. Texte vu à l'écran : « Ouest: Village Cool » et « Sud: Ville de Clatos ». La lecture depuis le nord indiquait seulement l'envers de la pancarte. Cette séquence contient les tâtonnements et les pages de dialogue réellement exécutés ; aucune optimisation non rejouée n'est présentée comme testée.
- `analysis/route_sign_neighbor_continuation.json`, départ 109 397, arrivée 109 561 : trajet court vers l'écran voisin, confirmé par relecture normale après diagnostic. L'écran montre un chemin à l'ouest d'une grande colonne ; ce n'est pas une arrivée attestée à Cool.

Ces JSON sont des intervalles absolus [début, fin, masque], uniquement sur l'original SHA256 `a31a931a7fb66f2d3486af8d3bda261ea9aa2e40e47a6120cd87f368d332c3dd`. En l'absence d'état, reprendre depuis le reset la route publique route_cool.json limitée à 109 397, puis ajouter l'une de ces continuations. Elles ne contiennent pas le préfixe du reset. Les captures étaient visibles pendant les essais, mais leurs fichiers/empreintes n'ont pas été conservés ; ne pas inventer de SHA256 de PNG.

Le diagnostic de navigation en lisant une structure d'acteur à l'offset WRAM 0x6a46 donnait des valeurs transitoires/stagnantes pendant des combats et changements de carte. Il ne constitue pas une position principale fiable dans tous les contextes. Les branches de recherche à partir d'états ne prouvent ni l'exhaustivité des sorties ni l'impossibilité de passer une colonne. Aucun script diagnostique perdu ou non vérifié n'est publié comme solution.

Prochaine action nécessaire : rétablir `upload/Star Ocean FR.smc` (6 291 456 octets, SHA256 ci-dessus), cloner le dernier main, reconstruire le cœur et la cible, valider catalogue et round-trip BPS, puis reconstruire les points depuis les routes publiques. Les chemins privés de la section précédente sont historiques et actuellement absents. Reprendre ensuite la navigation vers Cool et sa validation sur le propre état de la cible. Les sauvegardes de cartouche restent distinctes des états d'émulateur ; aucune validation SRAM nouvelle.

Le travail est bloqué par l'absence de l'entrée privée, et non achevé. L'échéance du 29 octobre à 22 h Paris reste une cible non atteinte.


# Reprise : lettre reçue et chemin de Cool

## Historique du matin — fichiers restaurés puis reperdus

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
