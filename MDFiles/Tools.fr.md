### Outils additionnels
#### Formattage des résultats
Il vous suffit de glisser-déposer le fichier `results.txt` créer par le programme, et cliquer sur "Valider". Un fichier csv sera créer au même emplacement.
#### Renommer vidéos
Glissez-déposez le dossier contenant les vidéos à renommer. Entrez le nom/numéro de la caméra (e.g. `GP07`) et son emplacement (ville, rue...), puis cliquez sur "Valider". Chaque vidéo sera renommée au format `camera_emplacement_AAAAMMJJ_HHhMM.ext`, avec *ext* l'extension conservée du fichier vidéo, et `AAAAMMJJ_HHhMM` la date de création formattée de la vidéo.\
**/!\\** *Ne pas utiliser de caractères spéciaux dans le nom des fichiers.*
#### Séparer vidéos
Dans les cas où un grand nombre de vidéos doivent être analysées (>10), il est nécessaire de les séparer en sous-dossiers. Il est aussi recommandé de le faire pour plus de 5 vidéos, car cela permet au programme de mieux gérer la mémoire, mais ce n'est pas obligatoire. Le dossier parent pourra toujours être donné en entier au programme, qui se chargera de traiter chaque sous-dossier.\
Glissez-déposez le dossier contenant les vidéos, puis renseignez le nombre de vidéos par sous-dossier, enfin cliquez sur "Valider".
#### Aggréger résultats
Si les vidéos étaient séparées en sous dossiers, vous aurez peut être besoin de récupérer les résultats de l'ensemble des vidéos en une seule fois. Il suffit de glisser-déposer le dossier parent et cliquer sur "Valider". L'outil ira chercher récursivement les fichiers `results.txt` dans les sous-dossiers, et les combinera en en fichier unique dans le dossier parent. 
#### Réparer vidéos
Si les vidéos sont endommagées (e.g. VLC Media Player un message d'erreur similaire à "Index endommagé ou absent") le programme ne sera pas capable de les lire correctement, il est donc nécessaire de réparer les vidéos en amont. Glissez et déposez le dossier sur la fenêtre puis cliquez sur "Valider". L'outil va récursivement regarder les vidéos dans le dossier et les sous-dossiers pour les réparer à l'aide de [FFmpeg](#ffmpeg). Les fichiers vidéo `file.ext` avec *file* le nom de la vidéo et *ext* l'extension du format vidéo seront **remplacés** par `file.r.mkv`. Si cette réparation ne marche pas, bonne chance.\
**/!\\** La réparation peut changer la durée de la vidéo, créant un décalage temporel : assurez-vous que le temps de la vidéo reste aligné au temps réel, ou corrigez quand on vous le demande avant analyse vidéo.
#### Changer date de vidéos
Si des vidéos sont mal datées (la date de *dernière modification* doit correspondre au moment où la vidéo s'est terminée, cad le moment où elle a commencé + sa durée), cet outil va re-dater toutes les vidéos d'un dossier (pas les sous-dossiers) avec une date de départ. Glissez-déposez le dossier sur la fenêtre, entrez la date de **départ** de la première vidéo au format indiqué, puis cliquez sur "Valider".

#### Formattage directionnel
Pour obtenir un fichier de résultats directionnels pour le dossier, il suffit de glisser-déposer le dossier dans la fenêtre et de cliquer sur « Valider ». Le programme recherchera les dossiers de captures d'écrans pour effectuer la correspondance entrée/sortie. Si certains véhicules n'ont pas pu être suivis sur l'ensemble de l'intersection, le programme entrera dans une phase de correspondance manuelle.

Un véhicule entrant vous sera présenté, ainsi que 12 correspondances potentielles parmi les véhicules sortants. Les correspondances potentielles sont sélectionnées sur la base de la ressemblance visuelle et de l'heure de traversée. Vous pouvez soit sélectionner le véhicule correspondant s'il est trouvé, soit l'ignorer si vous ne pouvez pas déterminer avec certitude une correspondance. Au fur et à mesure, le programme commencera à déterminer s'il est suffisamment sûr de lui pour accepter ou rejeter automatiquement certaines correspondances, afin de vous faciliter la tâche.

<a name="ffmpeg"></a>
### FFMPEG
Est un project gratuit et open-source avec pour objectif de gérer les fichiers vidéo, audio, et autres multimédias. FFmpeg n'est **pas** installé nativement sur les appareils Windows, il est donc nécessaire de l'installer afin d'utiliser l'outil Réparer vidéos..\
Voici un [tutoriel]([https://phoenixnap.com/kb/ffmpeg-windows](https://lecrabeinfo.net/installer-ffmpeg-sur-windows.html)) pour installer FFmpeg sur windows 11.\
*Rappel :Vous pouvez ouvrir un terminal Windows en pressant `win + r`, taper `cmd` puis presser `Entrée`.
