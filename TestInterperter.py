from Interpreter import Interpreter, InterpreterError
from Lexer import Lexer
from Parser import Parser

class TestInterpreter:
    def __init__(self):
        self.interpreter = Interpreter()
        self.tests_passed = 0
        self.tests_failed = 0

    def run(self):
        print("Running test_simple_assignment")
        self.test_simple_assignment()

        print("Running test_arithmetic_operations")
        self.test_arithmetic_operations()

        print("Running test_if_statements")
        self.test_if_statements()

        print("Running test_if_statement_with_block")  # בדיקה לטיפול בסוגריים מסולסלים במשפט if
        self.test_if_statement_with_block()

        print("Running test_function_def_and_call")
        self.test_function_def_and_call()

        print("Running test_division_by_zero")
        self.test_division_by_zero()

        print("Running test_nested_function_calls")
        self.test_nested_function_calls()

        print("Running test_complex_boolean_logic")
        self.test_complex_boolean_logic()

        print("Running test_lambda_execution")
        self.test_lambda_execution()

        print("Running test_lambda_file_execution")
        self.test_lambda_file_execution()

        print("Running test_minus_operation")
        self.test_minus_operation()

        print("Running test_block_statements")  # בדיקה לטיפול בסוגריים מסולסלים
        self.test_block_statements()

        self.print_results()

    def assert_equal(self, actual, expected, message):
        if actual == expected:
            self.tests_passed += 1
        else:
            self.tests_failed += 1
            print(f"Test failed: {message}")
            print(f"Expected: {expected}, Got: {actual}")

    def test_if_statement_with_block(self):
        
        ast = [
            ('ASSIGN', 'x', 5),
            ('IF', ('GREATER', 'x', 3),
                [
                    ('ASSIGN', 'y', ('PLUS', 'x', 2)),
                    ('ASSIGN', 'z', ('MINUS', 'y', 1))
                ],
                [
                    ('ASSIGN', 'y', 0),
                    ('ASSIGN', 'z', 0)
                ])
        ]
        self.interpreter.interpret(ast)
        self.assert_equal(self.interpreter.variables['y'], 7, "If statement with block (true branch) failed")
        self.assert_equal(self.interpreter.variables['z'], 6, "If statement with block (true branch) failed")

        ast = [
            ('ASSIGN', 'x', 2),
            ('IF', ('GREATER', 'x', 3),
                [
                    ('ASSIGN', 'y', ('PLUS', 'x', 2)),
                    ('ASSIGN', 'z', ('MINUS', 'y', 1))
                ],
                [
                    ('ASSIGN', 'y', 0),
                    ('ASSIGN', 'z', 0)
                ])
        ]
        self.interpreter.interpret(ast)
        self.assert_equal(self.interpreter.variables['y'], 0, "If statement with block (false branch) failed")
        self.assert_equal(self.interpreter.variables['z'], 0, "If statement with block (false branch) failed")

    def test_simple_assignment(self):
        ast = [('ASSIGN', 'x', 10)]
        self.interpreter.interpret(ast)
        self.assert_equal(self.interpreter.variables['x'], 10, "Simple assignment failed")

    def test_arithmetic_operations(self):
        ast = [('ASSIGN', 'x', ('PLUS', 10, 5))]
        self.interpreter.interpret(ast)
        self.assert_equal(self.interpreter.variables['x'], 15, "Arithmetic addition failed")

        ast = [('ASSIGN', 'y', ('MULTIPLY', 3, 4))]
        self.interpreter.interpret(ast)
        self.assert_equal(self.interpreter.variables['y'], 12, "Arithmetic multiplication failed")

    def test_if_statements(self):
     self.interpreter.variables = {}
     ast = [('ASSIGN', 'x', 10), ('IF', ('GREATER', 'x', 5), ('ASSIGN', 'y', 20), ('ASSIGN', 'y', 0))]
     self.interpreter.interpret(ast)
     print(f"Variables after true branch execution: {self.interpreter.variables}")
     self.assert_equal(self.interpreter.variables.get('y'), 20, "If statement (true branch) failed")

     ast = [('ASSIGN', 'x', 3), ('IF', ('GREATER', 'x', 5), ('ASSIGN', 'y', 20), ('ASSIGN', 'y', 0))]
     self.interpreter.interpret(ast)
     print(f"Variables after false branch execution: {self.interpreter.variables}")
     self.assert_equal(self.interpreter.variables.get('y'), 0, "If statement (false branch) failed")


     ast = [('ASSIGN', 'x', 3), ('IF', ('GREATER', 'x', 5), ('ASSIGN', 'y', 20), ('ASSIGN', 'y', 0))]
     self.interpreter.interpret(ast)
     print(f"Variables after else block: {self.interpreter.variables}")
     self.assert_equal(self.interpreter.variables['y'], 0, "If statement (false branch) failed")


    def test_function_def_and_call(self):
        self.interpreter.variables = {}

        ast = [('DEFUN', 'add', ['a', 'b'], ('PLUS', 'a', 'b'))]
        self.interpreter.interpret(ast)
        assert 'add' in self.interpreter.functions, "Function definition failed"

        ast = [('CALL', 'add', [3, 4])]
        result = self.interpreter.interpret(ast)
        self.assert_equal(result, 7, "Function call failed")

    def test_division_by_zero(self):
        ast = [('ASSIGN', 'x', ('DIVIDE', 10, 0))]
        try:
            self.interpreter.interpret(ast)
            print("No error raised for division by zero")
            self.assert_equal(False, True, "Division by zero should raise an error")
        except InterpreterError as e:
            print(f"Error raised: {str(e)}")
            self.assert_equal(str(e), "Division by zero", "Division by zero error handling failed")

    def test_nested_function_calls(self):
        ast = [
            ('DEFUN', 'add', ['a', 'b'], ('PLUS', 'a', 'b')),
            ('DEFUN', 'double_add', ['x', 'y'], ('CALL', 'add', [('CALL', 'add', ['x', 'y']), 'x']))
        ]
        self.interpreter.interpret(ast)

        ast = [('CALL', 'double_add', [2, 3])]
        result = self.interpreter.interpret(ast)
        self.assert_equal(result, 7, "Nested function call failed")

    def test_complex_boolean_logic(self):

        result = self.interpreter.interpret([('AND', True, False)])
        assert result == False, f"Expected False, got {result}"

        result = self.interpreter.interpret([('OR', True, False)])
        assert result == True, f"Expected True, got {result}"

        result = self.interpreter.interpret([('AND', ('GREATER', 5, 3), ('EQUAL', 4, 4))])
        assert result == True, f"Expected True, got {result}"

        result = self.interpreter.interpret([('OR', ('LESS', 5, 3), ('NOT_EQUAL', 2, 1))])
        assert result == True, f"Expected True, got {result}"

        result = self.interpreter.interpret([('OR', ('AND', ('GREATER', 5, 3), ('EQUAL', 4, 4)), ('NOT_EQUAL', 2, 1))])
        assert result == True, f"Expected True, got {result}"

        result = self.interpreter.interpret([('AND', ('OR', True, False), False)])
        assert result == False, f"Expected False, got {result}"

        print("test_complex_boolean_logic passed")

    def test_lambda_execution(self):
        code = "Lambda (a, b) a + b;"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()

        print(f"Generated AST for lambda: {ast}")

        lambda_func = self.interpreter.interpret(ast)
        result = lambda_func(3, 4)
        self.assert_equal(result, 7, "Lambda execution failed")

    def test_lambda_file_execution(self):
        try:
            file_path = "test.lambda"
            ast = self.interpreter.interpret_from_file(file_path)
            print(f"Generated AST for file: {ast}")
            print("Lambda file execution succeeded.")
        except Exception as e:
            print(f"Error occurred while executing lambda file: {str(e)}")
            self.assert_equal(False, True, "Lambda file execution failed")

    def test_minus_operation(self):

        ast = [('ASSIGN', 'z', ('MINUS', 10, 3))]
        self.interpreter.interpret(ast)
        self.assert_equal(self.interpreter.variables['z'], 7, "Minus operation failed")

    def test_block_statements(self):

        ast = [
            ('ASSIGN', 'x', 5),
            ('IF', ('GREATER', 'x', 3),  # תנאי בודק אם x גדול מ-3
                [
                    ('ASSIGN', 'y', ('PLUS', 'x', 2)),
                    ('ASSIGN', 'z', ('MINUS', 'y', 1))
                ],
                [
                    ('ASSIGN', 'y', 0),
                    ('ASSIGN', 'z', 0)
                ])
        ]
        self.interpreter.interpret(ast)
        self.assert_equal(self.interpreter.variables['y'], 7, "Block statement (true branch) failed")
        self.assert_equal(self.interpreter.variables['z'], 6, "Block statement (true branch) failed")

    def print_results(self):
        print(f"Tests passed: {self.tests_passed}")
        print(f"Tests failed: {self.tests_failed}")


if __name__ == "__main__":
    test_interpreter = TestInterpreter()
    test_interpreter.run()
