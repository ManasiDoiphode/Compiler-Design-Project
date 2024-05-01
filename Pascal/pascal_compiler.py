import re
import os.path
import time
import resource

# Step 1: Lexical Analysis
def tokenize(code):
    keywords = {'for', 'to', 'do', 'begin', 'end'}
    operators = {'+', '-', '*', '/'}
    tokens = []
    code = re.findall(r'\b\w+\b|[\+\-\*/]', code)
    for token in code:
        if token in keywords:
            tokens.append(('KEYWORD', token))
        elif token in operators:
            tokens.append(('OPERATOR', token))
        elif token.isdigit():
            tokens.append(('NUMBER', token))
        else:
            tokens.append(('IDENTIFIER', token))
    return tokens

# Step 2: Syntactic Analysis (Parsing)
def parse(tokens):
    i = 0
    n = len(tokens)
    while i < n:
        if tokens[i][1] == 'for':
            # Expecting a loop construct: for <identifier> := <number> to <number> do
            loop_tokens = []
            j = i + 1  # Start from the token after 'for'
            while j < n and tokens[j][1] != 'do':
                loop_tokens.append(tokens[j])
                j += 1
            loop_tokens.append(tokens[j])  # Include 'do' keyword
            print("Loop tokens:", loop_tokens)  # Debugging print statement
            # Check if loop tokens form a valid loop construct
            if (
                len(loop_tokens) == 7 and
                loop_tokens[0][0] == 'IDENTIFIER' and  # Check for loop variable
                loop_tokens[1][1] == ':=' and  # Check for assignment operator
                loop_tokens[2][0] == 'NUMBER' and  # Check for start value
                loop_tokens[3][1] == 'to' and  # Check for 'to' keyword
                loop_tokens[4][0] == 'NUMBER' and  # Check for end value
                loop_tokens[5][1] == 'do'  # Check for 'do' keyword
            ):
                print(f'Found loop construct:')
                print(f'Loop variable: {loop_tokens[0][1]}')
                print(f'Start value: {loop_tokens[2][1]}')
                print(f'End value: {loop_tokens[4][1]}')
                i = j + 1  # Skip the loop construct
                # Parse loop body (tokens until 'end')
                while i < n and tokens[i][1] != 'end':
                    print(tokens[i])  # Print loop body
                    i += 1
                print(f'End of loop')
            else:
                # print(f'Error: Invalid loop construct')
                break
        else:
            print(tokens[i])
            i += 1

# Step 3: Semantic Analysis
def semantic_analysis(tokens):
    i = 0
    n = len(tokens)
    while i < n:
        if tokens[i][1] == 'for':
            # Expecting a loop construct: for <identifier> := <number> to <number> do
            if (
                tokens[i+1][0] == 'IDENTIFIER' and
                tokens[i+2][1] == ':=' and
                tokens[i+3][0] == 'NUMBER' and
                tokens[i+4][1] == 'to' and
                tokens[i+5][0] == 'NUMBER' and
                tokens[i+6][1] == 'do'
            ):
                loop_variable = tokens[i+1][1]
                start_value = tokens[i+3][1]
                end_value = tokens[i+5][1]
                # Check if loop variable is valid
                if not loop_variable.isalpha():
                    print(f'Error: Invalid loop variable "{loop_variable}"')
                    break
                # Check if start and end values are integers
                if not start_value.isdigit():
                    print(f'Error: Invalid start value "{start_value}"')
                    break
                if not end_value.isdigit():
                    print(f'Error: Invalid end value "{end_value}"')
                    break
                i += 7  # Skip the loop construct
                # Perform semantic analysis on loop body (tokens until 'end')
                while i < n and tokens[i][1] != 'end':
                    # Here, you can add more semantic checks as needed
                    i += 1
            else:
                # print(f'Error: Invalid loop construct')
                break
        else:
            i += 1


# Step 4: Intermediate Code Generation
def generate_intermediate_code(tokens):
    intermediate_code = []
    # Generate intermediate code based on the tokens
    for token_type, token_value in tokens:
        if token_type == 'KEYWORD' and token_value == 'for':
            # Start of loop
            intermediate_code.append('// Start of loop')
            intermediate_code.append('LOOP_START:')
            # Load initial value of loop variable into a register
            intermediate_code.append(f'    LOAD_CONSTANT {tokens[2][1]}, {tokens[0][1]}')
            # Load end value of loop into a register
            intermediate_code.append(f'    LOAD_CONSTANT {tokens[4][1]}, endValue')
            # Comparison to check if loop should continue
            intermediate_code.append('    COMPARE i, endValue')
            # Jump to end of loop if end condition is met
            intermediate_code.append('    JUMP_IF_GREATER_EQUAL END_LOOP')
            # Loop body
            intermediate_code.append('    // Loop body goes here')
        elif token_type == 'KEYWORD' and token_value == 'end':
            # End of loop
            intermediate_code.append('// End of loop')
            intermediate_code.append('    INCREMENT i')
            intermediate_code.append('    JUMP LOOP_START')
            intermediate_code.append('')
            intermediate_code.append('END_LOOP:')
    return '\n'.join(intermediate_code)

# Function to measure memory usage
def get_memory_usage():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

# Read Pascal code from file
file_name = 'example.pas'
if os.path.exists(file_name):
    with open(file_name, 'r') as file:
        pascal_code = file.read()

    # Measure start time
    start_time = time.time()

    # Tokenize the code
    tokens = tokenize(pascal_code)

    # Parse the tokens
    parse(tokens)

    # Perform semantic analysis
    semantic_analysis(tokens)

    # Generate intermediate code
    intermediate_code = generate_intermediate_code(tokens)

    # Write intermediate code to a file
    with open('result.txt', 'w') as f:
        f.write(intermediate_code)

    # Measure end time
    end_time = time.time()

    # Calculate time taken
    time_taken = end_time - start_time

    # Calculate memory consumed
    memory_consumed = get_memory_usage()

    print("Intermediate code written to result.txt")
    print(f"Time taken: {time_taken} seconds")
    print(f"Memory consumed: {memory_consumed} bytes")
else:
    print(f"Error: File '{file_name}' not found")
