<table>
  <tr>
    <th>Image</th>
    <th>Comment</th>
  </tr>
  <tr>
    <td><img src="images/lines/AIX1_good.png" width="250"></td>
    <td>Bonne ligne, couvre la voie sans empiéter sur une autre ou sur des véhicules stationnés. Eloignée d'obstacles occultants et du bord de l'image.</td>
  </tr>
  <tr>
    <td><img src="images/lines/AIX1_bad.png" width="250"></td>
    <td>Pourrait interférer avec la voie d'entrée en bas à droite.</td>
  </tr>
  <tr>
    <td><img src="images/lines/AIX1.jpg" width="250"></td>
    <td>Exemple pour directionnel. Lignes orientées vers le centre de l'intersection.</td>
  </tr>
  <tr>
    <td><img src="images/lines/AIX2.jpg" width="250"></td>
    <td>Lignes bien placées pour leurs voies respectives. La voie du fonc est occultées par le panneau et ne peut pas être comptée.</td>
  </tr>
  <tr>
    <td><img src="images/lines/MEZES.jpg" width="250"></td>
    <td>Autre bon exemple pour directionnel.</td>
  </tr>
  <tr>
    <td>
      <img src="images/lines/nuit%202%20off.jpg" width="250">
      <img src="images/lines/nuit%202%20on.jpg" width="250">
    </td>
    <td>Attention à ce que la ligne 0 ne se superpose pas au container, qui pourrait créer des faux positifs, en particulier avec les variations de lumière.</td>
  </tr>
  <tr>
    <td>
      <img src="images/lines/obstruct.JPG" width="250">
      <img src="images/lines/obstruct_n.jpg" width="250">
    </td>
    <td>Selon le placement de la caméra, les obstructions visuelles sont plus ou moins fortes. Ici un 2 roues passait derrière le camion.</td>
  </tr>
  <tr>
    <td><img src="images/lines/PEGOMAS.jpg" width="250"></td>
    <td>Lignes bien placées. L'environnement de la ligne 1 (éloignement, véhicules stationnés, obstacles visuels) rend l'attention portée au placement cruciale et le comptage difficile.</td>
  </tr>
  <tr>
    <td><img src="images/lines/perspectived.jpg" width="250"></td>
    <td>Ici, par jeu de perspective, l'IA a considéré qu'en plus de la camionnette, l'ensemble camionnette ressemblait à un camion grue et l'a compté à tort. Cela est dû au placement de la ligne, qui fait compter l'IA précisément à ce point de superposition.</td>
  </tr>
  <tr>
    <td><img src="images/lines/remorque.jpg" width="250"></td>
    <td>Généralement, les remorques sont considérées comme des véhicules à part.</td>
  </tr>
  <tr>
    <td><img src="images/lines/RODEZ.jpg" width="250"></td>
    <td>Exemple OD. Les lignes du fond sont correctement placées. La ligne de gauche subit un problème de sous-comptage en entrée : les buissons épais cachent les véhicules entrant par cett vois (pas les sortant). Décaler la ligne vers la droite pallierait le problème, <b>mais</b> les véhicules circulant sur le carrefour giratoire pourrait la traverser.</td>
  </tr>
  <tr>
    <td><img src="images/lines/setup%201.jpg" width="250"></td>
    <td>Ici, la ligne 1, plus proche, offre une meilleure qualité de détection. La placer plus près du bas de l'image pourrait empêcher l'IA de détecter les véhicuels avant qu'il n'aient croisé la ligne.</td>
  </tr>
  <tr>
    <td><img src="images/lines/setup%202.jpg" width="250"></td>
    <td>Excellent placement de la caméra, l'angle de vue permet une détection et une catégorisation des véhicules casi-parfaite. Le fond sans ambiguïté (bâtiment) permet d'étendre la ligne pour assurer les détection, sans être un danger de surcomptage.</td>
  </tr>
  <tr>
    <td><img src="images/lines/STJUNIEN1.jpg" width="250"></td>
    <td>Au delà de la luminosité trop absse pour l'IA, la ligne du bas est trop proche du bas de l'image, et celle de droite trop proche d'un obstacle occultant (bâtiment).</td>
  </tr>
  <tr>
    <td><img src="images/lines/STJUNIEN2.jpg" width="250"></td>
    <td>Bon exemple pour enquête directionnelle. Attention, ici la ligne du fond a été placée légèrement trop bas et a parfois compté des véhicles circulant sur le carrefour giratoire.</td>
  </tr>
  <tr>
    <td><img src="images/lines/VALENCE.jpg" width="250"></td>
    <td>Bon exemple directionnel. Ici la voie du bas a été analysée en 2 lignes pour une détection plus précise. Il y a sous-comptage des voies latérales à cause du manque du luminosité (les véhicules se détachent mal du fond).</td>
  </tr>
</table>

