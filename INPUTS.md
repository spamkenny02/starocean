# Entrées privées et reproduction

ROM française attendue : `upload/Star Ocean FR.smc`, 6 291 456 octets, SHA256 `a31a931a7fb66f2d3486af8d3bda261ea9aa2e40e47a6120cd87f368d332c3dd`.

Pour reconstruire le prototype d’ouverture :

```sh
g++ -shared -fPIC -O2 -fwrapv analysis/sdd1_standalone.cpp -o analysis/sdd1.so
python analysis/build_routine_prototype.py
python analysis/make_bps_prototype.py
```

Le patch compressé dans `patches/` se décompresse avec gzip. Il est strictement expérimental et ne couvre que le parcours d’ouverture. Il ne faut pas le présenter comme un patch pour le jeu entier.

Les scripts exploratoires des étapes antérieures demandent aussi la ROM anglaise et le patch anglais fournis séparément, ainsi que les catalogues qu’ils génèrent. Aucun de ces fichiers privés n’est inclus.

Le cœur de test est Snes9x au commit `1bcc369e89f08243e0a462882fb1f3e42e51de3a`. Le patch d’instrumentation et le pilote headless sont inclus. Le pilote demande numpy et Pillow.

Le code du décompresseur conserve sa licence Snes9x. Aucune licence globale nouvelle n’est attribuée aux contenus tiers.
