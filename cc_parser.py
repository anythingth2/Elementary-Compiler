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
        priority = {
        'STR': 1,
        'INT': 2,
        'ARR': 3
        }
        variables = list(self.storage.values())
        variables.sort(key=lambda var: priority[var.type])
        return variables


variable_initializer = VariableInitializer()


# counter and stack for asm label and loop index
str_ct = 0
lp_ct = 0
end_ct = {'if': 0, 'lp': 0}
pop_ct_stack = []  # store pop round of pop end: and is else checker
lp_stack = []
end_stack = []

# loop operator add/sub
loop_op = {
    'inc': 'add     ',
    'dec': 'sub     '
}


# jump condition map sign (invert for short if)
j_cond = {
    '=': 'jne     ',
    '!=': 'je     ',
    '>': 'jle     ',
    '>=': 'jl     ',
    '<': 'jge     ',
    '<=': 'jg     ',

    'inc': 'jg     ',
    'dec': 'jl     ',
}


def jmp_end(type):  # type is if or lp(loop)
    global end_ct, end_stack
    end_stack.append(f'end{type}{end_ct[type]}:')
    end_ct[type] += 1
    return end_stack[-1][:-1]


def label_end():
    global end_stack
    try:
        return end_stack.pop()
    except IndexError:
        return None


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
    if code: source_code += code

# statement


def p_stm_newline(t):
    '''stm : stm NEWLINE
           | NEWLINE'''
    t[0] = t[1]  # no action, empty line


def p_stm_eot(t):
    '''stm : EOT'''
    t[0] = True
    if end_stack:
        print("Line ({}) : Syntax error expected 'end'".format(t.lineno(1)))
        t[0] = None
        parser.errok()


def p_stm_assign(t):
    '''stm : ID ASSIGNMENT expr'''
    if t[3] == None:
        return None
    elif t[1] not in names:  # for declare
        variable_initializer.register(t[1],
                                      Variable(aliase=f'var_{t[1]}', type='INT', length=1))
    elif type(names[t[1]]) == list:  # require var, not arr
        print("Line ({}) : Syntax error array '{}' expected index".format(
            t.lineno(1), t[1].value))
        parser.errok()
        return None
    names[t[1]] = t[3]
    t[0] = (t[2], ('VAR', t[1]), t[3])
    emit_sourcecode(cc_codegen.assign_number(
        variable_initializer.getVariable(t[1]).aliase, t[3]))


def p_stm_assign_arr(t):
    '''stm : ID ASSIGNMENT L_ARRAY NUMBER R_ARRAY
           | ID ASSIGNMENT L_ELEM_ARRAY elem R_ELEM_ARRAY '''
    if t[1] not in names:
        if t[3] == '[':
            names[t[1]] = [0]*t[4]

            variable_initializer.register(t[1],
                                          Variable(aliase=f'var_{t[1]}', type='ARR', length=t[4]))
        elif t[3] == '{':
            names[t[1]] = t[4]
            variable_initializer.register(t[1],
                                          Variable(aliase=f'var_{t[1]}', type='ARR', length=len(t[4]), init_value=[terminal[1] for terminal in t[4]]))
    t[0] = (t[2], ('ARR', t[1], 0), names[t[1]])
    if None in t[0]:
        t[0] = None


def p_stm_assign_arr_index(t):
    '''stm : ID L_ARRAY expr R_ARRAY ASSIGNMENT expr '''
    t[0] = True
    try:
        variable = variable_initializer.getVariable(t[1])
        emit_sourcecode(cc_codegen.assign_array(variable.aliase, t[3], t[6]))
        global index
        if t[3][0] == 'INT':
            index = t[3][1]

        elif t[3][0] == 'VAR':
            index = names[t[3][1]][1]
        elif t[3][0] == 'ARR':
            index = names[t[3][1]][t[3][2]][1]
        try:
            names[t[1]][index] = t[6]
            t[0] = (t[5], ('ARR', t[1], t[3]), t[6])
            if None in t[0]:
                t[0] = None
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
    '''stm : IF cond
           | ELSE IF cond '''
    if t[1] == 'else' and not pop_ct_stack:
        print("Line ({}) : Syntax error found 'else' without 'if' or 'else if'".format(
            t.lineno(1)))
        t[0] = None
        parser.errok()
    elif t[2]:
        if t[1] == 'if':
            pop_ct_stack.append(1)
            cond = t[2]
        elif t[1] == 'else':
            pop_ct_stack[-1] += 1
            cond = t[3]
            end_label = label_end()
            emit_sourcecode(f'''
        jmp     {jmp_end("if")}
        {end_label}
        ''')
        emit_sourcecode(f'''
    {cc_codegen.expr_generator(cond[1])}
        push    rdi
    {cc_codegen.expr_generator(cond[2])}
        pop     rdx
        cmp     rdx, rdi
        {j_cond[cond[0]]}{jmp_end("if")}
        ''')
        t[0] = True


