# Backend

The backend service lives in `app/backend/` and exposes the API used by the project application.

## Main Modules

- `app/backend/main.py`: FastAPI application entrypoint.
- `app/backend/routes/`: API route definitions.
- `app/backend/db/`: database connection, models, schemas, and CRUD helpers.

## Local Development

Install the backend dependencies from `app/backend/pyproject.toml`, then run the FastAPI application from the backend module.

The backend should be treated as the contract between the database layer and the frontend application.

## API Reference

### Main

**Module:** `app.backend.main`

Creates the FastAPI application and registers the backend routers.

::: app.backend.main

### Database

**Module:** `app.backend.db.database`

Configures the SQLAlchemy engine, session factory, declarative base, and database-session dependency.

::: app.backend.db.database

### Models

**Module:** `app.backend.db.models`

Defines the backend SQLAlchemy ORM models for carousels, alternatives, and interactions.

::: app.backend.db.models

### Schemas

**Module:** `app.backend.db.schemas`

Defines Pydantic schemas used by backend route handlers for validation and serialization.

::: app.backend.db.schemas

### CRUD

**Module:** `app.backend.db.crud`

Contains database helper functions used by backend routes.

::: app.backend.db.crud

## Routes

### Carousels

**Module:** `app.backend.routes.carousels`

Defines endpoints for creating, reading, and managing carousels.

::: app.backend.routes.carousels

### Interactions

**Module:** `app.backend.routes.interactions`

Defines endpoints for recording and processing carousel interaction events.

::: app.backend.routes.interactions

### System

**Module:** `app.backend.routes.system`

Defines system-level endpoints such as health checks.

::: app.backend.routes.system
