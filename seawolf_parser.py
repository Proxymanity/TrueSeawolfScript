import ply
from ply import yacc
import seawolf_lexer
from seawolf_lexer import tokens

global_variables = dict()
# global_variables[‘ABC’] = 5

precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'NOT'),
    ('left', 'LESST', 'GREATERT','LESSEQ','GREATEREQ','EQUALTO','NOTEQ'),
    ('left', 'IN'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'FLDIV'),
    ('left', 'EXP'),
    ('left', 'MODULO'),
    ('left', 'MULT', 'DIVIDE'),
)


class Node:
    def __init__(self, type, children=None, leaf=None):
        self.type = type
        if children:
            self.children = children
        else:
            self.children = []
        self.leaf = leaf

    def evaluate(self):
        print("Evaluate")
        return 0

    def execute(self):
        print("Execute")

class ListNode(Node):
    def __init__(self,l):
        self.value = list(l)
        print("ListNode")
    def evaluate(self):
        print("Evaluate ListNode")
        return self.value

    def execute(self):
        return self.value

class StringNode(Node):
    def __init__(self, v):
        self.value = str(v)
        #self.value = self.value[1:-1]  # to eliminate the left and right double quotes uneeded
        print("StringNode")

    def evaluate(self):
        print("Evaluate StringNode")
        return self.value

    def execute(self):
        print("Execute StringNode")
        return self.value


class NumberNode(Node):
    def __init__(self, v):
        self.value = int(v)
        print("NumberNode")
    def evaluate(self):
        print("Evaluate NumberNode")
        return self.value
    def execute(self):
        print("Execute NumberNode")
        return(self.value)

class IfNode(Node):
    def __init__(self, c, t, e):
        self.condition = c
        self.thenBlock = t
        self.elseBlock= e
        print("IfNode")
    def evaluate(self):
        print("Evaluate IfNode")
        return 0
    def execute(self):
        print("Execute IfNode")
        if(self.condition.evaluate()):
            self.thenBlock.execute()
        else:
            self.elseBlock.execute()

class IfNode2(Node):
    def __init__(self, c, t):
        self.condition = c
        self.thenBlock = t
        print("IfNode2")
    def evaluate(self):
        print("Evaluate IfNode2")
        return 0
    def execute(self):
        print("Execute IfNode2")
        if(self.condition.evaluate()):
            self.thenBlock.execute()


class PrintNode(Node):
    def __init__(self, v):
        self.value = v
        ("PrintNode")

    def evaluate(self):
        print("Evaluate PrintNode")
        return 0

    def execute(self):
        print("Execute NumberNode")
        print(self.value.evaluate())


class BlockNode(Node):
    def __init__(self, sl):
        self.statementNodes = [sl]
        print("BlockNode")

    def evaluate(self):
        print("Evaluate BlockNode")
        return 0

    def execute(self):
        print("Execute BlockNode")
        for statement in self.statementNodes:
            statement.execute()


def p_statements(p):
    """
        statements : statement
                    | statement statements
    """
    p[0] = p[1]

def p_assignment(p):
    """
        statement : VARNAME EQUALS expression SEMI
    """
    global_variables[p[1]] = p[3]
def p_print(p):
    """
        statements : PRINT LPAREN statements RPAREN SEMI
    """
    p[0] = PrintNode(p[3])
def p_statement(p):
    """
        statement : expression
                    | LCURL statements RCURL
    """
    if(p[1] == '{'):
        p[0] = BlockNode(p[2])
    elif(isinstance(p[1],int)):
        print("Number")
        p[0] = NumberNode(p[1])
    elif(isinstance(p[1],str)):
        print("string")
        p[0] = StringNode(p[1])
    else:
        p[0] = ListNode(p[1])

def p_if(p):
    """
        statement : IF LPAREN statements RPAREN LCURL statements RCURL else
    """
    if(not(p[8] is None)):
        print("noner")
        p[0] = IfNode(p[3],p[6],p[8])
    else:
        p[0] = p[0] = IfNode2(p[3],p[6])
def p_else(p):
    """
       else : ELSE LCURL statements RCURL
                    | empty
    """
    if(len(p) > 2):
        p[0] = p[3]
    else:
        pass

def p_expression_string(p):
    """
        expression : string_expression
    """
    p[0] = p[1]

def p_expression_list(p):
    """
        expression : list
    """
    p[0] = p[1]

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
    if((type(p[1]) == type(p[3])) or (type(p[1]) == int and type(p[3]) == float) or (type(p[1])== float and type(p[3])==int)):
        if p[2] == '+':
            p[0] = p[1] + p[3]
        if p[2] == '-':
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
    else:
        p[0] = "SEMANTIC ERROR"
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
        #print("Undefined ID '%s'" % p[1])
        p[0] = "SEMANTIC ERROR"

def p_index(p):
    """
        expression : list LBRACK expression RBRACK
                | string_expression LBRACK expression RBRACK
    """
    if(isinstance(p[3],int) and(isinstance(p[1], list) or isinstance(p[1],str))):
            p[0] = (p[1])[p[3]]
    else:
        p[0] = "SEMANTIC ERROR"

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
    elif (type(p[1]) == type(p[3])):
        p[0] = p[1] + p[3]
    else:
        p[0] = "SEMANTIC ERROR"

def p_string_expression(p):
    """
        string_expression : string_expression PLUS string_expression
            | STRING
    """
    if len(p) > 2:
        if p[2] == "+":
            if (type(p[1]) == type(p[3])):
                p[0] = p[1] + p[3]
            else:
                p[0] = "SEMANTIC ERROR"
    elif p[1] == "":
        p[0] = p[0]
    else:
        p[0] = p[1].strip("\"")

def p_in(p):
    """
        expression : expression IN list
                | string_expression IN string_expression
    """
    if(isinstance(p[1],float)):
        p[0] = "SEMANTIC ERROR"
    else:
        if p[1] in p[3]:
            p[0] = 1
        else:
            p[0] = 0


def p_empty(p):
    """
        empty :
    """
    pass

def p_error(p):
    print("SYNTAX ERROR")

parser = yacc.yacc()
