"""Command line interface for the Azure Blob template snippets."""

from __future__ import annotations

import argparse
from typing import Any, Sequence

from .templates import (
    Manifest,
    choose_manifest,
    create_demo_templates,
    discover_manifests,
    format_manifest_list,
    load_template_text,
)


def _seed_command(_args: argparse.Namespace) -> None:
    create_demo_templates()
    print("Created demo templates under container 'demo/templates/'.")


def _list_command(_args: argparse.Namespace) -> None:
    manifests = discover_manifests()
    if not manifests:
        print("No templates found.")
        return
    print(format_manifest_list(manifests))


def _show_command(args: argparse.Namespace) -> None:
    manifests = discover_manifests()
    if not manifests:
        print("No templates found.")
        return

    selected: Manifest | None = None
    if args.id:
        selected = next((item for item in manifests if item.id == args.id), None)
        if not selected:
            print(f"Template with id '{args.id}' not found.")
            return
    else:
        selected = choose_manifest(manifests)
        if not selected:
            return

    template_text = load_template_text(selected.prefix)
    blob_name = f"{selected.prefix}template.md"
    divider = "=" * 40
    print(f"\n{divider}\nTemplate: {blob_name}\n{divider}\n")
    print(template_text)


def _add_seed_parser(subparsers: argparse._SubParsersAction[Any]) -> None:
    parser = subparsers.add_parser(
        "seed",
        help="Create three demo templates under the 'demo/templates/' prefix.",
    )
    parser.set_defaults(func=_seed_command)


def _add_list_parser(subparsers: argparse._SubParsersAction[Any]) -> None:
    parser = subparsers.add_parser(
        "list", help="List available template manifests in storage."
    )
    parser.set_defaults(func=_list_command)


def _add_show_parser(subparsers: argparse._SubParsersAction[Any]) -> None:
    parser = subparsers.add_parser(
        "show",
        help="Display a template's markdown file, optionally by specifying an id.",
    )
    parser.add_argument(
        "--id",
        dest="id",
        help="Manifest id to load directly. If omitted, an interactive prompt is used.",
    )
    parser.set_defaults(func=_show_command)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m azure_blob_snippets.cli",
        description="Work with demo templates stored in Azure Blob Storage.",
    )
    subparsers = parser.add_subparsers(dest="command")
    _add_seed_parser(subparsers)
    _add_list_parser(subparsers)
    _add_show_parser(subparsers)
    return parser


def main(argv: Sequence[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    command = getattr(args, "func", None)
    if not command:
        parser.print_help()
        return
    command(args)


if __name__ == "__main__":
    main()

