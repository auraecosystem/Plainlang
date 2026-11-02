# Plainlang roadmap

## 0.1 — executable language bootstrap

- [x] Tokenizer and source locations.
- [x] Recursive-descent parser and AST.
- [x] Variables, functions, returns and expressions.
- [x] Small interpreter and CLI.
- [x] Standard-library-free unit tests.
- [x] Initial grammar and language specification.
- [ ] Broader conformance suite and release review.

## 0.2 — language semantics

- Specify static and dynamic type strategy.
- Specify scope, mutability, equality, numeric precision and error semantics.
- Add assignment, conditional expressions/statements and loops only after their semantics are specified.
- Add source spans to AST nodes and structured diagnostics.
- Add deterministic serialization for the semantic representation.

## 0.3 — compiler and runtime

- Introduce a typed intermediate representation.
- Add bytecode format and VM evaluation strategy.
- Define memory, resource and cancellation limits.
- Add module/package resolution and reproducible builds.
- Establish cross-implementation conformance tests.

## 0.4 — developer tooling

- Formatter, language server protocol implementation and editor support.
- Debugger hooks, stack traces and structured runtime inspection.
- Package and dependency integrity model.

## 0.5 — natural-language and hybrid programming

- Intent schema and translation interface.
- Generate inspectable formal source with source-to-intent provenance.
- Require parse, semantic and policy validation before execution.
- Clarify ambiguous instructions instead of guessing.
- Add explicitly delimited explanatory blocks to hybrid source.

## 0.6 — documentation platform

- Generate reference documentation from language metadata and semantic IR.
- Add plain-language explanations, linting and versioned publishing.
- Add safe, resource-limited runnable examples.

## 1.0 — production readiness

- Stable language specification and compatibility policy.
- Security review, sandboxing and capability model.
- Performance, portability and conformance benchmarks.
- Reproducible builds, signed releases and migration documentation.
