# Deployment

The repository uses GitHub Actions to publish a combined GitHub Pages site.

## MkDocs

MkDocs uses `docs/` as its source directory and publishes to the root of the Pages site.

## Quarto

Quarto uses `tutorial/` as its source directory and renders into `tutorial/docs/`.

During deployment, the workflow copies `tutorial/docs/` into the final site under `/tutorial/`.

## Live URLs

- MkDocs: `https://hovhannisyan91.github.io/DS223_Group_Project/`
- Quarto tutorial: `https://hovhannisyan91.github.io/DS223_Group_Project/tutorial/`

