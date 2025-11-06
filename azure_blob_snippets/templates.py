"""High level template operations backed by Azure Blob Storage."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import List, Sequence

from azure.storage.blob import ContainerClient

from .storage import TEMPLATES_ROOT, get_container_client


@dataclass
class Manifest:
    """Represents metadata describing a template directory."""

    id: str
    name: str
    version: str
    description: str
    prefix: str


def create_demo_templates(container: ContainerClient | None = None) -> None:
    """Seed storage with three demo templates under 'templates/'."""
    container = container or get_container_client()

    for idx in range(1, 4):
        prefix = f"{TEMPLATES_ROOT}tpl-{idx:02d}/"
        manifest = {
            "id": f"tpl-{idx:02d}",
            "name": f"Sample Template {idx}",
            "version": "1.0.0",
            "description": "Demo manifest for selection workflow",
        }
        template_text = (
            "This is a demo template.\n"
            "Bla-bla-bla placeholder line 2.\n"
            "Bla-bla-bla placeholder line 3.\n"
            "Bla-bla-bla placeholder line 4.\n"
        )

        container.upload_blob(
            name=prefix + "manifest.json",
            data=json.dumps(manifest, indent=2).encode("utf-8"),
            overwrite=True,
        )
        container.upload_blob(
            name=prefix + "template.md",
            data=template_text.encode("utf-8"),
            overwrite=True,
        )


def discover_manifests(container: ContainerClient | None = None) -> List[Manifest]:
    """Return all manifests under the templates root."""
    container = container or get_container_client()
    manifests: List[Manifest] = []

    for blob in container.list_blobs(name_starts_with=TEMPLATES_ROOT):
        if not blob.name.endswith("/manifest.json"):
            continue
        blob_bytes = container.download_blob(blob.name).readall()
        data = json.loads(blob_bytes.decode("utf-8"))
        prefix = blob.name.removesuffix("manifest.json")
        manifests.append(
            Manifest(
                id=data.get("id", ""),
                name=data.get("name", ""),
                version=data.get("version", ""),
                description=data.get("description", ""),
                prefix=prefix,
            )
        )

    manifests.sort(key=lambda item: item.id)
    return manifests


def format_manifest_list(manifests: Sequence[Manifest]) -> str:
    """Render manifests into a printable list."""
    lines = ["Available templates:"]
    for idx, manifest in enumerate(manifests, 1):
        lines.append(
            f"  {idx}. {manifest.name} "
            f"(id={manifest.id}, version={manifest.version})"
        )
    return "\n".join(lines)


def choose_manifest(manifests: Sequence[Manifest]) -> Manifest | None:
    """Prompt the user to choose a manifest from the given list."""
    if not manifests:
        print("No templates found.")
        return None

    print(format_manifest_list(manifests))
    upper_bound = len(manifests)

    while True:
        raw = input(f"Enter a template number [1..{upper_bound}]: ").strip()
        if raw.isdigit():
            value = int(raw)
            if 1 <= value <= upper_bound:
                return manifests[value - 1]
        print("Invalid selection. Try again.")


def load_template_text(prefix: str, container: ContainerClient | None = None) -> str:
    """Download the selected template.md content."""
    container = container or get_container_client()
    blob_name = prefix + "template.md"
    data = container.download_blob(blob_name).readall()
    return data.decode("utf-8")

