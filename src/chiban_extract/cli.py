"""Command-line interface.

    chiban-extract extract <pdf-or-url> [--property-name N] [--known-address A] [--json]

Exit codes: 0 = success, 1 = nothing found, 2 = input/usage error.
"""

from __future__ import annotations

import argparse
import json
import sys

from .pdf import read_pdf
from .pipeline import extract_from_text


def _print_json(obj: dict) -> None:
    print(json.dumps(obj, ensure_ascii=False, indent=2))


def _cmd_extract(args: argparse.Namespace) -> int:
    try:
        doc = read_pdf(args.source)
    except Exception as e:
        print(f"error: could not read PDF: {e}", file=sys.stderr)
        return 2
    result = extract_from_text(
        doc.text,
        page_count=doc.page_count,
        property_name=args.property_name,
        known_address=args.known_address,
        other_property_names=args.other_property or None,
    )
    if args.json:
        _print_json(result.to_dict())
    else:
        if result.best:
            print(f"best: {result.best.address} [{result.best.kind.value}]")
        else:
            print("best: (none)")
        for c in result.candidates[:10]:
            marker = "*" if result.best and c.address == result.best.address else " "
            print(f"  {marker} {c.address} [{c.kind.value}]"
                  f"{' (near keyword)' if c.near_keyword else ''}")
        for w in result.warnings:
            print(f"warning: {w}", file=sys.stderr)
    return 0 if result.best else 1


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="chiban-extract",
        description="Extract Japanese addresses and land lot numbers (chiban) from PDFs",
    )
    sub = p.add_subparsers(dest="command", required=True)

    pe = sub.add_parser("extract", help="extract addresses from a PDF (path or URL)")
    pe.add_argument("source", help="PDF file path or http(s) URL")
    pe.add_argument("--property-name", help="scope extraction near this property name")
    pe.add_argument("--known-address", help="validate candidates against this known address")
    pe.add_argument("--other-property", action="append", default=[],
                    help="other property names in the same document (repeatable)")
    pe.add_argument("--json", action="store_true", help="output JSON")
    pe.set_defaults(func=_cmd_extract)

    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
