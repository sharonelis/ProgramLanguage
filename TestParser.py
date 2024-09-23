from Lexer import Lexer, LexerError
from Parser import Parser, ParserError

class TestParser:
    def __init__(self):
        self.tests_passed = 0
        self.tests_failed = 0
    
    def run(self):
        self.test_arith_expr()
        self.test_string_operations()
        self.test_boolean_expr()
        self.test_if_statement()
        self.test_complex_if_statement()
        self.test_complex_logical_if_statement()
        self.test_function_call()
        self.test_unexpected_token()
        self.test_basic_function_definition()
        self.test_defun_call()
        self.test_more_arith_expr()
        self.test_if_with_block()
        self.test_lambda()
        self.test_and_token()
        self.test_minus_token()
        self.test_nested_minus_expression()
        self.test_if_statement_with_block()
        self.test_missing_closing_brace()
        self.test_extra_closing_brace()

        print(f"Tests passed: {self.tests_passed}")
        print(f"Tests failed: {self.tests_failed}")

    def assert_equal(self, value, expected, message):
        if value == expected:
            self.tests_passed += 1
        else:
            self.tests_failed += 1
            print(f"Test failed: {message}")
            print(f"Expected: {expected}, Got: {value}")

    def test_basic_function_definition(self):
        code = "Defun factorial (n) { n * factorial(n - 1); }"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        parsed = parser.parse()
        expected = [
            ('DEFUN', 'factorial', ['n'], ('MULTIPLY', 'n', ('CALL', 'factorial', [('MINUS', 'n', 1)])))
        ]
        self.assert_equal(parsed, expected, "Basic function definition parsing failed")

    def test_arith_expr(self):
        code = "3 + 5 * (2 - 1)"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        parsed = parser.parse()
        expected = [('PLUS', 3, ('MULTIPLY', 5, ('MINUS', 2, 1)))]
        print(f"Generated AST for arithmetic expression: {parsed}")
        self.assert_equal(parsed, expected, "Arithmetic expression parsing failed")

    def test_boolean_expr(self):
        code = "TRUE && FALSE || TRUE"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        parsed = parser.parse()
        expected = [('OR', ('AND', True, False), True)]
        print(f"Generated AST for boolean expression: {parsed}")
        self.assert_equal(parsed, expected, "Boolean expression parsing failed")

    def test_if_statement(self):
        code = "if (x > 1) { y = 2; } else { y = 3; }"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        parsed = parser.parse()
        expected = [
            ('IF', ('GREATER', 'x', 1), [('ASSIGN', 'y', 2)], [('ASSIGN', 'y', 3)])
        ]
        self.assert_equal(parsed, expected, "If statement parsing failed")

    def test_if_statement_with_block(self):
        code = "if (x > 1) { y = y + 2; z = z - 1; } else { w = w + 5; }"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        parsed = parser.parse()
        expected = [
            ('IF', ('GREATER', 'x', 1), 
                [('ASSIGN', 'y', ('PLUS', 'y', 2)), ('ASSIGN', 'z', ('MINUS', 'z', 1))],
                [('ASSIGN', 'w', ('PLUS', 'w', 5))])
        ]
        print(f"Generated AST for if statement with block: {parsed}")
        self.assert_equal(parsed, expected, "If statement with block parsing failed")

    def test_function_call(self):
        code = "factorial(5);"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        parsed = parser.parse()
        expected = [('CALL', 'factorial', [5])]
        self.assert_equal(parsed, expected, "Function call parsing failed")

    def test_unexpected_token(self):
        code = "Defun factorial (n) { n & factorial(n - 1); }"  # '&' is not expected
        lexer = Lexer(code)
        try:
            tokens = lexer.tokenize()
            print("Test failed: No error was raised for unexpected token '&'")
            self.assert_equal(False, True, "Unexpected token did not raise an error")
        except LexerError as e:
            print(f"Error caught as expected: {e}")
            self.assert_equal(str(e), "Unexpected character: &", "Unexpected token test passed")

    def test_more_arith_expr(self):
        code = "(5 + 3) * 2"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        parsed = parser.parse()
        expected = [('MULTIPLY', ('PLUS', 5, 3), 2)]
        self.assert_equal(parsed, expected, "Arithmetic expression with parentheses parsing failed")

    def test_defun_call(self):
        code = 'Defun add(a, b) { a + b; }'
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        parsed = parser.parse()
        expected = [('DEFUN', 'add', ['a', 'b'], ('PLUS', 'a', 'b'))]
        self.assert_equal(parsed, expected, "Defun call parsing failed")

    def test_complex_if_statement(self):
        code = "if (x >= 10) { x = 100; } else { x = 0; }"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        parsed = parser.parse()
        expected = [('IF', ('GREATER_EQUAL', 'x', 10), [('ASSIGN', 'x', 100)], [('ASSIGN', 'x', 0)])]
        self.assert_equal(parsed, expected, "Complex if statement parsing failed")

    def test_complex_logical_if_statement(self):
        code = "if (x < y && y > z) { max = y; } else { max = z; }"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        parsed = parser.parse()
        expected = [
            ('IF', 
             ('AND', ('LESS', 'x', 'y'), ('GREATER', 'y', 'z')), 
             [('ASSIGN', 'max', 'y')], 
             [('ASSIGN', 'max', 'z')])
        ]
        self.assert_equal(parsed, expected, "Complex logical if statement parsing failed")

    def test_if_with_block(self):
        code = """
        if (x > 5) {
            y = y * 2;
            z = z + 1;
        } else {
            y = y - 1;
        }
        """
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        parsed = parser.parse()
        expected = [
            ('IF', 
                ('GREATER', 'x', 5), 
                [('ASSIGN', 'y', ('MULTIPLY', 'y', 2)), ('ASSIGN', 'z', ('PLUS', 'z', 1))], 
                [('ASSIGN', 'y', ('MINUS', 'y', 1))]
            )
        ]
        self.assert_equal(parsed, expected, "If statement with block parsing failed")

    def test_string_operations(self):
        code = '"Hello" + 5'  # בדיקת חיבור לא חוקי של מחרוזת עם מספר
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        try:
            parser.parse()
            self.assert_equal(False, True, "String operations did not raise an error")
        except ParserError:
            self.assert_equal(True, True, "String operations test passed")

    def test_lambda(self):
        code = "Lambda (a, b) a + b;"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        parsed = parser.parse()
        expected = [
            ('LAMBDA', ['a', 'b'], ('PLUS', 'a', 'b'))
        ]
        self.assert_equal(parsed, expected, "Lambda parsing failed")

    def test_and_token(self):
        code = "x && y"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        parsed = parser.parse()
        expected = [('AND', 'x', 'y')]
        print(f"Generated AST for AND expression: {parsed}")
        self.assert_equal(parsed, expected, "AND token parsing failed")

    def test_minus_token(self):
        code = "a - b"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        parsed = parser.parse()
        expected = [('MINUS', 'a', 'b')]
        print(f"Generated AST for MINUS expression: {parsed}")
        self.assert_equal(parsed, expected, "MINUS token parsing failed")

    def test_nested_minus_expression(self):
        code = "a - (b - c)"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        parsed = parser.parse()
        expected = [('MINUS', 'a', ('MINUS', 'b', 'c'))]
        print(f"Generated AST for nested MINUS expression: {parsed}")
        self.assert_equal(parsed, expected, "Nested MINUS expression parsing failed")

    def test_missing_closing_brace(self):
        code = "if (x > 5) { y = y + 1; z = z - 1;"  # Missing closing brace
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        try:
            parser.parse()
            self.assert_equal(False, True, "Missing closing brace should raise an error")
        except ParserError as e:
            self.assert_equal(str(e), "Expected '}' but reached end of input", "Missing closing brace error handling failed")

    def test_extra_closing_brace(self):
        code = "if (x > 5) { y = y + 1; } }"  # Extra closing brace
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        try:
            parser.parse()
            self.assert_equal(False, True, "Extra closing brace should raise an error")
        except ParserError as e:
            self.assert_equal(str(e), "Unexpected token: <Token type='RBRACE', value=}>", "Extra closing brace error handling failed")

# הפעלת הבדיקות
if __name__ == "__main__":
    test_parser = TestParser()
    test_parser.run()
