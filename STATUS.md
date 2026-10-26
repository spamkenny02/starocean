# État et limites

## Prototype d’ouverture

- Image de 12 Mio, mapping 96 Mbit particulier.
- Gestionnaire DMA0 de 128 octets ; 109 signatures d’appels remplacées.
- 570 adresses sources, 571 tuples observés banque/adresse/longueur.
- Audio : banque E3 → 43 et deux lecteurs de banques adaptés.
- Déplacement de 83 opérandes SRAM : sauvegardes non validées.
- Test de 24 000 images, introduction puis maison ; S-DD1 désactivé dans le cœur.
- Tous les couples longueur/FNV32 distincts des transferts redirigés sont connus de la référence ; l’ordre et le nombre de répétitions diffèrent.

## Objectif suivant : couverture du jeu

- Retrouver les autres tables et transferts et distinguer les candidats des références exécutées.
- Couvrir les banques remappées, les autres canaux DMA et les appels non interceptés.
- Adapter le placement au volume total et éviter les collisions source/banque.
- Tester exploration, transitions, combats et menus.
- Vérifier réellement sauvegarde/chargement et matériel compatible.

Le gestionnaire s’arrête sur une case vide pour une source absente de son catalogue : le prototype n’est donc pas utilisable comme version complète.
