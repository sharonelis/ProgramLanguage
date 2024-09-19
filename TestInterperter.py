from Interpreter import Interpreter, InterpreterError

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

        print("Running test_function_def_and_call")
        self.test_function_def_and_call()

        print("Running test_division_by_zero")
        self.test_division_by_zero()

        print("Running test_nested_function_calls")
        self.test_nested_function_calls()

        print("Running test_complex_boolean_logic")
        self.test_complex_boolean_logic()

        self.print_results()

    def assert_equal(self, actual, expected, message):
        if actual == expected:
            self.tests_passed += 1
        else:
            self.tests_failed += 1
            print(f"Test failed: {message}")
            print(f"Expected: {expected}, Got: {actual}")

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
        ast = [('ASSIGN', 'x', 10), ('IF', ('GREATER', 'x', 5), ('ASSIGN', 'y', 20), ('ASSIGN', 'y', 0))]
        self.interpreter.interpret(ast)
        self.assert_equal(self.interpreter.variables['y'], 20, "If statement (true branch) failed")

        ast = [('ASSIGN', 'x', 3), ('IF', ('GREATER', 'x', 5), ('ASSIGN', 'y', 20), ('ASSIGN', 'y', 0))]
        self.interpreter.interpret(ast)
        self.assert_equal(self.interpreter.variables['y'], 0, "If statement (false branch) failed")

    def test_function_def_and_call(self):
        self.interpreter.variables = {}  # איפוס משתנים לפני הבדיקה

        # Function definition: def add(a, b) { a + b }
        ast = [('DEFUN', 'add', ['a', 'b'], ('PLUS', 'a', 'b'))]
        self.interpreter.interpret(ast)
        assert 'add' in self.interpreter.functions, "Function definition failed"

        # Function call: add(3, 4)
        ast = [('CALL', 'add', [3, 4])]
        result = self.interpreter.interpret(ast)
        self.assert_equal(result, 7, "Function call failed")

    def test_division_by_zero(self):
     print("Running test: test_division_by_zero")
     ast = [('ASSIGN', 'x', ('DIVIDE', 10, 0))]
     try:
        self.interpreter.interpret(ast)
        print("No error raised for division by zero")  # אם השגיאה לא מתרחשת
        self.assert_equal(False, True, "Division by zero should raise an error")
     except InterpreterError as e:
        print(f"Error raised: {str(e)}")  # הדפסת תוכן השגיאה
        self.assert_equal(str(e), "Division by zero", "Division by zero error handling failed")


    def test_nested_function_calls(self):
        # הגדרת פונקציה שמקוננת קריאה לפונקציה אחרת
        ast = [
            ('DEFUN', 'add', ['a', 'b'], ('PLUS', 'a', 'b')),
            ('DEFUN', 'double_add', ['x', 'y'], ('CALL', 'add', [('CALL', 'add', ['x', 'y']), 'x']))
        ]
        self.interpreter.interpret(ast)

        # קריאה לפונקציה מקוננת
        ast = [('CALL', 'double_add', [2, 3])]
        result = self.interpreter.interpret(ast)
        self.assert_equal(result, 7, "Nested function call failed")

    def test_complex_boolean_logic(self):
     print("Running test_complex_boolean_logic")
     ast = [('ASSIGN', 'x', ('AND', True, ('OR', False, True)))]
     self.interpreter.interpret(ast)
    
    # הדפסת ערך 'x' שנקבע לפי הלוגיקה הבוליאנית
     print(f"Value of 'x' after complex boolean logic: {self.interpreter.variables['x']}")
    
     self.assert_equal(self.interpreter.variables['x'], True, "Complex boolean logic failed")


    def print_results(self):
        print(f"Tests passed: {self.tests_passed}")
        print(f"Tests failed: {self.tests_failed}")

if __name__ == "__main__":
    test_interpreter = TestInterpreter()
    test_interpreter.run()
