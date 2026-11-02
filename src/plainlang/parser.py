"""Recursive-descent parser for the Plainlang 0.1 bootstrap language."""
from __future__ import annotations

from dataclasses import dataclass
import ast as py_ast

from .lexer import Token, tokenize


@dataclass
class Literal:
    value: object


@dataclass
class Name:
    value: str


@dataclass
class Binary:
    left: object
    operator: str
    right: object


@dataclass
class Unary:
    operator: str
    operand: object


@dataclass
class Call:
    callee: object
    arguments: list[object]


@dataclass
class Let:
    name: str
    value: object


@dataclass
class ExpressionStatement:
    expression: object


@dataclass
class Return:
    value: object | None


@dataclass
class Function:
    name: str
    parameters: list[str]
    body: list[object]


@dataclass
class Program:
    statements: list[object]


class ParseError(SyntaxError):
    pass


class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.current = 0

    def parse(self) -> Program:
        statements = []
        self._separators()
        while not self._check("EOF"):
            statements.append(self._declaration())
            self._separators()
        return Program(statements)

    def _declaration(self):
        if self._match_ident("function", "fn"):
            return self._function()
        if self._match_ident("let"):
            name = self._consume("IDENT", "Expected a variable name")
            self._consume_value("=", "Expected '=' after variable name")
            return Let(name.value, self._expression())
        return self._statement()

    def _function(self):
        name = self._consume("IDENT", "Expected a function name")
        self._consume_value("(", "Expected '(' after function name")
        parameters = []
        if not self._check_value(")"):
            while True:
                parameters.append(self._consume("IDENT", "Expected parameter name").value)
                if not self._match_value(","):
                    break
        self._consume_value(")", "Expected ')' after parameters")
        self._consume_value("{", "Expected '{' before function body")
        body = self._block()
        return Function(name.value, parameters, body)

    def _block(self):
        statements = []
        self._separators()
        while not self._check_value("}") and not self._check("EOF"):
            statements.append(self._declaration())
            self._separators()
        self._consume_value("}", "Expected '}' after function body")
        return statements

    def _statement(self):
        if self._match_ident("return"):
            if self._check("EOF") or self._check_value("}") or self._check("NEWLINE") or self._check_value(";"):
                return Return(None)
            return Return(self._expression())
        return ExpressionStatement(self._expression())

    def _expression(self):
        return self._equality()

    def _equality(self):
        expr = self._comparison()
        while self._match_value("==", "!="):
            op = self._previous().value
            expr = Binary(expr, op, self._comparison())
        return expr

    def _comparison(self):
        expr = self._term()
        while self._match_value(">", ">=", "<", "<="):
            op = self._previous().value
            expr = Binary(expr, op, self._term())
        return expr

    def _term(self):
        expr = self._factor()
        while self._match_value("+", "-"):
            op = self._previous().value
            expr = Binary(expr, op, self._factor())
        return expr

    def _factor(self):
        expr = self._unary()
        while self._match_value("*", "/", "%"):
            op = self._previous().value
            expr = Binary(expr, op, self._unary())
        return expr

    def _unary(self):
        if self._match_value("-"):
            return Unary("-", self._unary())
        return self._call()

    def _call(self):
        expr = self._primary()
        while self._match_value("("):
            args = []
            if not self._check_value(")"):
                while True:
                    args.append(self._expression())
                    if not self._match_value(","):
                        break
            self._consume_value(")", "Expected ')' after arguments")
            expr = Call(expr, args)
        return expr

    def _primary(self):
        if self._match("NUMBER"):
            raw = self._previous().value
            return Literal(float(raw) if "." in raw else int(raw))
        if self._match("STRING"):
            return Literal(py_ast.literal_eval(self._previous().value))
        if self._match_ident("true"):
            return Literal(True)
        if self._match_ident("false"):
            return Literal(False)
        if self._match_ident("none"):
            return Literal(None)
        if self._match("IDENT"):
            return Name(self._previous().value)
        if self._match_value("("):
            expr = self._expression()
            self._consume_value(")", "Expected ')' after expression")
            return expr
        token = self._peek()
        raise ParseError(f"Expected an expression at {token.line}:{token.column}")

    def _separators(self):
        while self._match("NEWLINE") or self._match_value(";"):
            pass

    def _match_ident(self, *values):
        if self._check("IDENT") and self._peek().value in values:
            self.current += 1
            return True
        return False

    def _match_value(self, *values):
        if self._peek().value in values:
            self.current += 1
            return True
        return False

    def _match(self, kind):
        if self._check(kind):
            self.current += 1
            return True
        return False

    def _check(self, kind):
        return self._peek().kind == kind

    def _check_value(self, value):
        return self._peek().value == value

    def _consume(self, kind, message):
        if self._check(kind):
            self.current += 1
            return self._previous()
        token = self._peek()
        raise ParseError(f"{message} at {token.line}:{token.column}")

    def _consume_value(self, value, message):
        if self._match_value(value):
            return self._previous()
        token = self._peek()
        raise ParseError(f"{message} at {token.line}:{token.column}")

    def _peek(self):
        return self.tokens[self.current]

    def _previous(self):
        return self.tokens[self.current - 1]


def parse(source: str) -> Program:
    return Parser(tokenize(source)).parse()
