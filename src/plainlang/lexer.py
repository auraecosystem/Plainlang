"""Tokenizer for the Plainlang 0.1 bootstrap language."""
from __future__ import annotations

from dataclasses import dataclass
import re


@dataclass(frozen=True)
class Token:
    kind: str
    value: str
    line: int
    column: int


_TOKEN_RE = re.compile(
    r"(?P<SPACE>[ \t\r]+)|(?P<NEWLINE>\n)|(?P<COMMENT>\#[^\n]*)|"
    r'(?P<STRING>"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\')|'
    r"(?P<NUMBER>\d+(?:\.\d+)?)|(?P<IDENT>[A-Za-z_][A-Za-z0-9_]*)|"
    r"(?P<OP>->|==|!=|<=|>=|[+*/%=<>-])|(?P<PUNCT>[(){},;])"
)


class LexError(SyntaxError):
    """Raised when source contains an unknown character or malformed token."""


def tokenize(source: str) -> list[Token]:
    tokens: list[Token] = []
    line = column = 1
    position = 0
    while position < len(source):
        match = _TOKEN_RE.match(source, position)
        if not match:
            char = source[position]
            raise LexError(f"Unexpected character {char!r} at {line}:{column}")
        kind = match.lastgroup or ""
        value = match.group()
        if kind not in {"SPACE", "COMMENT"}:
            tokens.append(Token(kind, value, line, column))
        newlines = value.count("\n")
        if newlines:
            line += newlines
            column = len(value.rsplit("\n", 1)[-1]) + 1
        else:
            column += len(value)
        position = match.end()
    tokens.append(Token("EOF", "", line, column))
    return tokens
