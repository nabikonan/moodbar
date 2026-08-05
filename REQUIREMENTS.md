# Requirements — Moodbar

Ce document recense les contraintes, exigences et décisions (prises ou en attente) du projet. Il complète le [README.md](README.md), qui décrit le fonctionnement général et l'architecture.

## Cadre du projet

- **Projet académique** : le MVP doit être défendable devant un jury et devant des chefs d'établissement potentiellement intéressés. Chaque choix technique doit être compris de bout en bout par l'équipe (langage, outils, code, fonctionnement, impacts) — pas de solution "boîte noire" qu'on ne saurait pas expliquer.
- **Budget** : aucun budget alloué en dehors du temps investi, à une exception près : le matériel de la borne IoT (voir [Matériel](#matériel)), approuvé pour ce MVP. Toute autre dépense (service payant, hébergement payant, matériel additionnel) reste **hors périmètre du MVP**.

## Contraintes techniques

- Priorité aux langages/outils déjà maîtrisés : HTML, CSS, Python, SQL/MySQL, R/RStudio, Git/GitHub, Bash.
- JavaScript (vanilla) est accepté comme extension nécessaire pour l'interactivité du frontend (nouveau, à apprendre en cours de route) — pas de framework JS (React/Vue) tant que la complexité ne le justifie pas.
- Développement incrémental, **step by step**, en commençant par le frontend (application web) avant le backend, le dashboard et la borne IoT.
- Toute techno retenue doit rester gratuite (outils open source, offres free-tier) — voir [Hors périmètre](#hors-périmètre-pour-linstant).

## Exigences fonctionnelles

- 3 boutons de vote : 🙂 Content, 😐 Neutre, 🙁 Pas content.
- Feedback immédiat après un vote : effet sonore + message aléatoire (encouragement/motivation), adapté à l'humeur choisie.
- Chaque vote est horodaté et envoyé au backend.
- Le dashboard agrège les votes et affiche des tendances (répartition, évolution dans le temps).
- Deux points de collecte alimentent le même backend : application web et borne IoT.

## Exigences non fonctionnelles

- **Simplicité d'interaction** : vote en quelques secondes, sans effort cognitif.
- **Anonymat** : aucune authentification, aucune donnée personnelle collectée (uniquement humeur + horodatage, éventuellement une source/lieu).
- **Accessibilité** : interface utilisable sur poste fixe, tablette ou smartphone, sans installation.
- **Quasi temps réel** : le dashboard doit refléter les votes récents sans délai perceptible important (pas nécessairement du WebSocket — un polling régulier est acceptable dans un premier temps).

## Modèle de données (esquisse)

Table `votes` :

| Champ | Type | Description |
|---|---|---|
| `id` | int, PK auto-increment | identifiant unique |
| `humeur` | enum/varchar (`content`, `neutre`, `pas_content`) | humeur votée |
| `horodatage` | datetime | date/heure du vote |
| `source` | varchar (`web`, `iot`) | origine du vote |
| `lieu` | varchar, nullable | localisation de la borne (si applicable) |

À ajuster une fois le backend en cours de conception.

## Matériel

Borne IoT physique (voir [moodbar-iot/](moodbar-iot/)) : Arduino Uno, LCD 16x2 en
câblage parallèle (pas de module I2C), 3 boutons poussoirs, LED verte, LED jaune,
LED rouge, 3 résistances 220 Ω, buzzer, breadboard, fils de connexion. Pas de
servo-moteur pour cette première version.

Brochage (montage réel) :

| Composant | Broche |
|---|---|
| LED verte (Heureux) | D7 |
| LED jaune (Neutre) | D9 |
| LED rouge (Triste) | D10 |
| Bouton Heureux | D13 |
| Bouton Neutre | D6 |
| Bouton Triste | A4 |
| Buzzer | D8 |
| LCD RS | D12 |
| LCD E | D11 |
| LCD D4 | D5 |
| LCD D5 | D4 |
| LCD D6 | D3 |
| LCD D7 | D2 |

## Décisions ouvertes

- **Hébergement / déploiement** : uniquement des offres gratuites (ex. free-tier Render/Railway/PythonAnywhere, GitHub Pages pour le frontend statique) — à confirmer une fois le backend fonctionnel en local.
- **Gestion des assets frontend** (sons, messages) : fichiers statiques locaux dans un premier temps, à revoir si besoin de gestion dynamique côté backend.

## Décisions tranchées

- **Borne IoT → prototype matériel Arduino Uno** : LCD, boutons, LEDs et buzzer pilotés par un Arduino Uno (voir [moodbar-iot/](moodbar-iot/) et [Matériel](#matériel)), qui transmet les votes en série à un bridge Python relayant vers l'API backend existante — même flux que l'application web. La page web dédiée en mode kiosque (`kiosk.html`) est conservée comme **solution de secours logicielle** (démo sans matériel, développement avant que le boîtier soit imprimé).
- **Dashboard analytique → Python (Streamlit)** : reste dans le même langage que le backend (un seul écosystème Python à gérer), et se connecte directement à la même base MySQL.

## Hors périmètre (pour l'instant)

- Authentification ou identification des utilisateurs.
- Analyse de sentiment avancée / traitement du langage naturel.
- Support multi-établissement.
- Application mobile native.
- Toute solution impliquant une dépense au-delà du matériel de la borne IoT déjà approuvé (voir [Matériel](#matériel)) : hébergement payant, services tiers payants, matériel additionnel (Raspberry Pi, ESP32, capteurs...).
