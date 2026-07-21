# Moodbar — Backend

API FastAPI qui collecte les votes (web + borne IoT simulée) et sert aussi le frontend statique (`moodbar-frontend/`) sur la même origine.

## Prérequis

- Python 3
- MySQL en local (le service doit tourner)

## Installation

```bash
python -m venv venv
./venv/Scripts/pip install -r requirements.txt   # (Linux/Mac : venv/bin/pip)
```

## Configuration

1. Copier `.env.example` en `.env`
2. Renseigner les identifiants MySQL locaux (`DB_USER`, `DB_PASSWORD`, ...)

## Base de données

Appliquer le schéma une fois :

```bash
mysql -u <user> -p < schema.sql
```

Crée la base `moodbar` et la table `votes`.

## Lancer le serveur

```bash
./venv/Scripts/python -m uvicorn main:app --port 8000   # (Linux/Mac : venv/bin/python)
```

- Frontend : http://localhost:8000/ (page web) et http://localhost:8000/kiosk.html (borne simulée)
- API : `POST /api/votes` (enregistrer un vote), `GET /api/votes` (lister les votes)

## Endpoints

| Méthode | Route | Description |
|---|---|---|
| POST | `/api/votes` | Enregistre un vote (`humeur`, `source`, `lieu` optionnel) |
| GET | `/api/votes` | Liste les derniers votes (paramètre `limit`, défaut 100) |
