# E-commerce ShopAPI

---

API e-commerce développée avec **FastAPI**, **Poetry** et **Docker** dans le cadre du module d’industrialisation logicielle.

Le projet met en place une architecture backend moderne avec gestion des dépendances, conteneurisation et pipeline CI/CD.

---

# Technologies utilisées

- Python 3.11
- FastAPI
- Poetry
- Docker / Docker Compose
- Pytest
- Flake8
- Black
- MyPy
- GitHub Actions

---

# Structure du projet

```
team2_ecommerce_fast_api/
│
├── app/
│ ├── main.py
│ ├── models/
│ ├── routers/
│ ├── services/
│ ├── repositories/
│ └── core/
│
├── tests/
├── docs/
│
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
├── poetry.lock
│
├── .github/
│ └── workflows/
│    └── ci.yml
│
└── README.md
```

---

# Installation avec Poetry

Cloner le projet :

```
git clone https://github.com/Lee-Rudy/team2_ecommerce_fast_api.git
cd team2_ecommerce_fast_api

```
Installer les dépendances :
```bash
poetry install
```

Lancer l'application :
```bash
poetry run uvicorn app.main:app --reload
```

L’API sera accessible sur :

```
http://localhost:8000
```
Documentation interactive :
```
http://localhost:8000/docs
```

Lancer le projet avec Docker
Construire et démarrer le conteneur :

```
docker compose up --build
```

L’API sera accessible sur :
```
http://localhost:8000
```

---

# Docker Image (CI/CD)

Le pipeline GitHub Actions construit automatiquement une image Docker et la publie sur Docker Hub à chaque push sur main.

Docker Hub repository :
```
https://hub.docker.com/r/geraldinefrancois/team2_ecommerce_fast_api
```

Image la plus récente :
```
geraldinefrancois/team2_ecommerce_fast_api:latest
```

Télécharger et exécuter l'image :

```
docker pull geraldinefrancois/team2_ecommerce_fast_api:latest
docker run -p 8000:8000 geraldinefrancois/team2_ecommerce_fast_api:latest
```

---

# Tests

Exécuter les tests :
```
poetry run pytest
```

---

# Qualité du code
Vérifier la qualité du code :

```
poetry run flake8
poetry run black --check .
poetry run mypy .
```
---

# CI/CD

### Le pipeline GitHub Actions vérifie automatiquement :

- l’installation des dépendances

- la qualité du code (flake8, black, mypy)

- l’exécution des tests

- la couverture de tests (≥ 80%)

- la construction de l’image Docker

- la publication de l’image sur Docker Hub

- Le pipeline s’exécute à chaque push et pull request.

---
# API Documentation

FastAPI génère automatiquement la documentation :

Swagger UI :
```
/docs
```
ReDoc :
```
/redoc
```
---

# Auteur

Projet réalisé par **Team2** dans le cadre du module Developpement Avance.
- [@GeraldineFrancois](https://github.com/GeraldineFrancois)
- [@R-Christina](https://github.com/R-Christina)
- [@Lee-Rudy](https://github.com/Lee-Rudy)
- [@fehiz77](https://github.com/fehiz77)
- [@AmbiNtsoah](https://github.com/AmbiNtsoah)
