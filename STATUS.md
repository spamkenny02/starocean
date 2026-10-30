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


## Lettre de l’épidémie et premiers combats sur le chemin de Cool

La référence a couvert la fin de la scène du QG, la lettre annonçant l’épidémie, le départ de Milly, la sortie nord de Clatos, deux combats extérieurs et le dialogue avec Dorn sur le chemin. La mini-carte a été affichée. Le village de Cool n’est pas encore attesté : l’exploration s’arrête dans les chemins et embranchements.

Un ancien replay du prototype s’arrêtait sur `$F9:7029`, 64 octets, juste avant la lettre. Le contrôle des sources DMA persistantes le signale même lorsque le PC est échantillonné dans NMI. Le premier pointeur `$F9:7015` et le déplacement 20 apparaissent à l’offset source `0x69418`, dans des entrées de neuf octets séparées par trois octets nuls. Le dériveur accepte maintenant ce séparateur contrôlé. Il retient 16 482 entrées et 12 277 sources secondaires distinctes, toujours classées comme déduites.

Catalogue courant : **30 578 clés**, dont **2 274 observées sur l’original** (+298 depuis f70bd39), 8 demandes du prototype avec source physique déduite, et 28 296 autres déduites/comparées. +311 clés au total. Les longueurs de reconstruction cumulées passent à 2 743 086 octets (+143 360) : les nouvelles lectures de cartes et de combats nécessitaient aussi des extensions de longueur. Aucun conflit de source physique n’est recensé. 72 PC observés (+2 : `$C0:2E25`, `$C6:0E31`), couverts par les 110 hooks existants ; seul DMA0 est exercé en jeu.

Cible : `f1586ead9c5f1a95dcc8a5825c6bfe9a3190de59337f2e5fc7c338919135cc1c`. Toutes les destinations du catalogue passent le validateur, distance de recherche maximale 211, et le BPS passe le round-trip avec les trois CRC.

Le replay commun depuis le reset atteint 110 429 images : 97 488 transferts redirigés, 1 963 tuples source/longueur/empreinte sans erreur, aucun arrêt détecté. **Cela ne valide pas une progression de scénario identique** : la référence est dans les chemins, tandis que le prototype est encore dans Clatos. La scène de lecture de la lettre est toutefois présente sur les deux ROMs.

Une continuation propre au prototype corrige ensuite la navigation. À 115 438 images, la sortie de Clatos, un combat extérieur contre le groupe avec loup-garou et lapins, la victoire, le passage de niveau et le retour au chemin sont attestés à l’écran. Sur cette continuation seule (départ 110 429) : 10 311 transferts redirigés, 1 115 tuples vérifiés sans erreur, aucun arrêt détecté et S-DD1 désactivé. Ne pas additionner les tuples distincts des deux périmètres comme s’ils étaient disjoints. Les empreintes des captures sont conservées sans publier les images.

Un point original au panneau à 109 397 images a aussi été reconstruit par replay ; sa capture est identique au premier relevé. L’exploration alternative depuis ce point est conservée séparément. La prochaine action est d’achever la navigation vers Cool et d’y couvrir la scène de Milly. Sauvegarde/chargement de cartouche, matériel et scénario complet restent non validés.


## Blocage de reprise constaté le 28 octobre 2026

L'inspection du workspace `/workspace/scratch/872b8bba255b` confirme l'absence des répertoires `upload/`, `analysis/` et `starocean/`. Les états privés ci-dessous décrivent les derniers points historiques ; ils ne sont plus disponibles dans cette exécution. Aucun nouveau parcours, transfert DMA, rebuild ou test n'a été exécuté le 28 octobre lors de ce constat.

La ROM source exacte doit être remise à disposition dans ce workspace : `upload/Star Ocean FR.smc`, 6 291 456 octets, SHA256 `a31a931a7fb66f2d3486af8d3bda261ea9aa2e40e47a6120cd87f368d332c3dd`. Ne pas rechercher de fichiers privés ailleurs. Les sources, routes et catalogues publics sont récupérables depuis GitHub ; ils ne remplacent pas la ROM privée.

