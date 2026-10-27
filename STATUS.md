# Objectif : version française complète sans S-DD1

La cible est la traduction BadCompany fournie. La version actuelle reste expérimentale : aucune validation du jeu entier n’a été faite.

## Jalon précédent

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

## Reprise du 27 octobre — scénario initial

La référence instrumentée atteint la sortie du QG (petite pièce attenante, passage inférieur droit), les deux groupes de voleurs puis Baird et le dialogue dans la maison. Parcours complet depuis le reset : `analysis/route_story_oct27.json`, 60 820 images. Le personnage n'était pas devant une sortie dans le bas de la grande salle : cette tentative était bloquée par le décor.

Catalogue : 19 103 adresses (+531), dont 1 779 observées sur l’original (+1 170), longueur de reconstruction cumulée 1 882 158 octets, aucun conflit de source physique recensé. Il reste 17 321 entrées déduites des comparaisons/structures et trois demandes du prototype avec source physique déduite. Les longueurs observées sont les maxima des relevés présents, pas une preuve d'exhaustivité future.

69 points d'appel de DMA compressé observés au total (+6), couverts par les 110 remplacements existants. Les nouveaux PC sont `$C0:23BA`, `$C0:23EB`, `$C0:2BF6`, `$C3:9550`, `$C3:993B`, `$C3:9957` (voir le fichier versionné pour la liste exacte). Aucun nouveau canal rencontré : seul DMA0 reste exercé en jeu. Aucun changement des octets des gestionnaires n'a été nécessaire à cette extension.

Reconstruction : cible SHA256 `10837701a3b53b572346785e95b77148e3aadd9ecc23bc37824a0f798e02d91e`. Les 19 103 destinations passent le validateur indépendant (distance maximale 120). Le BPS est redécodé octet par octet et ses trois CRC sont contrôlés.

Attention à l'instrumentation : la bibliothèque locale compilée avant la dernière modification de `dma.cpp` sous-comptait les transferts (638 sur la première tentative). Elle a été recompilée ; ce premier décompte ne constitue pas la preuve de validation. `analysis/story_validation.json` porte le résultat de la relecture effectuée avec le cœur reconstruit.

Le premier replay de Baird a réellement échoué sur la boucle `$64:8096` : source DMA0 `$F6:4345`, 64 octets, absente du catalogue. `analysis/baird_missing_source.json` conserve ce diagnostic. La correction est conservée séparément dans `patched_runtime_requests.json` (priorité 9), sans la présenter comme une observation de la ROM originale. La source physique `$36:4345` est déduite du mapping par défaut et des sources voisines vérifiées ; elle doit encore être confirmée par un DMA original équivalent.

Le comparateur exploite maintenant la clé source sauvegardée sur la pile du gestionnaire pour contrôler chaque tuple clé/longueur/empreinte contre une décompression indépendante de la ROM française. Les empreintes absentes de la route originale restent comptées séparément, même lorsqu'elles passent ce contrôle. Un échantillon pris dans la boucle d'arrêt invalide la validation.

Les demandes supplémentaires identifiées pendant les essais successifs de Baird sont `$F6:4345`, `$F4:2349` et `$EB:C443`, chacune sur 64 octets. Elles ne sont pas reclassées comme observées sur l'original. Le relevé avec rythme d'attaque différent (`route_baird_reference_variant.json`) a apporté 16 autres nouvelles adresses et 36 observations supplémentaires ; il n'a pas confirmé ces trois demandes. Ses 27 233 transferts sont décrits dans `baird_variant_observed.json.gz`.

### Résultat du dernier replay de la cible publiée

Sur les 64 145 images demandées, le prototype passe la sortie du QG et les deux groupes de voleurs, puis se bloque pendant Baird : nouvelle source manquante `$EB:C3D8`, 64 octets. Elle n'est pas encore intégrée. Le compteur d'images continue pendant la boucle d'arrêt : ce nombre n'est donc pas une progression de scénario réussie.

38 944 transferts ont été redirigés avant le blocage. Les 1 517 tuples distincts clé/longueur/empreinte vérifiés correspondent tous à une décompression de la source française choisie dans le catalogue. Sept paires longueur/FNV32 ne figurent pas dans la route originale principale, mais passent ce contrôle par clé ; elles ne sont pas présentées comme observées sur l'original. Les trois sources ajoutées depuis les demandes du prototype conservent une provenance physique déduite.

S-DD1 est désactivé sur les 114 échantillons, aucun transfert S-DD1 résiduel n'est journalisé, mais dix échantillons atteignent la boucle d'arrêt. Le comparateur échoue donc volontairement (`dma_checks_passed=false`). Les 84 captures comparées n'en ont que 23 identiques ; les combats divergent en timing et en décisions. Aucune équivalence visuelle complète n'est revendiquée.

La première action suivante est de traiter `$EB:C3D8`, puis de refaire la reconstruction et le parcours. La référence originale, indépendante, a terminé Baird et atteint les dialogues chez la mère de Ratix à 64 145 images. Ni la sauvegarde de cartouche, ni Cool/Metox/Calnus, ni le jeu complet ne sont validés sur ce prototype.


