from functools import reduce


class CodeGenerator:

    def __init__(self):
        self.directives = ['global _main']
        self.text = ''
        self.data = []

    def compile(self):
        code = ''
        if len(self.directives) > 0:
            _directives = list(
                map(lambda direc: '\t' + direc.replace(' ', '\t'), self.directives))
            code += reduce(lambda acc, ele: acc + '\n' + ele, _directives)
        code += '\n'
        code += '\tsection\t.text'
        code += self.text
        code += '\n'
        code += '\tsection\t.data'
        if len(self.data) > 0:
            _data = list(map(lambda ele: '\t' + ele.replace(' ','\t'),self.data))
            code += reduce(lambda acc, ele:acc + '\n' + ele, _data)
        code += '\n'

        return code

    def generate(self, path='./generated.nasm'):
        with open(path, 'w', encoding='utf-8') as f:
            f.write(self.compile())