Après restauration : vérifier le SHA256, récupérer les outils publics et le cœur Snes9x instrumenté indiqué dans INPUTS.md, reconstruire la cible avec les positions de lookup conservées, lancer validate_catalog.py et vérifier le round-trip BPS. En l'absence des anciens états, rejouer depuis le reset `route_cool.json` sur l'original et `route_cool_target.json` sur la cible. Vérifier les scènes à l'écran avant de continuer vers Cool ; charger uniquement un état du même SHA256. Aucun état instantané ne constitue une validation de sauvegarde de cartouche.

Échéance visée : **29 octobre 2026 à 22 h, Europe/Paris**. Le scénario complet reste non validé. Le dernier bilan expérimental demeure celui du commit `babd6e580c54cb2086cbb9ddb40f80ab2ac73e38`.


## Restauration effective et extension — 28 octobre 2026

Le blocage précédent est levé : la nouvelle pièce jointe française correspond exactement au SHA256 attendu. Le dépôt a été récupéré à fa6b86d et Snes9x recompilé au commit documenté avec l'instrumentation publiée. La reconstruction initiale a reproduit f1586e… ; le validateur et le round-trip BPS ont été relancés. Les états perdus ont été recréés depuis le reset : original au panneau à 109 397 images et prototype après le combat à 115 438, avec des captures PNG identiques aux empreintes historiques.

L'original a poursuivi dans un écran de chemin avec une colonne et un passage étroit, et terminé deux combats supplémentaires ; le second affichait « Voleur rigolo » et « Attaque furtive ! ». Il s'arrête à 116 527 images, toujours sans arrivée attestée à Cool. Le premier segment (109 397–113 265) fournit 6 947 transferts, 941 observations distinctes dont les empreintes ont toutes été vérifiées par décompression indépendante. Huit clés deviennent observées : sept étaient déduites, une était absente ($ED:E9F4, 64 octets). La branche suivante apporte 3 801 transferts supplémentaires sans autre clé nouvelle ni longueur insuffisante constatée ; son relevé est publié séparément.

Catalogue courant : **30 579 clés**, **2 282 observées**, 8 demandes du prototype avec source physique déduite, 28 289 autres déduites/comparées ; 2 743 150 octets de reconstruction. Aucun nouveau PC depuis les 72 déjà observés ; 110 hooks inchangés. Seul DMA0 reste exercé. Le fusionneur incrémental préserve les clés, sources, maxima de longueur et priorités de la base ; une seconde fusion reproduit exactement le catalogue. Aucune donnée ROM n'est publiée.

Nouvelle cible : `faa3735e12320fc700f85ce86abda2f638bb8aa583cf6c3315d3b4822807bd32`. Les 30 579 destinations passent le validateur, distance maximale 211, et le BPS est redécodé et contrôlé avec ses trois CRC. Le replay depuis le reset à 115 438 images passe **107 799 transferts redirigés**, **2 284 tuples source/longueur/empreinte**, aucun arrêt ni source DMA non résolue persistante, S-DD1 désactivé. La capture finale est identique au jalon historique. Deux PNG tronqués (58 200 et 66 600) ont été mis à l'écart et exclus des comparaisons. Un premier journal anormalement court de 20 036 transferts a été rejeté ; le replay suivant fournit le décompte ci-dessus. Aucun diagnostic causal définitif de cet incident de journalisation n'est revendiqué.

La continuation cible à 124 303 images passe séparément 2 513 transferts et 224 tuples sans erreur, mais finit près de la rivière, à une position différente de l'original. Ne pas additionner les tuples comme des ensembles disjoints. **La nouvelle portion de carte originale n'est pas encore validée sur la cible et Cool n'est pas atteint.** Les adresses déduites ne sont toujours pas une couverture complète. Sauvegarde/chargement de cartouche, DMA1 et matériel restent non validés. Les routes et points exacts figurent dans NEXT_RUN.md ; l'objectif du 29 octobre à 22 h Paris reste une cible non atteinte.


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


## Audit public du 29 octobre — sans ROM

Le dépôt a été restauré à 4fa021c. La ROM française reste absente ; aucun nouveau parcours, bloc exécuté, rebuild ou round-trip BPS n'a été effectué lors de cet audit. Le catalogue et le patch publiés ne sont pas modifiés.

`analysis/audit_public_evidence.py` contrôle les métadonnées conservées : 30 579 clés et positions de lookup uniques, aucun trou sur les chaînes de recherche, distance maximale 211. Chaque observation détaillée exportée retrouve la même source physique, une longueur suffisante et la priorité observée dans le catalogue. Aucune contradiction constatée. Ce contrôle ne décompresse aucun octet et ne revalide pas les empreintes sur la ROM.

