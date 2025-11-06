## Azure Blob Snippets

CLI utilities that work with demo templates stored in Azure Blob Storage (Azurite by default).

### Prerequisites

- Python 3.13 or newer.
- [uv](https://github.com/astral-sh/uv) installed globally.
- Docker (optional, for running Azurite locally).

### Setup

1. Create a local environment file:
   ```bash
   cp .env-example .env
   ```
   Update `AZURE_STORAGE_CONNECTION_STRING` if you want to use a real storage account instead of Azurite.
2. Install dependencies with uv:
   ```bash
   uv sync
   ```

### Running Azurite with Docker

```bash
docker run -d --name azurite-blob \
  -p 10000:10000 \
  -v "C:\work\azurite:/data" \
  mcr.microsoft.com/azure-storage/azurite \
  azurite-blob --blobHost 0.0.0.0 --blobPort 10000 --location /data
```

When Azurite is running the default connection string `UseDevelopmentStorage=true` works out of the box.

### Commands

The utility is exposed as a module. Use uv (or python) to run the entrypoint:

```bash
uv run python -m azure_blob_snippets.cli seed  # create demo data
uv run python -m azure_blob_snippets.cli list  # list manifests
uv run python -m azure_blob_snippets.cli show  # pick and show a template
```

- `seed` uploads three demo folders under `demo/templates/`.
- `list` prints available manifests with their ids.
- `show` prompts for a template (or accepts `--id tpl-01`) and prints its `template.md`.
