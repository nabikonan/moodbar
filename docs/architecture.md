# Architecture du projet Moodbar

## Vision

Système de monitoring de l'humeur en temps réel pour le **Dakar Institute of
Technology** — projet académique (MVP, sans budget matériel). Les étudiants votent
leur humeur (🙂/😐/🙁) via une appli web ou une borne IoT simulée ; les votes sont
centralisés et visualisés dans un dashboard analytique.

## Vue d'ensemble

```
┌─────────────────────┐        ┌──────────────────────┐
│  Application Web      │        │  Borne IoT (simulée)   │
│  (index.html)          │        │  (kiosk.html)          │
│  moodbar-frontend/     │        │  même code, mode       │
└──────────┬─────────────┘        │  kiosque plein écran   │
           │                      └──────────┬─────────────┘
           │        POST /api/votes          │
           │         {humeur, source}         │
           └───────────────┬──────────────────┘
                            ▼
                 ┌────────────────────────┐
                 │  Backend FastAPI         │
                 │  moodbar-backend/         │
                 │  - sert aussi le frontend │
                 │    statique (même origine)│
                 │  - pool de connexions DB  │
                 └───────────┬────────────────┘
                             ▼
                 ┌────────────────────────┐
                 │  MySQL (Railway, distant) │
                 │  table `votes`            │
                 └───────────┬────────────────┘
                             ▼ (lecture directe SQL)
                 ┌────────────────────────┐
                 │  Dashboard Streamlit      │
                 │  moodbar-dashboard/        │
                 │  donut + barres Plotly     │
                 └────────────────────────┘
```

## Les composants

### 1. Frontend (`moodbar-frontend/`) — HTML/CSS/JS vanilla

- **`index.html`** — app web : bloc branding (« M🙂🙁dBar » + « Dakar Institute of
  Technology » + logo), 3 boutons de vote, feedback sonore + message, et le lien
  discret vers le dashboard admin.
- **`kiosk.html`** — même logique, boutons agrandis pour un usage tactile en mode
  kiosque (`data-source="iot"` au lieu de `"web"`), pas de branding ni de lien admin.
- **`script.js`** (partagé) : joue un son (`AudioContext` réutilisé, pas recréé à
  chaque clic), affiche un message aléatoire, envoie le vote en `fetch POST`, gère
  l'échec réseau avec un message d'erreur visible.
- **`style.css`** (partagé) : tout le visuel, y compris les couleurs par humeur
  (vert/ambre/corail) réutilisées ensuite dans le dashboard.

### 2. Backend (`moodbar-backend/`) — FastAPI (Python)

- **`main.py`** — 2 routes :
  - `POST /api/votes` : insère un vote (`humeur`, `source`, `lieu` optionnel).
  - `GET /api/votes` : liste les derniers votes (utilisé pour debug/API, pas par le
    dashboard qui lit directement la DB).
  - Monte aussi `moodbar-frontend/` en fichiers statiques sur `/` → un seul service,
    une seule origine, pas de souci CORS.
- **`db.py`** — pool de connexions MySQL (`mysql.connector.pooling`, 5 connexions) :
  la base étant hébergée à distance (Railway), ouvrir une connexion par requête
  coûterait ~2s de handshake réseau à chaque vote.

### 3. Base de données — MySQL

Une seule table `votes` :

| Champ | Type | Rôle |
|---|---|---|
| `id` | int PK auto-increment | identifiant |
| `humeur` | enum(`content`,`neutre`,`pas_content`) | humeur votée |
| `horodatage` | datetime | horodatage du vote |
| `source` | varchar(`web`,`iot`) | origine |
| `lieu` | varchar nullable | localisation borne (optionnel) |

Schéma défini dans `moodbar-backend/schema.sql`.

### 4. Dashboard (`moodbar-dashboard/`) — Streamlit (Python)

- **`app.py`** : se connecte **directement** à la même base MySQL (pas via l'API
  backend), avec cache 30s (`st.cache_data`).
- Filtre par période + granularité (jour/semaine/mois).
- 3 métriques en cartes, un **donut** (répartition globale) et un **diagramme en
  bandes** (évolution dans le temps) en Plotly, couleurs de marque cohérentes avec
  les boutons du frontend, table de détail brute en bas de page.

## Décisions d'architecture clés (documentées dans `REQUIREMENTS.md`)

- **Aucune authentification** — anonymat total, ni pour voter ni pour consulter le
  dashboard.
- **Un seul écosystème Python** pour backend + dashboard (FastAPI + Streamlit),
  MySQL comme unique base.
- **JS vanilla uniquement**, pas de framework front (React/Vue) — complexité pas
  justifiée pour 3 boutons.
- **Borne IoT simulée en logiciel** (pas de Raspberry Pi/ESP32) — contrainte budget.
- **Tout doit rester gratuit** (outils open source, free-tier).

## Ajouts récents (26/07/2026), par-dessus cette base

- Le petit lien admin sur `index.html` vers le dashboard Streamlit.
- Le branding « MoodBar · DIT » sur la page web.
- Le donut + le diagramme en bandes Plotly, et le thème carte du dashboard (à la
  place des graphiques Streamlit natifs basiques).

Détail complet de ces ajouts dans [rapport-2026-07-26.md](rapport-2026-07-26.md).
