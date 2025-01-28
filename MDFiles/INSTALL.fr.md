## Installation
### Prérequis
- [Python = 3.12](https://www.python.org/downloads/release/python-3127/)
- [git](https://git-scm.com/downloads/win)

### Installation facile (bêta, windows uniquement)
Téléchargez et exécutez le fichier [TransMobSetup](../TransMobIASetup.exe).\
Ceci installera les fichiers du programme sur votre ordinateur, dans `Documents` par défaut, mais vous pouvez choisir un autre emplacement.

### Installation Manuelle
- Ouvrir un powershell/commandline shell : win+r, taper "powershell" ou "cmd", puis `Entrée`
- Naviguer jusqu'à l'emplacement dans lequel vous souhaitez installer le programme (Utilisez `cd <nom_dossier>` pour naviguer)
- Dans le shell, exécutez : `git clone https://github.com/AlixMenard/transmob`
- Allez dans le dépôt : `cd transmob`
- Installez les librairies nécessaires : `pip install -r requirements.txt`
- Dans le shell, exécutez : `pip install fastreid==1.4.0 --no-deps`
- FastReID n'est plus à jour, des modifications sont nécessaires. Trouvez le dossier d'installation (généralement `C:\Users\<user>\AppData\Local\Programs\Python\PythonX\Lib\site-packages`) et remplacez le dossier **fastreid** par [celui-ci](https://github.com/AlixMenard/fastreid) (décompressez-le avant). il faut aussi télécharger le [modèle FastReId](README.fr.md#FastReId) et le placer dans le dossier FastReId_config.

\* Ces étapes vont aussi installer les models YOLO de tailles *n*, *s*, *m* et *l*. La première fois que vous demanderez au programme d'utiliser le modèle de taille *x*, il le téléchargera automatiquement avant de commencer.  \
Utiliser le modèle *x* avec une carte graphique nécessite de télécharger le modèle OnlyVans correspondant. Celui-ci devrait être téléchargé automatiquement par l'installer et visible dans `weights/vansx.pt`. S'il n'a pas été correctement téléchargé, le modèle devrait être disponible [ici](amenard.perso.ec-m.fr/Transmob/vansx.pt) (serveur étudiant de l'école de l'auteur, Alix Ménard) ou sur le serveur de l'entreprise `BASE DE DONNEES\Programmes\IA comptage\transmob\weights\vansx.pt`.

### Optionnel
Si l'ordinateur a une [carte graphique compatible avec CUDA](https://en.wikipedia.org/wiki/CUDA#GPUs_supported), il faut télécharger et installer [NVIDIA CUDA toolkit](https://developer.nvidia.com/cuda-downloads).\
Durant la prochaine étape, après avoir installé les librairies requises, il faut désinstaller les librairies pytorch par défaut (`pip uninstall torch torchvision torchaudio`) et les réinstaller avec le support de CUDA sur le [site de PyTorch](https://pytorch.org/get-started/locally/). Sélectionnez la version *Stable*, votre système d'exploitation, *pip*, *python* et une *version de CUDA* ([voir compatibilité version/carte graphique ici](https://en.wikipedia.org/wiki/CUDA#GPUs_supported)), puis copier et exécuter la commande donnée par le site.\
Avoir une carte graphique compatible avec CUDA est hautement recommandé pour de meilleures performances.
