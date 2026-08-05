# Firmware — borne Moodbar (Arduino Uno)

## Matériel

Voir la section « Matériel » de [REQUIREMENTS.md](../../REQUIREMENTS.md) pour la
liste complète des composants et le tableau de brochage.

LCD 16x2 câblé en **mode parallèle** (RS, E, D4-D7 branchés directement sur
l'Arduino), pas de module I2C.

## Librairies Arduino requises

Aucune installation nécessaire : `LiquidCrystal` est fournie nativement avec
l'IDE Arduino (contrairement à un montage I2C qui aurait demandé
`LiquidCrystal_I2C`).

## Flash

1. Brancher l'Arduino Uno en USB.
2. Dans l'IDE Arduino : sélectionner la carte « Arduino Uno » et le bon port
   (Outils → Port).
3. Ouvrir `moodbar_kiosk.ino`, cliquer sur **Téléverser**.
4. Ouvrir le **Moniteur série** (9600 bauds) : chaque vote doit afficher une ligne
   `VOTE:content`, `VOTE:neutre` ou `VOTE:pas_content`.
5. **Fermer le Moniteur série avant de lancer `moodbar-iot/bridge/`** : un port
   série ne peut être ouvert que par un programme à la fois, le bridge Python ne
   pourra pas s'y connecter tant que le Moniteur série de l'IDE le retient.

## Points de débogage connus

- **Écran LCD qui n'affiche rien** : vérifier le câblage RS/E/D4-D7 face au
  brochage documenté dans `REQUIREMENTS.md`, ainsi que le potentiomètre de
  contraste (souvent une broche `V0` à relier à un potentiomètre ou à un pont
  diviseur de tension — sinon l'écran peut rester tout blanc ou tout noir même
  si le câblage logique est correct).
- **Boutons qui ne réagissent pas / réagissent tout le temps** : les boutons
  utilisent `INPUT_PULLUP`, donc ils doivent relier la broche numérique
  directement à la **masse** (GND) quand on appuie — pas besoin de résistance de
  pull-down externe. Un appui se lit `LOW`, le repos se lit `HIGH`.
- **LEDs trop faibles ou qui grillent** : vérifier la résistance 220 Ω en série
  sur chaque LED (entre la broche Arduino et l'anode, ou entre la cathode et la
  masse).

## Format de sortie série

Une ligne par vote, envoyée juste après l'action utilisateur :

```
VOTE:content
VOTE:neutre
VOTE:pas_content
```

C'est ce que lit `moodbar-iot/bridge/serial_to_api.py` pour relayer le vote vers
le backend Moodbar.
