# Moodbar — Dashboard

Dashboard Streamlit qui se connecte à la même base MySQL que le backend pour visualiser les tendances de vote.

## Installation

```bash
python -m venv venv
./venv/Scripts/pip install -r requirements.txt   # (Linux/Mac : venv/bin/pip)
```

## Configuration

1. Copier `.env.example` en `.env`
2. Renseigner les identifiants MySQL locaux (les mêmes que pour le backend)

## Lancer le dashboard

```bash
./venv/Scripts/python -m streamlit run app.py   # (Linux/Mac : venv/bin/python)
```

Ouvre http://localhost:8501

## Fonctionnalités

- Répartition globale des humeurs sur une période choisie
- Évolution dans le temps (jour / semaine / mois)
- Détail des votes (table brute, filtrée par période)
- Bouton "Actualiser" pour forcer un rafraîchissement des données (le cache expire de toute façon après 30s)
