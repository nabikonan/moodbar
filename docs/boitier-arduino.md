# Boîtier de la borne Moodbar — spécification

Conception d'une véritable borne interactive (plutôt qu'un simple boîtier
utilitaire) pour accueillir le prototype Arduino décrit dans
[moodbar-iot/](../moodbar-iot/).

## Caractéristiques

- Façade inclinée, pensée pour un usage debout (hall, cafétéria, bibliothèque).
- Écran LCD centré sur la façade.
- Trois gros boutons colorés (vert / jaune / rouge), correspondant aux 3 humeurs.
- Une LED au-dessus de chaque bouton.
- Une grille (perforations) au niveau du buzzer, pour laisser passer le son.
- L'Arduino Uno et le câblage fixés à l'intérieur du boîtier.
- Couvercle arrière démontable, pour l'accès maintenance (câblage, mise à jour du
  firmware, remplacement de composant).

## Dimensions proposées

| Dimension | Valeur |
|---|---|
| Largeur | 180 mm |
| Hauteur | 160 mm |
| Profondeur | 90 mm |

## État d'avancement

- Une première vue 3D (façade, arrière, côté, intérieur avec composants,
  dimensions générales) a été produite lors de la phase de conception.
- **Modélisation 3D définitive et fichiers d'impression (STL/STEP) : à faire.**
  Cette étape nécessite un outil de CAO (Tinkercad, Fusion 360, FreeCAD...) — ce
  document ne fournit que la spécification fonctionnelle et les dimensions
  cibles, pas de modèle 3D généré.

## Prochaines étapes

1. Finaliser le modèle 3D à partir de cette spécification.
2. Vérifier l'intégration réelle des composants (LCD, boutons, LEDs, buzzer,
   Arduino Uno + câblage) dans le volume proposé.
3. Exporter les fichiers d'impression et lancer l'impression 3D.
