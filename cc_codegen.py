

class TokenType:
    terminal = 'terminal'
    expression = 'expression'
    number = 'number'
    string = 'string'


def checkTokenType(token):
    if len(token) == 3:
        return TokenType.expression
    _type, _ = token
    if _type == 'INT':
        return TokenType.number
    elif _type == 'STR':
        return TokenType.string
    raise Exception


def expr_assignment(left,right):
    return f'{left} = {right};'
def expr_operator_add(left,right):
    return f'{left} + {right}'
def expr_operator_minus(left,right):
    return f'{left} - {right}'
def expr_operator_multiply(left,right):
    return f'{left} * {right}'
def expr_operator_divide(left,right):
    return f'{left} / {right}'


switcher = {
    ':=': expr_assignment,
    '+': expr_operator_add,
    '-': expr_operator_minus,
    '*':expr_operator_multiply,
    '/':expr_operator_divide
}
def _expr_generator(node):
    action, left, right = node
    if checkTokenType(left) == TokenType.expression:
        left = _expr_generator(left)
    if checkTokenType(right) == TokenType.expression:
        right = _expr_generator(right)
    return switcher[action](left,right)
def expr_generator(node):
    header = """
    push    rax
    push    rcx
    push    rdx
    """

    footer = """
    mov     []

    pop     rdx
    pop     rcx
    pop     rax
    """



generated_code = expr_generator(root)
print(generated_code)

# Code by Jane

def assign_number(terminal):        #terminal('var','name_var','value')
    return f"""
    push    r8

    mov     r8,{terminal[2]}
    mov     [{terminal[1]}],r8

    pop     r8
    """