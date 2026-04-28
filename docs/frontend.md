# Frontend

The frontend lives in `app/front/` and is implemented with Streamlit.

## Main Files

- `app/front/main.py`: main Streamlit entrypoint.
- `app/front/pages/`: Streamlit pages.
- `app/front/bandit_utils.py`: shared frontend utilities.

## Pages

- Create carousels.
- Record or simulate interactions.
- View analytics.

The frontend should communicate with the backend API instead of accessing the database directly.

## API Reference

### Main

**Module:** `app.front.main`

Defines the main Streamlit application entrypoint.

::: app.front.main

### Bandit Utilities

**Module:** `app.front.bandit_utils`

Contains shared utility functions for bandit-related frontend behavior.

::: app.front.bandit_utils

## Pages

### Analytics

**Module:** `app.front.pages.Analytics`

Defines the Streamlit analytics page.

::: app.front.pages.Analytics

### Create Carousels

**Module:** `app.front.pages.Create_Carousels`

Defines the Streamlit page for creating carousels.

::: app.front.pages.Create_Carousels

### Interaction

**Module:** `app.front.pages.Interaction`

Defines the Streamlit page for recording or simulating interactions.

::: app.front.pages.Interaction
