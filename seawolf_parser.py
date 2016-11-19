import ply
from ply import yacc
import seawolf_lexer
from seawolf_lexer import tokens

error = False;

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

class AssignNode(Node):
    def __init__(self,Name,Value):
        self.name = Name
        self.value = Value
        print("AssignNode")
    def evaluate(self):
        print("AssignNode Evaluate")
        if(isinstance(self.value,binOPNode)):
            print(self.value.evaluate())
            global_variables[self.name] = self.value.evaluate()
        else:
            global_variables[self.name] = self.value
        pass

    def execute(self):
        print("AssignNode Execute")
        if(isinstance(self.value,binOPNode)):
            print(self.value.evaluate())
            global_variables[self.name] = self.value.evaluate()
        else:
            global_variables[self.name] = self.value
        pass

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
        print("v is " + str(v))
    def evaluate(self):
        print("Evaluate StringNode")
        return self.value

    def execute(self):
        print("Execute StringNode")
        return self.value
class FloatNode(Node):
    def __init__(self, v):
        self.value = v
        print("FloatNode")

    def evaluate(self):
        print("Evaluate FloatNode")
        return self.value

    def execute(self):
        print("Execute FloatNode")
        return (self.value)

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
        self.thenBlock = BlockNode(t)
        self.elseBlock= BlockNode(e)
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
        self.thenBlock = BlockNode(t)
        print("ifNode2")
    def evaluate(self):
        print("Evaluate ifNode2")
        return 0
    def execute(self):
        print("Execute ifNode2")
        if(self.condition.evaluate()):
            self.thenBlock.execute()

class WhileNode(Node):
    def __init__(self, c, t):
        self.condition = c
        self.thenBlock = BlockNode(t)
        print("WhileNode")
    def evaluate(self):
        print("Evaluate while")
        return 0
    def execute(self):
        print("Execute while")
        while(self.condition.evaluate()):
            print("WhileLooping")
            self.thenBlock.execute()


class PrintNode(Node):
    def __init__(self, v):
        self.value = v
        ("PrintNode")

    def evaluate(self):
        print("Evaluate PrintNode")
        print(self.value.evaluate())

    def execute(self):
        print("Execute PrintNode")
        print(self.value.evaluate())


class BlockNode(Node):
    def __init__(self, sl):
        if(isinstance(sl,list)):
            self.statementNodes = sl
        else:
            self.statementNodes = [sl]
        print("BlockNode")

    def evaluate(self):
        print("Evaluate BlockNode")
        return 0

    def execute(self):
        print("Execute BlockNode")
        for statement in self.statementNodes:
            statement.execute()

class VarNode(Node):
    def __init__(self,Name):
        print("VarNode")
        self.name = Name
    def evaluate(self):
        try:
            if(isinstance(global_variables[self.name],int) or isinstance(global_variables[self.name],str) or isinstance(global_variables[self.name],float) or isinstance(global_variables[self.name],list)):
                return global_variables[self.name]
            else:
                r1 = global_variables[self.name]
                result = global_variables[self.name].evaluate()
                return result
        except LookupError:
            semanticError()
    def execute(self):
        try:
            if(isinstance(global_variables[self.name],int) or isinstance(global_variables[self.name],str) or isinstance(global_variables[self.name],float) or isinstance(global_variables[self.name],list)):
                return global_variables[self.name]
            else:
                return global_variables[self.name].evaluate()
        except LookupError:
            semanticError()

