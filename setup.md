Starting your stack-based DSL compiler project on Windows 11 using Python is an ideal choice because it allows you to focus on core compiler concepts rather than wrestling with type systems or memory management.

Here is a complete project setup guide and modular folder structure designed to scale from a simple calculator all the way to a full-featured programming language and eventual Rust port.

---

## 1. Recommended Project Structure

A clean compiler project separates concerns strictly into phases: lexing, parsing, semantic analysis, code generation, and virtual machine execution.

```text
stacky_compiler/
├── src/
│   └── stacky/
│       ├── __init__.py
│       ├── lexer.py       # Converts source text into tokens
│       ├── parser.py      # Builds the AST from tokens
│       ├── semantic.py    # Name resolution and type checking
│       ├── compiler.py    # Emits bytecode from the AST
│       └── vm.py          # Stack-based virtual machine execution
├── tests/
│   ├── test_lexer.py
│   ├── test_parser.py
│   └── test_vm.py
├── examples/
│   └── milestone1.stacky
├── pyproject.toml
└── README.md

```

---

## 2. Step-by-Step Setup Guide (Windows 11)

Open your terminal (PowerShell or Command Prompt) and execute the following steps to initialize your environment:

### Step 1: Create the Project Directory

```powershell
mkdir stacky_compiler
cd stacky_compiler

```

### Step 2: Set Up a Python Virtual Environment

Verify your Python installation and create an isolated environment:

```powershell
python -m venv venv
venv\Scripts\activate

```

### Step 3: Initialize Project Configuration

Create a simple `pyproject.toml` file in the root directory to manage your package and testing dependencies:

```toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "stacky"
version = "0.1.0"
description = "A stack-based educational DSL compiler"
readme = "README.md"
requires-python = ">=3.10"
dependencies = []

[dependency-groups]
dev = [
    "pytest>=8.0.0"
]

```

*(Note: You can install development dependencies using `pip install -e .[dev]` or simply `pip install pytest` for now).*

### Step 4: Create the Core Source Files

Generate your package and test files to establish the modular layout:

```powershell
New-Item -ItemType Directory -Force src/stacky, tests, examples
New-Item src/stacky/__init__.py, src/stacky/lexer.py, src/stacky/parser.py, src/stacky/semantic.py, src/stacky/compiler.py, src/stacky/vm.py
New-Item tests/test_vm.py

```

---

## 3. Your First Smoke Test

To verify everything is working, let's wire up a minimal test for Milestone 1 (a basic calculator expression like `2 3 + 4 *`).

Create a test in `tests/test_vm.py`:

```python
from stacky.vm import run
from stacky.compiler import compile_node
from stacky.parser import parse
from stacky.lexer import tokenize

def test_basic_calculator():
    source = "2 3 + 4 *"
    tokens = tokenize(source)
    ast = parse(tokens)
    
    bytecode = []
    compile_node(ast, bytecode)
    
    result = run(bytecode)
    assert result == 20  # (2 + 3) * 4 = 20

```

---

## What to Focus on Next

With your workspace ready on Windows 11, you can begin implementing the pipeline stages one by one. Would you like to write the implementation code for **Phase 1 (Lexer and Parser)** or set up the **Virtual Machine execution loop** first?