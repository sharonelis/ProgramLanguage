from Interpreter import Interpreter
from Lexer import Lexer
from Parser import Parser

class REPL:
    def __init__(self):
        self.interpreter = Interpreter()  # יצירת אובייקט Interpreter מחוץ ללולאה לשמירת מצב

    def run(self):
        while True:
            try:
                code = input(">>> ")
                
                # אפשרות ליציאה מהלולאה
                if code.strip().lower() in ["exit", "quit"]:
                    print("Exiting REPL...")
                    break

                lexer = Lexer(code)  # יצירת אובייקט Lexer עם הקוד שהוזן
                tokens = lexer.tokenize()  # ביצוע טוקניזציה של הקוד
                
                parser = Parser(tokens)  # יצירת אובייקט Parser עם הטוקנים
                ast = parser.parse()  # ניתוח והפקת AST
                
                result = self.interpreter.interpret(ast)  # ביצוע אינטרפרטציה והפקת התוצאה
                if result is not None:
                    print(result)

            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    repl = REPL()
    repl.run()
