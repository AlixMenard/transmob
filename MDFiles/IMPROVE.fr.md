# Guide pour l'amélioration du programme
## Version de YOLO

Si une nouvelle version plus performante de YOLO sort, téléchargez les modèles et placez les dans le dossier `weights`. Ensuite, dans `GUI.py`, modifiez cette ligne :
<p align="center">
  <img src="images/YOLO_version.png?raw=true" alt="Version YOLO" title="Version YOLO" width="45%"/><br>
  <em>Version YOLO</em>
</p>
Il faut changer le nom générique du modèle YOLO (e.g. `yolov8{m}.pt` ou `yolo11{m}.pt`). Le paramètre `{m}` changera automatiquement en fonction de la taille de modèle choisie au lancement. *Verifiez bien le nom des modèles pour mettre le bon nom générique.*

## Paramètres du traqueur

### Lignes pour modification

Le suivi de véhicule est fait avec BoT-SORT. Les paramètres sont disponibles dans `TransmobYTC/Analyze.py` (pour la version carte graphique, sinon `TransmobYT/Analyze.py`) aux lignes :
<table>
  <tr>
    <td align="center" width="45%">
      <img src="images/Tracker_YTC.png?raw=true" alt="Traqueur YTC" title="Traqueur YTC"/>
      <br/><sub>Traqueur YTC</sub>
    </td>
    <td align="center" width="45%">
      <img src="images/Tracker_YT.png?raw=true" alt="Traqueur YT" title="Traqueur YT"/>
      <br/><sub>Traqueur YT</sub>
    </td>
  </tr>
</table>

### Paramètres de suivi

| Paramètres généraux      | Détection & Suivi        | Critères d'association        |
|----------------------|----------------------------|--------------------------|
| **`cmc_method`**: Méthode de correction des mouvements caméra. | **`track_high_thresh`**: Confiance min pour associer les détections. | **`match_thresh`**: Seuil IoU pour associer la détection à une traque. |
| **`device`**: `cuda:0` (carte graphique) ou `cpu`. | **`track_low_thresh`**: Confiance min pour la traque. | **`proximity_thresh`**: Distance max entre 2 cadres pour association. |
| **`half`**: utilise FP16 pour la rapidité, si disponible. | **`new_track_thresh`**: Confiance min pour commencer une traque. | **`appearance_thresh`**: Similarité min pour association par visuel. |
| **`frame_rate`**: Influe sur le *track_buffer*. | **`track_buffer`**: Nombres max d'images pour conserver une traque perdue. | **`fuse_first_associate`**: Utiliser le visuel et le mouvement pour la première association. |
| **`with_reid`**: Autorise l'utilisation de la reconnaissance visuelle. | | **`reid_weights`**: Chemin vers le modèle de reconnaissance visuelle. |
| **`per_class`**: Traquer les objets séparéments par classe (non recommandé). |   |   |


*\* IoU : Aire d'Intersection / Aier d'Union*
*Une traque est l'ensemble des éléments composant le suivi **d'un** véhicule.*

### Aides
- **trop d'échanges d'ID** Augmenter `track_buffer`, baisser `match_thresh`, `proximity_thresh`, `appearance_thresh`.
- **Mauvaises associations** Augmenter `match_thresh`, `proximity_thresh`, `appearance_thresh`.
- **Détections manquantes** Baisser `new_track_thresh`, `track_high_thresh`.
- **Perte traque après occlusion** Augmenter `track_buffer`, ajuster `appearance_thresh`.

## Entraîner un nouveau modèle

De nombreux tutos sont disonibles en ligne pour entraîner un moèdel personnalisé de YOLO. Ils peuvent différer selon la version de YOLO utilisée. Voici la [page Ultralytics pour l'entraînement](https://docs.ultralytics.com/modes/train/)  officielle, valide jusqu'à YOLOv12. La page présente tous les paramètres, ainsi qu'un tutoriel vidéo pour un guide étape pétape.

Entraîner un modèle nécessite un ensemble de donnée, certains peuvent être trouvés sur des sites comme [Roboflow Universe](https://universe.roboflow.com/).

## OnlyVans

OnlyVans est le modèle utilisé spécifiquement pour identifier les camionnettes, afin d'éviter les voitures catégorisées en camions. La version originale est basée sur YOLO11, et entraînnée sur [cet ensemble de données](https://universe.roboflow.com/maryam-mahmood-6hoeq/vans/dataset/3). Si vous entraîner un nouveau modèle OnlyVans, voici comment l'implementer : dans `TransmobYTC/Vehicle.py`
<p align="center">
  <img src="images/OnlyVans_import.png?raw=true" alt="Import OnlyVans" title="Import OnlyVans" width="45%"/>
  <br>
  <em>Import OnlyVans</em>
</p>
Changer le chemin pour celui du nouveau modèle.
