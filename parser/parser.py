import ply.lex as lex


tokens = (
    'NAME', 'NUMBER', 'STRING',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MODULO', 'ASSIGNMENT',
    'L_PAREN', 'R_PAREN', 'PRINT',
    'SEPARATOR', 'L_ARRAY', 'R_ARRAY', 'L_ELEM_ARRAY', 'R_ELEM_ARRAY',
    'EQUALS', 'NOT_EQUALS', 'UPWARD', 'UPWARD_EQUALS', 'DOWNWARD', 'DOWNWARD_EQUALS',
    'IF', 'ELSE', 'BEGIN', 'END', 'REPEAT', 'INC', 'DEC', 'TO', 'NEWLINE'
)

# Tokens
t_STRING = r'\".*\"' # r'\"[a-zA-Z0-9_]*\"'

t_PRINT = r'show:'
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_MODULO = r'mod'
t_ASSIGNMENT = r':='

t_EQUALS = r'='
t_NOT_EQUALS = r'!='
t_UPWARD = r'>'
t_UPWARD_EQUALS = r'>='
t_DOWNWARD = r'<'
t_DOWNWARD_EQUALS = r'<='

t_SEPARATOR = r','
t_L_ARRAY = r'\['
t_R_ARRAY = r'\]'
t_L_ELEM_ARRAY = r'\{'
t_R_ELEM_ARRAY = r'\}'

t_L_PAREN = r'\('
t_R_PAREN = r'\)'

t_IF = r'if'
t_ELSE = r'else'
t_BEGIN = r'begin'
t_END = r'end'
t_REPEAT = r'repeat'
t_INC = r'inc'
t_DEC = r'dec'
t_TO = r'to'

t_NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'

def t_NUMBER(t):
    r'0x[0-9a-fA-f]+|\d+'
    try:
        if t.value[:2] == '0x':
            t.value = int(t.value, 16)
        else:
            t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t


def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    return t


# Ignored characters
t_ignore = " \t"


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    # t.lexer.skip(1)
    
# Build the lexer
import ply.lex as lex
lexer = lex.lex()

# -------------------------------------------------------------------------------------------
# Parsing rules

precedence = (
    ('left','PLUS','MINUS'),
    ('left','TIMES','DIVIDE','MODULO'),
    ('right','UMINUS'),
    )

# dictionary of variable names
names = { }

# statement
def p_stm_assign(t):
    '''stm : NAME ASSIGNMENT expr NEWLINE
           | NAME ASSIGNMENT arr NEWLINE'''
    names[t[1]] = t[3]

def p_stm_if(t):
    'stm : IF cond NEWLINE BEGIN NEWLINE stm END NEWLINE'
    pass
    # print(t[1])

def p_stm_if_else(t):
    'stm : IF cond NEWLINE BEGIN NEWLINE stm END NEWLINE ELSE NEWLINE BEGIN NEWLINE stm END NEWLINE'
    pass
    # print(t[1])

def p_stm_loop(t):
    '''stm : REPEAT expr TO expr INC expr NEWLINE BEGIN NEWLINE stm END NEWLINE
           | REPEAT expr TO expr DEC expr NEWLINE BEGIN NEWLINE stm END NEWLINE'''
    if t[5] == 'inc':
        pass
    if t[5] == 'dec':
        pass

def p_stm_print(t):
    'stm : PRINT str NEWLINE'
    pass


# exoression
def p_expr_op(t):
    '''expr : expr PLUS expr
            | expr MINUS expr
            | expr TIMES expr
            | expr DIVIDE expr
            | expr MODULO expr'''
    if t[2] == '+'  : 
        t[0] = t[1] + t[3]
    elif t[2] == '-': 
        t[0] = t[1] - t[3]
    elif t[2] == '*': 
        t[0] = t[1] * t[3]
    elif t[2] == '/': 
        t[0] = t[1] / t[3]
    elif t[2] == 'mod': 
        t[0] = t[1] % t[3]

def p_expr_uminus(t):
    'expr : MINUS expr %prec UMINUS'
    t[0] = -t[2]

def p_expr_group(t):
    'expr : L_PAREN expr R_PAREN'
    t[0] = t[2]

def p_expr_number(t):
    'expr : NUMBER'
    t[0] = t[1]

def p_expr_name(t):
    'expr : NAME'
    try:
        t[0] = names[t[1]]
    except LookupError:
        print("Undefined name '%s'" % t[1])
        t[0] = 0


# condition
def p_cond_op(t):
    '''cond : cond EQUALS cond
            | cond NOT_EQUALS cond
            | cond UPWARD cond
            | cond UPWARD_EQUALS cond
            | cond DOWNWARD cond
            | cond DOWNWARD_EQUALS cond'''
    if t[2] == '='  : 
        t[0] = (t[1] == t[3])
    elif t[2] == '!=': 
        t[0] = (t[1] != t[3])
    elif t[2] == '>': 
        t[0] = (t[1] > t[3])
    elif t[2] == '>=': 
        t[0] = (t[1] >= t[3])
    elif t[2] == '<': 
        t[0] = (t[1] < t[3])
    elif t[2] == '<=': 
        t[0] = (t[1] <= t[3])

def p_cond_expr(t):
    'cond : expr'
    t[0] = bool(t[1])

def p_cond_group(t):
    'cond : L_PAREN cond R_PAREN'
    t[0] = bool(t[2])


# array
def p_arr_size(t):
    'arr : L_ARRAY expr R_ARRAY'
    pass

def p_arr_elem(t):
    'arr : L_ELEM_ARRAY expr R_ELEM_ARRAY'
    pass


# element
def p_elem(t):
    'elem : expr'
    pass
    # t[0] = bool(t[1])

def p_elem_many(t):
    'elem : expr SEPARATOR elem'
    pass


# string
def p_str(t):
    '''str : expr
           | STRING'''
    t[0] = t[1]

def p_str_many(t):
    'str : str SEPARATOR str'
    pass


# error
def p_error(t):
    print("Syntax error at '%s'" % t.value)

import ply.yacc as yacc
parser = yacc.yacc()

# ---------------------------------------------------------------------------------------------

while True:
    try:
        s = input('calc > ')   # Use raw_input on Python 2
    except EOFError:
        break
    parser.parse(s)