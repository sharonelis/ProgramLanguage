from Parser import ParserError
from Lexer import Lexer
from Parser import Parser


class InterpreterError(Exception):
    pass

class Interpreter:
    def __init__(self):
        self.variables = {}
        self.functions = {}

    def interpret(self, ast):
        result = None
        for statement in ast:
            result = self.execute_statement(statement)
        return result  # החזרת התוצאה הסופית

    def interpret_from_file(self, file_path):
        try:
            # קריאת תוכן הקובץ
            with open(file_path, 'r') as file:
                code = file.read()
            
            # ביצוע תהליך ניתוח לקסיקלי ותחבירי
            lexer = Lexer(code)
            tokens = lexer.tokenize()

            parser = Parser(tokens)
            ast = parser.parse()

            # הרצת הקוד מהעץ התחבירי שנוצר
            self.interpret(ast)
            print("File executed successfully.")
        except Exception as e:
            print(f"Error while executing file: {str(e)}")

    def execute_statement(self, statement):
     if isinstance(statement, list):  # אם מדובר בבלוק של פקודות (רשימה)
        result = None
        for expr in statement:
            result = self.execute_statement(expr)
        return result  # החזרת תוצאה אחרונה מבלוק הפקודות

     if isinstance(statement, tuple):
        if statement[0] == 'NEGATE':
            return -self.execute_statement(statement[1])
        if statement[0] == 'IF':
            return self.execute_if_statement(statement)
        elif statement[0] in ('PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE'):
            return self.execute_arith_expr(statement)
        elif statement[0] in ('GREATER', 'LESS', 'EQUAL', 'NOT_EQUAL', 'GREATER_EQUAL', 'LESS_EQUAL'):
            return self.execute_comparison_expr(statement)
        elif statement[0] == 'ASSIGN':
            return self.execute_assignment(statement)
        elif statement[0] == 'DEFUN':
            return self.execute_function_def(statement)
        elif statement[0] == 'CALL':
            return self.execute_function_call(statement)
        elif statement[0] == 'LAMBDA':
            return self.execute_lambda(statement)
        elif statement[0] in ('AND', 'OR'):
            return self.execute_boolean_expr(statement)
        else:
            raise InterpreterError(f"Unknown statement type: {statement[0]}")

     elif isinstance(statement, str):
        # טיפול במחרוזות - אם זו מחרוזת היא תוחזר כמו שהיא
        if statement.startswith('"') and statement.endswith('"'):
            return statement.strip('"')
        if statement in self.variables:
            return self.variables[statement]
        else:
            raise InterpreterError(f"Undefined variable: {statement}")

     else:
        return statement

    def execute_block(self, block):
     """Execute a block of statements."""
     result = None
     for stmt in block:
        result = self.execute_statement(stmt)
     return result

    def execute_if_statement(self, statement):
     condition = self.execute_statement(statement[1])
     if condition:
        return self.execute_block(statement[2])  # Execute then branch
     elif statement[3] is not None:
        return self.execute_block(statement[3])  # Execute else branch if it exists




    def convert_to_number(self, value):
        """המרה של ערכים למספרים אם מדובר במחרוזות או משתנים"""
        if isinstance(value, str):
            if value in self.variables:
                value = self.variables[value]
            else:
                raise InterpreterError(f"Variable '{value}' is not defined")
            
            if isinstance(value, str) and value.isdigit():
                return int(value)
            try:
                return float(value)
            except ValueError:
                raise InterpreterError(f"Cannot convert '{value}' to a number")
        return value

    def execute_arith_expr(self, statement):
        left = self.execute_statement(statement[1])
        right = self.execute_statement(statement[2])

        # בדיקת חיבור מחרוזות
        if isinstance(left, str) or isinstance(right, str):
            raise InterpreterError(f"Cannot perform arithmetic on strings: {left}, {right}")

        # המרה למספרים רק אם מדובר בביטויים אריתמטיים
        left = self.convert_to_number(left)
        right = self.convert_to_number(right)

        if statement[0] == 'PLUS':
            return left + right
        elif statement[0] == 'MINUS':
            return left - right
        elif statement[0] == 'MULTIPLY':
            return left * right
        elif statement[0] == 'DIVIDE':
            if right == 0:
                raise InterpreterError("Division by zero")
            return left / right
        else:
            raise InterpreterError(f"Unknown arithmetic operator: {statement[0]}")

    def execute_comparison_expr(self, statement):
        left = self.convert_to_number(self.execute_statement(statement[1]))
        right = self.convert_to_number(self.execute_statement(statement[2]))
        
        if statement[0] == 'GREATER':
            return left > right
        elif statement[0] == 'LESS':
            return left < right
        elif statement[0] == 'EQUAL':
            return left == right
        elif statement[0] == 'NOT_EQUAL':
            return left != right
        elif statement[0] == 'GREATER_EQUAL':
            return left >= right
        elif statement[0] == 'LESS_EQUAL':
            return left <= right

    def execute_boolean_expr(self, statement):
        left = self.execute_statement(statement[1])
        right = self.execute_statement(statement[2])

        if not isinstance(left, bool):
            raise InterpreterError(f"Left operand must be boolean: {left}")
        if not isinstance(right, bool):
            raise InterpreterError(f"Right operand must be boolean: {right}")

        if statement[0] == 'AND':
            return left and right
        elif statement[0] == 'OR':
            return left or right
        else:
            raise InterpreterError(f"Unknown boolean operator: {statement[0]}")

    def execute_assignment(self, statement):
        var_name = statement[1]
        value = self.execute_statement(statement[2])
        self.variables[var_name] = value
        return value

    def execute_if_statement(self, statement):
        condition = self.execute_statement(statement[1])
        if condition:
            # בדיקה אם then_branch הוא בלוק (רשימה של פקודות)
            if isinstance(statement[2], list):
                for stmt in statement[2]:
                    result = self.execute_statement(stmt)
                return result
            else:
                return self.execute_statement(statement[2])
        elif statement[3] is not None:
            # בדיקה אם else_branch הוא בלוק (רשימה של פקודות)
            if isinstance(statement[3], list):
                for stmt in statement[3]:
                    result = self.execute_statement(stmt)
                return result
            else:
                return self.execute_statement(statement[3])

    def execute_function_def(self, statement):
        func_name = statement[1]
        params = statement[2]
        body = statement[3]
        self.functions[func_name] = (params, body)
    
    def execute_function_call(self, statement):
        func_name = statement[1]
        args = statement[2]

        if func_name not in self.functions:
            raise InterpreterError(f"Function '{func_name}' not defined")

        params, body = self.functions[func_name]
        prev_vars = self.variables.copy()

        for param, arg in zip(params, args):
            self.variables[param] = self.execute_statement(arg)

        result = self.execute_statement(body)
        self.variables = prev_vars
        return result

    def execute_lambda(self, statement):
        params = statement[1]
        body = statement[2]

        def lambda_func(*args):
            prev_vars = self.variables.copy()

            for param, arg in zip(params, args):
                self.variables[param] = arg

            result = self.execute_statement(body)

            self.variables = prev_vars
            return result

        return lambda_func
