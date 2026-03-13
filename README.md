# E-commerce ShopAPI

API e-commerce développée avec **FastAPI**, **Poetry** et **Docker** dans le cadre du module d'industrialisation logicielle.

---

## Description du projet et contexte métier

Cette API REST fournit une plateforme e-commerce complète permettant de gérer :

- **Gestion des produits** : CRUD complet avec filtres, recherche et catégorisation
- **Gestion des catégories** : Organisation des produits par catégories multiples
- **Gestion des stocks** : Suivi des mouvements (entrées/sorties) avec historique
- **Gestion des utilisateurs** : Système d'authentification avec rôles (user, admin, superadmin)
- **Authentification JWT** : Sécurisation des endpoints par tokens

L'architecture suit les principes Clean Architecture avec séparation claire des couches (models, repositories, services, routers).

---

## Technologies utilisées

- **Python 3.11**
- **FastAPI** - Framework web moderne et performant
- **SQLAlchemy** - ORM pour la gestion de base de données
- **Poetry** - Gestionnaire de dépendances
- **Docker / Docker Compose** - Conteneurisation
- **Pytest** - Framework de tests avec couverture (>80%)
- **Flake8** - Linter Python
- **Black** - Formateur de code
- **MyPy** - Vérification de types
- **GitHub Actions** - CI/CD automatisé

---

## Prérequis et installation

### Prérequis

- **Python 3.11+**
- **Poetry** (pour installation locale)
- **Docker & Docker Compose** (pour conteneurisation)
- **Git**

### Installation locale avec Poetry

1. Cloner le projet :

```bash
git clone https://github.com/Lee-Rudy/team2_ecommerce_fast_api.git
cd team2_ecommerce_fast_api
```

2. Installer les dépendances :

```bash
poetry install
```

3. Activer l'environnement virtuel :

```bash
poetry shell
```

---

## Lancer l'application en local

### Avec Poetry

```bash
poetry run uvicorn app.main:app --reload
```

L'API sera accessible sur `http://localhost:8000`

Documentation interactive : `http://localhost:8000/docs`

### Avec Docker

#### Lancer l'API :

```bash
docker compose up api --build
```

L'API sera accessible sur `http://localhost:8000`

#### Lancer en arrière-plan :

```bash
docker compose up api --build -d
```

#### Voir les logs :

```bash
docker compose logs -f api
```

#### Arrêter les conteneurs :

```bash
docker compose down
```

#### Arrêter et supprimer les volumes :

```bash
docker compose down -v
```

#### Reconstruire sans cache :

```bash
docker compose build --no-cache api
docker compose up api
```

---

## Lancer les tests

### Avec Docker (recommandé)

#### Lancer tous les tests avec rapport de couverture :

```bash
docker compose up test --build
```

**Résultat attendu :**
- 46 tests exécutés
- Couverture : **90.91%** (>80% requis)
- Rapport HTML généré dans `htmlcov/`

#### Lancer les tests en mode interactif :

```bash
docker compose run --rm test
```

#### Lancer des tests spécifiques :

```bash
# Tests d'API uniquement
docker compose run --rm test pytest tests/test_api_endpoints.py -v

# Tests de schémas uniquement
docker compose run --rm test pytest tests/test_schemas_simple.py -v

# Tests avec pattern
docker compose run --rm test pytest tests/test_product* -v
```

#### Voir le rapport de couverture :

Après avoir lancé les tests, ouvrir dans le navigateur :

```
./htmlcov/index.html
```

### En local (avec Poetry)

```bash
# Tests avec couverture complète
poetry run pytest --cov=app --cov-report=term-missing --cov-report=html --cov-fail-under=80

# Tests simples
poetry run pytest -v

# Tests d'un fichier spécifique
poetry run pytest tests/test_api_endpoints.py -v
```

---

## Structure du projet

```
team2_ecommerce_fast_api/
│
├── app/                          # Code source de l'application
│   ├── main.py                   # Point d'entrée FastAPI
│   ├── database.py               # Configuration SQLAlchemy
│   │
│   ├── models/                   # Modèles SQLAlchemy + Pydantic
│   │   ├── user.py
│   │   ├── product.py
│   │   ├── category.py
│   │   ├── stock_movement.py
│   │   └── product_category.py
│   │
│   ├── repositories/             # Couche d'accès aux données
│   │   ├── UserRepo.py
│   │   ├── product_repo.py
│   │   ├── category_repo.py
│   │   └── stock_movement_repo.py
│   │
│   ├── services/                 # Logique métier
│   │   ├── auth_service.py
│   │   ├── UserService.py
│   │   ├── product_service.py
│   │   ├── category_service.py
│   │   └── stock_movement_service.py
│   │
│   ├── routers/                  # Endpoints API
│   │   ├── route_auth.py
│   │   ├── User.py
│   │   ├── route_product.py
│   │   ├── category.py
│   │   └── route_stock_movement.py
│   │
│   └── core/                     # Configuration et utilitaires
│
├── tests/                        # Suite de tests (46 tests)
│   ├── ci/                       # Tests pour CI/CD
│   ├── test_api_endpoints.py     # Tests des endpoints
│   ├── test_schemas_simple.py    # Tests validation Pydantic
│   ├── test_services_simple.py   # Tests logique métier
│   ├── test_category_operations.py
│   ├── test_product_operations.py
│   ├── test_stock_operations.py
│   ├── test_user_operations.py
│   └── test_complete_flows.py    # Tests end-to-end
│
├── .github/
│   └── workflows/
│       └── ci.yml                # Pipeline CI/CD
│
├── Dockerfile                    # Image Docker pour l'API
├── Dockerfile.test               # Image Docker pour les tests
├── docker-compose.yml            # Orchestration des services
├── pyproject.toml                # Configuration Poetry
├── poetry.lock                   # Versions figées des dépendances
└── README.md
```