Sur les 2 282 clés historiquement classées observées, **2 267 ont un relevé détaillé dans les fichiers publics**, et **15 ne conservent que leur provenance historique `observed fr_live`**. La liste figure dans public_evidence_audit.json ; ces quinze clés ne sont ni déclassées ni considérées comme nouvellement vérifiées. Les exports détaillés couvrent 68 des 72 PC de la liste observée. Les quatre PC sans relevé détaillé exporté sont C2:FE2D, CA:6899, CA:68CB et CA:E4F8. Les 72 PC de cette liste ne doivent pas être confondus avec les 110 remplacements implantés dans la ROM. Seul DMA0 apparaît dans ces exports. Les exports peuvent se recouper : ne pas additionner leurs compteurs comme des parcours indépendants.

Les deux continuations du panneau sont maintenant aussi disponibles avec leur préfixe complet depuis le reset : route_sign_front_from_reset.json (111 942 images) et route_sign_neighbor_from_reset.json (109 561). `compose_route.py` coupe proprement le préfixe à 109 397 et y joint les intervalles absolus de la continuation. L'égalité des masques de touches a été contrôlée pour chaque image avec les segments publiés ; les bornes et le refus des recouvrements/masques invalides ont été vérifiés. Une chaîne de lookup volontairement cassée a été rejetée par l'auditeur. **Ces contrôles de composition ne sont pas une nouvelle exécution en émulateur.**

Le blocage de scénario reste l'absence de la ROM exacte. Après son rétablissement : contrôler son SHA256, reconstruire/valider la cible, rejouer les routes depuis le reset et reprendre vers Cool. Réexporter les observations correspondant aux quinze clés et quatre PC historiques lorsqu'ils sont réexercés. Cool, Metox, Calnus et la couverture complète ne sont pas validés.


## Reprise du 29–30 octobre — Cool atteint, correction vérifiée

La ROM française remise à disposition correspond au SHA256 attendu. Le cœur a été recompilé depuis `snes9xgit/snes9x` au commit documenté, avec le patch instrumenté. La cible précédente faa3735e… a d'abord été reproduite et revérifiée.

La référence originale atteint Cool, lit le dialogue de l'homme infecté à l'entrée, couvre l'arrivée de Milly puis les dialogues chez Maltos et Milly. Dernier point original : **131 767 images**, scène extérieure avec Milly et Dorn encore en cours. Aucun retour achevé à Clatos n'est revendiqué. Le chemin utile depuis le premier panneau passe légèrement au sud avant de bifurquer à l'ouest ; à l'écran du pont suivant, continuer au nord sur la rive ouest. La rive est était une exploration distincte. Les routes sont des suites de touches effectivement exécutées, y compris les tâtonnements.

Le prototype précédent s'arrête au nord du pont sur **CF:8A5D, 24 576 octets**. Cette lecture est maintenant confirmée sur l'original et ajoutée avec huit autres clés. Le catalogue passe à **30 588 clés**, dont **2 343 observées** (+61 : neuf ajouts et 52 promotions de clés auparavant déduites). Les longueurs existantes n'ont pas dû être augmentées ; la reconstruction cumulée atteint **2 775 918 octets** (+32 768). Aucun conflit de source physique, aucun nouveau PC : 72 PC observés, 110 hooks et gestionnaires de 152 octets inchangés. Seul DMA0 a été exercé. Les 30 579 anciennes positions de lookup sont conservées ; distance maximale 211. La fusion incrémentale est idempotente.

Cible courante : `eda13e6d09f0783e6854d552a1a62e4a460ae7c32b00143d9dbb1aec2ccc0aa0`. Les 30 588 destinations passent `validate_catalog.py`. Le BPS est redécodé octet par octet et ses trois CRC sont vérifiés ; le gzip publié contient exactement ce patch. Le replay depuis le reset jusqu'à 121 900 images franchit l'ancien arrêt : **115 999 transferts**, **2 301 tuples clé/longueur/FNV32** contrôlés, aucun arrêt ni source non résolue persistante, S-DD1 désactivé.