class binOPNode(Node):
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c
    def evaluate(self):
        if(isinstance(self.a,int)):
            self.a= NumberNode(self.a)
        if(isinstance(self.c,int)):
            self.c= NumberNode(self.c)
        result = 0
        if self.b == '+':
            result = self.a.evaluate() + self.c.evaluate()
        if self.b == '-':
            result = self.a.evaluate() - self.c.evaluate()
        elif self.b == '*':
            result = self.a.evaluate() * self.c.evaluate()
        elif self.b == '/':
            result = self.a.evaluate() / self.c.evaluate()
        elif self.b == '%':
            result = self.a.evaluate() % self.c.evaluate()
        elif self.b == '**':
            result = self.a.evaluate() ** self.c.evaluate()
        elif self.b == '//':
            result = self.a.evaluate() // self.c.evaluate()
        if (isinstance(result, int)):
            print("Number")
            return NumberNode(result)
        elif (isinstance(result, float)):
            print("float")
            return FloatNode(result)
        elif (isinstance(result, str)):
            print("string")
            return StringNode(result)
        elif (isinstance(result, list)):
            return ListNode(result)

    def execute(self):
        if(isinstance(self.a,int)):
            self.a= NumberNode(self.a)
        if(isinstance(self.c,int)):
            self.c= NumberNode(self.c)
        result = 0
        if self.b == '+':
            result = self.a.evaluate() + self.c.evaluate()
        if self.b == '-':
            result = self.a.evaluate() - self.c.evaluate()
        elif self.b == '*':
            result = self.a.evaluate() * self.c.evaluate()
        elif self.b == '/':
            result = self.a.evaluate() / self.c.evaluate()
        elif self.b == '%':
            result = self.a.evaluate() % self.c.evaluate()
        elif self.b == '**':
            result = self.a.evaluate() ** self.c.evaluate()
        elif self.b == '//':
            result = self.a.evaluate() // self.c.evaluate()
        if (isinstance(result, int)):
            print("Number")
            return NumberNode(result)
        elif (isinstance(result, float)):
            print("float")
            return FloatNode(result)
        elif (isinstance(result, str)):
            print("string")
            return StringNode(result)
        elif (isinstance(result, list)):
            return ListNode(result)


class CompareNode(Node):
    def __init__(self,a,b,c):
        self.arg1 = a
        self.op =b
        self.arg2 = c
    def evaluate(self):
        #self.arg1.evaluate()
        #self.arg2.evaluate()
        if(isinstance(self.arg1,int)):
            self.arg1= NumberNode(self.arg1)
        if(isinstance(self.arg1,int)):
            self.arg2= NumberNode(self.arg2)

        if self.op == '<':
            if  self.arg1.evaluate() < self.arg2.evaluate():
                result = 1
            else:
                result = 0
        elif self.op == '>':
            if  self.arg1.evaluate() > self.arg2.evaluate():
                result = 1
            else:
                result = 0
        elif self.op == '<=':
            if  self.arg1.evaluate() <= self.arg2.evaluate():
                result = 1
            else:
                result = 0
        elif self.op == '>=':
            if  self.arg1.evaluate() >= self.arg2.evaluate():
                result = 1
            else:
                result = 0
        elif self.op == '==':
            if  self.arg1.evaluate() == self.arg2.evaluate():
                result = 1
            else:
                result = 0
        elif self.op == '<>':
            if  self.arg1.evaluate() != self.arg2.evaluate():
                result = 1
            else:
                result = 0
        return result

    def execute(self):
        result = 0
        if(isinstance(self.arg1,int)):
            self.arg1= NumberNode(self.arg1)
        if(isinstance(self.arg1,int)):
            self.arg2= NumberNode(self.arg2)
        if self.op == '<':
            if self.arg1.evaluate() < self.arg2.evaluate():
                result = 1
            else:
                result = 0
        elif self.op == '>':
            if self.arg1.evaluate() > self.arg2.evaluate():
                result = 1
            else:
                result = 0
        elif self.op == '<=':
            if self.arg1.evaluate() <= self.arg2.evaluate():
                result = 1
            else:
                result = 0
        elif self.op == '>=':
            if self.arg1.evaluate() >= self.arg2.evaluate():
                result = 1
            else:
                result = 0
        elif self.op == '==':
            if self.arg1.evaluate() == self.arg2.evaluate():
                result = 1
            else:
                result = 0
        elif self.op == '<>':
            if self.arg1.evaluate() != self.arg2.evaluate():
                result = 1
            else:
                result = 0
        return result

class LogicNode(Node):
    def __init__(self,a,b,c):
        print("Logic")
        self.arg1 = a
        self.op = b
        self.arg2 = c
    def evaluate(self):
        print("evaluate Logic")
        if(isinstance(self.arg1,int)):
            self.arg1= NumberNode(self.arg1)
        if(isinstance(self.arg1,int)):
            self.arg2= NumberNode(self.arg2)
        a = self.arg1.evaluate()
        b = self.arg2.evaluate()
        result = 0
        if((isinstance(a,int) and isinstance(b,int))):
            if(self.op == 'AND'):
                if a == 0 or b == 0:
                    result = 0
                else:
                    result = 1
            elif(self.op == 'OR'):
                if a == 0 and b == 0:
                    result = 0
                else:
                    result = 1
            else:
                semanticError()
        else:
            semanticError()
        return result

    def execute(self):
        print("Execute Logic")
        if(isinstance(self.arg1,int)):
            self.arg1= NumberNode(self.arg1)
        if(isinstance(self.arg1,int)):
            self.arg2= NumberNode(self.arg2)
        a = self.arg1.evaluate()
        b = self.arg2.evaluate()
        result = 0
        if ((isinstance(a, int) and isinstance(b, int))):
            if (self.op == 'AND'):
                if a == 0 or b == 0:
                    result = 0
                else:
                    result = 1
            elif (self.op == 'OR'):
                if a == 0 and b == 0:
                    result = 0
                else:
                    result = 1
            else:
                semanticError()
        else:
            semanticError()
        return result

