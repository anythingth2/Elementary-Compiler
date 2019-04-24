import ply.lex as lex


tokens = (
    'NAME', 'NUMBER', "STRING",
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MODULO', 'ASSIGNMENT',
    'L_PAREN', 'R_PAREN', 'PRINT',
    "SEPARATOR", "L_ARRAY", 'R_ARRAY', 'L_SIZE_ARRAY', 'R_SIZE_ARRAY',
    'EQUALS', 'NOT_EQUALS', 'UPWARD', 'UPWARD_EQUALS', 'DOWNWARD', 'DOWNWARD_EQUALS',
    'IF', 'ELSE', 'BEGIN', 'END', 'REPEAT', 'INC', 'DEC', 'TO'
)

# Tokens


t_STRING = r'\"[a-zA-Z0-9_]*\"'

t_PRINT = r'show:'
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_MODULO = r'mod'
t_ASSIGNMENT = r':='

t_EQUALS = r'='
t_NOT_EQUALS = r'!='
t_UPWARD = r'>'
t_UPWARD_EQUALS = r'>='
t_DOWNWARD = r'<'
t_DOWNWARD_EQUALS = r'<='

t_SEPARATOR = r','
t_L_ARRAY = r'\['
t_R_ARRAY = r'\]'
t_L_SIZE_ARRAY = r'\{'
t_R_SIZE_ARRAY = r'\}'

t_LPAREN = r'\('
t_RPAREN = r'\)'

t_IF = r'if'
t_ELSE = r'else'
t_BEGIN = r'begin'
t_END = r'end'
t_REPEAT = r'repeat'
t_INC = r'inc'
t_DEC = r'dec'
t_TO = r'to'

t_NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'


def t_NUMBER(t):
    r'0x[0-9a-fA-f]+|\d+'
    try:
        if t.value[:2] == '0x':
            t.value = int(t.value, 16)
        else:
            t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t


# Ignored characters
t_ignore = " \t"


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    # t.lexer.skip(1)


# Build the lexer
lexer = lex.lex(debug=1)
if __name__ == '__main__':
    while True:
        try:
            line = input('cc> ')
            lexer.input(line)
            while True:
                token = lex.token()
                if not token:
                    break
                print(token)
        except:
            break
