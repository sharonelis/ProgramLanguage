class LexerError(Exception):
    def __init__(self, message, pos):
        super().__init__(message)
        self.pos = pos

class Token:
    def __init__(self, type_, value, pos):
        self.type = type_
        self.value = value
        self.pos = pos

    def __repr__(self):
        return f"<Token type='{self.type}', value={self.value}>"

class Lexer:
    def __init__(self, code):
        self.code = code
        self.pos = 0
        self.current_char = code[self.pos] if self.code else None
        self.keywords = {
            'Defun': 'DEFUN',
            'Lambda': 'LAMBDA',
            'TRUE': 'BOOLEAN',
            'FALSE': 'BOOLEAN',
            'if': 'IF',
            'then': 'THEN',
            'else': 'ELSE'
        }

    def advance(self):
        self.pos += 1
        if self.pos < len(self.code):
            self.current_char = self.code[self.pos]
        else:
            self.current_char = None

    def tokenize(self):
        tokens = []
        while self.current_char is not None:
            if self.current_char.isspace():
                self.advance()
            elif self.current_char == '#':
                self.skip_comment()  # התעלמות משורה של הערה
            elif self.current_char.isdigit():
                tokens.append(self.make_integer())
            elif self.current_char.isalpha():
                tokens.append(self.make_identifier_or_keyword())
            elif self.current_char == '+':
                tokens.append(Token('PLUS', '+', self.pos))
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token('MINUS', '-', self.pos))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token('MULTIPLY', '*', self.pos))
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token('DIVIDE', '/', self.pos))
                self.advance()
            elif self.current_char == '%':
                tokens.append(Token('MODULO', '%', self.pos))
                self.advance()
            elif self.current_char == '&':
                if self.peek() == '&':
                    tokens.append(Token('AND', '&&', self.pos))
                    self.advance()
                    self.advance()
                else:
                    raise LexerError(f"Unexpected character: {self.current_char}", self.pos)
            elif self.current_char == '|':
                if self.peek() == '|':
                    tokens.append(Token('OR', '||', self.pos))
                    self.advance()
                    self.advance()
                else:
                    raise LexerError(f"Unexpected character: {self.current_char}", self.pos)
            elif self.current_char == '=' and self.peek() == '=':
                tokens.append(Token('EQUAL', '==', self.pos))
                self.advance()
                self.advance()
            elif self.current_char == '!' and self.peek() == '=':
                tokens.append(Token('NOT_EQUAL', '!=', self.pos))
                self.advance()
                self.advance()
            elif self.current_char == '!':
                tokens.append(Token('NOT', '!', self.pos))
                self.advance()
            elif self.current_char == '>':
                if self.peek() == '=':
                    tokens.append(Token('GREATER_EQUAL', '>=', self.pos))
                    self.advance()
                else:
                    tokens.append(Token('GREATER', '>', self.pos))
                self.advance()
            elif self.current_char == '<':
                if self.peek() == '=':
                    tokens.append(Token('LESS_EQUAL', '<=', self.pos))
                    self.advance()
                else:
                    tokens.append(Token('LESS', '<', self.pos))
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token('LPAREN', '(', self.pos))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token('RPAREN', ')', self.pos))
                self.advance()
            elif self.current_char == '{':
                tokens.append(Token('LBRACE', '{', self.pos))
                self.advance()
            elif self.current_char == '}':
                tokens.append(Token('RBRACE', '}', self.pos))
                self.advance()
            elif self.current_char == ',':
                tokens.append(Token('COMMA', ',', self.pos))
                self.advance()
            elif self.current_char == ';':
                tokens.append(Token('SEMICOLON', ';', self.pos))
                self.advance()
            elif self.current_char == '=':
                tokens.append(Token('ASSIGN', '=', self.pos))
                self.advance()
            elif self.current_char == ':':  # הוספת טיפול בתו ':'
                tokens.append(Token('COLON', ':', self.pos))
                self.advance()
            elif self.current_char == '"':
                tokens.append(self.make_string())
            else:
                raise LexerError(f"Unknown character: {self.current_char}", self.pos)
        
        return tokens
    
    def skip_comment(self):
        """ מתעלם מהערות שמתחילות ב-# """
        while self.current_char is not None and self.current_char != '\n':
            self.advance()
        self.advance()  # קידום מעבר לסוף השורה

    def peek(self):
        peek_pos = self.pos + 1
        if peek_pos < len(self.code):
            return self.code[peek_pos]
        else:
            return None

    def make_integer(self):
        start_pos = self.pos
        while self.current_char is not None and self.current_char.isdigit():
            self.advance()
        value = self.code[start_pos:self.pos]
        return Token('INTEGER', int(value), start_pos)

    def make_identifier_or_keyword(self):
        start_pos = self.pos
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            self.advance()
        value = self.code[start_pos:self.pos]
        token_type = self.keywords.get(value, 'IDENTIFIER')
        return Token(token_type, value, start_pos)

    def make_string(self):
        start_pos = self.pos
        self.advance()  # Skip the opening quote
        string_value = ''
        while self.current_char is not None and self.current_char != '"':
            string_value += self.current_char
            self.advance()
        if self.current_char == '"':
            self.advance()  # Skip the closing quote
            return Token('STRING', string_value, start_pos)
        else:
            raise LexerError(f"Unterminated string at position {start_pos}", start_pos)
