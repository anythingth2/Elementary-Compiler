import ply.yacc as yacc
from cc_lexer import tokens
import cc_codegen


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

# dictionary
names = {}      # variable names = { 'n':3, 'ar':[1,2,3], ... }
indexs = {}     # loop indexs
strings = {}    # printed strings
strlens = {}    # string lengths

# temp before store to strings = {}
strtemp = ''


class Variable:
    def __init__(self, aliase, type, length=None, init_value=None):
        self.aliase = aliase
        self.type = type
        self.length = length
        self.init_value = init_value


class VariableInitializer:
    def __init__(self):
        self.storage = {}

    def register(self, label, variable):
        self.storage[label] = variable

    def getVariable(self, label):
        return self.storage[label]

    def getAllVariable(self):
        return self.storage.values()


variable_initializer = VariableInitializer()


# counter and stack for asm label and loop index
str_ct = 0
lp_ct = 0
end_ct = {'if': 0, 'lp': 0}
lp_stack = []
end_stack = []

# else checker
else_checker = False

# jump condition map sign (invert for short if)
j_cond = {
    '=': 'jne   ',
    '!=': 'je    ',
    '>': 'jle   ',
    '>=': 'jl    ',
    '<': 'jge   ',
    '<=': 'jg    ',

    'inc': 'jg    ',
    'dec': 'jl    ',
}


def jmp_end(type):  # type is if or lp(loop)
    global end_ct, end_stack
    end_stack.append(f'end{type}{end_ct[type]}:')
    end_ct[type] += 1
    return end_stack[-1][:-1]


def label_end(lineno):
    global end_stack
    try:
        return end_stack.pop()
    except IndexError:
        print("Line ({}) : Syntax error unexpected 'end'".format(lineno))
        parser.errok()


def label_loop():
    global lp_ct, lp_stack
    lp_stack.append(f'lp{lp_ct}')
    lp_ct += 1
    return lp_stack[-1]+':'


def jmp_loop():
    global lp_stack
    try:
        return lp_stack.pop()
    except IndexError:
        pass    # no action, error same unexpected 'end'

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


def p_stm_newline(t):
    '''stm : NEWLINE'''
    pass  # no action, empty line


def p_stm_assign(t):
    '''stm : ID ASSIGNMENT expr NEWLINE'''
    if t[1] not in names: # for declare
        variable_initializer.register(t[1],
                                      Variable(aliase=f'var_{t[1]}', type='INT', length=1))
    else:
        if type(names[t[1]]) == list: # require var, not arr
            print("Line ({}) : Syntax error array '{}' expected index".format(
                t.lineno(1), t[1].value))
            return None
            # t[0] = None
            # parser.errok()
    names[t[1]] = t[3]
    t[0] = (t[2], ('VAR', t[1]), t[3])
    emit_sourcecode(cc_codegen.assign_number(
        variable_initializer.getVariable(t[1]).aliase, t[3]))


def p_stm_assign_arr(t):
    '''stm : ID ASSIGNMENT L_ARRAY NUMBER R_ARRAY NEWLINE
           | ID ASSIGNMENT L_ELEM_ARRAY elem R_ELEM_ARRAY NEWLINE'''
    if t[1] not in names:
        if t[3] == '[':
            names[t[1]] = [0]*t[4]

            variable_initializer.register(t[1],
                                          Variable(aliase=f'var_{t[1]}', type='ARR', length=t[4]))
        elif t[3] == '{':
            names[t[1]] = t[4]
            variable_initializer.register(t[1],
                                          Variable(aliase=f'var_{t[1]}', type='ARR', length=len(t[4]), init_value=[terminal[1] for terminal in t[4]]))
    print(f'stm_assign_array {t[4]}')
    t[0] = (t[2], ('ARR', t[1], 0), names[t[1]])


def p_stm_assign_arr_index(t):
    '''stm : ID L_ARRAY expr R_ARRAY ASSIGNMENT expr NEWLINE'''
    try:
        names[t[1]][0]
        if t[3][0] == 'INT':
            index = t[3][1]
        elif t[3][0] == 'VAR':
            index = names[t[3][1]][1]
        elif t[3][0] == 'ARR':
            index = names[t[3][1]][t[3][2]][1]
        try:
            names[t[1]][index] = t[6]
            t[0] = (t[5], ('ARR', t[1], t[3]), t[6])
        except ValueError:
            print("Line ({}) : Index '{}[{}]' out of range".format(
                t.lineno(1), t[1], t[3]))
            t[0] = None
            parser.errok()
    except LookupError:
        print("Line ({}) : Undefined name '{}'".format(t.lineno(1), t[1]))
        t[0] = None
        parser.errok()
    except TypeError:
        print("Line ({}) : Syntax error '{}' is not array".format(
            t.lineno(1), t[1]))
        t[0] = None
        parser.errok()