Les continuations propres à la cible atteignent ensuite **129 651 images**, avec le titre **« Village Cool »** visible. Le combat supplémentaire est terminé, puis l'entrée est franchie. Sur les segments disjoints de ce parcours cible, le bilan agrégé et l'union exacte des tuples figurent dans `oct30_cool_scenario_coverage.json` ; ne pas sommer les ensembles de tuples des rapports individuels. Tous ces contrôles DMA passent. La route complète composée n'a pas été rejouée une seconde fois d'un seul tenant ; le préfixe depuis le reset et les continuations du même SHA256 sont distingués.

L'audit public distingue toujours quinze clés historiquement observées sans relevé détaillé conservé. Les nouveaux relevés exportés ne contiennent que des adresses, longueurs, empreintes, canaux, PC et compteurs. Les images, ROMs, données graphiques et états restent privés. Une capture originale tronquée à 28 800 a été exclue de la comparaison du préfixe ; les captures finales citées ont été inspectées.

`run_headless.py` écrit maintenant le frame de départ d'une continuation dans `run.json`. Ce défaut de métadonnées a été corrigé ; les anciens départs de cette reprise ont été renseignés depuis les commandes enregistrées. Un test réel de continuation 129 651 → 129 711 vérifie ce champ, sans revendiquer un nouveau jalon. `validate_original_trace.py` contrôle indépendamment les empreintes des traces originales ; les tests rejettent une empreinte modifiée et un SHA de provenance incorrect.

**Scénario complet toujours non validé.** La scène de Maltos/Milly reste à rejouer sur la cible, puis la référence doit terminer son dialogue extérieur et poursuivre vers Metox et le Calnus. Sauvegarde/chargement SRAM, DMA1 en jeu et matériel réel restent non validés. L'échéance visée du 29 octobre à 22 h Paris n'a pas été atteinte.


## 30 octobre — Maltos, Milly et retour à Clatos validés sur la cible

L'original a terminé la scène extérieure de Dorn et Milly à Cool, la transition vers la maison de Clatos et les dialogues suivants. Le titre « Ville de Clatos » a été vu à l'écran. Le menu montre maintenant Ratix et Milly, sans Dorn. La cible sans S-DD1 a rejoint la maison de Maltos après adaptation des déplacements, puis rejoué les mêmes dialogues, les scènes extérieures et le retour à Clatos. Son menu confirme également Ratix–Milly. Metox et le Calnus restent à couvrir.

Neuf clés déjà présentes passent de déduites à observées, après vérification indépendante de la trace originale retenue. Aucun ajout de clé ni extension de longueur, aucun conflit physique et aucun nouveau PC. Le catalogue contient **30 588 clés, dont 2 352 observées**, huit demandes du prototype avec provenance physique déduite et 28 228 autres déduites/comparées. La fusion est idempotente. Les 72 PC observés, 110 hooks et gestionnaires DMA0/1 de 152 octets ne changent pas ; seul DMA0 reste exercé.

La reconstruction, le validateur des 30 588 destinations et le round-trip BPS avec trois CRC ont été exécutés. La ROM cible est **strictement identique** à eda13e6d… : seuls les statuts de preuve changent. Le manifeste de lookup et le patch BPS publié sont eux aussi inchangés.

Le segment original 131 767 → **141 936** a été rejoué : **7 528 transferts**, 461 observations détaillées exportées et vérifiées indépendamment. Le nouveau replay cible de la scène, 137 892 → **157 001**, contrôle **14 445 transferts** et **533 tuples clé/longueur/FNV32**, sans erreur de décompression, boucle d'arrêt, source non résolue persistante ou S-DD1 résiduel. Les captures finales de menu sont identiques entre les deux passages originaux et entre les deux passages cibles respectifs ; les statistiques des personnages peuvent différer entre ROMs après leurs combats distincts.

Les volumes de journal ne sont pas identiques entre passages : 5 360 lignes dans l'exploration originale interactive initiale, puis 7 528 dans le replay original retenu ; 13 462 puis 14 445 pour deux replays cibles de la scène. La cause de cet écart n'est pas établie. Les journaux ne sont pas additionnés et aucune équivalence déterministe de tous les transferts ou de toutes les images n'est revendiquée. Le relevé original publié est celui du replay retenu, dont chaque empreinte est vérifiée. Les contrôles des deux passages cibles restent distincts dans les rapports.

