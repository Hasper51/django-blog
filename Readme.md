# Django Blog with Docker Compose, Makefile, and PostgreSQL

**Django Blog** - Django REST API application based on onion architecture.

## Requirements

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [GNU Make](https://www.gnu.org/software/make/)

## 📦 Main Features
- 🔑 Registration and authorization of users
- ✍️ Creating, editing and deleting posts
- 💬 Comment and like system
- 🖼️ Uploading images to articles
- 🔍 Search by articles
- ❤️ Subscription system
- 🔔 Notification system
- 📊 Admin panel for content management

## 🛠 Tech Stack

### Backend
- **Python 3.12**
- **Django 5.1**
- **Django Ninja**: for building APIs
- **PostgreSQL**: database
- **Celery**: for background task processing (with Redis)
- **PyJWT**: JSON Web Token-based authentication

### DevOps
- **Docker**: containerization

### Testing and Automation
- **Pytest**: for testing
- **Factory Boy**: for fixture generation
- **Pre-commit**: automated code checks
- **isort**: import sorting
- **autoflake**: unused code removal


## 🚀 How to Use

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your_username/your_repository.git
   cd your_repository

2. Install all required packages in `Requirements` section.
3. Rename .env_example to . env and enter your details if necessary.
4. Run with the commands:
`make migrations`,
`make migrate`,
`make app`

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
