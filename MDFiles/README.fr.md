# transmob
Suivi vidéo de véhicule basé sur [YOLOv11](https://github.com/ultralytics/ultralytics) \
Langues :[![en](https://img.shields.io/badge/lang-en-red.svg)](../README.md)
[![fr](https://img.shields.io/badge/lang-fr-blue.svg)](README.fr.md)

## Installation
Suivez les instructions de [Install](MDFiles/INSTALL.fr.md).

### Méthode lancement 1
- Allez dans le dossier *transmob*
- Lancez "start.vbs". Arès le premier lancement, un raccourci sera disponible sur le Bureau pour y accéder plus facilement.
- Le programme va se lancer puis se mettre à jour. Pas de panique si le lancement est un peu long.
- Une fenêtre vous donnera 2 options : le programme d'analyse vidéo, ou des [Outils additionnels](#Tools)
### Méthode lancement 2
- Ouvrez un powershell/commandline shell : win+r, tapez "powershell" ou "cmd", puis `Entrée`
- Naviguez jusqu'au dépôt (à *<chemin_précédent>/transmob*)
- Exécutez `py GUI.py`
### Usage
- Glissez et déposez le dossier contenant les vidéos à analyser (**chaque** fichier sera analysé, pensez à supprimer les duplicata, comme ceux avec différentes extensions, comme "fichier.mp4" et "fichier.lrv")
- Choissisez les options que vous voulez :
  - `Nombre de frames` :
    - 1 : chaque image sera analysée
    - 2 : une image sur deux sera analysée (deux fois plus rapide, réduis le taux de détetion, très fortement déconseillé pour les vidéos avec une qualité d'image basse)
  - `Model YOLO` : les modèles plus gros sont plus précis, mais considérablement plus lent dans le plupart des cas. Avec le support CUDA, le ralentissement lié à la taille du modèle est négligeable et toujours utiliser le modèle de taille *x* est fortement conseillé. 
  - `Types de véhicules` : Types de véhicules à compter, Les autre seront ignorés. Si les piétons (*person*) sont comptés, les vélos et motocylettes (*bicycle* and *motorbike*) ne peuvent pas être ignorés.
  - `Avec vidéo` : Si oui, la vidéo sera affichée durant son traitement. Cela ralentit considérablement le processus. C'est en revanche très utile pour juger de l'efficacité de détection d'un modèle sur une vidéo dont vous n'êtes pas certain.e de la qualité.
  - `Avec captures d'écran` : Enregistrera une capture de chaque véhicule compter, pour validation ou anlyse supplémentaire.
  - `Un seul setup` : Si oui, seule la première vidéo du dossier sera montrée pour tracer les lignes de comptage. Toutes les autres vidéos auront les même lignes.
  - `Valider les lignes` (Si `Un seul setup` est séléctionné) : Transferera les lignes à chaque vidéo du dossier, mais les affichera pour validation et permettre des modifications.
- Start
- Pour chaque vidéo :
  - Une fenêtre pop-up sera affichée pour vérifier la date de départ de la vidéo. Le nom de la fenêtre correspond au nom de la vidéo. La fenêtre affiche l'heure estimée de création de la vidéo en se basant sur la date de création du fichier. Si elle est correcte, cliquez sur "Valider", et le programme considerera alors les heures de départ estimée pour les autres vidéos du dossier elles aussi correctes. Sinon, entrez la date de départ de la vidéo **en entier**, le format spécifié doit être respecté.
  - La première image de chaque vidéo sera montrée, successivement, pour créer les lignes de comptage. Il faut 3 clics pour créer une ligne : les 2 premiers clics définissent les points de début et de fin de la ligne, le 3e clic défini la direction de comptage. A une intersection, Il est recommendé d'effectuer le 3e clic au milieu de l'intersection. \
**/!\\** *les 2 premiers clics définissant la ligne à travers laquelle les véhicules seront comptés, ils doivent être précis pour ne pas rater de véhicule ou en compter trop. Cependant, la précision du 3e clic n'a aucune importance. Si plusieurs lignes sont placées, l'ordre doit rester le même sur toutes les vidéos.*
  - Après avoir défini toutes les lignes sur l'image, pressez `Entrée` pour valider, et répéter pour chaque vidéo.
- Quand plus aucune vidéo n'est montrée, le paramétrage est terminé et le programme va analyser toutes les vidéos. Ne pas ouvrir le fichier `results.txt`durant le processus, cela pourrait empêcher le prgoramme d'écrire le résultat et le bloquer. \
*Note : Si les commandes python comme `py GUI.py` ne marchent pas, remplacez `py` par `python` (e.g. `python GUI.py`)*

### Bon usage
- Les noms des fichiers et des dossiers ne doivent pas contenir d'espace ou de caractères spéciaux
- Pour des intersections complexes, comme des carrefours giratoires, placez les lignes de manières à ce qu'un véhicule engagé circulant proche de la ligne ne puisse pas la traverser sans quitter l'intersection
- Pensez à bien couvrir l'ensemble de la zone de passage, en particulier pour les passages piétons, pour lesquels les piétons peuvent traverser autour plutôt que sur le passage exactement
- ~Les fichiers MP4 et LRV donnent les même résultats, car YOLO réduit la qualité de l'image avant de l'analyser.Cependant, les fichiers LRV sont bien plus légers sur le processeur et la mémoire de l'ordinateur.~ Les fichiers MP4 ont une meilleure robustesse face à la compressionque les fichiers LRV face à la décompresseion, et obtiennent de meilleurs résultats avec SAHI.

<a name="Tools"></a>
### Outils additionnels
Des outils additionnels utiles sont disponibles. Pour y accèder, ouvrez une invite de commande et naviguez jusqu'au dossier du projet (voir la [partie Installation](#Install) pour plus d'indications sur la navigation via invite de commande). Exécutez `py Tools.py` (ou `python Tools.py`) pour ouvrir une fenêtre incluant les différents outils.
Les outils permettent :
- Formattage des résultats
- Renommer vidéos
- Séparer vidéos
- Aggréger résultats
- Réparer vidéos

Plus de détails sont disponibles [ici](MDFiles/Tools.fr.md).

## ~~transmob~~

Detection d'objet par YOLO, suivi par SORT.\
Analyse en parallèle des vidéos.

## ~~transmobNT~~

Detection d'objet par YOLO, suivi par SORT.\
Analyse en parallèle des vidéos.\
Parallélisation interne des vidéos (detection // suivi) \
**/!\\** *La version avec vidéo ne doit pas être interrompue avant que la vidéo ait été complètement analysée. Sinon, un redémarrage sera nécessaire.*

## transmobYT

Detection d'objet par YOLO, suivi par YOLO via BoT-SORT.\
Analyse en parallèle des vidéos.\

## transmobYTC

Detection d'objet par YOLO, suivi par YOLO via BoT-SORT.\
YOLO et autres processus tournant sur CUDA.\
L'usage de CUDA empêche la parallèlisation des vidéos qui sont de facto analysées successivement.\
les performances de CUDA de discriminer *trucks* (*camions*) en *trucks and vans* (*camions et camionettes*).

## Notes
- Classic et NT sont discontinués pour des raisons d'efficacité
- Les performances doivent être améliorées avec SAHI -> Implémentation de BoTSORT et ReId indépendemment de YOLO

### Performances
**Précision :** transmob == transmobNT < transmobYT == transmobYTC 

**Distinction camionette vs voiture/camion :** 
- Modèle unique, entrainé sur COCO et un ensemble de données supplémentaire,mauvaises performannces (84% des camionettes sont toujours catégorisées en voiture/camion). COCO contient peut être déjà des camionnettes listées comme voiture ou camion, et/ou les données additionnelles sont insuffisantes face à COCO. 
- Modèle additionnel, entrainé spécifiquement sur les données de camionnettes, les reconnait avec une haute confiance, ce qui permet une comparaison de confiance entre la détection orginale et celle faite par le modèle secondaire. Sur les tests de validation, en comparant les *confiances* du modèle COCO et celles du modèle secondaire sur des images de voiture et camions (de COCO) et de camionnettes (des données supplémentaires), un taux de discrimination réussie de 90% est atteint en plaçant un seuil du *ratio de confiances* (COCO/secondaire) à approximativement `1.08211`. (Au dessus du seuil, le modèle entrainé sur COCO prime, en dèça le véhicule est considéré comme une camionette)

**Rapidité :** transmobYTC >> transmobYT > transmobNT >= transmob \
YTC n'est que peu affecté en temps par la taille du modèle utilisé, les autres processus sont affectés par un ratio q\~=1.3  \
Les vidéos peuvent être analysées par 2 images à la fois. Sur de la qualité basse, à éviter.

**Modèles :** 
Du plus léger au plus lourd : *n*, *s*, *m*, *l*, *x*. \
*m* et supérieurs offrent une detection parfaite en simple frame sur les versions YT et YTC, tandis que *n* est à ~95% et *s* est estimé au dessus de 97%. \
En double frame, les modèles se situent entre 80% et 95% (estimation max), avec (surprenamment) la meilleur performance pour *l*.

### A faire
- [x] Organisation des fichiers pour un ordre de traitemetn optimisé 
- [X] Support CUDA
- [X] Banc de test (modèle *x* déterminé par inférence)
- [x] Traiter person + bicycle -> bicycle uniquement (idem avec motorbikes)
  - [x] └> Faire tourner sur CUDA avec Numba
    - [X] └> banc de test pour l'efficacité de numba
- [x] ~Essayer parallélisation interne des vidéos sur YTC~ *La parallélisation n'est pas compatible avec CUDA*
- [X] Capture d'écran des véhicules comptés pour chaque processus
- [X] Paramétrage rapide en cas de vidéos avec le même PDV
- [X] Groupement de vidéos efficace en termes de mémoire
- [X] Distinguer SUV (voitures larges), camionnettes aet camions
- [ ] Implémenter ReId pour éviter les pertes de suivi
- [ ] Etude directionnelle
      
### Mentions légales
YOLO étant sous [license AGPL-3.0](https://firebasestorage.googleapis.com/v0/b/ultralytics-public-site.appspot.com/o/license%2FAGPL-3.0-Software-License.pdf?alt=media), ce code l'est aussi. En termes simples, il peut être utilisé avec un objectif commercial au sein de l'entreprise, mais ne peut pas être utilisé comme service en ligne/hébergé accessible à des utilisateurs publiques ou privés. Dans un tel cas, l'entièreté du code source doit être rendu disponible aux utilisateurs, à moins d'acheter une license entreprise à Ultralytics.

Ce projet a utilisé [les donnéesde COCO](https://cocodataset.org/#home) ainsi que de [Maryam Mahmood](https://universe.roboflow.com/maryam-mahmood-6hoeq/vans/dataset/3) pour entrainer plus en profondeur le modèle YOLO.

La détection d'objet utilise la [méthode SAHI](https://pypi.org/project/sahi/) et leur suivi repose sur [BoT-SORT](https://github.com/NirAharon/BoT-SORT) implementé via [BoxMOT](https://github.com/mikel-brostrom/boxmot). 
<a name="FastReId"></a>
Le suivi de véhicule est amélioré avec [FastReId](https://github.com/JDAI-CV/fast-reid) (Modèle disponible [ici](https://github.com/JDAI-CV/fast-reid/releases/download/v0.1.1/veriwild_bot_R50-ibn.pth), entrainé sur [VeRi-Wild](https://github.com/PKU-IMRE/VERI-Wild)) (Bien que non-renseigné sur [PWC](https://paperswithcode.com/), FastReId surpasse la plupart des méthodes listées sur la plupart des sets de données.)
