# ETL

The ETL code lives in `app/etl/`.

## Main Files

- `app/etl/etl.py`: ETL logic.
- `app/etl/create_tables.py`: table creation workflow.
- `app/etl/Database/`: database models and connection helpers.

## Purpose

The ETL layer prepares data for the application database and keeps database setup logic separate from the backend API.

## API Reference

### ETL Pipeline

**Module:** `app.etl.etl`

Contains the main ETL workflow logic.

::: app.etl.etl

### Table Creation

**Module:** `app.etl.create_tables`

Creates database tables from the SQLAlchemy model metadata.

::: app.etl.create_tables

### Database

**Module:** `app.etl.Database.database`

Configures database connectivity for the ETL layer.

::: app.etl.Database.database

### Models

**Module:** `app.etl.Database.models`

Defines SQLAlchemy models used by the ETL layer.

::: app.etl.Database.models
