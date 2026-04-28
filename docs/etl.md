# ETL

The ETL code lives in `app/etl/`.

## Main Files

- `app/etl/etl.py`: ETL logic.
- `app/etl/create_tables.py`: table creation workflow.
- `app/etl/Database/`: database models and connection helpers.

## Purpose

The ETL layer prepares data for the application database and keeps database setup logic separate from the backend API.

## API Reference

::: app.etl.etl
