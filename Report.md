# Custom Language Interpreter Project Report

## Introduction

This report provides an overview of the design decisions, challenges faced, and solutions implemented during the development of a custom language interpreter. The interpreter supports basic arithmetic, boolean logic, conditional expressions, function definitions and calls, lambda expressions, and recursion. The goal was to create an interpreter that could execute commands both interactively and from a program file, effectively handling various language features.

## Design Decisions

### Language Features

1. **Basic Arithmetic and Boolean Operations**:
   - The language includes support for basic arithmetic operations (`+`, `-`, `*`, `/`, `%`) and boolean operations (`&&`, `||`, `!`).

2. **Comparison Operations**:
   - Support for comparison operators (`==`, `!=`, `<`, `>`, `<=`, `>=`) was included to enable conditional logic.

3. **Conditional Expressions**:
   - `if-else` expressions were implemented to allow for conditional execution of code.

4. **Function Definitions and Calls**:
   - The language supports defining functions using the `Defun` keyword and calling them with arguments.

5. **Lambda Expressions**:
   - Lambda expressions were added to allow for anonymous functions and higher-order functions.

6. **Recursion**:
   - Recursion was supported to simulate iterative processes and to enable complex function definitions.

7. **Interactive Mode and Program Execution**:
   - The interpreter can run in interactive mode, allowing users to enter commands line by line, and in program execution mode, running a full program from a file.

### Abstract Syntax Tree (AST)

The interpreter uses an Abstract Syntax Tree (AST) to represent the parsed structure of the code. Different types of nodes represent numbers, booleans, identifiers, binary operations, unary operations, function definitions, function calls, lambda expressions, and if-else expressions.

### Environment and Call Stack

An environment was designed to manage variable scopes and function environments. A call stack was implemented to manage function calls and recursion, ensuring proper handling of nested function calls and scope resolution.

## Challenges Faced

### 1. Error Handling

**Challenge**:
- Providing meaningful and accurate error messages was crucial for debugging and user experience. Ensuring that the interpreter could identify and report errors accurately, such as type mismatches, undefined variables, and syntax errors, was challenging.

**Example**:
- When a variable is used before it is defined, the interpreter should report an `Undefined Variable` error.

#### Solution:
- Implemented comprehensive error handling throughout the interpreter. Custom exceptions were used to capture specific error conditions, and detailed error messages were provided to indicate the nature and location of errors.

```python
class LexerError(Exception):
    def __init__(self, message, pos):
        super().__init__(message)
        self.pos = pos