def p_stm_if(t):
    '''stm : IF cond NEWLINE
           | ELSE IF cond NEWLINE'''
    # compare and jump are in cond
    global else_checker
    else_checker = True


def p_stm_else(t):
    '''stm : ELSE NEWLINE'''
    global else_checker
    if else_checker:
        end_label = label_end(t.lineno(1))
        emit_sourcecode('   jmp       {jmp_end()}\n')
        emit_sourcecode('   {end_label}\n')
        else_checker = False
    else:
        print("Line ({}) : Syntax error found 'else' without 'if' or 'else if'".format(
            t.lineno(1)))
        t[0] = None
        parser.errok()


def p_stm_loop(t):
    '''stm : REPEAT expr TO expr INC expr NEWLINE
           | REPEAT expr TO expr DEC expr NEWLINE'''
    index_label = f'idx{lp_ct}'
    indexs[index_label] = t[2]
    variable_initializer.register(index_label,
                                  Variable(aliase=index_label, type='INT', length=1, init_value=0))
    # emit_sourcecode(cc_codegen.expr_generator(t[2]))
    # emit_sourcecode(f'  mov     [{index_label}], dword rdi\n')
    # emit_sourcecode(f'{label_loop()}\n')
    # emit_sourcecode(f'  cmp     [{index_label}], dword {t[4][1]}\n')
    # emit_sourcecode(f'  {j_cond[t[5]]}     {jmp_end("lp")}\n')
    # emit_sourcecode(f'  add     [{index_label}], dword {t[6][1]}\n')
    emit_sourcecode(cc_codegen.expr_generator(t[2]))
    emit_sourcecode(f'  mov     [{index_label}], dword rdi\n')
    emit_sourcecode(cc_codegen.expr_generator(t[4]))
    emit_sourcecode('   push    rdi\n') # compared value
    emit_sourcecode(cc_codegen.expr_generator(t[6]))
    emit_sourcecode('   push    rdi\n') # inc/dec
    emit_sourcecode(f'{label_loop()}\n')
    emit_sourcecode('   pop     rdx\n') # get inc/dec
    emit_sourcecode('   pop     rcx\n') # get compared value
    emit_sourcecode(f'  cmp     [{index_label}], dword rcx\n')
    emit_sourcecode(f'  {j_cond[t[5]]}     {jmp_end("lp")}\n')
    emit_sourcecode(f'  add     [{index_label}], dword rdx\n')
    emit_sourcecode('   push    rcx\n') # reserve inc/dec
    emit_sourcecode('   push    rdx\n') # reserve compared value


def p_stm_end(t):
    '''stm : END NEWLINE'''
    end_label = label_end(t.lineno(1))
    if end_label:
        if 'lp' in end_label:
            emit_sourcecode(f'   jmp       {jmp_loop()}\n')
        emit_sourcecode(f'   {end_label}\n')


def p_stm_print(t):
    '''stm : PRINT str NEWLINE'''
    global strtemp, str_ct
    str_label = f'msg{str_ct}'
    strings[str_label] = strtemp
    variable_initializer.register(str_label,
                                  Variable(aliase=str_label, type='STR', init_value=strtemp))
    strlen_label = f'len{str_ct}'
    strlens[strlen_label] = len(strtemp)
    variable_initializer.register(strlen_label,
                                  Variable(aliase=strlen_label, type='INT', length=1, init_value=len(strtemp)))
    strtemp = ''
    emit_sourcecode('mov    edx, len{str_ct}\n')
    emit_sourcecode('mov    ecx, msg{str_ct}\n')
    emit_sourcecode('mov    ebx, 1\n')
    emit_sourcecode('mov    eax, 4\n')
    emit_sourcecode('int    0x80\n')
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
        variable = variable_initializer.getVariable(t[1])
        if variable.type == 'ARR':
            t[0] = ('ARR', variable.aliase, 0)
        else:
            t[0] = ('VAR', variable.aliase)
    except LookupError:
        print("Line ({}) : Undefined name '{}'".format(
            t.lineno(1), t[1].value))
        t[0] = None
        parser.errok()


