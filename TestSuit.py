import unittest
from Interpreter import Interpreter  # ייבוא המחלקה Interpreter
from Lexer import Lexer  # ייבוא המחלקה Lexer
from Parser import Parser  # ייבוא המחלקה Parser

class TestSuite(unittest.TestCase):
    def run_code(self, code):
        print(f"Running code:\n{code}\n{'-'*40}")
        
        # יצירת אובייקט Lexer עם הקוד
        lexer = Lexer(code)
        print("Lexer created.")
        
        # ביצוע טוקניזציה של הקוד
        tokens = lexer.tokenize()
        print(f"Tokens:\n{tokens}\n{'-'*40}")
        
        # יצירת אובייקט Parser עם הטוקנים
        parser = Parser(tokens)
        print("Parser created.")
        
        # ניתוח והפקת AST
        ast = parser.parse()
        print(f"AST:\n{ast}\n{'-'*40}")
        
        # יצירת אובייקט Interpreter עם ה-AST
        interpreter = Interpreter()
        print("Interpreter created.")
        
        # ביצוע אינטרפרטציה והפקת התוצאה
        result = interpreter.interpret(ast)
        print(f"Result:\n{result}\n{'='*40}\n")
        
        return result

    # בדיקות לביטויים אריתמטיים
    def test_arith_expr(self):
        print("Test: Arithmetic Expression")
        code = "3 + 4"
        expected = 7
        result = self.run_code(code)
        print(f"Expected: {expected}, Got: {result}\n{'#'*40}\n")
        self.assertEqual(result, expected)

    # בדיקות לביטויים לוגיים
    def test_boolean_expr(self):
        print("Test: Boolean Expression")
        code = "TRUE && FALSE"
        expected = False
        result = self.run_code(code)
        print(f"Expected: {expected}, Got: {result}\n{'#'*40}\n")
        self.assertEqual(result, expected)

    

    # בדיקות של הגדרת פונקציות וקריאה לפונקציות
    def test_function_def_and_call(self):
        print("Test: Function Definition and Call")
        code = "Defun add(a, b) { a + b; } add(2, 3)"
        expected = 5
        result = self.run_code(code)
        print(f"Expected: {expected}, Got: {result}\n{'#'*40}\n")
        self.assertEqual(result, expected)

   
    # בדיקות שגיאות תחביר
    def test_syntax_error(self):
        print("Test: Syntax Error")
        code = "3 +"
        try:
            self.run_code(code)
        except Exception as e:
            print(f"Caught Exception: {e}\n{'#'*40}\n")
            self.assertIsInstance(e, Exception)
        else:
            self.fail("Exception was not raised for syntax error.")

    # בדיקות עבור משתנה לא מוגדר
    def test_undefined_variable(self):
        print("Test: Undefined Variable")
        code = "x + 5"
        try:
            self.run_code(code)
        except Exception as e:
            print(f"Caught Exception: {e}\n{'#'*40}\n")
            self.assertIsInstance(e, Exception)
        else:
            self.fail("Exception was not raised for undefined variable.")

    # בדיקות של משתנים מקומיים וגלובליים
    def test_scope_handling(self):
        print("Test: Scope Handling")
        code = "Defun foo() { x = 10; } foo(); x"
        try:
            self.run_code(code)
        except Exception as e:
            print(f"Caught Exception: {e}\n{'#'*40}\n")
            self.assertIsInstance(e, Exception)
        else:
            self.fail("Exception was not raised for undefined global variable.")

   
    def test_runtime_error(self):
        print("Test: Runtime Error (Division by Zero)")
        code = "10 / 0"
        try:
            self.run_code(code)
        except Exception as e:
            print(f"Caught Exception: {e}\n{'#'*40}\n")
            self.assertIsInstance(e, Exception)
        else:
            self.fail("Exception was not raised for runtime error (division by zero).")

if __name__ == "__main__":
    unittest.main()
