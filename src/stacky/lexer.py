# src/stacky/lexer.py
import re

# Define operator precedence here so the lexer can detect unary minus contexts
PRECEDENCE = {
    '+': 1,
    '-': 1,
    '*': 2,
    '/': 2,
    '^': 3
}

def tokenize(expression: str) -> list[str]:
    """
    Advanced context-aware tokenizer.
    Merges negative signs directly into numbers when they act as unary prefixes,
    or converts them to 'neg' for non-numeric terms.
    """
    # Raw structural split pattern for identifiers, numbers, and operators
    raw_pattern = r'[a-zA-Z][a-zA-Z0-9]*|\d+(?:\.\d+)?|[\+\-\*\/\^\(\),]'
    raw_tokens = re.findall(raw_pattern, expression)
    
    refined_tokens = []
    i = 0
    while i < len(raw_tokens):
        token = raw_tokens[i]
        
        # Check if the token is a minus sign
        if token == '-':
            # Determine if it's unary based on the preceding refined token
            is_unary = (
                len(refined_tokens) == 0 or 
                refined_tokens[-1] == '(' or 
                refined_tokens[-1] == ',' or 
                refined_tokens[-1] in PRECEDENCE
            )
            
            # Peek at the next token to ensure a number follows it
            if is_unary and i + 1 < len(raw_tokens) and raw_tokens[i+1].replace('.', '', 1).isdigit():
                # Merge the minus sign with the number directly
                refined_tokens.append("-" + raw_tokens[i+1])
                i += 2
                continue
            elif is_unary:
                # If it's a unary minus before a function or variable (e.g., -x), use 'neg'
                refined_tokens.append('neg')
                i += 1
                continue
                
        refined_tokens.append(token)
        i += 1
        
    return refined_tokens