from Lexer import Lexer, LexerError
from Parser import Parser, ParserError


def test_lexer(code):
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    print(f"Tokens for '{code}':")
    for token in tokens:
        print(token)

# דוגמאות בדיקה:
test_lexer('3 + 4')
test_lexer('10 - 2 * 5')
test_lexer('TRUE && FALSE')
test_lexer('Defun add(a, b) { a + b; }')
test_lexer('"Hello World"')
test_lexer('if (x > 5) then y = y + 1; else y = y - 1;')


#Ido's Tests
class TestLexer:
    def __init__(self):
        self.tests_passed = 0
        self.tests_failed = 0
    
    def run(self):
       
        self.test_basic_tokenization()
        self.test_arithmetic_operations()
        self.test_boolean_operations()
        self.test_comparison_operations()
        self.test_string_tokenization()
        self.test_unknown_character()
        self.test_unterminated_string()
        self.test_invalid_character()
        self.assert_equal(True, True, "Test")

        print(f"Tests passed: {self.tests_passed}")
        print(f"Tests failed: {self.tests_failed}")

        #self.parse_function_def()


    def assert_equal(self, value, expected, message):
        if value == expected:
            self.tests_passed += 1
        else:
            self.tests_failed += 1
            print(f"Test failed: {message}")
            print(f"Expected: {expected}, Got: {value}")

    def test_basic_tokenization(self):
        code = "Defun factorial (n) { return n; }"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        expected = [
            ('DEFUN', 'Defun'), ('IDENTIFIER', 'factorial'), ('LPAREN', '('), 
            ('IDENTIFIER', 'n'), ('RPAREN', ')'), ('LBRACE', '{'), 
            ('IDENTIFIER', 'return'), ('IDENTIFIER', 'n'), ('SEMICOLON', ';'), 
            ('RBRACE', '}')
        ]
        self.assert_equal([(t.type, t.value) for t in tokens], expected, "Basic tokenization failed")
    
    def test_arithmetic_operations(self):
        code = "5 + 3 * (2 - 1)"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        expected = [
            ('INTEGER', 5), ('PLUS', '+'), ('INTEGER', 3), 
            ('MULTIPLY', '*'), ('LPAREN', '('), 
            ('INTEGER', 2), ('MINUS', '-'), ('INTEGER', 1), ('RPAREN', ')')
        ]
        self.assert_equal([(t.type, t.value) for t in tokens], expected, "Arithmetic operations failed")
    
    def test_boolean_operations(self):
        code = "TRUE && FALSE || !TRUE"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        expected = [
            ('BOOLEAN', 'TRUE'), ('AND', '&&'), ('BOOLEAN', 'FALSE'), 
            ('OR', '||'), ('NOT', '!'), ('BOOLEAN', 'TRUE')
        ]
        self.assert_equal([(t.type, t.value) for t in tokens], expected, "Boolean operations failed")
    
    def test_comparison_operations(self):
        code = "5 > 3 && 2 <= 1"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        expected = [
            ('INTEGER', 5), ('GREATER', '>'), ('INTEGER', 3), 
            ('AND', '&&'), ('INTEGER', 2), ('LESS_EQUAL', '<='), ('INTEGER', 1)
        ]
        self.assert_equal([(t.type, t.value) for t in tokens], expected, "Comparison operations failed")
    
    def test_string_tokenization(self):
        code = '"hello world"'
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        expected = [('STRING', 'hello world')]
        self.assert_equal([(t.type, t.value) for t in tokens], expected, "String tokenization failed")
    
    def test_unknown_character(self):
        code = "@"
        lexer = Lexer(code)
        try:
            lexer.tokenize()
            self.assert_equal(False, True, "Unknown character did not raise error")
        except LexerError:
            self.assert_equal(True, True, "Unknown character test passed")
    
    def test_unterminated_string(self):
        code = '"hello'
        lexer = Lexer(code)
        try:
            lexer.tokenize()
            self.assert_equal(False, True, "Unterminated string did not raise error")
        except LexerError:
            self.assert_equal(True, True, "Unterminated string test passed")

    def parse_function_def (self):
        code = "Defun factorial (n) { return n; }"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        parsed = parser.parse()
        expected = [
            ('DEFUN', 'factorial', ['n'], ('RETURN', 'n'))
        ]
        self.assert_equal(parsed, expected, "Basic function definition parsing failed")

    def test_invalid_character(self):
       code = "Defun factorial (n) { n * factorial(n - 1); }"
       lexer = Lexer(code)
       tokens = lexer.tokenize()
       print(tokens)

    def test_unexpected_token(self):
        code = "Defun factorial (n) { n & factorial(n - 1); }"  # '&' is not expected
        lexer = Lexer(code)
        try:
            tokens = lexer.tokenize()  # זה אמור להיכשל עם LexerError
            self.assert_equal(False, True, "Unexpected token did not raise an error")
        except LexerError as e:
            # הבדיקה תעבור אם שגיאה אכן הורמה
            self.assert_equal(str(e), "Unexpected character: &", "Unexpected token test passed")
    
if __name__ == "__main__":
    test_lexer = TestLexer()
    test_lexer.run()

