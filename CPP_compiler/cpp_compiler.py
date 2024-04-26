import time
import resource
import sys

# Token class to store token information
class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

# Lexical Analyzer function
def lex(file):
    tokens = []
    line_number = 0

    for line in file:
        line_number += 1
        words = line.split()
        for word in words:
            token = Token('', word)

            # Simple categorization for demo purpose
            if word in ["for", "int", "return"]:
                token.type = "KEYWORD"
            elif word in ["{", "}"]:
                token.type = "BRACE"
            elif word in ["=", "<", ";"]:
                token.type = "OPERATOR"
            elif word.isdigit():
                token.type = "INTEGER"
            else:
                token.type = "IDENTIFIER"
            
            tokens.append(token)
    
    return tokens

# Syntactical Analyzer function
def parse(tokens):
    # Simplified parsing for demo purpose
    for token in tokens:
        if token.value == "for":
            return True
    return False

# Intermediate Code Generator function
def generate_intermediate_code(tokens):
    # Simplified intermediate code generation for demo purpose
    code = []
    for token in tokens:
        if token.value == "for":
            code.append(f"LOOP_START:")
        elif token.value == "{":
            code.append(f"LOOP_BODY_START:")
        elif token.value == "}":
            code.append(f"LOOP_BODY_END:")
        elif token.type == "IDENTIFIER":
            code.append(f"LOAD {token.value}")
        elif token.type == "INTEGER":
            code.append(f"PUSH {token.value}")
        elif token.value == "=":
            code.append(f"STORE")
        elif token.value == "<":
            code.append(f"COMPARE")
            code.append(f"JUMP_IF_FALSE LOOP_BODY_END")
    return "\n".join(code)

def main():
    start_time = time.time()
    start_mem = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

    try:
        with open("example.cpp", "r") as file:
            tokens = lex(file)

            if not parse(tokens):
                print("Error: Unable to parse the source code!")
                return
            
            intermediate_code = generate_intermediate_code(tokens)

            # Write intermediate code to result.txt
            with open("result.txt", "w") as result_file:
                result_file.write(intermediate_code)

            end_time = time.time()
            end_mem = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

            elapsed_time = end_time - start_time
            mem_consumed = end_mem - start_mem

            print("Intermediate code generated successfully!")
            print(f"Time taken: {elapsed_time} seconds")
            print(f"Memory consumed: {mem_consumed} kilobytes")

    except FileNotFoundError:
        print("Error opening file!")

if __name__ == "__main__":
    main()
