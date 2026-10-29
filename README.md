# Star Ocean FR — suppression du S-DD1

Portage expérimental du mécanisme 96 Mbit vers la traduction française BadCompany. **Le jeu complet n’est pas encore couvert.**

La version élargie contient 30 579 adresses sources, dont 2 282 observées pendant les relevés. Les routines des canaux DMA 0 et 1 sont implantées ; seul le canal 0 a été exercé par les parcours de jeu actuels. Le contrôle de recherche compare les 24 bits de l’adresse source afin d’éviter les collisions du premier prototype.

Le prototype passe Baird, la nuit, le réveil et les scènes suivantes, dont la lettre annonçant l’épidémie. Une route corrigée permet de sortir de Clatos et de terminer un combat extérieur, avec victoire, passage de niveau et retour au chemin. **Le village de Cool n’est pas encore atteint.** Les timings divergent : les mêmes touches peuvent laisser les deux ROMs à des endroits différents. [Couverture des scènes](analysis/cool_scenario_coverage.json) et [contrôles de la route corrigée](analysis/cool_target_route_validation.json).

- [Audit des preuves publiques, sans ROM](analysis/public_evidence_audit.json)
- [Reproduction et fichiers d’entrée](INPUTS.md)
- [État, limites et objectif complet](STATUS.md)
- [Bilan précédent jusqu’au retour au QG](analysis/story_validation.json)
- [Bilan précédent des menus](analysis/extended_validation.json)
- [Patch BPS élargi expérimental, compressé avec gzip](patches/Star_Ocean_FR_extended_EXPERIMENTAL.bps.gz)
- [Ancien prototype limité à l’ouverture](patches/Star_Ocean_FR_opening_EXPERIMENTAL.bps.gz)

Les ROMs complètes, états de jeu, données graphiques extraites et bibliothèques compilées ne sont pas publiés. Les catalogues ne contiennent que des adresses, longueurs et informations de validation ; la reconstruction nécessite la ROM source exacte.

Crédits : neviksti (hack 96 Mbit original), Snes9x et Andreas Naive (décompresseur), BadCompany et ses collaborateurs (traduction française). La licence Snes9x des sources tierces est conservée. Aucune licence globale nouvelle n’est attribuée aux contenus tiers.
