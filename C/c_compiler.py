import time
import resource
import re

class Compiler:
    def __init__(self):
        self.output = ""

    def tokenize(self, source_code):
        # List of C keywords
        keywords = {'auto', 'break', 'case', 'char', 'const', 'continue', 'default', 'do', 'double', 'else',
                    'enum', 'extern', 'float', 'for', 'goto', 'if', 'int', 'long', 'register', 'return',
                    'short', 'signed', 'sizeof', 'static', 'struct', 'switch', 'typedef', 'union', 'unsigned',
                    'void', 'volatile', 'while'}

        # List of C operators
        operators = {'+', '-', '*', '/', '=', '==', '!=', '<', '>', '<=', '>=', '&&', '||', '!', '&', '|', '^',
                    '~', '<<', '>>', '+=', '-=', '*=', '/=', '%=', '&=', '|=', '^=', '<<=', '>>=', ',', ';', ':',
                    '(', ')', '[', ']', '{', '}', '.', '->', '++', '--', '?', '::', '...'}

        # Split source code by whitespace
        tokens = source_code.split()

        # List to store tokenized output
        tokenized_output = []

        for token in tokens:
            # Check if the token is a keyword
            if token in keywords:
                tokenized_output.append(('KEYWORD', token))
            # Check if the token is an operator
            elif token in operators:
                tokenized_output.append(('OPERATOR', token))
            # Check if the token is a numeric literal
            elif token.isdigit():
                tokenized_output.append(('LITERAL', token))
            # Check if the token is a string literal
            elif token.startswith('"') and token.endswith('"'):
                tokenized_output.append(('STRING_LITERAL', token))
            # Check if the token is an identifier
            elif token.isidentifier():
                tokenized_output.append(('IDENTIFIER', token))
            # Otherwise, treat it as an unknown token
            else:
                tokenized_output.append(('UNKNOWN', token))

        return tokenized_output


    def parse(self, tokens):
        # Placeholder for syntactic analysis (parsing)
        # For simplicity, we'll construct a basic abstract syntax tree (AST)
        ast = []

        # Check if tokens list is empty
        if not tokens:
            print("Error: Empty input tokens list.")
            return ast

        # Current index in the tokens list
        current_index = 0

        # Loop through the tokens
        while current_index < len(tokens):
            token = tokens[current_index]

            # If token is a loop (for simplicity, consider only 'for' loops)
            if token[1] == 'for':
                # Find the index of '(' and ')'
                start_index = current_index + 1  # Start from the next token
                end_index = tokens.index('{', start_index) if '{' in tokens[start_index:] else len(tokens)

                # Extract loop condition
                loop_condition = [str(t[1]) if isinstance(t, tuple) else t for t in tokens[start_index + 1:end_index]]

                # Find the start of the loop body
                body_start_index = end_index if '{' in tokens[start_index:] else start_index

                # Find the end of the loop body
                body_end_index = tokens.index('}', body_start_index) if '}' in tokens[body_start_index:] else len(tokens)

                # Extract loop body
                loop_body = tokens[body_start_index + 1: body_end_index]

                # Construct loop node for AST
                loop_node = ('LOOP', loop_condition, loop_body)

                # Add loop node to AST
                ast.append(loop_node)

                # Move current_index to the end of the loop body
                current_index = body_end_index

            # Increment current_index
            current_index += 1

        return ast



    def check_semantics(self, parsed_ast):
        # Placeholder for semantic analysis
        # For simplicity, check if each function declaration has a return statement
        for node in parsed_ast:
            if node[0] == 'FUNCTION_DECLARATION':
                function_name = node[1]
                parameters = node[2]

                # Check if the function has a return statement
                has_return = False
                for sub_node in parsed_ast:
                    if sub_node[0] == 'RETURN_STATEMENT':
                        has_return = True
                        break

                if not has_return:
                    print(f"Warning: Function '{function_name}' does not have a return statement.")

    def generate_intermediate_code(self, parsed_ast):
        # Placeholder for intermediate code generation
        # For simplicity, generate intermediate code for each node in the parsed AST
        intermediate_code = []

        print("Parsed AST:")
        print(parsed_ast)

        for node in parsed_ast:
            if node[0] == 'LOOP':
                loop_condition = ' '.join(node[1])
                loop_body = ' '.join([str(t[1]) if isinstance(t, tuple) else t for t in node[2]])
                intermediate_code.append(f"LOOP ({loop_condition}) {{ {loop_body} }}")
            elif node[0] == 'FUNCTION_DECLARATION':
                function_name = node[1]
                parameters = node[2]
                intermediate_code.append(f"FUNCTION {function_name} ({', '.join(parameters)})")
            elif node[0] == 'RETURN_STATEMENT':
                expression = ' '.join(node[1])
                intermediate_code.append(f"RETURN {expression}")

        print("Intermediate code:")
        print(intermediate_code)

        return "\n".join(intermediate_code)



    def compile(self, source_code):
        tokens = self.tokenize(source_code)
        parsed_ast = self.parse(tokens)
        self.check_semantics(parsed_ast)
        intermediate_code = self.generate_intermediate_code(parsed_ast)
        return intermediate_code

def measure_time_and_memory(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        start_memory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        result = func(*args, **kwargs)
        end_time = time.time()
        end_memory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        print(f"Time taken: {end_time - start_time} seconds")
        print(f"Memory consumption: {end_memory - start_memory} bytes")
        return result
    return wrapper

@measure_time_and_memory
def compile_c_file(file_path):
    with open(file_path, 'r') as file:
        source_code = file.read()

    compiler = Compiler()
    intermediate_code = compiler.compile(source_code)
    
    # Write intermediate code to a result file
    result_file_path = "result.txt"
    with open(result_file_path, "w") as result_file:
        result_file.write(intermediate_code)
    
    print(f"Intermediate code written to {result_file_path}")

    return intermediate_code

# Example usage
if __name__ == "__main__":
    intermediate_code = compile_c_file("example.c")
