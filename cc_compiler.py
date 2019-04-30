import cc_lexer
import cc_parser
import argparse
import os

# Inorder traversal : Left -> Root -> Right


def trav(root, sp):
    print(root)
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


def generate_tokens_file(filename, tokens):
    with open(f'./bin/{filename}.tokens', 'w') as f:
        f.write('\n'.join(tokens))


def generate_nasm_file(filename, code, variables):
    header = """
    global   _main
    extern   _atoi
    extern   _printf
    default  rel

    section  .text
_main:
    
    push     rbx                    ; we don't ever use this, but it is necesary
                                    ; to align the stack so we can call stuff
    dec      rdi  
    """

    debugging = ''
    for label, terminal in variables.items():
        debugging += f'''
        mov     rdi, format
        mov     rsi,[{label}]
        xor     rax, rax
        call    _printf
        '''

    footer = """
    pop     rbx
    ret
    section .data
format  db  "%d",10,0
    section .bss
    
    """
    # terminal ('type', value)
    for label, var_type in variables.items():
        # print(f'terminal {terminal}')
        # var_type = terminal[0]
      
        if var_type == 'INT':

            var_size = 'resd'
            length = 1
        elif var_type == 'STR':
            # value = value.replace('\n', '",20,"')
            # value = f'"{value}",0'
            var_size = 'resb'
            length = 1
        else:
            continue
        footer += f"""
{label}:    {var_size}  {length}

        """



    with open(f'./bin/{filename}.nasm', 'w') as f:
        f.write(header + code + debugging + footer)


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
        cc_codes = f.readlines()

    code_tokens = []

    for line in cc_codes:
        cc_lexer.lexer.input(line)
        for token in cc_lexer.lexer:
            code_tokens.append(str(token))

        tree = cc_parser.parser.parse(line)

    generate_tokens_file(filename, code_tokens)
    print(cc_parser.names)
    generate_nasm_file(filename, cc_parser.source_code, cc_parser.names)
