# src/stacky/parser.py

from stacky.lexer import tokenize

# Precedence configuration for Shunting Yard algorithm
PRECEDENCE = {
    '+': 1,
    '-': 1,
    '*': 2,
    '/': 2,
    '^': 3
}

RIGHT_ASSOCIATIVE = {'^'}
MATH_CONST = {'pi', 'e'}

def infix_to_postfix(infix_expression: str) -> str:
    """Converts a standard infix expression string into a postfix token string."""
    tokens = tokenize(infix_expression)
    output_queue = []
    operator_stack = []

    for token in tokens:
        # Check if the token is a negative or positive float/int string
        is_numeric = token.replace('.', '', 1).isdigit() or (token.startswith('-') and token[1:].replace('.', '', 1).isdigit())
        
        if is_numeric or token.lower() in MATH_CONST:
            output_queue.append(token.lower())
            
        elif token in PRECEDENCE:
            while operator_stack and operator_stack[-1] in PRECEDENCE:
                top_op = operator_stack[-1]
                higher_precedence = PRECEDENCE[top_op] > PRECEDENCE[token]
                equal_precedence = PRECEDENCE[top_op] == PRECEDENCE[token]
                is_left_assoc = token not in RIGHT_ASSOCIATIVE
                
                if higher_precedence or (equal_precedence and is_left_assoc):
                    output_queue.append(operator_stack.pop())
                else:
                    break
            operator_stack.append(token)
            
        elif token == ',':
            while operator_stack and operator_stack[-1] != '(':
                output_queue.append(operator_stack.pop())
            
        elif token == '(':
            operator_stack.append(token)
            
        elif token == ')':
            while operator_stack and operator_stack[-1] != '(':
                output_queue.append(operator_stack.pop())
            if operator_stack and operator_stack[-1] == '(':
                operator_stack.pop()

    while operator_stack:
        output_queue.append(operator_stack.pop())

    return " ".join(output_queue)


def parse(tokens: list[str]):
    """Parses postfix tokens into an Abstract Syntax Tree (AST) using a stack."""
    stack = []

    for token in tokens:
        # Support numeric literals (ints and floats)
        is_numeric = token.replace('.', '', 1).isdigit() or (token.startswith('-') and token[1:].replace('.', '', 1).isdigit())
        
        if is_numeric:
            # Cast to float if it contains a dot, otherwise int
            val = float(token) if '.' in token else int(token)
            stack.append(("integer", val))
        elif token in {"+", "-", "*", "/", "^"}:
            if len(stack) < 2:
                raise SyntaxError(f"Stack underflow while parsing operator: {token}")
            right = stack.pop()
            left = stack.pop()
            stack.append(("binary", token, left, right))
        else:
            raise SyntaxError(f"Unknown token: {token}")

    if len(stack) != 1:
        raise SyntaxError("Incomplete expression")

    return stack[0]


def print_ast(node, prefix="", is_last=True, is_root=True):
    """
    Recursively prints the AST in a clean tree-like ASCII format.
    """
    if not node:
        return

    node_type = node[0]
    
    # Format the label based on node type
    if node_type == "integer":
        label = f"integer({node[1]})"
        children = []
    elif node_type == "unary":
        _, op, operand = node
        label = f"unary({op})"
        children = [operand]
    elif node_type == "binary":
        _, op, left, right = node
        label = f"binary({op})"
        children = [left, right]
    else:
        label = str(node)
        children = []

    # Print current node
    if is_root:
        print(f"Root: {label}")
        child_prefix = ""
    else:
        marker = "└── " if is_last else "├── "
        print(prefix + marker + label)
        extension = "    " if is_last else "│   "
        child_prefix = prefix + extension

    # Recursively print children
    for i, child in enumerate(children):
        print_ast(child, child_prefix, i == len(children) - 1, is_root=False)

