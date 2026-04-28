# API Reference

This page documents the project Python modules with `mkdocstrings`.

## Backend

Backend modules define the FastAPI application, API routes, database models, request/response schemas, and database access helpers.

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

## Backend Routes

Route modules define HTTP endpoints exposed by the FastAPI backend.

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

## ETL

ETL modules prepare and load data used by the application database.

### ETL Pipeline

**Module:** `app.etl.etl`

Contains the main ETL workflow logic.

::: app.etl.etl

### Table Creation

**Module:** `app.etl.create_tables`

Creates database tables from the SQLAlchemy model metadata.

::: app.etl.create_tables

### ETL Database

**Module:** `app.etl.Database.database`

Configures database connectivity for the ETL layer.

::: app.etl.Database.database

### ETL Models

**Module:** `app.etl.Database.models`

Defines SQLAlchemy models used by the ETL layer.

::: app.etl.Database.models

## Frontend

Frontend modules implement the Streamlit application and shared UI logic.

### Main

**Module:** `app.front.main`

Defines the main Streamlit application entrypoint.

::: app.front.main

### Bandit Utilities

**Module:** `app.front.bandit_utils`

Contains shared utility functions for bandit-related frontend behavior.

::: app.front.bandit_utils

### Analytics Page

**Module:** `app.front.pages.Analytics`

Defines the Streamlit analytics page.

::: app.front.pages.Analytics

### Create Carousels Page

**Module:** `app.front.pages.Create_Carousels`

Defines the Streamlit page for creating carousels.

::: app.front.pages.Create_Carousels

### Interaction Page

**Module:** `app.front.pages.Interaction`

Defines the Streamlit page for recording or simulating interactions.

::: app.front.pages.Interaction

## Data Science

Data science modules contain modeling or decision logic used by the project.

### Main

**Module:** `app.ds.main`

Defines the data science module entrypoint.

::: app.ds.main
