# transmob
Suivi vidéo de véhicule basé sur [YOLOv11](https://github.com/ultralytics/ultralytics) \
Langues : [![fr](https://img.shields.io/badge/lang-fr-blue.svg)](https://github.com/AlixMenard/transmob/blob/main/README.fr.md)
[![en](https://img.shields.io/badge/lang-en-red.svg)](https://github.com/AlixMenard/transmob/blob/main/README.md)

## Installation
### Prérequis
- [Python >= 3.12](https://www.python.org/downloads/)
- [git](https://git-scm.com/downloads/win)
### Optionnel
Si l'ordinateur a une [carte graphique compatible avec CUDA](https://en.wikipedia.org/wiki/CUDA#GPUs_supported), il faut télécharger et installer [NVIDIA CUDA toolkit](https://developer.nvidia.com/cuda-downloads).\
Durant la prochaine étape, après avoir installé les librairies requises, il faut désinstaller les librairies pytorch par défaut (`pip uninstall torch torchvision torchaudio`) et les ré-installer avec le support de CUDA sur le [site de PyTorch](https://pytorch.org/get-started/locally/). Sélectionnez la version *Stable*, votre système d'exploitation, *pip*, *python* et une *version de CUDA* ([voir compatibilité version/carte graphique ici](https://en.wikipedia.org/wiki/CUDA#GPUs_supported)), puis copier et exécuter la commande donnée par le site.\
Avoir une carte graphique compatible avec CUDA est hautement recommandé pour de meilleurs performances.

### Installer
- Ouvrir un powershell/commandline shell : win+r, taper "powershell" ou "cmd", puis `Entrée`
- Naviguer jusqu'à l'emplacement ou vous souhaiter installer le programme (Utilisez `cd <nom_dossier>` pour naviguer)
- Exécutez `git clone https://github.com/AlixMenard/transmob`
- Allez dans le dépôt : `cd transmob`
- Installez les librairies nécessaires : `pip install -r requirements.txt`\
\* Ces étapes vont aussi installer les models YOLOv8 de tailles *n*, *s*, *m* et *l*. La première fois que vous demanderez au programme d'utiliser le modèle de taille *x*, il le téléchargera automatiquement avant de commencer.

### Méthode lancement 1
- Ouvrez un powershell/commandline shell : win+r, tapez "powershell" ou "cmd", puis `Entrée`
- Naviguez jusqu'au dépôt (à *<chemin_précédent>/transmob*)
- Exécutez `py GUI.py`
### Méthode lancement 2
- Allez dans le dossier *transmob*
- Lancez "start.vbs". Arès le premier lancement, un raccourci sera disponible sur le Bureau pour y accéder plus facilement".
- Le programme va se lancer puis se mettre à jour. Pas de panique si le lancement est un peu long.
### Usage
- Glissez et déposez le dossier contenant les vidéos à analyser (**chaque** fichier sera analysé, pensez à supprimer les duplicata, comme ceux avec différentes extensions, comme "fichier.mp4" et "fichier.lrv")
- Choissisez les options que vous voulez :
  - Process (explained below)
  - Frame number : 1, chaque image se analysée, 2,une image sur deux sera analysée (deux fois plus rapide, réduis le taux de détetion, très fortement déconseillé pour les vidéos avec une qualité d'image basse)
  - YOLO model : les modèles plus gros sont plus précis, mais considérablement plus lent dans le plupart des cas. Avec le support CUDA, le ralentissement lié à la taille du modèle est négligeable et toujours utiliser le modèle de taille *x* est fortement conseillé. 
  - Classes : Types de véhicules à compter, Les autre seront ignorés. Si les piétons (*person*) sont comptés, les vélos et motocylettes (*bicycle* and *motorbike*) ne peuvent pas être ignorés.
  - Number of cores : Nombre de cœurs dédiés au programme. Si l'ordinateur possède 10 cœurs physiques ou plus, les recommendations sont *Classic (4)*, *Nested Threads (3)* and *YallO (4)*.
  - With video : Si oui, la vidéo sera affichée durant son traitement. Cela ralentit considérablement le processus. C'est en revanche très utile pour juger de l'efficacité de détection d'un modèle sur une vidéo dont vous n'êtes pas certain.e de la qualité.
- Start
- La première image de chaque vidéo sera montrée, successivement, pour créer les lignes de comptage. Il faut 3 clics pour créer une ligne : les 2 premiers clics définissent les points de début et de fin de la ligne, le 3e clic défini la direction de comptage. A une intersection, Il est recommendé d'effectuer le 3e clic au milieu de l'intersection. **/!\\** *les 2 premiers clics définissant la ligne à travers laquelle les véhicules seront comptés, ils doivent être précis pour ne pas rater de véhicule ou en compter trop. Cependant, la précision du 3e clic n'a aucune importance. Si plusieurs lignes sont placées, l'ordre doit rester le même sur toutes les vidéos.*
- Avec la première image, une fenêtre pop-up sera affichée pour vérifier la date de départ de la vidéo. Le programme montrera la date de création de la vidéo en première proposition, Que vous pouvez confirmer avec "Valider". Si cette date n'est pas correcte, vous pouvez taper la date réelle, au format (aaaa-MM-jj hh:mm), puis cliquer sur "Changer".
- Après avoir défini toutes les lignes sur l'image, pressez `Entrée` pour valider, et répéter pour chaque vidéo.
- Quand plus aucune vidéo n'est montrée, le paramétrage est terminé et le programme va analyser toutes les vidéos. Ne pas ouvrir le fichier `results.txt`durant le processus, cela pourrait empêcher le prgoramme d'écrire le résultat et le bloquer. \
*Note : Si les commandes python comme `py GUI.py` ne marchent pas, remplacez `py` par `python` (e.g. `python GUI.py`)*

### Bon usage
- Les noms des fichiers et des dossiers ne doivent pas contenir d'espace ou de caractères spéciaux
- Pour des intersections complexes, comme des carrefours giratoires, placez les lignes de manières à ce qu'un véhicule engagé circulant proche de la ligne ne puisse pas la traverser sans quitter l'intersection
- Pensez à bien couvrir l'ensemble de la zone de passage, en particulier pour les passages piétons, pour lesquels les piétons peuvent traverser autour plutôt que sur le passage exactement
- Les fichiers MP4 et LRV donnent les même résultats, car YOLO réduit la qualité de l'image avant de l'analyser.Cependant, les fichiers LRV sont bien plus légers sur le processeur et la mémoire de l'ordinateur.

## transmob

Detection d'objet par YOLO, suivi par SORT.\
Analyse en parallèle des vidéos.

## transmobNT

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
L'usage de CUDA empêche la parallèlisation des vidéos qui sont de facto analysées successivement.

### Performances
**Précision :** transmob == transmobNT < transmobYT == transmobYTC \
**Rapidité :** transmobYTC >> transmobYT > transmobNT >= transmob \
YTC n'est que peu affecté en temps par la taille du modèle utilisé, les autres processus sont affectés par un ratio q\~=1.3  \
Les vidéos peuvent être analysées par 2 images à la fois. Sur de la qualité basse, à éviter.

**Modèles :** 
Du plus léger au plus lourd : *n*, *s*, *m*, *l*, *x*. \
*m* et supérieurs offrent une detection parfaite en simple frame sur les versions YT et YTC, tandis que *n* est à ~95% et *s* est estimé au dessus de 97%. \
En double frame, les modèles se situent entre 80% et 95% (estimation max), avec la meilleur performance pour *l*.

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
- [ ] Annuler la création d'une ligne en cas d'erreur
- [ ] Analyse directionnelle

### Mentions légales
YOLO étant sous [license AGPL-3.0](https://firebasestorage.googleapis.com/v0/b/ultralytics-public-site.appspot.com/o/license%2FAGPL-3.0-Software-License.pdf?alt=media), ce code l'est aussi. En termes simples, il peut être utilisé avec un objectif commercial au sein de l'entreprise, mais ne peut pas être utilisé comme service en ligne/hébergé accessible à des utilisateurs publiques ou privés. Dans un tel cas, l'entièreté du code source doit être rendu disponible aux utilisateurs, à moins d'acheter une license entreprise à Ultralytics.

Ce projet a utilisé [les donnéesde COCO](https://cocodataset.org/#home) ainsi que de [Maryam Mahmood](https://universe.roboflow.com/maryam-mahmood-6hoeq/vans/dataset/3) pour entrainer plus en profondeur le modèle YOLO.
