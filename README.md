# Star Ocean FR — suppression du S-DD1

Portage expérimental du mécanisme 96 Mbit vers la traduction française BadCompany. **Le jeu complet n’est pas encore couvert.**

La version élargie contient 18 572 adresses sources, dont 609 observées pendant les relevés. Les routines des canaux DMA 0 et 1 sont implantées ; seul le canal 0 a été exercé par les parcours de jeu actuels. Le contrôle de recherche compare les 24 bits de l’adresse source afin d’éviter les collisions du premier prototype.

Le test de 42 815 images atteint l’introduction, la maison, un changement de pièce et les menus objets, statut et équipements avec le S-DD1 désactivé. Les 27 919 transferts redirigés ont tous une empreinte longueur/FNV32 connue des exécutions de référence. L’image finale des équipements est identique à celle de la ROM française d’origine. Ce résultat ne prouve pas le fonctionnement du reste du jeu.

- [Reproduction et fichiers d’entrée](INPUTS.md)
- [État, limites et objectif complet](STATUS.md)
- [Résultats structurés du dernier test](analysis/extended_validation.json)
- [Patch BPS élargi expérimental, compressé avec gzip](patches/Star_Ocean_FR_extended_EXPERIMENTAL.bps.gz)
- [Ancien prototype limité à l’ouverture](patches/Star_Ocean_FR_opening_EXPERIMENTAL.bps.gz)

Les ROMs complètes, états de jeu, données graphiques extraites et bibliothèques compilées ne sont pas publiés. Les catalogues ne contiennent que des adresses, longueurs et informations de validation ; la reconstruction nécessite la ROM source exacte.

Crédits : neviksti (hack 96 Mbit original), Snes9x et Andreas Naive (décompresseur), BadCompany et ses collaborateurs (traduction française). La licence Snes9x des sources tierces est conservée. Aucune licence globale nouvelle n’est attribuée aux contenus tiers.
