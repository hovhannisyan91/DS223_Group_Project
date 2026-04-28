# DS223 Group Project

This documentation describes the project repository, application components, and deployment workflow.

The Quarto course tutorial is maintained separately under `tutorial/` and is published at:

[Open tutorial](tutorial/)

## Repository Layout

- `app/backend/`: FastAPI service and database API.
- `app/front/`: Streamlit frontend.
- `app/etl/`: database setup and ETL utilities.
- `app/ds/`: data science module.
- `docs/`: MkDocs documentation source.
- `tutorial/`: Quarto tutorial source.

## Deployment

GitHub Actions builds two outputs:

- MkDocs from `docs/` to the site root.
- Quarto from `tutorial/` to `/tutorial/`.

