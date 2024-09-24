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
            else:
                statements.append(self.parse_expression())
        return statements

    def parse_expression(self):
        if self.current_token.type == 'INTEGER' or self.current_token.type == 'LPAREN':
            expr = self.parse_arith_expr()
        elif self.current_token.type == 'BOOLEAN':
            expr = self.parse_boolean_expr()
        elif self.current_token.type == 'IDENTIFIER':
            if self.peek() and self.peek().type == 'ASSIGN':
                expr = self.parse_assignment()
            elif self.peek() and self.peek().type in ('GREATER', 'LESS', 'EQUAL', 'NOT_EQUAL', 'GREATER_EQUAL', 'LESS_EQUAL'):
                expr = self.parse_comparison_expr()
            elif self.peek() and self.peek().type in ('AND', 'OR'):
                expr = self.parse_boolean_expr()
            else:
                expr = self.parse_arith_expr()
        elif self.current_token.type in ('GREATER', 'LESS', 'EQUAL', 'NOT_EQUAL', 'GREATER_EQUAL', 'LESS_EQUAL'):
            expr = self.parse_comparison_expr()
        elif self.current_token.type == 'STRING':
            expr = self.parse_string()
            if self.peek() and self.peek().type in ('PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE'):
                raise ParserError(f"Cannot perform '{self.peek().value}' on strings")
        elif self.current_token.type == 'LAMBDA':
            expr = self.parse_lambda()
        elif self.current_token.type == 'IF':
            expr = self.parse_if_statement()
        elif self.current_token.type in ('AND', 'OR'):
            expr = self.parse_boolean_expr()
        else:
            raise ParserError(f"Unexpected token: {self.current_token}")

        if self.current_token and self.current_token.type == 'SEMICOLON':
            self.advance()

        return expr

    def parse_arith_expr(self):
        left = self.parse_term()
        while self.current_token and self.current_token.type in ('PLUS', 'MINUS'):
            op = self.current_token.type
            self.advance()

            if not self.current_token:
                raise ParserError("Unexpected end of expression after operator")

            if self.current_token.type not in ('INTEGER', 'IDENTIFIER', 'LPAREN'):
                raise ParserError(f"Unexpected token '{self.current_token.value}' after operator {op}")

            right = self.parse_term()
            left = (op, left, right)
        return left

    def parse_term(self):
        left = self.parse_factor()
        while self.current_token and self.current_token.type in ('MULTIPLY', 'DIVIDE', 'MODULO'):
            op = self.current_token.type
            self.advance()
            if not self.current_token:
                raise ParserError("Incomplete expression, expected a term after operator")
            right = self.parse_factor()
            left = (op, left, right)
        return left

    def parse_factor(self):
        token = self.current_token
        if not token:
            raise ParserError("Unexpected end of input, expected a factor")

        if token.type == 'MINUS':
            self.advance()
            if not self.current_token:
                raise ParserError("Unexpected end of expression after '-'")
            return ('NEGATE', self.parse_factor())

        if token.type == 'INTEGER':
            self.advance()
            return token.value
        elif token.type == 'STRING':
            self.advance()
            return token.value
        elif token.type == 'BOOLEAN':
            self.advance()
            return token.value == 'TRUE'
        elif token.type == 'IDENTIFIER':
            if self.peek() and self.peek().type == 'LPAREN':
                return self.parse_function_call()
            else:
                self.advance()
                return token.value
        elif token.type == 'LPAREN':
            self.advance()
            expr = self.parse_expression()
            if not self.match('RPAREN'):
                raise ParserError("Expected ')' after expression")
            return expr
        else:
            raise ParserError(f"Unexpected token in factor: {token}")

    def parse_boolean_expr(self):
        left = self.parse_comparison_expr()
        while self.current_token and self.current_token.type in ('AND', 'OR'):
            op = self.current_token.type
            self.advance()
            right = self.parse_comparison_expr()
            left = (op, left, right)
        return left

    def parse_if_statement(self):
     print("Starting parse_if_statement")
     self.advance()  # Advance past 'IF'
     print(f"After advancing past IF, current token: {self.current_token}")

     if not self.match('LPAREN'):
        raise ParserError("Expected '(' after 'IF'")

     print(f"After matching '(', current token: {self.current_token}")
     condition = self.parse_boolean_or_comparison_expr()
     print(f"Parsed condition: {condition}")
     print(f"Current token after condition: {self.current_token}")

     if not self.match('RPAREN'):
        raise ParserError("Expected ')' after condition")

     print(f"After matching ')', current token: {self.current_token}")

    # תיקון: ביטול הבדיקה על THEN
     print("Parsing then_branch")
     then_branch = self.parse_block_or_expression()

     print(f"Parsed then_branch: {then_branch}")

     if isinstance(then_branch, list) and 'return' in then_branch:
        # אם יש שימוש ב-return, נתעלם מהמילה ונחזיר את הביטוי הסופי
        then_branch = [exp for exp in then_branch if exp != 'return']

     if self.match('ELSE'):
        print("Found 'ELSE', parsing else_branch")
        else_branch = self.parse_block_or_expression()

        if isinstance(else_branch, list) and 'return' in else_branch:
            # גם ב-else, אם יש return, נוודא רק את הביטוי
            else_branch = [exp for exp in else_branch if exp != 'return']

        print(f"Parsed else_branch: {else_branch}")
        return ('IF', condition, then_branch, else_branch)

     print(f"Returning IF statement without ELSE branch")
     return ('IF', condition, then_branch, None)

    def parse_block_or_expression(self):
     if self.match('LBRACE'):
        statements = []
        while not self.match('RBRACE'):
            if not self.current_token:  # אם נגמרו הטוקנים לפני סוגר המסולסל
                raise ParserError("Expected '}' but reached end of input")  # שינוי ההודעה כאן
            statements.append(self.parse_expression())
        return statements
     else:
        return self.parse_expression()


    def parse_function_def(self):
        self.advance()  # Advance past 'DEFUN'
        func_name = self.current_token.value
        self.advance()  # Advance past function name
        if not self.match('LPAREN'):
            raise ParserError("Expected '(' after function name")
        
        params = []
        while self.current_token and self.current_token.type != 'RPAREN':
            params.append(self.current_token.value)
            self.advance()
            if self.current_token.type == 'COMMA':
                self.advance()
        
        if not self.match('RPAREN'):
            raise ParserError("Expected ')' after parameters")
        
        if not self.match('LBRACE'):
            raise ParserError("Expected '{' to start function body")
        
        body = []
        while self.current_token and self.current_token.type != 'RBRACE':
            body.append(self.parse_expression())
        
        if not self.match('RBRACE'):
            raise ParserError("Expected '}' after function body")
        
        if len(body) == 1:
            body = body[0]
        
        return ('DEFUN', func_name, params, body)

    def parse_function_call(self):
        func_name = self.current_token.value
        self.advance()  # Advance past the IDENTIFIER
        if self.current_token and self.current_token.type == 'LPAREN':
            self.advance()  # Advance past '('
            args = []
            while self.current_token and self.current_token.type != 'RPAREN':
                args.append(self.parse_expression())
                if self.current_token and self.current_token.type == 'COMMA':
                    self.advance()
            if not self.match('RPAREN'):
                raise ParserError("Incomplete function call, expected ')' after arguments")
            return ('CALL', func_name, args)
        else:
            return func_name

    def parse_comparison_expr(self):
        left = self.parse_term()
        while self.current_token and self.current_token.type in ('GREATER', 'LESS', 'EQUAL', 'NOT_EQUAL', 'GREATER_EQUAL', 'LESS_EQUAL'):
            operator = self.current_token.type
            self.advance()
            right = self.parse_term()
            left = (operator, left, right)
        return left

    def parse_boolean_value(self):
        value = self.current_token.value == 'TRUE'
        self.advance()
        return value

    def parse_boolean_or_comparison_expr(self):
        left = self.parse_comparison_expr()
        while self.current_token and self.current_token.type in ('AND', 'OR'):
            operator = self.current_token.type
            self.advance()
            right = self.parse_comparison_expr()
            left = (operator, left, right)
        return left

    def parse_string(self):
        left = self.current_token.value
        self.advance()

        while self.current_token and self.current_token.type == 'PLUS':
            operator = self.current_token.type
            self.advance()

            if self.current_token.type != 'STRING':
                raise ParserError("Expected string after '+' operator in string concatenation")

            right = self.current_token.value
            self.advance()
            left = (operator, left, right)

        return left

    def parse_paren_expr(self):
        self.advance()  # Advance past '('
        expr = self.parse_expression()
        if not self.match('RPAREN'):
            raise ParserError("Expected ')' after expression")
        return expr

    def parse_assignment(self):
        var_name = self.current_token.value
        self.advance()  # Advance past IDENTIFIER
        if not self.match('ASSIGN'):
            raise ParserError("Expected '=' after variable name")
        value = self.parse_expression()
        return ('ASSIGN', var_name, value)

    def peek(self):
        peek_pos = self.pos + 1
        if peek_pos < len(self.tokens):
            return self.tokens[peek_pos]
        return None

    def match(self, token_type):
        if self.current_token and self.current_token.type == token_type:
            self.advance()
            return True
        elif not self.current_token:
            raise ParserError(f"Unexpected end of input, expected '{token_type}'")
        return False

    def parse_lambda(self):
     self.advance()  # Advance past 'Lambda'
    
     if not self.match('LPAREN'):
        raise ParserError("Expected '(' after 'Lambda'")
    
     params = []
     while self.current_token and self.current_token.type != 'RPAREN':
        params.append(self.current_token.value)
        self.advance()
        if self.current_token.type == 'COMMA':
            self.advance()
    
     if not self.match('RPAREN'):
        raise ParserError("Expected ')' after parameters")
    
     body = self.parse_expression()
    
     # Handle possible nested lambdas
     if self.current_token and self.current_token.type == 'LAMBDA':
        nested_lambda = self.parse_lambda()  # Parse nested lambda
        return ('LAMBDA', params, nested_lambda)
    
     return ('LAMBDA', params, body)


