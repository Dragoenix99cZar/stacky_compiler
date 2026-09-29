Build the stack-based DSL as a **learning compiler project**. Python is the better starting point because it lets you focus on compiler concepts instead of Rust’s ownership and type-system details. Later, reimplement the same language or VM in Rust to learn systems-level compiler engineering.

A good progression is:

## 1. Implement a tiny language

Start with arithmetic:

```text
2 3 + 4 *
```

This means:

```text
(2 + 3) * 4
```

Use postfix notation because it naturally maps to a stack machine.

Add features in this order:

1. Integer literals
2. Arithmetic operations: `+ - * /`
3. Boolean values and comparisons
4. Variables
5. Conditional execution
6. Loops
7. User-defined functions
8. A standard library
9. Bytecode serialization
10. Static checking or type inference

## 2. Separate the compiler stages

Keep the stages distinct:

```text
source text
    ↓
lexer
    ↓
tokens
    ↓
parser
    ↓
AST
    ↓
semantic analysis
    ↓
bytecode
    ↓
stack-based virtual machine
```

Even though a simple postfix language can execute directly from tokens, deliberately building an AST teaches more compiler design.

For example:

```text
2 3 +
```

could become:

```text
Add(
    Integer(2),
    Integer(3)
)
```

Then compile it into:

```text
PUSH 2
PUSH 3
ADD
```

## 3. Write the first compiler in Python

A minimal lexer:

```python
def tokenize(source: str) -> list[str]:
    return source.split()
```

A simple parser for postfix expressions:

```python
def parse(tokens: list[str]):
    stack = []

    for token in tokens:
        if token.isdigit():
            stack.append(("integer", int(token)))
        elif token in {"+", "-", "*", "/"}:
            right = stack.pop()
            left = stack.pop()
            stack.append(("binary", token, left, right))
        else:
            raise SyntaxError(f"Unknown token: {token}")

    if len(stack) != 1:
        raise SyntaxError("Incomplete expression")

    return stack[0]
```

A bytecode compiler:

```python
def compile_node(node, output):
    if node[0] == "integer":
        output.append(("PUSH", node[1]))

    elif node[0] == "binary":
        _, operator, left, right = node

        compile_node(left, output)
        compile_node(right, output)

        operations = {
            "+": "ADD",
            "-": "SUB",
            "*": "MUL",
            "/": "DIV",
        }

        output.append((operations[operator],))
```

A basic VM:

```python
def run(program):
    stack = []

    for instruction in program:
        opcode = instruction[0]

        if opcode == "PUSH":
            stack.append(instruction[1])
        elif opcode == "ADD":
            right = stack.pop()
            left = stack.pop()
            stack.append(left + right)
        elif opcode == "SUB":
            right = stack.pop()
            left = stack.pop()
            stack.append(left - right)
        elif opcode == "MUL":
            right = stack.pop()
            left = stack.pop()
            stack.append(left * right)
        elif opcode == "DIV":
            right = stack.pop()
            left = stack.pop()
            stack.append(left / right)

    return stack[-1]
```

This teaches the core relationship:

```text
AST → instructions → stack effects
```

For example:

```text
ADD: [a, b] → [a + b]
MUL: [a, b] → [a * b]
```

Thinking in stack effects is especially useful because it gives you a basis for validation. You can detect malformed programs before execution if an instruction requires more stack values than are available.

## 4. Add compiler concepts deliberately

Do not only add language features. Add the concepts that compiler designers use:

- **Lexing:** converting characters into tokens
- **Parsing:** determining grammatical structure
- **AST construction:** representing program structure
- **Name resolution:** determining what variables refer to
- **Semantic analysis:** checking whether programs make sense
- **Intermediate representation:** representing programs between source and machine code
- **Code generation:** producing bytecode
- **Virtual-machine execution:** interpreting bytecode
- **Optimization:** improving generated code
- **Diagnostics:** producing useful errors

For each feature, implement the complete pipeline. For example, variables should pass through:

```text
let x = 10
    ↓
tokens
    ↓
AST
    ↓
symbol table
    ↓
LOAD_CONSTANT 10
STORE_GLOBAL x
```

## 5. Then port the VM to Rust

Once the Python implementation works, rewrite only the VM first:

```text
Python lexer/parser/compiler → Rust bytecode VM
```

This lets you compare implementations while keeping the language unchanged.

Then port the compiler stages one by one:

1. Bytecode representation
2. Runtime values
3. VM execution
4. Lexer
5. Parser
6. Semantic analysis
7. Diagnostics

Rust becomes particularly educational when implementing:

- tagged runtime values
- bytecode ownership
- call frames
- closures
- garbage collection
- arenas
- source spans
- error propagation
- concurrent execution

## 6. A strong project roadmap

A useful sequence is:

### Milestone 1: Calculator

```text
2 3 +
```

### Milestone 2: Variables

```text
10 let x
x 2 *
```

### Milestone 3: Structured syntax

```text
let x = 10;
print(x * 2);
```

### Milestone 4: Control flow

```text
if condition {
    ...
} else {
    ...
}
```

### Milestone 5: Functions

```text
fn square(x) {
    x * x
}
```

### Milestone 6: Bytecode VM

Add instruction offsets, jumps, local slots, and call frames.

### Milestone 7: Static types

Start with simple types:

```text
Int
Bool
String
```

Then reject errors such as:

```text
true + 4
```

### Milestone 8: Rust implementation

Rebuild the stable design in Rust and compare the two runtimes.

The key is to avoid starting with a large language. A tiny language that has a lexer, parser, semantic checker, bytecode compiler, VM, tests, and good error messages will teach you more than a large unfinished language.

---

### What is **Virtual Machine (VM)**?

In the context of my compiler pipeline, a **Virtual Machine (VM)** is essentially a **software-simulated CPU**.

Instead of translating your code directly into native machine code (like x86 or ARM) for your physical processor, your compiler translates it into **bytecode** (instructions like `PUSH`, `ADD`, `MUL`), and the VM is the engine that executes those instructions.

---

### What Makes Up Your Stacky VM?

Looking back at my `src/stacky/vm.py`, the VM consists of two main components:

1. **The Stack (Memory):** A simple Python list (`stack = []`) that acts as a Last-In, First-Out (LIFO) data structure. Numbers and intermediate results are pushed onto it and popped off it.
2. **The Execution Loop:** A loop that iterates through your compiled bytecode instructions one by one, inspecting the opcode and modifying the stack accordingly:
* When it sees `('PUSH', 2)`, it appends `2` to the stack.
* When it sees `('ADD',)`, it pops the top two numbers, adds them together, and pushes the result back onto the stack.

---

### Why Do Compilers Use a Virtual Machine?

* **Portability:** Because your VM is written in Python (and eventually Rust), your language (`Stacky`) can run on Windows, Mac, Linux, or even inside a browser without needing to change the compiler. It is completely independent of your physical hardware.
* **Simplicity:** Building a real hardware compiler that talks directly to an Intel CPU is notoriously complex. Building a software VM is lightweight—it takes fewer than 30 lines of code to simulate an entire processor core using a stack and a `for` loop!
* **The Heart of Modern Languages:** Famous languages use this exact architecture. For example, **Java** compiles down to bytecode (`.class` files) which are then executed by the JVM (Java Virtual Machine). **Python** itself compiles your `.py` files into `.pyc` bytecode, which is then executed by Python's own stack-based virtual machine.

By building this VM, you've essentially implemented the execution layer of a real programming language!