# src/stacky/compiler.py

def compile_node(node, output: list):
    """Recursively compiles AST nodes into flat bytecode instructions."""
    if node[0] == "integer":
        output.append(("PUSH", node[1]))

    elif node[0] == "binary":
        _, operator, left, right = node

        # Postfix evaluation: evaluate left, then right
        compile_node(left, output)
        compile_node(right, output)

        operations = {
            "+": "ADD",
            "-": "SUB",
            "*": "MUL",
            "/": "DIV",
            "^": "POW",
        }

        if operator not in operations:
            raise ValueError(f"Unsupported operator: {operator}")

        output.append((operations[operator],))