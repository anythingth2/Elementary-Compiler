import cc_lexer

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

while True:
    try:
        s = input('calc > ')   # Use raw_input on Python 2
    except EOFError:
        break
    # parser.parse(s)
    print(yacc.parse(s))