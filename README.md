# 🛒 Team2 E-commerce FastAPI

API e-commerce développée avec **FastAPI**, **Poetry** et **Docker** dans le cadre du module d’**industrialisation logicielle**.

Ce projet met en place une **architecture backend moderne** avec :

- gestion des dépendances avec **Poetry**
- conteneurisation avec **Docker**
- automatisation avec **GitHub Actions**
- tests automatisés et contrôle qualité

---

# ⚙️ Technologies utilisées

| Technologie | Description |
|-------------|-------------|
| Python 3.11 | Langage principal |
| FastAPI | Framework API moderne |
| Poetry | Gestion des dépendances |
| Docker | Conteneurisation |
| Docker Compose | Orchestration locale |
| Pytest | Tests automatisés |
| Flake8 | Analyse statique |
| Black | Formatage du code |
| MyPy | Vérification de types |
| GitHub Actions | Pipeline CI/CD |

---

# 📁 Structure du projet


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
│ └── ci.yml
│
└── README.md


---

# 🚀 Installation avec Poetry

### 1️⃣ Cloner le projet


git clone git@github.com:Lee-Rudy/team2_ecommerce_fast_api.git
cd team2_ecommerce_fast_api
2️⃣ Installer les dépendances
poetry install
3️⃣ Lancer l'application
poetry run uvicorn app.main:app --reload
Accès à l’API
http://localhost:8000
Documentation interactive
http://localhost:8000/docs
🐳 Lancer le projet avec Docker

Construire et démarrer les conteneurs :

docker compose up --build

L’API sera disponible sur :

http://localhost:8000
📦 Docker Image (CI/CD)

Le pipeline GitHub Actions construit automatiquement une image Docker et la publie sur Docker Hub à chaque push sur la branche main.

Repository Docker Hub
https://hub.docker.com/r/geraldinefrancois/team2_ecommerce_fast_api
Image la plus récente
geraldinefrancois/team2_ecommerce_fast_api:latest
Télécharger et exécuter l'image
docker pull geraldinefrancois/team2_ecommerce_fast_api:latest
docker run -p 8000:8000 geraldinefrancois/team2_ecommerce_fast_api:latest
🧪 Tests

Exécuter les tests :

poetry run pytest
🔎 Qualité du code

Vérifier la qualité du code :

poetry run flake8
poetry run black --check .
poetry run mypy .
🔄 CI/CD

Le pipeline GitHub Actions vérifie automatiquement :

installation des dépendances

qualité du code (flake8, black, mypy)

exécution des tests

couverture de tests (≥ 80%)

construction de l’image Docker

publication sur Docker Hub

Le pipeline s’exécute automatiquement à chaque :

push

pull request

📚 Documentation API

FastAPI génère automatiquement la documentation :

Swagger UI
/docs
ReDoc
/redoc
👥 Auteur

Projet réalisé par Team2 dans le cadre du module d’industrialisation logicielle.
