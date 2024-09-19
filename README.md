# Custom Language Interpreter User Guide

## Introduction

This guide explains how to run the custom language interpreter that was implemented using the `Lexer`, `Parser`, `Interpreter`, and `REPL` classes. The interpreter is designed to execute custom `.lambda` programs in both interactive mode and program execution mode.

## Prerequisites

- Ensure you have Python installed on your system.
- Ensure all necessary files are placed in the same directory: `Lexer.py`, `Parser.py`, `Interpreter.py`, and `REPL.py`.
- Save your language programs with the `.lambda` suffix.

## Running the Interpreter

### Interactive Mode

1. Open a terminal or command prompt.
2. Navigate to the directory containing the interpreter files.
3. Run the following command to start the interactive mode:

    ```sh
    python REPL.py
    ```

4. You will see the prompt `Lambda>`. You can now enter commands one by one. After typing a command, press Enter to execute it and see the result.

    Example:

    ```plaintext
    Lambda> 2 + 3
    5
    Lambda> def add(x, y): x + y
    Function created!
    Lambda> add(2, 3)
    5
    Lambda> (lambda x: x + 1)(4)
    5
    Lambda> if True: 1 else: 0
    1
    ```

    To exit the interactive mode, press `Ctrl+C` or type `exit`.

### Full Program Execution Mode

1. Open a terminal or command prompt.
2. Navigate to the directory containing the interpreter files and your `.lambda` program file.
3. Run the following command:

    ```sh
    python REPL.py your_program.lambda
    ```

    Replace `your_program.lambda` with the name of your `.lambda` file.

    Example:

    Assuming you have a file named `test.lambda` with the following content:

    ```plaintext
    # Define functions
    def add(a, b): a + b
    def multiply(a, b): a * b
    def factorial(n): if n == 0: 1 else: n * factorial(n - 1)

    # Function calls
    add(2, 3)      # Expected output: 5
    multiply(3, 4) # Expected output: 12
    factorial(5)   # Expected output: 120

    # Lambda function calls
    (lambda x: x + 1)(10)   # Expected output: 11
    (lambda f: f(2))(lambda x: x + 3) # Expected output: 5

    # Nested function call
    def make_adder(x): lambda y: x + y
    (make_adder(10))(5) # Expected output: 15
    ```

    Run the following command:

    ```sh
    python REPL.py test.lambda
    ```

    You will see the interpreter execute each line and print the results:

    ```plaintext
    Executing: def add(a, b): a + b
    Function created!
    Executing: def multiply(a, b): a * b
    Function created!
    Executing: def factorial(n): if n == 0: 1 else: n * factorial(n - 1)
    Function created!
    Executing: add(2, 3)
    5
    Executing: multiply(3, 4)
    12
    Executing: factorial(5)
    120
    Executing: (lambda x: x + 1)(10)
    11
    Executing: (lambda f: f(2))(lambda x: x + 3)
    5
    Executing: def make_adder(x): lambda y: x + y
    Function created!
    Executing: (make_adder(10))(5)
    15
    ```

## Conclusion

This guide explains how to run the custom language interpreter in both interactive and program execution modes. By following these instructions, you will be able to test and run `.lambda` programs efficiently. Make sure to check that Python is installed correctly and that your program files are in the correct format.