def p_expr_name_arr(t):
    '''expr : ID L_ARRAY expr R_ARRAY'''
    try:
        t[0] = ('ARR', t[1], t[3])
    except LookupError:
        print("Line ({}) : Undefined name '{}'".format(
            t.lineno(1), t[1].value))
        t[0] = None
        parser.errok()
    except ValueError:
        print("Line ({}) : Index '{}[{}]' out of range".format(
            t.lineno(1), t[1].value, t[3].value))
        t[0] = None
        parser.errok()


# condition
def p_cond_op(t):
    '''cond : expr EQUALS expr
            | expr NOT_EQUALS expr
            | expr UPWARD expr
            | expr UPWARD_EQUALS expr
            | expr DOWNWARD expr
            | expr DOWNWARD_EQUALS expr'''
    t[0] = (t[2], t[1], t[3])
    emit_sourcecode(cc_codegen.expr_generator(t[1]))
    emit_sourcecode('push   rdi\n')
    emit_sourcecode(cc_codegen.expr_generator(t[3]))
    emit_sourcecode('pop    rdx\n')
    emit_sourcecode('cmp    rdi, rdx\n')
    emit_sourcecode(f'{j_cond[t[2]]}{jmp_end("if")}\n')


def p_cond_expr(t):
    '''cond : expr'''
    t[0] = ('!=', t[1], 0)
    emit_sourcecode(cc_codegen.expr_generator(t[1]))
    emit_sourcecode('cmp    rdi, 0\n')
    emit_sourcecode('{j_cond["!="]}{jmp_end("if")}\n')


# element
def p_elem(t):
    '''elem : NUMBER'''
    t[0] = [('INT', t[1])]


def p_elem_many(t):
    '''elem : NUMBER SEPARATOR elem'''
    t[3].insert(0, ('INT', t[1]))
    t[0] = t[3]


# string
def p_str(t):
    '''str : expr
           | STRING'''
    global strtemp
    strtemp += f't[1]'


def p_str_many(t):
    '''str : str SEPARATOR str'''
    pass    # no action

# ---------------------------------------------------------------------------------
# error


def p_error(t):
    pass
    # print("Line ({}) : Syntax error at '{}'".format(t.lineno, t.value))
    # parser.errok()

# # error assign
# def p_err_id(t):
#     '''stm : error ASSIGNMENT expr NEWLINE'''
#     print("Line ({}) : Syntax error can't assign to '{}'".format(t.lineno(1), t[1]))
#     parser.errok()

# def p_err_assign(t):
#     '''stm : ID error expr NEWLINE'''
#     print("Line ({}) : Syntax error unexpected '{}'".format(t.lineno(2), t[2]))
#     parser.errok()

# def p_err_assign_arr_l(t):
#     '''stm : ID ASSIGNMENT error expr R_ARRAY NEWLINE
#            | ID ASSIGNMENT error elem R_ELEM_ARRAY NEWLINE'''
#     print("Line ({}) : Syntax error unexpected '{}'".format(t.lineno(3), t[3]))
#     parser.errok()

# def p_err_assign_arr_r(t):
#     '''stm : ID ASSIGNMENT L_ARRAY expr error NEWLINE
#            | ID ASSIGNMENT L_ELEM_ARRAY elem error NEWLINE'''
#     print("Line ({}) : Syntax error unexpected '{}'".format(t.lineno(5), t[5]))
#     parser.errok()

# def p_err_arr_index_l(t):
#     '''stm : ID error expr R_ARRAY ASSIGNMENT expr NEWLINE'''
#     print("Line ({}) : Syntax error unexpected '{}'".format(t.lineno(2), t[2]))
#     parser.errok()

# def p_err_arr_index_r(t):
#     '''stm : ID L_ARRAY expr error ASSIGNMENT expr NEWLINE'''
#     print("Line ({}) : Syntax error unexpected '{}'".format(t.lineno(4), t[4]))
#     parser.errok()

# def p_err_arr_index_assign(t):
#     '''stm : ID L_ARRAY expr R_ARRAY error expr NEWLINE'''
#     print("Line ({}) : Syntax error unexpected '{}'".format(t.lineno(5), t[5]))
#     parser.errok()

