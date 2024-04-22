#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

// Token types
typedef enum {
    TOKEN_IDENTIFIER,
    TOKEN_KEYWORD,
    TOKEN_OPERATOR,
    TOKEN_LITERAL,
    TOKEN_UNKNOWN
} TokenType;

// Token structure
typedef struct {
    TokenType type;
    char value[100]; // Assuming a maximum token length of 100 characters
} Token;

// Function to check if a string is a keyword
int isKeyword(char *str) {
    char keywords[32][10] = {
        "auto", "break", "case", "char", "const", "continue", "default", "do",
        "double", "else", "enum", "extern", "float", "for", "goto", "if",
        "int", "long", "register", "return", "short", "signed", "sizeof", "static",
        "struct", "switch", "typedef", "union", "unsigned", "void", "volatile", "while"
    };
    
    for(int i = 0; i < 32; i++) {
        if(strcmp(str, keywords[i]) == 0) {
            return 1; // Keyword found
        }
    }
    
    return 0; // Not a keyword
}

// Function to tokenize input source code
void tokenize(FILE *inputFile, FILE *outputFile) {
    char buffer[100]; // Buffer to store current token
    int bufferIndex = 0;
    
    while (fgets(buffer, sizeof(buffer), inputFile) != NULL) {
        for(int i = 0; i <= strlen(buffer); i++) {
            // If current character is a delimiter or end of string
            if(buffer[i] == ' ' || buffer[i] == '\n' || buffer[i] == '\t' || buffer[i] == ';' || buffer[i] == '(' || buffer[i] == ')' || buffer[i] == '{' || buffer[i] == '}') {
                if(bufferIndex > 0) {
                    buffer[bufferIndex] = '\0'; // Null-terminate the buffer
                    
                    // Identify token type and write to output file
                    Token token;
                    if(isKeyword(buffer)) {
                        token.type = TOKEN_KEYWORD;
                    } else if(isalnum(buffer[0])) {
                        token.type = TOKEN_IDENTIFIER;
                    } else {
                        token.type = TOKEN_UNKNOWN;
                    }
                    
                    strcpy(token.value, buffer);
                    fprintf(outputFile, "Token: Type=%d, Value=%s\n", token.type, token.value);
                    
                    bufferIndex = 0; // Reset buffer index
                }
            }
            // If current character is an operator
            else if(buffer[i] == '+' || buffer[i] == '-' || buffer[i] == '*' || buffer[i] == '/' || buffer[i] == '=') {
                if(bufferIndex > 0) {
                    buffer[bufferIndex] = '\0'; // Null-terminate the buffer
                    
                    // Tokenize identifier or keyword before operator
                    Token token;
                    if(isKeyword(buffer)) {
                        token.type = TOKEN_KEYWORD;
                    } else if(isalnum(buffer[0])) {
                        token.type = TOKEN_IDENTIFIER;
                    } else {
                        token.type = TOKEN_UNKNOWN;
                    }
                    
                    strcpy(token.value, buffer);
                    fprintf(outputFile, "Token: Type=%d, Value=%s\n", token.type, token.value);
                    
                    bufferIndex = 0; // Reset buffer index
                }
                
                // Tokenize operator
                Token token;
                token.type = TOKEN_OPERATOR;
                token.value[0] = buffer[i];
                token.value[1] = '\0'; // Null-terminate the string
                fprintf(outputFile, "Token: Type=%d, Value=%s\n", token.type, token.value);
            }
            // If current character is a literal (assuming integers for simplicity)
            else if(isdigit(buffer[i])) {
                buffer[bufferIndex++] = buffer[i]; // Add character to buffer
            }
            // If current character is part of an identifier
            else if(isalpha(buffer[i]) || buffer[i] == '_') {
                buffer[bufferIndex++] = buffer[i]; // Add character to buffer
            }
            // Ignore whitespace and other characters
        }
    }
}

int main() {
    FILE *inputFile, *outputFile;
    char inputFileName[100], outputFileName[] = "output.txt";
    
    // Input file name
    printf("Enter input file name: ");
    scanf("%s", inputFileName);
    
    // Open input file
    inputFile = fopen(inputFileName, "r");
    if (inputFile == NULL) {
        printf("Error: Unable to open input file.\n");
        return 1;
    }
    
    // Open output file
    outputFile = fopen(outputFileName, "w");
    if (outputFile == NULL) {
        printf("Error: Unable to create output file.\n");
        fclose(inputFile);
        return 1;
    }
    
    // Tokenize input source code and write output to file
    tokenize(inputFile, outputFile);
    
    // Close files
    fclose(inputFile);
    fclose(outputFile);
    
    printf("Tokenization completed. Output written to output.txt.\n");
    
    return 0;
}
