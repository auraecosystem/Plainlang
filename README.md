# Plainlang

**Plainlang is an experimental programming-language ecosystem combining a formal language, natural-language programming, hybrid source, and plain-language documentation.**

The repository currently contains an existing Jekyll website in its original root layout. That site is preserved. The new language implementation is being introduced alongside it, beginning with a dependency-free Python bootstrap interpreter so that syntax and runtime behavior can be exercised before a production compiler and VM are selected and stabilized.

## Project status

Plainlang is pre-alpha. The 0.1 bootstrap supports variables, numeric and string literals, arithmetic, comparisons, functions, returns, and basic built-ins (`print`, `str`, `len`). It is an interpreter prototype, not yet a production compiler, bytecode VM, static type checker, or natural-language execution engine.

## Quick start

Requires Python 3.11 or newer. From the repository root:

```bash
PYTHONPATH=src python -m plainlang check examples/hello.pln
PYTHONPATH=src python -m plainlang run examples/hello.pln
PYTHONPATH=src python -m unittest discover -s tests -v
```

Install locally with `python -m pip install -e .`, then use `plainlang check` or `plainlang run`.

## Language example

```plainlang
function greet(name) {
    return "Hello, " + name
}

let message = greet("Plainlang")
print(message)
```

## Architecture

- `src/plainlang/lexer.py` — tokenization.
- `src/plainlang/parser.py` — recursive-descent parser and AST.
- `src/plainlang/runtime.py` — explicit interpreter; no `eval` or dynamic code execution.
- `src/plainlang/cli.py` — command-line interface.
- `language/` and `docs/` — language grammar, specification, architecture and roadmap.
- Existing Jekyll website files remain in place and are not part of the interpreter package.

## Design principles

1. Formal Plainlang source has deterministic, specified semantics.
2. Natural-language instructions are proposed inputs, not executable authority.
3. AI-generated code must be inspectable, parsed, validated and authorized before execution.
4. Hybrid source keeps explanatory text distinct from executable constructs.
5. The compiler, runtime and documentation tools share stable language definitions and semantic metadata.
6. External side effects require explicit capabilities and authorization.

## Roadmap

See [the language specification](docs/LANGUAGE_SPEC.md), [architecture](docs/ARCHITECTURE.md), and [roadmap](docs/ROADMAP.md). The current bootstrap is intentionally small; type checking, bytecode, sandboxing, language-server support, natural-language translation and the documentation platform are future milestones.

## Existing website

`README.mkdn`, the Jekyll configuration, website content, assets, Ruby dependencies, and existing CI are retained. The legacy website's original documentation and license are not silently rewritten by this language bootstrap.

## Contributing

Contributions should include tests for behavior changes and update the language specification when syntax or semantics change. Do not treat an undocumented parser behavior as a language guarantee.
