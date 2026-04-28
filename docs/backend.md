# Backend

The backend service lives in `app/backend/` and exposes the API used by the project application.

## Main Modules

- `app/backend/main.py`: FastAPI application entrypoint.
- `app/backend/routes/`: API route definitions.
- `app/backend/db/`: database connection, models, schemas, and CRUD helpers.

## Local Development

Install the backend dependencies from `app/backend/pyproject.toml`, then run the FastAPI application from the backend module.

The backend should be treated as the contract between the database layer and the frontend application.