## Nouveau jalon — sources secondaires et Baird franchi

La source `$EB:C3D8` et les demandes suivantes provenaient des **secondes lectures** d’une routine de deux DMA de 64 octets. L’adresse secondaire n’est pas stockée sous forme d’un pointeur 24 bits complet : elle est calculée à partir du premier pointeur et d’un déplacement à Y+3. Cela explique son absence dans la recherche des pointeurs bruts.

L’analyse contrôlée retrouve les huit demandes manquantes identifiées : `$F6:4345`, `$F4:2349`, `$EB:C443`, `$EB:C3D8`, `$F2:FD90`, `$F2:ACA4`, `$ED:4576`, `$EC:3032`. Elle retient 16 032 entrées de table et 11 945 sources secondaires distinctes, avec une provenance déduite. Le résultat est reproductible depuis un manifeste d’ancrages figé. Il ne prouve pas que toutes ces lectures ont lieu dans le jeu.

Catalogue courant : **30 267 adresses**, dont **1 976 observées sur l’original**, 8 demandées par le prototype avec source physique déduite, et 28 283 autres déduites/comparées. Depuis le commit a231e4c : +11 164 clés, +197 clés observées sur l’original. 70 PC de DMA compressé observés (+1, `$C2:10B8`), couverts par les 110 hooks existants. Seul DMA0 est exercé en jeu ; DMA1 reste implanté sans validation de scénario.

Le constructeur peut désormais conserver les positions de recherche existantes. Les 19 103 positions du jalon précédent restent inchangées après l’extension ; reconstruire uniquement avec ces positions reproduit exactement le SHA256 précédent. Le prototype d’ouverture conserve aussi son SHA256 historique. Les contrôles indépendants valident les 30 267 destinations, sans chevauchement, distance de recherche maximale 211. La cible courante est `9718581903ccf9cf74308ff611fdbecf6c5cb412f5a7b7b64c974a5ffe676e51` ; le BPS est vérifié par redécodage complet et trois CRC.

Le premier replay avec les sources appariées a passé Baird et atteint la nuit dans la maison à 64 145 images : 49 579 transferts redirigés, 1 713 tuples source/longueur/empreinte contrôlés sans erreur, aucun échantillon de boucle d’arrêt, S-DD1 désactivé. Il ne faut pas confondre cette réussite avec une équivalence image par image du combat.

La référence originale a poursuivi jusqu’à 85 650 images : nuit, réveil, sortie de la maison, retour au QG, Milly à l’extérieur puis dialogue avec l’ancien. Dernière image : extérieur du QG avec une teinte dorée, pendant une transition de scène. La suite de cette scène et le départ vers Cool ne sont pas encore attestés. Les dialogues ne doivent pas être nommés « lettre entièrement lue » sans vérification supplémentaire.

Le même parcours de touches est rejoué sur la cible finale ; son résultat figure dans `analysis/story_validation.json`. Les positions divergent après les combats : la continuation précédente atteignait le retour en ville, sans rejoindre le QG avec les mêmes entrées. Une validation DMA réussie ne certifie donc pas une couverture identique de scénario. Sauvegarde de cartouche, chargement, autres canaux et matériel réel restent non validés.

### Correction de l’arrêt masqué et résultat final

Une première continuation après Baird s’immobilisait sur `$F8:9E1B`, 64 octets : image strictement inchangée malgré les commandes, source/longueur DMA persistantes et PC échantillonné à l’entrée NMI. Les contrôles d’empreintes restaient corrects et aucun échantillon ne montrait directement la boucle du gestionnaire. `masked_stall.json` conserve cet échec ; le comparateur signale désormais les sources DMA non résolues persistantes.

Cette lecture est bien la seconde source d’une paire : premier pointeur `$F8:9E04`, déplacement 23, entrée à l’offset source `0x49861`. Elle était exclue par l’exigence initiale de trois entrées consécutives. Le filtre exige maintenant deux entrées structurées, avec les mêmes contrôles de code, consommation du décodeur et ancrages. Le manifeste final régénéré est identique depuis ses ancrages figés. Les 11 945 sources secondaires demeurent classées comme déductions ; ce nombre ne mesure pas une couverture de jeu.

La cible finale a été rejouée depuis le reset jusqu’à 85 650 images : **70 052 transferts redirigés**, **1 914 tuples source/longueur/empreinte** vérifiés sans erreur, aucun échantillon de boucle d’arrêt ni source DMA non résolue persistante, S-DD1 désactivé. Quarante empreintes de transfert ne figurent pas dans la route originale principale mais passent le contrôle indépendant par clé ; elles ne deviennent pas pour autant des observations sur l’original. Parmi 126 captures communes, 40 sont identiques, dont la vue finale dorée du QG. Le replay franchit Baird, la nuit, le réveil, le retour au QG et le dialogue avec l’ancien. La continuation exacte de la scène dorée reste à relever avant de nommer la suite.

Les deux états privés à 85 650 images sont prêts pour poursuivre chacun avec son SHA256 propre. Le prochain jalon est la fin de cette scène puis le départ vers Cool. Aucune sauvegarde de cartouche, aucun chargement SRAM et aucun matériel réel n’ont été validés.
