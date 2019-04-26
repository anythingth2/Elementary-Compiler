from cc_lexer import *
from cc_parser import *
import argparse
import os

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
    _argparser = argparse.ArgumentParser()
    _argparser.add_argument('path', type=str,)
    #  open source code
    args = _argparser.parse_args()

    if not os.path.isfile(args.path):
        print('file not found')
        exit()
    path = args.path
    basename = os.path.basename(path)
    filename = basename.split('.')[0]
    with open(path, "r") as f:
        code = f.readlines()

        # compile
    code_tokens = []
    code_asm = ''

    for line in code:
        # line = code.read()
        # lexer
        lexer.input(line)
        for token in lexer:
            print(token.type, end=' ')
            # if token.value == '\n':
            #     print()
            code_tokens.append(str(token))
# parser
        tree = parser.parse(line)

        # print()
        # if tree:
        #     trav(tree, int(len(tree)/2))

    with open(f'./bin/{filename}.tokens', 'w') as f:
        f.write('\n'.join(code_tokens))
