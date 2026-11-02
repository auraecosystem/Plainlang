# Plainlang architecture

## Current bootstrap

The 0.1 bootstrap is a small Python implementation intended to validate language design quickly:

```text
.pln source -> lexer -> tokens -> recursive-descent parser -> AST -> interpreter -> output
```

The interpreter has an explicit AST evaluator. It does not use Python `eval`, `exec`, shell execution, or dynamic module loading. Built-ins are deliberately allowlisted. This is a language prototype, not a hardened hostile-code sandbox.

## Target architecture

```text
Formal source ---------> compiler frontend ----┐
Natural-language input -> intent/translation ---+--> semantic validation
Hybrid source ----------> hybrid parser --------┘          |
                                                          v
                                                   Plainlang Semantic IR
                                                          |
                                          type / policy / capability checks
                                                          |
                                               interpreter or bytecode VM
                                                          |
                                                    execution results
                                                          |
                                  documentation generator and explanations
```

## Architectural boundaries

- **Language specification:** syntax, values, evaluation rules and compatibility.
- **Compiler frontend:** lexer, parser, AST, name resolution, type checking and diagnostics.
- **Semantic IR:** stable, serializable representation shared by compiler, tooling, intelligence and docs.
- **Runtime:** deterministic evaluation, resource limits and capability enforcement.
- **Intelligence adapter:** proposes formal source or IR; it cannot bypass compiler validation or runtime policy.
- **Documentation engine:** derives API and language reference material from authoritative metadata and source annotations.
- **Website:** existing Jekyll content remains untouched while the new platform is designed.

## Production implementation direction

A Rust compiler/runtime is a candidate for a later production implementation, but this is not a commitment until performance, portability, contributor experience and implementation costs are evaluated. The Python bootstrap provides executable behavioral examples and conformance tests that a future implementation can reuse.

## Security model

The current interpreter exposes only three built-ins and no direct filesystem, network, process, reflection or import capability. It is not safe to execute untrusted programs in a shared service: there are no OS-level isolation guarantees, memory quotas, CPU quotas or robust cancellation yet. A production runtime must enforce capability-based access and operating-system isolation independently of AI-generated code.