class NotNode(Node):
    def __init__(self,a):
        print("NotNode")
        self.arg = a
    def evaluate(self):
        print("Evaluate Not")
        if(isinstance(self.arg,int)):
            self.arg= NumberNode(self.arg)

        a = self.arg.evaluate
        if(isinstance(a,int)):
            if a == 0:
                return 1
            else:
                return 0
        else:
            semanticError()
    def execute(self):
        print("Execute Not")
        if(isinstance(self.arg,int)):
            self.arg= NumberNode(self.arg)
        a = self.arg.evaluate
        if(isinstance(a,int)):
            if a == 0:
                return 1
            else:
                return 0
        else:
            semanticError()
def p_statements(p):
    """
        statements : statement
                    | statements statement

    """
    #return all the nodes here
    if len(p) == 2 and p[1]:
        p[0] = p[1]
    elif len(p) == 3:
        if(not(isinstance(p[2],list))):
            p[2] = [p[2]]
        if(not(isinstance(p[1],list))):
            p[1] = [p[1]]
        p[0] = p[1] + p[2]


def p_assign(p):
    """
        statement : VARNAME EQUALS expression SEMI
    """
    print("assignment")
    global_variables[p[1]] = 0
    p[0] = AssignNode(p[1],p[3])


def p_print(p):
    """
        statement : PRINT LPAREN statement RPAREN SEMI
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
    elif(isinstance(p[1],float)):
        print("float")
        p[0] = FloatNode(p[1])
    elif(isinstance(p[1],str)):
        print("string")
        p[0] = StringNode(p[1])
    elif(isinstance(p[1],list)):
        p[0] = ListNode(p[1])
    else:
        p[0] = p[1]

def p_if(p):
    """
        statement : IF LPAREN statements RPAREN LCURL statements RCURL else
    """
    if(not(p[8] is None)):
        p[0] = IfNode(p[3],p[6],p[8])
    else:
        p[0] = IfNode2(p[3],p[6])
def p_else(p):
    """
       else : ELSE LCURL statements RCURL
                    | empty
    """
    if(len(p) > 2):
        p[0] = p[3]
    else:
        pass

def p_while(p):
    """
        statement : WHILE LPAREN statements RPAREN LCURL statements RCURL
    """
    p[0] = WhileNode(p[3], p[6])

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
    p[0] = binOPNode(p[1],p[2],p[3])

def p_expression_and(p):
    """
        expression : expression AND expression
    """
    p[0] = LogicNode(p[1],'AND',p[3])

def p_expression_or(p):
    """
        expression : expression OR expression
    """
    p[0] =  LogicNode(p[1], 'AND', p[3])
def p_expression_not(p):
    """
        expression : NOT expression
    """
    p[0] = NotNode(p[2])

def p_expression_compare(p):
    """
        expression : expression LESST expression
                | expression GREATERT expression
                | expression LESSEQ expression
                | expression GREATEREQ expression
                | expression EQUALTO expression
                | expression NOTEQ expression
    """
    print("compare")
    p[0] = CompareNode(p[1],p[2],p[3])



def p_expression_Paren(p):
    """
        expression : LPAREN expression RPAREN
    """
    p[0] = p[2]



def p_expression_number(p):
    """
        expression : NUMBER
    """
    p[0] = NumberNode(p[1])

def p_expression_var(p):
    """
        expression : VARNAME
    """
    p[0] = VarNode(p[1])

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

def semanticError():
    error = True
    print("SEMANTIC ERROR")

def resetError():
    error = False

def p_error(p):
    error = True
    print("SYNTAX ERROR")

parser = yacc.yacc()
