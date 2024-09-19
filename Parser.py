from Lexer import Lexer, LexerError

class ParserError(Exception):
    pass

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[self.pos] if self.tokens else None

    def advance(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = None

    def parse(self):
        return self.parse_program()

    def parse_program(self):
        statements = []
        while self.current_token is not None:
            if self.current_token.type == 'DEFUN':
                statements.append(self.parse_function_def())
            elif self.current_token.type == 'IF':
                statements.append(self.parse_if_statement())
            elif self.current_token.type == 'LAMBDA':  # הוספת תמיכה בלמבדה
                statements.append(self.parse_lambda_expr())
            else:
                statements.append(self.parse_expression())
        return statements

    def parse_lambda_expr(self):
        self.advance()  # Advance past 'LAMBDA'
        if not self.match('LPAREN'):
            raise ParserError("Expected '(' after 'Lambda'")

        # Parse parameters
        params = []
        while self.current_token and self.current_token.type != 'RPAREN':
            params.append(self.current_token.value)
            self.advance()
            if self.current_token.type == 'COMMA':
                self.advance()

        if not self.match('RPAREN'):
            raise ParserError("Expected ')' after parameters")

        # Parse the body of the lambda expression
        body = self.parse_expression()

        return ('LAMBDA', params, body)

    def parse_expression(self):
        if self.current_token.type == 'INTEGER' or self.current_token.type == 'LPAREN':
            # ניתוח ביטוי אריתמטי או ביטוי בתוך סוגריים
            expr = self.parse_arith_expr()
        elif self.current_token.type == 'BOOLEAN':
            expr = self.parse_boolean_expr()
        elif self.current_token.type == 'IDENTIFIER':
            if self.peek() and self.peek().type == 'ASSIGN':
                expr = self.parse_assignment()
            elif self.peek() and self.peek().type in ('GREATER', 'LESS', 'EQUAL', 'NOT_EQUAL', 'GREATER_EQUAL', 'LESS_EQUAL'):
                expr = self.parse_comparison_expr()
            else:
                expr = self.parse_arith_expr()
        elif self.current_token.type in ('GREATER', 'LESS', 'EQUAL', 'NOT_EQUAL', 'GREATER_EQUAL', 'LESS_EQUAL'):
            # טיפול בביטויי השוואה שמופיעים בתחילת הביטוי
            expr = self.parse_comparison_expr()
        elif self.current_token.type == 'STRING':
            # בדיקת ניתוח מחרוזת
            expr = self.parse_string()

            # הרמת שגיאה במקרה של ניסיון לבצע פעולה אריתמטית על מחרוזות
            if self.peek() and self.peek().type in ('PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE'):
                raise ParserError(f"Cannot perform '{self.peek().value}' on strings")

        else:
            raise ParserError(f"Unexpected token: {self.current_token}")

        # נתקדם מעבר לנקודה-פסיק אם היא מופיעה
        if self.current_token and self.current_token.type == 'SEMICOLON':
            self.advance()

        return expr

    # שאר הקוד נשאר זהה
