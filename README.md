# Django PostgreSQL Base

## Description

This project is a base implementation for building Django applications with PostgreSQL as the database. It provides a robust foundation for developing scalable and maintainable web applications, integrating essential tools and features such as Celery for task management, Redis for caching, and HTMX for UI enhancements.

Goal of this project id to have a start point for future projects as well learn and apply new technologies. Not everything here is the prefered way of working, but can lead to a nice learning.

---

## How to Install

1. **Prerequisites**

    - [Docker engine](https://docs.docker.com/engine/install/)
    - [uv](https://docs.astral.sh/uv/getting-started/installation/)

2. **Clone the Repository**:

   ```bash
   git clone https://github.com/vitorsmonteiro/django_postgresql_base.git
   cd django_postgresql_base

3. **Setup a virtual environmnet:**

    ```bash
    uv sync
    source .venv/bin/activate
    ```

4. **Set up environment variables:**
    Create a `.env.dev` file in the root directory.
    Add the necessary environment variables (e.g., DB_HOST, DB_USER, DB_PASSWORD, REDIS_HOST, etc.). Follow the provided `.env` file.

5. **Run docker**

    ```bash
    docker compose up -d --build
    ```

6. **Run mdabase**

    ```bash
    docker compose exec web python manage.py migrate
    ```

## Used Technologies

- Backend: [Django](https://www.djangoproject.com/)
- Database: [PostgreSQL](https://www.postgresql.org/)
- Rest API: [Django ninja](https://django-ninja.dev/)
- Task Queue: [Celery](https://docs.celeryq.dev/en/stable/index.html)
- Cache: [Redis](https://redis.io/)
- Frontend:
  - [Fontawesome](https://fontawesome.com/)
  - [Bootstrap](https://getbootstrap.com/)
  - [HTMX](https://htmx.org/)
- Containerization: [Docker](https://www.docker.com/)
- Testing: [Pytest](https://docs.pytest.org/en/stable/)
- Linting:
  - [Ruff](https://docs.astral.sh/ruff/#testimonials)
  - [djlint](https://djlint.com/)
  - [mypy](https://mypy.readthedocs.io/en/stable/index.html)
- Package management: [uv](https://docs.astral.sh/uv/getting-started/installation/)

## Current Features

- User authentication and management
- Blog functionality with posts, topics, and comments
- Task management with a to-do list
- Asynchronous task handling with Celery
- Caching with Redis
- Pagination for large datasets
- Admin interface for managing models

## License

This project is licensed under the terms of the MIT license.
