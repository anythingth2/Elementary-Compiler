expression_count = 0


class TokenType:
    terminal = 'terminal'
    expression = 'expression'
    number = 'number'
    string = 'string'
    variable = 'variable'


def isTerminal(token):
    return len(token) == 2


def checkTokenType(token):
    if len(token) == 3:
        return TokenType.expression
    _type, _ = token
    if _type == 'INT':
        return TokenType.number
    elif _type == 'STR':
        return TokenType.string
    elif _type == 'VAR':
        return TokenType.variable
    raise Exception


def getReferenceFromToken(token):
    return f'[{token[1]}]' if token[0] == 'VAR' else token[1]


expr_workspace = ''


def emit_expression_code(code):
    global expr_workspace
    expr_workspace += code
def get_expression_code():
    global expr_workspace
    t = expr_workspace
    expr_workspace = ''
    return t

def expr_assignment(left, right):
    if checkTokenType(left) == TokenType.expression:
        left = _expr_generator(left)

    if checkTokenType(right) == TokenType.expression:
        right = _expr_generator(right)


switcher = {
    ':=': expr_assignment,
    '+': 'add   rbx, rax',
    '-': 'sub   rbx, rax',
    '*': 'imul  rbx, rax',
    '/': '''
        xchg    rbx, rax
        cqo
        mov     rcx, rbx
        idiv    rcx
        mov     rbx, rax
    ''',
    'mod': '''
        xchg    rbx, rax
        cqo
        mov     rcx, rbx
        idiv    rcx
        mov     rbx, rdx
    '''
}


def _expr_generator(node):

    action, left, right = node

    if checkTokenType(left) == TokenType.expression:
        # switcher[action](left, right)
        _expr_generator(left)
    else:
        emit_expression_code(f'''
        mov     rax, {getReferenceFromToken(left)}
        ''')
    emit_expression_code('''
    push    rax
    ''')
    if checkTokenType(right) == TokenType.expression:

        # switcher[action](left, right)
        _expr_generator(right)
    else:
        emit_expression_code(f'''
    mov     rax, {getReferenceFromToken(right)}
        ''')
    emit_expression_code('''
    pop     rbx
    ''')
    # left is rbx
    # right is rax
    emit_expression_code(f'''
{switcher[action]}
    mov     rax, rbx
    ''')


def expr_generator(expr_root):

    header = f"""
    push    rax
    push    rbx
    push    rcx
    push    rdx
    """

    _expr_generator(expr_root)
    code = get_expression_code()

    footer = f"""
    mov     rdi, rax

    pop     rdx
    pop     rcx
    pop     rbx
    pop     rax

    """

    return header + code + footer


# Code by Jane

def assign_number(var_name, expr_root):  # terminal('var','name_var','value')

    return expr_generator(expr_root) + f"""
    mov     [{var_name}], rdi
    """

# อาเรย์ที่เก็บต้องเป็นขนาด qd แต่ถ้าไม่ใช่ต้องทำการแก้ไขโค้ด
# โดยต้องส่งขนาดของอาเรย์ว่าเป็น dw dd qd
# แล้วค่อยทำการเลือกว่าจะให้ค่าใส่ด้วยอะไร และaddress array ต้องเพิ่มทีละเท่าไหร่


def assign_array(terminal):  # terminal('var','name_var','index','value')
    return f"""
    push    r8                                      ;save register

    mov     r8,qword [{terminal[3]}]                ;temp=value
    mov     [{terminal[1]}+{terminal[2]}*8]         ;array[index]=temp

    pop     r8
    """
