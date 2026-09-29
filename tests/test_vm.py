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

