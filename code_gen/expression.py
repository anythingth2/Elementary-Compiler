import abc
from code_gen import data_type as DataType


class Expression:

    # like extern _printf
    def eval_pre_define(self) -> str:
        return ''

    def eval_bss(self) -> str:
        return ''
    
    def eval_data(self) -> str:
        return ''

    @abc.abstractmethod
    def eval(self) -> str:
        return ''


class DefineInitailizedVariable(Expression):
    def __init__(self, var: DataType.DataType, value: DataType.ImmediateValue):
        self.var = var
        self.value = value

    def eval(self):
        return ''
    #   label:  db  "HELOELOELO"
    def eval_data(self):
        return f'{self.var.label}:\t{self.var.size}\t{self.value.eval()}'

class DefineUninitailizedVariable(Expression):
    def __init__(self, var: DataType.DataType, length:int):
        self.var = var
        self.length = length

    def eval(self):
        return ''
    #   label:  db  "HELOELOELO"
    def eval_bss(self):
        return f'{self.var.label}:\t{self.var.size}\t{self.length}'

class printText(Expression):
    def __init__(self, text: DataType.DataType):
        self.text = text

    def eval(self):
        return f"""
    push    rax
    push    rcx
    lea     rdi, [{self.text.label}]
    mov     rax, 1
    call    _printf
    pop     rcx
    pop     rax

        """