def p_stm_else(t):
    '''stm : ELSE '''
    t[0] = True
    if pop_ct_stack:
        end_label = label_end()
        emit_sourcecode(f'''
    jmp     {jmp_end("if")}
    {end_label}''')
    else:
        print("Line ({}) : Syntax error found 'else' without 'if' or 'else if'".format(
            t.lineno(1)))
        t[0] = None
        parser.errok()


def p_stm_loop(t):
    '''stm : REPEAT expr TO expr INC expr
           | REPEAT expr TO expr DEC expr '''
    t[0] = True
    pop_ct_stack.append(1)
    index_label = f'idx{lp_ct}'
    indexs[index_label] = t[2]
    variable_initializer.register(index_label,
                                  Variable(aliase=index_label, type='INT', length=1, init_value=0))
    emit_sourcecode(f'''
{cc_codegen.expr_generator(t[2])}
    mov     [{index_label}], rdi
{cc_codegen.expr_generator(t[4])}
    push    rdi
{cc_codegen.expr_generator(t[6])}
    push    rdi
{label_loop()}
    pop     rdx
    pop     rcx
    cmp     [{index_label}], rcx
    {j_cond[t[5]]}{jmp_end("lp")}
    {loop_op[t[5]]}[{index_label}], rdx
    push    rcx
    push    rdx
    ''')


def p_stm_end(t):
    '''stm : END '''
    t[0] = True
    if pop_ct_stack:
        for i in range(pop_ct_stack.pop()):
            end_label = label_end()
            if end_label:
                if 'lp' in end_label:
                    emit_sourcecode(f'\n    jmp     {jmp_loop()}\n    ')
                emit_sourcecode(f'{end_label}\n')
            else:
                print("Line ({}) : Syntax error unexpected 'end'".format(t.lineno(1)))
                t[0] = None
                parser.errok()
    else:
        print("Line ({}) : Syntax error unexpected 'end'".format(t.lineno(1)))
        t[0] = None
        parser.errok()


# expression
def p_expr_op(t):
    '''expr : expr PLUS expr
            | expr MINUS expr
            | expr TIMES expr
            | expr DIVIDE expr
            | expr MODULO expr'''
    if t[2] in ['/', 'mod'] and t[3][0] == 'INT' and t[3][1] == 0:
        print("Line ({}) : Syntax error divide or modulo by zero ".format(t.lineno(3)))
        t[0] = None
        parser.errok()
    t[0] = (t[2], t[1], t[3])
    
    if None in t[0]:
        t[0] = None


def p_expr_uminus(t):
    '''expr : MINUS expr %prec UMINUS'''
    t[0] = (t[1], ('INT', 0), t[2])
    if None in t[0]:
        t[0] = None


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
        print("Line ({}) : Undefined name '{}'".format(t.lineno(1), t[1]))
        t[0] = None
        parser.errok()


def p_expr_name_arr(t):
    '''expr : ID L_ARRAY expr R_ARRAY'''
    try:
        variable = variable_initializer.getVariable(t[1])
        t[0] = ('ARR', variable.aliase, t[3])
    except LookupError:
        print("Line ({}) : Undefined name '{}'".format(t.lineno(1), t[1]))
        t[0] = None
        parser.errok()
    except ValueError:
        print("Line ({}) : Index '{}[{}]' out of range".format(
            t.lineno(1), t[1].value, t[3].value))
        t[0] = None
        parser.errok()
    # default t[0] = None

# condition
def p_cond_op(t):
    '''cond : expr EQUALS expr
            | expr NOT_EQUALS expr
            | expr UPWARD expr
            | expr UPWARD_EQUALS expr
            | expr DOWNWARD expr
            | expr DOWNWARD_EQUALS expr'''
    t[0] = (t[2], t[1], t[3])
    if None in t[0]:
        t[0] = None


def p_cond_expr(t):
    '''cond : expr'''
    t[0] = ('!=', t[1], ('INT', 0))
    if None in t[0]:
        t[0] = None


# element
def p_elem(t):
    '''elem : NUMBER'''
    t[0] = [('INT', t[1])]


def p_elem_many(t):
    '''elem : NUMBER SEPARATOR elem'''
    t[3].insert(0, ('INT', t[1]))
    t[0] = t[3]


def p_stm_print(t):
    '''stm : PRINT msg '''
    t[0] = True
    emit_sourcecode(cc_codegen.printf_generator(variable_initializer, t[2]))

