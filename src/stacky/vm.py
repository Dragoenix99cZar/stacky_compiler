# src/stacky/vm.py

def run(program):
    """Executes a list of bytecode instructions and returns the top of the stack."""
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
            if right == 0:
                raise ZeroDivisionError("Division by zero in VM")
            stack.append(left / right)
        elif opcode == "POW":
            right = stack.pop()
            left = stack.pop()
            stack.append(left ** right)
        else:
            raise RuntimeError(f"Unknown opcode: {opcode}")

    return stack[-1] if stack else None