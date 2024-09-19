<program> ::= <statement> | <statement> <program>

<statement> ::= <expression> | <function_def> | <lambda_expr> | <boolean_expr> | <arith_expr> | <compare_expr> | <if_statement>

<expression> ::= <arith_expr> | <boolean_expr> | <compare_expr> | <function_call> | <boolean_value> | <integer>

<function_def> ::= "Defun" <identifier> "(" <identifier> ("," <identifier>)* ")" "{" <expression> "}"

<lambda_expr> ::= "Lambda" "(" <identifier> ("," <identifier>)* ")" <expression>

<boolean_expr> ::= <expression> "&&" <expression> 
                | <expression> "||" <expression>
                | "!" <expression>

<arith_expr> ::= <expression> "+" <expression>
               | <expression> "-" <expression>
               | <expression> "*" <expression>
               | <expression> "/" <expression>
               | <expression> "%" <expression>

<compare_expr> ::= <expression> "==" <expression>
                | <expression> "!=" <expression>
                | <expression> ">" <expression>
                | <expression> "<" <expression>
                | <expression> ">=" <expression>
                | <expression> "<=" <expression>

<function_call> ::= <identifier> "(" <expression> ("," <expression>)* ")"

<if_statement> ::= "if" "(" <compare_expr> ")" "then" <statement> "else" <statement>

<boolean_value> ::= "TRUE" | "FALSE"

<integer> ::= [0-9]+

<identifier> ::= [a-zA-Z_][a-zA-Z0-9_]* 