def p_stm_print_hex(t):
    '''stm : PRINT_HEX msg '''
    t[0] = True
    emit_sourcecode(cc_codegen.printf_generator(variable_initializer, t[2], isHex=True))


# string
def p_msg(t):
    '''msg : str SEPARATOR msg
           | str '''
    if len(t) == 2:
        t[0] = [t[1]]
    else:
        t[0] = [t[1]] + t[3]


def p_str(t):
    '''str : expr
           | STRING'''
    global strtemp
    strtemp += f'{t[1]}'
    t[0] = t[1]


# ---------------------------------------------------------------------------------
# error


def p_error(t):
    pass
    # if t:
    #     print("Line ({}) : Syntax error at '{}'".format(t.lineno, t.value))
    #     parser.errok()

# # error statement
# def p_err_stm(t):
#     '''stm : error'''
#     print("Line ({}) : Syntax error at '{}' statement not recognize".format(t.lineno(1), t[1]))
#     parser.errok()

def p_err_assign(t):
    '''stm : ID error'''
    print("Line ({}) : Syntax error after identifier '{}'".format(t.lineno(2), t[2].value))
    parser.errok()

def p_err_assign_value(t):
    '''stm : ID ASSIGNMENT error'''
    print("Line ({}) : Syntax error for assignment at '{}'".format(t.lineno(3), t[3].value))
    parser.errok()

def p_err_assign_arr(t):
    '''stm : ID ASSIGNMENT L_ARRAY expr error
           | ID ASSIGNMENT L_ELEM_ARRAY elem error'''
    if t[3] == '[':
        print("Line ({}) : Syntax error for array size at '{}'".format(t.lineno(5), t[5].value))
    elif t[3] == '{':
        print("Line ({}) : Syntax error for array element at '{}'".format(t.lineno(5), t[5].value))
    parser.errok()

def p_err_arr_index(t):
    '''stm : ID L_ARRAY expr error'''
    print("Line ({}) : Syntax error for array index at '{}' expected ']'".format(t.lineno(4), t[4].value))
    parser.errok()

# error if
def p_err_if_cond(t):
    '''stm : IF error'''
    print("Line ({}) : Syntax error expected condition after 'if''".format(t.lineno(2)))
    parser.errok()

def p_err_else(t):
    '''stm : ELSE error'''
    print("Line ({}) : Syntax error expected 'if' or '<newline>' after 'else'".format(t.lineno(2)))
    parser.errok()

def p_err_elseif_cond(t):
    '''stm : ELSE IF error'''
    print("Line ({}) : Syntax error expected condition after 'else if'".format(t.lineno(3)))
    parser.errok()


# error loop
def p_err_loop_to(t):
    '''stm : REPEAT expr error'''
    print("Line ({}) : Syntax error 'repeat' expected 'to'".format(t.lineno(3)))
    parser.errok()

def p_err_loop_step(t):
    '''stm : REPEAT expr TO expr error'''
    print("Line ({}) : Syntax error 'repeat' expected 'inc' or 'dec'".format(t.lineno(5)))
    parser.errok()


# error print
def p_err_print(t):
    '''stm : PRINT error '''
    print("Line ({}) : Syntax error after 'show'".format(t.lineno(2), t[2]))
    parser.errok()

def p_err_print_hex(t):
    '''stm : PRINT_HEX error '''
    print("Line ({}) : Syntax error after 'show_hex'".format(t.lineno(2), t[2]))
    parser.errok()

# error expression
def p_err_expr_op(t):
    '''expr : expr PLUS error
            | expr MINUS error
            | expr TIMES error
            | expr DIVIDE error
            | expr MODULO error'''
    print("Line ({}) : Syntax error at '{}' in expression".format(
        t.lineno(3), t[3].value))
    parser.errok()

def p_err_expr_paren(t):
    '''expr : L_PAREN expr error'''
    print("Line ({}) : Syntax error expected ')'".format(t.lineno(3), t[3].value))
    parser.errok()

# error condition
def p_err_cond_op(t):
    '''expr : expr EQUALS error
            | expr NOT_EQUALS error
            | expr UPWARD error
            | expr UPWARD_EQUALS error
            | expr DOWNWARD error
            | expr DOWNWARD_EQUALS error'''
    print("Line ({}) : Syntax error at '{}' in condition".format(t.lineno(3), t[3].value))
    parser.errok()

# # error string
# def p_str_many(t):
#     '''str : str error str'''
#     print("Line ({}) : Syntax error unexpected '{}' between element".format(t.lineno(2), t[2].value))
#     parser.errok()


# build the parser
parser = yacc.yacc()
