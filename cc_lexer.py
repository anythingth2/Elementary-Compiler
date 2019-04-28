reserved = {
    'show'      : 'PRINT',
    'if'        : 'IF',
    'else'      : 'ELSE',
    'end'       : 'END',
    'repeat'    : 'REPEAT',
    'inc'       : 'INC',
    'dec'       : 'DEC',
    'to'        : 'TO',
    'mod'       : 'MODULO'
 }

tokens = [   
    'ID', 'NUMBER', 'STRING', 'ASSIGNMENT', 
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'L_PAREN', 'R_PAREN',
    'L_ARRAY', 'R_ARRAY', 'L_ELEM_ARRAY', 'R_ELEM_ARRAY', 'SEPARATOR', 
    'EQUALS', 'NOT_EQUALS', 'UPWARD', 'UPWARD_EQUALS', 'DOWNWARD', 'DOWNWARD_EQUALS',
    'NEWLINE'
 ] + list(reserved.values())

# Tokens
t_STRING = r'"[a-zA-Z0-9_;:=\t\r\n\'\\ ]*"'
# t_STRING = r'"[a-zA-Z0-9_]*"' # inside wrong!

t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_ASSIGNMENT = r':='
t_L_PAREN = r'\('
t_R_PAREN = r'\)'

t_EQUALS = r'='
t_NOT_EQUALS = r'!='
t_UPWARD = r'>'
t_UPWARD_EQUALS = r'>='
t_DOWNWARD = r'<'
t_DOWNWARD_EQUALS = r'<='

t_SEPARATOR = r','
t_L_ARRAY = r'\['
t_R_ARRAY = r'\]'
t_L_ELEM_ARRAY = r'\{'
t_R_ELEM_ARRAY = r'\}'

def t_ID(t):
     r'[a-zA-Z_][a-zA-Z_0-9]*'
     t.type = reserved.get(t.value, 'ID')    # check for reserved words
     return t

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

def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    return t


# Ignored characters
t_ignore = " \t"


def t_error(t):
    print("Illegal character : '{}'".format(t.value[0]))
    # t.lexer.skip(1)


# Build the lexer
import ply.lex as lex
lexer = lex.lex()


# if __name__ == '__main__':
#     while True:
#         try:
#             line = input('cc> ')
#             lexer.input(line)
#             while True:
#                 token = lex.token()
#                 if not token:
#                     break
#                 print(token)
#         except:
#             break
