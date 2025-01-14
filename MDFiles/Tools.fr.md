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
Si les vidéos sont endommagées (e.g. VLC Media Player un message d'erreur similaire à "Index endommagé ou absent") le programme ne sera pas capable de les lire correctement, il est donc nécessaire de réparer les vidéos en amont. Glissez et déposez le dossier sur la fenêtre puis cliquez sur "Valider". L'outil va récursivement regarder les vidéos dans le dossier et les sous-dossiers pour les réparer. Les fichiers vidéo `file.ext` avec *file* le nom de la vidéo et *ext* l'extension du format vidéo seront **remplacés** par `file.r.mkv`. Si cette réparation ne marche pas, bonne chance.\
**/!\\** La réparation peut changer la durée de la vidéo, créant un décalage temporel : assurez-vous que le temps de la vidéo reste aligné au temps réel, ou corrigez quand on vous le demande avant analyse vidéo.