# # error if
# def p_err_if(t):
#     '''stm : error cond NEWLINE
#            | error IF cond NEWLINE
#            | ELSE error cond NEWLINE'''
#     print("Line ({}) : Syntax error expected 'if' or 'else if' before condition".format(t.lineno(1)))
#     parser.errok()

# # error loop
# def p_err_loop_repeat(t):
#     '''stm : error expr TO expr INC expr NEWLINE
#            | error expr TO expr DEC expr NEWLINE'''
#     print("Line ({}) : Syntax error expected 'repeat' before".format(t.lineno(1)))
#     parser.errok()

# def p_err_loop_to(t):
#     '''stm : REPEAT expr error expr INC expr NEWLINE
#            | REPEAT expr error expr DEC expr NEWLINE'''
#     print("Line ({}) : Syntax error 'repeat' expected 'to'".format(t.lineno(3)))
#     parser.errok()

# def p_err_loop_step(t):
#     '''stm : REPEAT expr TO expr error expr NEWLINE'''
#     print("Line ({}) : Syntax error expected 'inc' or 'dec'".format(t.lineno(5)))
#     parser.errok()

# # error print
# def p_err_print(t):
#     '''stm : error str NEWLINE'''
#     print("Line ({}) : Syntax error expected 'show' before string".format(t.lineno(1)))
#     parser.errok()

# def p_err_string(t):
#     '''stm : PRINT error NEWLINE'''
#     print("Line ({}) : Syntax error unexpected '{}' after 'show'".format(t.lineno(2), t[2]))
#     parser.errok()

# error expression


def p_err_expr_op(t):
    '''expr : expr error expr'''
    print("Line ({}) : Syntax error unexpected '{}' between expression".format(
        t.lineno(2), t[2].value))
    parser.errok()

# def p_err_expr_uminus(t):
#     '''expr : error expr %prec UMINUS'''
#     print("Line ({}) : Syntax error unexpected '{}' before expression".format(t.lineno(1), t[1].value))
#     parser.errok()

# def p_err_expr_lparen(t):
#     '''expr : error expr R_PAREN'''
#     print("Line ({}) : Syntax error unexpected '{}'".format(t.lineno(1), t[1].value))
#     parser.errok()

# def p_err_expr_rparen(t):
#     '''expr : L_PAREN expr error'''
#     print("Line ({}) : Syntax error unexpected '{}'".format(t.lineno(3), t[3].value))
#     parser.errok()

# # error value
# def p_err_value(t):
#     '''expr : error'''
#     print("Line ({}) : Syntax error unexpected '{}'".format(t.lineno(1), t[1].value))
#     parser.errok()

# def p_err_name_larr(t):
#     '''expr : ID error expr R_ARRAY'''
#     print("Line ({}) : Syntax error unexpected '{}'".format(t.lineno(2), t[2].value))
#     parser.errok()

# def p_err_name_rarr(t):
#     '''expr : ID L_ARRAY expr error'''
#     print("Line ({}) : Syntax error unexpected '{}'".format(t.lineno(4), t[4].value))
#     parser.errok()

# # error condition
# def p_cond_op(t):
#     '''cond : expr error expr'''
#     print("Line ({}) : Syntax error unexpected '{}' between expression".format(t.lineno(2), t[2].value))
#     parser.errok()

# def p_cond_expr(t):
#     '''cond : error'''
#     print("Line ({}) : Syntax error unexpected '{}'".format(t.lineno(1), t[1].value))
#     parser.errok()

# def p_err_cond_lparen(t):
#     '''cond : error expr R_PAREN'''
#     print("Line ({}) : Syntax error unexpected '{}'".format(t.lineno(1), t[1].value))
#     parser.errok()

# def p_err_cond_rparen(t):
#     '''cond : L_PAREN expr error'''
#     print("Line ({}) : Syntax error unexpected '{}'".format(t.lineno(3), t[3].value))
#     parser.errok()


# # error element
# def p_err_elem_many(t):
#     '''elem : expr error elem'''
#     print("Line ({}) : Syntax error unexpected '{}' between element".format(t.lineno(2), t[2].value))
#     parser.errok()


# # error string
# def p_str_many(t):
#     '''str : str error str'''
#     print("Line ({}) : Syntax error unexpected '{}' between element".format(t.lineno(2), t[2].value))
#     parser.errok()

# build the parser
parser = yacc.yacc()
