from functools import reduce


class CodeGenerator:

    def __init__(self, expressions: list = None):
        self.directives = set()
        self.data = set()
        self.bss = set()
        if expressions is not None:
            self.expressions = expressions
        else:
            self.expressions = []

    def compile(self):



        self.directives = set(['\tglobal\t_main','\textern\t_printf','\tdefault\trel'])

        for expr in self.expressions:
            self.directives.add(expr.eval_pre_define())
            self.data.add(expr.eval_data())
            self.bss.add(expr.eval_bss())

        code = ''
        code += reduce(lambda acc, ele: acc + '\n' + ele, self.directives)
        code += '\n'
        code += '\tsection\t.text\n'
        code += '_main:\n'
        code += '\tpush\trbx\n'
        code += '\tdec\trdi\n'
        code += '\n'
        for expr in self.expressions:
            code += expr.eval()

        code += '\tpop\trbx\n'
        code += '\tret\n'
        code += '\n'

        code += '\tsection\t.data\n'
        code += reduce(lambda acc, ele: acc + '\n' + ele, self.data)
        code += '\n'

        code += '\tsection\t.bss\n'
        code += reduce(lambda acc, ele: acc + '\n' + ele, self.bss)

        return code

    def generate(self, path='./generated.nasm'):
        with open(path, 'w', encoding='utf-8') as f:
            f.write(self.compile())
