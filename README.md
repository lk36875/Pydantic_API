# Project structure
This FastAPI project is structured to provide a web application with functionalities around managing <i>places</i> and <i>opinions</i> about those places.

## Modules Functionality

### Installation
The project uses Poetry for dependency management. To install the project dependencies, use the command:

```
poetry install --no-root
```

To create tables in the database, use the command:

```
poetry run python -m fastapi_project.db.create_tables
```

To run the FastAPI application, use the command:

```
poetry run uvicorn fastapi_project.main:app --reload
```

### Project Structure
#### Core
The core module, specifically in pydantic_core.py and sqlalchemy_core.py, defines Pydantic models for data validation and SQLAlchemy models for database interactions, respectively. These models are essential for handling the data structure of <i>places</i> and <i>opinions</i>.

#### Database (DB)
The db module contains scripts like create_db.py and create_tables.py for initializing the database and creating necessary tables.

#### Repositories
The repositories module, found in repositories.py, implements the data access layer, providing an abstraction over the database operations for <i>places</i> and <i>opinions</i>.

#### Routers
The routers module defines the API routes for <i>places</i> and <i>opinions</i>. These routes handle HTTP requests and responses, interacting with the repositories to perform CRUD operations.

#### Tests
The tests module contains unit and integration tests for API endpoints and database operations, ensuring the reliability of the application.

#### Async Routes
The project leverages asynchronous routes, as seen in the routers, to handle HTTP requests. This asynchronous approach is beneficial for IO-bound operations, such as database interactions, improving the application's performance.

#### Tests

Tests are implemented using pytest-asyncio and async-asgi-testclient. To run the tests, use the command:

```
poetry run pytest
```

#### Migrations
Migrations are managed through Alembic.
