import ply.yacc as yacc
from cc_lexer import tokens
import cc_codegen
from cc_compiler import trav


# Parsing rules
precedence = (
    ('left', 'ASSIGNMENT'),
    ('left', 'EQUALS', 'NOT_EQUALS'),
    ('left', 'UPWARD', 'UPWARD_EQUALS', 'DOWNWARD', 'DOWNWARD_EQUALS'),

    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'MODULO'),
    ('right', 'UMINUS'),

    ('left', 'L_PAREN', 'R_PAREN', 'L_ARRAY', 'R_ARRAY'),
)

# dictionary of variable names
names = {}          # { 'n':3, 'ar':[1,2,3], ... }
indexs = {}          

# counter and stack for asm label and loop index
lp_ct = 0
idx_ct = 0
end_ct = 0
lp_stack = []
end_stack = []

# else checker
else_checker = False 

# if/else/loop match checker
end_checker = []
def mark_end(lineno):
    end_checker.append(lineno)

def unmark_end():
    try:
        end_checker.pop()

# jump condition map sign (invert for short if)
j_cond = {
    '='  : 'JNE   ',
    '!=' : 'JE    ',
    '>'  : 'JLE   ',
    '>=' : 'JL    ',
    '<'  : 'JGE   ',
    '<=' : 'JG    '
}

def jmp_end():
    end_stack.append('end'+str(end_ct)+':')
    end_ct += 1
    return end_stack[-1][:-1]

def label_end():
    try:
        return end_stack.pop()
    except IndexError:

# for generate nasm code
source_code = ''

### Tag type ###
# Integer     -> ('INT', expr)
# Variable    -> ('VAR', ID)
# Array       -> ('ARR', ID, INDEX) *default INDEX = 0

# for generate nasm code
source_code = ''
def emit_sourcecode(code):
    global source_code
    source_code += code

# statement
def p_stm_assign(t):
    '''stm : ID ASSIGNMENT expr NEWLINE'''
    t[1] = f'var_{t[1]}'
    # names[t[1]] = t[3]
    if t[1] not in names:
        names[t[1]] = 'INT'
    t[0] = (t[2], ('VAR', t[1]), t[3])


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
    print('expr_op')
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
    '''cond : expr EQUALS expr
            | expr NOT_EQUALS expr
            | expr UPWARD expr
            | expr UPWARD_EQUALS expr
            | expr DOWNWARD expr
            | expr DOWNWARD_EQUALS expr'''
    t[0] = (t[2], t[1], t[3])

    if t[1][0] == 'INT':
        t
    elif t[1][0] == 'VAR':
        pass
    elif t[1][0] == 'ARR':
        pass
    source_code += 'CMP     ' #+ t[1] + 

    source_code += j_cond[t[2]] + jmp_end() + '\n'


def p_cond_expr(t):
    '''cond : expr'''
    t[0] = t[1]


def p_cond_group(t):
    '''cond : L_PAREN expr R_PAREN'''
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
    pass
    # print(t[1])


def p_str_many(t):
    '''str : str SEPARATOR str'''
    # no action


# error
def p_error(t):
    print("Line ({}) : Syntax error at '{}'".format(t.lineno, t.value))


# build the parser
parser = yacc.yacc()
