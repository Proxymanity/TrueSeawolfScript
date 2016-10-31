import ply
from ply import yacc
import seawolf_lexer
from seawolf_lexer import tokens

global_variables = dict()
# global_variables[‘ABC’] = 5

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'MODULO')
)

def p_variables(p):
    """
    variable : VARNAME
    """
    if(global_variables.has_key(p[1])):
        p[0] = global_variables[p[1]]


def p_expression(p):
    '''expression : expression PLUS expression
            | expression MINUS expression
            | expression TIMES expression
            | expression DIVIDE expression
            | expression MODULO expression
            | LPAREN expression RPAREN
            | NUMBER '''
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


def p_program(p):
    """
        program : expression
    """
    p[0] = p[1]


#def p_assignment(p):
 #   """
  #      assignment : VARNAME EQUALS expression
   # """
    #global_variables[p[1]] = p[3]
    #p[0] = p[3]
    #print (global_variables)

def p_factor(p):
    """
    factor : INT_CONST
        | LPAREN expression RPAREN
        | variable
    """
    if len(p) == 4:
        p[0] = p[2]
    else:
        p[0] = int(p[1])

def p_error(p):
    print("Syntax error")
parser = yacc.yacc()
