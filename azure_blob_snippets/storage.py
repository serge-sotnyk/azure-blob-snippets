"""Connection helpers for Azure Blob Storage."""

import os

from azure.core.exceptions import ResourceExistsError
from azure.storage.blob import BlobServiceClient, ContainerClient
from dotenv import load_dotenv

CONTAINER_NAME = "demo"
TEMPLATES_ROOT = "templates/"

# Load environment variables from .env if present.
load_dotenv()


def _connection_string() -> str:
    """Return the storage connection string, falling back to Azurite default."""
    standard = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    if standard:
        return standard
    alternative = os.getenv("MDX_AZURE_STORAGE_CONNECTION_STRING")
    if alternative:
        return alternative
    return "UseDevelopmentStorage=true"


def get_container_client() -> ContainerClient:
    """Return a container client, creating the container if it does not exist."""
    service = BlobServiceClient.from_connection_string(_connection_string())
    container = service.get_container_client(CONTAINER_NAME)
    try:
        container.create_container()
    except ResourceExistsError:
        pass
    return container

