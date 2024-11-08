# Django Boilerplate with Docker Compose, Makefile, and PostgreSQL

This is a basic template for Django projects configured to use Docker Compose, Makefile, and PostgreSQL.

## Requirements

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [GNU Make](https://www.gnu.org/software/make/)

## How to Use

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your_username/your_repository.git
   cd your_repository

2. Install all required packages in `Requirements` section.


### Implemented Commands

* `make app` - up application and database/infrastructure
* `make app-logs` - follow the logs in app container
* `make app-down` - down application and all infrastructure
* `make storages` - up only storages. you should run your application locally for debugging/developing purposes
* `make storages-logs` - foolow the logs in storages containers
* `make storages-down` - down all infrastructure

### Most Used Django Specific Commands

* `make migrations` - make migrations to models
* `make migrate` - apply all made migrations
* `make collectstatic` - collect static
* `make superuser` - create admin user

```
django-blog
├─ core
│  ├─ api
│  │  ├─ schemas.py
│  │  ├─ urls.py
│  │  ├─ v1
│  │  │  ├─ posts
│  │  │  │  ├─ handlers.py
│  │  │  │  ├─ schemas.py
│  │  │  │  ├─ __init__.py
│  │  │  │  └─ __pycache__
│  │  │  ├─ urls.py
│  │  │  ├─ __init__.py
│  │  │  └─ __pycache__
│  │  ├─ __init__.py
│  │  └─ __pycache__
│  ├─ apps
│  │  ├─ common
│  │  │  ├─ apps.py
│  │  │  ├─ models.py
│  │  │  ├─ __init__.py
│  │  │  └─ __pycache__
│  │  ├─ notifications
│  │  │  ├─ admin.py
│  │  │  ├─ apps.py
│  │  │  ├─ models.py
│  │  │  ├─ tests.py
│  │  │  ├─ views.py
│  │  │  └─ __init__.py
│  │  ├─ posts
│  │  │  ├─ admin.py
│  │  │  ├─ apps.py
│  │  │  ├─ entities
│  │  │  │  ├─ posts.py
│  │  │  │  ├─ __init__.py
│  │  │  │  └─ __pycache__
│  │  │  ├─ models.py
│  │  │  ├─ services
│  │  │  │  ├─ posts.py
│  │  │  │  ├─ __init__.py
│  │  │  │  └─ __pycache__
│  │  │  ├─ __init__.py
│  │  │  └─ __pycache__
│  │  ├─ users
│  │  │  ├─ admin.py
│  │  │  ├─ apps.py
│  │  │  ├─ models.py
│  │  │  ├─ views.py
│  │  │  ├─ __init__.py
│  │  │  └─ __pycache__
│  │  ├─ __init__.py
│  │  └─ __pycache__
│  ├─ project
│  │  ├─ asgi.py
│  │  ├─ settings
│  │  │  ├─ main.py
│  │  │  ├─ __init__.py
│  │  │  └─ __pycache__
│  │  ├─ urls.py
│  │  ├─ wsgi.py
│  │  ├─ __init__.py
│  │  └─ __pycache__
│  ├─ __init__.py
│  └─ __pycache__
├─ Dockerfile
├─ docker_compose
│  ├─ app.yaml
│  └─ storages.yaml
├─ entrypoint.sh
├─ Makefile
├─ manage.py
├─ media
│  └─ posts
│     └─ doja-cat-woman.jpeg
├─ poetry.lock
├─ pyproject.toml
└─ Readme.md

```