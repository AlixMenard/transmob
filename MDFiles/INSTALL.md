## Installation
### Pre-requisite
- [Python = 3.12](https://www.python.org/downloads/release/python-3127/)
- [git](https://git-scm.com/downloads/win)

### Easy Installation (beta, windows only)
Download and execute the [TransMobSetup](../TransMobIASetup.exe) file.\
This will install the program files on your computer, in `Documents` by default, but you can choose another location.

### Manual Installation
- Open a powershell/commandline shell : win+r, type "powershell" or "cmd", enter
- Navigate to the desired place to store the algorithm (use `cd <folder_name>` to navigate)
- In the shell, execute : `git clone https://github.com/AlixMenard/transmob`
- Go in the repository : `cd transmob`
- Install the necessary packages : `pip install -r requirements.txt`
- In the shell, execute : `pip install fastreid==1.4.0 --no-deps`
- As FastReId is not updated, some modifications are necessary. Find the installation folder (usually `C:\Users\<user>\AppData\Local\Programs\Python\PythonX\Lib\site-packages`) and replace the **fastreid** folder with [this one](https://github.com/AlixMenard/fastreid) (unzip it beforehand). It is also necessary to download the [FastReId model](../README.md#FastReId) and place it in the FastReId_config folder. 

\* This will install the yolo models of sizes *n*, *s*, *m* and *l*. On the first time you ask the program to use the model of size *x*, it will be automatically downloaded before processing. \
Running the *x* model with a GPU requires to download the corresponding OnlyVans model. It should be automatically downloaded by the installer and visible as `weights/vansx.pt`. If it was not correctly downloaded, it should be available [here](amenard.perso.ec-m.fr/Transmob/vansx.pt) (author Alix Menard's student school server) or on the company's server under `BASE DE DONNEES\Programmes\IA comptage\transmob\weights\vansx.pt`.

### Optionnal
If the computer has a [CUDA compatible graphic card](https://en.wikipedia.org/wiki/CUDA#GPUs_supported), you need to download and install [NVIDIA CUDA toolkit](https://developer.nvidia.com/cuda-downloads).\
During the next step, after installing the required modules, you need to uninstall pytorch modules (`pip uninstall torch torchvision torchaudio`) and re-install it with CUDA support on the [Pytorch Website](https://pytorch.org/get-started/locally/). Select the *Stable* version, the correct OS, *pip*, *python* and a *CUDA SDK version* ([see here for graphic card/version compatibility](https://en.wikipedia.org/wiki/CUDA#GPUs_supported)), then copy and execute the command given by the website.\
A CUDA compatible graphic card is highly recommended for increased speed performances.

