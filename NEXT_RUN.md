# Reprise après le relevé de Clatos

Lire STATUS.md et analysis/story_validation.json avant de reconstruire. Le scénario complet n'est pas terminé.

## Référence originale

La sortie du QG se trouve dans la petite pièce accessible par l'ouverture noire au nord-est de la grande salle. Dans cette petite pièce, aller vers le passage inférieur droit, centré dans l'ouverture : le bord droit bloque le personnage. Le bas de la grande salle n'était pas la sortie.

La référence a passé les deux groupes de voleurs puis Baird. Dernier état privé : `/workspace/scratch/872b8bba255b/analysis/runs/fr_story_baird_reference/end.state`, 64 145 images, même SHA256 original `a31a931a7fb66f2d3486af8d3bda261ea9aa2e40e47a6120cd87f368d332c3dd`. Capture finale : dialogue « Mère de Ratix : À bientôt. » dans la maison. Une variante d'attaques existe dans `analysis/runs/fr_baird_reference_variant/`, avec sa propre route et le même SHA256. Ne pas remplacer l'un par l'autre implicitement.

Le parcours complet est versionné dans `analysis/route_story_baird.json`. L'autre route, `route_baird_reference_variant.json`, change le rythme des confirmations à partir de 53 030 images. Cette variante a ajouté 16 adresses au catalogue et confirmé 36 clés supplémentaires sur l'original.

## Prototype

Dernière cible reconstruite : SHA256 `10837701a3b53b572346785e95b77148e3aadd9ecc23bc37824a0f798e02d91e`. Catalogue 19 103 clés : 1 779 observées sur l'original, 17 321 déduites des comparaisons/structures, 3 demandées par le prototype avec source physique déduite. Le détail des résultats et de tout blocage de Baird figure dans `analysis/story_validation.json` et STATUS.md.

Les essais ont identifié les sources manquantes `$F6:4345`, `$F4:2349` et `$EB:C443`, 64 octets chacune. Elles sont désormais intégrées via `patched_runtime_requests.json` et `merge_catalogs.py`, sans les classer comme lectures observées sur l'original. Les sources physiques présumées suivent le mapping par défaut déjà vérifié sur les sources voisines. Les essais précédents sont documentés dans `baird_missing_source.json`.

Le cœur local doit être recompilé après application de `snes9x_port_test.patch`. Une ancienne bibliothèque sous-comptait les transferts. Le nouveau journal plain_dma.csv ajoute la clé d'origine sauvegardée sur la pile du gestionnaire, après longueur/empreinte/PC. `compare_replays.py` vérifie la décompression par clé et détecte les échantillons de boucle d'arrêt `$64:8096`/`$64:8196` ; S-DD1=false ne suffit pas à prouver qu'un combat fonctionne.

## Actions suivantes

1. Traiter la source manquante **`$EB:C3D8`, 64 octets**, repérée pendant Baird sur le dernier prototype. Elle n’est pas encore intégrée. Dernier état privé du prototype : `analysis/runs/fr_baird_three_keys/end.state`, SHA256 `10837701a3b53b572346785e95b77148e3aadd9ecc23bc37824a0f798e02d91e`, 64 145 images, boucle d’arrêt. Les 38 944 transferts précédents passent les 1 517 contrôles par clé, mais le replay global échoue. Ne pas revendiquer la validation de Baird. Le journal et les échantillons contiennent la clé DMA0 ; un état privé du même SHA256 permet aussi de lire les exports debug_dma_source/debug_dma_length.
2. Poursuivre la référence originale depuis les dialogues dans la maison : retour au QG, lettre, puis départ vers Cool et Metox. Confirmer la scène à l'écran avant de la nommer dans le bilan.
3. Fusionner les nouvelles traces, reconstruire, exécuter validate_catalog.py et le round-trip BPS, puis rejouer les routes sur la nouvelle cible depuis le reset. Ne jamais charger un état d'un SHA256 différent.
4. Préserver la distinction entre état instantané et sauvegarde de cartouche. SRAM, chargement, autres canaux et matériel réel restent à tester.

Les ROMs, images de jeu et états sont privés ; ne publier que code, routes, métadonnées, empreintes et patches différentiels.
