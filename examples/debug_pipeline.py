from stacky.parser import infix_to_postfix, parse, print_ast
from stacky.lexer import tokenize
from stacky.compiler import compile_node
from stacky.vm import run

def inspect_infix_pipeline(infix_source: str):
    print("*"*70)
    print(f"=== === === INFIX SOURCE CODE === === ===")
    print(f"  {infix_source}\n")

    # 0. Frontend Translation: Infix to Postfix
    postfix_str = infix_to_postfix(infix_source)
    print(f"=== 0. SHUNTING YARD (Postfix Translation) ===")
    print(f"  {postfix_str}\n")

    # 1. Lexer Stage
    tokens = tokenize(postfix_str)
    print(f"=== 1. LEXER (Tokens) ===")
    print(f"  {tokens}\n")

    # 2. Parser Stage
    ast = parse(tokens)
    print(f"=== 2. PARSER (Abstract Syntax Tree) ===")
    print(f"  {ast}\n")
    print_ast(ast)
    print()

    # 3. Compiler Stage
    bytecode = []
    compile_node(ast, bytecode)
    print(f"=== 3. COMPILER (Bytecode Instructions) ===")
    for instruction in bytecode:
        print(f"  {instruction}")
    print()

    # 4. Virtual Machine Stage
    result = run(bytecode)
    print(f"=== 4. VIRTUAL MACHINE (Execution Result) ===")
    print(f"  Final Stack Result: {result}\n")

if __name__ == "__main__":
    inspect_infix_pipeline("(2+3)*4")
    inspect_infix_pipeline("2 ^ ( 1 + 2 )")
    inspect_infix_pipeline("-5 * (1.3 * 2) + 21.1 /7")