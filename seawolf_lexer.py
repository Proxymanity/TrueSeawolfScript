import ply
from ply import lex

reserved = {
    'and' : 'AND',
    'or' : 'OR',
    'not' : 'NOT'
}
tokens = ['LPAREN','RPAREN','PLUS','MINUS', 'MULT', 'DIVIDE', 'MODULO', 'EQUALS', 'VARNAME', 'NUMBER', 'STRING', 'LBRACK', 'RBRACK', 'COMMA','LESST','GREATERT',
            'LESSEQ','GREATEREQ','EQUALTO', 'NOTEQ','EXP','FLDIV'] + list(reserved.values())

def t_error(t):
    pass

t_ignore = r' \t'

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_PLUS = r'\+'
t_MINUS = r'-'
t_MULT = r'\*'
t_DIVIDE = r'/'
t_MODULO = r'%'
t_STRING = r'"[ !#-~_] [ !#-~_]*"'
t_EQUALS = r'='
def t_VARNAME(p):
    r'[_a-zA-Z] [_a-zA-Z0-9]*'
    p.type = reserved.get(p.value)  # Check for reserved words
    return p
t_LBRACK = r'\['
t_RBRACK = r'\]'
t_COMMA = r','

t_EXP = r'\*\*'
t_FLDIV = r'//'

t_LESST = r'<'
t_GREATERT = r'>'
t_LESSEQ = r'<='
t_GREATEREQ = r'>='
t_EQUALTO = r'=='
t_NOTEQ = r'<>'

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