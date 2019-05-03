import platform
import cc_parser
expression_count = 0


class TokenType:
    terminal = 'terminal'
    expression = 'expression'
    number = 'number'
    string = 'string'
    variable = 'variable'
    array = 'array'


def isTerminal(token):
    return len(token) != 3 or token[0] == 'ARR'


def checkTokenType(token):
    if token:
        if len(token) == 3 and  token[0] != 'ARR':
            return TokenType.expression
        _type = token[0]
        if _type == 'INT':
            return TokenType.number
        elif _type == 'STR':
            return TokenType.string
        elif _type == 'VAR':
            return TokenType.variable
        elif _type == 'ARR':
            return TokenType.array
        # raise Exception


def getReferenceFromToken(token):
    if token:
        return f'[{token[1]}]' if token[0] == 'VAR' else token[1]


def getRegerenceFromArray(token):
    _, var_name, index_root = token
    source_code = ''
    source_code += expr_generator(index_root)

    source_code += f'''
    mov     r12, {var_name}
    mov     rax, qword [r12 + rdi * 8]
    '''
    return source_code


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
    if left:
        if checkTokenType(left) == TokenType.expression:
            left = _expr_generator(left)

    if right:
        if checkTokenType(right) == TokenType.expression:
            right = _expr_generator(right)


switcher = {
    ':=': expr_assignment,
    '+': 'add     rbx, rax',
    '-': 'sub     rbx, rax',
    '*': 'imul     rbx, rax',
    '/': '''
    xchg     rbx, rax
    cqo
    mov     rcx, rbx
    idiv     rcx
    mov     rbx, rax
    ''',
    'mod': '''
    xchg     rbx, rax
    cqo
    mov     rcx, rbx
    idiv     rcx
    mov     rbx, rdx
    '''
}


def _expr_generator(node):
    if node:
        action, left, right = node

        if checkTokenType(left) == TokenType.expression:
            # switcher[action](left, right)
            _expr_generator(left)
        else:
            if checkTokenType(left) == TokenType.array:
                emit_expression_code(getRegerenceFromArray(left))
            else:
                emit_expression_code(f'''
        mov     rax, {getReferenceFromToken(left)}
        ''')
        emit_expression_code('''
    push    rax
    ''')
        if checkTokenType(right) == TokenType.expression:

            _expr_generator(right)
        else:
            if checkTokenType(right) == TokenType.array:
                emit_expression_code(getRegerenceFromArray(right))
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
    if expr_root:
        save_register = set(['rax'])
        header = f"""
;---------------------- expr start ---------------------
    push    rax
    push    rbx
    push    rcx
    push    rdx
    """
        
 

        if isTerminal(expr_root):
            if checkTokenType(expr_root) == TokenType.array:
                code = getRegerenceFromArray(expr_root)
                code += '''
                mov     rdi, rax
                '''
            else:
                code = f'''
            mov     rdi, {getReferenceFromToken(expr_root)}
            '''
        else:
            _expr_generator(expr_root)
            code = get_expression_code()
            code += '''
            mov     rdi, rax
            '''
        footer = f"""
    pop     rdx
    pop     rcx
    pop     rbx
    pop     rax
;---------------------- expr end ----------------------
    """


        return header + code + footer


# Code by Jane

def assign_number(var_name, expr_root):  # terminal('var','name_var','value')
    if var_name and expr_root:
        return expr_generator(expr_root) + f"""
    mov     [{var_name}], rdi
    """

# อาเรย์ที่เก็บต้องเป็นขนาด qd แต่ถ้าไม่ใช่ต้องทำการแก้ไขโค้ด
# โดยต้องส่งขนาดของอาเรย์ว่าเป็น dw dd qd
# แล้วค่อยทำการเลือกว่าจะให้ค่าใส่ด้วยอะไร และaddress array ต้องเพิ่มทีละเท่าไหร่


def assign_array(var_name, index_root, expr_root):  
    return f'''
{expr_generator(index_root)}
    push    rdi
{expr_generator(expr_root)}
    pop     r11
    mov     r12, {var_name}
    mov     [r12 + r11 * 8], qword rdi
    '''

printf_count = 0


def printf_generator(variable_initializer, params, isHex=False):
    save_registers = set(['rax', 'rcx'])
    argument_registers = ['rsi', 'rdx', 'rcx', 'r8', 'r9']
    message_format = ''
    source_code = ''
    for param in params:
        if isinstance(param, str):
            message_format += param
        else:
            message_format += '0x%x' if isHex else '%d'
            argument = argument_registers.pop(0)
            save_registers.add(argument)
            source_code += expr_generator(param)
            source_code += f'''
            mov     {argument}, rdi
            '''
    global printf_count
    format_label = f'printf_{printf_count}'
    printf_count += 1
    variable_initializer.register(format_label, cc_parser.Variable(
        aliase=format_label, type='STR', init_value=message_format))

    source_code += f'''
        mov     rdi, {format_label}
        xor     rax, rax
        call    {'_' if platform.system() == 'Darwin' else ''}printf
    '''

    for register in save_registers:
        source_code = f'''
        push    {register}
{source_code}
        pop     {register}
        '''
    if len(save_registers) % 2 == 1:
        register = list(save_registers)[0]
        source_code = f'''
        push    {register}
{source_code}
        pop     {register}
        '''

    return source_code
