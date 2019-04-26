import cc_parser
parser = cc_parser.parser

test_case = 'x := 3+1*99-94/11'
test_case += '\n'

root = parser.parse(test_case)
print(root)


class TokenType:
    terminal = 'terminal'
    expression = 'expression'
    number = 'number'
    string = 'string'


def checkTokenType(token):
    if isinstance(token, tuple):
        return TokenType.expression
    elif isinstance(token, int):
        return TokenType.number
    elif isinstance(token, str):
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


def code_generator(node):
    action, left, right = node
    if checkTokenType(left) == TokenType.expression:
        left = code_generator(left)
    if checkTokenType(right) == TokenType.expression:
        right = code_generator(right)
    return switcher[action](left,right)


generated_code = code_generator(root)
print(generated_code)
