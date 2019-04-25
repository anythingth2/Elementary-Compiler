from cc_lexer import *
from cc_parser import *

if __name__ == '__main__':
    #  open source code
    try:
        code = open("cc_test_code/add.cc", "r")
        # code = open("cc_test_code/hello.cc", "r")
    except:
        print('File error : can\'t open file')

    # compile
    for line in code:
        try:
            # lexer
            lexer.input(line)
            for token in lexer:
                print(token, end=' ')
            # parser
            print('<Tree : ', parser.parse(line), ' >', sep='')
            # print()
        except EOFError:
            print('File error : End Of File')
            break
    code.close() 