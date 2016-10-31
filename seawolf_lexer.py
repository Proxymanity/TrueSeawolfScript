import ply
from ply import lex

tokens = ('LPAREN','RPAREN','PLUS','MINUS', 'MULT', 'DIVIDE', 'MODULO', 'EQUALS', 'VARNAME', 'NUMBER', 'QUOTE', 'STRING',)

def t_error(t):
    pass

t_ignore = r'[ \t]'

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_PLUS = r'\+'
t_MINUS = r'-'
t_MULT = r'\*'
t_DIVIDE = r'/'
t_MODULO = r'%'
t_QUOTE = r'"'
t_STRING = r'"[ !#-~_] [ !#-~_]*"'
t_EQUALS = r'='
t_VARNAME = r'[_a-zA-Z] [_a-zA-Z0-9]*'


def t_NUMBER(p):
    r'([0-9]+[\.][0-9]+) | ([0-9]+)'
    try:
        p.value = int(p.value)
        return p
    except ValueError:
        pass

    try:
        p.value = float(p.value)
        return p
    except ValueError:
        print("Number Error")
        p.value = 0
    return p

lexer = lex.lex()
if __name__ == '__main__':
     lex.runmain()