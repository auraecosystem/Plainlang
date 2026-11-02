"""Command-line interface for the Plainlang bootstrap interpreter."""
from __future__ import annotations

import argparse
from pathlib import Path
import sys

from .lexer import tokenize
from .parser import parse
from .runtime import Interpreter


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="plainlang", description="Plainlang language bootstrap tool")
    parser.add_argument("command", choices=("check", "run", "tokens"), help="operation to perform")
    parser.add_argument("source", type=Path, help="Plainlang source file (.pln)")
    parser.add_argument("--version", action="version", version="plainlang 0.1.0-dev")
    args = parser.parse_args(argv)
    try:
        source = args.source.read_text(encoding="utf-8")
        if args.command == "tokens":
            for token in tokenize(source):
                print(f"{token.line}:{token.column}\t{token.kind}\t{token.value}")
        elif args.command == "check":
            parse(source)
            print(f"OK: {args.source} parsed successfully")
        else:
            Interpreter().run(parse(source))
        return 0
    except (OSError, SyntaxError, RuntimeError) as exc:
        print(f"plainlang: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
