# Project Status: Stack-Based DSL Compiler (`stacky`)

## 2026-09-26

## 1. What Was Discussed

* **Compiler Architecture Strategy:** Designing an educational stack-based language (inspired by Forth/PostScript) to learn compiler design phases before porting the engine to Rust.


* **Pipeline Separation:** The necessity of cleanly separating source text, lexing, parsing, AST generation, semantic validation, bytecode compilation, and virtual machine execution.


* **Frontend Engineering:** Implementing a Shunting Yard algorithm for infix-to-postfix conversion and an advanced context-aware lexer to handle floats, operator precedence, and unary negative signs/negation.
* **Developer Ergonomics:** Setting up a Windows 11 local repository workspace, handling PowerShell UTF-8 redirection formatting, and building a debugging pipeline script to visualize every phase transparently.

---

## 2. What We Achieved

* **Project Structure & Git Setup:**
* Initialized a modular package layout under `src/stacky/` with isolated test and example directories.


* Added a robust standard `.gitignore` file for Python virtual environments and caches.


* **Advanced Lexer (`src/stacky/lexer.py`):**
* Built a regex-driven context-aware tokenizer capable of merging unary negative signs directly into numeric tokens (e.g., `-5`) or converting them to `neg` expressions.


* **Shunting Yard & AST Parser (`src/stacky/parser.py`):**
* Implemented `infix_to_postfix` supporting standard operator precedence and parentheses grouping (`+`, `-`, `*`, `/`, `^`).
* Built an AST parser mapping postfix tokens into hierarchical nested tuples (`integer`, `unary`, `binary`).
* Added a custom recursive ASCII tree visualizer (`print_ast`) to inspect AST structures clearly.


* **Bytecode Compiler & Stack VM (`src/stacky/compiler.py` & `src/stacky/vm.py`):**
* Implemented a recursive bytecode emitter translating AST nodes into flat sequential instructions (`PUSH`, `ADD`, `SUB`, `MUL`, `DIV`, `NEG`, `POW`).
* Built a stack-based evaluation virtual machine loop that executes instructions successfully and handles float/integer math accurately.


* **Diagnostics:** Created an end-to-end debug script (`examples/debug_pipeline.py`) to trace data flow through every single stage of the compiler pipeline.

---

## 3. TODOs & Next Steps

- Milestone 2: Variables & Symbol Tables
  - Implement assignment syntax (e.g., `let x = 10`).
  - Build a symbol table to track variable scopes and identifiers.
  - Add new bytecode instructions like `STORE_GLOBAL` and `LOAD_GLOBAL`.

* Milestone 3 & 4: Control Flow
  - Introduce conditional execution (`if`/`else` blocks) with bytecode jump instructions and instruction offsets.

* Milestone 5 & 6: Functions & Advanced Features
  - Add user-defined function syntax (e.g., `fn square(x) { x * x }`), call frames, and local slots.
  - Milestone 8: The Rust Port


* Once the Python language specification is complete and stable, rewrite the bytecode VM and compiler stages in Rust to learn systems-level memory management and ownership handling.

