from cc_lexer import *
from cc_parser import *

if __name__ == '__main__':
    file = "cc_test_code/prints.cc"
    # file = "cc_test_code/findmax.cc"
    # file = "cc_test_code/ifelse.cc"

    # open source code
    try:    
        code = open(file, "r")
    except:
        print('File error : can\'t open file \'{}\''.format(file))
        exit(0)
    
    # compile
    for line in code:
        # lexer
        lexer.input(line) 
        for token in lexer:
            print(token.type, end=' ')
        # parser
        tree = parser.parse(line) 
        print('\n<Tree : ', tree, ' >\n', sep='')

    code.close() 