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
                | VARNAME EQUALS string_expression
                | VARNAME EQUALS list
    """
    global_variables[p[1]] = p[3]

def p_string_expression(p):
    """
        string_expression : string_expression PLUS string_expression
            | STRING
    """
    if len(p) > 2:
        if p[2] == "+":
            p[0] = p[1] + p[2]
    else:
        p[0] = p[1].strip("\"")

def p_statement(p):
    """
        statement : expression
            | string_expression
            | list
    """
    print(p[1])


def p_expression(p):
    """
        expression : expression PLUS expression
            | expression MINUS expression
            | expression MULT expression
            | expression DIVIDE expression
            | expression MODULO expression
            | expression EXP expression
            | expression FLDIV expression
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
    elif p[2] == '**':
        p[0] = p[1] ** p[3]
    elif p[2] == '//':
        p[0] = p[1] // p[3]

def p_expression_and(p):
    """
        expression : expression AND expression
    """
    if isinstance(p[1],int) and isinstance(p[3],int):
        if p[1] == 0 or p[3] == 0:
            p[0] = 0
        else:
            p[0] = 1

def p_expression_or(p):
    """
        expression : expression OR expression
    """
    if isinstance(p[1], int) and isinstance(p[3], int):
        if p[1] == 0 and p[3] == 0:
            p[0] = 0
        else:
            p[0] = 1
    else:
        p[0] = "SEMANTIC ERROR"

def p_expression_not(p):
    """
        expression : NOT expression
    """
    if isinstance(p[1], int):
        if p[1] == 0:
            p[0] = 1
        else:
            p[0] = 0

def p_expression_compare(p):
    """
        expression : expression LESST expression
                | expression GREATERT expression
                | expression LESSEQ expression
                | expression GREATEREQ expression
                | expression EQUALTO expression
                | expression NOTEQ expression
    """
    if isinstance(p[1], int) and isinstance(p[3], int):
        if p[2] == '<':
            if p[1] < p[3]:
                p[0] = 1
            else:
                p[0] = 0
        elif p[2] == '>':
            if p[1] > p[3]:
                p[0] = 1
            else:
                p[0] = 0
        elif p[2] == '<=':
            if p[1] <= p[3]:
                p[0] = 1
            else:
                p[0] = 0
        elif p[2] == '>=':
            if p[1] >= p[3]:
                p[0] = 1
            else:
                p[0] = 0
        elif p[2] == '==':
            if p[1] == p[3]:
                p[0] = 1
            else:
                p[0] = 0
        elif p[2] == '<>':
            if p[1] != p[3]:
                p[0] = 1
            else:
                p[0] = 0
    else:
        p[0] = "SEMANTIC ERROR"



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



def p_list(p):
    """
        list : LBRACK list_item RBRACK
            | LBRACK RBRACK
    """
    if(len(p) > 3):
        p[0] = p[2]
    else:
        p[0] = []

def p_list_item(p):
    """
        list_item : list_item COMMA list_item
            | expression
    """
    if (len(p) < 3):
        p[0] = [p[1]]
    else:
        p[0] = p[1] + p[3]

def p_error(p):
    print("Syntax error\n")

parser = yacc.yacc()