Points de reprise : `fr_oct30_original_party/end.state` à 141 936 et `fr_oct30_target_dialogues_recheck/end.state` à 157 001, chacun avec son SHA propre. Les deux sont des états d'émulateur, menus ouverts, pas des sauvegardes de cartouche. Les nouvelles routes complètes sont composées de segments exécutés ; leurs nouvelles continuations ont été rejouées, pas l'ensemble final depuis le reset en une seule exécution. Fermer le menu, attendre la fin du fondu puis préparer le trajet vers Metox. Le jeu entier, la SRAM, DMA1 en jeu et le matériel réel restent non validés.


## 30 octobre — départ de Clatos et nouveau combat corrigé

Les deux ROMs ont quitté la maison puis franchi la sortie nord de Clatos. Le passage emprunte les escaliers vers la rue basse et le pont inférieur : tenter de traverser directement depuis le perron surélevé bloquait contre le décor. La scène de départ montre Dorn et Milly ; Dorn évoque les vers de montagne. Le combat suivant affiche Ratix, Milly et Dorn. La cible finale revient sur le chemin après un combat contre Petit lap. **Metox et le Calnus ne sont toujours pas atteints.**

L'ancienne cible eda13e6d… s'arrêtait réellement à `$64:8096` sur `$FA:E65D`, 64 octets. La table source à 0xB1CA9 contient FA:E64F + 14. La relecture originale a ensuite confirmé directement FA:E65D et son empreinte 2ccd05d0, et relevé une seconde clé FA:7F39. Ces deux clés sont donc observées sur l'original ; la demande provisoire déduite est supplantée dans le catalogue par cette preuve. 134 clés existantes sont promues, sans extension de longueur ni conflit physique.

Catalogue : **30 590 clés, 2 488 observées**, huit demandes du prototype conservant une source physique déduite, 28 094 autres clés déduites/comparées ; reconstruction cumulée 2 776 046 octets. **73 PC observés**, dont le nouveau `$C0:2F15`, couvert par les 110 hooks existants. Gestionnaires de 152 octets inchangés, DMA0 seulement exercé. Les anciennes positions de lookup sont préservées ; distance maximale 211. Fusion idempotente, audit public cohérent ; quinze anciennes clés observées restent sans relevé détaillé public.

Nouvelle cible : **9a2126ffa611115849ea8b32cf1a5ed43806aa2c83398a5bd5b88c4f004e8963**. Les 30 590 destinations passent le validateur indépendant ; le nouveau BPS est redécodé octet par octet avec ses trois CRC. **Replay complet depuis le reset jusqu'à 168 591 images : 164 257 transferts redirigés, 2 540 tuples clé/longueur/FNV32 vérifiés**, aucun arrêt, aucune source non résolue persistante ni transfert S-DD1 résiduel ; 281 échantillons S-DD1 faux. Les 2 540 tuples sont distincts par clé/longueur/empreinte ; 2 443 paires longueur/empreinte seules.

Référence originale retenue : continuation 141 936 → 154 943, 13 074 transferts et 1 073 relevés détaillés (1 025 vérifications source/longueur/empreinte), tous vérifiés indépendamment. L'exploration interactive initiale avait 4 181 transferts et une autre position finale ; cet écart reste inexpliqué, les deux compteurs ne sont pas additionnés. La référence est un segment, la cible un parcours depuis le reset : leurs images à la même frame absolue ne sont pas alignées. Aucune équivalence universelle n'est revendiquée. L'essai intermédiaire 0b939cef… a été interrompu ; il ne compte pas comme cible validée.

Reprise originale : `analysis/runs/fr_oct30_departure_reference_recheck/end.state`, 154 943, sur le chemin au nord du premier panneau, près de la végétation à droite. Reprise cible : `analysis/runs/fr_oct30_departure_final/end.state`, 168 591, chemin juste au sud du panneau après le combat. Employer uniquement le SHA de chaque ROM. Routes : `route_oct30_departure_original.json` et `route_oct30_departure_target.json` ; la route cible entière a cette fois été réellement rejouée d'un seul tenant. Bilans : `oct30_departure_*`. Prochaine action : résoudre le trajet vers Metox depuis le panneau sur chaque ROM, avec captures et nouveaux relevés. Les états sont des instantanés d'émulateur ; SRAM, DMA1, matériel et scénario complet restent non validés. L'échéance visée n'est pas atteinte.
