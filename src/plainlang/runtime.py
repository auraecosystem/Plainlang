"""Small, explicit interpreter for the Plainlang 0.1 language subset."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from .parser import Binary, Call, ExpressionStatement, Function, Let, Literal, Name, Program, Return, Unary, parse


class PlainlangRuntimeError(RuntimeError):
    pass


@dataclass
class UserFunction:
    declaration: Function
    closure: dict[str, object]


class _ReturnSignal(Exception):
    def __init__(self, value):
        self.value = value


class Interpreter:
    def __init__(self, output: Callable[..., None] = print):
        self.output = output
        self.globals: dict[str, object] = {"print": self._print, "str": str, "len": len}
        self.environment = self.globals
        self.call_depth = 0

    def run(self, program: Program):
        result = None
        for statement in program.statements:
            result = self._execute(statement)
        return result

    def _execute(self, node):
        if isinstance(node, Let):
            self.environment[node.name] = self._evaluate(node.value)
            return self.environment[node.name]
        if isinstance(node, ExpressionStatement):
            return self._evaluate(node.expression)
        if isinstance(node, Function):
            if node.name in self.environment:
                raise PlainlangRuntimeError(f"Name already defined: {node.name}")
            self.environment[node.name] = UserFunction(node, self.environment.copy())
            return None
        if isinstance(node, Return):
            raise _ReturnSignal(None if node.value is None else self._evaluate(node.value))
        raise PlainlangRuntimeError(f"Unsupported statement: {type(node).__name__}")

    def _evaluate(self, node):
        if isinstance(node, Literal):
            return node.value
        if isinstance(node, Name):
            if node.value not in self.environment:
                raise PlainlangRuntimeError(f"Undefined name: {node.value}")
            return self.environment[node.value]
        if isinstance(node, Unary):
            value = self._evaluate(node.operand)
            if node.operator == "-" and isinstance(value, (int, float)) and not isinstance(value, bool):
                return -value
            raise PlainlangRuntimeError(f"Unary '-' requires a number, got {type(value).__name__}")
        if isinstance(node, Binary):
            left, right = self._evaluate(node.left), self._evaluate(node.right)
            try:
                operations = {
                    "+": lambda: left + right, "-": lambda: left - right,
                    "*": lambda: left * right, "/": lambda: left / right,
                    "%": lambda: left % right, "==": lambda: left == right,
                    "!=": lambda: left != right, ">": lambda: left > right,
                    ">=": lambda: left >= right, "<": lambda: left < right,
                    "<=": lambda: left <= right,
                }
                return operations[node.operator]()
            except (TypeError, ZeroDivisionError) as exc:
                raise PlainlangRuntimeError(f"Invalid operation '{node.operator}': {exc}") from exc
        if isinstance(node, Call):
            callee = self._evaluate(node.callee)
            args = [self._evaluate(arg) for arg in node.arguments]
            if isinstance(callee, UserFunction):
                declaration = callee.declaration
                if len(args) != len(declaration.parameters):
                    raise PlainlangRuntimeError(
                        f"{declaration.name} expects {len(declaration.parameters)} arguments, got {len(args)}"
                    )
                if self.call_depth >= 128:
                    raise PlainlangRuntimeError("Maximum function call depth exceeded (128)")
                previous = self.environment
                local = callee.closure.copy()
                local.update(zip(declaration.parameters, args))
                self.environment = local
                self.call_depth += 1
                try:
                    for statement in declaration.body:
                        self._execute(statement)
                except _ReturnSignal as signal:
                    return signal.value
                finally:
                    self.call_depth -= 1
                    self.environment = previous
                return None
            if callable(callee):
                try:
                    return callee(*args)
                except (TypeError, ValueError) as exc:
                    raise PlainlangRuntimeError(f"Builtin call failed: {exc}") from exc
            raise PlainlangRuntimeError("Attempted to call a value that is not a function")
        raise PlainlangRuntimeError(f"Unsupported expression: {type(node).__name__}")

    def _print(self, *values):
        self.output(*values)
        return None


def execute(source: str, output: Callable[..., None] = print):
    return Interpreter(output=output).run(parse(source))
