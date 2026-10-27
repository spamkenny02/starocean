# Reprise après Baird et le retour au QG

Dernier jalon : Baird est franchi sans S-DD1. Le replay de 85 650 images atteint la même vue dorée extérieure du QG que l’original, après nuit, réveil, retour au QG et dialogue avec l’ancien. La suite de cette transition n’est pas encore identifiée ; ne pas prétendre avoir atteint Cool ou lu entièrement une lettre sans voir la scène.

## États privés exacts

- Original : `analysis/runs/fr_chapter2_live/end.state` (copie composée : `analysis/runs/fr_chapter2_reference/end.state`), 85 650 images, SHA256 `a31a931a7fb66f2d3486af8d3bda261ea9aa2e40e47a6120cd87f368d332c3dd`.
- Prototype courant : `analysis/runs/fr_chapter2_groups2/end.state`, 85 650 images, SHA256 `9718581903ccf9cf74308ff611fdbecf6c5cb412f5a7b7b64c974a5ffe676e51`.
- Route complète depuis le reset : `analysis/route_chapter2.json`. Les touches automatiques avant 24 000 images restent définies dans run_headless.py.

Le workspace est `/workspace/scratch/872b8bba255b`. Les outils et le cœur sont dans `analysis/`, la copie publique dans `starocean/analysis/`. Ne jamais charger un état d’un autre SHA256. Toute nouvelle reconstruction impose une relecture depuis le reset pour la nouvelle cible.

## Catalogue et outils

30 267 clés : 1 976 observées sur l’original, 8 demandées par le prototype avec source physique déduite, 28 283 autres déduites/comparées. 70 PC observés, 110 hooks, gestionnaires DMA0/1 de 152 octets ; seul DMA0 a été exercé en jeu.

La routine autour de l’offset source 0x39900 lit deux blocs de 64 octets. La seconde adresse ajoute le déplacement Y+3 au premier pointeur. `derive_paired_dma_sources.py` récupère ces sources à partir d’ancrages figés, de la consommation du décodeur et de suites de deux entrées de neuf octets au minimum. `paired_dma_sources.json.gz` contient 16 032 entrées et 11 945 clés secondaires distinctes ; toutes ne sont pas observées en jeu.

Le constructeur conserve les cases existantes avec `--lookup-slots lookup_slots.json.gz`. Après extension, ajouter `--write-lookup-slots lookup_slots.json.gz` et versionner le manifeste. Les 19 103 anciennes cases sont inchangées ; le prototype d’ouverture garde son SHA256 historique. Exécuter validate_catalog.py et le round-trip BPS après chaque reconstruction.

Attention : un gel sur une source absente peut être masqué par NMI, PC 00:F9F9. L’ancienne continuation s’arrêtait ainsi sur F8:9E1B alors que les empreintes DMA précédentes passaient. Cette source est désormais intégrée par la règle des paires de deux entrées, et le comparateur détecte les sources DMA non résolues persistantes. S-DD1=false et absence d’échantillon au gestionnaire ne suffisent pas à valider un parcours.

## Suite

1. Continuer la scène dorée sur l’original avec des attentes et confirmations courtes, relever le texte et la prochaine destination.
2. Rejouer la même continuation sur le prototype du même SHA256 ; corriger le parcours si les timings divergent et conserver une route distincte si nécessaire.
3. Poursuivre vers Cool, puis Metox et Calnus. Confirmer chaque scène à l’écran. Ne pas limiter le suivi aux empreintes : contrôler mouvements, dialogues, combats, effets et menus.
4. Fusionner les traces et garder séparées observations originales, demandes du prototype et déductions statiques.

Dernier bilan : 70 052 DMA redirigés, 1 914 tuples vérifiés, aucune erreur de décompression ni arrêt détecté ; 40 captures identiques sur 126, dont la dernière. La couverture du scénario entier, SRAM/sauvegarde de cartouche, chargement et matériel réel restent à établir. Les états instantanés ne prouvent pas la sauvegarde de cartouche.

Ne publier ni ROM, ni données graphiques extraites, ni états privés. Code, routes, métadonnées, empreintes et patches différentiels uniquement.
