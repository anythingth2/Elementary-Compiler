from cc_lexer import *
from cc_parser import *

# Inorder traversal : Left -> Root -> Right

def trav(root, sp):
    rng = 5
    if root != None:
        if type(root) == tuple:
            print(' '*sp*rng, root[0])
        else:
            print(' '*sp*rng, root)
        try:
            trav(root[1], sp-1)
        except:
            pass
        try:
            trav(root[2], sp+1)
        except:
            pass

if __name__ == '__main__':
    #  open source code
    try:
        code = open("cc_test_code/add.cc", "r")
        # code = open("cc_test_code/hello.cc", "r")
    except:
        print('File error : can\'t open file')

    # compile
    try:
        for line in code:
        # line = code.read()
# lexer
            lexer.input(line)
            for token in lexer:
                print(token.type, end=' ')
                # if token.value == '\n':
                #     print()
# parser
            tree = parser.parse(line)
            # print('<Tree : ', tree, ' >', sep='')
            print()
            trav(tree, int(len(tree)/2))
        # print()
    except EOFError:
        print('File error : can\'t open file')
    code.close() 