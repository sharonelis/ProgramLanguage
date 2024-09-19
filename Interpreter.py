from Parser import ParserError

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

    def execute_statement(self, statement):
        if isinstance(statement, tuple):
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
            elif statement[0] in ('AND', 'OR'):  # הוספת תמיכה באופרטורים לוגיים
                return self.execute_boolean_expr(statement)
            else:
                raise InterpreterError(f"Unknown statement type: {statement[0]}")
        elif isinstance(statement, str):
            # חפש את ערך המשתנה בסביבה
            if statement in self.variables:
                return self.variables[statement]
            else:
                raise InterpreterError(f"Undefined variable: {statement}")
        else:
            # במקרה של ערכים רגילים כמו מספרים או בוליאנים
            return statement

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
        left = self.convert_to_number(self.execute_statement(statement[1]))
        right = self.convert_to_number(self.execute_statement(statement[2]))
        
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

        if not isinstance(left, bool) or not isinstance(right, bool):
            raise InterpreterError(f"Operands must be boolean: {left}, {right}")

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
            return self.execute_statement(statement[2])
        elif statement[3] is not None:
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
