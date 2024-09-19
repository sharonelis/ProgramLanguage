import unittest
from Interpreter import Interpreter  # ייבוא המחלקה Interpreter
from Lexer import Lexer  # ייבוא המחלקה Lexer
from Parser import Parser  # ייבוא המחלקה Parser

class TestSuite(unittest.TestCase):
    def run_code(self, code):
        lexer = Lexer(code)  # יצירת אובייקט Lexer עם הקוד
        tokens = lexer.tokenize()  # ביצוע טוקניזציה של הקוד
        parser = Parser(tokens)  # יצירת אובייקט Parser עם הטוקנים
        ast = parser.parse()  # ניתוח והפקת AST
        interpreter = Interpreter()  # יצירת אובייקט Interpreter עם ה-AST
        return interpreter.interpret(ast)  # ביצוע אינטרפרטציה והפקת התוצאה

    # בדיקות לביטויים אריתמטיים
    def test_arith_expr(self):
        code = "3 + 4"
        self.assertEqual(self.run_code(code), 7)

    # בדיקות לביטויים לוגיים
    def test_boolean_expr(self):
        code = "TRUE && FALSE"
        self.assertEqual(self.run_code(code), False)

    # בדיקות לביטויים של השוואות
    def test_compare_expr(self):
        code = "5 > 3"
        self.assertEqual(self.run_code(code), True)

    # בדיקות של הגדרת פונקציות וקריאה לפונקציות
    def test_function_def_and_call(self):
        code = "Defun add(a, b) a + b; add(2, 3)"
        self.assertEqual(self.run_code(code), 5)

    # בדיקות לפונקציות רקורסיביות
    def test_recursion(self):
        code = "Defun fact(n) if n == 0 1 else n * fact(n - 1); fact(5)"
        self.assertEqual(self.run_code(code), 120)

    # בדיקות טיפול במחרוזות
    def test_string_handling(self):
        code = '"hello" + " world"'
        self.assertEqual(self.run_code(code), 'hello world')

    # בדיקות שגיאות תחביר
    def test_syntax_error(self):
        code = "3 +"
        with self.assertRaises(Exception):
            self.run_code(code)

    # בדיקות עבור משתנה לא מוגדר
    def test_undefined_variable(self):
        code = "x + 5"
        with self.assertRaises(Exception):
            self.run_code(code)

    # בדיקות של משתנים מקומיים וגלובליים
    def test_scope_handling(self):
        code = "Defun foo() { x = 10; } foo(); x"
        with self.assertRaises(Exception):
            self.run_code(code)  # משתנה 'x' לא מוגדר מחוץ לפונקציה

    # בדיקות עבור תנאים מקוננים
    def test_nested_conditions(self):
        code = "if (5 > 3) { if (2 < 4) { 1 } else { 0 } }"
        self.assertEqual(self.run_code(code), 1)

    # בדיקות שגיאות בזמן ריצה, לדוגמה חלוקה באפס
    def test_runtime_error(self):
        code = "10 / 0"
        with self.assertRaises(Exception):
            self.run_code(code)

if __name__ == "__main__":
    unittest.main()
