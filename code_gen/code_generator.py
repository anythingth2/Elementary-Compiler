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

        def formatter(text): return  text.replace(' ', '\t')

        self.directives = set([formatter(' global _main')])

        for expr in self.expressions:
            self.directives.add(formatter(expr.eval_pre_define()))
            self.data.add(formatter(expr.eval_data()))
            self.bss.add(formatter(expr.eval_bss()))

        code = ''
        code += reduce(lambda acc, ele: acc + '\n' + ele, self.directives)
        code += '\n'
        code += '\tsection\t.text\n'

        for expr in self.expressions:
            code += expr.eval()
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
