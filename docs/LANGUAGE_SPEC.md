# Plainlang language specification — 0.1 draft

**Status:** bootstrap draft; syntax may change before 1.0.

## Goals

Plainlang aims to make programs readable without sacrificing explicit, testable semantics. Formal source is authoritative for execution. Natural-language and explanatory source are separate language layers that must be translated into validated formal constructs before execution.

## Source files

The proposed source extension is `.pln`. A source file is UTF-8 text. `#` begins a line comment. Statements are separated by newlines or semicolons; braces delimit function bodies.

## Declarations

```plainlang
let count = 3

function add(left, right) {
    return left + right
}
```

`fn` is accepted as an alias for `function`. Parameters are positional. Function declarations are available in the environment where they are declared. The bootstrap interpreter currently uses dynamically typed values; static type declarations are reserved for a later specification.

## Values and expressions

The bootstrap supports integers, floating-point numbers, strings, booleans (`true`, `false`), and `none`. Parentheses group expressions. Operators, from lower to higher precedence:

1. `==`, `!=`
2. `>`, `>=`, `<`, `<=`
3. `+`, `-`
4. `*`, `/`, `%`
5. unary `-`
6. function calls

Arithmetic follows Python's numeric behavior where applicable; division by zero and incompatible operands produce Plainlang runtime errors. This compatibility is an implementation detail to be replaced by fully specified language semantics before 1.0.

## Statements

- `let name = expression` binds a name in the current environment.
- `function name(parameters) { ... }` declares a function.
- `return expression` returns from the current function; bare `return` returns `none`.
- An expression may appear as a statement.

## Built-ins

- `print(value, ...)` writes values to the configured output sink.
- `str(value)` converts a value to text.
- `len(value)` returns the length of a supported value.

## Errors

Lexical and parse errors include source line and column where available. Runtime errors identify undefined names, invalid operations, incorrect function arity, and excessive call depth.

## Explicit non-goals for 0.1

No loops, imports, classes, static type system, network access, filesystem APIs, concurrency, macros, bytecode, optimizer, or implicit natural-language execution are implemented in this bootstrap.
