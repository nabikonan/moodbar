# Bridge série → API — borne Moodbar

Relaie les votes envoyés par l'Arduino (voir `../firmware/`) sur le port série
vers l'API existante du backend Moodbar (`POST /api/votes`), exactement comme le
fait `moodbar-frontend/script.js` pour l'application web. Aucun changement côté
backend n'est nécessaire.

## Installation

```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Configuration

Copier `.env.example` en `.env` et ajuster :

- `SERIAL_PORT` — le port série de l'Arduino. Sous Windows, à trouver dans le
  **Gestionnaire de périphériques → Ports (COM et LPT)** une fois l'Arduino
  branché en USB (ex. `COM3`).
- `SERIAL_BAUD` — doit correspondre à `Serial.begin(9600)` dans le firmware
  (9600 par défaut, ne pas changer sans changer aussi le sketch).
- `BACKEND_URL` — l'URL du backend FastAPI (`http://localhost:8000` en local, ou
  l'URL de déploiement une fois hébergé).
- `KIOSK_LIEU` — optionnel, un nom de lieu pour cette borne (ex. `Hall principal`)
  si plusieurs bornes physiques sont déployées un jour.

## Lancement

```
python serial_to_api.py
```

Le script reste actif en continu, se reconnecte automatiquement si le port série
se déconnecte, et affiche dans la console chaque vote transmis (ou chaque échec
d'envoi, sans jamais planter silencieusement).
