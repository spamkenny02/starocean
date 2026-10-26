# Objectif : version française complète sans S-DD1

La cible est la traduction BadCompany fournie. La version actuelle reste expérimentale : aucune validation du jeu entier n’a été faite.

## Résultats acquis

- Prototype d’ouverture conservé et reproductible : SHA256 cible `e00caf90b85cfcb216b1fc5462511dd7a5b1cbf368f355fb527371103b86bec3`.
- Catalogue étendu : 18 572 adresses, 609 observées, aucune ambiguïté de page source constatée dans les relevés présents.
- Recherche par clé complète 24 bits ; validation de chaque destination, de ses octets décompressés et de l’absence de chevauchement. Distance de recherche maximale : 119 cases.
- Gestionnaires DMA0/1 de 152 octets, 110 points d’appel. Canal 1 non exercé en jeu à ce stade.
- Placement étendu utilisant des banques complètes et des demi-banques de 32 Kio, avec contrôle des limites de DMA et des plages réservées.
- Introduction, déplacement dans la maison, changement de pièce et menus objets/statut/équipements testés sans S-DD1 sur Snes9x.
- 27 919 transferts redirigés, tous avec une empreinte longueur/FNV32 connue. Les nombres de répétitions et timings peuvent différer ; aucune comparaison universelle image par image n’est revendiquée.
- Patch BPS redécodé et comparé octet par octet à la ROM produite, avec les trois CRC vérifiés.

## Travail restant avant une version complète

- Établir l’exhaustivité des tables françaises et les longueurs effectivement demandées pour les entrées seulement déduites.
- Couvrir les autres cartes, les transitions, les combats, effets et scènes du scénario.
- Vérifier les points d’appel non rencontrés et les autres canaux DMA éventuellement utilisés.
- Tenir compte de l’état des registres de remappage si une même adresse CPU est observée avec plusieurs sources physiques ; le fusionneur signale ces conflits.
- Tester réellement sauvegarde et chargement. Le déplacement de 83 opérandes SRAM ne suffit pas à les valider ; le mapping SRAM de la cible doit également être vérifié.
- Tester du matériel compatible avec ce mapping particulier. Une exécution sur le cœur instrumenté n’est pas une validation matérielle.

Le gestionnaire s’arrête sur une case vide si une source manque. Les longueurs du catalogue sont des longueurs de reconstruction, pas une preuve que tous les DMA du jeu ont été recensés.

Le prochain jalon porte sur des parcours extérieurs et les combats, tout en poursuivant l’analyse des tables non résolues. Les sauvegardes feront l’objet d’un contrôle distinct des états instantanés d’émulateur.
