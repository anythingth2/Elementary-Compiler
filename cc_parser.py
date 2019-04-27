import ply.yacc as yacc
from cc_lexer import tokens
from cc_codegen import *

# for debug
import inspect

# Parsing rules
precedence = (
    ('left', 'EQUALS', 'NOT_EQUALS'),
    ('left', 'UPWARD', 'UPWARD_EQUALS', 'DOWNWARD', 'DOWNWARD_EQUALS'),

    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'MODULO'),
    ('right', 'UMINUS'),

    ('left', 'L_PAREN', 'R_PAREN', 'L_ARRAY', 'R_ARRAY'),
)

# dictionary of variable names
names = {}          # { 'n':3, 'ar':[1,2,3], ... }


### Tag type ###
# Integer     -> ('INT', expr)
# Variable    -> ('VAR', ID)
# Array       -> ('ARR', ID, INDEX) *default INDEX = 0

# for generate nasm code
source_code = ''

# statement


def p_stm_assign(t):
    '''stm : ID ASSIGNMENT expr NEWLINE'''
    if checkTokenType(t[3]) == TokenType.expression:
        expr_generator(t[3])
    names[t[1]] = t[3]
    t[0] = (t[2], ('VAR', t[1]), t[3])
    # print(inspect.getframeinfo(inspect.currentframe()).function, t, '\n')

def p_stm_assign_arr(t):
    '''stm : ID ASSIGNMENT L_ARRAY expr R_ARRAY NEWLINE
           | ID ASSIGNMENT L_ELEM_ARRAY elem R_ELEM_ARRAY NEWLINE'''
    if t[3] == '[':
        names[t[1]] = [0]*t[4][1]
    elif t[3] == '{':
        names[t[1]] = t[4]
    t[0] = (t[2], ('ARR', t[1], 0), names[t[1]])

def p_stm_assign_arr_index(t):
    '''stm : ID L_ARRAY expr R_ARRAY ASSIGNMENT expr NEWLINE'''
    if t[3] > 0:
        try:
            names[t[1]][t[3]] = t[6]
            t[0] = (t[5], ('ARR', t[1], t[3]), t[6])
        except LookupError:
            print("Line ({}) : Undefined name '{}'".format(t.lineno, t[1]))
            t[0] = None
        except ValueError:
            print("Line ({}) : Index '{}[{}]' out of range".format(
                t.lineno, t[1], t[3]))
            t[0] = None
    else:
        print("Line ({}) : Index '{}[{}]' out of range".format(
            t.lineno, t[1], t[3]))
        t[0] = None


def p_stm_if(t):
    '''stm : IF cond NEWLINE
           | ELSE IF cond NEWLINE'''
    pass

def p_stm_else(t):
    '''stm : ELSE NEWLINE'''
    pass


def p_stm_loop(t):
    '''stm : REPEAT expr TO expr INC expr NEWLINE
           | REPEAT expr TO expr DEC expr NEWLINE'''
    if t[5] == 'inc':
        pass
    if t[5] == 'dec':
        pass

def p_stm_end(t):
    '''stm : END NEWLINE'''
    pass

def p_stm_print(t):
    '''stm : PRINT str NEWLINE'''
    pass


# expression
def p_expr_op(t):
    '''expr : expr PLUS expr
            | expr MINUS expr
            | expr TIMES expr
            | expr DIVIDE expr
            | expr MODULO expr'''
    t[0] = (t[2], t[1], t[3])


def p_expr_uminus(t):
    '''expr : MINUS expr %prec UMINUS'''
    t[0] = (t[1], 0, t[2])


def p_expr_group(t):
    '''expr : L_PAREN expr R_PAREN'''
    t[0] = t[2]


def p_expr_number(t):
    '''expr : NUMBER'''
    t[0] = ('INT', t[1])


def p_expr_name(t):
    '''expr : ID'''
    try:
        if type(names[t[1]]) is list:
            t[0] = ('ARR', t[1], 0)
        else:
            t[0] = ('VAR', t[1])
    except LookupError:
        print("Line ({}) : Undefined name '{}'".format(t.lineno, t[1]))
        t[0] = None


def p_expr_name_arr(t):
    '''expr : ID L_ARRAY expr R_ARRAY'''
    try:
        t[0] = ('ARR', t[1], t[3])
    except LookupError:
        print("Line ({}) : Undefined name '{}'".format(t.lineno, t[1]))
        t[0] = None
    except ValueError:
        print("Line ({}) : Index '{}[{}]' out of range".format(
            t.lineno, t[1], t[3]))
        t[0] = None


# condition
def p_cond_op(t):
    '''cond : cond EQUALS cond
            | cond NOT_EQUALS cond
            | cond UPWARD cond
            | cond UPWARD_EQUALS cond
            | cond DOWNWARD cond
            | cond DOWNWARD_EQUALS cond'''
    t[0] = (t[2], t[1], t[3])


def p_cond_expr(t):
    '''cond : expr'''
    t[0] = t[1]


def p_cond_group(t):
    '''cond : L_PAREN cond R_PAREN'''
    t[0] = t[2]


# element
def p_elem(t):
    '''elem : expr'''
    t[0] = [t[1][1]]


def p_elem_many(t):
    '''elem : expr SEPARATOR elem'''
    t[3].insert(0, t[1][1])
    t[0] = t[3]


# string
def p_str(t):
    '''str : expr
           | STRING'''
    t[0] = t[1]


def p_str_many(t):
    '''str : str SEPARATOR str'''
    t[0] = (t[2], t[1], t[3])


# error
def p_error(t):
    print("Line ({}) : Syntax error at '{}'".format(t.lineno, t.value))


import ply.yacc as yacc
parser = yacc.yacc()


# if __name__ == '__main__':
#     while True:
#         try:
#             s = input('cc > ')   # Use raw_input on Python 2
#             s += '\n'
#         except EOFError:
#             break
#     # parser.parse(s)
#         print(yacc.parse(s))
