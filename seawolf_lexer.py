import ply
from ply import lex

tokens = ['LPAREN','RPAREN','PLUS','MINUS','MULT', 'DIVIDE', 'INT_CONST', 'EQUALS','VARNAME','MODULO']

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
t_INT_CONST = r'[0-9]+'   #0 -> 9 one or more times, if no have ‘r’ then “[0-9]+” will be 1 token and not several

t_EQUALS = r'='
t_VARNAME = r'[_a-zA-Z] [_a-zA-Z0-9]*'

lexer = lex.lex()
