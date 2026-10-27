# Star Ocean FR — suppression du S-DD1

Portage expérimental du mécanisme 96 Mbit vers la traduction française BadCompany. **Le jeu complet n’est pas encore couvert.**

La version élargie contient 30 267 adresses sources, dont 1 976 observées pendant les relevés. Les routines des canaux DMA 0 et 1 sont implantées ; seul le canal 0 a été exercé par les parcours de jeu actuels. Le contrôle de recherche compare les 24 bits de l’adresse source afin d’éviter les collisions du premier prototype.

Le prototype passe désormais les deux groupes de voleurs et Baird sans S-DD1, puis la nuit, le réveil, le retour au QG et le dialogue avec l’ancien. Le parcours de 85 650 images atteint la même vue finale dorée du QG que la référence. Les combats et les timings divergent : ce résultat n’est pas une équivalence complète image par image. [Le bilan](analysis/story_validation.json) détaille les vérifications. Cool, Metox, Calnus, la suite du scénario et les sauvegardes de cartouche restent à valider.

- [Reproduction et fichiers d’entrée](INPUTS.md)
- [État, limites et objectif complet](STATUS.md)
- [Bilan du scénario et des combats](analysis/story_validation.json)
- [Bilan précédent des menus](analysis/extended_validation.json)
- [Patch BPS élargi expérimental, compressé avec gzip](patches/Star_Ocean_FR_extended_EXPERIMENTAL.bps.gz)
- [Ancien prototype limité à l’ouverture](patches/Star_Ocean_FR_opening_EXPERIMENTAL.bps.gz)

Les ROMs complètes, états de jeu, données graphiques extraites et bibliothèques compilées ne sont pas publiés. Les catalogues ne contiennent que des adresses, longueurs et informations de validation ; la reconstruction nécessite la ROM source exacte.

Crédits : neviksti (hack 96 Mbit original), Snes9x et Andreas Naive (décompresseur), BadCompany et ses collaborateurs (traduction française). La licence Snes9x des sources tierces est conservée. Aucune licence globale nouvelle n’est attribuée aux contenus tiers.
