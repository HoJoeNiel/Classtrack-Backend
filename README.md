
# Classtrack-Backend
Backend repo for our ClassTrack project

## Responsibilities:

### Authentication:
-   User registration (`POST /register`)
-   Login & token generation (`POST /login`)
-   Logout (`POST /logout`)
-   Password hashing & JWT authentication

#### Delegation
* Register:  Luis
* Login: Darren
* Logout: Luis


### Database Migration and Models
-   Designing tables (users, posts, comments, etc.)
-   Setting up SQLAlchemy models
-   Writing Alembic migrations

#### Delegation
- Luis
- Darren


### CRUD Operations (Core Business Logic)
-   Implementing API endpoints for main resources (e.g., posts, comments)
-   Writing database queries (async SQLAlchemy or raw SQL)

#### Delagation
- Dan
- Luis
- Darren

Testing & Error Handling:
-- Luis


## Example Project Structure

```
backend/
├── app/
│   ├── api/                # API endpoints
│   │   ├── v1/
│   │   │   ├── endpoints/
│   │   │   │   ├── auth.py   # Login, register, logout
│   │   │   │   ├── users.py  # CRUD for users
│   │   │   │   ├── posts.py  # CRUD for posts
│   │   │   │   ├── __init__.py
│   │   │   ├── __init__.py
│   │   ├── __init__.py
│   │   
│   ├── core/               # Configurations & security
│   │   ├── config.py        # Settings (DB URL, secrets)
│   │   ├── security.py      # Password hashing, JWT tokens
│   │   ├── database.py      # DB connection setup
│   │   ├── __init__.py
│   │   
│   ├── db/                 # Database models & migrations
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   ├── post.py
│   │   │   ├── __init__.py
│   │   ├── repositories/    # CRUD logic
│   │   │   ├── user_repo.py
│   │   │   ├── post_repo.py
│   │   │   ├── __init__.py
│   │   ├── migrations/      # Alembic migrations
│   │   ├── __init__.py
│   │   
│   ├── tests/              # Automated tests
│   │   ├── test_auth.py
│   │   ├── test_users.py
│   │   ├── test_posts.py
│   │   ├── __init__.py
│   │   
│   ├── main.py             # Entry point
│   ├── dependencies.py      # Shared dependencies
│   ├── __init__.py
│   
├── alembic/                # Database migrations folder (Alembic)
├── .env                    # Environment variables
├── requirements.txt         # Dependencies (FastAPI, asyncpg, etc.)
├── Dockerfile               # Docker config for deployment
├── docker-compose.yml       # PostgreSQL + FastAPI setup
├── .gitignore
```

#### **Main Application**
- `main.py` - Starts FastAPI app & includes routes

#### **API**
- `api/v1/endpoints/` - API endpoints (routes)

#### **Configuration & Security**
- `core/config.py` - Stores settings (DB URL, JWT secret)
- `core/security.py` - Password hashing & JWT authentication

#### **Database**
- `db/models/` - SQLAlchemy database models
- `db/repositories/` - Contains reusable database queries
- `db/migrations/` - Alembic migration scripts

#### **Testing**
- `tests/` - Unit tests using pytest

#### **Docker & Deployment**
- `Dockerfile` - Defines the Docker container for the backend
- `docker-compose.yml` - Runs FastAPI + PostgreSQL locally


## Technologies:
### Framework:
* FastAPI

### Database:
- Postgresql
- asyncpg (Driver)

### Language:
- Python

### Authentication:
- JWT authentication


