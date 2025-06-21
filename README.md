# Django REST API Blog System

![Python](https://img.shields.io/badge/Python-3.12-blue.svg)
![Django](https://img.shields.io/badge/Django-5.2-green.svg)
![Django REST Framework](https://img.shields.io/badge/DRF-3.16-red.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-blue.svg)
![Docker](https://img.shields.io/badge/Docker-Compose-blue.svg)
![Tests](https://img.shields.io/badge/Tests-Pytest-yellow.svg)

A production-ready blogging API built with Django and Django REST Framework. This project was developed to demonstrate best practices in API design, testing, containerization, and security.

---

## ✨ Core Features

*   **Models & Relationships:** Well-structured Django models for `Author`, `Post`, and `Comment` with optimized relationships (`ForeignKey`), indexing, and robust `on_delete` policies.
*   **Production-Ready API:** A versioned (`/api/v1/`) and fully-featured REST API covering full CRUD for Posts, nested creation of Comments, advanced filtering, and granular, owner-based permissions.
*   **Interactive Documentation:** Auto-generated, interactive API documentation (Swagger/OpenAPI) powered by `drf-spectacular`.
*   **Comprehensive Testing:** A high-coverage test suite using `pytest` that validates models, API endpoints, permissions, and business logic.
*   **Containerized Environment:** The entire application and its PostgreSQL database are containerized using Docker and Docker Compose for seamless setup and deployment consistency.
*   **Secure by Design:** Secrets are managed via environment variables (`.env.prod`), and defensive validation is implemented at both the serializer and view levels.

---

## 🚀 Getting Started

There are two ways to run this project: using Docker (recommended for a consistent production-like environment) or setting it up locally on your machine.

### Method 1: Docker Setup (Recommended)

This method handles all dependencies, services, and networking automatically.

#### Prerequisites
*   Docker
*   Docker Compose

#### Installation & Launch
1.  **Clone the Repository**
    ```bash
    git clone https://github.com/<your-username>/blog-system-bluedrive.git
    cd blog-system-bluedrive
    ```

2.  **Configure the Environment**
    Copy the example environment file. The default values are configured for the Docker Compose setup.
    ```bash
    cp .env.example .env
    ```

3.  **Build and Run with Docker Compose**
    ```bash
    docker-compose up --build -d
    ```

4.  **Apply Database Migrations** if has new changes
    ```bash
    docker-compose exec blog-system python manage.py migrate
    ```

7. **Create super user**
    ```bash
    docker-compose exec blog-system python manage.py createsuperuser
    ```


✅ **Done!** The API is now running and available at `http://127.0.0.1:8001`.

---

### Method 2: Local Python Environment Setup (Without Docker)

This method is for running the Django application directly on your host machine.

#### Prerequisites
*   Python 3.12
*   PostgreSQL installed and running on your local machine.

#### Installation & Launch
1.  **Clone the Repository**
    ```bash
    git clone https://github.com/<your-username>/blog-system-bluedrive.git
    cd blog-system-bluedrive
    ```

2.  **Create a Virtual Environment**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure the Environment**
    -   Create a database in your local PostgreSQL instance (e.g., named `blog_local_db`).
    -   Copy the example environment file: `cp .env.example .env`.
    -   **Edit the `.env` file** with your local database credentials.
        ```
        # .env (Example for local setup)
        SECRET_KEY=your_secret_key_here
        DEBUG=True
        DB_NAME=blog_local_db
        DB_USER=your_local_postgres_user
        DB_PASSWORD=your_local_postgres_password
        DB_HOST=localhost  # Or 127.0.0.1
        DB_PORT=5432
        ```

5.  **Apply Database Migrations**
    ```bash
    python manage.py migrate
    ```

6.  **Run the Development Server**
    ```bash
    python manage.py runserver
    ```

7. **Create super user**
    ```bash
    python manage.py createsuperuser
    ```

✅ **Done!** The API is now running locally at `http://127.0.0.1:8000`.


---

## 🧪 Running the Test Suite

The test suite is designed to be executed inside the Docker container to ensure it runs in a consistent environment.

```bash
# Run the full test suite
docker-compose exec blog-system pytest -s
docker-compose exec blog-system pytest -v

# Run with coverage report
docker-compose exec blog-system pytest --cov

# Run a specific test file or with arguments
docker-compose exec blog-system pytest tests/test_blog_api.py -k "delete"
```

---

## 📖 API Usage & Endpoints

The API is versioned and accessible under the `/api/v1/` prefix.

*   **Interactive Docs (Swagger UI):** `http://127.0.0.1:8001/api/docs/`
*   **Django Admin:** `http://127.0.0.1:8001/admin/`

### Example `cURL` Requests

#### List All Active Posts
```bash
curl http://127.0.0.1:8001/api/v1/posts/
```

#### Create a Post (Requires Authentication)
*First, create an author and user. Then, you would obtain a token or use session authentication.*
```bash
# This is a conceptual example. Authentication would be required.
curl -X POST http://127.0.0.1:8001/api/v1/posts/ \
     -H "Content-Type: application/json" \
     -H "Authorization: Token your_auth_token_here" \
     -d '{"title": "My New Post via cURL", "content": "This is the content."}'
```

#### Filter Posts by Author
```bash
curl "http://127.0.0.1:8001/api/v1/posts/?author_name=James%20Marco"
```

---

## 🏗️ Project Architecture

The project follows a clean, decoupled architecture to separate concerns.

```
/
├── .dockerignore
├── .env.example
├── docker-compose.yml
├── Dockerfile
├── manage.py
├── README.md
├── requirements.txt
│
├── api/                  # DRF App: Serializers, API Views, API URLs, Permissions
│   ├── permissions.py
│   ├── serializers.py
│   ├── urls.py
│   └── views.py
│
├── blog/                 # Core Django App: Models, Business Logic, Admin
│   ├── admin.py
│   ├── models.py
│   └── ...
│
├── blog_project/         # Project Configuration: Settings, Root URLs
│   ├── settings.py
│   └── urls.py
│
└── tests/                # Test Suite: Pytest fixtures and tests
    ├── conftest.py
    ├── test_api.py
    ├── test_models.py
    └── test_permissions.py
```

---

## 🌳 Git Branching and Visualization

This project follows a structured Git workflow designed for maximum clarity, stability, and collaboration. It is a phased-based model inspired by GitFlow, with a highly descriptive feature branch naming convention to ensure every branch's purpose is immediately clear.

### Branch Roles

*   `main`
    *   The production branch. Contains only stable, tagged releases.
    *   All merges into `main` are from the `mvp_phase` branch for releases. Direct commits are forbidden.

*   `mvp_phase`
    *   The primary development and integration branch for the Minimum Viable Product.
    *   This is the "next release" branch. All feature branches are merged into this branch for integration testing.

*   `phase_X/<epic-or-feature>-<specific-task>`
    *   **This is the convention for all new work.** These are short-lived branches for features, chores, bug fixes, or refactoring.
    *   **Structure:**
        *   `phase_X`: The project phase (e.g., `phase_2`, `phase_5`).
        *   `<epic-or-feature>`: The larger feature or category of work (e.g., `rest-api`, `hypercare`).
        *   `<specific-task>`: The specific, atomic action being taken (e.g., `create-post-endpoints`, `setup-ruff`).
    *   **Examples:**
    *   *   `phase_5/hypercare-documentation`
        *   `phase_5/hypercare-ruff`
    *   These branches are always created from `mvp_phase` and merged back via a Pull Request.

*   `migrations` **(Special Purpose Branch)**
    *   This branch is dedicated solely to managing Django migration files.
    *   **Purpose:** To prevent migration conflicts by centralizing all database schema changes into a single, linear history.


### Visual Representation
*This diagram illustrates the flow of branches. The text above defines the specific naming convention.*

```
      main ----------------------------------------------------o (v1.0)
         ^                                                   /
         |                                                  /
 (Release)                                                 /
         |                                                /
     mvp_phase ---o-----------o--------------------o-------o---------->
                / \         / \                  / \     /
               /   \       /   \                /   \   /
 (PR Merge)   /     \     /     \              /     \ /
             /       \   /       \            /       X
  feature/A ---o    |  /         \          /         \
                    | /           \        /           \
  feature/B --------o--------------o      /             \
                                         /               \
  feature/C ---------------------------o----------------

```
---

### Key Design Decisions
This section highlights some of the design decisions made over the assessment specifications.
*   **Defensive Validation:** In addition to DRF's built-in validators, custom validation rules are implemented at the serializer level (e.g., for comment length, unique titles) to proactively prevent invalid data.
*   **API Versioning:** The API is explicitly versioned in the URL (`/api/v1/`) to provide a stable contract for clients and allow for future non-breaking changes.
*   **Multi-Stage Docker Build:** The `Dockerfile` uses a multi-stage build to create a lean, secure production image by separating build-time dependencies from runtime requirements.
*   **Code Quality & Static Analysis:**
    *   I decided to integrate modern static analysis tools to enforce high code quality and prevent common errors before runtime.
    *   **Ruff** is used for high-performance linting and auto-formatting, ensuring a consistent and readable code style across the entire project.
    *   **Mypy** is configured for static type checking, leveraging Python's type hints to catch potential type-related bugs early in development, leading to a more robust and self-documenting codebase.
