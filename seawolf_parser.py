import ply
from ply import yacc
import seawolf_lexer
from seawolf_lexer import tokens

global_variables = dict()
# global_variables[‘ABC’] = 5

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULT', 'DIVIDE', 'MODULO'),
)

def p_assignment(p):
    """
        statement : VARNAME EQUALS expression
                | VARNAME EQUALS string
    """
    global_variables[p[1]] = p[3]

def p_string(p):
    """
        string : STRING
    """
    p[0] = p[1].strip("\"")

def p_statement(p):
    """
        statement : expression
            | string
    """
    print(p[1])


def p_expression(p):
    """
        expression : expression PLUS expression
            | expression MINUS expression
            | expression MULT expression
            | expression DIVIDE expression
            | expression MODULO expression
    """
    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]
    elif p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        p[0] = p[1] / p[3]
    elif p[2] == '%':
        p[0] = p[1] % p[3]


def p_expression_Paren(p):
    """
        expression : LPAREN expression RPAREN
    """
    p[0] = p[2]


def p_expression_number(p):
    """
        expression : NUMBER
    """
    p[0] = p[1]


def p_expression_var(p):
    """
        expression : VARNAME
    """
    try:
        p[0] = global_variables[p[1]]
    except LookupError:
        print("Undefined ID '%s'" % p[1])
        p[0] = 0



#def p_assignment(p):
 #   """
  #      assignment : VARNAME EQUALS expression
   # """
    #global_variables[p[1]] = p[3]
    #p[0] = p[3]
    #print (global_variables)

#def p_factor(p):
#    """
#    factor : INT_CONST
#        | LPAREN expression RPAREN
#        | variable
#    """
#    if len(p) == 4:
#        p[0] = p[2]
#    else:
#        p[0] = int(p[1])

def p_error(p):
    print("Syntax error\n")

parser = yacc.yacc()
