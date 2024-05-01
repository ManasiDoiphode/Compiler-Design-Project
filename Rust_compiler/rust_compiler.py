import re
import time
import resource

class TokenType:
    # Define existing token types
    FOR = 'FOR'
    IDENTIFIER = 'IDENTIFIER'
    OPEN_PAREN = 'OPEN_PAREN'
    CLOSE_PAREN = 'CLOSE_PAREN'
    OPEN_BRACE = 'OPEN_BRACE'
    CLOSE_BRACE = 'CLOSE_BRACE'
    SEMICOLON = 'SEMICOLON'
    RANGE = 'RANGE'
    STRING_LITERAL = 'STRING_LITERAL'
    NOT = 'NOT'
    COMMA = 'COMMA'
    # Define new token type for function
    FN = 'FN'

# Update token definitions to include 'fn' keyword
token_defs = [
    # Updated token definition for function
    (TokenType.FN, r'\bfn\b'), # Using \b to match word boundary to ensure it's a whole word
    # Existing token definitions
    (TokenType.FOR, r'for'),
    (TokenType.IDENTIFIER, r'[a-zA-Z_][a-zA-Z0-9_]*'),
    (TokenType.OPEN_PAREN, r'\('),
    (TokenType.CLOSE_PAREN, r'\)'),
    (TokenType.OPEN_BRACE, r'\{'),
    (TokenType.CLOSE_BRACE, r'\}'),
    (TokenType.SEMICOLON, r';'),
    (TokenType.RANGE, r'\d+\.\.\d+'),
    (TokenType.STRING_LITERAL, r'"(?:\\.|[^"\\])*"'),
    (TokenType.NOT, r'!'),
    (TokenType.COMMA, r',')
]


def tokenize(source_code):
    tokens = []
    while source_code:
        # Skip whitespace and comments
        if source_code.startswith('//'):
            comment_end = source_code.find('\n')
            if comment_end == -1:  # Handle case where comment extends to end of file
                break
            source_code = source_code[comment_end + 1:].lstrip()
            continue
        
        # Tokenize based on token definitions
        for token_type, pattern in token_defs:
            match = re.match(pattern, source_code)
            if match:
                token = match.group(0)
                if token_type != TokenType.RANGE:  # Skip RANGE token, as it's just a separator
                    tokens.append((token_type, token))
                source_code = source_code[len(token):].lstrip()
                print("Found token:", token)  # Print found token
                break
        else:
            print("Invalid token:", source_code)  # Print invalid token
            raise SyntaxError('Invalid token: ' + source_code)
    return tokens


# Intermediate Code Generator function
def generate_intermediate_code(tokens):
    # Initialize intermediate code
    intermediate_code = ""
    # Flag to track if we are inside a loop
    inside_loop = False
    
    # Iterate through tokens
    for token_type, token_value in tokens:
        # Check if the token is 'for' keyword
        if token_type == TokenType.FOR:
            # Start of loop
            intermediate_code += "LOOP_START:\n"
            inside_loop = True
        # Check if the token is '{'
        elif token_type == TokenType.OPEN_BRACE:
            # Start of loop body
            intermediate_code += "LOOP_BODY_START:\n"
        # Check if the token is '}'
        elif token_type == TokenType.CLOSE_BRACE:
            # End of loop body
            intermediate_code += "LOOP_BODY_END:\n"
        # Check if the token is an identifier (variable)
        elif token_type == TokenType.IDENTIFIER:
            # Load the variable value
            intermediate_code += f"LOAD {token_value}\n"
        # Check if the token is an integer
        elif token_type == TokenType.RANGE:
            # Push the integer value
            intermediate_code += f"PUSH {token_value}\n"
        # Check if the token is '='
        elif token_type == TokenType.NOT:
            # Store the value
            intermediate_code += "STORE\n"
        # Check if the token is '<'
        elif token_type == TokenType.COMMA:
            # Compare values
            intermediate_code += "COMPARE\n"
            # Jump to loop body end if false
            intermediate_code += "JUMP_IF_FALSE LOOP_BODY_END\n"
    
    # Return the generated intermediate code
    return intermediate_code


# Main compiler function
def compile_rust(source_file, output_file):
    start_time = time.time()
    start_memory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    
    # Load Rust source code
    with open(source_file, 'r') as f:
        rust_code = f.read()

    # Lexical analysis
    tokens = tokenize(rust_code)
    
    # Generate intermediate code
    intermediate_code = generate_intermediate_code(tokens)
    
    # Write intermediate code to output file
    with open(output_file, 'w') as f:
        f.write(intermediate_code)
    
    end_time = time.time()
    end_memory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    
    # Calculate time and memory consumed
    elapsed_time = end_time - start_time
    memory_consumed = end_memory - start_memory
    
    print(f"Compilation completed in {elapsed_time} seconds")
    print(f"Memory consumed: {memory_consumed} KB")

# Run the compiler
if __name__ == "__main__":
    source_file = "example.rs"
    output_file = "result.txt"
    compile_rust(source_file, output_file)
