import ply.yacc as yacc
from cc_lexer import tokens
from cc_codegen import *


# Parsing rules
precedence = (
    ('left', 'EQUALS', 'NOT_EQUALS'),
    ('left', 'UPWARD', 'UPWARD_EQUALS', 'DOWNWARD', 'DOWNWARD_EQUALS'),

    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'MODULO'),
    ('right', 'UMINUS'),

    ('left', 'L_PAREN', 'R_PAREN', 'L_ARRAY', 'R_ARRAY'),
)

# dictionary 
names = {}      # variable names = { 'n':3, 'ar':[1,2,3], ... }
indexs = {}     # loop indexs     
strings = {}    # printed strings
strlens = {}    # string lengths

# temp before store to strings = {}
strtemp = ''

# counter and stack for asm label and loop index
str_ct = 0
lp_ct = 0
end_ct = {'if':0, 'lp':0}
lp_stack = []
end_stack = []

# else checker
else_checker = False 

# # if/else/loop match checker
# end_checker = []
# def mark_end(lineno):
#     end_checker.append(lineno)

# def unmark_end():
#     try:
#         end_checker.pop()

# jump condition map sign (invert for short if)
j_cond = {
    '='  : 'jne   ',
    '!=' : 'je    ',
    '>'  : 'jle   ',
    '>=' : 'jl    ',
    '<'  : 'jge   ',
    '<=' : 'jg    ',

    'inc': 'jg    ',
    'dec': 'jl    ',
}

def jmp_end(type):
    # type is if or lp(loop)
    end_stack.append('end'+type+str(end_ct[type])+':')
    end_ct[type] += 1
    return end_stack[-1][:-1]

def label_end(lineno):
    try:
        return end_stack.pop()
    except IndexError:
        print("Line ({}) : Syntax error unexpected 'end'".format(lineno))

def label_loop():
    lp_stack.append('lp'+str(lp_ct))
    lp_ct += 1
    return lp_stack[-1]+':'

def jmp_loop():
    try:
        return lp_stack.pop()
    except IndexError:
        pass    # no action, error same unexpected 'end'

# for generate nasm code
source_code = ''

### Tag type ###
# Integer     -> ('INT', expr)
# Variable    -> ('VAR', ID)
# Array       -> ('ARR', ID, INDEX) *default INDEX = 0

# statement
def p_stm_assign(t):
    '''stm : ID ASSIGNMENT expr NEWLINE'''
    if checkTokenType(t[3]) == TokenType.expression:
        expr_generator(t[3])
    names[t[1]] = t[3]
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
    # compare and jump are in cond
    else_checker = True

def p_stm_else(t):
    '''stm : ELSE NEWLINE'''
    if else_checker:
        jmp_end('if')
        else_checker = False
    else:
        print("Line ({}) : Syntax error found 'else' without 'if'".format(t.lineno))

def p_stm_loop(t):
    '''stm : REPEAT expr TO expr INC expr NEWLINE
           | REPEAT expr TO expr DEC expr NEWLINE'''
    indexs['idx'+str(lp_ct)] = t[2]
    source_code +=  label_loop()+'\n'+\
                    '   cmp     idx'+str(lp_ct-1)+', '+str(t[4])+'\n'+\
                    '   '+j_cond[t[5]]+'      '+jmp_end('lp')+'\n'+\
                    '   add     idx'+str(lp_ct-1)+', '+str(t[6])+'\n'

def p_stm_end(t):
    '''stm : END NEWLINE'''
    end_label = label_end(t.lineno)
    if 'lp' in end_label:
        source_code +=  '   j       '+jmp_loop()+'\n'
    source_code +=  '   '+end_label+'\n'

def p_stm_print(t):
    '''stm : PRINT str NEWLINE'''
    strings['msg'+str(str_ct)] = strtemp
    strlens['len'+str(str_ct)] = len(strtemp)
    strtemp = ''
    source_code +=  'mov    edx, len'+str(str_ct)+'\n'+\
                    'mov    ecx, msg'+str(str_ct)+'\n'+\
                    'mov    ebx, 1\n'+\
                    'mov    eax, 4\n'+\
                    'int    0x80\n'
    str_ct += 1


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
    '''cond : expr EQUALS expr
            | expr NOT_EQUALS expr
            | expr UPWARD expr
            | expr UPWARD_EQUALS expr
            | expr DOWNWARD expr
            | expr DOWNWARD_EQUALS expr'''
    t[0] = (t[2], t[1], t[3])
    pass
    # if t[1][0] == 'INT':
    #     pass
    # elif t[1][0] == 'VAR':
    #     pass
    # elif t[1][0] == 'ARR':
    #     pass
    # source_code += 'CMP     ' #+ t[1] + 
    # source_code += j_cond[t[2]] + jmp_end() + '\n'


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
    strtemp += str(t[1])


def p_str_many(t):
    '''str : str SEPARATOR str'''
    pass    # no action


# error
def p_error(t):
    print("Line ({}) : Syntax error at '{}'".format(t.lineno, t.value))


# build the parser
parser = yacc.yacc()