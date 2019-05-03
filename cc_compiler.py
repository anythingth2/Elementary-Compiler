import cc_lexer
import cc_parser
import argparse
import os
import platform


def generate_tokens_file(filename, tokens):
    path = f'./bin/{filename}.tokens'
    with open(path, 'w') as f:
        f.write('\n'.join(tokens))
    return path


def generate_nasm_file(filename, code, variable_initializer):
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
;    dec      rdi  

 
    """

    # debugging = ''
    # for variable in variable_initializer.getAllVariable():
    #     if variable.type == 'INT':
    #         debugging += f'''
    # mov     rdi, format
    # mov     rsi,[{variable.aliase}]
    # xor     rax, rax
    # call    {prefix_precedure}printf
    # '''

    init_variables = ''
    uninit_variables = ''

    # terminal ('type', value)
    for variable in variable_initializer.getAllVariable():
        aliase = variable.aliase
        var_type = variable.type
        length = variable.length

        if variable.init_value != None:
            init_value = variable.init_value
            if var_type == 'INT':
                var_size = 'dq'
                init_variables += f'{aliase}:   {var_size}  {init_value}\n'
            elif var_type == 'STR':
                var_size = 'db'
                text = '"' + init_value.replace(r'\n', r'", 10,"') + '",10,0'
                init_variables += f'{aliase}:   {var_size}   {text}\n'
            elif var_type == 'ARR':
                var_size = 'dq'
                init_variables += f'{aliase}:   {var_size}  { ", ".join(list(map(lambda v:str(v),init_value)))}\n'
        else:
            if var_type == 'INT':
                var_size = 'resq'
            elif var_type == 'STR':
                var_size = 'resb'
            elif var_type == 'ARR':
                var_size = 'resq'
            uninit_variables += f'{aliase}:     {var_size}  {length}\n'

    footer = f"""
    pop     rbx
    ret
    section .data
format:  db  "%d",10,0
{init_variables}
    section .bss
{uninit_variables}
    """

    path = f'./bin/{filename}.nasm'
    with open(path, 'w') as f:
        f.write(header + code  + footer)
        # f.write(header + code +debugging + footer)
    return path


def compileAndRun(nasm_path):
    execute_format = 'fmacho64' if platform.system() == 'Darwin' else 'felf64'
    execute_extension = '' if platform.system() == 'Darwin' else 'elf'
    base_path = '.'.join(nasm_path.split('.')[:-1])

    command = f'nasm -{execute_format} {nasm_path} && gcc {base_path}.o -o {base_path}.{execute_extension} && ./{base_path}.{execute_extension}'
    print(command)
    os.system(command)

if __name__ == '__main__':
    _argparser = argparse.ArgumentParser()
    _argparser.add_argument('path', type=str,)
    _argparser.add_argument('-compile_run',action='store_true',default=False)
    #  open source code
    args = _argparser.parse_args()
    

    if not os.path.isfile(args.path):
        print('file not found')
        exit()

    path = args.path
    if args.compile_run:
        compileAndRun(path)
        exit()
    
    basename = os.path.basename(path)
    filename = basename.split('.')[0]
    with open(path, "r") as f:
        cc_codes = f.readlines()
        cc_codes[-1] += '\n'
        cc_codes.append('\n')

    code_tokens = []

    for line in cc_codes:
        cc_lexer.lexer.input(line)
        for token in cc_lexer.lexer:
            code_tokens.append(str(token))

        tree = cc_parser.parser.parse(line)

    generate_tokens_file(filename, code_tokens)
    nasm_path = generate_nasm_file(
        filename, cc_parser.source_code, cc_parser.variable_initializer)
    compileAndRun(nasm_path)
