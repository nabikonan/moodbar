# Moodbar 🙂😐🙁

**Moodbar** est un système de monitoring de l'humeur en temps réel, conçu pour les établissements d'enseignement supérieur. Le projet combine une application web et un dispositif IoT afin de mesurer, visualiser et analyser en continu l'état émotionnel des étudiants au sein d'un établissement.

> **Note sur le MVP** : projet académique sans budget matériel alloué. La borne IoT est donc **simulée en logiciel** (une page web dédiée en mode kiosque, pas de matériel physique) pour cette version. Le déploiement sur un vrai dispositif IoT reste envisageable en roadmap future.

## Sommaire

- [Contexte et objectifs](#contexte-et-objectifs)
- [Fonctionnement général](#fonctionnement-général)
- [Expérience utilisateur](#expérience-utilisateur)
- [Architecture](#architecture)
- [Stack technique](#stack-technique)
- [Dashboard analytique](#dashboard-analytique)
- [Cas d'usage](#cas-dusage)
- [État du projet](#état-du-projet)

## Contexte et objectifs

Dans un établissement d'enseignement supérieur, l'humeur générale des étudiants (stress, fatigue, satisfaction, démotivation...) est rarement mesurée de manière continue et objective. Elle est pourtant un indicateur précieux pour :

- **Les étudiants** : exprimer leur ressenti du moment de façon simple et immédiate, sans jugement.
- **L'établissement** : détecter des tendances (baisse de moral avant les examens, amélioration après un événement, etc.) et adapter ses actions en conséquence.
- **Les équipes pédagogiques et administratives** : disposer d'un indicateur factuel et agrégé pour piloter des initiatives de bien-être étudiant.

Moodbar répond à ce besoin en proposant un point de collecte physique (borne IoT) et/ou digital (application web), couplé à un dashboard de visualisation des tendances en temps réel.

## Fonctionnement général

1. Un étudiant interagit avec une borne IoT ou l'application web Moodbar.
2. Il sélectionne l'une des trois humeurs proposées via un bouton dédié :
   - 🙂 **Content**
   - 😐 **Neutre**
   - 🙁 **Pas content**
3. L'interface réagit immédiatement avec :
   - un **effet sonore** associé à l'humeur sélectionnée,
   - un **message aléatoire** de motivation ou d'encouragement, adapté à l'humeur choisie.
4. La donnée collectée (humeur + horodatage) est envoyée en temps réel vers le backend.
5. Le **dashboard** agrège ces données et affiche les tendances globales de l'humeur au sein de l'établissement.

## Expérience utilisateur

L'interface a été pensée pour être **simple, épurée et intuitive**, afin de garantir une interaction rapide (quelques secondes) sans effort cognitif pour l'utilisateur :

- 3 boutons uniques, un par humeur, avec des icônes universellement reconnaissables (🙂😐🙁).
- Aucune authentification ou saisie complexe requise pour voter.
- Un retour immédiat (son + message) qui rend l'interaction agréable et engageante.
- Des messages de motivation variés et tirés aléatoirement, pour éviter la répétition et personnaliser l'expérience à chaque passage.

## Architecture

Moodbar repose sur deux points de collecte complémentaires qui alimentent un backend commun et un dashboard partagé :

```
┌─────────────────┐        ┌─────────────────┐
│   Application    │        │   Borne IoT       │
│   Web (3 boutons)│        │   simulée (page   │
│                  │        │   web, mode       │
│                  │        │   kiosque)        │
└────────┬─────────┘        └────────┬──────────┘
         │                           │
         │      Vote (humeur +       │
         │        horodatage)        │
         └───────────┬───────────────┘
                     ▼
            ┌──────────────────┐
            │  Backend / API    │
            │  (collecte,       │
            │   stockage,       │
            │   traitement      │
            │   temps réel)     │
            └────────┬──────────┘
                     ▼
            ┌──────────────────┐
            │  Dashboard         │
            │  analytique        │
            │  (tendances,       │
            │   agrégats,        │
            │   visualisations)  │
            └──────────────────┘
```

- **Application web** : point de collecte accessible depuis un navigateur (poste fixe, tablette, smartphone).
- **Borne IoT** : pour le MVP, simulée par une page web dédiée en mode kiosque (mêmes 3 boutons, pensée pour un usage sans smartphone ni souris/clavier). Un vrai dispositif physique (hall, cafétéria, bibliothèque...) reste une évolution possible hors MVP.
- **Backend** : centralise les votes, les horodate, les stocke et les rend disponibles en temps réel pour l'analyse.
- **Dashboard** : interface de visualisation à destination de l'établissement, affichant les tendances globales de l'humeur (par période, par lieu, par événement...).

## Stack technique

La stack est choisie en priorité parmi les langages/outils déjà maîtrisés, pour un développement progressif. Voir [REQUIREMENTS.md](REQUIREMENTS.md) pour le détail des contraintes.

### Décidé

| Brique | Techno |
|---|---|
| Frontend (application web) | HTML, CSS, JavaScript |
| Backend / API | Python (FastAPI) |
| Base de données | MySQL |
| Gestion de version | Git / GitHub |
| Scripts / automatisation | Bash |
| Borne IoT (simulée) | HTML, CSS, JavaScript — page dédiée en mode kiosque, même stack que le frontend |
| Dashboard analytique | Python (Streamlit) |

### À définir

| Brique | Options envisagées |
|---|---|
| Hébergement / déploiement | uniquement des offres gratuites (free-tier) |

> **Contrainte budget** : aucun budget alloué hors temps investi — toute solution payante est hors périmètre du MVP.

## Dashboard analytique

Le dashboard permet de visualiser en temps réel :

- La répartition globale des humeurs (🙂/😐/🙁) sur une période donnée.
- L'évolution de la tendance dans le temps (par jour, semaine, mois).
- Des pics ou anomalies pouvant être corrélés à des événements spécifiques (période d'examens, vacances, événements de campus...).

Cet outil est destiné aux équipes pédagogiques et administratives afin de mieux comprendre le climat émotionnel de l'établissement et d'ajuster leurs actions de bien-être étudiant en conséquence.

## Cas d'usage

- **Un étudiant** passe devant une borne Moodbar en sortant d'un cours et exprime son ressenti en un geste.
- **Un étudiant** ouvre l'application web pour signaler son humeur du jour et reçoit un message d'encouragement.
- **L'administration** consulte le dashboard chaque semaine pour suivre l'évolution du moral général et anticiper d'éventuelles périodes de tension (avant les partiels, par exemple).

## État du projet

Le projet en est actuellement au stade de conception. Les prochaines étapes prévues sont :

- [x] Définition de la stack technique (application web, backend, base de données, borne IoT simulée). Dashboard encore à trancher.
- [x] Développement de la borne IoT simulée (page web mode kiosque).
- [x] Développement de l'application web et de l'API de collecte (FastAPI + MySQL, testé de bout en bout en local).
- [x] Développement du dashboard de visualisation (Streamlit, connecté à la même base MySQL, testé de bout en bout avec des données réelles).
- [x] Conception détaillée de l'interface utilisateur (maquettes) — voir [docs/maquettes.html](docs/maquettes.html).
- [ ] Phase de test en conditions réelles au sein de l'établissement.