---

## Documentation de l'API

FastAPI génère automatiquement une documentation interactive complète.

### Swagger UI (interface interactive)

```
http://localhost:8000/docs
```

Permet de :
- Visualiser tous les endpoints
- Tester les requêtes directement
- Voir les schémas de données

### ReDoc (documentation alternative)

```
http://localhost:8000/redoc
```

Documentation élégante et lisible des endpoints.

---

## Endpoints principaux

### Authentification

- `POST /auth/login` - Connexion utilisateur (retourne un JWT)

### Produits

- `GET /products/` - Liste tous les produits
- `GET /products/{id}` - Détail d'un produit
- `POST /products/` - Créer un produit
- `PUT /products/{id}` - Modifier un produit
- `DELETE /products/{id}` - Supprimer un produit
- `GET /products/search?name=...` - Rechercher par nom
- `GET /products/filter?...` - Filtrer (category_id, min_price, max_price, in_stock)

### Catégories

- `GET /categories/` - Liste toutes les catégories
- `GET /categories/{id}` - Détail d'une catégorie
- `POST /categories/` - Créer une catégorie
- `PUT /categories/{id}` - Modifier une catégorie
- `DELETE /categories/{id}` - Supprimer une catégorie

### Mouvements de stock

- `GET /stock-movements/` - Liste tous les mouvements
- `POST /stock-movements/` - Enregistrer un mouvement (IN/OUT)

### Utilisateurs (requiert authentification)

- `GET /users/` - Liste tous les utilisateurs (Admin+)
- `GET /users/{id}` - Détail d'un utilisateur (Admin+)
- `POST /users/` - Créer un utilisateur (Superadmin)
- `PUT /users/{id}` - Modifier un utilisateur (Admin+)
- `DELETE /users/{id}` - Supprimer un utilisateur (Superadmin)

---

## Qualité du code et normes

### Standards respectés

- **Black** : Formatage automatique (line-length: 88)
- **Flake8** : Lint sans erreurs
- **MyPy** : Vérification des types
- **Google Style Docstrings** : Documentation complète du code
- **Coverage** : 90.91% (>80% requis)

### Commandes de vérification

```bash
# Vérifier le formatage
poetry run black --check app tests

# Formater automatiquement
poetry run black app tests

# Linter
poetry run flake8 app tests

# Vérification de types
poetry run mypy app

# Tests avec couverture
poetry run pytest --cov=app --cov-report=term-missing --cov-fail-under=80
```

---

## CI/CD avec GitHub Actions

Le pipeline automatisé vérifie à chaque push et pull request :

### Job `quality`
- Installation des dépendances
- Lint avec Flake8
- Formatage avec Black
- Vérification des types avec MyPy

### Job `test`
- Installation des dépendances
- Exécution de tous les tests (46 tests)
- Vérification du coverage (≥ 80%)
- Génération du rapport de couverture

**Coverage actuel : 90.91%** ✅

Le pipeline s'exécute automatiquement sur les branches `main` et `develop`.

---

## Docker Hub

Le pipeline publie automatiquement l'image Docker sur Docker Hub.

**Repository :**
```
https://hub.docker.com/r/geraldinefrancois/team2_ecommerce_fast_api
```

**Télécharger et exécuter l'image :**

```bash
docker pull geraldinefrancois/team2_ecommerce_fast_api:latest
docker run -p 8000:8000 geraldinefrancois/team2_ecommerce_fast_api:latest
```

---

## Base de données

L'application utilise SQLite en développement :

```
sqlite:///./e-commerce.db
```

Les tables sont créées automatiquement au démarrage via SQLAlchemy.

**Modèles disponibles :**
- Users (avec authentification et rôles)
- Products (avec catégories multiples)
- Categories
- StockMovements (historique des mouvements)
- ProductCategories (table d'association)

---

## Contributeurs

Projet réalisé par **Team2** dans le cadre du module Développement Avancé.

- [@GeraldineFrancois](https://github.com/GeraldineFrancois)
- [@R-Christina](https://github.com/R-Christina)
- [@Lee-Rudy](https://github.com/Lee-Rudy)
- [@fehiz77](https://github.com/fehiz77)
- [@AmbiNtsoah](https://github.com/AmbiNtsoah)

---

## Licence

Ce projet est développé dans un cadre académique.
