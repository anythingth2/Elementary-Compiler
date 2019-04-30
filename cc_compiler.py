import cc_lexer
import cc_parser
import argparse
import os
import platform

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
    path = f'./bin/{filename}.tokens'
    with open(path, 'w') as f:
        f.write('\n'.join(tokens))
    return path


def generate_nasm_file(filename, code, variables):
    prefix_precedure = '_' if platform.system() == 'Darwin' else ''
    header = f"""
    global   {prefix_precedure}main
    extern   {prefix_precedure}atoi
    extern   {prefix_precedure}printf
    default  rel

    section  .text
{prefix_precedure}main:
    
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
        call    {prefix_precedure}printf
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

    path = f'./bin/{filename}.nasm'
    with open(path, 'w') as f:
        f.write(header + code + debugging + footer)
    return path


def compileAndRun(nasm_path):
    execute_format = 'fmacho64' if platform.system() == 'Darwin' else 'felf64'
    execute_extension = '' if platform.system == 'Darwin' else 'elf'
    base_path = '.'.join(nasm_path.split('.')[:-1])
    os.system(
        f'nasm -{execute_format} {nasm_path} && gcc {base_path}.o -o {base_path}.{execute_extension} && ./{base_path}.{execute_extension}')


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
    nasm_path = generate_nasm_file(
        filename, cc_parser.source_code, cc_parser.names)
    compileAndRun(nasm_path)
